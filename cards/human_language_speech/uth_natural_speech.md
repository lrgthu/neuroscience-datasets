# UT Austin Naturalistic Speech fMRI (`UT-Speech` / `ds003020`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: The flagship **deep single-subject** naturalistic speech fMRI corpus (`LeBel et al., Scientific Data, 2023`; extending `Huth et al., Nature, 2016`), powering modern LLM voxelwise encoding, cortical semantic-map discovery, and non-invasive continuous semantic decoding (`Tang et al., Nature Neuroscience, 2023`).
- **Stimulus Design & Timing**: Unscripted autobiographical stories from *The Moth Radio Hour* (`10–15 min` per story). All `8` subjects (`UTS01–UTS08`) completed the core `5`-session `27`-story battery (`~6 hours`), while `UTS01–UTS03` completed up to `15–20` sessions (`80–95` stories, `~16–18+ hours` per subject). Includes visual/auditory/motor/language localizers and `pycortex` cortical surfaces.

## 2. Recording Specifications & Preprocessing
- **Acquisition & Derivatives**: `3T` Siemens Skyra (`2.6 mm` isotropic, `TR = 2.00 s`, multiband `2`). Both raw BIDS NIfTI volumes and motion-corrected, detrended, within-run z-scored `HDF5` matrices (`derivatives/preprocessed_data/`) plus Praat `TextGrid` word/phoneme alignments (`derivatives/TextGrids/`) are directly available in `ds003020`.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Hold out **`wheretheressmoke`** (`1` story repeated `5–10` times across sessions) as the untouched test set; use story-level $k$-fold or contiguous `50-TR` chunk cross-validation on training stories to select ridge penalties $\lambda$.
- **Repeat Structure & Noise Ceiling**: Compute **Signal Power Explained (`SPE` / `CC_max`)** across the `5–10` repeats of `wheretheressmoke` (`Hsu et al., 2004`; `Schoppe et al., 2016`) rather than reporting unnormalized $r$ alone.
- **Critical Modeling Pitfalls**:
  1. **Lanczos Interpolation + `[1, 2, 3, 4]` TR FIR Delays**: In Huth Lab pipelines, word-level embeddings positioned at word midpoints are resampled to TR acquisition centers via a `3`-lobe Lanczos filter, then lagged by `2, 4, 6, 8 s` (`1–4 TRs`).
  2. **Banded Ridge Nuisance Control**: Word-rate (`1` impulse per word) and mel-spectrogram / articulatory features explain substantial variance in superior temporal cortex; use `himalaya` (`MultipleKernelRidgeCV` / `BandedRidgeCV`) with separate $\lambda_g$ hyperparameters per feature space.

## 4. Programmatic Download & Quickstart
```bash
# Install OpenNeuro ds003020 via DataLad and pull preprocessed HDF5 + TextGrids for UTS01
datalad install https://github.com/OpenNeuroDatasets/ds003020.git
cd ds003020
datalad get derivatives/TextGrids derivatives/preprocessed_data/UTS01
```

## 5. Verified Primary References
- **`lebel2023utspeech`**: LeBel, A., Wagner, L., Jain, S., et al. (2023). *A natural language fMRI dataset for voxelwise encoding models*. Scientific Data (`10.1038/s41597-023-02437-z`).
- **`huth2016semantic`**: Huth, A. G., de Heer, W. A., Griffiths, T. L., Theunissen, F. E., & Gallant, J. L. (2016). *Natural speech reveals the semantic maps that tile human cerebral cortex*. Nature (`10.1038/nature17637`).
