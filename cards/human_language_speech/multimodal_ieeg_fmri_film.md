# Utrecht Open Multimodal iEEG & fMRI Audiovisual Film Dataset (`ds003688` / Berezutskaya et al. 2022)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Bridges the fundamental gap between **human intracranial electrophysiology (`ECoG`/`sEEG` high-gamma)** and **non-invasive whole-brain `3T/7T fMRI`** under identical naturalistic audiovisual stimulation (`Berezutskaya et al., Scientific Data, 2022`). Crucially, **`18` participants completed BOTH presurgical fMRI and subsequent invasive iEEG** on the exact same short film (`N = 63` unique individuals across `51` iEEG + `30` fMRI sessions), providing a rare ground-truth testbed for neurovascular coupling and cross-modal representation alignment.
- **Stimulus Structure & Rich Annotations**: A `6.5-minute` (`390 s`) edited clip from the Dutch live-action film *Pippi Longstocking* (*Pippi Langkous*), structured into `13` interleaved `30 s` blocks: `6` visual+music blocks (`0` speech) alternating with `7` visual+naturalistic Dutch dialogue blocks, bundled in BIDS `stimuli/` with millisecond phoneme/word TextGrids, pitch/intensity envelopes, and frame-by-frame visual object/face/scene annotations.

## 2. Recording Specifications & Preprocessing
- **Intracranial Cohort (`N = 51`, ages `5–55`)**: Subdural `ECoG` grids/strips (`1 cm` pitch) and penetrating `sEEG` depth shafts (`512–2,048 Hz`, Micromed amplifiers at UMC Utrecht) projected onto individual `T1w` cortical surfaces (`FreeSurfer` `pial` coordinates in `iEEG-BIDS`), with clinically annotated bad/epileptogenic channels flagged in `*_channels.tsv`.
- **fMRI Cohort (`N = 30`, ages `7–47`)**: High-temporal-resolution `3T` `3D-PRESTO` whole-brain scans (`TR_vol ≈ 0.608 s`, `4 mm` isotropic) plus `7T` high-spatial-resolution EPI subsets, enabling sub-second BOLD deconvolution alongside `ECoG` high-frequency broadband (`HFB`, `60–140 Hz`).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Leave-one-speech-block-out (`7` speech blocks of `30 s` each) for linguistic encoding, or `13-block` stratified CV with hemodynamic boundary padding for audiovisual models; use `N = 18` paired brains for direct `HFB ↔ BOLD` translation benchmarks.
- **Critical Modeling Pitfalls**:
  1. **Control for the `30 s` Speech-Block Boxcar**: Because speech occurs strictly inside `7` discrete `30 s` windows (`53.8%` of total duration), even random vectors multiplied by word onsets achieve high raw correlations (`r > 0.4` in `STG`) purely by tracking block-level auditory presence! Always include a binary speech-block indicator, acoustic spectrogram/envelope, and word-onset impulse baseline, or compute correlations strictly within concatenated speech blocks.
  2. **Per-Subject JSON Timing & Sampling Verification**: Read exact `RepetitionTime` / `SamplingFrequency` from each participant's BIDS JSON sidecar rather than hardcoding a single global sampling rate.
  3. **Exclude Pathological Contacts & Model Age Covariates**: Filter `status == "good"` channels in `*_channels.tsv` and include participant age (`5–55 yr`) when comparing cross-subject latency or spectral tilt.

## 4. Programmatic Download & Quickstart
```bash
# Install OpenNeuro BIDS repository (iEEG + 3T/7T fMRI + audiovisual annotations)
datalad install https://github.com/OpenNeuroDatasets/ds003688.git
git clone https://github.com/UMCU-RIBS/Open-multimodal-iEEG-fMRI-dataset.git
```

## 5. Verified Primary References
- **`berezutskaya2022multimodal`**: Berezutskaya, J., Vansteensel, M. J., Aarnoutse, E. J., Freudenburg, Z. V., Piantoni, G., Branco, M. P., & Ramsey, N. F. (2022). *Open multimodal iEEG-fMRI dataset from naturalistic stimulation with a short audiovisual film*. Scientific Data, 9, 91 (`10.1038/s41597-022-01173-0`).
