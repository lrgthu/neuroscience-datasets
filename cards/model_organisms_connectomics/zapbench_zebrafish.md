# ZAPBench (`Zebrafish Activity Prediction Benchmark` · `Lueckmann et al., ICLR 2025`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Introduces the first standardized machine-learning forecasting benchmark for **cellular-resolution activity across an entire vertebrate brain** (`Lueckmann et al., ICLR 2025 Spotlight`, `arXiv:2503.02618`, Google Research × HHMI Janelia × Harvard), tracking **`71,721` segmented single neurons** continuously over **`7,879` volumetric frames (`~2.0 hours` at `914 ms/frame`)** in an awake, behaving larval zebrafish.
- **Unprecedented Dual Formulation (`71k × T` Multivariate Time Series + `4D` Video)**:
  - Unlike human fMRI (`~10^5` coarse `2 mm` hemodynamic voxels) or mammalian electrophysiology (`<1%` sparse subsampling of cortex), ZAPBench captures nearly every neuron in the larval zebrafish brain simultaneously—releasing **both** extracted cell traces (`traces` `[7879, 71721]`) **and** the underlying 3D motion-stabilized volumetric video (`[7879, 2048, 1328, 72]`) + dense 3D cell segmentation masks!
  - Furthermore, the **exact same larval zebrafish specimen** is undergoing nanometer-scale serial EM connectomic reconstruction, positioning ZAPBench as a flagship testbed for connectome-informed foundation models.
- **`9` Virtual-Reality Visual Stimulus Regimes**: Closed-loop optomotor `gain` adaptation, coherent motion `dots`, whole-field `flash`, phototactic `taxis` (**held out as a zero-shot OOD test condition!**), `turning`, `position`, `open_loop` replay, `rotation`, and spontaneous `dark`.

## 2. Recording Specifications & Cloud TensorStore Layout
- **Cloud-Native Zarr v3 Streaming (`gs://zapbench-release/volumes/20240930/`)**:
  - Zero-download-barrier streaming directly into JAX / PyTorch via Google **`TensorStore`** (`zarr3` driver):
    - `traces`: `7,879 × 71,721` (`float32` normalized $\Delta F/F$ traces, `~2.2 GB` total—fits entirely in laptop/GPU RAM!).
    - `aligned`: `4D` motion-registered calcium fluorescence volumes (`terabyte-scale` chunked Zarr v3).
    - `segmentation`: `3D` voxel-level single-soma segmentation mask linking all `71,721` trace columns to exact `(x, y, z)` brain coordinates.
    - Stimulus covariate channels & `zapbench` JAX/Flax reference baselines (`Linear`, `NLinear`, `TiDE`, `TSMixer`, `Time-Mix`, `3D/4D UNet`).

## 3. Canonical Splits, Evaluation Horizons & Modeling Pitfalls
- **Official Benchmark Matrix (`2` Context Lengths × `32`-Step Forecast Horizon)**:
  - **Short Context (`C = 4` frames = `3.66 s`)** vs. **Long Context (`C = 256` frames = `234 s`)** predicting **`H = 1..32` future frames** (`0.91 s` to `29.2 s`), scored by elementwise **Mean Absolute Error (`MAE`)** per condition and on the zero-shot held-out **`taxis`** condition.
- **Critical Modeling Pitfalls**:
  1. **Do Not Judge Models Solely at `H = 1` (`914 ms`)**: Because nuclear-localized `GCaMP` fluorescence decays over several seconds, `1`-step ahead variance is dominated by trivial AR(1) persistence; meaningful separation between multivariate dynamics (`TSMixer` / `4D UNet` / graph transformers) and univariate linear models emerges at **`H = 4..32` steps** and when conditioned on visual stimulus covariates!
  2. **Respect Official Guard Margins Between Chronological Splits**: `zapbench.data_utils` inserts temporal buffer gaps around train/val/test boundaries inside each condition so `C = 256` lookback windows never leak validation frames into training targets—always load splits via `zapbench` specs rather than naive array slicing.
  3. **Single-Animal Geometry (`N = 1` Brain)**: Cross-validation in ZAPBench tests **temporal and sensory-regime generalization** within one `71,721`-neuron brain; combine with multi-subject larval zebrafish light-sheet cohorts (`Chen, Mu et al., 2018`, `N = 18`) when evaluating cross-animal anatomical alignment.

## 4. Programmatic Download & Quickstart
```bash
# Stream the full 7,879 × 71,721 whole-brain trace matrix directly from GCS via TensorStore (zero auth!)
uv run --with tensorstore --with numpy python -c "
import tensorstore as ts
ds = ts.open({
    'driver': 'zarr3',
    'kvstore': 'gs://zapbench-release/volumes/20240930/traces',
}).result()
print('ZAPBench trace tensor shape (timesteps, neurons):', ds.shape, ds.dtype)
sample = ds[:10, :5].read().result()
print('First 10 frames × 5 neurons loaded cleanly:', sample.shape)
"
```

## 5. Verified Primary References
- **`lueckmann2025zapbench`**: Lueckmann, J.-M., Immer, A., Chen, A., et al. (2025). *ZAPBench: A Benchmark for Whole-Brain Activity Prediction in Zebrafish*. International Conference on Learning Representations (`ICLR 2025`, `arXiv:2503.02618`).
