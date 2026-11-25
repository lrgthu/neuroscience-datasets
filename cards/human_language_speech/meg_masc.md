# MEG-MASC (`ds004078` / Gwilliams et al. 2023)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Standardizes **millisecond-resolved naturalistic speech MEG** (`Gwilliams et al., Scientific Data, 2023`), widely adopted for temporal response functions (`TRF`), phonetic feature tracking (`Gwilliams et al., Nature Communications, 2022`), contrastive speech-brain retrieval (`Défossez et al., Nature Machine Intelligence, 2023`), and hierarchical predictive coding.
- **Stimulus Design & Timing**: Four naturalistic stories from the Manually Annotated Sub-Corpus (`MASC`: *Cable Spool Boy*, *LW1*, *Black Willow*, *Easy Money*, totaling `~56 minutes` unique audio; `7,745` word tokens and `~29,000` phonemes per session) voiced by distinct speakers. Crucially, `22 / 27` participants returned for a **second identical session (`ses-1`)**, doubling per-subject data (`~2 hours`) and enabling direct `ses-0 ↔ ses-1` noise-ceiling estimation.

## 2. Recording Specifications & Preprocessing
- **Acquisition**: `208`-channel KIT axial gradiometer MEG (`1,000 Hz`, NYU Abu Dhabi) in `mne-bids` format, complete with digitized headshape points (`Polhemus`) and individual `T1w` structural MRIs for cortical source reconstruction.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Leave-one-story-out (`4` stories) or contiguous `10%` temporal block splits (`Défossez et al. 2023` protocol) with boundary buffer exclusions.
- **Critical Modeling Pitfalls**:
  1. **Never Split Overlapping Epochs Randomly**: Because consecutive phonemes/words are separated by `80–250 ms` while `1.0 s` windows overlap by `75–92%`, random `train_test_split` on epochs memorizes raw time-series overlap rather than generalizing to unseen speech!
  2. **Avoid Pre-Onset Baseline Subtraction in Rapid Speech**: Subtracting `[-200, 0 ms]` per phoneme injects the neural response to phoneme $t-1$ (and phoneme transition bigram statistics) directly into every post-onset sample. Filter continuous data (`0.5–40 Hz`) and apply robust scaling (`RobustScaler` clipped at `±20 SD`) on continuous runs first.
  3. **Inter-Session Helmet Shift**: Sensor indices are head-movement sensitive across `ses-0` and `ses-1`; fit session-specific spatial layers or project to cortical source space.

## 4. Programmatic Download & Quickstart
```bash
# Install BIDS MEG-MASC dataset via OpenNeuro DataLad (or load directly with mne-bids)
datalad install https://github.com/OpenNeuroDatasets/ds004078.git
```

## 5. Verified Primary References
- **`gwilliams2023megmasc`**: Gwilliams, L., Flick, G., Marantz, A., Pylkkänen, L., Poeppel, D., & King, J.-R. (2023). *Introducing MEG-MASC a high-quality magneto-encephalography dataset for evaluating natural speech processing*. Scientific Data (`10.1038/s41597-023-02752-5`).
