# Adolescent Brain Cognitive Development Study (`ABCD` · `N = 11,878`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Tracks adolescent brain development over a decade (`ages 9–10` through `19–20`, `Casey et al., Dev. Cogn. Neurosci., 2018`) across `21` US research sites (`Siemens`, `GE`, `Philips` `3T`). Alongside `UK Biobank` (older adults) and `HCP-YA` (young adults), `ABCD` anchors the developmental pole of human brain foundation modeling and inspired landmark methodological reforms on **Brain-Wide Association Studies (`BWAS`, `Marek et al., Nature, 2022`)**.
- **Functional Protocol**: `4 × 5 min` (`20 min`) resting-state fMRI (`TR = 0.80 s`, `2.4 mm` isotropic) plus `3` cognitive/affective fMRI tasks: **Monetary Incentive Delay (`MID`)**, **Stop-Signal Task (`SST`)**, and **Emotional N-Back (`EN-Back` faces/places)**.

## 2. Recording Specifications & Preprocessing
- **ABCD-BIDS Community Collection (`ABCC`, NDA Collection `3165`)**: Provides HCP-style `CIFTI 91k` cortical surface + subcortical derivatives, respiratory-notch-filtered `FD` motion traces, and matched discovery/replication split assignments (`ARMS-1` / `ARMS-2`).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Critical Modeling Pitfalls**:
  1. **Multiband Respiratory Pseudomotion**: At `TR = 0.80 s`, pediatric breathing (`~18–25 breaths/min = 0.3–0.4 Hz`) contaminates raw `6-DOF` head-motion parameters—always apply `0.31–0.43 Hz` notch filtering to motion traces (`Fair et al. 2020`) before `FD < 0.2 mm` frame censoring!
  2. **Vendor (`GE / Philips / Siemens`) & Family Stratification**: Scanner vendor differences strongly separate raw timeseries and FC matrices; test generalization via **leave-site-out CV** and keep `rel_family_id` intact.

## 4. Programmatic Download & Quickstart
```bash
# Requires institutional NIH NDA Data Use Certification (https://nda.nih.gov/abcd)
# For an immediate open-access developmental cohort with EEG + fMRI, see `hbn_multimodal`!
```

## 5. Verified Primary References
- **`casey2018abcd`**: Casey, B. J., Cannonier, T., Conley, M. I., et al. (2018). *The Adolescent Brain Cognitive Development (ABCD) study: Imaging acquisition across 21 sites*. Developmental Cognitive Neuroscience (`10.1016/j.dcn.2018.03.001`).
