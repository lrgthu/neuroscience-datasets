# Rutishauser Lab Human Medial Temporal & Frontal Single-Neuron NWB Suite (`DANDI:000004`, `000469`, `000623`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Largest harmonized open-access **Neurodata Without Borders (`NWB`)** collection of **human single-neuron recordings** (`>4,835` spike-sorted units across `135` sessions) from Behnke–Fried hybrid depth microwires in neurosurgical epilepsy monitoring patients, curated by Ueli Rutishauser's consortium:
  1. **`DANDI:000004` — Declarative Recognition Memory (`Chandravadia et al., Scientific Data, 2020`)**: `1,576` single neurons (`65` sessions across `42` patients) in **hippocampus** and **amygdala** during new/old visual category learning and `1–6` confidence-rated recognition memory.
  2. **`DANDI:000469` — Sternberg Working Memory (`Kyzar et al., Scientific Data, 2024`)**: `1,809` single neurons (`41` sessions across `21` patients) spanning **MTL** (`hippocampus`, `amygdala`) and **medial frontal cortex** (`dACC`, `pre-SMA`, `vmPFC`) maintaining `1–3` concept-screened images across delay intervals.
  3. **`DANDI:000623` — Multimodal Naturalistic Movie Watching (`Keleş et al., Scientific Data, 2024`)**: `1,450` single neurons (`29` sessions across `16` patients) with simultaneous **intracranial macro-EEG (`iEEG`)**, **microwire LFP**, **`500 Hz` eye tracking**, event-boundary behavior, and matched **`3T` fMRI** watching Hitchcock's *Bang! You're Dead*.

## 2. Recording Specifications & Preprocessing
- **Hybrid Electrodes & Spike Sorting**: `8` platinum-iridium `40 µm` microwires protruding from the tip of clinical depth electrodes (`32 kHz` broadband, semi-automatically spike-sorted with `OSort` quality metrics: isolation distance, ISI `< 3 ms` refractory violations `< 3%`, waveform SNR) stored natively inside self-contained NWB `units` tables with MNI coordinates.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Pseudopopulation vs. Simultaneous Decoding**: Within-session models capture real-time **theta-phase spike-field locking** (`dACC ↔ hippocampus`), whereas cross-session **pseudopopulations** align condition-matched trials (`old/new × confidence` or `working-memory load 1–3`) via stratified $K$-fold splits; on `DANDI:000623`, use contiguous movie time-blocks synchronized across all `16` patients.
- **Critical Modeling Pitfalls**:
  1. **Patient Cohort Overlap & Hierarchical Inference**: Each Dandiset numbers participants independently (`42`, `21`, `16` patient cohorts across multi-site Cedars-Sinai / Toronto / Johns Hopkins releases); always group cross-validation and mixed-effects statistics at the **patient/session level**, never treating co-recorded neurons as independent observations.
  2. **Account for Personalized Screening Bias in `DANDI:000469`**: Because the `5` Sternberg task images per session were actively chosen from a prior screening block based on selective neural firing, baseline concept-tuning rates in the Sternberg block are enriched by design.
  3. **Event-Boundary Saccade Confounds in `DANDI:000623`**: Cognitive event boundaries during movie watching co-occur with blinks, pupil dilations, and saccadic resets—always include the provided `500 Hz` eye-tracking regressors when modeling hippocampal event-boundary cells.

## 4. Programmatic Download & Quickstart
```bash
# Stream or download all three standardized human single-unit NWB Dandisets
uvx dandi download DANDI:000004 DANDI:000469 DANDI:000623
```

## 5. Verified Primary References
- **`chandravadia2020human`**: Chandravadia, N., Liang, D., Schjetnan, A. G. P., Carlson, A., Faraut, M., Chung, J. M., et al. (2020). *A NWB-based dataset and processing pipeline of human single-neuron activity during a declarative memory task*. Scientific Data (`10.1038/s41597-020-0415-9`).
- **`kyzar2024sternberg`**: Kyzar, M., Kamiński, J., Brzezicka, A., Reed, C. M., Chung, J. M., Mamelak, A. N., & Rutishauser, U. (2024). *Dataset of human-single neuron activity during a Sternberg working memory task*. Scientific Data (`10.1038/s41597-024-02943-8`).
- **`keles2024multimodal`**: Keleş, Ü., Dubois, J., Le, K. J. M., Tyszka, J. M., Kahn, D. A., Reed, C. M., et al. (2024). *Multimodal single-neuron, intracranial EEG, and fMRI brain responses during movie watching in human patients*. Scientific Data (`10.1038/s41597-024-03029-1`).
