# Pixar *Partly Cloudy* Developmental Social Brain 3T fMRI (`Partly-Cloudy`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Published by `Richardson, Lisandrelli, Riobueno-Naylor, & Saxe (Nature Communications, 2018)` (`OpenNeuro:ds000228`), **Partly-Cloudy** is one of cognitive neuroscience's most widely taught and benchmarked developmental fMRI datasets (featured natively in `nilearn.datasets.fetch_development_fmri`), charting how the **Theory-of-Mind (`ToM`)** network (`bilateral TPJ`, `precuneus/PC`, `dmPFC/mmPFC/vmPFC`) functionally segregates from the **Physical Pain** network (`anterior insula`, `dACC`, `secondary somatosensory`, `MFG`) between ages `3` and `12`.
- **Stimulus Design & Timing**:
  - Single `5.6-minute` (`168 TRs` at `TR = 2.0 s`) passive viewing of a **silent** (no dialogue; background musical score muted in original design) edit of Disney/Pixar's animated short *Partly Cloudy* (`2009`).
  - Preceded by `10 s` (`5 TRs`) rest and `10 s` (`5 TRs`) opening logos; dense expert-coded event timestamps label **`Mental`** (`4` events, `44 s` — false beliefs, desires, emotional surprise), **`Pain`** (`7` events, `26 s` — alligator bites, electric eel shocks, porcupine quills), **`Social`**, and **`Control`** scenes.
- **Subject Cohort**: `155` total participants: **`122` children** (`ages 3.5–12.3 years`, `64` female) plus **`33` adults** (`ages 18–39 years`, `20` female), accompanied by out-of-scanner behavioral Theory-of-Mind battery scores in children.

## 2. Recording Specifications & Preprocessing
- **Acquisition Hardware & Resolution**: `3T` Siemens Magnetom Tim Trio (MIT), `32`-channel pediatric/adult head coils, whole-brain gradient-echo EPI with online prospective motion correction (**`PACE`**) at `3.0 mm` isotropic (`TR = 2.0 s`, `TE = 30 ms`, `168` volumes).
- **Released Derivatives (`ds000228`)**:
  - Raw BIDS (`sub-pixar001` to `sub-pixar155`), MNI-normalized preprocessed BOLD volumes + `aCompCor` / motion-artifact confound regressors (`derivatives/`), and explicit behavioral `participants.tsv` (`Age`, `AgeGroup`, `Child_Adult`, `ToM` composite score, `IQ`).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Protocols**:
  1. **Developmental Brain-Age / ToM Prediction**: `5`-fold stratified CV across the `155` subjects predicting chronological age or behavioral `ToM` score from `ToM × Pain` functional connectivity / ISFC matrices while partialling out `mean FD`.
  2. **Reverse-Correlation Event Discovery**: Identify TR peaks in adult `rTPJ` vs. `dACC/aINS` (`N = 33`) and evaluate developmental trajectory of inter-region anti-correlation and child-to-adult ISC (`N = 122`).
- **Critical Modeling Pitfalls**:
  1. **Motion Confound Control Is Non-Negotiable**: Head motion (`FD`) drops steeply from age `3` to adulthood; any age-classification or connectivity study that omits `CompCor` + spike scrubbing + `FD`-matched sensitivity checks risks measuring pediatric head motion rather than neural maturation!
  2. **Pre-Movie Offset (`10 s` Black + `10 s` Logos)**: Verify `events.tsv` zero-time convention (`scan trigger t = 0` vs. `movie start t = 10 s`) before convolving canonical HRFs.

## 4. Programmatic Download & Quickstart
```bash
# Option A: Full 155-subject BIDS & derivatives via DataLad / OpenNeuro
datalad install https://github.com/OpenNeuroDatasets/ds000228.git

# Option B: Direct Nilearn Python fetcher (preprocessed MNI + confounds + phenotypic table)
python -c "from nilearn.datasets import fetch_development_fmri; data = fetch_development_fmri()"
```

## 5. Verified Primary References
- **`richardson2018partlycloudy`**: Richardson, H., Lisandrelli, G., Riobueno-Naylor, A., & Saxe, R. (2018). *Development of the social brain from age three to twelve years*. Nature Communications (`10.1038/s41467-018-03399-2`).
