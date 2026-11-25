# Human Connectome Project Lifespan (`HCP-Development` & `HCP-Aging` · Release 2.0)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Extends the surface-based grayordinate architecture (`CIFTI 91,282` + `MSMAll` + `ICA-FIX`) of `HCP-YA` across the human lifespan on commercial `3T` Siemens Prisma scanners (`Harms et al., NeuroImage, 2018`; `Somerville et al., NeuroImage, 2018`; `Bookheimer et al., NeuroImage, 2019`). Release 2.0 on the NIMH Data Archive (`NDA`) delivers preprocessed structural, resting-state, task fMRI, diffusion, and arterial spin labeling (`ASL`) packages for **`1,377` cross-sectional Visit 1 participants**:
  - **`HCP-Development` (`HCP-D`, `NDA:2846`, `N = 652`, ages `5–21`)**: Tracks cortical myelination, executive control maturation, pubertal hormone trajectories, and network segregation across childhood and adolescence (including a longitudinal follow-up sub-cohort).
  - **`HCP-Aging` (`HCP-A`, `NDA:2847`, `N = 725`, ages `36–100+`)**: Samples typical, non-demented adult aging through centenarians alongside vascular health, menopause/endocrine status, `0.4 × 0.4 × 2.0 mm` high-resolution hippocampal turbo spin-echo (`TSE`), and whole-brain `pCASL` cerebral perfusion.
- **Task fMRI Batteries**:
  - **`HCP-D`**: Conditioned Approach Response Inhibition Task (`CARIT` Go/No-Go), `Emotion` (`Hariri` face/shape matching), and `Guessing` (monetary reward/loss conditioning).
  - **`HCP-A`**: `CARIT` Go/No-Go, `FACENAME` (episodic face-name encoding/recall), and `VISMOTOR` (visual-motor checkerboard/button calibration for neurovascular reactivity).

## 2. Recording Specifications & Preprocessing
- **Harmonized 4-Site `3T` Siemens Prisma Protocol (`80 mT/m` gradients, `32`-ch head coil)**:
  - **Structural**: `0.8 mm` isotropic `T1w` multi-echo `MPRAGE` (with prospective volumetric navigator `vNav` motion re-acquisition!) and `0.8 mm` `T2w` `SPACE` (`T1w/T2w` intracortical myelin maps).
  - **Functional (`rfMRI` & `tfMRI`)**: `2.0 mm` isotropic `2D` multiband `8` gradient-echo EPI (`TR = 0.80 s`, `TE = 37 ms`, `FA = 52°`), acquired in matched **`AP` (`Anterior-to-Posterior`)** and **`PA` (`Posterior-to-Anterior`)** phase-encoding pairs (`4 × 6.5 min = 26 min` rest for ages `8–100+`; `6 × 3.5 min = 21 min` rest for ages `5–7`).
  - **Diffusion (`dMRI`)**: `1.5 mm` isotropic multiband `4` (`b = 1500` and `3000 s/mm²`, `185` directions across `AP/PA` pairs).
  - **Perfusion (`ASL`)**: Pseudo-continuous `2.5 mm` multi-delay `pCASL` quantifying cerebral blood flow (`CBF`) and arterial transit time (`ATT`).
- **HCP Lifespan Pipelines**: Surface reconstruction, `MSMAll` areal-feature alignment into `32k_fs_LR` grayordinate space (`91,282` cortical vertices + subcortical voxels), spatial `ICA-FIX` denoising, and parcellated `Glasser 360 MMP1.0` `.ptseries.nii` connectomes.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Protocol**: Stratified `10`-fold cross-validation grouped by acquisition site (`Harvard`, `MGH`, `UCLA`, `UMinn`/`WashU`) and family/subject ID (preventing sibling or Visit 1/Visit 2 leakage), evaluating NIH Toolbox fluid/crystallized cognition, `brain-age` gap, or foundation-model linear probing.
- **Critical Modeling Pitfalls**:
  1. **Never Splice `HCP-YA` (`ages 22–35`) Directly Between `HCP-D` (`5–21`) and `HCP-A` (`36–100+`) Without Harmonization**: `HCP-YA` used a custom `Connectome Skyra` with `LR/RL` phase encoding (`TR = 0.72 s`, `60 min` rest), whereas `HCP-D`/`HCP-A` used `Prisma` `AP/PA` phase encoding (`TR = 0.80 s`, `26 min` rest). Unharmonized `5–100` concatenations produce a spurious jump across ages `22–35`!
  2. **Vascular & Motion Confounding at Lifespan Extremes**: Both `5–8` year-olds and `80+` year-olds exhibit elevated `FD` (mitigated partially in T1w/T2w by `vNav`, but residual in EPI), and older adults show steep neurovascular coupling attenuation—incorporate `pCASL` `CBF`/`ATT` covariates in `HCP-A` before attributing BOLD variance changes to synaptic activity.
  3. **Balanced `AP + PA` Pairing**: Just as `LR/RL` must be balanced in `HCP-YA`, `AP` and `PA` runs compress vs. stretch orbitofrontal and occipital poles differently—always balance `AP` and `PA` runs per participant.

## 4. Programmatic Download & Quickstart
```bash
# Requires institutional NIMH Data Archive (NDA) Data Use Certification for Collections 2846 (HCP-D) & 2847 (HCP-A)
uvx --from nda-tools downloadcmd -dp <PACKAGE_ID> -u <NDA_USERNAME> -d ./hcp_lifespan_2.0
```

## 5. Verified Primary References
- **`harms2018hcplifespan`**: Harms, M. P., Somerville, L. H., Ances, B. M., et al. (2018). *Extending the Human Connectome Project across ages: Imaging protocols for the Lifespan Development and Aging projects*. NeuroImage (`10.1016/j.neuroimage.2018.09.060`).
- **`bookheimer2019hcpaging`**: Bookheimer, S. Y., Salat, D. H., Terpstra, M., et al. (2019). *The Lifespan Human Connectome Project in Aging: An overview*. NeuroImage (`10.1016/j.neuroimage.2018.10.009`).
- **`somerville2018hcpdev`**: Somerville, L. H., Bookheimer, S. Y., Buckner, R. L., et al. (2018). *The Lifespan Human Connectome Project in Development: A large-scale study of brain connectivity development in 5–21 year olds*. NeuroImage (`10.1016/j.neuroimage.2018.08.050`).
