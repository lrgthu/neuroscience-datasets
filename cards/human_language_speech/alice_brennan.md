# *Alice in Wonderland* Naturalistic fMRI & EEG Corpus (`ds002322` & Deep Blue / Brennan & Hale)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Unites **spatial localization (`3T fMRI`)** and **millisecond temporal prediction (`61-ch EEG`)** on the exact same naturalistic narrative stimulus—Chapter 1 of Lewis Carroll's *Alice's Adventures in Wonderland*—coupled with formal syntactic complexity metrics from Context-Free Grammars (`CFG`), Minimalist Grammars (`MG`), and recurrent/n-gram language models (`Brennan et al., Brain and Language, 2016`; `Brennan & Hale, PLoS ONE, 2019`; `Bhattasali et al., LREC, 2020`, `https://aclanthology.org/2020.lrec-1.15/`).
- **Stimulus & Linguistic Annotations**: `12.4 minutes` (`2,129` word tokens, `84` sentences) narrated by Kristen McQuillan (LibriVox) and time-stretched by `20%` via pitch-synchronous overlap-add (`PSOLA`) to preserve intelligibility inside scanner acoustic noise. Shipped with word-by-word forced alignments, `F0`/RMS prosody, subtitle log-frequency, bigram/trigram/RNN surprisal, and bottom-up/left-corner syntactic parse step counts.

## 2. Recording Specifications & Preprocessing
- **3T fMRI (`OpenNeuro:ds002322`, `N = 26` retained of `29`)**: Acquired on a `3T` GE Discovery MR750 (`TR = 2.0 s`, `372` volumes). Split across two hardware sequence phases: a single-echo EPI subgroup (`3 × 3 × 3 mm`, `TE = 27 ms`) and a `3`-echo EPI subgroup (`3.75 × 3.75 × 3.8 mm`, `TE2 = 27.5 ms`).
- **61-Channel Scalp EEG (`UMich Deep Blue:10.7302/746w-g237` & `10.7302/Z29C6VNH`, `N = 49` raw / `N = 33` QC-clean)**: Brain Products `actiCHamp` active electrodes (`500 Hz`, `0.1–200 Hz` hardware passband, ICA ocular artifact cleaned in FieldTrip `.mat` format).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Contiguous temporal block cross-validation (`k`-fold over non-overlapping story segments with `>=20 s` fMRI boundary trims) or mixed-effects / ridge nested model comparison (`Brennan & Hale, 2019`).
- **Critical Modeling Pitfalls**:
  1. **Harmonize `ds002322` Single-Echo and Multi-Echo Subgroups**: Do not naively mix multi-echo `echo-1`/`echo-3` or raw native-voxel grids with the single-echo subjects! Extract `echo-2` (`TE = 27.5 ms`, matching `TE = 27 ms`), warp to common MNI space, z-score per run/subject, and include a sequence-subgroup nuisance indicator.
  2. **Isolate Hierarchical Syntax via Nested Baseline Subtraction**: Because syntactic node counts covary with word onset rate, acoustic energy, and surface n-gram surprisal, evaluate unique variance (`ΔR²` / `ΔAIC`) strictly *over and above* acoustic + lexical + sequential n-gram baselines.
  3. **Account for 20% PSOLA Time-Stretching in Audio Foundation Models**: Speech SSL encoders (`Wav2Vec2`, `HuBERT`, `Whisper`) see slower-than-typical syllable rates (`~2.8–3.2 Hz`); extract features directly from the distributed experimental `.wav` file rather than raw LibriVox audio.

## 4. Programmatic Download & Quickstart
```bash
# 1. Install BIDS 3T fMRI cohort from OpenNeuro
datalad install https://github.com/OpenNeuroDatasets/ds002322.git
# 2. Download 61-ch EEG FieldTrip MAT files & word predictors from UMich Deep Blue
#    https://doi.org/10.7302/746w-g237  and  https://doi.org/10.7302/Z29C6VNH
```

## 5. Verified Primary References
- **`brennan2019hierarchical`**: Brennan, J., & Hale, J. (2019). *Hierarchical structure guides rapid linguistic predictions during naturalistic listening*. PLoS ONE, 14(1), e0207741 (`10.1371/journal.pone.0207741`).
- **`brennan2016abstract`**: Brennan, J., Stabler, E. P., Van Wagenen, S. E., Luh, W.-M., & Hale, J. (2016). *Abstract linguistic structure correlates with temporal activity during naturalistic comprehension*. Brain and Language, 157–158, 81–94 (`10.1016/j.bandl.2016.04.008`).
