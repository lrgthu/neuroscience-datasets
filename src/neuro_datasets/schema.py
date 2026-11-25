"""Data models and NaN-safe schema validation for neuroscience dataset records."""

from __future__ import annotations

import dataclasses
import math
import re
from collections.abc import Mapping, Sequence
from typing import Any

ALLOWED_CATEGORIES: frozenset[str] = frozenset(
    {
        "human_vision_multimodal",
        "human_language_speech",
        "nhp_electrophysiology",
        "rodent_circuits_population",
        "human_resting_connectomics",
        "bci_motor_prosthetics",
        "model_organisms_connectomics",
    }
)

ALLOWED_SPECIES: frozenset[str] = frozenset(
    {
        "human",
        "macaque",
        "mouse",
        "rat",
        "marmoset",
        "zebrafish",
        "drosophila",
        "celegans",
    }
)

ALLOWED_MODALITIES: frozenset[str] = frozenset(
    {
        "fMRI_7T",
        "fMRI_3T",
        "fMRI_4T",
        "MEG",
        "EEG",
        "ECoG_iEEG",
        "sEEG",
        "Microwire_Single_Unit",
        "Utah_Array",
        "Silicon_Probe",
        "Neuropixels",
        "Two_Photon",
        "Widefield_Calcium",
        "Light_Sheet",
        "Eye_Tracking",
        "Behavior",
        "Diffusion_MRI",
        "Structural_MRI",
        "EM_Connectomics",
    }
)

ALLOWED_DOMAINS: frozenset[str] = frozenset(
    {
        "natural_images",
        "natural_movies",
        "natural_speech",
        "reading",
        "multilingual",
        "object_recognition",
        "motor_reaching",
        "speech_bci",
        "decision_making",
        "spatial_navigation",
        "working_memory",
        "mental_imagery",
        "affective_emotion",
        "multimodal",
        "resting_state",
        "videogames",
        "synthetic_ood",
        "retinotopy",
        "clinical_lifespan",
        "connectomics",
        "behavioral_similarity",
    }
)

ALLOWED_ACCESS_TIERS: frozenset[str] = frozenset(
    {"open", "registered", "credentialed"}
)

ALLOWED_FORMATS: frozenset[str] = frozenset(
    {
        "BIDS",
        "NWB",
        "NIfTI",
        "CIFTI_GIfTI",
        "HDF5_MAT",
        "FIF_MNE",
        "Zarr_NPZ",
        "TextGrid_TSV",
        "BrainVision_EDF",
        "Parquet_CSV",
        "WebDataset_Tar",
    }
)

_ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]{1,63}$")
_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@dataclasses.dataclass(frozen=True)
class ScaleSpec:
    """Quantitative and spatial/temporal resolution metrics for a dataset.

    Attributes:
        n_subjects: Positive integer count of biological subjects.
        hours_per_subject: Typical recording duration per subject in hours, or None.
        total_hours: Cumulative recording duration across subjects in hours, or None.
        n_stimuli: Count of unique images, stories, movies, or task conditions, or None.
        n_channels_or_voxels: Spatial dimensionality description (voxels/channels/units).
        sampling_rate_or_tr: Temporal sampling rate (Hz) or fMRI repetition time (TR).
    """

    n_subjects: int
    hours_per_subject: float | None
    total_hours: float | None
    n_stimuli: int | None
    n_channels_or_voxels: str
    sampling_rate_or_tr: str


@dataclasses.dataclass(frozen=True)
class AccessSpec:
    """Data licensing, hosting portal, and programmatic download metadata."""

    tier: str
    license: str
    primary_portal: str
    accession_ids: tuple[str, ...]
    urls: Mapping[str, str]
    download_cli: str


@dataclasses.dataclass(frozen=True)
class ModelingSpec:
    """Canonical evaluation splits, noise ceiling structure, and known pitfalls."""

    recommended_tasks: tuple[str, ...]
    standard_splits: str
    noise_ceiling_or_repeat_structure: str
    key_pitfalls: tuple[str, ...]


@dataclasses.dataclass(frozen=True)
class CitationSpec:
    """Verified bibliography links into references.bib."""

    primary_bib_keys: tuple[str, ...]
    related_bib_keys: tuple[str, ...]
    primary_doi_or_arxiv: str


@dataclasses.dataclass(frozen=True)
class DatasetRecord:
    """Validated single-dataset specification linking YAML metadata and Markdown card."""

    id: str
    name: str
    short_name: str
    category: str
    species: tuple[str, ...]
    modalities: tuple[str, ...]
    domains: tuple[str, ...]
    year: int
    summary_en: str
    summary_zh: str
    scale: ScaleSpec
    brain_regions: tuple[str, ...]
    data_formats: tuple[str, ...]
    access: AccessSpec
    modeling: ModelingSpec
    citations: CitationSpec
    card_path: str
    last_verified: str


def _require_non_empty_str(mapping: Mapping[str, Any], key: str, ctx: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{ctx}: expected non-empty string for {key!r}, got {value!r}")
    return value.strip()


def _require_str_tuple(
    mapping: Mapping[str, Any],
    key: str,
    ctx: str,
    allowed: frozenset[str] | None = None,
    allow_empty: bool = False,
) -> tuple[str, ...]:
    raw = mapping.get(key)
    if raw is None and allow_empty:
        return ()
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)):
        raise ValueError(f"{ctx}: expected list of strings for {key!r}, got {raw!r}")
    cleaned: list[str] = []
    for item in raw:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"{ctx}: blank or non-string item in {key!r}: {item!r}")
        token = item.strip()
        if allowed is not None and token not in allowed:
            raise ValueError(
                f"{ctx}: invalid token {token!r} in {key!r}; allowed={sorted(allowed)}"
            )
        cleaned.append(token)
    if not allow_empty and not cleaned:
        raise ValueError(f"{ctx}: {key!r} must contain at least one entry")
    return tuple(cleaned)


def _validate_optional_positive_float(
    value: Any, key: str, ctx: str, upper_bound: float
) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{ctx}: expected number or null for {key!r}, got {value!r}")
    numeric = float(value)
    if not math.isfinite(numeric) or not 0.0 < numeric <= upper_bound:
        raise ValueError(
            f"{ctx}: expected finite {key} in (0, {upper_bound}], got {value!r}"
        )
    return numeric


def _validate_positive_int(
    value: Any, key: str, ctx: str, upper_bound: int, allow_none: bool = False
) -> int | None:
    if value is None and allow_none:
        return None
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{ctx}: expected integer for {key!r}, got {value!r}")
    if not 1 <= value <= upper_bound:
        raise ValueError(
            f"{ctx}: expected integer {key} in [1, {upper_bound}], got {value!r}"
        )
    return value


def _parse_scale(raw_scale: Any, ctx: str) -> ScaleSpec:
    if not isinstance(raw_scale, Mapping):
        raise ValueError(f"{ctx}: 'scale' must be a mapping, got {raw_scale!r}")
    n_subjects = _validate_positive_int(
        raw_scale.get("n_subjects"), "scale.n_subjects", ctx, upper_bound=1_000_000
    )
    assert n_subjects is not None
    return ScaleSpec(
        n_subjects=n_subjects,
        hours_per_subject=_validate_optional_positive_float(
            raw_scale.get("hours_per_subject"),
            "scale.hours_per_subject",
            ctx,
            upper_bound=5_000.0,
        ),
        total_hours=_validate_optional_positive_float(
            raw_scale.get("total_hours"),
            "scale.total_hours",
            ctx,
            upper_bound=500_000.0,
        ),
        n_stimuli=_validate_positive_int(
            raw_scale.get("n_stimuli"),
            "scale.n_stimuli",
            ctx,
            upper_bound=100_000_000,
            allow_none=True,
        ),
        n_channels_or_voxels=_require_non_empty_str(
            raw_scale, "n_channels_or_voxels", ctx
        ),
        sampling_rate_or_tr=_require_non_empty_str(
            raw_scale, "sampling_rate_or_tr", ctx
        ),
    )


def _parse_access(raw_access: Any, ctx: str) -> AccessSpec:
    if not isinstance(raw_access, Mapping):
        raise ValueError(f"{ctx}: 'access' must be a mapping, got {raw_access!r}")
    tier = _require_non_empty_str(raw_access, "tier", ctx)
    if tier not in ALLOWED_ACCESS_TIERS:
        raise ValueError(f"{ctx}: invalid access.tier={tier!r}")
    raw_urls = raw_access.get("urls")
    if not isinstance(raw_urls, Mapping) or "homepage" not in raw_urls:
        raise ValueError(f"{ctx}: access.urls must be a mapping with 'homepage'")
    urls: dict[str, str] = {}
    for k, v in raw_urls.items():
        if not isinstance(k, str) or not isinstance(v, str) or not v.startswith("http"):
            raise ValueError(f"{ctx}: invalid URL entry {k!r}: {v!r}")
        urls[k] = v.strip()
    return AccessSpec(
        tier=tier,
        license=_require_non_empty_str(raw_access, "license", ctx),
        primary_portal=_require_non_empty_str(raw_access, "primary_portal", ctx),
        accession_ids=_require_str_tuple(
            raw_access, "accession_ids", ctx, allow_empty=True
        ),
        urls=urls,
        download_cli=_require_non_empty_str(raw_access, "download_cli", ctx),
    )


def _parse_modeling(raw_mod: Any, ctx: str) -> ModelingSpec:
    if not isinstance(raw_mod, Mapping):
        raise ValueError(f"{ctx}: 'modeling' must be a mapping, got {raw_mod!r}")
    return ModelingSpec(
        recommended_tasks=_require_str_tuple(raw_mod, "recommended_tasks", ctx),
        standard_splits=_require_non_empty_str(raw_mod, "standard_splits", ctx),
        noise_ceiling_or_repeat_structure=_require_non_empty_str(
            raw_mod, "noise_ceiling_or_repeat_structure", ctx
        ),
        key_pitfalls=_require_str_tuple(raw_mod, "key_pitfalls", ctx),
    )


def _parse_citations(raw_cit: Any, ctx: str) -> CitationSpec:
    if not isinstance(raw_cit, Mapping):
        raise ValueError(f"{ctx}: 'citations' must be a mapping, got {raw_cit!r}")
    return CitationSpec(
        primary_bib_keys=_require_str_tuple(raw_cit, "primary_bib_keys", ctx),
        related_bib_keys=_require_str_tuple(
            raw_cit, "related_bib_keys", ctx, allow_empty=True
        ),
        primary_doi_or_arxiv=_require_non_empty_str(
            raw_cit, "primary_doi_or_arxiv", ctx
        ),
    )


def parse_dataset_record(raw: Mapping[str, Any], source_label: str) -> DatasetRecord:
    """Validates a raw YAML dictionary and returns an immutable DatasetRecord.

    Args:
        raw: Parsed YAML mapping representing a single neuroscience dataset.
        source_label: File path or identifier used in diagnostic error messages.

    Returns:
        Validated frozen DatasetRecord instance.

    Raises:
        ValueError: If any field is missing, out of range, NaN/Inf, or violates
            controlled vocabularies.
    """
    dataset_id = _require_non_empty_str(raw, "id", source_label)
    if _ID_PATTERN.match(dataset_id) is None:
        raise ValueError(f"{source_label}: invalid snake_case id={dataset_id!r}")
    category = _require_non_empty_str(raw, "category", source_label)
    if category not in ALLOWED_CATEGORIES:
        raise ValueError(f"{source_label}: invalid category={category!r}")
    year_val = raw.get("year")
    if isinstance(year_val, bool) or not isinstance(year_val, int):
        raise ValueError(f"{source_label}: expected integer year, got {year_val!r}")
    if not 1990 <= year_val <= 2035:
        raise ValueError(f"{source_label}: year {year_val} outside [1990, 2035]")
    last_verified = _require_non_empty_str(raw, "last_verified", source_label)
    if _DATE_PATTERN.match(last_verified) is None:
        raise ValueError(
            f"{source_label}: last_verified must be YYYY-MM-DD, got {last_verified!r}"
        )
    return DatasetRecord(
        id=dataset_id,
        name=_require_non_empty_str(raw, "name", source_label),
        short_name=_require_non_empty_str(raw, "short_name", source_label),
        category=category,
        species=_require_str_tuple(
            raw, "species", source_label, allowed=ALLOWED_SPECIES
        ),
        modalities=_require_str_tuple(
            raw, "modalities", source_label, allowed=ALLOWED_MODALITIES
        ),
        domains=_require_str_tuple(
            raw, "domains", source_label, allowed=ALLOWED_DOMAINS
        ),
        year=year_val,
        summary_en=_require_non_empty_str(raw, "summary_en", source_label),
        summary_zh=_require_non_empty_str(raw, "summary_zh", source_label),
        scale=_parse_scale(raw.get("scale"), source_label),
        brain_regions=_require_str_tuple(raw, "brain_regions", source_label),
        data_formats=_require_str_tuple(
            raw, "data_formats", source_label, allowed=ALLOWED_FORMATS
        ),
        access=_parse_access(raw.get("access"), source_label),
        modeling=_parse_modeling(raw.get("modeling"), source_label),
        citations=_parse_citations(raw.get("citations"), source_label),
        card_path=_require_non_empty_str(raw, "card_path", source_label),
        last_verified=last_verified,
    )
