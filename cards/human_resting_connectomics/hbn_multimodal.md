# Child Mind Institute Healthy Brain Network (`HBN` · `3T Movie fMRI` + `128-Ch EEG`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: The largest **openly downloadable (`--no-sign-request` AWS S3)** multimodal human developmental brain dataset (`Alexander et al., Scientific Data, 2017`), spanning `>3,500–4,500` children and adolescents (`ages 5–21`). Uniquely pairs **high-density `128`-channel EEG + eye-tracking** across `6` passive/cognitive tasks with **`3T` naturalistic movie-watching fMRI** (*Despicable Me*, *The Present*), resting-state fMRI, diffusion MRI, and morphometry—powering both naturalistic movie developmental studies and the **NeurIPS 2025 EEG Foundation Challenge (`HBN-EEG` on NEMAR/OpenNeuro)**.

## 2. Recording Specifications & Preprocessing
- **EEG Battery (`500 Hz`, `128`-ch EGI HydroCel)**: Resting-state (eyes open/closed), `Surround Suppression`, `Movie Watching` (*Despicable Me*, *Diary of a Wimpy Kid*, *Funhouse*, *The Present*), `Contrast Change Detection` (`CCD`), `Sequence Learning`, and `Symbol Search` (`WISC-V`), standardized into `BIDS-EEG` (`s3://fcp-indi/data/Projects/HBN/BIDS_EEG/`).
- **MRI Battery (`TR = 0.80 s` at `3T` sites)**: Resting-state (`2 × 5 min`) + naturalistic movies (*Despicable Me* `10 min`, *The Present* `3.4 min`) + `T1w/T2w` + multi-shell `DKI`.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Critical Modeling Pitfalls**:
  1. **Check Field Strength (`Site-SI` is `1.5T`!)**: Early `Site-SI` (Staten Island) MRI scans were acquired on a `1.5T` Siemens Avanto (`TR = 1.45 s`), whereas `Site-RU`, `Site-CBIC`, and `Site-CUNY` use `3T` Siemens Prisma (`TR = 0.80 s`, `2.4 mm`)—filter or harmonize by `site` explicitly!
  2. **Pediatric Head Motion & Sponge Impedance**: Children aged `5–9` exhibit high framewise displacement in MRI and outer-ring sponge drying/bridging in `128-ch` EGI caps—use `BIDS_EEG` quality metrics and `FD < 0.2–0.3 mm` thresholds.

## 4. Programmatic Download & Quickstart
```bash
# Anonymous direct download from AWS Open Data (zero registration for imaging & BIDS-EEG!)
aws s3 ls --no-sign-request s3://fcp-indi/data/Projects/HBN/BIDS_EEG/
aws s3 ls --no-sign-request s3://fcp-indi/data/Projects/HBN/MRI/
```

## 5. Verified Primary References
- **`alexander2017hbn`**: Alexander, L. M., Escalera, J., Ai, L., et al. (2017). *An open resource for transdiagnostic research in pediatric mental health and learning disorders*. Scientific Data (`10.1038/sdata.2017.181`).
