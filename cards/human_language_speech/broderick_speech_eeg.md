# Broderick Naturalistic Speech 128-Ch EEG (`Broderick-EEG` / `dryad.070jc`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: The classic lightweight, fast-running **1-hour crucial-experiment testbed** for continuous speech TRFs (`Broderick et al., Current Biology, 2018`). Packs **five complementary experiments** into one public CC0 archive:
  1. **Natural Audiobook (`N = 19`)**: `20` trials (`~3 min` each, `~60 min` total) of Hemingway's *The Old Man and the Sea*.
  2. **Cocktail-Party Dichotic Attention (`N = 33`)**: Attended vs. unattended competing audiobooks (*20,000 Leagues Under the Sea* vs. *Journey to the Center of the Earth*).
  3. **Speech-in-Noise**, **Time-Reversed Speech** (crucial negative control!), and **Comprehension-Matched Controls**.

## 2. Recording Specifications & Preprocessing
- **Acquisition**: `128`-channel BioSemi ActiveTwo scalp EEG (`512 Hz`, distributed at `128 Hz` in clean `.mat` arrays alongside aligned `128 Hz` speech envelopes, word onset/offset vectors, and content/function word annotations).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: `20`-fold leave-one-trial-out (`~3 min` per trial) nested ridge CV (`mTRFpy` / `eelbrain` / `himalaya`, lags `[-100, +700 ms]`).
- **Critical Modeling Pitfalls**:
  1. **Mandatory Word-Onset Impulse Regressor**: Assigning a `768-d` LLM vector to word onsets and zero elsewhere allows ridge regression to reconstruct a constant impulse via the mean vector norm; **always include an explicit `1-d` lexical/all-word onset impulse + acoustic envelope + half-wave rectified envelope derivative** as baseline features and test $\Delta r > 0$.
  2. **Built-In Falsification Control**: Validate any new linguistic/LLM metric on the **unattended cocktail-party stream** and **time-reversed speech** sub-datasets—if $\Delta r$ remains positive on reversed speech, your feature is leaking acoustic prosody!

## 4. Programmatic Download & Quickstart
```bash
# Public CC0 download from Dryad (lightweight ~2-3 GB MATLAB/HDF5 bundle; runs in minutes on laptop CPU/MPS!)
open "https://datadryad.org/dataset/doi:10.5061/dryad.070jc"
```

## 5. Verified Primary References
- **`broderick2018speech`**: Broderick, M. P., Anderson, A. J., Di Liberto, G. M., Crosse, M. J., & Lalor, E. C. (2018). *Electrophysiological correlates of semantic dissimilarity reflect the comprehension of natural, narrative speech*. Current Biology (`10.1016/j.cub.2018.01.080`).
