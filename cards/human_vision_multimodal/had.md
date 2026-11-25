# Human Action Dataset (`HAD`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Created by the Beijing Normal University Cognitive Neuroscience Lab (`Zhou et al., Scientific Data, 2023`; companion to `NOD`), **HAD** (`OpenNeuro:ds004488`) maximizes **stimulus and subject breadth** for naturalistic human action recognition—covering `21,600` completely distinct `2.0 s` video clips across `180` Human Action Clips and Segments (`HACS`) categories and `30` participants.
- **Stimulus Design & Timing**:
  - Each participant completed `12` functional runs (`60` clips/run = `720` unique clips/subject).
  - The `180` action categories cycled once every `3` runs (`4` distinct exemplar clips per category per subject; `120` distinct exemplars per category across the `30` subjects → `180 × 120 = 21,600` total clips with **zero clip overlap**).
  - Each trial displayed a silent `2.0 s` video clip (`16° × 16°`) followed by a `2.0 s` fixation cross (`4.0 s` SOA).
- **Subject Cohort**: `30` healthy young adults (`sub-01` to `sub-30`; overlaps partially with the `NOD` static-image cohort for cross-static/dynamic comparisons).

## 2. Recording Specifications & Preprocessing
- **Acquisition Hardware & Resolution**: `3T` Siemens Magnetom Prisma, `64`-channel head coil, multiband-`3` gradient-echo EPI at `2.0 mm` isotropic spatial resolution (`TR = 2.0 s`, `TE = 34 ms`, flip angle `90°`).
- **Released Derivatives (`ds004488`)**:
  - Raw BIDS NIfTIs, `fMRIPrep` + `ciftify` surface reconstructions (`fsLR` `32k` / `91,282` CIFTI grayordinates), single-clip GLM beta maps, and HCP MMP `1.0` cortical parcellations.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Train video/action encoders or category classifiers on runs `1–9` (`540` clips, `3` cycles of `180` categories) and test on held-out runs `10–12` (`180` clips, `1` cycle), or use odd-cycle (`runs 1–6`) vs. even-cycle (`runs 7–12`) splits.
- **Category-Level Reliability**: Because individual video clips are never repeated (`n_repeats = 1`), compute split-half reliability across the `180`-category response profiles (`odd` vs. `even` cycles) rather than per-clip repeatability.
- **Critical Modeling Pitfalls**:
  1. **`720` Clips/Subject vs. `21,600` Cohort Total**: Never confuse cohort-wide unique stimuli (`21,600`) with per-subject trial count (`720`); single-subject linear probes over high-dimensional video ViTs require strong `L2` regularization or multi-subject shared readouts.
  2. **Silent Presentation**: Strip audio tracks from HACS source videos before extracting multimodal video embeddings.
  3. **Fixed `4 s` Unjittered SOA**: Standardize single-trial GLM beta maps within each of the `12` runs before cross-run classification or RSA.

## 4. Programmatic Download & Quickstart
```bash
# Install HAD raw BIDS and ciftify/GLM derivatives via DataLad
datalad install https://github.com/OpenNeuroDatasets/ds004488.git
aws s3 ls --no-sign-request s3://openneuro.org/ds004488/derivatives/ciftify/

# Official validation & action-decoding notebooks
git clone https://github.com/BNUCNL/HAD-fmri.git
```

## 5. Verified Primary References
- **`zhou2023had`**: Zhou, M., Gong, Z., Dai, Y., Wen, Y., Liu, Y., & Zhen, Z. (2023). *A large-scale fMRI dataset for human action recognition*. Scientific Data (`10.1038/s41597-023-02325-6`).
