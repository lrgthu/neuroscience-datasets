# Global Neuroscience Datasets Knowledge Base Rules (`neuroscience-datasets`)

## 1. Domain Scope Gate (Neuroscience / Brain / NeuroAI Research Only; Non-Neuroscience & Ops Exempt)

- **GATE N — Neuroscience, Cognitive Science, NeuroAI, BCI, & Connectomics Research (`neuroscience-datasets`)**:
  Whenever **any** conversation, `/plan`, `/boost`, `/grill-me`, `/goal`, `/teamwork` session, subagent (`research`, `self`), `run_workflow` pipeline, or `swarm` worker explores **neuroscience, brain encoding/decoding, cross-species or cross-modal neural alignment, neural population dynamics/manifolds, BCI/neuroprosthetics, neuroimaging cohorts, or connectomics**—across Stages `0 → 1 → 2 → 3`:
  - You **MUST** read the `neuroscience-datasets` skill (`skills/neuroscience-datasets/SKILL.md`) and query the live curated knowledge base (`query_kb.py`) **before** selecting datasets from parametric memory, designing crucial/full experiments, writing data loaders, or citing dataset papers, and propagate this skill to delegated subagents/workflows/swarms.
- **EXPLICIT EXEMPTION**:
  Non-neuroscience ML/AI/systems research (e.g., pure RecSys, LLM serving, pure math, general vision/NLP without neural recordings) and everyday coding/homelab ops are **exempt**.

---

## 2. Core Non-Negotiable Neuroscience Dataset & Auto-Evolution Guardrails

1. **KB-First Grounding & Confound/Leakage Pre-Check**:
   - Query `query_kb.py` (`--query`, `--species`, `--modality`, `--pitfalls`, `--show-cards`) to ground sample sizes ($N$), stimulus counts, access tiers (`open` / `registered` / `credentialed`), local mirror availability (`local/mirrors.local.yaml`), canonical holdout splits (`shared1000`, `wheretheressmoke`, `TVSD` 30-repeat test, `FALCON` held-out days), and noise-ceiling formulas (`ncsnr`, `SPE`, `cvPCA`, `co-bps`).
   - **Never** design or endorse an evaluation protocol that violates documented KB pitfalls (e.g., `Spampinato` block-design temporal confound, `ZuCo` teacher-forcing EEG-to-text leakage, `Open-fMIND` `preproc` motion-scrubbing breaking stimulus alignment, or `Open-fMIND`/`TUEG` upstream-downstream overlap).
2. **Zero-Hallucination Dataset Citations**:
   - Pull verified BibTeX keys directly via `query_kb.py --ids <id> --bibtex` before writing `.bib` files or manuscript tables.
3. **Verified Auto-Backfill into Local Knowledge Base (Authorized)**:
   - When research exploration uncovers a high-value public neuroscience dataset or critical newly verified split/leakage pitfall **missing** from the local KB checkout, you **may automatically add/update it** in the local `neuroscience-datasets` repository **provided all 4 verification gates pass**: (a) OpenAlex/Crossref citation check (`scholarly_graph.py bib-verify`) + live portal/accession check, (b) zero private IPs/hostnames/paths in tracked files, (c) `uv run python scripts/build_catalog.py && uv run ruff check src scripts tests skills && uv run pytest -v && uv run python scripts/build_catalog.py --check`, and (d) commit cleanly locally (pushing to public GitHub only when requested or in dedicated KB maintenance turns) and note `[KB Auto-Updated: <id>]` briefly in your response.
