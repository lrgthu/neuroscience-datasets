# Majaj-Hong Macaque V4 & IT Benchmark (`MajajHong2015`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Served for a decade as the primary quantitative yardstick of **Brain-Score** (`Majaj, Hong, Solomon & DiCarlo, J. Neurosci., 2015`), explicitly parametrizing **identity-preserving nuisance transformations** (2D position, 3D pose/rotation, scale) across `64` 3D objects from `8` categories (`animals, boats, cars, chairs, faces, fruits, planes, tables`) at three variation tiers (`V0`, `V3`, `V6`; `3,200` images in `.public`, `5,760` total).
- **Stimulus Timing**: `100 ms` rapid serial presentation (`100 ms` blank ISI, `8°` visual angle) during passive fixation; neural firing rates are canonically integrated over `[70, 170] ms` post-stimulus onset.

## 2. Recording Specifications & Preprocessing
- **Sites**: Chronic Utah microelectrode arrays in two rhesus macaques (`Chabo` and `Tito`); the `MajajHong2015.public` xarray/NetCDF assembly exposes `88` `V4` sites and `168` `IT` sites (`256` sites × `3,200` stimuli × `~28–50` repetitions).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Stratified splits **grouped by `object_name`** (`64` objects) rather than random image index.
- **Critical Modeling Pitfalls**:
  1. **Synthetic Composite Domain Gap**: Stimuli are grayscale 3D CAD meshes superimposed onto uncorrelated natural background photographs—models relying on scene-object co-occurrence or chromaticity behave very differently here than on `TVSD` or `NSD`.
  2. **Estimator Identifiability Sensitivity**: Partial Least Squares (`PLS-25`) vs. $L_2$ Ridge vs. unregularized `CKA` exhibit distinct eigenspectrum weighting; ideal lightweight dataset (`<500 MB` trial-averaged matrix) for analytical/empirical identifiability ablations!

## 4. Programmatic Download & Quickstart
```bash
# Load directly as a labeled xarray DataAssembly via brainscore_vision
uv run python -c "import brainscore_vision as bsv; da = bsv.load_dataset('MajajHong2015.public'); print(da.shape)"
```

## 5. Verified Primary References
- **`majaj2015ventral`**: Majaj, N. J., Hong, H., Solomon, E. A., & DiCarlo, J. J. (2015). *Simple learned weighted sums of inferior temporal neuronal firing rates accurately predict human core object recognition performance*. Journal of Neuroscience (`10.1523/jneurosci.5181-14.2015`).
