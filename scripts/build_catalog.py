"""CLI driver to validate dataset specs, query entries, and build catalog artifacts."""

from __future__ import annotations

import argparse
import json
import logging
import pathlib
import sys
from collections.abc import Sequence

from neuro_datasets import exporter
from neuro_datasets import loader
from neuro_datasets import schema

logger = logging.getLogger(__name__)


def _parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate neuroscience datasets and build catalog/README/Pages files."
    )
    parser.add_argument(
        "--repo-root",
        type=pathlib.Path,
        default=pathlib.Path(__file__).resolve().parents[1],
        help="Path to the neuroscience-datasets repository root.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify generated files match repository inputs without writing.",
    )
    parser.add_argument(
        "--query",
        type=str,
        default=None,
        help="Filter and print matching datasets instead of building.",
    )
    parser.add_argument(
        "--modality",
        type=str,
        default=None,
        help="Optional modality filter (e.g., fMRI_7T, MEG, ECoG_iEEG, Neuropixels).",
    )
    parser.add_argument(
        "--species",
        type=str,
        default=None,
        help="Optional species filter (e.g., human, macaque, mouse).",
    )
    return parser.parse_args(argv)


def _filter_records(
    records: Sequence[schema.DatasetRecord],
    query: str | None,
    modality: str | None,
    species: str | None,
) -> list[schema.DatasetRecord]:
    matched: list[schema.DatasetRecord] = []
    q_lower = query.lower().strip() if query is not None else None
    mod_lower = modality.lower().strip() if modality is not None else None
    sp_lower = species.lower().strip() if species is not None else None

    for rec in records:
        if mod_lower is not None and not any(
            mod_lower in m.lower() for m in rec.modalities
        ):
            continue
        if sp_lower is not None and not any(
            sp_lower == s.lower() for s in rec.species
        ):
            continue
        if q_lower is not None:
            haystack = " ".join(
                [
                    rec.id,
                    rec.short_name,
                    rec.name,
                    rec.summary_en,
                    rec.summary_zh,
                    " ".join(rec.domains),
                    " ".join(rec.brain_regions),
                    " ".join(rec.access.accession_ids),
                ]
            ).lower()
            if q_lower not in haystack:
                continue
        matched.append(rec)
    return matched


def _compute_expected_outputs(
    catalog: loader.LoadedCatalog, repo_root: pathlib.Path
) -> dict[pathlib.Path, str]:
    outputs: dict[pathlib.Path, str] = {
        repo_root / "catalog" / "datasets.json": exporter.render_datasets_json(catalog),
        repo_root / "catalog" / "datasets.csv": exporter.render_tidy_csv(
            catalog.records
        ),
        repo_root / "docs" / "catalog_data.js": exporter.render_pages_js(catalog),
    }
    readme_en = repo_root / "README.md"
    if readme_en.is_file():
        outputs[readme_en] = exporter.splice_readme_block(
            readme_en.read_text(encoding="utf-8"),
            exporter.render_markdown_catalog(catalog.records, lang="en"),
        )
    readme_zh = repo_root / "README_zh.md"
    if readme_zh.is_file():
        outputs[readme_zh] = exporter.splice_readme_block(
            readme_zh.read_text(encoding="utf-8"),
            exporter.render_markdown_catalog(catalog.records, lang="zh"),
        )
    return outputs


def _run_build_or_check(repo_root: pathlib.Path, check_only: bool) -> int:
    catalog = loader.load_repository_catalog(repo_root)
    expected_outputs = _compute_expected_outputs(catalog, repo_root)
    if check_only:
        drifted: list[str] = []
        for out_path, expected_text in expected_outputs.items():
            if not out_path.is_file():
                drifted.append(f"missing: {out_path.relative_to(repo_root)}")
                continue
            actual_text = out_path.read_text(encoding="utf-8")
            if actual_text != expected_text:
                drifted.append(f"out-of-sync: {out_path.relative_to(repo_root)}")
        if drifted:
            logger.error("Catalog drift detected: %s", ", ".join(drifted))
            return 1
        logger.info(
            "OK: %d datasets validated and all generated artifacts are in sync.",
            len(catalog.records),
        )
        return 0

    for out_path, expected_text in expected_outputs.items():
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(expected_text, encoding="utf-8")
    prov_path = repo_root / "catalog" / "datasets_provenance.json"
    prov_dict = exporter.build_provenance_dict(catalog, repo_root)
    prov_path.write_text(
        json.dumps(prov_dict, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    logger.info(
        "Built catalog for %d datasets (%d BibTeX keys).",
        len(catalog.records),
        len(catalog.bibtex_by_key),
    )
    return 0


def main(argv: Sequence[str] | None = None) -> None:
    """Entrypoint for validating, querying, and building the dataset catalog."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = _parse_args(argv)
    repo_root = args.repo_root.resolve()

    if (
        args.query is not None
        or args.modality is not None
        or args.species is not None
    ):
        catalog = loader.load_repository_catalog(repo_root)
        matches = _filter_records(
            catalog.records, args.query, args.modality, args.species
        )
        for rec in matches:
            mods = ",".join(rec.modalities)
            sys.stdout.write(
                f"{rec.id:<24} | {rec.short_name:<16} | { '/'.join(rec.species):<8} "
                f"| N={rec.scale.n_subjects:<4} | {mods} | {rec.card_path}\n"
            )
        logger.info("Matched %d / %d datasets.", len(matches), len(catalog.records))
        return

    exit_code = _run_build_or_check(repo_root, check_only=args.check)
    if exit_code != 0:
        sys.exit(exit_code)


if __name__ == "__main__":
    main()
