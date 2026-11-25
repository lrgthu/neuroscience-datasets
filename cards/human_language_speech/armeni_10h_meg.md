# Armeni `10`-Hour Head-Cast *Sherlock Holmes* MEG (`10.34973/5rpw-rn92` / Armeni et al. 2022)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Pioneered the **deep within-participant precision-MEG paradigm** for naturalistic language modeling (`Armeni, Güçlü, van Gerven, & Schoffelen, Scientific Data, 2022`), inspiring subsequent ultra-deep benchmarks such as `LibriBrain`. Instead of scanning dozens of subjects for `30–60 minutes` with large helmet-repositioning variance, `3` participants each completed **`10` separate `~1-hour` sessions (`10 hours` / `~85,000+` word tokens per subject)** while wearing **custom 3D-printed MRI-molded foam head casts**.
- **Stimulus & Behavioral Tracking**: All `10` stories from Arthur Conan Doyle's *The Adventures of Sherlock Holmes* (`ses-001` *A Scandal in Bohemia* through `ses-010` *The Adventure of the Noble Bachelor*), accompanied by word- and phoneme-level forced alignments (`FAVE` / Penn Phonetics Lab), lexical frequency/surprisal tables, simultaneous `EyeLink 1000` pupil/gaze tracking, and post-story comprehension + literary appreciation ratings.

## 2. Recording Specifications & Preprocessing
- **Hardware & Head-Cast Precision**: `275`-channel CTF axial gradiometer MEG (`1,200 Hz`, Donders Centre for Cognitive Neuroimaging) with continuous `HPI` head-coil localization (`3` coils embedded directly into custom nylon/polyurethane foam head casts), achieving **`<0.5 mm` within-session motion and `<1.5 mm` cross-day repositioning accuracy** across all `10` sessions—allowing sensor-level weights or single beamformer/minimum-norm inverse operators (`T1w` anatomical MRI included) to pool cleanly across `10` hours.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: `10-fold` leave-one-session/story-out (`ses-001`..`ses-010`) evaluated separately inside `sub-001`, `sub-002`, and `sub-003`.
- **Critical Modeling Pitfalls**:
  1. **Individual-Participant Statistical Replication (`N = 3`)**: Follow the psychophysics / precision-fMRI standard (`Naselaris / Kay / Gallant` paradigm): test encoding/decoding hypotheses via non-parametric story-block permutation within each subject (`α = 0.05` FDR-corrected across sensors/parcels) and report consistency across all `3/3` brains rather than `df = 2` group-mean tests.
  2. **CTF Reference Compensation & `50 Hz` Mains**: Apply standard CTF `3rd-order` reference-sensor synthetic gradiometer denoising (`mne.io.read_raw_ctf(..., clean_names=True)`), inspect session-specific bad-channel annotations, and z-score each continuous run before concatenating sessions.
  3. **Second-Language (`L2`) Proficiency Context**: Participants are highly proficient non-native (Dutch `L1`, C1/C2 English) academic listeners; keep `L2` English comprehension context in mind when comparing phonetic/lexical dynamics against `L1` cohorts (`MEG-MASC`, `LibriBrain`).

## 4. Programmatic Download & Quickstart
```bash
# Dataset is archived in MEG-BIDS format on the Donders Data Repository:
# https://doi.org/10.34973/5rpw-rn92 (supports WebDAV / rclone download after free registration)
```

## 5. Verified Primary References
- **`armeni2022tenhour`**: Armeni, K., Güçlü, U., van Gerven, M. A. J., & Schoffelen, J.-M. (2022). *A 10-hour within-participant magnetoencephalography narrative dataset to test models of language comprehension*. Scientific Data, 9, 278 (`10.1038/s41597-022-01382-7`).
