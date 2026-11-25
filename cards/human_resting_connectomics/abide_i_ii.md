# Autism Brain Imaging Data Exchange (`ABIDE I` & `ABIDE II`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Grassroots open-science landmark pooling retrospectively acquired structural and resting-state `3T` MRI from **`2,226` datasets** across **`24+` international institutions (`36` site-collections)** to study Autism Spectrum Disorder (`ASD`) connectomics (`Di Martino et al., Molecular Psychiatry, 2014`; `Di Martino et al., Scientific Data, 2017`):
  - **`ABIDE I` (`2014`, `N = 1,112` across `17` sites, ages `7–64`)**: `539` individuals with `ASD` and `573` age-matched Typical Controls (`TC`), accompanied by `ADOS`, `ADI-R`, `SRS`, and `FIQ/VIQ/PIQ` scores. Thanks to the **Preprocessed Connectomes Project (`PCP`)** and `nilearn.datasets.fetch_abide_pcp`, `ABIDE I` became the de facto clinical classification benchmark for virtually every brain graph neural network (`BrainNetCNN`, `BrainGNN`, `BrainGB`, `BrainNetTF`) and fMRI foundation model (`BrainLM`, `SwiFT`, `Brain-JEPA`, `Open-fMIND`).
  - **`ABIDE II` (`2017`, `N = 1,114` across `19` sites, ages `5–64`)**: Adds `521` `ASD` and `593` `TC` datasets with enriched female representation, psychiatric comorbidity phenotyping (`ADHD`, anxiety), and **`N = 284` diffusion MRI (`dMRI`)** scans across `5` sites plus `N = 38` longitudinal `1–4 yr` follow-ups (`UCLA`, `UPSM`).

## 2. Recording Specifications & Preprocessed Connectomes Project (`PCP`)
- **Heterogeneous Real-World Clinical `3T` Acquisition**:
  - Single `5–10 min` resting-state EPI run per subject (`TR = 1.5–3.0 s`, `~3.0 mm` voxels; `12` sites eyes-open vs. `5` sites eyes-closed in `ABIDE I`) paired with `1 mm` `T1w` anatomical MRI (`FreeSurfer` cortical thickness & surface area derivatives included).
- **`PCP` 16-Variant Pipeline Matrix (`ABIDE I` on anonymous AWS S3)**:
  - Processed identically through **`4` software stacks** (`CPAC`, `CCS`, `DPARSF`, `NIAK`) crossed with **`4` nuisance strategies** (`bandpass 0.01–0.1 Hz` on/off × `Global Signal Regression` on/off), releasing `3D/4D` NIfTI maps (`ALFF`, `fALFF`, `ReHo`, `VMHC`, `degree centrality`, `eigenvector centrality`) and ROI timeseries (`Craddock CC200`, `CC400`, `AAL-116`, `Harvard-Oxford`, `Dosenbach-160`, `EZ`, `Talairach-Tournoux`).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Benchmark Splits (`AUROC ~ 0.67–0.76` realistic ceiling!)**:
  1. **Pooled Site-Stratified 10-Fold CV**: Either the strict visual-QC subset of `Abraham et al., NeuroImage, 2017` (**`N = 871`**: `403 ASD / 468 TC`) or the `BrainGB`/`BrainNetTF` `CPAC` subset (**`N = 1,009–1,035`**), stratified jointly by `(SITE_ID, DX_GROUP)`.
  2. **Leave-One-Site-Out (`LOSO`) Evaluation**: Essential to verify that a classifier generalizes to unseen scanners rather than memorizing site biases (`LOSO` accuracy typically drops `3–6 pp` below pooled CV).
- **Critical Modeling Pitfalls**:
  1. **Beware Reported Accuracies `>80–85%` (Data Leakage Red Flag)**: Large-scale benchmarks (`Abraham et al., 2017`; `Heinsfeld et al., 2018`; `BrainGB, 2022`) consistently establish an `ABIDE I` diagnostic ceiling around **`67–75%` accuracy (`0.70–0.77` AUROC)** due to single-run (`~6 min`) scan noise and DSM-IV/5 clinical heterogeneity. Higher claims nearly always stem from global feature selection/PCA/`ComBat` before train/test splitting or window-level slicing across train and test!
  2. **Fit `ComBat` / Temporal Resampling Strictly Inside Training Folds**: Never run `neuroCombat` on the full `N = 1,035` cohort using test labels/covariates before splitting, and resample site-varying `TR`s (`1.5–3.0 s`) explicitly when feeding raw ROI timeseries into sequence foundation models.
  3. **Audit `ABIDE I` ↔ `ABIDE II` Subject Overlap & Head Motion**: Regress or stratify `mean_fd` (`func_mean_fd` in `Phenotypic_V1_0b_preprocessed1.csv`) and exclude overlapping longitudinal IDs when testing `ABIDE I → ABIDE II` zero-shot transfer.

## 4. Programmatic Download & Quickstart
```bash
# 1. Instant one-line fetch via Nilearn (no credentials required)
uv run --with nilearn python -c "
from nilearn.datasets import fetch_abide_pcp
data = fetch_abide_pcp(data_dir='./abide_pcp', pipeline='cpac', band_pass_filtering=True, global_signal_regression=False, derivatives=['rois_cc200'], quality_checked=True)
print('Loaded QC-passed ABIDE I subjects:', len(data.rois_cc200))
"

# 2. Direct anonymous AWS S3 browsing for raw BIDS and ABIDE I / ABIDE II archives
aws s3 ls --no-sign-request s3://fcp-indi/data/Projects/ABIDE/
aws s3 ls --no-sign-request s3://fcp-indi/data/Projects/ABIDE2/
```

## 5. Verified Primary References
- **`dimartino2014abide`**: Di Martino, A., Yan, C.-G., Li, Q., et al. (2014). *The autism brain imaging data exchange: towards a large-scale evaluation of the intrinsic brain architecture in autism*. Molecular Psychiatry (`10.1038/mp.2013.78`).
- **`dimartino2017abide2`**: Di Martino, A., O'Connor, D. A., Chen, B., et al. (2017). *Enhancing studies of the connectome in autism using the autism brain imaging data exchange II*. Scientific Data (`10.1038/sdata.2017.10`).
