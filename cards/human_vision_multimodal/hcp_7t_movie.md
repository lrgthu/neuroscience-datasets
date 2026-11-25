# HCP 7T Movie-Watching & Retinotopy (`HCP-7T-Movie` · `N = 184`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Uniquely combines **large-cohort `7T` breadth (`N = 184` subjects)**, **sub-second `1.0 s` TR temporal resolution at `1.6 mm` isotropic**, **gold-standard `pRF` retinotopy (`N = 181`, `Benson et al., Journal of Vision, 2018`)**, **twin genetics**, and **paired `3T` HCP-YA task/connectome data** in the exact same participants!
- **7T Functional Battery (`4` scan sessions/subject)**:
  - **`tfMRI_MOVIE1..4` (`~60 min`)**: `4–5` short film clips (`1–4 min` each) interleaved with `20 s` rest periods per run (`MOVIE1` & `MOVIE3`: Creative Commons short films; `MOVIE2` & `MOVIE4`: Hollywood excerpts including *Inception*, *Social Network*, *Ocean's Eleven*, *Home Alone*, *Star Wars*). Every run concludes with the **exact same `83 s` validation clip**!
  - **`tfMRI_RET*` (`30 min`, `6` runs)**: Rotating wedges, expanding/contracting rings, and drifting bars (`pRF` eccentricity, polar angle, and size maps publicly available on OSF `bw9ec` with zero DUA!).
  - **`rfMRI_REST1..4` (`60 min`)**: `4 × 15 min` `7T` resting-state runs + simultaneous `1,000 Hz` EyeLink gaze/pupil tracking across all runs.

## 2. Recording Specifications & Preprocessing
- **Canonical Files**: `1.6 mm` `59k` and `2.0 mm` `32k` (`91,282` grayordinate) `MSMAll` + `ICA-FIX` cleaned CIFTI `.dtseries.nii` files (`hp2000_clean`).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Critical Modeling Pitfalls**:
  1. **Strip the Repeated `83 s` Validation Clip Before Cross-Run Training**: Every single movie run (`MOVIE1..4`) ends with the identical `83 s` validation montage! If you train on `MOVIE1..3` and test on `MOVIE4` without masking out that final segment, test metrics are severely inflated by 3× training memorization.
  2. **Group Subject Splits by `Family_ID`**: Cortical folding, functional topography, and movie ISC are heritable across MZ/DZ twins.
  3. **Use `MSMAll` Surface Registration**: Cross-subject alignment gains massive SNR from areal-feature `MSMAll` registration compared to anatomical `MSMSulc` or volumetric `FNIRT`.

## 4. Programmatic Download & Quickstart
```bash
# Public HCP 7T Retinotopy pRF maps require zero registration on OSF:
uvx osfclient -p bw9ec list
# Full 7T MOVIE1-4 CIFTI time-series via s3://hcp-openaccess (after free ConnectomeDB click-through)
```

## 5. Verified Primary References
- **`benson2018hcpretinotopy`**: Benson, N. C., Jamison, K. W., Arcaro, M. J., et al. (2018). *The Human Connectome Project 7 Tesla retinotopy dataset: Description and population receptive field analysis*. Journal of Vision (`10.1167/18.13.23`).
- **`vanessen2013hcp`**: Van Essen, D. C., Smith, S. M., Barch, D. M., et al. (2013). *The WU-Minn Human Connectome Project: An overview*. NeuroImage (`10.1016/j.neuroimage.2013.05.041`).
