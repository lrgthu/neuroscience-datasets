# Contributing & Dataset Curation Checklist

Thank you for helping expand and maintain the **Neuroscience Datasets Knowledge Base**!

## Adding or Updating a Dataset

1. **Scaffold the Entry**:
   ```bash
   uv run python scripts/new_dataset.py \
     --id <snake_case_id> \
     --category <category> \
     --name "<Full Dataset Title>" \
     --short-name "<ShortBadge>"
   ```
2. **Verify Primary Publications & Accessions**:
   - Add canonical BibTeX entries to `references.bib` (prefer peer-reviewed journal/conference records over preprints when published, while keeping `eprint` if helpful).
   - Double-check exact subject count (`scale.n_subjects`), resolution (`scale.sampling_rate_or_tr`), license (`access.license`), and copy-pasteable download command (`access.download_cli`).
3. **Document Evaluation Rigor (`modeling` & `cards/`)**:
   - Specify the community-standard train/test split (`modeling.standard_splits`).
   - Specify trial repetition structure and noise-ceiling formula (`modeling.noise_ceiling_or_repeat_structure`).
   - Highlight concrete data-leakage, preprocessing, or statistical pitfalls (`modeling.key_pitfalls`).
4. **Rebuild & Run Full Verification**:
   ```bash
   uv run python scripts/build_catalog.py
   uv run ruff check src scripts tests
   uv run pytest -v
   uv run python scripts/build_catalog.py --check
   ```
