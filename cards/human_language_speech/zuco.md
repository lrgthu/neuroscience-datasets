# ZuCo 1.0 & ZuCo 2.0 Simultaneous EEG & Eye-Tracking Reading Corpora (`OSF:q3zws` & `OSF:2urht`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Largest publicly available **co-registered high-density scalp EEG + infrared eye-tracking** benchmark for natural, self-paced English sentence reading (`Hollenstein et al., Scientific Data, 2018`; `Hollenstein et al., LREC, 2020`). Unlike fixed-pace RSVP paradigms, participants read full sentences naturally on screen at their own pace while word-level fixation boundaries link oculomotor behavior directly to Fixation-Related Potentials (`FRPs`).
- **Two Complementary Releases (`N = 30` Total Readers, `1,846` Sentences)**:
  - **ZuCo 1.0 (`OSF:q3zws`, `N = 12`)**: `1,107` sentences (`21,629` words) spanning three tasks—Movie Review Sentiment Reading (`400` Stanford Sentiment Treebank sentences), Wikipedia Normal Reading (`300` sentences), and Wikipedia Task-Specific Relation Extraction (`407` sentences).
  - **ZuCo 2.0 (`OSF:2urht`, `N = 18`)**: `739` Wikipedia sentences (`390` Normal Reading + `349` Task-Specific Relation Annotation, including `63` controlled sentences read in both regimes to isolate top-down task goals).

## 2. Recording Specifications & Preprocessing
- **Co-Registered Acquisition**: `128`-channel EGI Geodesic HydroCel system (`500 Hz`, `105` clean scalp channels retained after removing outer face/neck/EOG ring channels and `automagic` MARA ICA artifact rejection) synchronized via hardware triggers with an `EyeLink 1000 Plus` eye tracker (`500 Hz`). Word-level `.mat`/HDF5 structures provide `FFD` (first fixation duration), `GD` (gaze duration), `TRT` (total reading time), `GPT` (go-past time), raw fixation time series, and `8` canonical frequency-band power envelopes (`theta1/2`, `alpha1/2`, `beta1/2`, `gamma1/2`).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Mandatory Methodological Warning — The ZuCo EEG-to-Text Leakage Audit (`Jo et al., 2024/2025`)**:
  1. **Implicit Teacher-Forcing & Pure-Noise Parity Trap**: `Jo et al. (arXiv:2405.06459; Scientific Reports, 2025)` proved that prominent ZuCo open-vocabulary `EEG-to-Text` baselines (`BLEU-1 > 40%`) suffered from **implicit teacher-forcing** during evaluation (feeding ground-truth previous tokens into `BART`) and/or overlapping sentence splits across subjects. Under true autoregressive `.generate()` on unseen sentences, prior models performed **identically when fed pure random Gaussian noise instead of real EEG**! Every generative or retrieval study on ZuCo **must** report a matched **Gaussian-noise input baseline (`X ~ N(0, I)`)** and **shuffled-trial baseline** alongside real EEG.
  2. **Deduplicate Shared Sentences Across Subjects & Tasks**: Split strictly by unique `sentence_id` (and exclude the `63` cross-task duplicate sentences from cross-task train/test leakage).
  3. **Saccadic Myogenic Confounds in `Beta`/`Gamma` Bands**: Fixation count and saccade amplitude strongly modulate scalp `30–100 Hz` power via extraocular muscle spikes; always test whether EEG features add predictive power *beyond* scalar word-level `FFD`/`GD`/`TRT` gaze durations alone.

## 4. Programmatic Download & Quickstart
```bash
# Download ZuCo 1.0 (OSF: q3zws) and ZuCo 2.0 (OSF: 2urht)
uvx osfclient -p q3zws clone ./zuco1
uvx osfclient -p 2urht clone ./zuco2
```

## 5. Verified Primary References
- **`hollenstein2018zuco`**: Hollenstein, N., Rotsztejn, J., Tröndle, M., Pedroni, A., Zhang, C., & Langer, N. (2018). *ZuCo, a simultaneous EEG and eye-tracking resource for natural sentence reading*. Scientific Data, 5, 180291 (`10.1038/sdata.2018.291`).
- **`hollenstein2020zuco2`**: Hollenstein, N., Tröndle, M., Zhang, C., & Langer, N. (2020). *ZuCo 2.0: A dataset of physiological recordings during natural reading and annotation*. Proceedings of LREC 2020, 138–146 (`10.3929/ethz-b-000464814` / `arXiv:1912.00903`).
- **`jo2024eegtotext`**: Jo, H., Yang, Y., Han, J., Duan, Y., Xiong, H., & Lee, W. H. (2025). *Evaluating EEG-to-text models through noise-based performance analysis*. Scientific Reports, 15 (`10.1038/s41598-025-29587-x` / `arXiv:2405.06459`).
