# Amsterdam Open MRI Collection (`AOMIC` · `ID1000`, `PIOP1` & `PIOP2`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: One of the largest **100% public-domain (`CC0-1.0`), zero-DUA, preprocessed multimodal human `3T` MRI collections** for individual-difference neuroscience (`Snoek et al., Scientific Data, 2021`), totaling **`1,370` participants** across three complementary sub-datasets acquired at the University of Amsterdam:
  1. **`AOMIC-ID1000` (`OpenNeuro:ds003097`, `N = 928`, ages `19–26`, general-population educational stratification)**: `3 × T1w` structural scans, `3 × 32-direction DWI` scans, and an `~11 min` (`290` volumes, `TR = 2.20 s`) **naturalistic movie-watching fMRI** run, paired with Intelligence Structure Test (`IST` fluid, crystallized, memory IQ), `NEO-FFI` Big-Five personality, `BIS/BAS`, and socioeconomic phenotypes.
  2. **`AOMIC-PIOP1` (`OpenNeuro:ds002785`, `N = 216`, ages `18–26`)**: `T1w`, `DWI`, **`6 min` multiband resting-state fMRI (`TR = 0.75 s`, `480` volumes)**, plus **`5` task fMRI paradigms**: `faces` dynamic emotional expressions (`TR = 0.75 s`), `workingmemory`, `emotionmatching` (`Hariri`), `gstroop` (gender-Stroop conflict), and `anticipation` (emotional cue anticipation).
  3. **`AOMIC-PIOP2` (`OpenNeuro:ds002790`, `N = 226`, ages `18–26`, upgraded `Philips Achieva dStream`)**: `T1w`, `DWI`, **`8 min` resting-state fMRI (`TR = 2.0 s`, `240` volumes)**, plus **`3` replicated task fMRI paradigms** (`workingmemory`, `emotionmatching`, `gstroop`) and `stop-signal` (`stopsignal`).

## 2. Recording Specifications & Included BIDS Derivatives
- **Ready-to-Model Preprocessed Derivatives Shipped Directly in OpenNeuro**:
  - **`fMRIPrep`** (`MNI152NLin2009cAsym` volumetric + `fsaverage5` cortical surface spaces + full motion/CompCor confound TSVs).
  - **`FreeSurfer`** cortical thickness, surface area, and subcortical volume parcellations + **`MRIQC`** automated image quality metrics.
  - **`MRtrix3` / `FSL` DWI Derivatives** (`dwipreproc` eddy/topup corrected diffusion tensors, `FA`/`MD`, and spherical deconvolution) + **`PhysIO` RETROICOR** regressors computed from in-scanner `496 Hz` pulse-oximeter and respiratory belt traces!

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Protocols**:
  - **Individual-Difference Connectome KRR / GNN (`ID1000`, `N = 928`)**: `10`-fold cross-validation predicting `IST` general/fluid/crystallized intelligence and `NEO-FFI` openness/neuroticism from movie-evoked functional connectivity (which consistently outperforms pure rest for trait prediction!).
  - **Cross-Scanner Upgrade Transfer (`PIOP1 → PIOP2`)**: Train task decoding or trait models on `PIOP1` (`Philips Achieva`, `MB3` rest `TR = 0.75 s`) and evaluate zero-shot transfer on `PIOP2` (`Achieva dStream`, sequential `TR = 2.0 s`).
- **Critical Modeling Pitfalls**:
  1. **`ID1000` Is Movie-Watching (`TR = 2.2 s`), Not Eyes-Fixated Rest**: Do not mislabel `ID1000` `task-moviewatching` as resting-state when pooling cohorts; conversely, exploit its shared stimulus timeline across all `928` brains for inter-subject correlation (`ISC`) and shared response modeling (`SRM`)!
  2. **Mixed Multiband (`TR = 0.75 s`) vs. Sequential (`TR = 2.0 s`) Within `PIOP1`**: Within `PIOP1` itself, `restingstate` and `faces` use `3×` multiband (`TR = 0.75 s`), whereas `workingmemory`, `emotionmatching`, `gstroop`, and `anticipation` use sequential `TR = 2.0 s`—never concatenate `PIOP1` rest and task timeseries without temporal resampling and per-run z-scoring.
  3. **Audit OpenNeuro Foundation-Model Overlap**: Filter `ds003097`, `ds002785`, and `ds002790` out of OpenNeuro pretraining dumps (`Open-fMIND`) before reporting downstream AOMIC benchmarks.

## 4. Programmatic Download & Quickstart
```bash
# Direct anonymous AWS S3 download of fMRIPrep derivatives (zero account or DUA required!)
aws s3 ls --no-sign-request s3://openneuro.org/ds003097/derivatives/fmriprep/
aws s3 ls --no-sign-request s3://openneuro.org/ds002785/derivatives/fmriprep/
aws s3 ls --no-sign-request s3://openneuro.org/ds002790/derivatives/fmriprep/
```

## 5. Verified Primary References
- **`snoek2021aomic`**: Snoek, L., van der Miesen, M. M., Beemsterboer, T., van der Leij, A. R., Eigenhuis, A., & Scholte, H. S. (2021). *The Amsterdam Open MRI Collection, a set of multimodal MRI datasets for individual difference analyses*. Scientific Data (`10.1038/s41597-021-00870-6`).
