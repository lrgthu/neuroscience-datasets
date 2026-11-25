# Allen Brain Observatory: Visual Coding (`Neuropixels` & `Two-Photon`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Pairs **sub-millisecond multi-area spiking hierarchy** (`Siegle et al., Nature, 2021` — up to `6` simultaneous Neuropixels probes across `VISp`, `VISl`, `VISrl`, `VISal`, `VISpm`, `VISam`, thalamic `LGd/LP`, and hippocampal `CA1/CA3/DG`) with **genetically defined Cre-line cell-type calcium imaging** (`de Vries et al., Nature Neuroscience, 2019/2020`) under an **identical standardized visual stimulus battery** (`Brain Observatory 1.1` & `Functional Connectivity` sets: drifting/static gratings, `118` natural scenes × `50` repeats, *Touch of Evil* natural movies, Gabor RF mapping, and flashes).

## 2. Recording Specifications & Preprocessing
- **Format & CCF Registration**: Every unit and ROI is registered to **Allen Mouse Common Coordinate Framework (`CCFv3`)** 3D coordinates, accompanied by `30 Hz` rotary-encoder running velocity and `EyeLink`/infrared pupil size & gaze tracking in standardized **NWB 2.0** files.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: `118` natural scenes (`80/20` image split or `10`-fold CV over the `118` scenes, `50` repeats/scene) and contiguous temporal chunks of `Natural Movie One` (`30 s` × `20` repeats) / `Natural Movie Three` (`120 s` × `10` repeats).
- **Critical Modeling Pitfalls**:
  1. **Apply Unit Quality Thresholds (`AllenSDK` Defaults)**: Unfiltered Kilosort units contain refractory-period violations and probe drift; enforce `isi_violations < 0.5`, `amplitude_cutoff < 0.1`, and `presence_ratio > 0.9` (checking `presence_ratio` specifically within the stimulus block of interest!).
  2. **Spontaneous Behavioral State (`Running` + `Pupil`)**: In awake head-fixed mice, spontaneous locomotion and arousal explain large shared rank-1/low-rank population fluctuations across all visual areas—model sensory + behavioral state jointly!

## 4. Programmatic Download & Quickstart
```bash
# Download Visual Coding Neuropixels NWB Dandiset 000021 (or query selectively via AllenSDK / AWS S3)
uvx dandi download DANDI:000021
aws s3 ls --no-sign-request s3://allen-brain-observatory/visual-coding-neuropixels/ecephys-cache/
```

## 5. Verified Primary References
- **`siegle2021neuropixels`**: Siegle, J. H., Jia, X., Durand, S., et al. (2021). *Survey of spiking in the mouse visual system reveals functional hierarchy*. Nature (`10.1038/s41586-020-03171-x`).
- **`devries2019twophoton`**: de Vries, S. E. J., Lecoq, J. A., Buice, M. A., et al. (2019/2020). *A large-scale standardized physiological survey reveals functional organization of the mouse visual cortex*. Nature Neuroscience (`10.1038/s41593-019-0550-9`).
