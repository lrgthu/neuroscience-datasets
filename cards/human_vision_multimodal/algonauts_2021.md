# Algonauts Project 2021 Dynamic Video fMRI (`Algonauts-2021`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Established the canonical short-event naturalistic video encoding benchmark (`Cichy et al., arXiv:2104.13714, 2021`), testing how computational video models explain whole-brain human `3T` BOLD responses across ventral (`V1–V4`, `LOC`, `FFA`, `PPA`), dorsal, and lateral (`EBA`, `STS`) visual streams during everyday dynamic events.
- **Stimulus Design & Timing**: `1,102` square-cropped (`268 × 268 px`, `~15°` visual angle), **muted** `3.0 s` video clips sampled from the **Moments in Time** / **Multi-Moments in Time** action datasets (`4.0 s`–`6.0 s` jittered event-related SOA across `4` functional sessions after `1` localizer/structural session):
  - **Training Set**: `1,000` unique `3 s` clips × `3` repetitions = `3,000` trials/subject.
  - **Test Set**: `102` held-out `3 s` clips × `10` repetitions = `1,020` trials/subject.
- **Subject Cohort**: `10` neurologically healthy adults (`sub-01` to `sub-10`) freely viewing the clips while performing occasional catch-trial action-category detection.

## 2. Recording Specifications & Preprocessing
- **Acquisition Hardware & Resolution**: `3T` Siemens Magnetom Prisma (MIT McGovern Institute), `64`-channel head coil, multiband factor `2` gradient-echo EPI at `2.5 mm` isotropic (`TR = 1.75 s`, `TE = 30 ms`).
- **Two Official Challenge Tracks**:
  - **Mini Track (`9` Functional/Retinotopic ROIs)**: `V1`, `V2`, `V3`, `V4` (retinotopic mapping) and `LOC`, `FFA`, `PPA`, `EBA`, `STS` (dynamic category localizers).
  - **Full Track (Whole-Brain Reliable Voxels)**: All cortical and subcortical voxels passing within-subject split-half repeat reliability screening.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Fit regularized ridge / partial-least-squares readouts on the `1,000`-video training set (`5`-fold or `10`-fold video CV for $\alpha$) and evaluate noise-ceiling-normalized Pearson correlation ($r / \text{NC}$) on the `102` `10`-repeat test clips.
- **Critical Modeling Pitfalls**:
  1. **Superseded Full Release (`BMD` / `ds005165`)**: The original 2021 challenge devkit withheld the `102`-video test BOLD responses for CodaLab leaderboard scoring; the full unblinded dataset (including raw BIDS NIfTIs, `fMRIPrep` surfaces, `GLMsingle` betas for **both** `1,000` train and `102` test clips, and rich semantic metadata) is now openly available on OpenNeuro as **`ds005165` (`bmd_moments`)**.
  2. **Muted Video Presentation**: Clips contain **no sound**; never supply original YouTube/Moments-in-Time audio waveforms to multimodal models, or spurious audio-visual correlations will distort `STS` interpretations.
  3. **Free-Viewing Regime**: Unlike `vim-2` or `NSD` (strict central fixation), subjects viewed the `3 s` videos naturally without fixation lock, engaging ecological gaze shifts toward salient actors and hands.

## 4. Programmatic Download & Quickstart
```bash
# Official Algonauts 2021 devkit & baseline feature-extraction pipeline
git clone https://github.com/Neural-Dynamics-of-Visual-Cognition-FUB/Algonauts2021_devkit.git

# Full unblinded raw BIDS + GLMsingle derivatives (1,000 train + 102 test) via OpenNeuro
datalad install https://github.com/OpenNeuroDatasets/ds005165.git
```

## 5. Verified Primary References
- **`cichy2021algonauts`**: Cichy, R. M., Dwivedi, K., Lahner, B., et al. (2021). *The Algonauts Project 2021 Challenge: How the Human Brain Makes Sense of a World in Motion*. `arXiv:2104.13714`.
- **`lahner2024bmd`**: Lahner, B., Dwivedi, K., Iamshchinina, P., et al. (2024). *Modeling short visual events through the BOLD moments video fMRI dataset and metadata*. Nature Communications (`10.1038/s41467-024-50310-3`).
