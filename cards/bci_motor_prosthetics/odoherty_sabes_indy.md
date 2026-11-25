# Sabes Lab Chronic Macaque M1/S1 Random-Grid Reaching (`Sabes-Indy-Loco` / `Zenodo:583331`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: A `47-session` longitudinal sensorimotor electrophysiology archive (`37` sessions from monkey **`Indy`** spanning ~`10 months`; `10` sessions from monkey **`Loco`**) capturing continuous, self-paced point-to-point reaching without artificial delay periods or center-out return resets (`O'Doherty, Cardoso, Makin, & Sabes, 2017`; `Makin et al., J. Neural Eng., 2018`).
- **Benchmark Role in Neural Foundation Models**: Serves both as the source of `NLB MC_RTT` (`Indy` single session) and as a flagship multi-session pretraining/transfer corpus for **`POYO`** (`Azabou et al., NeurIPS 2023`) and **`NDT2`** (`Ye et al., NeurIPS 2023`).

## 2. Recording Specifications & Preprocessing
- **Implant & Channels**: Chronic `96-channel` Utah microelectrode array in primary motor cortex (`M1`) across all sessions, supplemented by a second `96-channel` array in primary somatosensory cortex (`S1`, `192` channels total) in subset `Indy` and all `Loco` sessions.
- **Data Contents (`.mat` HDF5 v7.3 & `brainsets`/NWB)**:
  - `spikes`: Cell array `(N_channels × N_units)` of exact `24.414 kHz` spike timestamps (`unit 1` = unsorted threshold crossings; `units 2–5` = sorted single units) plus `wf` action-potential waveform snippets.
  - `finger_pos` & `target_pos`: Continuous `250 Hz` (`4 ms`) fingertip `(x, y, z)` kinematics (electromagnetic tracker) and active target coordinates.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Evaluation Protocol**: Causal or sliding-window (`e.g., 100–1,000 ms` history) decoding of `2D` `(vx, vy)` fingertip velocity evaluated via variance-weighted **$R^2$** on contiguous chronological held-out segments (`20%` tail of each session) or held-out sessions via few-shot unit-embedding calibration.
- **Critical Modeling Pitfalls**:
  1. **Strict Contiguous Temporal Splits**: Because reaching is continuous (`target k+1` spawns the instant `target k` is acquired), sliding `1 s` windows overlap in both neural history and arm inertia. Always split each session into contiguous chronological `train / val / test` blocks with a `≥ 2 s` buffer zone at split boundaries.
  2. **Differentiate Causal (`M1`) vs. Reafferent (`S1`) Latencies**: `S1` neurons peak *after* movement onset (`+20 to +80 ms` proprioceptive feedback), whereas `M1` neurons lead velocity (`-100 to -50 ms`); acausal bidirectional transformers leverage `S1` feedback that is unavailable to zero-lag causal BCI controllers unless explicitly modeled.
  3. **Handle Cross-Session Unit Turnover**: Never assume sorted unit `c, u` on Session `t` is the identical physical neuron on Session `t + 30 days`; use session-specific unit tokens (`POYO`) or unsorted channel-level multi-unit activity (`Makin et al., 2018`).

## 4. Programmatic Download & Quickstart
```bash
# Download all 47 Indy & Loco HDF5/.mat sessions from Zenodo (CC-BY-4.0)
uvx zenodo_get 10.5281/zenodo.583331
```

## 5. Verified Primary References
- **`odoherty2017sabes`**: O'Doherty, J. E., Cardoso, M. M. B., Makin, J. G., & Sabes, P. N. (2017). *Nonhuman Primate Reaching with Multichannel Sensorimotor Cortex Electrophysiology*. Zenodo (`10.5281/zenodo.583331` / `10.5281/zenodo.788569`).
- **`makin2018sabes`**: Makin, J. G., O'Doherty, J. E., Cardoso, M. M. B., & Sabes, P. N. (2018). *Superior arm-movement decoding from cortex with a new, unsupervised-learning algorithm*. Journal of Neural Engineering (`10.1088/1741-2552/aa9e95`).
- **`azabou2023poyo`**: Azabou, M., Arora, V., Ganesh, V., Mao, X., Nachimuthu, S., Mendelson, M., et al. (2023). *A Unified, Scalable Framework for Neural Population Decoding*. NeurIPS (`arXiv:2310.16046`).
- **`ye2023ndt2`**: Ye, J., Collinger, J. L., Wehbe, L., & Gaunt, R. (2023). *Neural Data Transformer 2: Multi-context Pretraining for Neural Spiking Activity*. NeurIPS (`10.52202/075280-3523`).
