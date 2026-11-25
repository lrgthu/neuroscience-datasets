# Peyrache & Buzsáki Thalamocortical Head-Direction Ring Dataset (`CRCNS:th-1` / `DANDI:000056`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: The textbook mammalian **1D Continuous Ring Attractor ($S^1$)** dataset (`Peyrache, Lacroix, Petersen & Buzsáki, Nature Neuroscience, 2015`), simultaneously recording thalamic (`ADn`) and cortical (`PoSub`) head-direction ensembles across **awake foraging, `REM` sleep, and `Slow-Wave Sleep (SWS)`** in `7` freely moving mice (`42` sessions, `~122.8 GB` standardized NWB release on `DANDI:000056`).
- **Why Computational Modelers Love `th-1`**: Because a single session (such as the famous **`Mouse12-120806`** benchmark shipped in `Pynapple` and `scikit-tda` tutorials) cleanly yields `~20–40` low-noise, full-circle-tiling `ADn` + `PoSub` HD cells in megabytes, `th-1` is the universal sanity-check oracle for testing nonlinear dimensionality reduction (`Isomap`, `UMAP`, `GPLVM`, `LFADS`, `CEBRA`), topological data analysis ($\beta_0 = 1, \beta_1 = 1$), and Bayesian sleep-state decoding before scaling to 2D toroidal or high-dimensional cortical datasets.

## 2. Recording Specifications & Preprocessing
- **Simultaneous Thalamocortical Probes**: Chronically implanted silicon probes in the **anterodorsal thalamic nucleus (`ADn`, `4`- or `8`-shank)** and **postsubiculum (`PoSub` / dorsal presubiculum, `8`-shank `64`-site)** sampled at `20 kHz` (spikes) and `1,250 Hz` (`LFP`), accompanied by `39.06 Hz` overhead dual-LED tracking (`x`, `y`, and head azimuth `θ ∈ [0, 2π)`) and curated sleep-stage intervals (`WAKE`, `REM`, `SWS`, plus `PoSub` `UP`/`DOWN` state transitions).
- **Dual Repository Access**: Available both in legacy Klusters/NeuroSuite `.res/.clu/.fet` + MATLAB format on `CRCNS:th-1` and as ready-to-load **NWB 2.0** files on **`DANDI:000056`** (`42` NWB files).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**:
  1. **Supervised / Semi-Supervised Angular Decoding**: Contiguous `50/50` or `5`-fold temporal block split of active `Wake` foraging (`bin_size = 50–200 ms`), evaluating circular mean absolute error (`atan2(sin(θ̂ - θ), cos(θ̂ - θ))`, typical Bayesian ceiling `~8–15°`).
  2. **Unsupervised Wake $\to$ Sleep Ring Transfer**: Fit `S¹` manifold or tuning curves on `Wake` only; verify preservation of pairwise angular tuning offsets and coherent virtual-head-direction trajectories in `REM` and `SWS`.
- **Critical Modeling Pitfalls**:
  1. **`10×` Temporal Compression & `DOWN`-State Silences in `SWS`**: During `REM`, virtual head direction sweeps at `1×` awake speed (`bin_size = 100–200 ms` works well). During `SWS`, thalamic-cortical coordination accelerates `~10-fold` (`bin_size = 10–20 ms` required!) and intermittently collapses during cortical `DOWN` states—filter out low-spike `DOWN` bins before running `Isomap` or `Ripser`, otherwise a central zero-firing hub fills the ring's hole!
  2. **Use Circular Loss Functions**: Always parameterize target angles as unit vectors $(\cos \theta, \sin \theta) \in \mathbb{R}^2$ or optimize von Mises log-likelihood; naive scalar regression on `[0, 2π)` fails catastrophically at the `0 / 2π` wrap-around boundary.
  3. **Respect `ADn` Anticipatory Time Shift (`~25 ms`)**: Thalamic `ADn` HD cells fire `~20–25 ms` ahead of instantaneous head direction (`anticipatory time interval`), whereas cortical `PoSub` HD cells track near-zero lag and carry conjunctive spatial modulation near arena walls.

## 4. Programmatic Download & Quickstart
```bash
# List and download NWB sessions from DANDI:000056 (e.g., canonical Mouse12-120806 session)
uvx dandi ls DANDI:000056 | head -n 8
uvx dandi download https://api.dandiarchive.org/api/dandisets/000056/versions/draft/assets/?path=sub-Mouse12
```

## 5. Verified Primary References
- **`peyrache2015internally`**: Peyrache, A., Lacroix, M. M., Petersen, P. C., & Buzsáki, G. (2015). *Internally organized mechanisms of the head direction sense*. Nature Neuroscience, 18(4), 569–575 (`10.1038/nn.3968`).
