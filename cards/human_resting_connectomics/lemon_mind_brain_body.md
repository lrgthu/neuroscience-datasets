# MPI-Leipzig Mind-Brain-Body Dataset (`MPI-LEMON` · `OpenNeuro:ds000221`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Bridges human neuroimaging, electrophysiology, peripheral autonomic physiology, and affective/cognitive psychology within a single deeply phenotyped open cohort (`Babayan et al., Scientific Data, 2019`, paired with the broader **`N = 318` `MPI-MBB`** cognitive/connectome study of `Mendes et al., Scientific Data, 2019`, both under `OpenNeuro:ds000221` and `FCP-INDI` / `GWDG`).
- **Two-Generation Design (`N = 227` in `LEMON`)**: Recruits **`154` young adults (`ages 20–35`)** and **`73` older adults (`ages 59–77`)** screened thoroughly for cardiovascular, neurological, and psychiatric conditions (with urine drug toxicology, anthropometrics, blood chemistry, and `20+` cognitive/emotion/mind-wandering scales).

## 2. Recording Specifications & Multimodal Inventory
- **3T Siemens Magnetom Verio (`32`-ch head coil)**:
  - **Quantitative Structural MRI**: `1.0 mm` isotropic **`MP2RAGE`** (yielding quantitative `T1` relaxation maps + proton-density bias-free `UNI` images), `T2w`, `FLAIR` white-matter hyperintensity scans, and susceptibility-weighted imaging (`SWI`/`QSM`).
  - **Resting-State fMRI (`15.3 min`)**: `2.3 mm` isotropic multiband `4` EPI (`TR = 1.40 s`, `TE = 30 ms`, `657` volumes, eyes open fixating a low-contrast cross) with **simultaneous in-scanner ECG, pulse oximetry, respiratory belt, and eye-tracking**. (In the broader `N = 318` `MPI-MBB` cohort of `Mendes et al. 2019`, participants completed up to `4 × 15.3 min = 61 min` of `rfMRI`!)
  - **Diffusion MRI**: `1.7 mm` isotropic multiband `3` (`60` directions at `b = 1000 s/mm²` + `7` `b0`s + reversed phase-encoding maps).
- **Resting-State EEG & Peripheral Cardiovascular Lab (`N = 216` EEG, `N = 195+` continuous blood pressure)**:
  - `62`-channel `BrainAmp MR plus` (`ActiCAP`, `10–10` montage referenced to `FCz`, `1` `VEOG` channel, `2,500 Hz` raw + `250 Hz` preprocessed `EEGLAB` `.set` derivatives) across **`16 × 60 s` interleaved blocks** (`8` Eyes-Closed + `8` Eyes-Open), alongside continuous Finapres beat-to-beat blood pressure, `ECG` heart-rate variability (`HRV`), and respiration.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Benchmark Tasks**:
  1. **Cross-Modal `EEG ↔ fMRI` Individual Difference Alignment**: Predicting individual functional connectivity gradients or `MP2RAGE` intracortical myelin from resting `62-ch` EEG spectral power / microstates / `1/f` aperiodic slope (`FOOOF`/`SpecParam`).
  2. **Heart–Brain & Autonomic Coupling**: Modeling how beat-to-beat `HRV`, baroreflex sensitivity, and respiration co-fluctuate with salience/default-mode network BOLD dynamics and pupil diameter.
- **Critical Modeling Pitfalls**:
  1. **EEG and fMRI Are Same-Subject, Separate-Session (NOT Simultaneous EEG-fMRI)**: Do not attempt `1.4 s` TR-level temporal regression between EEG power and BOLD timecourses—EEG was acquired in an electromagnetically shielded acoustic booth on a separate assessment day.
  2. **Bimodal Age Cohort (`No Ages 36–58`) & `5-Year` Age Bins**: Open metadata discretizes age into `5`-year intervals (`20–25`, ..., `70–75`) and omits ages `36–58`. Fitting unconstrained linear/polynomial age curves across the empty middle gap creates interpolation artifacts; use young-vs-old classification or interval-censored likelihoods.
  3. **Always Denoise `MP2RAGE` Background Prior to `fMRIPrep`/`FreeSurfer`**: Standard `ANTs` brain extraction fails on raw `MP2RAGE` `UNI` images because background air voxels contain high-amplitude division noise; multiply `UNI` by `INV2` (or download the pre-cleaned `MRI_Preprocessed_Derivatives` tarballs from `AWS S3` / `GWDG`).

## 4. Programmatic Download & Quickstart
```bash
# 1. Anonymous AWS S3 download of raw and preprocessed MRI + 62-ch EEG tarballs
aws s3 ls --no-sign-request s3://fcp-indi/data/Projects/INDI/MPI-LEMON/Compressed_tar/

# 2. Or clone the full MPI-MBB / LEMON BIDS repository from OpenNeuro via DataLad
uvx datalad install https://github.com/OpenNeuroDatasets/ds000221.git
```

## 5. Verified Primary References
- **`babayan2019lemon`**: Babayan, A., Erbey, M., Kumral, D., et al. (2019). *A mind-brain-body dataset of MRI, EEG, cognition, emotion, and peripheral physiology in young and old adults*. Scientific Data (`10.1038/sdata.2018.308`).
- **`mendes2019mpimbb`**: Mendes, N., Oligschläger, S., Lauckner, M. E., et al. (2019). *A functional connectome phenotyping dataset including cognitive state and personality measures*. Scientific Data (`10.1038/sdata.2018.307`).
