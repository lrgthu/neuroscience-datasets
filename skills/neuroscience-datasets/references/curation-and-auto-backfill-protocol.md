# Verified Curation & Auto-Backfill Protocol (`neuroscience-datasets`)

Follow this protocol whenever adding a newly discovered neuroscience dataset or updating an existing entry in the local `neuroscience-datasets` repository during research exploration.

---

## 1. Locate the Live Local Knowledge Base Checkout

Run:
```bash
python3 "<SKILL_DIR>/scripts/query_kb.py" --stats
```
Confirm `Source:` points to a local filesystem repository directory (e.g., `~/Documents/neuroscience-datasets`, or `$NEUROSCIENCE_DATASETS_ROOT`) rather than the remote HTTPS fallback URL. If running on an ephemeral cloud VM with no local checkout, do not attempt local writeback; instead report the candidate dataset spec in your response.

---

## 2. Controlled Vocabularies (`src/neuro_datasets/schema.py`)

Every `datasets/<category>/<id>.yaml` file must strictly use allowed tokens (or extend `schema.py` deliberately with unit tests if a genuinely new modality/species emerges):

- **`category`** (`1` string):
  `human_vision_multimodal` | `human_language_speech` | `nhp_electrophysiology` | `rodent_circuits_population` | `human_resting_connectomics` | `bci_motor_prosthetics` | `model_organisms_connectomics`
- **`species`** (`>=1` list):
  `human` | `macaque` | `mouse` | `rat` | `marmoset` | `zebrafish` | `drosophila` | `celegans`
- **`modalities`** (`>=1` list):
  `fMRI_7T` | `fMRI_3T` | `fMRI_4T` | `MEG` | `EEG` | `ECoG_iEEG` | `sEEG` | `Microwire_Single_Unit` | `Utah_Array` | `Silicon_Probe` | `Neuropixels` | `Two_Photon` | `Widefield_Calcium` | `Light_Sheet` | `Eye_Tracking` | `Behavior` | `Diffusion_MRI` | `Structural_MRI` | `EM_Connectomics`
- **`domains`** (`>=1` list):
  `natural_images` | `natural_movies` | `natural_speech` | `reading` | `multilingual` | `object_recognition` | `motor_reaching` | `speech_bci` | `decision_making` | `spatial_navigation` | `working_memory` | `mental_imagery` | `affective_emotion` | `multimodal` | `resting_state` | `videogames` | `synthetic_ood` | `retinotopy` | `clinical_lifespan` | `connectomics` | `behavioral_similarity`
- **`access.tier`**:
  `open` | `registered` | `credentialed`
- **`data_formats`** (`>=1` list):
  `BIDS` | `NWB` | `NIfTI` | `CIFTI_GIfTI` | `HDF5_MAT` | `FIF_MNE` | `Zarr_NPZ` | `TextGrid_TSV` | `BrainVision_EDF` | `Parquet_CSV` | `WebDataset_Tar`

---

## 3. Step-by-Step Verified Writeback Pipeline

1. **Verify Citations & Accession Metadata First (Zero Guessing)**:
   - Verify every primary and related paper via `scholarly_graph.py bib-verify` (OpenAlex / Crossref) or arXiv API/source unpack, preferring published peer-reviewed venue records over superseded preprints when available.
   - Confirm exact biological sample size (`scale.n_subjects`), stimulus count, sampling rate / `TR`, license, and portal accession ID (`OpenNeuro:ds*`, `DANDI:*`, `OSF:*`, `GIN:*`, `HuggingFace:*`, `Dryad:*`, `Figshare:*`).

2. **Scaffold Entry & Author Deep Card**:
   ```bash
   cd "<KB_ROOT>"
   uv run python scripts/new_dataset.py \
     --id <snake_case_id> \
     --category <category> \
     --name "<Full Dataset Title>" \
     --short-name "<ShortName>"
   ```
   - Populate `datasets/<category>/<id>.yaml`, `cards/<category>/<id>.md` ($\ge 200$ chars covering experimental paradigm, preprocessing levels, canonical splits, noise ceiling, `key_pitfalls`, and CLI download commands), and append verified BibTeX stanza(s) to `references.bib`.
   - **Privacy & Security Check**: Never write private RFC1918 LAN IPs, internal hostnames, credentials, or local cluster paths into any tracked file. Put local dataset cache paths strictly in `local/mirrors.local.yaml` (gitignored).

3. **Run the Mandatory 4-Command Build & Verification Gate**:
   ```bash
   cd "<KB_ROOT>"
   uv run python scripts/build_catalog.py
   uv run ruff check src scripts tests skills
   uv run pytest -v
   uv run python scripts/build_catalog.py --check
   ```
   - `build_catalog.py` automatically regenerates `catalog/datasets.json`, `catalog/datasets.csv`, `catalog/datasets_provenance.json`, `docs/catalog_data.js`, `README.md`, and `README_zh.md`. Because installed agent skills resolve directly to `<KB_ROOT>/catalog/datasets.json`, all research agents immediately see the new dataset with zero reinstall needed!

4. **Clean Local Git Commit (Push Only When Requested)**:
   - Stage only the intended KB files and create a descriptive local commit (`git commit -m "feat(kb): add <short_name> (<id>) verified dataset card"`).
   - Do **not** `git push` automatically during an unrelated research project session unless the user asks to sync/publish the KB; mention `[KB Auto-Updated: <id> (committed locally)]` in one line at the end of your research summary.
