# StudyForrest (`7T` Audio & `3T` Audiovisual *Forrest Gump* + Eye Gaze)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: A foundational open ecosystem for naturalistic cognition (`Hanke et al., Scientific Data, 2014, 2016`; `Sengupta et al., 2016`), combining **7T high-resolution audio-movie fMRI** (`N = 20`), **3T whole-brain audiovisual movie fMRI with simultaneous in-scanner 1,000 Hz eye-tracking** (`N = 15` overlapping subjects), retinotopic mapping, category localizers (`FFA/OFA/PPA/EBA/LOC`), musical genre runs, and dense community annotations (scene cuts, characters, portrayed emotions, speech transcripts, optical flow).
- **Stimulus Design & Timing**: Two-hour abridged **German-dubbed** version of *Forrest Gump*, split into `8` contiguous `~15 min` functional runs (`TR = 2.0 s`).

## 2. Recording Specifications & Preprocessing
- **Acquisition**:
  - **Phase 1 (`7T` Audio-Description Movie)**: `1.4 mm` isotropic T2*-weighted EPI (`TR = 2.0 s`), high spatial specificity across auditory, temporal, and ventral visual cortices.
  - **Phase 2 (`3T` Audiovisual Movie + Gaze)**: Whole-brain `3.0 mm` EPI (`TR = 2.0 s`) + `1,000 Hz` EyeLink 1000 gaze coordinates enabling **retinotopic/foveated** rather than screen-centered visual encoding!

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: `8`-fold leave-one-movie-segment-out cross-validation (`run-01` through `run-08`).
- **Critical Modeling Pitfalls**:
  1. **Segment-Boundary Stimulus Overlap**: Consecutive runs repeat several seconds of the preceding scene at run onset—**explicitly drop overlapping boundary TRs** so identical scenes never appear in both train and test folds!
  2. **German Audio Track**: All participants listened to the German dub (and German audio-description in 7T Phase 1); use German LLMs/ASR alignments rather than English *Forrest Gump* scripts.
  3. **Free-Viewing Gaze Shifts**: In 3T audiovisual runs, subjects freely moved their eyes—incorporate the simultaneous `1,000 Hz` gaze coordinates when modeling V1–V4 receptive fields.

## 4. Programmatic Download & Quickstart
```bash
# Install modular StudyForrest DataLad superdataset (or OpenNeuro ds000113)
datalad install https://github.com/psychoinformatics-de/studyforrest-data.git
```

## 5. Verified Primary References
- **`hanke2014studyforrest`**: Hanke, M., Baumgartner, F. J., Ibe, P., et al. (2014). *A high-resolution 7-Tesla fMRI dataset from complex natural stimulation with an audio movie*. Scientific Data (`10.1038/sdata.2014.3`).
- **`hanke2016studyforrest_av`**: Hanke, M., Adelhöfer, N., Kottke, D., et al. (2016). *A studyforrest extension, simultaneous fMRI and eye gaze recordings during prolonged natural stimulation*. Scientific Data (`10.1038/sdata.2016.92`).
- **`sengupta2016studyforrest_ret`**: Sengupta, A., Kaule, F. R., Guntupalli, J. S., et al. (2016). *A studyforrest extension, retinotopic mapping and localization of higher visual areas*. Scientific Data (`10.1038/sdata.2016.93`).
