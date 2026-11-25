# Stringer & Pachitariu 10,000-Neuron Mouse V1 (`Stringer-10k`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Directly measures the **asymptotic population eigenspectrum** of sensory cortex (`Stringer, Pachitariu, Steinmetz, Carandini & Harris, Nature, 2019`), showing via `~10,000` simultaneously imaged V1 neurons viewing `2,800` natural images (`× 2` repeats) that stimulus-related variance decays as a scale-free power law $\lambda_n \propto n^{-\alpha}$ with $\alpha \approx 1.04$ (`> 1 + 2/d` smoothness bound), balancing high capacity with smooth differentiability.
- **Included Control Cohorts (`10.25378/janelia.6845348`)**: Full-field natural images (`2,800`), spatially whitened images, low-dimensional `$d$-dimensional` projected images (`d = 1, 4, 8, 32`), drifting gratings, and spontaneous darkness recordings with `500-D` infrared face-motion SVD traces.

## 2. Recording Specifications & Preprocessing
- **Acquisition**: `11`-plane resonance-galvo-piezo 2-photon calcium imaging (`2.5 Hz` volume rate) in `Emx1-Cre;CaMKII-tTA;Ai94` (`GCaMP6s`) awake head-fixed mice, processed via `Suite2p` cell detection, neuropil subtraction, and spike deconvolution.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Cross-Validated PCA (`cvPCA`)**: Fit orthonormal singular vectors $U$ on Repeat 1 ($X^{(1)} \in \mathbb{R}^{M \times N}$, $M=2,800, N \approx 10,000$) and evaluate unbiased signal variance on Repeat 2 via $\hat{\lambda}_k = \frac{1}{M} (X^{(1)} u_k)^\top (X^{(2)} u_k)$.
- **Critical Modeling Pitfalls**:
  1. **Subtract Spontaneous Subspace First**: Ongoing behavioral arousal/whisking drives strong shared variance across V1; fit top `32–64` PCs on interspersed spontaneous blank-screen frames and project them out of `X_1` and `X_2` before running `cvPCA`.
  2. **`float64` Precision Required**: Power-law tail estimation over modes `k = 10..500` requires `float64` SVD/eigendecomposition so numerical roundoff does not bias log-log slope $\hat{\alpha}$ regressions.

## 4. Programmatic Download & Quickstart
```bash
# Public CC-BY-4.0 MAT archives (~3 GB total; ideal for fast local float64 spectral experiments!)
open "https://doi.org/10.25378/janelia.6845348"
```

## 5. Verified Primary References
- **`stringer2019highdim`**: Stringer, C., Pachitariu, M., Steinmetz, N., Carandini, M., & Harris, K. D. (2019). *High-dimensional geometry of population responses in visual cortex*. Nature (`10.1038/s41586-019-1346-5`).
