# Buzsáki Lab Hippocampal-Entorhinal Silicon-Probe Databank (`CellExplorer`, `hc-3`, `hc-11` & `DANDI`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: The most widely used open benchmark ecosystem for **hippocampal spatial coding, theta phase precession, sharp-wave ripple (`SWR`) memory replay, monosynaptic microcircuit inference, and self-supervised latent manifold learning** (`Mizuseki et al., Nature Neuroscience, 2011`; `Grosmark & Buzsáki, Science, 2016`; `Petersen & Buzsáki, Neuron, 2020`; `Petersen et al., Neuron, 2021`).
- **Flagship Sub-Collections**:
  1. **`CRCNS:hc-11` / `DANDI:000044` (`Grosmark & Buzsáki, Science, 2016` — Canonical `CEBRA` Rat Hippocampus Benchmark)**: Bilateral `128`-channel silicon-probe recordings in dorsal `CA1` of `4` Long-Evans rats (`Achilles`, `Buddy`, `Cicero`, `Gatsby`, `~50–120+` simultaneous single units/session) spanning `Pre-Sleep` (`~2–3 h`), **novel linear/circular track learning** (`~45–90 min`), and `Post-Sleep` (`~2–3 h`). Adopted in `CEBRA` (`Schneider, Lee & Mathis, Nature, 2023`) as the standard `1D × Direction` nonlinear topological embedding benchmark.
  2. **`CRCNS:hc-3` (`Mizuseki et al., 2011/2013`)**: `>7,700` single units across `11` rats recorded simultaneously in `CA1`, `CA3`, `DG`, and medial entorhinal cortex (`MEC Layers 2, 3, 5`) across open-field foraging, linear tracks, T-maze alternation, wheel running, and REM/non-REM sleep.
  3. **`DANDI:000059` (`Petersen & Buzsáki, Neuron, 2020`) & `DANDI:000003` (`Senzai & Buzsáki`)**: Reversible medial-septum cooling experiments (`51` NWB files, `~3.06 TB`) dissociating theta oscillation frequency from internal cell-assembly phase lags, plus laminar dentate gyrus granule vs. mossy cell identification (`101` NWB files, `~1.89 TB`).
  4. **`CellExplorer` Public Databank (`Petersen et al., Neuron, 2021`)**: Standardized `.cell_metrics.cellinfo.mat` and NWB tables across `>400` sessions (`rats` and `mice`), providing uniform waveform, burstiness, theta/ripple modulation, and short-latency (`1–4 ms`) spike cross-correlogram (`CCG`) ground-truth excitatory/inhibitory labels.

## 2. Recording Specifications & Preprocessing
- **Electrophysiology & State Annotations**: Broadband `20 kHz` or `30 kHz` recordings paired with `1,250 Hz` LFP, automated brain-state scoring (`WAKE`, `NREM`, `REM`), detected sharp-wave ripple events (`140–250 Hz` `CA1` pyramidal-layer envelope peaks), theta phase (`Hilbert` transform of `4–12 Hz` LFP), and dual-LED `2D`/OptiTrack `3D` head position & head orientation.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: For `hc-11` (`DANDI:000044`) manifold/decoding benchmarks (`CEBRA` protocol), bin spikes at `25 ms`, filter for active running (`speed > 5–10 cm/s`), and use `3`-fold contiguous temporal splits (`train`/`valid`/`test` over active laps) evaluating `kNN` or linear position + running-direction `R²` / median decoding error (`cm`) and persistent cohomology (`Betti` numbers).
- **Critical Modeling Pitfalls**:
  1. **Directional Splitting of 1D Place Fields**: On linear tracks, `CA1` pyramidal cells form largely orthogonal place maps for `Left -> Right` vs. `Right -> Left` runs, yielding a topological **cylinder / figure-8 loop** rather than a single undirected line segment—always evaluate `(position, direction)` jointly!
  2. **Immobility Ripple Replay vs. Theta Coding**: During reward port stops (`speed ≈ 0`), `CA1` fires compressed `50–100 ms` `SWR` trajectories sweeping across remote track locations; treating immobile time bins as "true current position" corrupts supervised encoders and inflates apparent decoding error.
  3. **Separate Pyramidal Cells from Fast-Spiking Interneurons**: Interneurons fire at `15–60 Hz` across the entire track and dominate unnormalized PCA/Poisson likelihoods unless identified via `CellExplorer` `putativeCellType` (`Pyramidal Cell` vs. `Narrow Interneuron` / `Wide Interneuron`).

## 4. Programmatic Download & Quickstart
```bash
# Download the NWB release of Grosmark & Buzsáki 2016 (hc-11 / CEBRA rat hippocampus benchmark, ~73 GB total or single-rat slice)
uvx dandi ls DANDI:000044
# Example: fetch Achilles novel linear-track NWB file only
uvx dandi download https://api.dandiarchive.org/api/dandisets/000044/versions/draft/assets/?path=sub-Achilles
```

## 5. Verified Primary References
- **`petersen2021cellexplorer`**: Petersen, P. C., Siegle, J. H., Steinmetz, N. A., Mahallati, S., & Buzsáki, G. (2021). *CellExplorer: A framework for visualizing and characterizing single neurons*. Neuron, 109(22), 3594–3608.e2 (`10.1016/j.neuron.2021.09.002`).
- **`grosmark2016diversity`**: Grosmark, A. D., & Buzsáki, G. (2016). *Diversity in neural firing dynamics supports both rigid and learned hippocampal sequences*. Science, 351(6280), 1440–1443 (`10.1126/science.aad1935`).
- **`petersen2020cooling`**: Petersen, P. C., & Buzsáki, G. (2020). *Cooling of medial septum reveals theta phase lag coordination of hippocampal cell assemblies*. Neuron, 107(4), 731–744.e3 (`10.1016/j.neuron.2020.05.023`).
- **`mizuseki2011hippocampal`**: Mizuseki, K., Diba, K., Pastalkova, E., & Buzsáki, G. (2011). *Hippocampal CA1 pyramidal cells form functionally distinct sublayers*. Nature Neuroscience, 14, 1174–1181 (`10.1038/nn.2894`).
