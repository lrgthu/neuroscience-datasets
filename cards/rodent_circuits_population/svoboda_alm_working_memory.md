# Svoboda Lab Mouse ALM Working-Memory & Brain-Wide Movement Map (`DANDI:000363` & `CRCNS:alm-5`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: The gold-standard experimental testbed for **mechanistic recurrent neural network (`RNN`) models of short-term memory, attractor dynamics, causal optogenetic perturbations, and Go-cue state-space reorganization** (`Inagaki et al., Nature, 2019`; `Chen, Liu, Wang, ..., Druckmann, Li & Svoboda, Cell, 2024`).
- **Delayed Directional Licking Paradigm**: Head-fixed mice discriminate a sensory `Sample` stimulus (`1.0–1.3 s` tactile pole position or auditory tone frequency), maintain a binary motor plan (`Lick Left` vs. `Lick Right`) across a memory `Delay` epoch (`1.2–2.0 s` fixed or exponentially distributed random delay) without moving the tongue, and execute directional licking immediately upon a `3 kHz` auditory `Go` cue.
- **Two Interlocking Open Releases**:
  1. **ALM Discrete Attractor & Perturbation Benchmark (`CRCNS:alm-5` / `Figshare:10.25378/janelia.7489253` — `Inagaki et al., Nature, 2019`)**: Extracellular `64`-channel silicon-probe and whole-cell membrane-potential (`V_m`) recordings in `ALM` across **fixed-delay** and **random-delay** schedules, paired with transient sub-second `VGAT-ChR2-EYFP` photoinhibition showing funnels back to discrete choice fixed points (plus occasional basin switches predicting behavioral errors).
  2. **Mesoscale Brain-Wide Memory-Guided Movement Map (`DANDI:000363` — `Chen et al., Cell, 2024`; companion `DANDI:000221` & `DANDI:000009`)**: Simultaneous multi-probe Neuropixels recordings (`>65,000` neurons across `ALM`, motor thalamus `VM/VAL/MD`, striatum, `SNr`, superior colliculus `SCm`, midbrain reticular nucleus `MRN`, deep cerebellar nuclei, pons, and medulla) combined with `ALM` photoinactivation and `300–400 Hz` two-camera orofacial pose tracking.

## 2. Recording Specifications & Preprocessing
- **Coding Direction (`CD`) & Mode Geometry**: Population dynamics cleanly decompose into orthogonal linear subspaces: the **Choice Coding Direction (`CD_delay`)** separating `Left` vs. `Right` motor plans during the delay, a **Non-Selective Ramping Mode** tracking temporal urgency toward the `Go` cue (`DANDI:000221`), and a **Movement Execution Subspace (`CD_response`)** into which `CD_delay` rapidly collapses within `~50 ms` of the `Go` cue (`Chen et al., 2024`).
- **Standardized NWB Access (`DANDI:000363`)**: Includes spike-sorted single units (`Kilosort` + strict unit QC), 3D `CCFv3` electrode coordinates reconstructed from cleared-brain light-sheet microscopy, trial structure (`sample`, `delay`, `go_cue`, `photostim` onset/power), lickport contact times, and high-speed `DeepLabCut` tongue/jaw/nose trajectories.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Fit multi-region or single-region RNNs/state-space models on **unperturbed control trials** (`80/20` trial split), then test **zero-shot causal generalization** on held-out unilateral and bilateral **delay-epoch photoinhibition trials** (predicting both post-perturbation neural recovery trajectories and behavioral error rates).
- **Critical Modeling Pitfalls**:
  1. **Fixed-Delay Integrator Ambiguity**: Standard line-attractor / leaky-integrator RNNs and discrete two-point attractor RNNs look nearly identical on fixed-delay `PSTH` averages; always evaluate candidate dynamical models on **random-delay trials** (where persistent selectivity plateaus early without ramping) and **perturbation trials** (`alm-5`).
  2. **Filter Early-Lick & Disengaged Trials**: Exclude trials with premature licks prior to the `Go` cue (`early_lick == 1`) and no-response blocks when estimating `CD_delay` projections.
  3. **Stream `DANDI:000363` Selectively**: Because `DANDI:000363` bundles `~65.7 TB` across `174` NWB assets (including raw video/electrophysiology), use `remfile` + `h5py`/`pynwb` byte-range streaming to pull `units` and `trials` tables in megabytes rather than downloading raw terabyte files.

## 4. Programmatic Download & Quickstart
```bash
# Stream NWB metadata from DANDI:000363 (Mesoscale Brain-Wide ALM Map) & DANDI:000221 (Go-Cue Loop)
uvx dandi ls DANDI:000363 | head -n 8
uvx dandi ls DANDI:000221 | head -n 5
# Inagaki et al. 2019 ALM discrete attractor MAT archive (~2 GB):
# https://doi.org/10.25378/janelia.7489253
```

## 5. Verified Primary References
- **`chen2024brainwide`**: Chen, S., Liu, Y., Wang, Z. A., Colonell, J. I., Liu, L. D., Hou, H., Tien, N.-W., Wang, T., Harris, T. D., Druckmann, S., Li, N., & Svoboda, K. (2024). *Brain-wide neural activity underlying memory-guided movement*. Cell, 187(3), 676–691.e16 (`10.1016/j.cell.2023.12.035`).
- **`inagaki2019discrete`**: Inagaki, H. K., Fontolan, L., Romani, S., & Svoboda, K. (2019). *Discrete attractor dynamics underlies persistent activity in the frontal cortex*. Nature, 566, 212–217 (`10.1038/s41586-019-0919-7`).
