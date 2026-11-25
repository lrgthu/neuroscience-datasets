---
name: neuroscience-datasets
description: >-
  Queries, audits, and auto-curates the verified Neuroscience Datasets Knowledge
  Base (112+ datasets across 8 species and 19 modalities: fMRI, MEG, EEG,
  iEEG/ECoG/sEEG, Utah Array, Neuropixels, 2-Photon, Light-Sheet, EM
  Connectomics). MUST activate automatically before selecting datasets,
  designing experiments, writing dataloaders, checking test-split/pretraining
  leakage, or citing dataset papers in any neuroscience, cognitive science,
  NeuroAI, brain encoding/decoding, BCI, population dynamics, or connectomics
  research exploration; also authorizes verified auto-backfill of newly
  discovered datasets into the local KB via bib-verify and build_catalog.py.
---

# Neuroscience Datasets Knowledge Base Skill (`neuroscience-datasets`)

> **Core Premise**: Parametric LLM memory routinely hallucinated neuroscience sample sizes ($N$), confuses false-friend DOIs, misses upstream foundation-model pretraining overlap, and repeats invalidated benchmark setups (such as temporally confounded block-design EEG or teacher-forced EEG-to-text). Always ground dataset selection, canonical splits, noise ceilings, CLI access, and BibTeX citations in the live verified knowledge base (`catalog/datasets.json`), and write verified discoveries back into the local KB checkout.

## Executable Tooling & Reference Guide

Use `<SKILL_DIR>/scripts/query_kb.py` (`python3` stdlib fast-path, `<25 ms`, auto-resolves local KB checkout via `.kb_root` / `$NEUROSCIENCE_DATASETS_ROOT` / `~/Documents/neuroscience-datasets` with HTTPS fallback):

1. **Inventory & Multi-Facet Search (`<SKILL_DIR>/scripts/query_kb.py`)**:
   ```bash
   # Live inventory summary (counts by category, species, modality, local mirrors)
   python3 "<SKILL_DIR>/scripts/query_kb.py" --stats

   # Ranked keyword + facet search (supports synonyms: fmri, ieeg, nhp, rodent, 2p, em, ephys)
   python3 "<SKILL_DIR>/scripts/query_kb.py" --query "THINGS visual" --modality fMRI,MEG,EEG,Utah_Array
   python3 "<SKILL_DIR>/scripts/query_kb.py" --species macaque,mouse --query "decision manifold" --access open
   python3 "<SKILL_DIR>/scripts/query_kb.py" --category bci_motor_prosthetics --pitfalls
   ```
2. **Deep Protocol, Split/Leakage Audit & Verified BibTeX Extraction**:
   ```bash
   # Inspect exact canonical splits, noise ceiling formulas, and confound pitfalls
   python3 "<SKILL_DIR>/scripts/query_kb.py" --ids nsd,things_data,tvsd --pitfalls

   # Read full technical Markdown cards + download CLI + private local mirror status
   python3 "<SKILL_DIR>/scripts/query_kb.py" --ids open_fmind,uth_natural_speech --show-cards

   # Emit 100%-verified deduplicated BibTeX stanzas for .bib files
   python3 "<SKILL_DIR>/scripts/query_kb.py" --ids nsd,things_data,tvsd --bibtex
   ```
3. **[Verified Auto-Backfill & Schema Protocol](./references/curation-and-auto-backfill-protocol.md)** — **Read whenever adding a newly discovered dataset or updating a split/pitfall card in the local KB repository**.

---

## Mandatory 4-Stage Research Integration Workflow (`Stages 0 → 1 → 2 → 3`)

### Stage 0 — Research Ideation & Crucial Experiment Design (`⇄ scientific-ideation`)
1. **Check Real Data Feasibility & Local Mirrors First**:
   - Run `query_kb.py` to verify actual subject counts ($N$), per-subject recording duration (`hours_per_subject`), stimulus counts, and `access.tier` (`open` vs. `registered` DUA vs. `credentialed`). Prefer `open` or locally mirrored (`[LOCAL MIRROR]`) datasets for `<4h` *Experimentum Crucis* falsification tests.
2. **Mine Cross-Modal / Cross-Species Bridges & Avoid Dead Benchmarks**:
   - Look for shared-stimulus bridges (`NSD` 7T ↔ `Alljoined-1.6M` EEG ↔ `NSD-Synthetic`; `THINGS-data` fMRI/MEG/EEG ↔ `TVSD` macaque 1,024-ch Utah array ↔ `CNeuroMod-THINGS` ↔ `THINGS-Behavior+`) and check `--pitfalls` so no candidate idea rests on a known artifact.

### Stage 1 — Literature Lineage & Zero-Hallucination `.bib` (`⇄ scholarly-graph-audit` / `literature-evidence-workflow`)
1. **Seed Graph Lineage with Verified DOIs**:
   - Extract `primary_doi_or_arxiv` from `query_kb.py` to seed `scholarly_graph.py lineage` and `citation-audit`.
2. **Export Audited BibTeX Keys**:
   - Run `python3 "<SKILL_DIR>/scripts/query_kb.py" --ids <id1,id2,...> --bibtex` instead of writing dataset BibTeX from memory.

### Stage 2 — Dataloader Engineering & Leakage/Confound Guards (`⇄ scientific-computing`)
Before writing dataset preprocessing or evaluation code, inspect `--show-cards --pitfalls` for the target dataset(s) and enforce:
- **Official Holdout Splits**: Lock exact community test sets (`NSD` `shared1000`, `UT-Speech` `wheretheressmoke`, `TVSD` `100 × 30-repeat` test images, `CNeuroMod` `Friends S7`, `FALCON` held-out calibration days, `ZAPBench` temporal horizon splits).
- **Pretraining-Downstream Decontamination**: When evaluating brain foundation models pretrained on `Open-fMIND` (`322` OpenNeuro datasets including `StudyForrest ds000113`, `Narratives ds002345`, `Sherlock ds001132`, `Alice ds002322`, `NNDb ds002837`, `LPPHK ds004718`) or `TUEG` (`tuh_eeg`), explicitly exclude overlapping downstream subjects/studies!
- **Preprocessing Regime Match**: Never use motion-scrubbed / `0.01–0.1 Hz` bandpassed resting derivatives (`Open-fMIND` `preproc`) for frame-locked stimulus encoding (use `quasiraw`); enforce `float64` (`scipy.linalg.eigh` / SVD) for high-dimensional eigenspectrum or Procrustes/ridge conditioning.
- **Temporal & Teacher-Forcing Leakage**: Ban random epoch splits on continuous naturalistic speech/movie/RSVP streams (`10–20 s` HRF buffer for fMRI; group by unique stimulus/run for M/EEG); ban teacher-forced next-token LLM scoring without zero-EEGshuffled-EEG ablation controls on `ZuCo`.

### Stage 3 — Manuscript Protocol `P1/P2` Identity & Tables (`⇄ scientific-writing` / `scientific-figures`)
- Bind every quantitative table/figure protocol (`8-Tuple Protocol Identity`) to the exact `DatasetRecord` fields (`n_subjects`, `sampling_rate_or_tr`, `standard_splits`, `noise_ceiling_or_repeat_structure`, and verified `primary_bib_keys`).

---

## Verified Auto-Backfill Loop (Keeping the Knowledge Base Alive)

Whenever an active exploration or literature unpack uncovers a **high-value public neuroscience dataset** (or a newly verified methodological pitfall on an existing entry) that is absent from `query_kb.py`:
1. Read **[curation-and-auto-backfill-protocol.md](./references/curation-and-auto-backfill-protocol.md)**.
2. Verify all citations (`scholarly_graph.py bib-verify`) and live accession URLs, author the YAML + Markdown card in the local KB repository (`python3 "<SKILL_DIR>/scripts/query_kb.py" --stats` prints the resolved local KB path), run the full 4-command verification gate (`build_catalog.py`, `ruff`, `pytest`, `build_catalog.py --check`), commit cleanly locally, and append a concise one-line note (`[KB Auto-Updated: <dataset_id>]`) in your reply.
