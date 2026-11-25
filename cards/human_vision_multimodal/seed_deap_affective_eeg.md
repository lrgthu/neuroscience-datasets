# SEED & DEAP Multimodal Affective Video/Music EEG Suite (`SEED / DEAP`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: **SEED** (`Zheng & Lu, IEEE TAMD, 2015`) and **DEAP** (`Koelstra et al., IEEE TAFFC, 2012`) are the two standard downstream evaluation benchmarks for **affective computing**, **EEG foundation model probing** (`LaBraM`, `BIOT`, `CBraMod`, `EEGPT`), **non-stationary cross-session/cross-subject transfer learning**, and **EEG + eye-tracking / peripheral physiological fusion**.
- **Suite Components (`Combined N = 47`, `55` Audiovisual Clips)**:
  1. **SJTU `SEED` (`N = 15` subjects × `3` sessions = `45` recordings)**:
     - Subjects (`7` male, `8` female) watched **`15` Chinese emotional film clips** (`~4 min` each; `5` Positive, `5` Neutral, `5` Negative; `5 s` hint + `~4 min` clip + `45 s` self-assessment + `15 s` rest).
     - Each participant repeated the entire experiment across **`3` separate sessions** spaced `≥1 week` apart (`12` of `15` subjects also have simultaneous **SMI eye-movement features**; extended in `SEED-IV` 4-class and `SEED-V` 5-class releases).
  2. **QMUL `DEAP` (`N = 32` subjects)**:
     - Subjects watched **`40` one-minute music video highlights** (`3 s` pre-trial baseline + `60 s` video) selected across the four quadrants of Russell's Valence–Arousal circumplex, rating each clip continuously (`1–9` Self-Assessment Manikin) on **Valence, Arousal, Dominance, and Liking** (`22` subjects also have frontal face video).

## 2. Recording Specifications & Preprocessing
- **`SEED` Hardware & Released Features**: `62`-channel ESI NeuroScan (`10-20` layout, `1,000 Hz` raw → `200 Hz` downsampled, `0–75 Hz` bandpass `.mat` files) + pre-extracted **Differential Entropy (`DE`)**, `PSD`, `DASM`, and `RASM` features across `5` canonical bands ($\delta$: `1–3 Hz`, $\theta$: `4–7 Hz`, $\alpha$: `8–13 Hz`, $\beta$: `14–30 Hz`, $\gamma$: `31–50 Hz`).
- **`DEAP` Hardware & Released Features**: `32`-channel BioSemi ActiveTwo EEG + `8` peripheral physiological channels (`hEOG`, `vEOG`, `zEMG`, `tEMG`, `GSR`, plethysmograph `BVP`, respiration, skin temperature) in both raw `512 Hz` `.bdf` and preprocessed `128 Hz` (`4.0–45.0 Hz`, EOG-removed, `[40 × 40 × 8064]` Python `.dat` / MATLAB `.mat` tensors).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Uncontaminated Evaluation Protocols**:
  - **SEED Within-Session**: Train on the **first `9` movie trials** (`3` Pos, `3` Neu, `3` Neg) and test on the **last `6` movie trials** (`2` Pos, `2` Neu, `2` Neg).
  - **SEED Cross-Session**: Train on Session 1, test on Session 2 and Session 3 (`≥7 days` electrode re-application drift).
  - **SEED / DEAP Cross-Subject (`LOSO`)**: Leave-one-subject-out across all `15` (`SEED`) or `32` (`DEAP`) subjects without target-subject label leakage.
- **Critical Modeling Pitfalls**:
  1. **Ban Random Epoch-Level K-Fold Splits**: Slicing `60 s` (`DEAP`) or `240 s` (`SEED`) videos into `1 s` windows and randomly assigning adjacent seconds to train and test leaks continuous session/trial state (`>98%` fake accuracy!). Group splits **strictly by `trial_id`, `session_id`, or `subject_id`**.
  2. **Pre-Trial Baseline Removal (`DEAP`)**: Subtract the `3 s` (`384` samples at `128 Hz`) pre-trial baseline power/DE per channel before pooling across the `60 s` (`7,680` samples) stimulus window (`InvBase` standard).
  3. **High-Frequency Facial EMG**: Frontal/temporal $\beta/\gamma$ (`14–50 Hz`) dominance in SEED partially reflects subtle facial expression muscle tone (`zEMG`/`tEMG` in DEAP explicitly tracks this)—verify pure cortical contributions via spatial/topographic inspection or ICA pruning.

## 4. Programmatic Download & Quickstart
```python
# After downloading licensed archives from SJTU BCMI (SEED) & QMUL (DEAP), load cleanly via TorchEEG:
from torcheeg.datasets import SEEDDataset, DEAPDataset
from torcheeg import transforms

seed_ds = SEEDDataset(root_path="./Preprocessed_EEG", chunk_size=200, overlap=0)
deap_ds = DEAPDataset(root_path="./data_preprocessed_python", chunk_size=128, baseline_num=3)
```

## 5. Verified Primary References
- **`zheng2015seed`**: Zheng, W.-L., & Lu, B.-L. (2015). *Investigating critical frequency bands and channels for EEG-based emotion recognition with deep neural networks*. IEEE Transactions on Autonomous Mental Development (`10.1109/TAMD.2015.2431497`).
- **`koelstra2012deap`**: Koelstra, S., Mühl, C., Soleymani, M., et al. (2012). *DEAP: A database for emotion analysis using physiological signals*. IEEE Transactions on Affective Computing (`10.1109/T-AFFC.2011.15`).
