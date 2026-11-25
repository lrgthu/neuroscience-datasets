# UK Biobank Brain Imaging Cohort (`UK-Biobank` · `N > 45,000–100,000`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Unmatched **single-protocol population scale** (`Miller et al., Nature Neuroscience, 2016`; `Alfaro-Almagro et al., NeuroImage, 2017/2018`), pairing fast multiband `3T` Siemens Skyra neuroimaging (`TR = 0.735 s`, `2.4 mm` isotropic) across tens of thousands of adults (`target N = 100,000`, `>5,000+` longitudinal repeat scans) with whole-genome sequencing, proteomics, lifestyle surveys, cognitive tests, and linked hospital electronic health records (`ICD-10`). Served as the primary self-supervised pretraining dataset for `BrainLM`, `Brain-JEPA`, `SwiFT`, and `Brain-Semantoks`.

## 2. Recording Specifications & Preprocessing
- **`35-Minute` Six-Modality Protocol**: `T1w` (`1 mm`), `T2-FLAIR`, `swMRI` (`QSM`), `dMRI` (`2` shells, `100` directions), `rfMRI` (`6 min`, `490` volumes, `FIX` ICA-denoised + `25/100`-node partial/full netmats), and `tfMRI` (`4 min` Hariri emotional faces vs. shapes). Over `4,000` precomputed **Imaging-Derived Phenotypes (`IDPs`)** accompany bulk NIfTI volumes on the UKB Research Analysis Platform (`RAP`).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Critical Modeling Pitfalls**:
  1. **Massive Confound Sensitivity (`Alfaro-Almagro et al. 2021`)**: At $N > 40,000$, scanner drift, assessment center (`4` UK imaging hubs), coil element failure epochs, `X/Y/Z` head position in bore, and mean head motion easily masquerade as cognitive/genetic signal—always include the canonical UKB imaging confound set (fit strictly on training folds!).
  2. **Healthy-Volunteer & Age Selection Bias**: UKB participants (`ages 44–82` at imaging) are older and healthier than the general population; models pretrained exclusively on UKB require age/task domain adaptation when transferred to pediatric (`ABCD`/`HBN`) or rich naturalistic paradigms (`Open-fMIND` provides a DUA-free open alternative!).

## 4. Programmatic Download & Quickstart
```bash
# Requires approved UK Biobank project on the cloud Research Analysis Platform (RAP)
# For an immediate open-access alternative with comparable downstream transfer, see `open_fmind`!
```

## 5. Verified Primary References
- **`miller2016ukbiobank`**: Miller, K. L., Alfaro-Almagro, F., Bangerter, N. K., et al. (2016). *Multimodal population brain imaging in the UK Biobank prospective epidemiological study*. Nature Neuroscience (`10.1038/nn.4393`).
- **`alfaroalmagro2017ukbqc`**: Alfaro-Almagro, F., Jenkinson, M., Bangerter, N. K., et al. (2017/2018). *Image processing and Quality Control for the first 10,000 brain imaging datasets from UK Biobank*. NeuroImage (`10.1016/j.neuroimage.2017.10.034`).
