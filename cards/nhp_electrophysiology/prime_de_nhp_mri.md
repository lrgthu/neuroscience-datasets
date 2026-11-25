# PRIMatE Data Exchange (`PRIME-DE` / Milham et al. *Neuron* 2018, 2020)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Did for non-human primate neuroimaging what the Human Connectome Project (`HCP`) and `1000 Functional Connectomes` did for human MRI: broke decades of small-sample (`n = 2–4`) laboratory silos by uniting **>25 international primate research centers** (`22` sites and `217` primates in the foundational 2018 release, expanded longitudinally to **>250 macaques**) into a **BIDS-standardized, openly downloadable AWS S3 repository** (`Milham et al., Neuron, 2018; PRIME-DE Consortium, Neuron, 2020`).
- **Translational Bridge Between Invasive NHP Electrophysiology & Human Whole-Brain fMRI**:
  - Combines structural (`T1w`, `T2w`), high-angular-resolution **diffusion MRI (`dMRI`)** (comparable directly against gold-standard macaque axonal tract-tracing atlases like `CoCoMac` / Kennedy `Markov` retrograde injections), **resting-state fMRI**, and **awake naturalistic movie-viewing fMRI** (`Rockefeller`, `NKI`, `NIMH`, `Oxford` cohorts).

## 2. Recording Specifications & Preprocessing
- **Field Strengths & Coils**: Spans clinical/research **`3T`**, **`4.7T`**, **`7T`**, and ultra-high-field **`9.4T`** horizontal/vertical bore scanners using custom multi-channel NHP phased-array head coils and implanted headposts (`0.75–1.5 mm` functional EPI; `0.3–0.5 mm` structural).
- **Companion Ecosystem (`PRIME-RE`)**: Paired with the **PRIMatE Resource Exchange (`PRIME-RE`)** providing standard macaque templates (**`NMT v2`**, **`Yerkes19`** `32k_fs_LR` cortical surfaces homologous to HCP human `fs_LR`), deep-learning NHP skull-stripping (`U-Net`), and `PCP-QAP` quality control reports.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Cross-Species & Foundation-Model Benchmarks**: Standard corpus for **human ↔ macaque functional alignment** (`Xu et al. PNAS 2020` joint embedding / cortical expansion maps), principal functional gradient evolution (`Margulies`), and cross-site NHP fMRI foundation pretraining using **Leave-One-Site-Out (`LOSO`)** validation.
- **Critical Modeling Pitfalls**:
  1. **Contrast Agent Sign Flip (`MION` vs. `BOLD`)**: Several awake `3T` sites injected iron-oxide `MION` contrast agent to boost contrast-to-noise ratio `3–5×`; because `MION` reflects cerebral blood volume (`CBV`) via $T_2^*$ dephasing, neural activation produces a **negative** raw EPI signal deflection (`-ΔS`) with a slower decay tail (`τ ~ 15–20 s`)—always invert `MION` time series (`× -1`) and check `task-*_bold.json` / site tables before computing directional lag or GLM betas!
  2. **Isoflurane Dose Suppresses Long-Range Frontoparietal Connectivity**: Deep isoflurane (`>1.2–1.5%`) nonlinearly attenuates thalamocortical and default-mode coherence; stratify or explicitly control for **anesthesia regimen (`awake`, `light medetomidine-ketamine`, `isoflurane %`)** using the consortium metadata tables.
  3. **Use Dedicated NHP Surface/Volume Registration (`NMT v2` / `Yerkes19`)**: Never run unmodified human `MNI152` priors; project cortical signals onto `Yerkes19` `32k` surfaces when aligning macaque `PRIME-DE` gradients with human `HCP` `CIFTI` surfaces.

## 4. Programmatic Download & Quickstart
```bash
# Anonymous direct download of BIDS-formatted site collections from AWS Open Data (fcp-indi)
aws s3 ls --no-sign-request s3://fcp-indi/data/Projects/PRIME-DE/
# Example: sync a single open BIDS site collection
aws s3 sync --no-sign-request s3://fcp-indi/data/Projects/PRIME-DE/site-oxford/ ./prime_de_oxford/
```

## 5. Verified Primary References
- **`milham2018primede`**: Milham, M. P., Ai, L., Koo, B., Xu, T., Amiez, C., Balezeau, F., et al. (2018). *An open resource for non-human primate imaging*. Neuron (`10.1016/j.neuron.2018.08.039`).
- **`milham2020primede`**: Milham, M. P., Petkov, C. I., Margulies, D. S., Schroeder, C. E., Basso, M. A., Belin, P., et al. (2020). *Accelerating the evolution of nonhuman primate neuroimaging*. Neuron (`10.1016/j.neuron.2019.12.023`).
