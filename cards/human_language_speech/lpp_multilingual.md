# Le Petit Prince Multilingual fMRI (`LPP` / `ds003643`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: The primary open **multilingual** naturalistic narrative neuroimaging benchmark (`Li et al., Scientific Data, 2022`), recording `112` participants across **English (`N = 49`)**, **Mandarin Chinese (`N = 35`)**, and **French (`N = 28`)** listening to the entire *The Little Prince* audiobook (`~100 minutes`, split into `9` runs) followed by comprehension quizzes.
- **Rich Linguistic Annotations (`annotation/`)**: Acoustic pitch (`F0`) and root-mean-square intensity, exact word/character timestamps, log lexical frequency, top-down/bottom-up **constituency parser node counts**, and static/contextualized embeddings across all three languages.

## 2. Recording Specifications & Preprocessing
- **Multi-Echo Acquisition**: `3T` GE Discovery MR750 multi-echo planar imaging (`3` echoes: `TE = 12.8, 27.5, 43.0 ms`, `TR = 2.0 s`), processed with **ME-ICA** (`tedana`) to separate $T_2^*$ BOLD fluctuations from non-BOLD head-motion and physiological artifacts—especially valuable in anterior temporal lobe (`ATL`) regions prone to susceptibility dropout.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Leave-one-run-out across `run-1` to `run-9`, with group-level statistical testing across subjects within each language (`EN`, `ZH`, `FR`).
- **Critical Modeling Pitfalls**:
  1. **Cross-Language Alignment**: Because human narrators read at language-specific cadences, run durations differ slightly across `EN`, `ZH`, and `FR`—align cross-lingual spaces via sentence-aligned translation indices rather than raw timepoints.
  2. **Syntactic vs. LLM Surprisal Collinearity**: Parser node count correlates with word length, punctuation pauses, and LLM surprisal; always partial out prosodic boundaries (`F0` resets + pause duration) and word-rate impulses.

## 4. Programmatic Download & Quickstart
```bash
datalad install https://github.com/OpenNeuroDatasets/ds003643.git
cd ds003643
datalad get annotation derivatives/EN/sub-EN057
```

## 5. Verified Primary References
- **`li2022lpp`**: Li, J., Bhattasali, S., Zhang, S., et al. (2022). *Le Petit Prince multilingual naturalistic fMRI corpus*. Scientific Data (`10.1038/s41597-022-01625-7`).
