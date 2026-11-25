# Stanford Intracortical Speech Neuroprosthesis & Brain-to-Text Benchmark (`Willett-Speech-BCI` / `Dryad:10.5061/dryad.x69p8czpq`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: First intracortical speech neuroprosthesis demonstrating rapid, large-vocabulary brain-to-text communication (`62 words/min`, `125,000-word` vocabulary) in a clinical participant (`T12`) with bulbar-onset amyotrophic lateral sclerosis (`ALS`) and severe dysarthria/anarthria (`Willett et al., Nature, 2023`).
- **Task Suite**:
  1. **Large-Vocabulary Sentence Copy / Vocalized & Silent Attempted Speech**: `12,100` prompted sentences spanning `24+` longitudinal recording sessions (`~10,850` sentences standardized into the widely adopted **Brain-to-Text Benchmark '24**), plus `50-word` small-vocabulary validation blocks (`9.1%` WER).
  2. **Instructed-Delay Orofacial, Phoneme & Single-Word Mapping**: Isolated movements of the jaw, lips, tongue, and larynx alongside `39` English phonemes to dissociate fine-grained articulatory somatotopy across dorsal (`6v-d`) and ventral (`6v-v`) speech premotor subfields.

## 2. Recording Specifications & Preprocessing
- **Microelectrode Implantation**: Four `64-channel` (`8 × 8`) intracortical Utah arrays (`256` total electrodes): two implanted in left **ventral premotor cortex (`area 6v`)** and two implanted in left **inferior frontal gyrus (`area 44` / Broca's area)**.
- **Feature Extraction (`20 ms` / `50 Hz`)**: Raw `30 kHz` voltage streams are high-pass filtered to extract per-channel **multi-unit threshold crossings (`TX`)** and **spike-band power (`SBP`, `250–5,000 Hz`)** concatenated into `512`-dimensional feature vectors per `20 ms` bin (`256 TX + 256 SBP`), rolling-block $z$-scored within each recording block to mitigate intraday baseline drift.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Benchmark Split & Metrics**: Each of the `24` competition sessions is partitioned chronologically into `train`, `test` (public validation), and `competitionHoldOut` sentence blocks. Models train with **Connectionist Temporal Classification (`CTC`)** loss over `39` ARPABET phonemes + silence token, evaluated on both raw **Phoneme Error Rate (`PER`)** and beam-search + LLM-rescored **Word Error Rate (`WER`)**.
- **Critical Modeling Pitfalls**:
  1. **Mandatory Day-Specific Input Projections & Rolling Normalization**: Electrode impedance, micromotion, and neural turnover shift firing statistics across days and even across `10-minute` blocks within a day. Always combine **within-block rolling $z$-scoring** with **day-specific affine input transformations** (plus white-noise + constant-offset data augmentation).
  2. **`Area 6v` vs. `Area 44` Channel Selection**: In participant `T12`, the two `area 44` arrays (`128` channels) contained almost no speech-related modulation (`Willett et al., 2023`); slicing to the `128` `area 6v` channels (`256` features: `128 TX + 128 SBP`) cuts input dimensionality in half and regularly improves generalization.
  3. **Decouple Neural Encoder Gains from Language Model Rescoring**: Always report un-rescored **CTC greedy `PER`** alongside $n$-gram + LLM-rescored `WER` so improvements in causal/bidirectional neural backbones (`GRU`, `Conformer`, `Mamba`, `Diphone CTC`) are never conflated with stronger external language priors.

## 4. Programmatic Download & Quickstart
```bash
# Download full Dryad dataset archive (CC0-1.0) and official baseline code
curl -L "https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.x69p8czpq/download" \
  -o willett_speech_bci_2023.zip
git clone https://github.com/fwillett/speechBCI.git
```

## 5. Verified Primary References
- **`willett2023speechbci`**: Willett, F. R., Kunz, E. M., Fan, C., Avansino, D. T., Wilson, G. H., Choi, E. Y., Kamdar, F. B., Glasser, M. F., Hochberg, L. R., Druckmann, S., Shenoy, K. V., & Henderson, J. M. (2023). *A high-performance speech neuroprosthesis*. Nature (`10.1038/s41586-023-06377-x`).
