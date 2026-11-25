# Open MEG Archive (`OMEGA` · `Niso et al., 2016`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: The first dedicated, continuously expanding open-science archive for raw Magnetoencephalography (`MEG`) paired with individual `T1w` anatomical MRI (`Niso et al., NeuroImage, 2016`), spearheaded by Sylvain Baillet's group at the McConnell Brain Imaging Centre (`MNI`, McGill University) and Université de Montréal (`UdeM`).
- **Birthplace of `MEG-BIDS`**: OMEGA served as the primary reference implementation for the **MEG-BIDS** extension (`Niso et al., Scientific Data, 2018`), establishing standardized sidecar conventions for fiducials (`NAS`/`LPA`/`RPA`), Polhemus 3D scalp digitization (`*_headshape.pos`), continuous head-localization coils (`HLC`), and matched **`sub-emptyroom`** environmental noise recordings across **`>300` participants** (primarily neurotypical adults plus Parkinson's/pain/epilepsy sub-cohorts).

## 2. Recording Specifications & Multimodal Assets
- **Hardware & Acquisition (`CTF 275` Whole-Head MEG)**:
  - `275` axial first-order SQUID gradiometers (`5 cm` baseline) + `29` reference array sensors enabling real-time `3rd`-order synthetic gradient environmental noise cancellation.
  - Sampled at **`2,400 Hz`** (`600 Hz` anti-aliasing low-pass filter) in magnetically shielded rooms (`60 Hz` mains line frequency).
  - Core protocol: **`≥5 min` eyes-open resting-state** (fixating a central cross; subset also includes eyes-closed and auditory/motor tasks), simultaneous bipolar **`VEOG`**, **`HEOG`**, and **`ECG`** channels, continuous `3`-coil head-position tracking, `~2 min` same-day **`sub-emptyroom`** noise scan, and defaced `1 mm` `3T` `T1w` MRI (`FreeSurfer` cortical surfaces pre-computed for source imaging in `Brainstorm` and `MNE-Python`).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Modeling Use Cases**:
  1. **Source-Space Oscillatory & Envelope Connectomics**: Projecting sensor timeseries onto individual `FreeSurfer` cortical surfaces (`dSPM`, `sLORETA`, or `LCMV` beamformer whitened by same-day `sub-emptyroom` noise covariance) to benchmark spectral power, phase-locking, and orthogonalized amplitude-envelope connectivity (`Hipp et al.`) across `Glasser` or `Desikan-Killiany` parcels.
  2. **Multi-Scanner `MEG` Foundation Pretraining**: Combining `OMEGA` (`275-ch` CTF axial gradiometers), `MOUS` (`ds003029`, `275-ch` CTF), and `Cam-CAN` (`306-ch` Elekta planar gradiometers + magnetometers) to train geometry-aware sensor/source neural tokenizers.
- **Critical Modeling Pitfalls**:
  1. **Match CTF `3rd-Order` Gradient Compensation Across Signal, Noise & Forward Model**: A classic bug in `MNE-Python` / custom pipelines is computing noise covariance from an uncompensated (`grade 0`) `sub-emptyroom` file while applying it to `grade 3` compensated resting data—causing catastrophic beamformer/minimum-norm source localization errors! Always enforce matching `raw.compensation_grade == 3` across data, noise covariance, and `mne.make_forward_solution`.
  2. **Variable Active Channel Counts (`~268–275` Sensors)**: Individual recording dates drop dead/jumping SQUIDs; never hard-code a fixed `275 × T` matrix index without reading `*_channels.tsv` (`status == bad`) and either interpolating to a canonical CTF helmet or mapping to cortical source parcels.
  3. **Account for Dual CTF Sites (`MNI` vs. `UdeM`) & `60 Hz` Harmonics**: Apply notch/zapline filtering at `60, 120, 180, 240 Hz`, regress cardiac/ocular `SSP` or `ICA` components locked to the simultaneous `ECG`/`EOG` leads, and stratify CV folds by recording site.

## 4. Programmatic Download & Quickstart
```bash
# 1. Zero-auth OpenNeuro download of the 5-subject MEG-BIDS OMEGA reference sample (with FreeSurfer anatomy)
aws s3 sync --no-sign-request s3://openneuro.org/ds000247 ./omega_bids_sample

# 2. Full >300-subject archive: register free account at https://www.mcgill.ca/bic/resources/omega (or via CONP DataLad)
```

## 5. Verified Primary References
- **`niso2016omega`**: Niso, G., Rogers, C., Moreau, J. T., et al. (2016). *OMEGA: The Open MEG Archive*. NeuroImage (`10.1016/j.neuroimage.2015.04.028`).
