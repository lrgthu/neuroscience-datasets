# SparrKULee (`85`-Subject Natural Speech `64`-Ch EEG Repository · KU Leuven)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Overcomes the `N = 15–25` sample-size bottleneck of traditional speech-tracking scalp EEG datasets by releasing **`168 hours` of `64`-channel natural speech EEG across `85` normal-hearing young adults** (`Accou et al., Data, 2024`). Serves as the official backbone of the **ICASSP Signal Processing Grand Challenges on Auditory EEG Decoding** (`2023` & `2024`), catalyzing deep nonlinear architectures (`VLAAI`, dilated CNN/Conformers, contrastive `CLIP`-style speech-brain match-mismatch models) beyond classical ridge `mTRF`s.
- **Stimulus Design**: Each participant listened binaurally via ER-3A insert earphones (`60–62 dBA`) to `90–150 minutes` (`6–10` trials of `~15 min` each) of continuous natural Flemish/Dutch audiobooks and podcasts without background noise, interspersed with short comprehension questions to maintain alertness.

## 2. Recording Specifications & Preprocessing
- **Hardware & BIDS Structure**: Recorded in a soundproof, electromagnetically shielded booth at KU Leuven (`ExpORL`) using a `64`-channel BioSemi ActiveTwo system at `8,192 Hz` hardware sampling rate, decimated to `1,024 Hz` in `EEG-BIDS` format alongside `48 kHz` stimulus waveforms, trigger synchronization channels, and pre-extracted `64 Hz` speech envelopes, voice fundamental frequency (`F0`), and `28`-band mel spectrograms.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Follow the official ICASSP Challenge two-axis generalization benchmark:
  - **Test Set 1 (Seen Subjects, Unseen Speech)**: Held-out stories from training participants (`sub-001`..`sub-071`), measuring within-distribution temporal generalization.
  - **Test Set 2 (Unseen Subjects, Unseen Speech)**: Completely held-out participants (`sub-072`..`sub-085`), measuring zero-shot population transfer.
- **Critical Modeling Pitfalls**:
  1. **Mandatory Re-Referencing of BioSemi ActiveTwo Signals**: Raw BioSemi recordings retain common-mode `CMS/DRL` drift (`>10 mV` DC offsets) and `50 Hz` European mains interference; always high-pass (`0.5 Hz`), notch/low-pass (`<32–40 Hz`), and apply common-average or mastoid re-referencing on continuous trials prior to windowing.
  2. **Hard-Negative Construction in Match-Mismatch Tasks**: Sample negative imposter audio clips strictly from the *same* speaker/story trial outside the `±1 s` autocorrelation radius; cross-story negatives allow trivial acoustic distribution shortcuts.
  3. **Credentialed Non-Commercial Access (`CC-BY-NC-4.0`)**: Hosted on KU Leuven RDR (`10.48804/K3VSND`) under free academic registration (`sparrkulee@kuleuven.be`).

## 4. Programmatic Download & Quickstart
```bash
# Clone official preprocessing, envelope extraction & baseline code from KU Leuven ExpORL
git clone https://github.com/exporl/auditory-eeg-challenge-2024-code.git
# Request free academic access token at: https://doi.org/10.48804/K3VSND
```

## 5. Verified Primary References
- **`accou2024sparrkulee`**: Accou, B., Bollens, L., Gillis, M., Verheijen, W., Van hamme, H., & Francart, T. (2024). *SparrKULee: A speech-evoked auditory response repository from KU Leuven, containing the EEG of 85 participants*. Data, 9(8), 94 (`10.3390/data9080094`).
