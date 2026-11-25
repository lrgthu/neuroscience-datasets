# Bao-Tsao Macaque Whole-IT Topographic Object-Space Map (`BaoTsao2020` / *Nature* 2020)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Unified isolated category-selective domains (face patches, body patches) with previously uncharted **"No-Man's-Land" (`NML`)** swaths of primate inferotemporal (`IT`) cortex (`Bao, She, McGill & Tsao, Nature, 2020`), proving that macaque IT forms a **coarse topographic map of the first two principal components of deep-network (`AlexNet fc6`) object space**:
  - **Axis 1 (`Animate` vs. `Inanimate`) × Axis 2 (`Spiky / High Aspect Ratio` vs. `Stubby / Compact`)** partitions IT into **four networks**—`Face`, `Body`, `Spiky-Inanimate`, and a newly predicted & physiologically confirmed **`Stubby` (`No-Man's-Land`)** network—each repeating sequentially across **three hierarchical posterior → middle → anterior stages** with progressively increasing 3D view invariance.
- **Stimulus Paradigms**:
  - **Multi-View Set (`1,224` Images)**: `51` inanimate and animate objects (`6` categories) rendered/photographed across `24` systematic 3D rotation viewpoints (`150 ms` ON / `150 ms` OFF passive fixation) to jointly quantify axis tuning and view-invariance progression across the 3 anatomical stages of each network.
  - **Independent Broad Object Set (`1,593` Images)**: Free-ranging isolated objects spanning natural categories used to verify out-of-distribution `fc6` axis-ramp predictions and discover the fourth (`Stubby`) quadrant.

## 2. Recording Specifications & Preprocessing
- **Multimodal Mapping (`Monkeys M1–M4`)**:
  - **MION Contrast-Enhanced `3T` fMRI**: Whole-hemisphere functional localizers + electrical microstimulation (`fMRI-EM`) confirming causal anatomical connectivity linking the `3` hierarchical patches within each of the `4` object-space networks.
  - **Targeted Single-Unit Electrophysiology**: Tungsten microelectrode and multi-channel linear probe recordings targeted precisely into fMRI-localized patches across all `4` networks × `3` stages (`[60, 220] ms` post-stimulus spike integration window after baseline subtraction).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Topographic & Axis-Coding Benchmarks**: Primary empirical anchor for **Topographic Deep Artificial Neural Networks (`TDANN`, `Margalit et al. Neuron 2024`)**, self-organizing cortical sheet models, and linear axis-ramp vs. exemplar-prototype hypothesis tests.
- **Critical Modeling Pitfalls**:
  1. **Hold Out Whole Objects (`51` Groups) on the `1,224` View Set**: Testing 3D pose tolerance across posterior (`stage 1`), middle (`stage 2`), and anterior (`stage 3`) patches requires training axis readouts on `K-1` objects and evaluating view-invariant consistency across the `24` views of unseen objects.
  2. **Silhouette / Aspect-Ratio Confounds in Low-Level Baselines**: Because `PC1/PC2` of `AlexNet fc6` on background-free objects correlate strongly with global curvature and aspect ratio (`spiky` vs. `stubby`), always benchmark candidate high-level representations against matched Gabor/pixel-PCA controls.
  3. **MION Impulse Response Polarity**: When analyzing the companion fMRI volumes, flip the sign of raw MION signal changes (`CBV` increase $\implies T_2^*$ darkening) and convolve predictors with the slower MION gamma kernel rather than human canonical BOLD HRF.

## 4. Programmatic Download & Quickstart
```bash
# Inspect published Nature Source Data tables & article metadata (full raw arrays via Tsao Lab academic request)
open "https://doi.org/10.1038/s41586-020-2350-5"
```

## 5. Verified Primary References
- **`bao2020itmap`**: Bao, P., She, L., McGill, M., & Tsao, D. Y. (2020). *A map of object space in primate inferotemporal cortex*. Nature (`10.1038/s41586-020-2350-5`).
