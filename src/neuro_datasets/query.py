"""Multi-facet search, relevance ranking, and protocol inspection for dataset catalogs."""

from __future__ import annotations

import dataclasses
import json
import math
import pathlib
import re
from collections.abc import Mapping, Sequence
from typing import Any

import yaml

SYNONYM_MAP: Mapping[str, tuple[str, ...]] = {
    "fmri": ("fmri", "fmri_7t", "fmri_3t", "fmri_4t"),
    "ieeg": ("ieeg", "ecog_ieeg", "seeg", "intracranial", "ecog"),
    "ecog": ("ecog", "ecog_ieeg", "intracranial"),
    "nhp": ("nhp", "macaque", "marmoset", "primate"),
    "monkey": ("monkey", "macaque", "marmoset", "primate"),
    "primate": ("primate", "macaque", "marmoset"),
    "rodent": ("rodent", "mouse", "rat"),
    "2p": ("2p", "two_photon", "2-photon", "calcium"),
    "calcium": ("calcium", "two_photon", "widefield_calcium", "light_sheet"),
    "em": ("em", "em_connectomics", "connectomics", "synaptic"),
    "connectome": ("connectome", "connectomics", "em_connectomics"),
    "feedback": ("feedback", "recurrent"),
    "recurrent": ("recurrent", "feedback"),
    "ephys": (
        "ephys",
        "neuropixels",
        "utah_array",
        "silicon_probe",
        "microwire_single_unit",
    ),
    "spikes": (
        "spikes",
        "spiking",
        "neuropixels",
        "utah_array",
        "silicon_probe",
        "microwire_single_unit",
    ),
}

_STOPWORDS: frozenset[str] = frozenset(
    {"a", "an", "and", "for", "in", "of", "on", "or", "the", "to", "with", "dataset"}
)
_TOKEN_RE = re.compile(r"[a-z0-9_+.-]+")


@dataclasses.dataclass(frozen=True)
class SearchFilter:
    """Typed filter criteria for querying compiled neuroscience dataset records.

    Attributes:
        query: Optional free-text search query.
        ids: Exact dataset IDs to retrieve, preserving requested order if non-empty.
        categories: Allowed category tokens (case-insensitive).
        species: Allowed species tokens (case-insensitive).
        modalities: Allowed modality substrings/tokens (case-insensitive).
        domains: Allowed domain substrings/tokens (case-insensitive).
        access_tiers: Allowed access tiers (`open`, `registered`, `credentialed`).
        formats: Allowed data format substrings/tokens (case-insensitive).
        min_subjects: Minimum biological subject count, or None.
        top_k: Maximum number of records to return in `[1, 500]`.
    """

    query: str | None = None
    ids: tuple[str, ...] = ()
    categories: tuple[str, ...] = ()
    species: tuple[str, ...] = ()
    modalities: tuple[str, ...] = ()
    domains: tuple[str, ...] = ()
    access_tiers: tuple[str, ...] = ()
    formats: tuple[str, ...] = ()
    min_subjects: int | None = None
    top_k: int = 15


@dataclasses.dataclass(frozen=True)
class ScoredDataset:
    """Ranked dataset entry paired with relevance score and optional local mirror info."""

    score: float
    entry: Mapping[str, Any]
    local_mirror: Mapping[str, Any] | None = None


def load_compiled_catalog(catalog_json_path: pathlib.Path) -> dict[str, Any]:
    """Loads the compiled `catalog/datasets.json` bundle from disk.

    Args:
        catalog_json_path: Path to `datasets.json`.

    Returns:
        Parsed top-level JSON dictionary with `datasets` list.

    Raises:
        ValueError: If the file does not exist or lacks a valid `datasets` list.
    """
    if not catalog_json_path.is_file():
        raise ValueError(f"Compiled catalog not found: {catalog_json_path}")
    with catalog_json_path.open("r", encoding="utf-8") as handle:
        payload: Any = json.load(handle)
    if not isinstance(payload, dict) or not isinstance(payload.get("datasets"), list):
        raise ValueError(f"Malformed catalog JSON in {catalog_json_path}")
    return payload


def load_local_mirrors(repo_root: pathlib.Path | None) -> dict[str, dict[str, Any]]:
    """Loads optional gitignored `local/mirrors.local.{yaml,json}` cache metadata.

    Args:
        repo_root: Local repository root directory, or None when running remotely.

    Returns:
        Mapping from dataset ID to private local mirror dictionary.
    """
    if repo_root is None:
        return {}
    json_mirror = repo_root / "local" / "mirrors.local.json"
    yaml_mirror = repo_root / "local" / "mirrors.local.yaml"
    raw_obj: Any = None
    if json_mirror.is_file():
        with json_mirror.open("r", encoding="utf-8") as handle:
            raw_obj = json.load(handle)
    elif yaml_mirror.is_file():
        with yaml_mirror.open("r", encoding="utf-8") as handle:
            raw_obj = yaml.safe_load(handle)
    if not isinstance(raw_obj, Mapping):
        return {}
    mirrors = raw_obj.get("mirrors", raw_obj)
    if not isinstance(mirrors, Mapping):
        return {}
    return {
        str(k): dict(v) for k, v in mirrors.items() if isinstance(v, Mapping)
    }


def _tokenize_query(query: str) -> list[tuple[str, ...]]:
    raw_tokens = [
        tok for tok in _TOKEN_RE.findall(query.lower()) if tok not in _STOPWORDS
    ]
    if not raw_tokens and query.strip():
        raw_tokens = [query.strip().lower()]
    groups: list[tuple[str, ...]] = []
    for tok in raw_tokens:
        groups.append(SYNONYM_MAP.get(tok, (tok,)))
    return groups


def _matches_facets(entry: Mapping[str, Any], spec: SearchFilter) -> bool:
    if spec.categories:
        cat = str(entry.get("category", "")).lower()
        if not any(c.lower() in cat for c in spec.categories):
            return False
    if spec.species:
        sp_set = {str(s).lower() for s in entry.get("species", ())}
        if not any(s.lower() in sp_set for s in spec.species):
            return False
    if spec.modalities:
        mods = [str(m).lower() for m in entry.get("modalities", ())]
        if not any(
            any(req.lower() in mod for mod in mods) for req in spec.modalities
        ):
            return False
    if spec.domains:
        doms = [str(d).lower() for d in entry.get("domains", ())]
        if not any(any(req.lower() in dom for dom in doms) for req in spec.domains):
            return False
    if spec.access_tiers:
        tier = str(entry.get("access", {}).get("tier", "")).lower()
        if tier not in {t.lower() for t in spec.access_tiers}:
            return False
    if spec.formats:
        fmts = [str(f).lower() for f in entry.get("data_formats", ())]
        if not any(any(req.lower() in fmt for fmt in fmts) for req in spec.formats):
            return False
    if spec.min_subjects is not None:
        n_subj = int(entry.get("scale", {}).get("n_subjects", 0))
        if n_subj < spec.min_subjects:
            return False
    return True


@dataclasses.dataclass(frozen=True)
class _IndexedBlobs:
    """Pre-lowercased field blobs for scoring a single dataset entry."""

    ds_id: str
    short_name: str
    species_tokens: frozenset[str]
    modality_blob: str
    acc_blob: str
    high_blob: str
    mid_blob: str
    pit_blob: str
    card_blob: str


def _build_indexed_blobs(entry: Mapping[str, Any]) -> _IndexedBlobs:
    species_tokens = frozenset(str(x).lower() for x in entry.get("species", ()))
    modality_blob = " ".join(str(x).lower() for x in entry.get("modalities", ()))
    modeling = entry.get("modeling", {})
    return _IndexedBlobs(
        ds_id=str(entry.get("id", "")).lower(),
        short_name=str(entry.get("short_name", "")).lower(),
        species_tokens=species_tokens,
        modality_blob=modality_blob,
        acc_blob=" ".join(
            str(x).lower() for x in entry.get("access", {}).get("accession_ids", ())
        ),
        high_blob=" ".join(
            [
                str(entry.get("name", "")).lower(),
                " ".join(str(x).lower() for x in entry.get("domains", ())),
                modality_blob,
                " ".join(species_tokens),
                " ".join(str(x).lower() for x in entry.get("brain_regions", ())),
            ]
        ),
        mid_blob=" ".join(
            [
                str(entry.get("summary_en", "")).lower(),
                str(entry.get("summary_zh", "")).lower(),
                " ".join(str(x).lower() for x in modeling.get("recommended_tasks", ())),
            ]
        ),
        pit_blob=" ".join(
            [
                str(modeling.get("standard_splits", "")).lower(),
                " ".join(str(x).lower() for x in modeling.get("key_pitfalls", ())),
            ]
        ),
        card_blob=str(entry.get("card_markdown", "")).lower(),
    )


def _has_term(text_blob: str, variant: str) -> bool:
    if len(variant) <= 4:
        return variant in set(re.findall(r"[a-z0-9]+", text_blob))
    return variant in text_blob


def _score_variant(blobs: _IndexedBlobs, variant: str) -> float:
    score = 0.0
    if variant in (blobs.ds_id, blobs.short_name):
        score += 30.0
    elif (
        _has_term(blobs.ds_id, variant)
        or _has_term(blobs.short_name, variant)
        or _has_term(blobs.acc_blob, variant)
    ):
        score += 15.0
    if variant in blobs.species_tokens or _has_term(blobs.modality_blob, variant):
        score += 22.0
    if _has_term(blobs.high_blob, variant):
        score += 8.0
    if _has_term(blobs.mid_blob, variant):
        score += 5.0
    if _has_term(blobs.pit_blob, variant):
        score += 3.0
    if _has_term(blobs.card_blob, variant):
        score += 1.5
    return score


def _score_entry(
    entry: Mapping[str, Any], token_groups: Sequence[tuple[str, ...]]
) -> float:
    if not token_groups:
        year = int(entry.get("year", 2000))
        n_subj = max(1, int(entry.get("scale", {}).get("n_subjects", 1)))
        return float(year - 1990) + 0.25 * math.log10(float(n_subj))

    blobs = _build_indexed_blobs(entry)
    matched_groups = 0
    total_score = 0.0
    for synonyms in token_groups:
        group_score = max(_score_variant(blobs, v) for v in synonyms)
        if group_score > 0.0:
            matched_groups += 1
            total_score += group_score

    min_required = (
        1 if len(token_groups) == 1 else max(1, math.ceil(0.6 * len(token_groups)))
    )
    if matched_groups < min_required:
        return 0.0
    if matched_groups == len(token_groups):
        total_score += 20.0
    return total_score


def search_catalog(
    catalog_payload: Mapping[str, Any],
    spec: SearchFilter,
    mirrors: Mapping[str, Mapping[str, Any]] | None = None,
) -> list[ScoredDataset]:
    """Filters and ranks compiled dataset entries according to `SearchFilter`.

    Args:
        catalog_payload: Parsed `catalog/datasets.json` dictionary.
        spec: Validated `SearchFilter` criteria.
        mirrors: Optional private local mirror overlay keyed by dataset ID.

    Returns:
        Ordered list of `ScoredDataset` matches up to `spec.top_k`.

    Raises:
        ValueError: If `spec.top_k` or `spec.min_subjects` is out of bounds.
    """
    if isinstance(spec.top_k, bool) or not 1 <= spec.top_k <= 500:
        raise ValueError(f"top_k must be in [1, 500], got {spec.top_k!r}")
    if spec.min_subjects is not None and (
        isinstance(spec.min_subjects, bool) or not 1 <= spec.min_subjects <= 10_000_000
    ):
        raise ValueError(f"min_subjects out of range: {spec.min_subjects!r}")

    mirror_map = mirrors if mirrors is not None else {}
    datasets = catalog_payload.get("datasets", ())
    if spec.ids:
        by_id = {str(item["id"]): item for item in datasets if isinstance(item, Mapping)}
        selected: list[ScoredDataset] = []
        for raw_id in spec.ids:
            norm_id = raw_id.strip().lower()
            if norm_id in by_id:
                selected.append(
                    ScoredDataset(
                        score=100.0,
                        entry=by_id[norm_id],
                        local_mirror=mirror_map.get(norm_id),
                    )
                )
        return selected[: spec.top_k]

    token_groups = _tokenize_query(spec.query) if spec.query else []
    ranked: list[ScoredDataset] = []
    for item in datasets:
        if not isinstance(item, Mapping) or not _matches_facets(item, spec):
            continue
        score = _score_entry(item, token_groups)
        if token_groups and score <= 0.0:
            continue
        ds_id = str(item.get("id", ""))
        ranked.append(
            ScoredDataset(
                score=score,
                entry=item,
                local_mirror=mirror_map.get(ds_id),
            )
        )

    ranked.sort(
        key=lambda m: (
            -m.score,
            -int(m.entry.get("year", 0)),
            str(m.entry.get("id", "")),
        )
    )
    return ranked[: spec.top_k]


def collect_unique_bibtex(matches: Sequence[ScoredDataset]) -> str:
    """Deduplicates and formats resolved BibTeX blocks across matched datasets.

    Args:
        matches: Sequence of ranked `ScoredDataset` results.

    Returns:
        Concatenated unique BibTeX stanzas separated by blank lines.
    """
    seen_headers: set[str] = set()
    blocks: list[str] = []
    for item in matches:
        raw_bib = str(item.entry.get("resolved_bibtex", "")).strip()
        if not raw_bib:
            continue
        for stanza in re.split(r"\n\s*\n(?=@)", raw_bib):
            clean = stanza.strip()
            if not clean:
                continue
            header = clean.splitlines()[0].strip()
            if header not in seen_headers:
                seen_headers.add(header)
                blocks.append(clean)
    return "\n\n".join(blocks)
