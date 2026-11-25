# THINGS-data (`THINGS-fMRI`, `THINGS-MEG`, `THINGS-EEG2`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Systematically samples object representations across `1,854` concrete, nameable object concepts (`Hebart et al., eLife, 2023`; `Gifford et al., NeuroImage, 2022`). Uniquely bridges **spatial resolution** (`3T fMRI`), **millisecond dynamics** (`MEG` & `EEG2`), **human perceptual similarity** (`4.7 million` odd-one-out triplet behavioral choices, `SPoSE` dimensions), and **macaque electrophysiology** (`TVSD`).
- **Sub-Dataset Breakdown**:
  - **THINGS-fMRI (`OpenNeuro:ds004192`)**: `N = 3` subjects, `12` sessions each, `8,740` unique images (`720` concepts × `12` exemplars + `100` validation images × `12` repeats), `500 ms` stimulus + `4.0 s` SOA (`odd-ball` catch detection on artificial images).
  - **THINGS-MEG (`OpenNeuro:ds004212`)**: `N = 4` subjects, `12` sessions each, `22,448` unique images (`1,854` concepts × `12` exemplars + `200` test images × `12` repeats), `500 ms` stimulus, `1.5 ± 0.2 s` SOA.
  - **THINGS-EEG2 (`OSF:3jk45`)**: `N = 10` subjects, `4` sessions each, `16,540` training images (`1,654` concepts × `10` images × `4` repeats) + `200` zero-shot test images (`200` disjoint concepts × `1` image × `80` repeats) in `100 ms` (`10 Hz`) RSVP streams (`82,160` trials/subject).

## 2. Recording Specifications & Preprocessing
- **Acquisition & Derivatives**:
  - **fMRI**: `3T` Siemens Prisma (`2 mm` isotropic, multiband `TR = 1.5 s`), fMRIPrep + **ICA-AROMA** + **GLMsingle** single-trial beta weights released directly on OpenNeuro/Figshare.
  - **MEG**: `275`-channel whole-head CTF axial gradiometer (`1,200 Hz`) with simultaneous eye-tracking.
  - **EEG2**: `64`-channel BrainVision actiCHamp (`1,000 Hz`, downsampled `100 Hz` / `250 Hz` epoched numpy arrays available on OSF).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Train strictly on single-trial / 4-repeat training concepts; evaluate zero-shot encoding/decoding/retrieval on the `100` (fMRI) or `200` (MEG/EEG2) multi-repeat test images drawn from **disjoint concepts**.
- **Repeat Structure & Noise Ceiling**: `12` repeats (fMRI/MEG) and `80` repeats (EEG2) on test stimuli provide high-SNR target embeddings for top-1/top-5 CLIP retrieval and split-half noise ceilings.
- **Critical Modeling Pitfalls**:
  1. **Concept Disjointness**: During hyperparameter tuning, split training validation folds **by concept (`1,654` / `720` concepts)** rather than randomly splitting exemplars, otherwise category-level visual templates leak across folds.
  2. **RSVP Overlap in EEG2**: At `10 Hz` presentation (`100 ms` onset-to-onset), time windows `[0, 600 ms]` contain responses to $5$ consecutive images; random sequence order averages out neighbors on the `80`-repeat test set, but single-trial training benefits from temporal ridge deconvolution.

## 4. Programmatic Download & Quickstart
```bash
# Install THINGS-fMRI and THINGS-MEG via DataLad (fetches metadata immediately; `datalad get` pulls arrays)
datalad install https://github.com/OpenNeuroDatasets/ds004192.git
datalad install https://github.com/OpenNeuroDatasets/ds004212.git

# Download preprocessed THINGS-EEG2 arrays from OSF
uvx osfclient -p 3jk45 clone ./things_eeg2
```

## 5. Verified Primary References
- **`hebart2023things`**: Hebart, M. N., Contier, O., Teichmann, L., et al. (2023). *THINGS-data, a multimodal collection of large-scale datasets for investigating object representations in human brain and behavior*. eLife (`10.7554/eLife.82580`).
- **`gifford2022thingseeg`**: Gifford, A. T., Dwivedi, K., Roig, G., & Cichy, R. M. (2022). *A large and rich EEG dataset for modeling human visual object recognition*. NeuroImage (`10.1016/j.neuroimage.2022.119754`).
