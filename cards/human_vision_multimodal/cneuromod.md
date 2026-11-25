# Courtois NeuroMod & Algonauts 2025 (`CNeuroMod`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Unprecedented **within-subject longitudinal depth** (`~80–200+ hours` of 3T fMRI per individual across `sub-01` to `sub-06`), enabling training of high-capacity multimodal video-audio-language neural foundation/encoding models directly on individual human brains (`Gifford et al., arXiv:2501.00504`).
- **Core Sub-Datasets**:
  - **`friends`**: Complete *Friends* sitcom Seasons 1–7 (`~75–80 hours` of audiovisual episodes with synchronized video, audio waveforms, and word/utterance transcripts).
  - **`movie10`**: Full-length films including *The Bourne Supremacy*, *The Wolf of Wall Street*, *Hidden Figures* (repeated twice), and BBC *Life* documentary (repeated twice).
  - **Auxiliary**: `hcptrt` (15 repetitions of HCP functional tasks), `retinotopy`, `shinobi` / `mario` closed-loop videogame play, physiological recordings, and MEG sessions.

## 2. Recording Specifications & Preprocessing
- **Acquisition & Derivatives**: `3T` Siemens Prisma (`2.0 mm` isotropic, multiband 4, `TR = 1.49 s`), preprocessed via `fMRIPrep` (`cifti-output 91k` grayordinates and `Schaefer 2018` `1,000`-parcel time-series released directly in the Algonauts 2025 starter kit).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**:
  - **Training**: *Friends* Seasons 1–6 + *Movie10*.
  - **In-Distribution Test**: *Friends* Season 7.
  - **Out-of-Distribution (OOD) Test**: Six diverse held-out films (*Chaplin*, *Princess Mononoke*, *Le Passe-Partout*, *Planet Earth*, *Pulp Fiction*, *World of Tomorrow*).
- **Critical Modeling Pitfalls**:
  1. **Cross-Modality Variance Confounding**: Sitcom scenes heavily couple speaker faces (vision), voice pitch/envelope (audio), and conversational semantics (LLM)—ideal testbed for **feature-space stacking** and **unique variance partitioning**.
  2. **Episode-Level Cross-Validation**: Never split adjacent TRs or adjacent scenes within the same 22-minute episode across train/val folds; narrative context and slow BOLD drift leak across several minutes.

## 4. Programmatic Download & Quickstart
```bash
# Full CNeuroMod modular DataLad superdataset (requires approved CNeuroMod SSH/token access)
datalad install -r git@github.com:courtois-neuromod/cneuromod.git

# Or inspect Algonauts 2025 public challenge portal for Schaefer-1000 parcel HDF5 bundles
# https://algonautsproject.com/
```

## 5. Verified Primary References
- **`gifford2025algonauts`**: Gifford, A. T., Bersch, D., St-Laurent, M., Pinsard, B., Boyle, J., Bellec, P., Oliva, A., Roig, G., & Cichy, R. M. (2025). *The Algonauts Project 2025 Challenge: How the Human Brain Makes Sense of Multimodal Movies*. arXiv (`arXiv:2501.00504`).
