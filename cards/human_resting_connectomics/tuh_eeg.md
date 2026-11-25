# Temple University Hospital EEG Corpus (`TUEG` / `TUAB` / `TUSZ` / `TUEV`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Plays the exact same foundational role for **scalp EEG foundation models** (`BENDR`, `BIOT`, `LaBraM` ICLR 2024, `EEGPT`, `CBraMod` ICLR 2025) that `UK Biobank` and `Open-fMIND` play for fMRI (`Obeid & Picone, Frontiers in Neuroscience, 2016`). Aggregates `>26,000–69,000` clinical EEG sessions (`>14,987` patients, `2002–present`, `>25,000 hours`) paired with free-text neurologist clinical reports and curated downstream benchmark corpora:
  - **`TUAB`** (*TUH Abnormal EEG*): Normal vs. pathological screening (`2,993` files, strict patient-disjoint train/eval split).
  - **`TUSZ`** (*TUH EEG Seizure*): Multi-class seizure onset/type detection & localization.
  - **`TUEV`** (*TUH EEG Events*): `6`-class clinical waveform classification (`SPSW`, `GPED`, `PLED`, `EYEM`, `ARTF`, `BCKG`).
  - **`TUAR` / `TUSL`**: Artifact and slowing benchmarks.

## 2. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Critical Modeling Pitfalls**:
  1. **Mandatory `TUEG` ↔ Downstream Test Patient De-Duplication**: Because `TUAB`, `TUEV`, and `TUSZ` were carved directly out of `TUEG`, you **must** exclude all downstream evaluation patient IDs from `TUEG` pretraining shards! Several early EEG pretraining papers accidentally leaked `TUAB`/`TUEV` eval patients during `TUEG` pretraining.
  2. **Standardize Montage (`AR` vs `LE`) & `60 Hz` Notch**: Clinical recordings span multiple decades of Nicolet/Natus hardware (`250–512 Hz`, `AR` vs `LE` reference); enforce uniform `0.5–75 Hz` bandpass + `60 Hz` notch + `200 Hz` resampling + `100 µV` clipping/normalization.

## 4. Programmatic Download & Quickstart
```bash
# Instant automated academic signup at NEDC -> fast rsync mirror access
open "https://isip.piconepress.com/projects/nedc/html/tuh_eeg/"
```

## 5. Verified Primary References
- **`obeid2016tueg`**: Obeid, I., & Picone, J. (2016). *The Temple University Hospital EEG Data Corpus*. Frontiers in Neuroscience (`10.3389/fnins.2016.00196`).
