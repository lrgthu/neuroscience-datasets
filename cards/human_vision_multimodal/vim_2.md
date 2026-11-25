# Gallant Lab Dynamic Natural Movies 4T fMRI (`vim-2`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Introduced by `Nishimoto et al. (Current Biology, 2011)`, `vim-2` bridged fast `15 Hz` spatiotemporal visual motion and slow `1 Hz` BOLD hemodynamics via 3D Gabor motion-energy pyramids and multi-lag FIR ridge regression, achieving the first naturalistic dynamic video reconstructions from human brain activity.
- **Stimulus Design & Timing**: Silent color natural movie clips (`512 × 512 px`, `15 fps`, `20° × 20°` field of view) compiled from diverse film trailers and wildlife/action footage while subjects fixated a central color-changing point:
  - **Estimation (`Train`)**: `12` distinct `600 s` (`10 min`) movie blocks (`7,200 s` = `120 min` = `7,200 TRs` total), each shown **once**.
  - **Validation (`Test`)**: `9` distinct `60 s` (`1 min`) movie sequences concatenated and shuffled across runs, with every `1 min` sequence repeated **`10` times** (`540 unique TRs × 10 repeats = 5,400 test TRs`).
- **Subject Cohort**: `3` healthy adult subjects (`S1`, `S2`, `S3` — `S.N.`, `A.T.V.`, `T.N.`) scanned across multiple sessions.

## 2. Recording Specifications & Preprocessing
- **Acquisition Hardware & Resolution**: `4T` Varian INOVA MRI system (UC Berkeley) with quadrature transmit/receive surface coil; `18` coronal EPI slices covering occipital and posterior temporal cortex (`2.0 × 2.0 × 2.5 mm` voxels, `TR = 1.0 s`, `TE = 28 ms`).
- **Released Derivatives (`CRCNS:vim-2`)**:
  - Motion-corrected, within-run detrended and z-scored `1 Hz` BOLD time-series matrices (`rt`: `[7200 × N_voxels]` train; `rv`: `[540 × N_voxels × 10]` validation repeats).
  - Full `15 Hz` RGB stimulus HDF5/MAT tensors (`Stimuli_Trn_FullRes`, `Stimuli_Val_FullRes`) and retinotopic cortical ROI masks.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Train spatiotemporal/video-foundation encoding models on the `7,200` estimation TRs (using contiguous `10-minute` block cross-validation to select per-voxel ridge penalties $\lambda_v$), and evaluate correlation $r$ and noise-ceiling-normalized $R^2$ against the `10`-repeat average of the `540` validation TRs.
- **Repeat Structure & Noise Ceiling**: Having `10` exact repeats (`rv` tensor shape `540 × V × 10`) permits unbiased estimation of explainable variance via leave-one-repeat-out or analytical Spearman–Brown reliability.
- **Critical Modeling Pitfalls**:
  1. **Mandatory Multi-Delay Hemodynamic Taps**: Pool `15 fps` video features into `1.0 s` TR bins and concatenate delayed copies (e.g., `delays = [2, 3, 4, 5, 6] s` or `[2, 4, 6] s`) so linear readouts capture voxelwise hemodynamic lag dispersion across `V1`, `MT+`, and ventral cortex.
  2. **Contiguous Block CV Only**: Never randomly shuffle individual `1 s` TRs during hyperparameter tuning—BOLD autocorrelation spans `~15–20 s` and leaks across adjacent TRs.
  3. **Silent Central-Fixation Regime**: `vim-2` has no auditory stream and enforces strict central fixation, isolating retinotopic visual motion from eye-movement and speech confounds.

## 4. Programmatic Download & Quickstart
```bash
# Download processed BOLD matrices and stimulus HDF5 archives from CRCNS (free registration)
curl -O -J --user <crcns_username> \
  https://portal.nersc.gov/project/crcns/download/vim-2/VoxelResponses_subject1.mat
curl -O -J --user <crcns_username> \
  https://portal.nersc.gov/project/crcns/download/vim-2/Stimuli.tar
```

## 5. Verified Primary References
- **`nishimoto2011vim2`**: Nishimoto, S., Vu, A. T., Naselaris, T., Benjamini, Y., Yu, B., & Gallant, J. L. (2011). *Reconstructing visual experiences from brain activity evoked by natural movies*. Current Biology (`10.1016/j.cub.2011.08.031`).
