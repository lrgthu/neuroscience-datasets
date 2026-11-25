# The "Podcast" Intracranial ECoG Dataset (`Podcast-ECoG` / `ds005574`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Combines **high spatial specificity** (`mm`-scale subdural ECoG grids/strips & depth contacts) and **millisecond temporal fidelity** (`512 Hz` high-gamma `70–200 Hz` broadband) in `9` neurosurgical patients listening to the exact same `30-minute` *This American Life* narrative (*"So a Monkey and a Horse Walk Into a Bar"*, `~5,000` words) (`Zada et al., Scientific Data, 2025`; `Goldstein et al., Nature Neuroscience, 2022`).
- **Pre-Packaged Feature Banks**: Ships directly with aligned audio, word-level transcripts, phonetic/acoustic envelopes, syntactic features, and autoregressive/masked LLM embeddings alongside `hassonlab/podcast-ecog-tutorials`.

## 2. Recording Specifications & Preprocessing
- **Electrodes & Coordinates**: `1,330` clean electrodes localized on individual `fsaverage` cortical surfaces and `MNI` coordinates across perisylvian language cortex (`HG`, `STG`, `MTG`, `IFG`, `vSMC`, `AG/SMG`).
- **Derivatives (`derivatives/ecogprep/`)**: Despiked, `60/120/180 Hz` notch-filtered, common-average re-referenced broadband high-gamma power (`70–200 Hz` Hilbert envelope at `512 Hz`).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: `K = 10` contiguous temporal folds (`~3 min` per fold) across the `30-minute` story; never shuffle individual word tokens!
- **Critical Modeling Pitfalls**:
  1. **Disentangling Next-Word Prediction from Co-Articulation & Context Autocorrelation**: When plotting lag-resolved encoding curves (`lag ∈ [-2,000, +2,000 ms]` relative to word onset `0 ms`), control for acoustic envelope, word onset impulses, and prior-word context to isolate genuine predictive vs. post-onset integrative dynamics across `STG` (Wernicke) and `IFG` (Broca).
  2. **Patient-Level Hierarchical Inference**: Electrodes within the same patient grid share local volume conduction and patient state—test hypotheses via hierarchical/cluster bootstrap over **patients (`N = 9`)** in addition to electrode counts.

## 4. Programmatic Download & Quickstart
```bash
# Clone BIDS-iEEG Podcast dataset from OpenNeuro
datalad install https://github.com/OpenNeuroDatasets/ds005574.git
cd ds005574
datalad get stimuli derivatives/ecogprep
```

## 5. Verified Primary References
- **`zada2025podcast`**: Zada, Z., Nastase, S. A., Aubrey, B., et al. (2025). *The “Podcast” ECoG dataset for modeling neural activity during natural language comprehension*. Scientific Data (`10.1038/s41597-025-05462-2`).
- **`goldstein2022shared`**: Goldstein, A., Zada, Z., Buchnik, E., et al. (2022). *Shared computational principles for language processing in humans and deep language models*. Nature Neuroscience (`10.1038/s41593-022-01026-4`).
