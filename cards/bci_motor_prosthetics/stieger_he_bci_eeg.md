# Stieger & He 62-Subject Multi-Session Continuous 2D Motor-Imagery BCI EEG (`Figshare:13123148`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Resolves the chronic scarcity of **longitudinal, multi-session closed-loop scalp BCI** data by releasing **`>600 hours`** of `1,000 Hz` high-density EEG across **`62` healthy adults**, **`598` sessions** (`7–11` sessions per participant spanning weeks), and **`>250,000` trials** (`Stieger, Engel, & He, Scientific Data, 2021`).
- **Closed-Loop 1D & 2D Cursor Control Tasks (`~450` trials/session)**:
  1. **`LR` (1D Horizontal)**: Left-hand vs. right-hand motor imagery driving left/right cursor velocity.
  2. **`UD` (1D Vertical)**: Bilateral both-hands motor imagery (up) vs. voluntary rest/relaxation (down).
  3. **`2D` (4-Target Continuous Control)**: Simultaneous horizontal and vertical sensorimotor-rhythm (`SMR`) modulation steering a cursor to top, bottom, left, or right peripheral targets.

## 2. Recording Specifications & Preprocessing
- **Hardware & Signal Quality**: `64-channel` Neuroscan `SynAmps RT` cap (`62` scalp `10–10` EEG electrodes + `2` EOG channels, bandpass `0.5–200 Hz`, `60 Hz` notch, sampled at **`1,000 Hz`**), distributed as self-contained `.mat` session structures on Figshare (`10.6084/m9.figshare.13123148`), BIDS-EEG on NEMAR/OpenNeuro, and natively loadable via `moabb.datasets.Stieger2021`.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Longitudinal & Foundation-Model Benchmark**: Ideal testbed for **human-in-the-loop co-adaptation** (tracking within-subject `mu` `8–14 Hz` desynchronization sharpening from Session `1` to Session `11`), **cross-session domain adaptation**, and **large-scale EEG foundation pretraining**.
- **Critical Modeling Pitfalls**:
  1. **Disentangle Sensorimotor Rhythm (`SMR`) from Closed-Loop Visual Pursuit / `EOG`**: Because real-time cursor movement is visible on screen throughout the feedback phase, horizontal/vertical smooth-pursuit eye movements (`EOG`) and parieto-occipital visual motion responses correlate with cursor velocity. Always inspect spatial topographies (`C3/C4` sensorimotor dipoles vs. frontal eye-field/ocular artifacts) and regress/reject EOG components.
  2. **Early-Termination Trial Length Bias**: Fast BCI learners hit `LR` targets in `<2.0 s` whereas harder `UD`/`2D` trials run closer to the `6.0 s` timeout; zero-padding variable-length trials leaks target identity via padding masks! Standardize fixed-duration epochs (e.g., `t ∈ [0.5, 2.5] s` post-feedback onset) for balanced 4-class classification, or switch to causal `100 ms` step-wise cursor-velocity regression.
  3. **Respect `MBSR` Behavioral Stratification**: Account for the randomized mindfulness (`MBSR`) vs. wait-list control cohort indicator in participant metadata when analyzing between-subject BCI illiteracy and learning rates.

## 4. Programmatic Download & Quickstart
```bash
# Download via MOABB (Stieger2021) or directly from Figshare (10.6084/m9.figshare.13123148)
uv pip install moabb
python -c "from moabb.datasets import Stieger2021; Stieger2021().download()"
```

## 5. Verified Primary References
- **`stieger2021bci`**: Stieger, J. R., Engel, S. A., & He, B. (2021). *Continuous sensorimotor rhythm based brain computer interface learning in a large population*. Scientific Data (`10.1038/s41597-021-00883-1`).
- **`jayaram2018moabb`**: Jayaram, V., & Barachant, A. (2018). *MOABB: trustworthy algorithm benchmarking for BCIs*. Journal of Neural Engineering (`10.1088/1741-2552/aadea0`).
