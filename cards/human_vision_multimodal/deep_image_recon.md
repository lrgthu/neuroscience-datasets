# Kamitani Deep Image Reconstruction 3T fMRI (`DeepRecon`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Published by `Shen et al. (PLOS Computational Biology, 2019)` (`OpenNeuro:ds001506`), **DeepRecon** is the definitive benchmark for testing whether brain-to-image reconstruction algorithms genuinely decode **arbitrary visual geometry** rather than merely retrieving memorized natural-image priors—pairing natural ImageNet training data with **out-of-distribution (`OOD`) artificial colored shapes, alphabetical letters, and voluntary mental imagery**.
- **Five Multi-Session Experimental Components (`Per Subject`)**:
  1. **Natural Image Training**: `1,200` ImageNet photographs (`150` categories × `8` exemplars) × `5` repeats = `6,000` trials (`8 s` presentation flashing at `2 Hz`).
  2. **Natural Image Test**: `50` disjoint ImageNet photographs × `24` repeats = `1,200` trials.
  3. **Artificial Shapes Test (`OOD`)**: `40` combinations of `8` geometric shapes (`square`, `circle`, `cross`, `plus`, `star`, etc.) × `5` colors (`red`, `green`, `blue`, `cyan`, `yellow`/achromatic) × `20` repeats = `800` trials.
  4. **Alphabetical Letters Test (`OOD`)**: `10` high-contrast letters (`A, C, E, I, N, O, R, S, T, U`) × `12` repeats = `120` trials.
  5. **Mental Imagery Test**: `25` cued natural objects and geometric shapes imagined with eyes closed (`8 s` imagery period) × `20` repeats = `500` trials.
- **Subject Cohort**: `3` healthy adult subjects (`sub-01` to `sub-03`), each scanned for `~20–24 hours` across `~15+` sessions (plus retinotopy and functional localizers).

## 2. Recording Specifications & Preprocessing
- **Acquisition Hardware & Resolution**: `3T` Siemens Magnetom Verio (ATR Kyoto), `12`-channel head coil, multiband-`4` gradient-echo EPI at **`2.0 mm` isotropic** (`TR = 2.0 s`, `TE = 43 ms`, `76` slices, full brain).
- **Released Derivatives**:
  - Raw BIDS NIfTIs (`ds001506`) + preprocessed trial-averaged / single-trial `.h5` ROI matrices (`V1`, `V2`, `V3`, `hV4`, `LOC`, `FFA`, `PPA`) hosted on `Figshare:7033577` (`bdpy` format).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Fit all voxel-to-feature decoders exclusively on the `1,200` natural training images; evaluate pixel correlation, SSIM, LPIPS, and pairwise identification across all `4` test suites (`Natural-50`, `Shapes-40`, `Letters-10`, `Imagery-25`) **without** fine-tuning on synthetic shapes or imagery!
- **Critical Modeling Pitfalls**:
  1. **The Generative Prior Sanity Check**: Modern latent-diffusion decoders trained on `NSD` can produce crisp-looking dogs or landscapes from noise; evaluating the exact same natural-trained decoder on `Shapes-40` and `Letters-10` immediately exposes semantic prior hallucination vs. genuine `V1–V4` spatial decoding.
  2. **Within-Run Shift & Standardization**: Shift BOLD volumes by `4 s` (`2 TRs`), average across the `8 s` (`4 TRs`) stimulus window, and z-score each voxel within every individual run using run baseline/rest periods (`bdpy` standard pipeline).

## 4. Programmatic Download & Quickstart
```bash
# Install raw BIDS dataset from OpenNeuro via DataLad
datalad install https://github.com/OpenNeuroDatasets/ds001506.git

# Preprocessed bdpy HDF5 ROI matrices & official reconstruction code
git clone https://github.com/KamitaniLab/DeepImageReconstruction.git
```

## 5. Verified Primary References
- **`shen2019deeprecon`**: Shen, G., Horikawa, T., Majima, K., & Kamitani, Y. (2019). *Deep image reconstruction from human brain activity*. PLOS Computational Biology (`10.1371/journal.pcbi.1006633`).
- **`horikawa2017god`**: Horikawa, T., & Kamitani, Y. (2017). *Generic decoding of seen and imagined objects using hierarchical visual features*. Nature Communications (`10.1038/ncomms15037`).
