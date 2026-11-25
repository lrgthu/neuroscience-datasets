# Freeman-Ziemba-Movshon Macaque V1 vs. V2 Naturalistic Texture Benchmark (`FreemanZiemba2013` / *Nature Neuroscience* 2013)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Solved a decades-long puzzle in visual systems neuroscience by identifying a sharp, quantitative physiological signature distinguishing primate **area V2** from **primary visual cortex (V1)** (`Freeman, Ziemba, Heeger, Simoncelli & Movshon, Nature Neuroscience, 2013`), and serves as the canonical early-visual (`V1` & `V2`) neural benchmark in **Brain-Score**.
- **Controlled Statistical Stimulus Design (`300` Images = `15 × 2 × 10`)**:
  - Starting from `15` grayscale natural texture photographs (e.g., bark, scales, pebbles, honeycomb, water), **Portilla–Simoncelli steerable-pyramid synthesis** generates `10` stochastic **naturalistic texture** realizations matching joint cross-orientation, cross-scale, and cross-position magnitude/phase correlations, alongside `10` **spectrally matched noise** realizations matching *only* the global 2D Fourier power spectrum (and pixel luminance histogram).
  - Presented in a `4°` raised-cosine aperture (`100 ms` ON + `100 ms` blank ISI, `20` pseudorandom repeats per image) centered individually on every isolated neuron's receptive field.

## 2. Recording Specifications & Preprocessing
- **Electrophysiology**: Quartz-platinum-tungsten single-unit extracellular microelectrode recordings from `102` `V1` single units and `103` `V2` single units (`205` units total across `13` opiate-anesthetized, paralyzed adult macaques: `2` *Macaca nemestrina* and `11` *Macaca fascicularis*, matched across eccentricities).
- **Brain-Score Assembly (`FreemanZiemba2013.public` / `movshon.FreemanZiemba2013.{V1,V2}-pls`)**: Packaged as millisecond-binned (`10 ms` / time-averaged `[50, 200] ms`) labeled `xarray` `NeuroidAssembly` objects with stimulus family, texture-vs-noise condition, sample ID, and neuron region metadata.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Stratified cross-validation **grouped by `texture_family`** (`15` families; Brain-Score `.public` exposes `9` families = `180` stimuli or `135` public split stimuli while holding out private families for leaderboard scoring).
- **Critical Modeling Pitfalls**:
  1. **Stratify Strictly by Texture Family**: Two stochastic Portilla–Simoncelli samples from the same texture family have virtually identical summary statistics by construction; splitting across random `image_id` rather than `texture_family` turns out-of-distribution generalization into trivial memorization of 15 family centroids.
  2. **Check the Mechanistic Dissociation (`TMI`), Not Just `PLS R`**: V1 neurons respond nearly identically to naturalistic textures and spectrally matched noise, whereas V2 neurons fire vigorously to higher-order naturalistic correlations (`Texture Modulation Index = (R_nat - R_noise) / (R_nat + R_noise)`). Always audit whether candidate architectures exhibit V1-like spectral invariance *in early layers* and V2-like cross-channel covariance selectivity *in second-stage layers*.
  3. **Latency Offset (`~10–15 ms` Delayed Modulation)**: In V2, higher-order texture selectivity emerges `~70–80 ms` post-onset (`~10–15 ms` after initial spectral onset response), providing a clean millisecond constraint for recurrent vs. feedforward V1→V2 circuits.

## 4. Programmatic Download & Quickstart
```bash
# Load public V1 & V2 single-unit xarray assembly via brainscore_vision
uv run python -c "import brainscore_vision as bsv; da = bsv.load_dataset('FreemanZiemba2013.public'); print(da.dims, da.sizes)"
```

## 5. Verified Primary References
- **`freeman2013v2`**: Freeman, J., Ziemba, C. M., Heeger, D. J., Simoncelli, E. P., & Movshon, J. A. (2013). *A functional and perceptual signature of the second visual area in primates*. Nature Neuroscience (`10.1038/nn.3402`).
