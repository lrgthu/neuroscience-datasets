# PhysioNet 109-Subject EEG Motor Movement/Imagery (`EEGMMIDB`) & MOABB Suite (`PhysioNet:eegmmidb` / `10.13026/C28G6P`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Combines the widest-population open motor-imagery scalp EEG dataset (**`109` subjects**, `1,526` `EDF+` recordings collected with **`BCI2000`**, `Schalk et al., IEEE TBME, 2004`; hosted on `PhysioNet`, `Goldberger et al., Circulation, 2000`) with **`MOABB` (*Mother of All BCI Benchmarks*)** (`Jayaram & Barachant, J. Neural Eng., 2018`), which enforces reproducible preprocessing, statistical meta-analysis across `30+` BCI datasets, and zero-leakage cross-subject splits.
- **14-Run Experimental Design per Subject**:
  - **Runs `1` & `2` (`1 min` each)**: Baseline eyes-open (`R01`) and eyes-closed (`R02`).
  - **Runs `3, 7, 11` (Executed) & `4, 8, 12` (Imagined) (`2 min` each)**: `T1` = Left Fist vs. `T2` = Right Fist (`T0` = Rest).
  - **Runs `5, 9, 13` (Executed) & `6, 10, 14` (Imagined) (`2 min` each)**: `T1` = Both Fists vs. `T2` = Both Feet (`T0` = Rest).

## 2. Recording Specifications & Preprocessing
- **Montage & Sampling**: `64` scalp Ag/AgCl electrodes positioned per the international `10–10` system (referenced to mastoids/earlobes, sampled at `160 Hz` without hardware notch filtering), capturing contralateral `mu` (`8–13 Hz`) and `beta` (`13–30 Hz`) event-related desynchronization/synchronization (`ERD/ERS`) over `C3`, `Cz`, and `C4`.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Benchmark Baseline Hierarchy**: Always compare modern deep/foundation EEG architectures (`EEGNet`, `Conformer`, `LaBraM`, `CBraMod`) against strong **Riemannian geometry (`Tangent Space + Logistic Regression` / `Minimum Distance to Mean`)** and **Filter-Bank CSP** baselines via `moabb.evaluations.CrossSubjectEvaluation`.
- **Critical Modeling Pitfalls**:
  1. **`T1` / `T2` Trigger Remapping Across Run Numbers**: Raw `EDF+` annotations reuse strings `T1` and `T2` with **different class semantics** depending on the run ID (`left/right fist` in `R03/04/07/08/11/12` vs. `both fists/both feet` in `R05/06/09/10/13/14`). Never parse `T1/T2` without conditioning on the run index; use `moabb.datasets.PhysionetMI(imagined=True)` or `mne.datasets.eegbci`!
  2. **Drop the 4 Malformed Subjects (`S088`, `S089`, `S092`, `S100`)**: `S088`, `S092`, and `S100` were sampled at `128 Hz` instead of `160 Hz` with `~1 s` rather than `4 s` trial windows, and `S089` contains corrupted annotations—standard `105-subject` cross-subject benchmarks exclude these four IDs explicitly.
  3. **Low Per-Subject Trial Count (`~45` imagery trials/pair)**: `EEGMMIDB` excels at **cross-subject population generalization (`N = 105–109`)**, whereas multi-day longitudinal within-subject learning requires `Stieger2021` (`stieger_he_bci_eeg`).

## 4. Programmatic Download & Quickstart
```bash
# Direct PhysioNet mirror or automatic MNE/MOABB caching & evaluation
uv pip install moabb
python -c "from moabb.datasets import PhysionetMI; ds = PhysionetMI(imagined=True); ds.download()"
```

## 5. Verified Primary References
- **`jayaram2018moabb`**: Jayaram, V., & Barachant, A. (2018). *MOABB: trustworthy algorithm benchmarking for BCIs*. Journal of Neural Engineering (`10.1088/1741-2552/aadea0`).
- **`schalk2004bci2000`**: Schalk, G., McFarland, D. J., Hinterberger, T., Birbaumer, N., & Wolpaw, J. R. (2004). *BCI2000: A General-Purpose Brain-Computer Interface (BCI) System*. IEEE Transactions on Biomedical Engineering (`10.1109/tbme.2004.827072`).
- **`goldberger2000physionet`**: Goldberger, A. L., Amaral, L. A. N., Glass, L., Hausdorff, J. M., Ivanov, P. C., Mark, R. G., et al. (2000). *PhysioBank, PhysioToolkit, and PhysioNet: Components of a New Research Resource for Complex Physiologic Signals*. Circulation (`10.1161/01.cir.101.23.e215`).
