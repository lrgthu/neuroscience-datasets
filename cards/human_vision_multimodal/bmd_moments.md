# BOLD Moments Dataset (`BMD`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Published by `Lahner et al. (Nature Communications, 2024)` (`OpenNeuro:ds005165`), **BMD** is the complete, unblinded, `GLMsingle`-processed flagship release of the MIT `3-second` dynamic visual event fMRI project (`N = 10` subjects, `4,020` video trials/subject). Combines deep within-subject video sampling with crowdsourced natural-language captions, action verbs, object/scene labels, and behavioral video memorability norms.
- **Stimulus Design & Timing**: `1,102` silent `3.0 s` naturalistic videos from **Moments in Time** (`1,000` training clips × `3` repeats across `30` train runs + `102` test clips × `10` repeats across `10` test runs, plus Session 1 retinotopy and dynamic category localizers). Each trial consists of `3.0 s` video + `1.0 s` inter-trial fixation (plus null baseline trials).
- **Subject Cohort**: `10` healthy adult volunteers (`sub-01` to `sub-10`), each completing `5` MRI sessions (`1` localizer/anatomical session + `4` main video sessions).

## 2. Recording Specifications & Preprocessing
- **Acquisition Hardware & Resolution**: `3T` Siemens Magnetom Prisma, `64`-channel head/neck coil, multiband-`2` gradient-echo EPI (`2.5 mm` isotropic, `TR = 1.75 s`, `TE = 30 ms`, flip angle `70°`).
- **Released Derivatives (`ds005165`)**:
  - **Raw BIDS & `fMRIPrep` Outputs**: Volume (`MNI152NLin2009cAsym`) and cortical surface (`fsLR` `91k` CIFTI / `fsaverage`) time-series.
  - **`GLMsingle` Single-Trial Betas**: Voxel-optimized HRF + `GLMdenoise` + fractional ridge regression (`TYPED_FITHRF_GLMDENOISE_RR`) for all `3,000` train trials and `1,020` test trials per subject, plus deconvolved FIR time-courses (`TRs 1–9`) and functional localizer masks (`V1–V4`, `LOC`, `OFA`, `FFA`, `EBA`, `PPA`, `RSC`, `TOS`, `STS`).
  - **Rich Stimulus Metadata**: `5` human-written sentence descriptions per clip, object/scene/action probabilities, and behavioral memorability ratings.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Train encoding, retrieval, or video-diffusion reconstruction models on the `1,000` `task-train` clips (`3` repeats) and evaluate on the `102` `task-test` clips (`10` repeats), never mixing train and test clips.
- **Noise Ceiling**: Official per-voxel/vertex `ncsnr` values (`NC = ncsnr^2 / (ncsnr^2 + 1/n)`, with $n = 3$ for train averages and $n = 10$ for test averages).
- **Critical Modeling Pitfalls**:
  1. **Separate Train vs. Test Run Acquisition**: `task-train` (`100` trials/run) and `task-test` (`102` trials/run) were recorded in separate runs; z-score betas **within every individual run** so run-level baseline/gain shifts cannot separate train and test distributions.
  2. **Silent Clips Only**: All `1,102` stimuli were presented muted; exclude audio streams when extracting multimodal video embeddings.
  3. **Variance Partitioning**: Action verbs, objects, scenes, and low-level motion co-vary strongly in 3-second real-world clips—use BMD's human metadata annotations for commonality / variance-partitioning analysis rather than attributing `EBA`/`STS` $R^2$ solely to one feature family.

## 4. Programmatic Download & Quickstart
```bash
# Install BIDS dataset and GLMsingle derivatives via DataLad or AWS S3 OpenNeuro mirror
datalad install https://github.com/OpenNeuroDatasets/ds005165.git
aws s3 ls --no-sign-request s3://openneuro.org/ds005165/derivatives/versionB/GLMsingle/

# Official Python analysis & variance-partitioning scripts
git clone https://github.com/blahner/BOLDMomentsDataset.git
```

## 5. Verified Primary References
- **`lahner2024bmd`**: Lahner, B., Dwivedi, K., Iamshchinina, P., et al. (2024). *Modeling short visual events through the BOLD moments video fMRI dataset and metadata*. Nature Communications (`10.1038/s41467-024-50310-3`).
