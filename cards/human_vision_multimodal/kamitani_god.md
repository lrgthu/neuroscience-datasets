# Generic Object Decoding (`GOD` / Horikawa & Kamitani 2017)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Established the modern **zero-shot feature decoding** paradigm (`Horikawa & Kamitani, Nature Communications, 2017`), demonstrating that linear decoders trained to predict intermediate CNN features from visual perception generalize both to **unseen ImageNet categories** and to **voluntary mental imagery**.
- **Stimulus Design & Timing**: `9 s` stimulus blocks (`12 × 12°` images flashing at `2 Hz` with central fixation color-change 1-back task, `TR = 3.0 s`).
  - **Training Perception**: `1,200` images (`150` ImageNet categories × `8` exemplars × `5` repeats = `6,000` blocks).
  - **Test Perception**: `50` images (`50` strictly held-out ImageNet categories × `1` exemplar × `35` repeats = `1,750` blocks).
  - **Test Imagery**: Verbal category cues (`15 s` imagery blocks × `20` repeats across `10–25` categories).

## 2. Recording Specifications & Preprocessing
- **Acquisition & ROIs**: `3T` Siemens Trio (`3.0 mm` isotropic, `TR = 3.0 s`), standard retinotopic (`V1–V4`) and functional localizers (`LOC`, `FFA`, `PPA`; merged ventral visual cortex mask `VC` contains `~4,400–4,600` voxels per subject). Preprocessed `.h5` (`bdpy`) ROI matrices are maintained by Kamitani Lab on Figshare/GitHub alongside raw BIDS on OpenNeuro (`ds001246`).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Fixed `1,200` train / `50` perception test / imagery test split.
- **Critical Modeling Pitfalls**:
  1. **Small-N Test Set Granularity (`N_test = 50`)**: Because each test item shifts top-1 accuracy by `2.0 pp`, always report **two-way pairwise identification accuracy** (`mean` over $\binom{50}{2} = 1,225$ pairs) and paired bootstrap confidence intervals across subjects (`sub-01` to `sub-05`).
  2. **Within-Run Baseline Rest Subtraction**: Follow the standard `bdpy` preprocessing (hemodynamic shift of `3 s` / `1 TR`, linear trend removal, and run-wise z-scoring before averaging across the `35` test repeats).

## 4. Programmatic Download & Quickstart
```bash
# Clone raw BIDS dataset from OpenNeuro
datalad install https://github.com/OpenNeuroDatasets/ds001246.git
```

## 5. Verified Primary References
- **`horikawa2017god`**: Horikawa, T., & Kamitani, Y. (2017). *Generic decoding of seen and imagined objects using hierarchical visual features*. Nature Communications (`10.1038/ncomms15037`).
