# Di Liberto Categorical Phonemic Feature Natural Speech EEG (`ds004408` & Dryad / Di Liberto et al. 2015)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Established the canonical **Multivariate Temporal Response Function (`mTRF`) hierarchical speech-tracking paradigm** (`Di Liberto, O'Sullivan, & Lalor, Current Biology, 2015`), demonstrating that non-invasive `1–8 Hz` scalp EEG tracks categorical **ARPAbet phonemes (`39` classes)** and **articulatory phonetic features (`19` manner/place/voicing dimensions)** beyond auditory cochlear spectrograms (`FS > S`), and that this phonemic enhancement selectively disappears during time-reversed speech. Forms the foundational acoustic-phonetic layer paired with `Broderick et al. (2018)` semantic N400 modeling and the `mTRF-Toolbox`.
- **Stimulus & Alignments**: `20` consecutive `~180 s` narrative segments (`~60 minutes` total) from a professional single-speaker audiobook reading of Ernest Hemingway's *The Old Man and the Sea*, forced-aligned via the Prosodylab-Aligner into exact millisecond word and `39`-phoneme intervals mapped onto `19` binary articulatory features (voiced, bilabial, labiodental, dental, alveolar, palatal, velar, glottal, plosive, fricative, nasal, liquid, glide, front/back/high/mid/low/diphthong vowels).

## 2. Recording Specifications & Preprocessing
- **128-Channel BioSemi ActiveTwo (`OpenNeuro:ds004408` & `Dryad:10.5061/dryad.070jc`)**: `N = 19` healthy normal-hearing native English speakers (`10` in the original 2015 natural + time-reversed cohort, standardized to the `19`-subject audiobook release in `ds004408` / `dryad.070jc`) recorded at `512 Hz` with `2` mastoid references in an electrically shielded soundbooth, typically bandpassed to `1–8 Hz` (or `0.5–15 Hz`), mastoid re-referenced, and downsampled to `128 Hz` for `mTRF` encoding (`[0, 300 ms]` lags).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: `20-fold` leave-one-trial-out cross-validation across the `20` contiguous `3-minute` story trials within each participant (`r_FS` vs. `r_S` paired Wilcoxon / $t$-test across `N = 19` subjects).
- **Critical Modeling Pitfalls**:
  1. **Control for Onset-Envelope Acoustics (`Daube et al., 2019` Critique)**: Phoneme boundaries coincide with sharp spectral flux / half-wave-rectified envelope derivatives (`env'`). Always include multi-band cochlear spectrograms **plus** acoustic onset derivatives (`S + S_onset`) in the baseline model before attributing `Δr` to abstract phonetic categories!
  2. **Use Banded Ridge Regression (`λ_F ≠ λ_S`)**: Fitting `S` (`16` continuous bands) and `FS` (`16` continuous + `19` binary features) with a single shared ridge penalty `λ` penalizes `S` suboptimally and creates illusory `FS > S` gains; tune separate ridge penalties via nested cross-validation (`himalaya.ridge.BandedRidgeCV`).
  3. **Avoid Epoch-Shuffled Splits**: Fit continuous convolution kernels (`mTRF` / `FIR`) on intact `180 s` runs rather than randomly shuffled `300 ms` phoneme epochs.

## 4. Programmatic Download & Quickstart
```bash
# Install BIDS 128-ch EEG + phoneme/word alignment archive from OpenNeuro
datalad install https://github.com/OpenNeuroDatasets/ds004408.git
```

## 5. Verified Primary References
- **`diliberto2015phoneme`**: Di Liberto, G. M., O'Sullivan, J. A., & Lalor, E. C. (2015). *Low-frequency cortical entrainment to speech reflects phoneme-level processing*. Current Biology, 25(19), 2457–2465 (`10.1016/j.cub.2015.08.030`).
- **`broderick2018speech`**: Broderick, M. P., Anderson, A. J., Di Liberto, G. M., Crosse, M. J., & Lalor, E. C. (2018). *Electrophysiological correlates of semantic dissimilarity reflect the comprehension of natural, narrative speech*. Current Biology, 28(5), 803–809.e3 (`10.1016/j.cub.2018.01.080`).
