# Human Connectome Project Young Adult (`HCP-YA` · `S1200`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Established the modern standard for **surface-based grayordinate neuroimaging (`CIFTI 91k` + `MSMAll`)**, **multiband `TR = 0.72 s` whole-brain fMRI**, and **brain-behavior benchmark evaluation** (`Van Essen et al., NeuroImage, 2013`; `Glasser et al., NeuroImage, 2013`). Nearly every fMRI foundation model (`BrainLM`, `Brain-JEPA`, `SwiFT`, `Brain-Semantoks`, `Open-fMIND`) uses `HCP-YA` (`~950–1,096` subjects with complete 4-run `rfMRI`) as its primary downstream evaluation benchmark for fluid/crystallized cognition (`r ~ 0.40–0.43`), sex classification (`AUROC ~ 0.95`), and 7-domain task decoding (`Working Memory`, `Gambling`, `Motor`, `Language` story vs. math, `Social` theory-of-mind, `Relational`, `Emotion`).

## 2. Recording Specifications & Preprocessing
- **Modalities in `S1200` (`N = 1,206` behavioral, `~1,113` structural `3T`, `~1,003` complete 4-run `rfMRI`, `N = 184` `7T`, `N = 95` `MEG`)**:
  - `0.7 mm` `T1w` & `T2w` (cortical thickness, sulcal depth, `T1w/T2w` myelin maps).
  - `3T` `2.0 mm` isotropic multiband `8` (`TR = 0.72 s`, `LR` and `RL` phase-encoding pairs).
  - `1.25 mm` `3`-shell (`b = 1000, 2000, 3000 s/mm²`, `270` directions) diffusion MRI.
  - `248`-channel 4D Neuroimaging `Magnes 3600` MEG (`rest`, `working memory`, `story/math`, `motor` in `95` twin subjects).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: `GroupKFold(n_splits=10)` grouped strictly by **`Family_ID`** (requiring Tier-2 Restricted demographic table or using pre-published family-safe split lists), plus the `N = 45` longitudinal **HCP Retest** cohort for intraclass correlation (`ICC`) ceiling checks.
- **Critical Modeling Pitfalls**:
  1. **Zero Tolerance for Cross-Fold Sibling Splitting**: Twins share ~50–100% genetics and shared environment; random splits are invalid on `HCP-YA`.
  2. **Always Balance `LR` and `RL` Runs**: Never train on `REST1_LR` alone without `REST1_RL`, as left/right susceptibility compression/stretching biases inter-hemispheric connectivity.

## 4. Programmatic Download & Quickstart
```bash
# Register free ConnectomeDB account -> generate AWS S3 key pair -> sync via aws-cli or datalad:
datalad install https://github.com/datalad-datasets/human-connectome-project-openaccess.git
```

## 5. Verified Primary References
- **`vanessen2013hcp`**: Van Essen, D. C., Smith, S. M., Barch, D. M., Behrens, T. E. J., Yacoub, E., & Uğurbil, K. (2013). *The WU-Minn Human Connectome Project: An overview*. NeuroImage (`10.1016/j.neuroimage.2013.05.041`).
- **`glasser2013hcppipelines`**: Glasser, M. F., Sotiropoulos, S. N., Wilson, J. A., et al. (2013). *The minimal preprocessing pipelines for the Human Connectome Project*. NeuroImage (`10.1016/j.neuroimage.2013.04.127`).
