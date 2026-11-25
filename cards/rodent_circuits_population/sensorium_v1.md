# SENSORIUM & Dynamic SENSORIUM Mouse V1 Benchmarks (`2022` & `2023`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: The standard machine-learning benchmark suite for **neural system identification ("digital twins") of mouse primary visual cortex (`V1`)** (`Willeke et al., NeurIPS, 2022`; `Turishcheva et al., NeurIPS, 2023/2024`), directly catalyzing modern shared-core + Gaussian-readout CNNs, 3D Factorized/Ensembled Video ResNets, and multimodal visual foundation models (`MICrONS` `Wang et al., Nature, 2025`).
- **Two Progressive Releases on G-Node (`GIN`)**:
  1. **`SENSORIUM 2022` (`cajal/Sensorium2022`, `arXiv:2206.08666`)**: `7` mice (`28,068` total `L2/3` excitatory `V1` neurons, `~3,500–4,500` neurons/mouse) viewing `~5,000` unique ImageNet grayscale natural scenes (`500 ms` presentation) plus `100` Oracle test images (`× 10` repeats), split into **`SENSORIUM`** (stimulus-only `2` mice) and **`SENSORIUM+`** (`5` mice with synchronized `pupil_size`, `pupil_dilation_rate`, `2D` `pupil_center`, and `treadmill_speed`).
  2. **`Dynamic SENSORIUM 2023` (`pollytur/Sensorium2023Data`, `arXiv:2305.19654` / `10.52202/079017-3777`)**: `10` mice (`78,853` total `V1` neurons across `L2–L5`, `~2 hours` dynamic video per mouse: `5` original competition mice + `5` bonus mice) viewing `360 × 640` `30 Hz` cinematic natural movies alongside **two official tracks**: **In-Domain (`ID`)** natural movie prediction and **Out-of-Distribution (`OOD`)** generalization to unseen parametric videos (`drifting gratings`, `Gaussian dot kinematograms`, `pink noise`, `Monet`, and `Trippy`).

## 2. Recording Specifications & Preprocessing
- **Acquisition & File Layout**: Multi-plane 2-photon calcium imaging (`~8 Hz` volumetric scan rate across cortical depths `150–450 µm` in `Slc17a7-Cre;Ai162` / `GCaMP6s` mice) processed via `CAIMAN`/`Suite2p` spike deconvolution. Each trial is stored as clean `.npy` arrays organized under `data/{images_or_videos, responses, behavior, pupil_center, meta/neurons, meta/trials}/`, including 3D cortical `(x, y, z)` soma coordinates for every neuron.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Official `tiers` metadata array (`'train'`, `'validation'`, `'test'`, `'final_test'`) locking single-repeat training clips/images separately from `10`-repeat `Oracle` evaluation sets and OOD synthetic stimulus tiers.
- **Critical Modeling Pitfalls**:
  1. **Model Gaze Shifts (`Shifter`) & Behavioral State Explicitly**: Awake mice move their eyes during natural viewing; winning architectures (`Factorized 3D ConvNeXt / Gru / Ensembled Recurrent Cores`, `Turishcheva et al. 2024`) feed `(pupil_x, pupil_y)` into a small coordinate-shift MLP that dynamically translates each neuron's spatial Gaussian readout grid at every frame, while concatenating locomotion and pupil dilation as feature channels.
  2. **Use Poisson Loss Over MSE**: Deconvolved calcium responses are strictly non-negative and heavy-tailed; training with Poisson negative log-likelihood markedly outperforms Gaussian MSE on both `Single-Trial Correlation` and `Correlation-to-Average`.
  3. **Respect Temporal Padding / Warm-Up Frames in Video (`2023`)**: Dynamic V1 neurons exhibit `300–1,000 ms` adaptation and recurrent history dependence—mask out the initial `~15–30` frames (`0.5–1.0 s`) of each movie clip from loss/metric evaluation just as the official `sensorium_2023` evaluator does.

## 4. Programmatic Download & Quickstart
```bash
# Clone official baseline & dataloader repo and pull a mouse archive from G-Node GIN
git clone https://github.com/ecker-lab/sensorium_2023.git
# Direct HTTPS zip archives for each mouse are hosted openly on GIN:
#   2022 Static Images:  https://gin.g-node.org/cajal/Sensorium2022
#   2023 Dynamic Videos: https://gin.g-node.org/pollytur/Sensorium2023Data
curl -sI https://gin.g-node.org/pollytur/Sensorium2023Data | head -n 5
```

## 5. Verified Primary References
- **`willeke2022sensorium`**: Willeke, K. F., Fahey, P. G., Bashiri, M., et al. (2022). *The Sensorium competition on predicting large-scale mouse primary visual cortex activity*. NeurIPS Datasets and Benchmarks (`arXiv:2206.08666`).
- **`turishcheva2023dynamicsensorium`**: Turishcheva, P., Fahey, P. G., Hansel, L., et al. (2023). *The Dynamic Sensorium competition for predicting large-scale mouse visual cortex activity from videos*. arXiv (`arXiv:2305.19654`).
- **`turishcheva2024retrospective`**: Turishcheva, P., Fahey, P. G., Vystrčilová, M., et al. (2024). *Retrospective for the Dynamic Sensorium Competition for predicting large-scale mouse primary visual cortex activity from videos*. Advances in Neural Information Processing Systems (`10.52202/079017-3777`, `arXiv:2407.09100`).
