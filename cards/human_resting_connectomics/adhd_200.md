# ADHD-200 Global Multi-Site Pediatric rs-fMRI Benchmark (`ADHD-200`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Launched clinical neuroimaging's first international machine learning competition (`ADHD-200 Consortium / Milham et al., Frontiers in Systems Neuroscience, 2012`; `Bellec et al., NeuroImage, 2017`), aggregating **`973` children and adolescents (`ages 7–21`)** across **`8` international sites** (`Peking University`, `Kennedy Krieger Institute`, `NeuroIMAGE`, `NYU Child Study Center`, `Oregon Health & Science University`, `University of Pittsburgh`, `Washington University in St. Louis`, and `Brown University`):
  - **`N = 776` Official Training Set**: `491` typically developing controls (`TDC`) and `285` youth with DSM-IV-TR `ADHD` (`ADHD-Combined`, `ADHD-Inattentive`, `ADHD-Hyperactive/Impulsive`), paired with dimensional `ADHD Index` / Conners' symptom severity, `IQ`, medication status, and handedness.
  - **`N = 197` Official Test Set**: Held-out evaluation cohort across `7` seen sites plus **`Brown University` (`N = 26`)** as a strictly unseen zero-shot scanner site.
- **Role in Foundation Models**: Alongside `HCP-YA` and `ABIDE I`, `ADHD-200` serves as a core pediatric clinical transfer benchmark for fMRI foundation models (`BrainLM`, `Brain-JEPA`, `Brain-Semantoks`, `Open-fMIND`) and graph neural networks.

## 2. Recording Specifications & Neuro Bureau Preprocessed Pipelines
- **Multi-Site `3T` (and `1.5T` subgroup) MRI**: `T1w` structural MRI + `5–8.5 min` resting-state EPI (`TR = 1.5–2.5 s`, varying slice order and eyes-open/closed instructions; `OHSU` concatenates `3 × 2.5 min` short runs, `NYU` provides `2 × 6 min` runs).
- **Three Open Neuro Bureau Preprocessed Releases (`s3://fcp-indi/data/Projects/ADHD200/Outputs/`)**:
  1. **`Athena` (`Cameron Craddock`, AFNI + FSL)**: `4 mm` MNI-space `4D` BOLD (filtered & unfiltered), nuisance-regressed (`WM`, `CSF`, `6` motion params, with/without `GSR`), and extracted ROI timeseries across `CC200`, `CC400`, `AAL-116`, `EZ`, `HO`, and `TT`.
  2. **`NIAK` (`Pierre Bellec`, `HDF5/.mat` & `NIfTI`)**: Scrubbed (`FD > 0.5 mm`) `BASC` multi-scale functional parcellations (`197`, `444`, `900+` regions).
  3. **`Burner` (`Carlton Chu`, `SPM8`)**: Modulated gray-matter and white-matter `DARTEL` voxel-based morphometry (`VBM`) maps.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Splits**:
  1. **Official `776 Train / 197 Test` Split** (reporting binary `TDC vs. ADHD`, `3-way` subtype accuracy, and zero-shot `Brown` site generalization).
  2. **5-Fold / 10-Fold Site-Stratified CV** on QC-passed `Athena` `CC200`/`Schaefer` subjects (excluding `Pittsburgh` and `WashU` when training purely binary `ADHD vs. TDC` classifiers unless balancing site prevalence!).
- **Critical Modeling Pitfalls**:
  1. **The Classic `Brown et al. (2012)` Personal-Characteristic Shortcut**: During the 2011 competition, `Brown et al.` won highest raw accuracy (**`62.5%`**) using **zero brain imaging data**—relying solely on `site`, `sex`, `age`, `IQ`, and `handedness`! Always benchmark imaging models against a `phenotypic-only` logistic/MLP baseline and report whether `fMRI` adds statistically significant $\Delta\text{AUROC}$ above demographics and `mean FD`.
  2. **`Pittsburgh` & `WashU` Are 100% Controls in Training**: Including control-only sites in naive cross-entropy training rewards models for learning scanner acquisition artifacts (`TR`, voxel grid, coil intensity) rather than fronto-striatal dysfunction.
  3. **Short-Run `OHSU` Concatenation & Head Motion**: `OHSU` runs are only `~78` volumes (`2.5 min`) each—demean/standardize each short run before concatenating, and regress `FD` aggressively to separate hyperactive head motion from intrinsic network connectivity.

## 4. Programmatic Download & Quickstart
```bash
# Anonymous direct download of Neuro Bureau Athena CC200 ROI timeseries & phenotypic CSVs from AWS Open Data
aws s3 ls --no-sign-request s3://fcp-indi/data/Projects/ADHD200/Outputs/athena/
aws s3 sync --no-sign-request \
  s3://fcp-indi/data/Projects/ADHD200/Outputs/athena/Athena_rois_cc200/ \
  ./adhd200_athena_cc200/
```

## 5. Verified Primary References
- **`milham2012adhd200`**: Milham, M. P., Fair, D. A., Mennes, M., & Mostofsky, S. H. (2012). *The ADHD-200 Consortium: a model to advance the translational potential of neuroimaging in clinical neuroscience*. Frontiers in Systems Neuroscience (`10.3389/fnsys.2012.00062`).
- **`bellec2017adhd200preproc`**: Bellec, P., Chu, C., Chouinard-Decorte, F., Benhajali, Y., Margulies, D. S., & Craddock, R. C. (2017). *The Neuro Bureau ADHD-200 Preprocessed repository*. NeuroImage (`10.1016/j.neuroimage.2016.06.034`).
- **`brown2012adhd200confound`**: Brown, M. R. G., Sidhu, G. S., Greiner, R., et al. (2012). *ADHD-200 Global Competition: diagnosing ADHD using personal characteristic data can outperform resting state fMRI measurements*. Frontiers in Systems Neuroscience (`10.3389/fnsys.2012.00069`).
