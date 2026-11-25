"""Scaffolds a new dataset YAML specification and companion Markdown card."""

from __future__ import annotations

import argparse
import datetime
import logging
import pathlib
import sys
from collections.abc import Sequence

from neuro_datasets import schema

logger = logging.getLogger(__name__)


def _parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scaffold a new neuroscience dataset YAML + Markdown card pair."
    )
    parser.add_argument("--id", required=True, help="Snake_case dataset id (e.g. hcp_ya).")
    parser.add_argument(
        "--category",
        required=True,
        choices=sorted(schema.ALLOWED_CATEGORIES),
        help="Target category directory.",
    )
    parser.add_argument("--name", required=True, help="Full dataset title.")
    parser.add_argument("--short-name", required=True, help="Short acronym/badge.")
    parser.add_argument(
        "--repo-root",
        type=pathlib.Path,
        default=pathlib.Path(__file__).resolve().parents[1],
        help="Repository root directory.",
    )
    return parser.parse_args(argv)


def _render_yaml_template(
    dataset_id: str, category: str, name: str, short_name: str, today: str
) -> str:
    card_rel = f"cards/{category}/{dataset_id}.md"
    return f"""id: {dataset_id}
name: "{name}"
short_name: "{short_name}"
category: {category}
species:
  - human
modalities:
  - fMRI_3T
domains:
  - natural_images
year: 2025
summary_en: "TODO: Concise 1-2 sentence English summary of experimental paradigm and contribution."
summary_zh: "TODO: 1-2 句中文核心概述（范式、模态与核心建模价值）。"
scale:
  n_subjects: 1
  hours_per_subject: null
  total_hours: null
  n_stimuli: null
  n_channels_or_voxels: "TODO: e.g. 2 mm isotropic whole-brain"
  sampling_rate_or_tr: "TODO: e.g. TR = 1.5 s"
brain_regions:
  - Whole-Brain
data_formats:
  - BIDS
access:
  tier: open
  license: CC0-1.0
  primary_portal: OpenNeuro
  accession_ids:
    - "OpenNeuro:dsXXXXXX"
  urls:
    homepage: "https://openneuro.org/"
  download_cli: "datalad install https://github.com/OpenNeuroDatasets/dsXXXXXX.git"
modeling:
  recommended_tasks:
    - voxelwise_encoding
  standard_splits: "TODO: Document canonical train/validation/test split."
  noise_ceiling_or_repeat_structure: "TODO: Document trial repeats and noise-ceiling formula."
  key_pitfalls:
    - "TODO: Document preprocessing, leakage, or autocorrelation pitfalls."
citations:
  primary_bib_keys:
    - TODO_verified_bib_key
  related_bib_keys: []
  primary_doi_or_arxiv: "10.XXXX/TODO"
card_path: "{card_rel}"
last_verified: "{today}"
"""


def _render_card_template(name: str, short_name: str) -> str:
    return f"""# {name} (`{short_name}`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: TODO
- **Stimulus Design & Timing**: TODO
- **Subject Cohort**: TODO

## 2. Recording Specifications & Preprocessing
- **Acquisition Hardware & Resolution**: TODO
- **Released Derivatives**: TODO

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: TODO
- **Repeat Structure & Noise Ceiling**: TODO
- **Critical Modeling Pitfalls**:
  1. TODO

## 4. Programmatic Download & Quickstart
```bash
# Verify accession and replace before committing
```

## 5. Verified Primary References
- Verify in `references.bib` via `scholarly_graph.py bib-verify` before running `scripts/build_catalog.py`.
"""


def main(argv: Sequence[str] | None = None) -> None:
    """Creates template YAML and Markdown files without overwriting existing ones."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = _parse_args(argv)
    repo_root = args.repo_root.resolve()
    yaml_path = repo_root / "datasets" / args.category / f"{args.id}.yaml"
    card_path = repo_root / "cards" / args.category / f"{args.id}.md"

    if yaml_path.exists() or card_path.exists():
        logger.error("Refusing to overwrite existing files: %s or %s", yaml_path, card_path)
        sys.exit(1)

    today = datetime.date.today().isoformat()
    yaml_path.parent.mkdir(parents=True, exist_ok=True)
    card_path.parent.mkdir(parents=True, exist_ok=True)
    yaml_path.write_text(
        _render_yaml_template(args.id, args.category, args.name, args.short_name, today),
        encoding="utf-8",
    )
    card_path.write_text(
        _render_card_template(args.name, args.short_name), encoding="utf-8"
    )
    logger.info("Scaffolded %s and %s", yaml_path, card_path)


if __name__ == "__main__":
    main()
