# Agent Operating & Maintenance Rules (`neuroscience-datasets`)

Whenever an AI agent (Google Antigravity, Claude Code, Codex CLI, Gemini CLI, or Cursor) queries, adds, or updates datasets in this repository, enforce the following non-negotiable standards:

## 1. Zero-Hallucination Bibliographic & Accession Integrity
1. **Never guess DOIs, arXiv IDs, author lists, OpenNeuro `ds*` IDs, DANDI IDs, sample sizes ($N$), or stimulus counts** from parametric memory.
2. Verify every new or modified entry in `references.bib` against OpenAlex / Crossref (`scholarly_graph.py bib-verify` when available) before committing.
3. Verify repository accession URLs (`OpenNeuro`, `DANDI`, `GIN`, `OSF`, `Dryad`, `Figshare`, `AWS Open Data`) and record the verification date (`YYYY-MM-DD`) in `last_verified`.

## 2. Public Repository Security & Hygiene
1. This is a **PUBLIC** GitHub repository (`lrgthu/neuroscience-datasets`).
2. **NEVER** write private LAN IP addresses, internal hostnames, SSH aliases, credentials, API keys, or internal cluster filesystem paths into `datasets/`, `cards/`, `catalog/`, `docs/`, or git commit messages.
3. Store any private local mirror paths exclusively in `local/mirrors.local.yaml` (which is `.gitignore`d).

## 3. Single-Source Build & Verification Pipeline
1. Edit source files in `datasets/<category>/<id>.yaml`, `cards/<category>/<id>.md`, and `references.bib` — **never** hand-edit generated blocks in `catalog/datasets.json`, `catalog/datasets.csv`, `docs/catalog_data.js`, or between `<!-- CATALOG:START --> ... <!-- CATALOG:END -->` in `README.md` / `README_zh.md`.
2. After any dataset addition or edit, always run:
   ```bash
   uv run python scripts/build_catalog.py
   uv run ruff check src scripts tests
   uv run pytest -v
   uv run python scripts/build_catalog.py --check
   ```
