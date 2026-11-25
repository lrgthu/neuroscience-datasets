# Natural Object Dataset (`NOD` / `ds004496`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Resolves the classic trade-off between **deep few-subject datasets** (`NSD` $N=8$, `THINGS-fMRI` $N=3$, `BOLD5000` $N=4$) and **shallow wide-cohort studies** by combining both in one `CC0` BIDS resource (`Gong et al., Scientific Data, 2023`, Beijing Normal University):
  - **Deep Sub-Cohort (`sub-01` to `sub-09`)**: `4,000` unique ImageNet images (`1,000` categories × `4` exemplars, single repeat) + `120` MS-COCO images (`× 10` repeats = `1,200` high-SNR test trials) + `pRF` retinotopy + `fLoc` category localizer.
  - **Broad Sub-Cohort (`sub-10` to `sub-30`, `N = 21`)**: `1,000` ImageNet images (`1` per category) shared across subjects to quantify inter-individual representational geometry and functional alignment.

## 2. Recording Specifications & Preprocessing
- **Acquisition & Derivatives**: `3T` Siemens Prisma (`2.0 mm` isotropic, multiband `3`, `TR = 2.0 s`). Ships on OpenNeuro (`ds004496`) with `fMRIPrep`, `FreeSurfer`, and `ciftify` `fsLR` cortical surface single-trial beta maps.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Train encoding models on the `4,000` ImageNet trials in `sub-01..09` and test zero-shot OOD scene generalization on the `120` (`10`-repeat) MS-COCO images; test cross-subject alignment across `sub-10..30`.
- **Critical Modeling Pitfalls**:
  1. **Cohort Stratification**: Always separate `sub-01..09` (deep) and `sub-10..30` (1-session broad) in protocol definitions.
  2. **ImageNet-to-COCO Shift**: ImageNet stimuli are single-object centric (`16° × 16°`) while the `120` COCO test stimuli contain multi-object clutter with longer `2 s` presentation durations—normalize within-run z-scores before cross-paradigm prediction.

## 4. Programmatic Download & Quickstart
```bash
datalad install https://github.com/OpenNeuroDatasets/ds004496.git
```

## 5. Verified Primary References
- **`gong2023nod`**: Gong, Z., Zhou, M., Dai, Y., Wen, Y., Liu, Y., & Zhen, Z. (2023). *A large-scale fMRI dataset for the visual processing of naturalistic scenes*. Scientific Data (`10.1038/s41597-023-02471-x`).
