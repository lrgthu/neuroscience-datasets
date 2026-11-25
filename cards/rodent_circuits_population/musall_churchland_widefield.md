# Musall & Churchland Cortex-Wide Widefield, 2P & Neuropixels Movement Dataset (`Musall-2019`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Transformed how systems neuroscience interprets single-trial cortical variability during cognitive tasks (`Musall, Kaufman, Juavinett, Gluf & Churchland, Nature Neuroscience, 2019`), demonstrating via **dorsal-cortex widefield calcium imaging, 2-photon cellular imaging, and cortical/subcortical Neuropixels electrophysiology** that **uninstructed spontaneous movements** (whisking, pupil, nose, jaw, body fidgeting) account for the lion's share of single-trial variance (`cvR² > 40%`), and introducing the canonical **`cvR²` (maximal/marginal) vs. `ΔR²` (unique variance)** linear encoding decomposition (`musall/ridgeModel`).
- **Delayed 2AFC Multisensory Task**: Head-fixed mice grab dual handles (`piezo` sensors), initiate trials, experience `1.0 s` sequences of lateralized visual flashes or auditory clicks, maintain their decision across a `1.0 s` memory delay, and lick left or right spouts upon servo spout movement.

## 2. Recording Specifications & Preprocessing
- **Three-Scale Validation (`CSHL DOI:10.14224/1.38599`)**:
  1. **Widefield Dorsal Cortex Imaging (`22` mice across `10` Cre lines)**: Transcranial macroscope imaging across the entire dorsal neocortex (`VIS`, `RS`, `PPC`, `SSp`, `MOp`, `MOs/ALM`), covering pan-excitatory (`Emx1`), laminar pyramidal (`Cux2` L2/3, `PlxnD1` IT, `Fezf2` PT/corticospinal), and inhibitory (`Pvalb`, `SST`, `VIP`) populations. Sampled at `30 Hz` with alternating **`473 nm` (calcium-dependent)** and **`405 nm` (calcium-independent hemodynamic reference)** illumination, compressed into `200` spatial (`U`) and temporal (`V`) SVD components aligned to **Allen CCFv3** landmarks.
  2. **Cellular 2-Photon & Neuropixels Controls**: Single-cell `2P` imaging across dorsal areas and penetrating `Neuropixels` recordings spanning cortex, striatum, thalamus, hippocampus, and midbrain confirm that movement dominance holds at single-spike resolution and extends subcortically.
  3. **Dense Behavioral Tracking**: Two `30 Hz` infrared cameras (face + body motion-energy SVDs), ultrasonic microphone, whisker optical sensor, handle touch/force piezos, rotary wheel, pupil diameter, and dual lick detectors.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: `10`-fold cross-validation across trials (`musall/ridgeModel`), constructing time-lagged design matrices (raised-cosine / boxcar event kernels for `task` variables + analog sensors + top `200` face/body video SVDs) to predict temporal SVD traces `V(t)` via per-component ridge penalties learned by nested empirical Bayes / CV.
- **Critical Modeling Pitfalls**:
  1. **Never Confuse Marginal `cvR²` with Unique `ΔR²`**: Because mice systematically adjust whisker/body posture right at stimulus onset and during the memory delay ("task-aligned uninstructed movements"), a model containing *only* task regressors absorbs movement variance and yields falsely inflated cognitive `cvR²`. Always report **$\Delta R^2_k = R^2_{\text{full}} - R^2_{\text{full} \setminus k}$** alongside marginal `cvR²`!
  2. **Fit Ridge Models in `200-D` SVD Space (`V`), Then Reconstruct `U · B̂`**: Fitting pixelwise across `540 × 640 = 345,600` pixels wastes orders of magnitude of RAM/compute; fitting in orthonormal SVD temporal space `V` is mathematically exact under isotropic ridge regularization and allows instant dorsal-cortex map projection via `U`.
  3. **Hemodynamic `405 nm` Subtraction**: Ensure the `405 nm` violet channel regression has been applied (`Vc` hemodynamically corrected components) so slow `0.1–2 Hz` vasomotion waves are not misattributed to neural state drift.

## 4. Programmatic Download & Quickstart
```bash
# Clone the official Churchland Lab ridge-regression & SVD widefield pipeline
git clone https://github.com/musall/ridgeModel.git
# Dataset archive is permanently hosted at Cold Spring Harbor Laboratory (DOI: 10.14224/1.38599):
curl -sLI https://doi.org/10.14224/1.38599 | grep -iE "^(http|location)"
```

## 5. Verified Primary References
- **`musall2019single`**: Musall, S., Kaufman, M. T., Juavinett, A. L., Gluf, S., & Churchland, A. K. (2019). *Single-trial neural dynamics are dominated by richly varied movements*. Nature Neuroscience, 22(10), 1677–1686 (`10.1038/s41593-019-0502-4`).
