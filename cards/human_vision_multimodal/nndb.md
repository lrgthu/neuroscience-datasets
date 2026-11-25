# Naturalistic Neuroimaging Database (`NNDb`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Published by `Aliko et al. (Scientific Data, 2020)` (`OpenNeuro:ds002837`), **NNDb** provides `~165 hours` of fast (`TR = 1.0 s`) whole-brain BOLD time-series from `86` adults watching **complete, unedited feature films** (`91–148 min` each) across `10` genres, paired with comprehensive **NIH Toolbox** scores (cognition, emotion, motor, sensation) for brain-phenotype modeling beyond resting-state fMRI.
- **Stimulus Design & Cohort Breakdown (`N = 86` across `10` Films)**:
  - *500 Days of Summer* (`N = 20`, romance/comedy, `91 min`)
  - *Citizenfour* (`N = 18`, documentary, `113 min`)
  - *The Usual Suspects*, *Pulp Fiction*, *The Shawshank Redemption*, *The Prestige*, *Back to the Future*, *Split*, *Little Miss Sunshine*, and *12 Years a Slave* (`N = 6` each).
  - Automated millisecond-aligned **word transcripts** (` TextGrid`/`events.tsv` via Gentle/kaldi) and **frame-level face detection annotations** are included directly in BIDS `events.tsv` files.

## 2. Recording Specifications & Preprocessing
- **Acquisition Hardware & Resolution**: `1.5T` Siemens MAGNETOM Avanto (Birkbeck-UCL Centre for NeuroImaging) with `32`-channel head coil, multiband-`4` EPI (`3.2 mm` isotropic, `TR = 1.0 s`, `TE = 54.8 ms`, flip angle `75°`) + `1.0 mm` T1w MP-RAGE. *(Deliberately acquired at `1.5T` with noise-attenuating earbuds to preserve ventral anterior temporal lobe / OFC signal and subject comfort across 2.5-hour sessions).*
- **Released Derivatives (`ds002837`)**:
  - Raw BIDS runs + `AFNI` + `ICA` denoised MNI152 (`3 mm`) continuous full-movie time-series seamlessly stitched across participant-initiated breaks and synchronized to exact film frame/TR indices.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Splits**:
  1. **Long-Context Multimodal Encoding**: Train long-horizon audio-video-language encoders on `8` movies and test zero-shot TR prediction on held-out *500 Days of Summer* (`N = 20`) and *Citizenfour* (`N = 18`).
  2. **Connectome / ISC Phenotype Prediction**: Predict held-out subjects' NIH Toolbox fluid cognition or emotion scores from movie-evoked ISFC / functional connectivity (`5`-fold CV stratified by movie).
- **Critical Modeling Pitfalls**:
  1. **Use Stitched Derivative Time-Series for ISC**: Raw `func/` runs vary in count and break timestamps per participant; always load `derivatives/` movie-locked NIfTIs when computing inter-subject correlations or aligning to movie timecodes.
  2. **`1.5T` Susceptibility & SNR Profile**: Compared to `3T`/`7T`, `1.5T` exhibits lower raw thermal BOLD sensitivity per voxel (`3.2 mm`) alongside **substantially reduced B0 dropout** in anterior temporal pole (`ATL`) and orbitofrontal cortex—valuable for semantic and affective studies!
  3. **Disjoint Subject Groups Across Films**: Because each subject watched only `1` movie, any cross-movie representational shift conflates stimulus genre with subject sample (`N = 6` on minor films) unless normalized by within-movie ISC ceilings.

## 4. Programmatic Download & Quickstart
```bash
# Install NNDb BIDS and ICA-cleaned full-movie MNI derivatives via DataLad
datalad install https://github.com/OpenNeuroDatasets/ds002837.git
aws s3 ls --no-sign-request s3://openneuro.org/ds002837/derivatives/
```

## 5. Verified Primary References
- **`aliko2020nndb`**: Aliko, S., Huang, J., Gheorghiu, F., Meliß, S., & Skipper, J. I. (2020). *A naturalistic neuroimaging database for understanding the brain using ecological stimuli*. Scientific Data (`10.1038/s41597-020-00680-2`).
