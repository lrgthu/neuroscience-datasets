# Neuroscience Datasets Knowledge Base

**English** | [中文文档 (`README_zh.md`)](./README_zh.md) | [**Interactive Explorer (GitHub Pages) ↗**](https://lrgthu.github.io/neuroscience-datasets/)

[![CI](https://github.com/lrgthu/neuroscience-datasets/actions/workflows/ci.yml/badge.svg)](https://github.com/lrgthu/neuroscience-datasets/actions/workflows/ci.yml)
[![Pages](https://github.com/lrgthu/neuroscience-datasets/actions/workflows/pages.yml/badge.svg)](https://lrgthu.github.io/neuroscience-datasets/)
[![License: MIT / CC-BY-4.0](https://img.shields.io/badge/License-MIT%20%2F%20CC--BY--4.0-blue.svg)](./LICENSE)

A **machine-readable, citation-verified knowledge base of neuroscience datasets** curated for research in **neural encoding & decoding**, **cross-species / cross-modal representation alignment**, **spectral & identifiability analysis**, and **population latent dynamics**.

Unlike flat link lists, every entry in this repository pairs a **strictly validated YAML specification** (`datasets/<category>/<id>.yaml`) with an **expert Markdown technical card** (`cards/<category>/<id>.md`) documenting:
1. **Exact Experimental Scale & Resolution**: Subject counts ($N$), per-subject recording hours, spatial coverage (`voxels / arrays / probes / 2P planes`), and sampling rates / `TR`.
2. **Canonical Train/Test Splits & Noise Ceilings**: Official holdout sets (`shared1000`, `wheretheressmoke`, `100 × 30-repeat TVSD`, `Friends S7`), trial repeat structures, and explainable-variance (`ncsnr`, `SPE`, `cvPCA`, `co-bps`) formulas.
3. **Battle-Tested Modeling Pitfalls & Leakage Guards**: Foundation-model pretraining overlap, epoch overlap leakage in rapid speech/RSVP, multimodal collinearity, slow block-prior drift (`pseudosessions`), and `float64` conditioning.
4. **Zero-Hallucination Provenance**: Copy-pasteable `DataLad` / `AWS S3` / `DANDI` / `ONE-api` CLI commands and 100% verified BibTeX citations (`references.bib`).

---

## Repository Architecture

```text
neuroscience-datasets/
├── datasets/<category>/<id>.yaml      # Authoritative single-source YAML metadata
├── cards/<category>/<id>.md           # Deep technical card (splits, noise ceiling, pitfalls, CLI)
├── references.bib                     # 100% verified BibTeX bibliography (OpenAlex/Crossref audited)
├── catalog/
│   ├── datasets.json                  # Compiled JSON bundle (metadata + Markdown + BibTeX) for AI agents
│   ├── datasets.csv                   # Tidy CSV (`1 row = 1 dataset`, atomic numeric columns)
│   └── datasets_provenance.json       # SHA-256 input digest & git provenance sidecar
├── docs/                              # Zero-dependency EN/ZH interactive explorer (GitHub Pages + offline file://)
├── local/mirrors.example.yaml         # Template for gitignored private cluster cache paths (`*.local.yaml`)
├── src/neuro_datasets/                # Typed schema validator (`NaN`-safe), loader, and exporters
└── scripts/
    ├── build_catalog.py               # Validates & compiles JSON, CSV, README tables, and Pages data
    └── new_dataset.py                 # 1-command scaffolder for adding new datasets
```

---

## Curated Dataset Catalog

<!-- CATALOG:START -->

### Human Vision & Multimodal Video (fMRI / MEG / EEG) (`6`)

| Dataset | Year | Species / Modalities | Subjects ($N$) & Scale | Access / Portal | Card & Primary Ref |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **CNeuroMod**<br><sub>Courtois NeuroMod & Algonauts 2025 Multimodal Movie Dataset</sub> | 2025 | human<br>`fMRI_3T`, `MEG`, `Structural_MRI` | `N=6`, ~80 h/subj, 250 stim | `registered` · [CNeuroMod](https://www.cneuromod.ca/) (CNeuroMod:friends) | [Card](./cards/human_vision_multimodal/cneuromod.md) · [`arXiv:2501.00504`](https://arxiv.org/abs/2501.00504) |
| **THINGS-data**<br><sub>THINGS-data (THINGS-fMRI, THINGS-MEG, THINGS-EEG2)</sub> | 2023 | human<br>`fMRI_3T`, `MEG`, `EEG` | `N=17`, ~12 h/subj, 26,107 stim | `open` · [OpenNeuro](https://things-initiative.org/) (OpenNeuro:ds004192) | [Card](./cards/human_vision_multimodal/things_data.md) · [`10.7554/eLife.82580`](https://doi.org/10.7554/eLife.82580) |
| **NSD**<br><sub>Natural Scenes Dataset (NSD)</sub> | 2021 | human<br>`fMRI_7T`, `Structural_MRI`, `Diffusion_MRI` | `N=8`, ~38 h/subj, 73,000 stim | `registered` · [AWS Open Data](https://naturalscenesdataset.org/) (AWS:s3://natural-scenes-dataset) | [Card](./cards/human_vision_multimodal/nsd.md) · [`10.1038/s41593-021-00962-x`](https://doi.org/10.1038/s41593-021-00962-x) |
| **BOLD5000**<br><sub>BOLD5000 (Release 2.0)</sub> | 2019 | human<br>`fMRI_3T`, `Structural_MRI`, `Behavior` | `N=4`, ~15 h/subj, 4,916 stim | `open` · [OpenNeuro](https://bold5000-dataset.github.io/website/) (OpenNeuro:ds001499) | [Card](./cards/human_vision_multimodal/bold5000.md) · [`10.1038/s41597-019-0052-3`](https://doi.org/10.1038/s41597-019-0052-3) |
| **GOD**<br><sub>Generic Object Decoding (Kamitani ImageNet Perception & Imagery fMRI)</sub> | 2017 | human<br>`fMRI_3T`, `Structural_MRI` | `N=5`, ~14 h/subj, 1,250 stim | `open` · [OpenNeuro](https://github.com/KamitaniLab/GenericObjectDecoding) (OpenNeuro:ds001246) | [Card](./cards/human_vision_multimodal/kamitani_god.md) · [`10.1038/ncomms15037`](https://doi.org/10.1038/ncomms15037) |
| **StudyForrest**<br><sub>StudyForrest (7T Audio & 3T Audiovisual Movie fMRI + Eye-Tracking)</sub> | 2016 | human<br>`fMRI_7T`, `fMRI_3T`, `Structural_MRI` | `N=20`, ~5 h/subj, 8 stim | `open` · [OpenNeuro](https://www.studyforrest.org/) (OpenNeuro:ds000113) | [Card](./cards/human_vision_multimodal/studyforrest.md) · [`10.1038/sdata.2016.92`](https://doi.org/10.1038/sdata.2016.92) |

### Human Language, Speech & Intracranial (fMRI / MEG / EEG / iEEG) (`8`)

| Dataset | Year | Species / Modalities | Subjects ($N$) & Scale | Access / Portal | Card & Primary Ref |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **Podcast-ECoG**<br><sub>The 'Podcast' Intracranial ECoG Natural Language Dataset</sub> | 2025 | human<br>`ECoG_iEEG`, `Structural_MRI` | `N=9`, ~0.5 h/subj, 1 stim | `open` · [OpenNeuro](https://openneuro.org/datasets/ds005574) (OpenNeuro:ds005574) | [Card](./cards/human_language_speech/podcast_ecog.md) · [`10.1038/s41597-025-05462-2`](https://doi.org/10.1038/s41597-025-05462-2) |
| **BrainTreebank**<br><sub>Brain Treebank (Large-Scale Multimodal Movie Intracranial sEEG)</sub> | 2024 | human<br>`sEEG`, `Structural_MRI` | `N=10`, ~4.3 h/subj, 21 stim | `open` · [BrainTreebank](https://braintreebank.dev/) (BrainTreebank:v1) | [Card](./cards/human_language_speech/braintreebank.md) · [`10.52202/079017-3060`](https://doi.org/10.52202/079017-3060) |
| **MEG-MASC**<br><sub>MEG-MASC (Millisecond Naturalistic Speech MEG Corpus)</sub> | 2023 | human<br>`MEG`, `Structural_MRI`, `Behavior` | `N=27`, ~2 h/subj, 4 stim | `open` · [OpenNeuro](https://openneuro.org/datasets/ds004078) (OpenNeuro:ds004078) | [Card](./cards/human_language_speech/meg_masc.md) · [`10.1038/s41597-023-02752-5`](https://doi.org/10.1038/s41597-023-02752-5) |
| **UT-Speech**<br><sub>UT Austin Naturalistic Narrative Speech fMRI (LeBel / Huth)</sub> | 2023 | human<br>`fMRI_3T`, `Structural_MRI` | `N=8`, ~11 h/subj, 95 stim | `open` · [OpenNeuro](https://openneuro.org/datasets/ds003020) (OpenNeuro:ds003020) | [Card](./cards/human_language_speech/uth_natural_speech.md) · [`10.1038/s41597-023-02437-z`](https://doi.org/10.1038/s41597-023-02437-z) |
| **LPP**<br><sub>Le Petit Prince (LPP) Multilingual Audiobook fMRI Corpus</sub> | 2022 | human<br>`fMRI_3T`, `Structural_MRI` | `N=112`, ~1.7 h/subj, 9 stim | `open` · [OpenNeuro](https://openneuro.org/datasets/ds003643) (OpenNeuro:ds003643) | [Card](./cards/human_language_speech/lpp_multilingual.md) · [`10.1038/s41597-022-01625-7`](https://doi.org/10.1038/s41597-022-01625-7) |
| **Narratives**<br><sub>Narratives Spoken Story fMRI Dataset</sub> | 2021 | human<br>`fMRI_3T`, `Structural_MRI`, `Behavior` | `N=345`, ~0.6 h/subj, 27 stim | `open` · [OpenNeuro](https://github.com/snastase/narratives) (OpenNeuro:ds002345) | [Card](./cards/human_language_speech/narratives.md) · [`10.1038/s41597-021-01033-3`](https://doi.org/10.1038/s41597-021-01033-3) |
| **MOUS**<br><sub>MOUS (Mother of Unification Studies — 204-Subject Paired fMRI & MEG)</sub> | 2019 | human<br>`fMRI_3T`, `MEG`, `Structural_MRI` | `N=204`, ~2.5 h/subj, 360 stim | `registered` · [Donders Repository](https://data.donders.ru.nl/collections/di/dccn/DSC_3011020.09_236) (Donders:di.dccn.DSC_3011020.09_236) | [Card](./cards/human_language_speech/mous.md) · [`10.1038/s41597-019-0020-y`](https://doi.org/10.1038/s41597-019-0020-y) |
| **Broderick-EEG**<br><sub>Broderick Naturalistic Audiobook & Cocktail-Party 128-Ch EEG Suite</sub> | 2018 | human<br>`EEG` | `N=19`, ~1 h/subj, 20 stim | `open` · [Dryad](https://datadryad.org/dataset/doi:10.5061/dryad.070jc) (Dryad:10.5061/dryad.070jc) | [Card](./cards/human_language_speech/broderick_speech_eeg.md) · [`10.1016/j.cub.2018.01.080`](https://doi.org/10.1016/j.cub.2018.01.080) |

### Non-Human Primate Multi-Area Electrophysiology (`3`)

| Dataset | Year | Species / Modalities | Subjects ($N$) & Scale | Access / Portal | Card & Primary Ref |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **TVSD**<br><sub>THINGS Ventral-Stream Spiking Dataset (TVSD)</sub> | 2025 | macaque<br>`Utah_Array`, `Eye_Tracking` | `N=2`, ~15 h/subj, 22,348 stim | `open` · [G-Node GIN](https://gin.g-node.org/paolo_papale/TVSD) (GIN:10.12751/g-node.hc7zlv) | [Card](./cards/nhp_electrophysiology/tvsd.md) · [`10.1016/j.neuron.2024.12.003`](https://doi.org/10.1016/j.neuron.2024.12.003) |
| **NLB-21**<br><sub>Neural Latents Benchmark '21 (NLB Macaque Motor, Sensory & Frontal Suite)</sub> | 2021 | macaque<br>`Utah_Array`, `Behavior`, `Eye_Tracking` | `N=4`, ~1.5 h/subj, 108 stim | `open` · [DANDI](https://neurallatents.github.io/) (DANDI:000127) | [Card](./cards/nhp_electrophysiology/nlb_2021.md) · [`arXiv:2109.04463`](https://arxiv.org/abs/2109.04463) |
| **MajajHong2015**<br><sub>Majaj-Hong Macaque V4 & IT Core Object Recognition Benchmark</sub> | 2015 | macaque<br>`Utah_Array`, `Behavior` | `N=2`, ~20 h/subj, 5,760 stim | `open` · [Brain-Score / DANDI](https://www.brain-score.org/) (BrainScore:MajajHong2015.public) | [Card](./cards/nhp_electrophysiology/majaj_hong_2015.md) · [`10.1523/jneurosci.5181-14.2015`](https://doi.org/10.1523/jneurosci.5181-14.2015) |

### Rodent Large-Scale Circuits & Population Recordings (`3`)

| Dataset | Year | Species / Modalities | Subjects ($N$) & Scale | Access / Portal | Card & Primary Ref |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **IBL-BWM**<br><sub>International Brain Laboratory (IBL) Brain-Wide Map</sub> | 2025 | mouse<br>`Neuropixels`, `Eye_Tracking`, `Behavior` | `N=139`, ~2.5 h/subj, 9 stim | `open` · [DANDI / ONE-API (AWS S3)](https://www.internationalbrainlab.com/data) (DANDI:000409) | [Card](./cards/rodent_circuits_population/ibl_brain_wide_map.md) · [`10.1038/s41586-025-09235-0`](https://doi.org/10.1038/s41586-025-09235-0) |
| **Allen-Vis**<br><sub>Allen Brain Observatory: Visual Coding (Neuropixels & Two-Photon)</sub> | 2021 | mouse<br>`Neuropixels`, `Two_Photon`, `Eye_Tracking` | `N=500`, ~3 h/subj, 118 stim | `open` · [DANDI / AWS Open Data](https://portal.brain-map.org/circuits-behavior/visual-coding) (DANDI:000021) | [Card](./cards/rodent_circuits_population/allen_visual_coding.md) · [`10.1038/s41586-020-03171-x`](https://doi.org/10.1038/s41586-020-03171-x) |
| **Stringer-10k**<br><sub>Stringer & Pachitariu 10,000-Neuron Mouse V1 Population Geometry Dataset</sub> | 2019 | mouse<br>`Two_Photon`, `Eye_Tracking`, `Behavior` | `N=7`, ~2.5 h/subj, 2,800 stim | `open` · [Figshare](https://doi.org/10.25378/janelia.6845348) (Figshare:10.25378/janelia.6845348) | [Card](./cards/rodent_circuits_population/stringer_mouse_v1.md) · [`10.1038/s41586-019-1346-5`](https://doi.org/10.1038/s41586-019-1346-5) |

<!-- CATALOG:END -->

---

## Quickstart (CLI, Python & AI Agents)

```bash
# 1. Install dependencies & run schema + cross-reference + unit tests
uv sync --extra dev
uv run pytest -v

# 2. Query datasets from the terminal (by keyword, modality, or species)
uv run python scripts/build_catalog.py --species human --modality ECoG
uv run python scripts/build_catalog.py --query "THINGS"

# 3. Scaffold a new dataset entry, edit YAML + Card + references.bib, and rebuild all artifacts
uv run python scripts/new_dataset.py \
  --id hcp_7t_movie \
  --category human_vision_multimodal \
  --name "HCP 7T Movie-Watching Dataset" \
  --short-name "HCP-7T-Movie"
uv run python scripts/build_catalog.py
```

### Private Local Cluster Cache Overlay (`local/mirrors.local.yaml`)
To track where datasets are mirrored on private workstations or GPU servers **without ever committing internal hostnames, IPs, or filesystem paths to this public repository**, copy `local/mirrors.example.yaml` to `local/mirrors.local.yaml` (which is strictly `.gitignore`-excluded).

---

## License

- **Code & Validation Scripts (`src/`, `scripts/`, `docs/` JS/CSS)**: [MIT License](./LICENSE)
- **Curated Dataset Cards & Structured Metadata (`datasets/`, `cards/`, `catalog/`)**: [CC-BY-4.0](./LICENSE)
- Underlying neuroscience datasets remain subject to their original licenses and Data Use Agreements (`access.license`).
