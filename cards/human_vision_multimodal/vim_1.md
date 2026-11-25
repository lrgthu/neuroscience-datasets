# Gallant Lab Natural Images 4T fMRI (`vim-1`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Released alongside `Kay et al. (Nature, 2008)` and `Naselaris et al. (Neuron, 2009)`, `vim-1` is the foundational human visual encoding dataset that introduced explicit Gabor-wavelet receptive-field encoding models, candidate-set zero-shot image identification (`92%` and `72%` top-1 from `1,000` candidates), and Bayesian natural image reconstruction.
- **Stimulus Design & Timing**: `1,870` grayscale natural photographs (`20° × 20°` circular aperture, `500 × 500 px` downsampled to `128 × 128` in standard modeling files) drawn from commercial photo libraries:
  - **Model Estimation (`Train`)**: `1,750` unique images presented `2` times each across `35` runs (`5` scan sessions). Each `1.0 s` presentation flashes the photograph `3` times (`200 ms` ON, `200 ms` OFF) followed by `3.0 s` isoluminant gray background (`4.0 s` SOA) while subjects fixate a central color-changing square.
  - **Model Validation (`Test`)**: `120` strictly disjoint novel photographs presented `13` times each (`1,560` trials total) to yield high-SNR trial-averaged cortical response vectors.
- **Subject Cohort**: `2` experienced psychophysical observers (`S1`, `S2` — authors `K.N.K.` and `T.N.`) with strict central fixation stability.

## 2. Recording Specifications & Preprocessing
- **Acquisition Hardware & Resolution**: `4T` Varian INOVA scanner (UC Berkeley) with quadrature transmit/receive surface coil covering occipital cortex; `18` coronal gradient-echo EPI slices at `2.0 × 2.0 × 2.5 mm` (`TR = 1.0 s`, `TE = 28 ms`, `FOV = 128 × 128 mm`).
- **Released Derivatives (`CRCNS:vim-1`)**:
  - `Stimuli.mat`: `128 × 128` estimation (`stimTrn`) and validation (`stimVal`) grayscale image arrays.
  - `EstimatedResponses.mat`: Voxelwise HRF-deconvolved response amplitudes (`dataTrnS1`, `dataValS1`, `dataTrnS2`, `dataValS2`), 3D voxel coordinates, and retinotopic ROI assignments (`1=V1`, `2=V2`, `3=V3`, `4=V3A/B`, `5=V4`, `7=LO`).
  - Raw run-level `VoxelResponses_subject1/2.tar` time-series for custom hemodynamic deconvolution benchmarks.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Fit regularized linear readout (`L2` ridge or sparse boosting) on the `1,750` estimation images (using cross-validation within the `1,750` set for hyperparameter tuning) and evaluate voxelwise Pearson $r$, $R^2$, `120`-way / `1,000`-way image identification, or pixel/generative reconstruction on the `120`-image validation set.
- **Noise Ceiling**: Compute split-half or `13`-trial repeatability across the `13` validation trials per image to separate irreducible measurement noise from model misspecification (`Naselaris et al., 2009`).
- **Critical Modeling Pitfalls**:
  1. **Grayscale & Circular Aperture**: Stimuli have zero chromatic information and sit inside a circular `20°` mask; replicate identical channel tiling and circular masking when extracting modern `ViT` / `ConvNeXt` / `CLIP` activations.
  2. **Pre-Deconvolved Betas vs. Raw Time-Series**: `EstimatedResponses.mat` already fits voxel-specific hemodynamic response functions jointly with trial amplitudes; never apply a second HRF convolution to `EstimatedResponses.mat`.
  3. **Occipital Slab Boundary**: Only occipital and lateral occipital visual areas (`V1–V4`, `V3A/B`, `LO`) are sampled; for whole-brain ventral/parietal semantics, pair `vim-1` with `NSD` or `BOLD5000`.

## 4. Programmatic Download & Quickstart
```bash
# Register for free academic credentials at https://crcns.org/register
curl -O -J --user <crcns_username> \
  https://portal.nersc.gov/project/crcns/download/vim-1/Stimuli.mat
curl -O -J --user <crcns_username> \
  https://portal.nersc.gov/project/crcns/download/vim-1/EstimatedResponses.mat.tar
```

## 5. Verified Primary References
- **`kay2008vim1`**: Kay, K. N., Naselaris, T., Prenger, R. J., & Gallant, J. L. (2008). *Identifying natural images from human brain activity*. Nature (`10.1038/nature06713`).
- **`naselaris2009bayesian`**: Naselaris, T., Prenger, R. J., Kay, K. N., Oliver, M., & Gallant, J. L. (2009). *Bayesian reconstruction of natural images from human brain activity*. Neuron (`10.1016/j.neuron.2009.09.006`).
