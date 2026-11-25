# Natural Scenes Dataset (`NSD`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: The gold-standard ultra-high-field (`7T`) deep-phenotyping human visual encoding and reconstruction dataset (`Allen et al., Nature Neuroscience, 2021/2022`). Pairs massive within-subject trial counts (`22,500–30,000` image trials per subject) with rich auxiliary localizers (`pRF` retinotopy, `fLoc` category localizer, resting-state, diffusion MRI, behavioral continuous recognition, and eye tracking).
- **Stimulus Design & Timing**: `73,000` square-cropped (`8.4° × 8.4°`) color natural scene images from **MS-COCO**. Each trial presents an image for `3.0 s` followed by a `1.0 s` blank (`4.0 s` SOA) while subjects fixate centrally and perform a continuous long-term old/new recognition judgment.
- **Subject Cohort**: `8` neurologically healthy adults (`subj01–subj08`). Subjects `01, 02, 05, 07` completed all `40` scan sessions (`30,000` trials each); `subj03, 06` completed `32` sessions; `subj04, 08` completed `30` sessions.

## 2. Recording Specifications & Preprocessing
- **Acquisition Hardware & Resolution**: `7T` Siemens Magnetom passively shielded scanner, gradient-echo EPI at `1.8 mm` isotropic spatial resolution (`TR = 1.6 s`, upsampled to `1.0 s` or `1.333 s` in preprocessed time-series preparations).
- **Released Derivatives**:
  - **Native & Surface Spaces**: `func1pt8mm`, `func1mm`, `MNI`, `fsaverage`, and `nsdgeneral` ROI masks.
  - **Single-Trial Betas (`GLMsingle`)**: Three beta versions (`b1`: fixed HRF; `b2`: voxelwise library HRF; **`b3` (`betas_fithrf_GLMdenoise_RR`)**: library HRF + GLMdenoise + fractional ridge regression — **strongly recommended**).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**:
  - **Test (`shared1000`)**: `1,000` images scheduled across all `8` subjects (`982` images viewed by all 4 full-40-session subjects; `515` images viewed 3 times by all 8 subjects).
  - **Train (`unique9000`)**: Up to `9,000` subject-specific images (`× 3` repeats = `27,000` trials) strictly disjoint from `shared1000`.
- **Repeat Structure & Noise Ceiling**:
  - Official per-voxel `ncsnr` maps quantify signal-to-noise SD ratio. For predictions evaluated against trial-averaged responses over $n$ repeats ($n = 3$ on full sessions), compute explainable variance ceiling via:
    $$\text{NC} = \frac{\text{ncsnr}^2}{\text{ncsnr}^2 + \frac{1}{n}}$$
- **Critical Modeling Pitfalls**:
  1. **Within-Session Z-Scoring Is Mandatory**: Raw `int16` beta files (divide by `300.0` to convert to `% BOLD signal change`) exhibit session-to-session mean and variance shifts; standardize each voxel to zero mean and unit variance **within every individual session** before pooling sessions.
  2. **Foundation Model Data Leakage**: Because NSD stimuli come directly from MS-COCO, vision-language models and diffusion priors trained on COCO captions/images require careful audit when making zero-shot claims.
  3. **Memory / Repetition Drift**: Repeat 1 ("novel") vs. Repeats 2–3 ("old") recruit distinct memory-retrieval and repetition-suppression dynamics outside early visual cortex.

## 4. Programmatic Download & Quickstart
```bash
# Browse NSD public AWS S3 bucket without credentials (after completing NSD data access form)
aws s3 ls --no-sign-request s3://natural-scenes-dataset/

# Sync func1pt8mm GLMsingle b3 betas and ROI masks for subj01
aws s3 sync --no-sign-request \
  s3://natural-scenes-dataset/nsddata_betas/ppdata/subj01/func1pt8mm/betas_fithrf_GLMdenoise_RR/ \
  ./nsd/subj01/betas_b3/
```

## 5. Verified Primary References
- **`allen2021nsd`**: Allen, E. J., St-Yves, G., Wu, Y., et al. (2021/2022). *A massive 7T fMRI dataset to bridge cognitive neuroscience and artificial intelligence*. Nature Neuroscience (`10.1038/s41593-021-00962-x`).
