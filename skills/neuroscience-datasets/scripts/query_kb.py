#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "pyyaml>=6.0.1",
# ]
# ///
"""Portable zero-latency query CLI for the Neuroscience Datasets Knowledge Base."""

from __future__ import annotations

import argparse
import collections
import dataclasses
import json
import math
import os
import pathlib
import re
import sys
import urllib.request
from collections.abc import Mapping, Sequence
from typing import Any

REMOTE_CATALOG_URL = (
    "https://raw.githubusercontent.com/lrgthu/neuroscience-datasets/"
    "main/catalog/datasets.json"
)

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
class QueryConfig:
    """Validated CLI query configuration for filtering and rendering KB results."""

    query: str | None
    ids: tuple[str, ...]
    categories: tuple[str, ...]
    species: tuple[str, ...]
    modalities: tuple[str, ...]
    domains: tuple[str, ...]
    access_tiers: tuple[str, ...]
    formats: tuple[str, ...]
    min_subjects: int | None
    top_k: int
    show_pitfalls: bool
    show_cards: bool
    show_bibtex: bool
    show_stats: bool
    as_json: bool


def _split_csv_arg(values: Sequence[str] | None) -> tuple[str, ...]:
    if not values:
        return ()
    tokens: list[str] = []
    for raw in values:
        for part in raw.split(","):
            cleaned = part.strip()
            if cleaned:
                tokens.append(cleaned)
    return tuple(tokens)


def resolve_kb_root(explicit_root: pathlib.Path | None) -> pathlib.Path | None:
    """Resolves a local checkout of `neuroscience-datasets` if available on disk.

    Args:
        explicit_root: Optional `--kb-root` path supplied on the command line.

    Returns:
        Resolved repository root containing `catalog/datasets.json`, or None.
    """
    candidates: list[pathlib.Path] = []
    if explicit_root is not None:
        candidates.append(explicit_root.expanduser())
    env_root = os.environ.get("NEUROSCIENCE_DATASETS_ROOT", "").strip()
    if env_root:
        candidates.append(pathlib.Path(env_root).expanduser())

    script_file = pathlib.Path(__file__).resolve()
    skill_dir = script_file.parents[1]
    pointer_file = skill_dir / ".kb_root"
    if pointer_file.is_file():
        pointed = pointer_file.read_text(encoding="utf-8").strip()
        if pointed:
            candidates.append(pathlib.Path(pointed).expanduser())

    candidates.extend(
        [
            script_file.parents[3],
            script_file.parents[1],
            pathlib.Path.home() / "Documents" / "neuroscience-datasets",
            pathlib.Path.home() / "neuroscience-datasets",
            pathlib.Path.home() / ".local" / "share" / "neuroscience-datasets",
        ]
    )
    for cand in candidates:
        resolved = cand.resolve()
        if (resolved / "catalog" / "datasets.json").is_file():
            return resolved
    return None


def load_catalog_bundle(
    kb_root: pathlib.Path | None, allow_remote: bool = True
) -> tuple[dict[str, Any], str]:
    """Loads `datasets.json` from local KB checkout or remote GitHub fallback.

    Args:
        kb_root: Resolved local repository root, or None.
        allow_remote: Whether to fetch from GitHub when no local checkout exists.

    Returns:
        Tuple of `(catalog_dict, source_label)`.

    Raises:
        ValueError: If neither local nor remote catalog can be loaded.
    """
    if kb_root is not None:
        local_json = kb_root / "catalog" / "datasets.json"
        with local_json.open("r", encoding="utf-8") as handle:
            data: Any = json.load(handle)
        if not isinstance(data, dict) or not isinstance(data.get("datasets"), list):
            raise ValueError(f"Invalid catalog JSON at {local_json}")
        return data, str(kb_root)

    if not allow_remote:
        raise ValueError(
            "Local neuroscience-datasets KB not found and --no-remote was set."
        )
    req = urllib.request.Request(
        REMOTE_CATALOG_URL, headers={"User-Agent": "neuroscience-datasets-skill/1.0"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        remote_data: Any = json.loads(resp.read().decode("utf-8"))
    if not isinstance(remote_data, dict) or not isinstance(
        remote_data.get("datasets"), list
    ):
        raise ValueError("Invalid remote catalog payload.")
    return remote_data, REMOTE_CATALOG_URL


def load_private_mirrors(kb_root: pathlib.Path | None) -> dict[str, dict[str, Any]]:
    """Loads gitignored `local/mirrors.local.{json,yaml}` if present locally."""
    if kb_root is None:
        return {}
    json_path = kb_root / "local" / "mirrors.local.json"
    yaml_path = kb_root / "local" / "mirrors.local.yaml"
    raw_obj: Any = None
    if json_path.is_file():
        with json_path.open("r", encoding="utf-8") as handle:
            raw_obj = json.load(handle)
    elif yaml_path.is_file():
        try:
            import yaml  # type: ignore[import-untyped]

            with yaml_path.open("r", encoding="utf-8") as handle:
                raw_obj = yaml.safe_load(handle)
        except ImportError:
            raw_obj = None
    if not isinstance(raw_obj, Mapping):
        return {}
    mirrors = raw_obj.get("mirrors", raw_obj)
    if not isinstance(mirrors, Mapping):
        return {}
    return {str(k): dict(v) for k, v in mirrors.items() if isinstance(v, Mapping)}


def _matches_facets(entry: Mapping[str, Any], cfg: QueryConfig) -> bool:
    if cfg.categories:
        cat = str(entry.get("category", "")).lower()
        if not any(c.lower() in cat for c in cfg.categories):
            return False
    if cfg.species:
        sp_set = {str(s).lower() for s in entry.get("species", ())}
        if not any(s.lower() in sp_set for s in cfg.species):
            return False
    if cfg.modalities:
        mods = [str(m).lower() for m in entry.get("modalities", ())]
        if not any(any(r.lower() in mod for mod in mods) for r in cfg.modalities):
            return False
    if cfg.domains:
        doms = [str(d).lower() for d in entry.get("domains", ())]
        if not any(any(r.lower() in dom for dom in doms) for r in cfg.domains):
            return False
    if cfg.access_tiers:
        tier = str(entry.get("access", {}).get("tier", "")).lower()
        if tier not in {t.lower() for t in cfg.access_tiers}:
            return False
    if cfg.formats:
        fmts = [str(f).lower() for f in entry.get("data_formats", ())]
        if not any(any(r.lower() in fmt for fmt in fmts) for r in cfg.formats):
            return False
    if cfg.min_subjects is not None:
        if int(entry.get("scale", {}).get("n_subjects", 0)) < cfg.min_subjects:
            return False
    return True


@dataclasses.dataclass(frozen=True)
class _EntryBlobs:
    """Pre-lowercased field blobs for fast query scoring."""

    ds_id: str
    short_name: str
    species_tokens: frozenset[str]
    modality_blob: str
    acc_blob: str
    high_blob: str
    mid_blob: str
    pit_blob: str
    card_blob: str


def _build_entry_blobs(entry: Mapping[str, Any]) -> _EntryBlobs:
    species_tokens = frozenset(str(x).lower() for x in entry.get("species", ()))
    modality_blob = " ".join(str(x).lower() for x in entry.get("modalities", ()))
    modeling = entry.get("modeling", {})
    return _EntryBlobs(
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


def _score_single_variant(blobs: _EntryBlobs, variant: str) -> float:
    sc = 0.0
    if variant in (blobs.ds_id, blobs.short_name):
        sc += 30.0
    elif (
        _has_term(blobs.ds_id, variant)
        or _has_term(blobs.short_name, variant)
        or _has_term(blobs.acc_blob, variant)
    ):
        sc += 15.0
    if variant in blobs.species_tokens or _has_term(blobs.modality_blob, variant):
        sc += 22.0
    if _has_term(blobs.high_blob, variant):
        sc += 8.0
    if _has_term(blobs.mid_blob, variant):
        sc += 5.0
    if _has_term(blobs.pit_blob, variant):
        sc += 3.0
    if _has_term(blobs.card_blob, variant):
        sc += 1.5
    return sc


def _score_entry(
    entry: Mapping[str, Any], token_groups: Sequence[tuple[str, ...]]
) -> float:
    if not token_groups:
        year = int(entry.get("year", 2000))
        n_subj = max(1, int(entry.get("scale", {}).get("n_subjects", 1)))
        return float(year - 1990) + 0.25 * math.log10(float(n_subj))

    blobs = _build_entry_blobs(entry)
    matched_groups = 0
    total_score = 0.0
    for synonyms in token_groups:
        best = max(_score_single_variant(blobs, v) for v in synonyms)
        if best > 0.0:
            matched_groups += 1
            total_score += best

    min_req = (
        1 if len(token_groups) == 1 else max(1, math.ceil(0.6 * len(token_groups)))
    )
    if matched_groups < min_req:
        return 0.0
    if matched_groups == len(token_groups):
        total_score += 20.0
    return total_score


def execute_search(
    catalog: Mapping[str, Any],
    cfg: QueryConfig,
    mirrors: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Executes multi-facet filtering and relevance ranking over catalog entries."""
    if not 1 <= cfg.top_k <= 500:
        raise ValueError(f"--top-k must be in [1, 500], got {cfg.top_k}")
    datasets = catalog.get("datasets", ())
    if cfg.ids:
        by_id = {str(d["id"]): d for d in datasets if isinstance(d, Mapping)}
        picked: list[dict[str, Any]] = []
        for req_id in cfg.ids:
            norm = req_id.lower()
            if norm in by_id:
                picked.append(
                    {
                        "score": 100.0,
                        "dataset": by_id[norm],
                        "local_mirror": mirrors.get(norm),
                    }
                )
        return picked[: cfg.top_k]

    token_groups: list[tuple[str, ...]] = []
    if cfg.query:
        raw_toks = [
            t for t in _TOKEN_RE.findall(cfg.query.lower()) if t not in _STOPWORDS
        ]
        if not raw_toks and cfg.query.strip():
            raw_toks = [cfg.query.strip().lower()]
        token_groups = [SYNONYM_MAP.get(t, (t,)) for t in raw_toks]

    scored: list[dict[str, Any]] = []
    for item in datasets:
        if not isinstance(item, Mapping) or not _matches_facets(item, cfg):
            continue
        score = _score_entry(item, token_groups)
        if token_groups and score <= 0.0:
            continue
        ds_id = str(item.get("id", ""))
        scored.append(
            {"score": round(score, 2), "dataset": item, "local_mirror": mirrors.get(ds_id)}
        )

    scored.sort(
        key=lambda row: (
            -float(row["score"]),
            -int(row["dataset"].get("year", 0)),
            str(row["dataset"].get("id", "")),
        )
    )
    return scored[: cfg.top_k]


def _render_stats(
    catalog: Mapping[str, Any],
    source_label: str,
    mirrors: Mapping[str, Mapping[str, Any]],
) -> str:
    datasets = catalog.get("datasets", ())
    cats = collections.Counter(str(d.get("category", "")) for d in datasets)
    species = collections.Counter(
        str(s) for d in datasets for s in d.get("species", ())
    )
    mods = collections.Counter(
        str(m) for d in datasets for m in d.get("modalities", ())
    )
    lines = [
        "# Neuroscience Datasets Knowledge Base — Live Inventory",
        f"- Source: `{source_label}`",
        f"- Total Verified Datasets: `{len(datasets)}` (Input SHA-256: `{str(catalog.get('input_sha256', ''))[:12]}...`)",
        f"- Configured Private Local Mirrors: `{len(mirrors)}`",
        "- Categories: "
        + ", ".join(f"`{k}` ({v})" for k, v in cats.most_common()),
        "- Species: "
        + ", ".join(f"`{k}` ({v})" for k, v in species.most_common()),
        "- Top Modalities: "
        + ", ".join(f"`{k}` ({v})" for k, v in mods.most_common(12)),
    ]
    return "\n".join(lines)


def _extract_bibtex_text(results: Sequence[Mapping[str, Any]]) -> str:
    seen: set[str] = set()
    blocks: list[str] = []
    for row in results:
        raw_bib = str(row["dataset"].get("resolved_bibtex", "")).strip()
        for stanza in re.split(r"\n\s*\n(?=@)", raw_bib):
            clean = stanza.strip()
            if clean and clean.splitlines()[0].strip() not in seen:
                seen.add(clean.splitlines()[0].strip())
                blocks.append(clean)
    return "\n\n".join(blocks)


def _append_detail_sections(
    lines: list[str], results: Sequence[Mapping[str, Any]], cfg: QueryConfig
) -> None:
    if cfg.show_pitfalls:
        lines.append("\n## Canonical Splits, Noise Ceilings & Evaluation Pitfalls")
        for row in results:
            ds = row["dataset"]
            mod = ds.get("modeling", {})
            lines.append(f"\n### `{ds['id']}` — {ds['name']}")
            lines.append(f"- **Standard Splits**: {mod.get('standard_splits')}")
            lines.append(
                f"- **Noise Ceiling / Repeat Structure**: "
                f"{mod.get('noise_ceiling_or_repeat_structure')}"
            )
            lines.append("- **Key Pitfalls & Confound Guards**:")
            for pit in mod.get("key_pitfalls", ()):
                lines.append(f"  - {pit}")

    if cfg.show_cards:
        lines.append("\n## Deep Technical Cards & Access CLI")
        for row in results:
            ds = row["dataset"]
            acc = ds.get("access", {})
            lines.append(f"\n---\n### Card: `{ds['id']}` (`{ds.get('card_path')}`)")
            if row.get("local_mirror"):
                lines.append(f"- **Private Local Mirror**: `{row['local_mirror']}`")
            lines.append(f"- **Download CLI**: `{acc.get('download_cli')}`")
            lines.append(
                f"- **Primary BibTeX Keys**: "
                f"`{', '.join(ds.get('citations', {}).get('primary_bib_keys', ()))}`\n"
            )
            lines.append(str(ds.get("card_markdown", "")).strip())


def _render_text_results(
    results: Sequence[Mapping[str, Any]], cfg: QueryConfig, source_label: str
) -> str:
    if not results:
        return f"No datasets matched in `{source_label}`."
    if cfg.show_bibtex:
        return _extract_bibtex_text(results)

    lines = [
        f"Matched `{len(results)}` dataset(s) from `{source_label}`:\n",
        "| ID | Short Name | Year | Species / Modalities | Scale | Access & Portal | Ref |",
        "| :--- | :--- | :---: | :--- | :--- | :--- | :--- |",
    ]
    for row in results:
        ds = row["dataset"]
        sp = "/".join(ds.get("species", ()))
        mods = ", ".join(ds.get("modalities", ())[:3])
        scale = ds.get("scale", {})
        hrs = (
            f", {scale['hours_per_subject']:g}h/subj"
            if scale.get("hours_per_subject") is not None
            else ""
        )
        mirror_tag = " [LOCAL MIRROR]" if row.get("local_mirror") else ""
        acc = ds.get("access", {})
        cit = ds.get("citations", {})
        lines.append(
            f"| `{ds['id']}` | **{ds['short_name']}**{mirror_tag} | {ds['year']} | "
            f"{sp} · `{mods}` | `N={scale.get('n_subjects')}`{hrs} | "
            f"`{acc.get('tier')}` · {acc.get('primary_portal')} | "
            f"`{cit.get('primary_doi_or_arxiv')}` |"
        )
    _append_detail_sections(lines, results, cfg)
    return "\n".join(lines)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Query the curated Neuroscience Datasets Knowledge Base."
    )
    parser.add_argument("--kb-root", type=pathlib.Path, default=None)
    parser.add_argument("--no-remote", action="store_true")
    parser.add_argument("-q", "--query", type=str, default=None)
    parser.add_argument("--ids", action="append", default=None)
    parser.add_argument("--category", action="append", default=None)
    parser.add_argument("--species", action="append", default=None)
    parser.add_argument("--modality", action="append", default=None)
    parser.add_argument("--domain", action="append", default=None)
    parser.add_argument("--access", action="append", default=None)
    parser.add_argument("--format", action="append", default=None)
    parser.add_argument("--min-subjects", type=int, default=None)
    parser.add_argument("--top-k", type=int, default=None)
    parser.add_argument("--pitfalls", action="store_true")
    parser.add_argument("--show-cards", action="store_true")
    parser.add_argument("--bibtex", action="store_true")
    parser.add_argument("--stats", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def _parse_query_config(args: argparse.Namespace) -> QueryConfig:
    default_top_k = 5 if args.show_cards and not args.ids else 15
    top_k = args.top_k if args.top_k is not None else default_top_k
    return QueryConfig(
        query=args.query,
        ids=_split_csv_arg(args.ids),
        categories=_split_csv_arg(args.category),
        species=_split_csv_arg(args.species),
        modalities=_split_csv_arg(args.modality),
        domains=_split_csv_arg(args.domain),
        access_tiers=_split_csv_arg(args.access),
        formats=_split_csv_arg(args.format),
        min_subjects=args.min_subjects,
        top_k=top_k,
        show_pitfalls=bool(args.pitfalls),
        show_cards=bool(args.show_cards),
        show_bibtex=bool(args.bibtex),
        show_stats=bool(args.stats),
        as_json=bool(args.json),
    )


def _format_json_results(
    results: Sequence[Mapping[str, Any]], cfg: QueryConfig, source_label: str
) -> str:
    out_items = []
    for row in results:
        item_copy = dict(row["dataset"])
        if not cfg.show_cards:
            item_copy.pop("card_markdown", None)
        if not cfg.show_bibtex:
            item_copy.pop("resolved_bibtex", None)
        out_items.append(
            {
                "score": row["score"],
                "local_mirror": row["local_mirror"],
                "dataset": item_copy,
            }
        )
    return (
        json.dumps(
            {"source": source_label, "count": len(out_items), "results": out_items},
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    )


def main(argv: Sequence[str] | None = None) -> None:
    """CLI entrypoint for querying datasets, pitfalls, cards, and BibTeX."""
    args = _build_parser().parse_args(argv)
    cfg = _parse_query_config(args)
    kb_root = resolve_kb_root(args.kb_root)
    catalog, source_label = load_catalog_bundle(
        kb_root, allow_remote=not args.no_remote
    )
    mirrors = load_private_mirrors(kb_root)

    if cfg.show_stats:
        if cfg.as_json:
            payload = {
                "source": source_label,
                "dataset_count": catalog.get("dataset_count"),
                "input_sha256": catalog.get("input_sha256"),
                "mirror_count": len(mirrors),
            }
            sys.stdout.write(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
        else:
            sys.stdout.write(_render_stats(catalog, source_label, mirrors) + "\n")
        return

    results = execute_search(catalog, cfg, mirrors)
    if cfg.as_json:
        sys.stdout.write(_format_json_results(results, cfg, source_label))
        return
    sys.stdout.write(_render_text_results(results, cfg, source_label) + "\n")


if __name__ == "__main__":
    main()
