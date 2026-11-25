# CNeuroMod-THINGS (`Static THINGS` ∩ `Dynamic Movies` in the Same Brains)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Directly links **static object-concept neuroimaging (`THINGS`)** and **80-hour multimodal movie neuroimaging (`CNeuroMod` / `Algonauts 2025`)** inside the **exact same individual human brains** (`St-Laurent, Pinsard, Contier, DuPré, Seeliger, Borghesani, Boyle, Bellec & Hebart, Scientific Data, 2026`). Previously, comparing static flash-image encoders (`NSD` / `THINGS-fMRI`) against continuous movie encoders (`Friends` / `StudyForrest`) was confounded by different subjects, scanners, and voxel spaces; `CNeuroMod-THINGS` eliminates all three confounds!
- **Experimental Design**: `4` core CNeuroMod participants completed `33–36` fMRI sessions (`~16.4 hours` per subject), viewing `4,320` unique THINGS images (`720` object categories × `6` exemplars × `3` repetitions = `12,960` trials/subject) in an NSD-style continuous recognition paradigm with graded confidence responses.

## 2. Recording Specifications & Preprocessing
- **Multimodal Synchronized Streams**: `3T` `2.0 mm` isotropic (`TR = 1.49 s`) preprocessed via `fMRIPrep` into the **exact same `T1w` and `CIFTI 91k` grayordinate grids** as all other CNeuroMod datasets (`GLMsingle` single-trial betas included), plus simultaneous in-scanner **eye-tracking / pupillometry**, **ECG**, **respiration**, **pulse oximetry**, and **electrodermal activity (`EDA`)**.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Splits**:
  1. **Cross-Paradigm Transfer (Static ↔ Dynamic Video)**: Fit voxelwise encoders on *Friends* / *Movie10* (`cneuromod`) and test zero-shot on `CNeuroMod-THINGS` static images (or vice versa!) within `sub-01, sub-02, sub-03, sub-06`.
  2. **Cross-Dataset Alignment (`CNeuroMod-THINGS` ↔ `THINGS-fMRI` ↔ `TVSD`)**: Shares the `720` core THINGS-fMRI concepts, enabling direct across-scanner human alignment and human-to-macaque V1/V4/IT alignment.
- **Critical Modeling Pitfalls**:
  1. **Paradigm Hemodynamic Mismatch**: Static single-trial `GLMsingle` betas reflect impulse responses to isolated images on blank backgrounds, whereas *Friends* `TR = 1.49 s` continuous BOLD reflects sustained audiovisual narrative flow—normalize response scales per voxel and account for temporal integration receptive fields!
  2. **Novelty vs. Familiarity Shift (`Repeat 1` vs `Repeats 2–3`)**: As in NSD, first presentations are `"new"` while subsequent presentations trigger memory retrieval and confidence judgments.

## 4. Programmatic Download & Quickstart
```bash
# Clone analysis/navigation code (open) & DataLad dataset (with CNeuroMod credentials)
git clone https://github.com/courtois-neuromod/cneuromod-things.git
datalad install git@github.com:courtois-neuromod/things.git
```

## 5. Verified Primary References
- **`stlaurent2026cneuromodthings`**: St-Laurent, M., Pinsard, B., Contier, O., DuPré, E., Seeliger, K., Borghesani, V., Boyle, J. A., Bellec, P., & Hebart, M. N. (2026). *CNeuroMod-THINGS, a densely-sampled fMRI dataset for visual neuroscience*. Scientific Data (`10.1038/s41597-026-06591-y`).
