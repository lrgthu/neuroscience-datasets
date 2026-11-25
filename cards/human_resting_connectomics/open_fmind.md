# Open-fMIND (`cbarbano/open-fmind` · Barbano et al., 2026)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Transforms the fragmented long tail of OpenNeuro into the largest **open-access, uniformly preprocessed, model-ready fMRI pretraining corpus** (`Barbano, Marraffini & Wassermann, Inria MIND, arXiv:2611.21215`). Whereas UK Biobank, HCP, and ABCD require gated Data Use Agreements and focus heavily on resting-state or narrow task batteries, **Open-fMIND** openly releases **`11,379` subjects**, **`45,731` runs (`6,044 hours`)**, and **`429` distinct task labels** (`81%` task runs, `19%` resting-state runs) across **`322` OpenNeuro studies**, achieving downstream transfer with Brain-Semantoks on `HCP-YA` (`r = 0.415` cognition, `0.945` sex AUROC), `ABIDE`, and `ADHD-200` on par with gated UK Biobank pretraining.
- **52-Atlas Multi-View Design (`14` Parcellation Families, `~2.4M` ROI Timeseries)**:
  - **Hard Parcellations (`labels` masker)**: `Schaefer` (`14` variants: `100–1000` in Yeo-7/17 + `+Tian S2 [432]` / `+Tian S3 [450]`), `Yan` (`12` variants: `100–800 × {yeo7, yeo17, kong17}`), `BASC` (`64, 122, 197, 325, 444`), `Tian` subcortical (`16, 32, 50`), `Harvard-Oxford` (`48` cortical, `21` subcortical), `Yeo` (`7, 17`), `AICHA` (`384`), `Glasser HCP-MMP1.0` (`360`), `AAL` (`166`), `Destrieux` (`150`), and `Pauli` subcortical (`16`).
  - **Soft Probabilistic Decompositions (`maps` masker preserving spatial overlap)**: `DiFuMo` (`64, 128, 256, 512, 1024`), `Smith` (`10, 20, 70`), and `MSDL` (`39`).

## 2. Recording Specifications, Variants & Storage Layout
- **Uniform `fMRIPrep 25.2.3` Volumetric Backbone**: Head-motion correction, T1w coregistration, optional slice-timing/SDC when metadata permits, and single-step resampling to `MNI152NLin2009cAsym` (`2 mm` isotropic; FreeSurfer disabled; no cerebellar parcellation in released atlases).
- **Two Released Versions (`4.32 TB` total across `1,787` uncompressed `~3 GB` WebDataset `.tar` shards)**:
  1. **`quasiraw` (`322` studies, `11,379` subjects, `45,731` runs, `2.38M` series)**: Unfiltered, unscrubbed ROI timeseries (`n_ROIs × 1 × 1 × n_timepoints`, `float32` NIfTI + JSON provenance sidecar) **strictly frame-aligned** with companion `fMRIPrep` confounds TSVs + Pearson connectivity matrices.
  2. **`preproc` (`320` studies, `11,320` subjects, `45,019` runs, `2.34M` series)**: Regresses `26` confounds (`24` expanded motion parameters + `WM` + `CSF`, **no GSR**), censors frames with `FD > 0.5 mm` prior to filtering, applies linear detrending + **`0.01–0.1 Hz` Butterworth bandpass**, standardizes each ROI to unit variance, and drops runs with `<50` remaining volumes (`712` runs excluded).
- **Selective HTTP Range-Request Streaming**: `index/*.parquet` records the exact `.tar` shard and byte offset of every file, allowing single-atlas (`e.g. atlas-schaefer400tians2`), rest-only, or single-run streaming without downloading `4.32 TB`.

## 3. Canonical Splits, Validation Benchmarks & Modeling Pitfalls
- **Technical Validation Baselines**:
  - **Multi-Visit Fingerprinting**: `1,649` subjects with $\ge 2$ sessions (`2,192` query visits in `57` studies) yield `72.0%` corpus-wide top-1 accuracy (`85.1%` within-dataset, $I_{\text{diff}} = 25.5$).
  - **Downstream Transfer**: Pretrain on resampled `TR = 2.0 s` windows (`160` volumes, z-scored per ROI) and evaluate frozen/probed representations on external cohorts (`HCP-YA`, `ABIDE`, `ADHD-200`).
- **Critical Modeling Pitfalls**:
  1. **Benchmark Study Overlap Leakage (`Check Accession List First!`)**: Open-fMIND v1.0 includes **`ds000113` (`StudyForrest`)**, **`ds002345` (`Narratives`)**, **`ds001132` (`Sherlock`)**, **`ds002322` (`Alice`)**, **`ds002837` (`Naturalistic Neuroimaging Database`)**, and **`ds004718` (`Le Petit Prince Cantonese`)**! Filter out any downstream evaluation study (and shared multi-study cohorts) using the Parquet provenance index before pretraining.
  2. **Never Use `preproc` for Frame-Locked Stimulus Encoding**: Because `preproc` drops `FD > 0.5 mm` frames (`58.4%` of runs lose $\ge 1$ volume) and low-passes at `0.1 Hz`, frame indices no longer match `events.tsv` timestamps—always start from **`quasiraw` + `quasiraw_confounds`** when aligning with naturalistic audio/video/task stimuli!
  3. **Scanner/Protocol Confounds & Variable `TR`**: Native `TR` varies across the `322` studies (always read `RepetitionTime` from each run's JSON sidecar and resample explicitly), and study-of-origin explains a median $\omega^2 = 0.082$ (`~8.2%`) of edge variance (`60.3%` 268-way site classification accuracy).
  4. **Hierarchical Atlas Sampling & Non-Uniform Licenses**: Sample **atlas family first, then resolution** (since `Schaefer + Yan` represent `26 / 52` atlases), keep all `52` views of a subject inside the same CV split, and inspect `LICENSES.tsv` if excluding `CC-BY-SA-4.0` (`ds001439`, `ds001722`, `ds001748`) or `CC-BY-NC-4.0` (`ds001338`).

## 4. Programmatic Download & Quickstart
```bash
# 1. Fetch lightweight metadata tables and Parquet byte-offset indices (~tens of MB, zero auth)
uvx --from huggingface_hub hf download cbarbano/open-fmind \
  README.md LICENSES.tsv atlases.tsv qc.tsv \
  index/preproc_timeseries.parquet index/quasiraw_timeseries.parquet \
  --repo-type dataset --local-dir ./open_fmind_meta

# 2. Stream or download a single parcellation (e.g., Schaefer-400 + Tian-S2 = 432 cortical+subcortical ROIs)
uvx --from huggingface_hub hf download cbarbano/open-fmind \
  --include "preproc/timeseries/atlas-schaefer400tians2/*" \
  --repo-type dataset --local-dir ./open_fmind_schaefer400tians2
```

## 5. Verified Primary References
- **`barbano2026openfmind`**: Barbano, C. A., Marraffini, G., & Wassermann, D. (2026). *Open-fMIND: A Large-Scale Open-Access fMRI Corpus for Pretraining Brain Foundation Models*. arXiv (`arXiv:2611.21215`).
- **Companion Native-Space 4D Voxel Corpus**: See **`readyneuro`** (`cards/human_resting_connectomics/readyneuro.md`, `817` OpenNeuro studies / `22,083 h` BOLD rigidly aligned at `2 mm` / `1.0 Hz` without parcellation) when training 4D volumetric ViT/MAE architectures rather than ROI-atlas models.
