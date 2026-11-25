# Rust-DiCarlo Macaque V4 vs. IT Natural-Scene Selectivity & Tolerance Benchmark (`Rust2012` / *J. Neurosci.* 2012)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Resolved a classic theoretical paradox between hierarchical feature selectivity (which narrows tuning and *increases* sparseness) and position/scale invariance (which broadens tuning and *decreases* sparseness): across `300` natural scenes (`8°` diameter, grayscale), single units in awake macaque **`V4` (`n = 143`)** and **`IT` (`n = 142`)** maintain **statistically indistinguishable lifetime and population sparseness (`~0.35` Vinje–Gallant index)** because increases in higher-order feature-conjunction selectivity from V4 to IT are quantitatively balanced by matched increases in position/scale tolerance (`Rust & DiCarlo, Journal of Neuroscience, 2012`).
- **Paired Scrambled-Scene Control**: Alongside the `300` natural scenes (`100 ms` ON / `100 ms` OFF rapid serial presentation during passive fixation), a paired sub-experiment contrasts `50` intact natural scenes against `50` **Portilla–Simoncelli scrambled counterparts** that preserve local V1/V2 spectral and marginal wavelet statistics while destroying global object conjunctions—revealing strong scrambling-induced sparseness loss in `IT` but minimal change in `V4`.

## 2. Recording Specifications & Preprocessing
- **Electrophysiology**: Well-isolated single-unit tungsten microelectrode recordings from `143` `V4` neurons and `142` `IT` (anterior/central TE) neurons in `2` awake rhesus macaques (`~10–20` repeats per stimulus), complemented in **Brain-Score** (`dicarlo.Rust2012`) by both single-unit (`Rust2012.single`) and chronic array (`Rust2012.array`) benchmarks.
- **Canonical Response Window**: Spike counts integrated over `[70, 170] ms` post-stimulus onset (accounting for retinal-to-V4/IT conduction latency).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: 10-fold stratified cross-validation across the `300` natural scenes (unlike `MajajHong2015`'s synthetic 3D composites, `Rust2012` tests genuine ecological natural-scene clutter without pasted object boundaries).
- **Critical Modeling Pitfalls**:
  1. **Noise-Bias Correction for Sparseness Metrics**: Uncorrected sample sparseness $S \propto 1 - (\sum r_i / N)^2 / (\sum r_i^2 / N)$ is positively biased by single-trial Poisson shot noise; always apply asymptotic trial-variance debiasing before comparing model activation sparseness (ReLU/GELU/LayerNorm) against biological V4/IT sparseness!
  2. **Receptive-Field Centering vs. `8°` Full-Field Presentation**: Stimuli were presented centrally (`8°` subtense) around fixation rather than shifted onto every V4 neuron's individual eccentric receptive field; spatially localized readouts are essential for V4 (`~2°–4°` RFs) compared with broader IT (`>6°` RFs).
  3. **Provenance Hygiene**: Cite the verified DOI **`10.1523/jneurosci.6125-11.2012`** (*J. Neurosci.* 32(30):10170–10182), never unverified typo strings.

## 4. Programmatic Download & Quickstart
```bash
# Evaluate models against V4 & IT natural-scene single-unit/array assemblies via brainscore_vision
uv run python -c "import brainscore_vision as bsv; print([k for k in dir(bsv) if 'Rust' in k])"
```

## 5. Verified Primary References
- **`rust2012sparseness`**: Rust, N. C., & DiCarlo, J. J. (2012). *Balanced increases in selectivity and tolerance produce constant sparseness along the ventral visual stream*. Journal of Neuroscience (`10.1523/jneurosci.6125-11.2012`).
