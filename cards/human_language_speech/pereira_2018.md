# Pereira Universal Linguistic Decoder Benchmark (`OSF:crwz7` / Pereira et al. 2018)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Introduced the first **universal semantic decoder** capable of training on single word concepts and decoding distributed semantic representations of arbitrary unseen English sentences (`Pereira et al., Nature Communications, 2018`), and subsequently became the single highest-SNR sentence reading benchmark in `Schrimpf et al. (PNAS, 2021)` and `Brain-Score Language`.
- **Three-Experiment Design (`807` Total Stimuli Across `N = 16` Subjects)**:
  - **Experiment 1 (`180` Word Concepts, `N = 16`)**: Concrete and abstract nouns, verbs, and adjectives presented across three disambiguating paradigms (sentences, concept-picture pairs, and semantic word clouds) to isolate modality-invariant conceptual representations.
  - **Experiment 2 (`384` Sentences, `N = 8` of `16`)**: `96` short passages (`4` sentences each) spanning `24` diverse everyday and encyclopedic topics (`4` passages per topic), each sentence presented for `4 s` (`4 s` ITI) and repeated `3` times across runs.
  - **Experiment 3 (`243` Sentences, `N = 6` of `16`, `9` unique subjects across Exp 2 + Exp 3)**: `72` longer Wikipedia-style narrative/expository passages (`3–4` sentences each) spanning `24` independent topics unconnected to Experiment 2.

## 2. Recording Specifications & Preprocessing
- **Acquisition & GLM Betas**: `3T` Siemens Trio whole-brain EPI (`TR = 2.0 s`, `2.0 × 2.0 × 4.0 mm` voxels). Standard `OSF:crwz7` `.mat` archives supply single-stimulus GLM beta vectors per voxel alongside anatomical (`AAL`) and individualized **functional localizer (`fROI`)** masks for the frontotemporal language network (`langloc`: `Sentences > Nonwords`), the domain-general Multiple-Demand (`MD`) network, default mode (`DMN`), and visual cortex.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Within-experiment `5-fold` ridge encoding across the `384` (`Exp 2`) and `243` (`Exp 3`) sentence betas in `langloc` voxels (`Schrimpf et al., 2021`), or cross-experiment zero-shot generalization (`Exp 1 → Exp 2/3` and `Exp 2 ↔ Exp 3`).
- **Critical Modeling Pitfalls**:
  1. **Passage-Disjoint vs. Sentence-Random Cross-Validation**: Subsequent methodological audits demonstrated that random sentence-level splits allow bag-of-words topic identity and within-passage BOLD carryover to inflate encoding scores; always report **passage-grouped** and **topic-grouped** cross-validation to isolate genuine compositional sentence encoding.
  2. **Respect Subject-Specific `langloc` Masks**: Averaging raw anatomical coordinates blurs adjacent language-selective and `MD` subregions inside left inferior frontal gyrus (`Broca's area`); restrict language alignment metrics to individualized `langloc` voxels.
  3. **Contextual Window Alignment**: When feeding sentences to autoregressive LLMs, distinguish isolated single-sentence context from full multi-sentence passage context, as human subjects read the `3–4` sentences of each passage in order.

## 4. Programmatic Download & Quickstart
```bash
# Clone the full OSF archive (MATLAB single-sentence betas, stimuli, and fROI masks)
uvx osfclient -p crwz7 clone ./pereira_2018
```

## 5. Verified Primary References
- **`pereira2018universal`**: Pereira, F., Lou, B., Pritchett, B., Ritter, S., Gershman, S. J., Kanwisher, N., Botvinick, M., & Fedorenko, E. G. (2018). *Toward a universal decoder of linguistic meaning from brain activation*. Nature Communications, 9, 963 (`10.1038/s41467-018-03068-4`).
- **`schrimpf2021neural`**: Schrimpf, M., Blank, I. A., Tuckute, G., Kauf, C., Hosseini, E. A., Kanwisher, N., Tenenbaum, J. B., & Fedorenko, E. G. (2021). *The neural architecture of language: Integrative modeling converges on predictive processing*. Proceedings of the National Academy of Sciences, 118(45), e2105646118 (`10.1073/pnas.2105646118`).
