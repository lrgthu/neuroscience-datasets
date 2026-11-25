# Algonauts Project 2019 Paired fMRI & MEG Object Recognition (`Algonauts-2019`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Unifies the landmark MIT `92-image` (`Cichy et al., Nature Neuroscience, 2014`) and `118-image` (`Cichy et al., Cerebral Cortex, 2016`) paired human `3T fMRI` + `306-channel MEG` datasets with a `78-image` held-out benchmark (`Cichy et al., CCN / arXiv:1905.05675, 2019`). Enables joint evaluation of cortical hierarchy (`EVC → IT`) and millisecond temporal cascade (`early → late` visual processing) via Representational Similarity Analysis (`RSA`) and `MEG–fMRI` fusion.
- **Stimulus Design & Timing**: `288` static color object photographs presented for `500 ms` centrally (`~2.9°–4.0°` visual angle) with orthogonal detection catch trials:
  - **Training Set 1 (`92` images)**: Segmented everyday objects on a uniform gray background spanning animate (human/non-human faces & bodies) and inanimate (natural & artificial) hierarchies (`Cichy et al., 2014`).
  - **Training Set 2 (`118` images)**: Distinct real-world object categories embedded in naturalistic scene backgrounds (`Cichy et al., 2016`).
  - **Challenge Test Set (`78` images)**: Held-out objects photographed on natural backgrounds matching the ecological statistics of Set 2.
- **Subject Cohort**: `N = 15` healthy adult participants per stimulus set and modality (with substantial subject overlap between MEG and fMRI cohorts in Sets 1 & 2).

## 2. Recording Specifications & Preprocessing
- **fMRI (`Track 1`)**: `3T` Siemens Trio (`2.0 mm` isotropic EPI, `TR = 2.0 s`), GLM $t$-statistic activation patterns extracted within **Early Visual Cortex (`EVC`)** and **Inferior Temporal Cortex (`IT`)**, summarized as subject-specific `[N_img × N_img]` Representational Dissimilarity Matrices (`RDMs`).
- **MEG (`Track 2`)**: `306-channel` Elekta Neuromag Triux (`1,000 Hz`, `20–30` repeats/stimulus), summarized as pairwise decoding/distance RDMs in **Early** (`~60–100 ms`) and **Late** (`~140–190 ms`) post-onset windows.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Metric**: Noise-ceiling-normalized squared Spearman rank correlation ($R^2 / \text{NC}$) between upper-triangular model RDMs and human subject RDMs in `EVC`, `IT`, `MEG-Early`, and `MEG-Late`.
- **Noise Ceiling**: Lower bound = mean squared Spearman correlation of each left-out subject's RDM with the `N - 1` group-average RDM; upper bound = correlation of each subject's RDM with the full `N`-subject grand-average RDM (`Nili et al., 2014`).
- **Critical Modeling Pitfalls**:
  1. **Silhouette vs. Natural Background Shift**: Set 1 (`92` images) lacks background texture, whereas Set 2 (`118`) and the `78`-image Test Set include natural scene backgrounds—early CNN/ViT layers calibrated solely on Set 1 underpredict background-driven `EVC` variance on Set 2/Test.
  2. **Image-Level Split Discipline**: When cross-validating feature-reweighted RSA, partition **by stimulus indices** ($K$-fold over images, keeping only `[idx_val × idx_val]` sub-blocks for validation), never by random RDM pairs!

## 4. Programmatic Download & Quickstart
```bash
# Download official Algonauts 2019 training/test stimulus sets, RDMs, and Python devkit
git clone https://github.com/Neural-Dynamics-of-Visual-Cognition-FUB/Algonauts2019_devkit.git
curl -L -O http://algonauts.csail.mit.edu/2019/data/Training_Data_92_Image_Set.zip
curl -L -O http://algonauts.csail.mit.edu/2019/data/Training_Data_118_Image_Set.zip
```

## 5. Verified Primary References
- **`cichy2014megfmri`**: Cichy, R. M., Pantazis, D., & Oliva, A. (2014). *Resolving human object recognition in space and time*. Nature Neuroscience (`10.1038/nn.3635`).
- **`cichy2019algonauts`**: Cichy, R. M., Roig, G., Andonian, A., et al. (2019). *The Algonauts Project: A Platform for Communication between the Sciences of Biological and Artificial Intelligence*. CCN / `arXiv:1905.05675` (`10.32470/ccn.2019.1018-0`).
- **`cichy2016fusion`**: Cichy, R. M., Pantazis, D., & Oliva, A. (2016). *Similarity-based fusion of MEG and fMRI reveals spatio-temporal dynamics in human cortex during visual object recognition*. Cerebral Cortex (`10.1093/cercor/bhw135`).
