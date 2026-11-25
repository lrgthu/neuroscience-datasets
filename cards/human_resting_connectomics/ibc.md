# Individual Brain Charting (`IBC` · `ds002685` · `67` Tasks)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: While `NSD` maximizes *visual scene count* and `CNeuroMod` maximizes *movie hours*, Inria/NeuroSpin's **Individual Brain Charting (`IBC`)** (`Pinho et al., Scientific Data, 2018` + Releases 2–5) maximizes **within-subject cognitive task diversity** (`67` distinct tasks, `>400` GLM functional contrasts, `~50+ hours` of `1.5 mm` `3T` fMRI per individual across `N = 13` subjects).
- **Batteries Included**: Full `HCP` task suite, `ARCHI` localizers, retinotopy, tonotopy, reading/speech comprehension, mental arithmetic, theory-of-mind, reward/gambling, motor somatotopy, visual search, and full-length audio/audiovisual movies (*Raiders of the Lost Ark*, *The Good, the Bad and the Ugly*).

## 2. Recording Specifications & Preprocessing
- **High-Spatial `3T` Acquisition**: `1.5 mm` isotropic (`TR = 2.0 s`, multiband `3`) with `Topup` `AP/PA` susceptibility distortion correction; precomputed GLM `z`-maps are browsable & downloadable immediately via NeuroVault alongside raw BIDS on OpenNeuro (`ds002685`) and EBRAINS.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Critical Modeling Pitfalls**:
  1. **Check Subject Availability Across Releases**: Early releases (`R1`) cover `ARCHI + HCP`, while later releases add specialized vision, sound, math, and movie batteries; check `participants.tsv` / task tables per release.
  2. **Exploit `IBC` to Validate Functional Selectivity Claims**: Before claiming a cortical region is "domain-specific", test your encoding/cognitive model across `IBC`'s `67` tasks in the exact same cortical surface vertices.

## 4. Programmatic Download & Quickstart
```bash
datalad install https://github.com/OpenNeuroDatasets/ds002685.git
```

## 5. Verified Primary References
- **`pinho2018ibc`**: Pinho, A. L., Amadon, A., Ruest, T., et al. (2018). *Individual Brain Charting, a high-resolution fMRI dataset for cognitive mapping*. Scientific Data (`10.1038/sdata.2018.105`).
