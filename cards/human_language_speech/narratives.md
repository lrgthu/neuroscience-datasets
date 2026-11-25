# Narratives Spoken Story fMRI (`Narratives` / `ds002345`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Complementing UT-Speech's *within-subject depth*, Princeton's **Narratives** collection (`Nastase et al., Scientific Data, 2021`) provides **broad across-subject breadth** (`N = 345` unique subjects, `891` functional runs) plus classic psychological manipulations of narrative context, perspective, scrambling, and synonym substitution.
- **Notable Stories Inside `ds002345`**:
  - **`21styear`**: `~56 min` continuous dual-timeline narrative (`N = 25`, `TR = 1.5 s`) — strong single-story encoding benchmark.
  - **`pieman` (`N = 82`)**: `7.5 min` benchmark story used for large-sample ISC and hyperalignment.
  - **`prettymouth` (`N = 40`)**, **`milkyway` (`N = 53`)**, **`sherlock` / `merlin`**, **`lucy`**, **`slumlordreach`**, **`tunnel`**, **`black`**, **`forgot`**.

## 2. Recording Specifications & Preprocessing
- **Derivatives Included**: Raw BIDS + `fMRIPrep` (`fsaverage6` cortical surface GIfTI files and `MNI152NLin2009cAsym` volumes) + `AFNI` denoised nuisance-regressed versions (`nosmooth` and `6 mm` smoothed) + `Gentle` forced-aligner word/phoneme timestamps.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Repeat / ISC Ceiling**: Because `20–82` subjects listen to identical time-locked audio, leave-one-subject-out **Inter-Subject Correlation (`ISC`)** cleanly bounds the stimulus-driven shared signal without requiring within-subject repeats.
- **Critical Modeling Pitfalls**:
  1. **Verify `RepetitionTime` Per Story**: Most stories use `TR = 1.5 s`, whereas legacy runs (e.g., `pieman` original Skyra cohort) use `TR = 1.5 s` or `2.0 s` with variable initial silence buffers (`music` / fixation lead-in documented in `stimuli/README`).
  2. **Use `nosmooth` Surface Derivatives (`fsaverage6`) for Fine-Scale Encoding**: Spatial `6 mm` smoothing inflates univariate ISC but blurs fine-grained multivariate/ridge tuning patterns.

## 4. Programmatic Download & Quickstart
```bash
# Install OpenNeuro ds002345 via DataLad and pull fsaverage6 AFNI-nosmooth derivatives for '21styear'
datalad install https://github.com/OpenNeuroDatasets/ds002345.git
cd ds002345
datalad get stimuli derivatives/afni-nosmooth/sub-*/func/*task-21styear*fsaverage6*.func.gii
```

## 5. Verified Primary References
- **`nastase2021narratives`**: Nastase, S. A., Liu, Y.-F., Hillman, H., et al. (2021). *The “Narratives” fMRI dataset for evaluating models of naturalistic language comprehension*. Scientific Data (`10.1038/s41597-021-01033-3`).
