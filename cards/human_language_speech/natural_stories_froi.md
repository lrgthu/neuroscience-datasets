# Fedorenko Lab Natural Stories fROI fMRI & Reading Corpus (`OSF:eyp8q` / Blank 2014 · Shain 2020 · Futrell 2021)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Bridges controlled psycholinguistic experimentation and ecologically valid narrative neuroscience (`Blank et al., Journal of Neurophysiology, 2014`; `Shain et al., Neuropsychologia, 2020`; `Futrell et al., Language Resources and Evaluation, 2021`). Standard unedited corpora rarely contain enough non-local syntactic dependencies (object-extracted relative clauses, tough-movement, clefts, idioms) to distinguish competing parsing and working-memory theories; the **Natural Stories Corpus** edits `10` stories (`10,245` words, `485` sentences) to pack dense, low-frequency syntactic constructions into fluent narratives.
- **Dual Behavioral + Neuroimaging Benchmark**:
  - **3T fMRI Functional-ROI Cohort (`N = 78`, `OSF:eyp8q`)**: Participants passively listened to `~4.5–6 min` recordings of the Natural Stories (including the foundational `Blank2014` cohort benchmarked in `Schrimpf et al., PNAS, 2021`), paired with independent functional localizers isolating the **Core Language Network (`langloc`)** and the **Multiple-Demand (`MD`) Executive Network**.
  - **Self-Paced Reading Cohort (`N = 181`, `GitHub:languageMIT/naturalstories`)**: Word-by-word behavioral reading times (`RT` in `ms`), hand-corrected Penn Treebank constituent & Universal Dependencies parses, and comprehension accuracies on the exact same `10,245` tokens.

## 2. Recording Specifications & Preprocessing
- **Subject-Specific `fROI` Extraction (`GSS` Method)**: `3T` Siemens Trio EPI (`TR = 2.0 s`). Rather than relying on group MNI template coordinates—which blur inter-individual variability across perisylvian association cortex—each participant's BOLD time series is extracted from individualized top-`10%` localizer-responsive voxels within `6` left-hemisphere language parcels (`IFGorb`, `IFG`, `MFG`, `AntTemp`, `PostTemp`, `AngG`), their right-hemisphere homologs, and `20` bilateral frontoparietal `MD` parcels.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Pre-registered `50%` exploratory vs. `50%` held-out confirmatory data split (`OSF:eyp8q`, `Shain et al. 2020`), or `leave-one-story-out` cross-validation across stories (`Schrimpf et al. 2021`, trimming initial/final rest TRs).
- **Critical Modeling Pitfalls**:
  1. **Model Continuous Hemodynamic Convolution Explicitly**: Spoken words arrive asynchronously (`3–4` words per `2.0 s` TR). Convolve word-onset impulses with canonical HRFs or fit Continuous-Time Deconvolutional Regression (`CDR`) while controlling for acoustic sound power, word rate, and lexical frequency.
  2. **Never Conflate `langloc` and `MD` Parcels**: Linguistic predictability (`PCFG` / `LLM` surprisal) selectively drives `langloc` fROIs without recruiting `MD` cortex (`Shain et al., 2020`), whereas exogenous task demands drive `MD` (`Blank et al., 2014`).
  3. **Account for Word-Order Spillover in SPR (`N = 181`)**: Behavioral RTs exhibit `1–3` word lag (`~300–600 ms`), whereas BOLD integrates over `4–8 s`; model lag structure appropriately in each modality.

## 4. Programmatic Download & Quickstart
```bash
# Download fROI fMRI time series & predictors (OSF) + treebanked SPR corpus (GitHub)
uvx osfclient -p eyp8q clone ./natural_stories_fmri
git clone https://github.com/languageMIT/naturalstories.git
```

## 5. Verified Primary References
- **`shain2020predictive`**: Shain, C., Blank, I., van Schijndel, M., Schuler, W., & Fedorenko, E. G. (2020). *fMRI reveals language-specific predictive coding during naturalistic sentence comprehension*. Neuropsychologia, 138, 107307 (`10.1016/j.neuropsychologia.2019.107307`).
- **`blank2014functional`**: Blank, I., Kanwisher, N., & Fedorenko, E. G. (2014). *A functional dissociation between language and multiple-demand systems revealed in patterns of BOLD signal fluctuations*. Journal of Neurophysiology, 112(5), 1105–1118 (`10.1152/jn.00884.2013`).
- **`futrell2021naturalstories`**: Futrell, R., Gibson, E. A. F., Tily, H. J., Blank, I., Vishnevetsky, A., Piantadosi, S. T., & Fedorenko, E. G. (2021). *The Natural Stories corpus: a reading-time corpus of English texts containing rare syntactic constructions*. Language Resources and Evaluation, 55(1), 63–77 (`10.1007/s10579-020-09503-7`).
