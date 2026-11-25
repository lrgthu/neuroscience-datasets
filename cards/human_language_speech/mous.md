# Mother of Unification Studies (`MOUS`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Uniquely combines **compositionality control** (intact sentences vs. lexically matched scrambled word lists), **amodal comparison** (`102` visual reading subjects `sub-V*` vs. `102` auditory listening subjects `sub-A*`), and **within-subject multimodal imaging** (every one of the `204` participants completed task fMRI, resting-state fMRI, structural T1w, diffusion MRI, and `275`-channel MEG) (`Schoffelen et al., Scientific Data, 2019`).
- **Stimulus Design**: `360` Dutch sentences (varying syntactic complexity including relative clauses) and `360` scrambled word-list analogs, divided so each subject saw/heard `180` sentences and `180` non-overlapping word lists in alternating mini-blocks.

## 2. Recording Specifications & Preprocessing
- **fMRI**: `3T` Siemens Trio (`TR = 2.0 s`, `3.5 × 3.5 × 3.0 mm`).
- **MEG**: `275`-channel axial gradiometer CTF system (`1,200 Hz`) with continuous head localization coils and `EyeLink 1000` eye-tracking.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Group-by-stimulus-root $k$-fold cross-validation (`10`-fold over the `360` base items) or cross-subject generalization (`N = 102` per sensory cohort).
- **Critical Modeling Pitfalls**:
  1. **Sentence ↔ Word-List Lexical Leakage**: Always assign a sentence and its scrambled word-list twin to the **same** CV fold when testing supra-word compositionality (`supraword` / context embeddings minus lexical embeddings).
  2. **Presentation Rate Differences**: Visual reading uses variable word duration matched to spoken duration (`~300–600 ms/word`), whereas auditory speech presents continuous co-articulated waveforms—include modality-appropriate sensory regressors.

## 4. Programmatic Download & Quickstart
```bash
# Access BIDS collection DSC_3011020.09_236 on Donders Repository (WebDAV / rclone supported)
open "https://data.donders.ru.nl/collections/di/dccn/DSC_3011020.09_236"
```

## 5. Verified Primary References
- **`schoffelen2019mous`**: Schoffelen, J.-M., Oostenveld, R., Lam, N. H. L., Uddén, J., Hultén, A., & Hagoort, P. (2019). *A 204-subject multimodal neuroimaging dataset to study language processing*. Scientific Data (`10.1038/s41597-019-0020-y`).
