# *The Grand Budapest Hotel* Social Movie 3T fMRI (`Budapest-fMRI`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Released by the Dartmouth Gobbini/Haxby group (`Visconti di Oleggio Castello et al., Scientific Data, 2020`, `OpenNeuro:ds003017`), **Budapest-fMRI** combines fast `1.0 s` multiband whole-brain sampling (`N = 25`), rich social/face/dialogue interactions, and standardized `fMRIPrep` cortical surfaces, making it one of the cleanest modern benchmarks for **surface hyperalignment**, **social/face VLM encoding**, and **multimodal brain foundation model evaluation**.
- **Stimulus Design & Timing**:
  - Prior to entering the scanner, each subject watched the first `~46.5 min` of Wes Anderson's *The Grand Budapest Hotel* (`2014`) outside the bore to establish character familiarity and plot context.
  - Inside the scanner, subjects watched the remaining **`~50.5 min`** divided into **`5` runs** (`598`, `498`, `535`, `618`, and `803` TRs at `TR = 1.0 s`), accompanied by `2` dynamic visual localizer runs (`faces`, `bodies`, `scenes`, `objects`, `scrambled objects`) in `21/25` subjects.
- **Subject Cohort**: `25` healthy right-handed adults (`13` female, `12` male) with normal or corrected-to-normal vision.

## 2. Recording Specifications & Preprocessing
- **Acquisition Hardware & Resolution**: `3T` Siemens Magnetom Prisma (Dartmouth Brain Imaging Center), `32`-channel head coil, multiband-`4` gradient-echo EPI at `2.5 mm` isotropic (`TR = 1.0 s`, `TE = 33 ms`, flip angle `59°`, `52` slices, full brain).
- **Released Derivatives (`ds003017`)**:
  - Raw BIDS NIfTIs (`anat` T1w/T2w + `func` movie + `fmap` spin-echo phase-encoding-reversed fieldmaps) and complete **`fMRIPrep`** volumetric (`MNI152NLin2009cAsym`) and surface (`fsaverage` / `fsnative`) derivatives + nuisance confound TSVs.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Leave-one-run-out (`5`-fold) across the `5` movie runs for within-subject/hyperaligned encoding models, plus split-cohort (`15` train / `10` test subjects) for cross-subject generalization.
- **Noise Ceiling**: Group leave-one-subject-out Inter-Subject Correlation (`ISC`) and hyperaligned ISC ceilings across `fsaverage` vertices (`r > 0.5–0.7` in early visual, auditory `STG`, `pSTS`, `FFA`, and `TPJ`).
- **Critical Modeling Pitfalls**:
  1. **Mandatory Boundary Trimming (`10 s` Replay Overlap)**: Runs `2–5` replay the last `10 s` (`10 TRs`) of the previous run (plus pre/post fixation padding); trim duplicated transition TRs and `~8 s` HRF tails before computing cross-run test metrics!
  2. **Second-Half Film Alignment Only**: Never align timestamps starting from `00:00:00` of the commercial Blu-ray/DVD; use the exact FFmpeg frame-cut script in `mvdoc/budapest-fmri-data` starting at `~00:46:28`.

## 4. Programmatic Download & Quickstart
```bash
# Install raw BIDS + fMRIPrep surface derivatives from OpenNeuro
datalad install https://github.com/OpenNeuroDatasets/ds003017.git
aws s3 ls --no-sign-request s3://openneuro.org/ds003017/derivatives/fmriprep/

# Official stimulus-cutting FFmpeg scripts & validation code
git clone https://github.com/mvdoc/budapest-fmri-data.git
```

## 5. Verified Primary References
- **`visconti2020budapest`**: Visconti di Oleggio Castello, M., Chauhan, V., Jiahui, G., & Gobbini, M. I. (2020). *An fMRI dataset in response to "The Grand Budapest Hotel", a socially-rich, naturalistic movie*. Scientific Data (`10.1038/s41597-020-00735-4`).
