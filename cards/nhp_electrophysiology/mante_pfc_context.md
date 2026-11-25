# Mante-Sussillo-Newsome Macaque PFC Context-Dependent Integration Dataset (`Mante2013-PFC` / *Nature* 2013)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Arguably the single most influential dataset bridging **recurrent neural network (`RNN`) dynamical-systems theory** and **prefrontal neurophysiology** (`Mante, Sussillo, Shenoy & Newsome, Nature, 2013`). Demonstrated that peri-arcuate prefrontal cortex (`PFC`/`FEF`) does *not* gate out irrelevant sensory inputs prior to PFC; instead, both relevant and irrelevant sensory streams enter PFC, where **context shifts the network along a slow line attractor so non-normal recurrent dynamics (`left` selection vectors vs. `right` readout vectors) selectively integrate only the context-relevant input**.
- **Behavioral Paradigm (`750 ms` Dual-Feature Random-Dot Integration)**:
  - Two adult male rhesus macaques (`Monkey A` and `Monkey F`) view colored, moving random-dot kinematograms (`750 ms` duration) following an explicit fixation context cue (`Motion Context` vs. `Color Context`), then execute a saccade to the matching color or motion target after a variable delay.
  - Systematically sweeps `6` signed motion coherences × `6` signed color coherences × `2` task contexts (`72` condition combinations).

## 2. Recording Specifications & Preprocessing
- **Electrophysiology**: `762` well-isolated single units recorded in and around the anterior bank of the arcuate sulcus (`FEF` / posterior dorsolateral `PFC`) using tungsten microelectrodes (`Monkey A` and `Monkey F`), openly distributed in `.mat` archives by the Mante Lab (`INI UZH`).
- **Targeted Dimensionality Reduction (`TDR`)**: Denoises neuronal firing rates via top-`12` principal components, fits per-neuron multivariable linear regressions against `[choice, motion, color, context]`, and orthogonalizes (`QR` decomposition) the time-invariant regression beta vectors to define interpretable 4D state-space axes (`choice`, `motion`, `color`, `context`).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Benchmarking Task-Trained RNNs (`Procrustes`, `SVCCA`, `CKA`, `DSA` / Ostrow et al.)**: Standard testbed for comparing architectural priors (vanilla `tanh` RNNs, `GRU`/`LSTM`, low-rank RNNs `Mastrogiuseppe & Ostojic`, Dale's-law excitatory/inhibitory RNNs) on topological fixed-point structure (`2` parallel context-shifted line attractors) and dynamical similarity.
- **Critical Modeling Pitfalls**:
  1. **Pseudopopulation Constraint (Sequential Recordings)**: Because units were not recorded simultaneously on a single 762-channel array, trial-shuffling across sessions preserves the condition-averaged `72`-trajectory tensor `(N_units × T_bins × N_conditions)` while destroying inter-neuronal trial-to-trial covariance—never fit single-trial `LFADS` co-smoothing here (use `NLB-21` or `SiegelMiller6Area` for simultaneous single-trial latents).
  2. **Separate `Monkey A` and `Monkey F` Before Pooling**: Firing-rate baselines, exact coherence levels, and unit counts differ between `Monkey A` and `Monkey F`; verify that geometric or dynamical claims replicate independently in both animals!
  3. **Non-Normal Amplification Requires Inspecting Left Eigenvectors**: Symmetric similarity metrics (`CKA`/`RSA`) on time-averaged rates can conflate distinct dynamical mechanisms (early input gating vs. late selection-vector relaxation)—evaluate vector-field Jacobians or **Dynamical Similarity Analysis (`DSA`)**.

## 4. Programmatic Download & Quickstart
```bash
# Open-access MATLAB (.mat) unit archives hosted by Valerio Mante's group at INI (ETH / UZH):
open "https://www.ini.uzh.ch/en/research/groups/mante/data.html"
```

## 5. Verified Primary References
- **`mante2013pfc`**: Mante, V., Sussillo, D., Shenoy, K. V., & Newsome, W. T. (2013). *Context-dependent computation by recurrent dynamics in prefrontal cortex*. Nature (`10.1038/nature12742`).
