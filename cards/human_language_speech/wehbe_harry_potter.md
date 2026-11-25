# CMU *Harry Potter* Word-by-Word Reading fMRI & MEG (`Wehbe et al. 2014`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Established simultaneous multi-tier decomposition of visual, orthographic, syntactic, semantic, and narrative character/motion subprocesses during continuous story reading (`Wehbe et al., PLoS ONE, 2014`), paired with companion `306`-channel MEG recordings of the exact same chapter (`Wehbe et al., EMNLP, 2014`) that pioneered aligning recurrent neural language model hidden states with millisecond brain dynamics (`Toneva & Wehbe, NeurIPS, 2019`).
- **Stimulus & Exact RSVP Timing**: Participants read **Chapter 9 of *Harry Potter and the Sorcerer's Stone*** (*The Midnight Duel*, `5,176` words total) presented one word at a time at screen center via Rapid Serial Visual Presentation (`RSVP`) for **exactly `0.5 s` per word** (`45 minutes` across `4` contiguous runs). Fixing fixation and word duration eliminates saccadic eye-movement artifacts while locking exactly `4` words to every `2.0 s` fMRI `TR`.

## 2. Recording Specifications & Preprocessing
- **3T fMRI Cohort (`N = 8`)**: Siemens Verio `3T` whole-brain EPI (`TR = 2.0 s`, `3 × 3 × 3 mm` isotropic voxels, `~25,000–30,000` cortical voxels per subject across `1,351` total TRs), distributed as ready-to-use MATLAB `.mat` matrices (`subject_1.mat`..`subject_8.mat`) with `AAL` ROI labels and rich multi-tier linguistic annotations (`195` interpretable visual, POS, dependency, and discourse features).
- **306-Channel MEG Cohort (`N = 9`)**: Elekta Neuromag `306`-sensor whole-head MEG (`102` magnetometers + `204` planar gradiometers, `1,000 Hz`, hosted via CMU Figshare `20658428`), resolving `50–600 ms` orthographic-to-semantic cascades word by word.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: `4-fold` leave-one-run-out cross-validation across the `4` narrative runs (`Toneva & Wehbe, 2019`), discarding `10–20` boundary TRs per run to prevent hemodynamic bleed and run-onset transients.
- **Critical Modeling Pitfalls**:
  1. **Stack 4-TR Hemodynamic FIR Lags (`2–8 s`)**: Because `TR = 2.0 s` spans `4` words while BOLD peaks `4–8 s` post-stimulus, construct TR-level regressors by averaging/summing the `4` word embeddings inside each `2 s` window and concatenating lags `[t-1, t-2, t-3, t-4]`.
  2. **Regress Out Visual Word Length & Formatting**: Under central RSVP, long words subtend wider retinal eccentricity and strongly drive early visual cortex; always partial out character length and punctuation before attributing early visual alignment to deep LLM layers.
  3. **Correction Notice (`10.1371/journal.pone.0123148`)**: Note minor figure/formatting errata documented by the authors; the underlying CMU `.mat` data matrices and stimulus alignments are unaffected.

## 4. Programmatic Download & Quickstart
```bash
# Download preprocessed 3T fMRI MATLAB files (subjects 1..8) from CMU
for s in $(seq 1 8); do
  curl -LO "http://www.cs.cmu.edu/~fmri/plosone/files/subject_${s}.mat"
done
```

## 5. Verified Primary References
- **`wehbe2014simultaneously`**: Wehbe, L., Murphy, B., Talukdar, P. P., Fyshe, A., Ramdas, A., & Mitchell, T. M. (2014). *Simultaneously uncovering the patterns of brain regions involved in different story reading subprocesses*. PLoS ONE, 9(11), e112575 (`10.1371/journal.pone.0112575`).
- **`wehbe2014aligning`**: Wehbe, L., Vaswani, A., Knight, K. K., & Mitchell, T. M. (2014). *Aligning context-based statistical models of language with brain activity during reading*. Proceedings of EMNLP 2014, 233–243 (`10.3115/v1/d14-1030`).
