# Consortium for Reliability and Reproducibility (`CoRR` · `Zuo et al., 2014`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Established the open-science gold standard for quantifying **test–retest reliability (`ICC`), connectome fingerprinting (`I_diff`), and multivariate discriminability** across functional and structural neuroimaging pipelines (`Zuo et al., Scientific Data, 2014`).
- **Global Multi-Sample Scale (`N = 1,629` Participants, `>5,000` Longitudinal Scans)**:
  - Aggregates **`36` distinct test–retest samples** from **`18` international institutions** (`5,093` resting-state fMRI scans, `3,357+` `T1w` anatomical scans, and `1,302` diffusion MRI scans across `ages 6–88`).
  - **Crown-Jewel Sub-Cohorts Inside `CoRR`**:
    1. **`HNU_1` (`Hangzhou Normal University`, `N = 30` adults × `10` sessions = `300` scans)**: Every participant was scanned for `10 min` (`TR = 2.0 s`, `T1w` + `rfMRI` + `ASL`) every `3` days over `1` month (`100 min` total per brain)—serving as a foundational precursor to dense precision-mapping cohorts (`Midnight Scan Club`) and shipped directly via `nilearn` / `OpenNeuro:ds000224`-style precision tutorials.
    2. **`NKI_2` (`Nathan Kline Institute Enhanced TRT`, `N = 24`–`70+`)**: Direct within-subject head-to-head comparison of three EPI sequences: `TR = 0.645 s` (`3 mm` multiband), `TR = 1.40 s` (`2 mm` multiband), and standard `TR = 2.50 s` (`3 mm`), plus `137`-direction `dMRI`.
    3. **`SWU_4` (`Southwest University`, `N = 235` × `2` sessions ~1 year apart)**, **`BNU_1..3` (`Beijing Normal University`)**, **`NYU_1..2`**, and **`MPG_1` (`Max Planck 7T`, `N = 22` at `1.5 mm` isotropic `7T`)**.

## 2. Recording Specifications & BIDS Archive
- **Standardized `RawDataBIDS` on Anonymous AWS S3 (`s3://fcp-indi/data/Projects/CORR/RawDataBIDS/`)**:
  - Organizes all `36` site cohorts (`BMB_1`, `BNU_1..3`, `DC_1`, `HNU_1`, `IACAS_1`, `IBATRT`, `IPCAS_1..8`, `JHNU`, `LMU_1..3`, `MPG_1`, `MRN_1`, `NKI_1..2`, `NYU_1..2`, `SWU_1..4`, `UM`, `UPSM_1`, `Utah_1..2`, `UWM`, `XHCUMS`) into BIDS `sub-*/ses-*/{anat,func,dwi}` hierarchies alongside `CPAC` / `CCS` / `NIAK` quality-control derivatives.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Metrics**:
  1. **Edgewise & Featurewise `ICC(2,1)` / `ICC(3,1)`** via linear mixed-effects variance decomposition ($\sigma^2_{\text{subject}} / (\sigma^2_{\text{subject}} + \sigma^2_{\text{session}} + \sigma^2_{\text{residual}})$).
  2. **Differential Identifiability ($I_{\text{diff}}$) & `Discriminability`** (`Amico & Goñi, 2018`; `Bridgeford et al., PLOS Biology, 2021`) across `HNU_1` (`10` sessions) and multi-site `CoRR` batteries when benchmarking new parcellations, GNN embeddings, or foundation-model representations.
- **Critical Modeling Pitfalls**:
  1. **Never Optimize `ICC` Alone Without Auditing `QC-FC` Motion Bias!**: Because head motion is a highly stable individual trait (`FD` test–retest `ICC > 0.6`), omitting denoising (`e.g., skipping ICA-AROMA / CompCor / 36P`) artificially **boosts** apparent test–retest `ICC` by preserving subject-specific motion artifacts! Always plot the **`ICC` vs. `|QC-FC|` Pareto frontier** (`Parkes et al., NeuroImage, 2018`).
  2. **Separate Within-Day (`Same Coil Placement`) from Multi-Day / Multi-Month Retests**: Samples with back-to-back within-session repeats conflate true trait stability with static head placement and transient vigilance; use multi-day cohorts (`HNU_1`, `BNU_1`, `NYU_2`, `SWU_4`) for realistic noise-ceiling estimates.
  3. **Account for Scan Length (`5 min` vs. `10+ min` Asymptote)**: Single `5 min` runs yield mean edgewise `ICC ~ 0.25–0.35`, whereas pooling `≥30–50 min` across `HNU_1` sessions pushes cortical connectome `ICC` above `0.70–0.85`.

## 4. Programmatic Download & Quickstart
```bash
# Anonymous direct download of HNU_1 (30 subjects × 10 sessions in BIDS) or NKI_2 from AWS Open Data
aws s3 ls --no-sign-request s3://fcp-indi/data/Projects/CORR/RawDataBIDS/
aws s3 sync --no-sign-request s3://fcp-indi/data/Projects/CORR/RawDataBIDS/HNU_1/ ./corr_hnu1_bids/
```

## 5. Verified Primary References
- **`zuo2014corr`**: Zuo, X.-N., Anderson, J. S., Bellec, P., et al. (2014). *An open science resource for establishing reliability and reproducibility in functional connectomics*. Scientific Data (`10.1038/sdata.2014.49`).
