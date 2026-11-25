# Cadena-Tolias-Ecker Macaque V1 Natural Image & ConvNet Metamer Dataset (`Cadena-V1` / *PLOS Comp Biol* 2019)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Provided the definitive awake-macaque V1 system-identification benchmark demonstrating that intermediate layers (`conv3_1`) of task-trained deep convolutional networks—and compact 3-layer data-driven CNNs with factorized spatial-feature readouts—substantially outperform classical Gabor wavelet filter banks and V1 simple/complex energy models (`Cadena, Denfield, Walker, Gatys, Tolias, Bethge & Ecker, PLOS Computational Biology, 2019`).
- **Stimulus Design (`7,250` Images across `5` Statistical Families)**:
  - `1,450` cropped grayscale natural photographs from **ImageNet**, paired `1:4` with `5,800` **Gatys Gram-matrix texture/feature syntheses** matched to VGG-19 layer statistics at `conv1_1`, `conv2_1`, `conv3_1`, and `conv4_1` (`1,450 × 5 = 7,250` unique stimuli, `140 × 140 px` covering `~2°–3°` centered on the population receptive field).
  - Rapid serial visual presentation (`60 ms` per image, zero blank ISI, `~35` images per `2.1 s` passive fixation trial) in two awake rhesus macaques maintaining tight gaze (`<0.5°` radius).

## 2. Recording Specifications & Preprocessing
- **Electrophysiology**: `32`-channel linear laminar silicon probes inserted acutely across `17` recording sessions into opercular macaque `V1` (`1°–3°` parafoveal eccentricity), yielding `166` spike-sorted, visually responsive units passing explainable-variance quality control (`FEV > 15%`).
- **Released Artifacts (`GIN:10.12751/g-node.2e31e3` & GitHub)**: Preprocessed stimulus tensors, spike counts integrated in the `[40, 100] ms` post-stimulus window, session/animal IDs, trial repetition indices (`2–4` repeats on train, `20–40` repeats on held-out test images), and reference TensorFlow/PyTorch factorized-readout baselines.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Explainable Variance Metric (`FEV`)**: Evaluates models via **Fraction of Explainable Variance Explained (`FEVe`)**, dividing raw $R^2$ (after subtracting per-stimulus trial-to-trial variance) by total explainable variance across high-repeat test stimuli (`~51%–55% FEVe` for VGG-19 `conv3_1` + sparse readout vs. `~30%–35%` for Gabor energy banks).
- **Critical Modeling Pitfalls**:
  1. **Seed-Family Leakage Between Natural & Synthesized Images**: Every ImageNet base image has four synthetic counterparts sharing low- and mid-level summary statistics (`conv1_1`–`conv4_1`). Random image-index splits leak exact local luminance/edge statistics across train and test; always split by the `1,450` **seed image families** (`1,160` train/val seeds = `5,800` images; `290` test seeds = `1,450` images).
  2. **Back-to-Back `60 ms` RSVP Overlap**: Because stimuli appear continuously every `60 ms` without blank intervals, spike counts after `+100 ms` contain onset transients from image $t+1$, while `[40, 100] ms` contains trailing off-responses from image $t-1$. Dynamic models extending beyond `60 ms` bins must explicitly condition on stimulus history.
  3. **Factorized Spatial × Feature Readout Regularization**: Standard dense linear ridge regression over full `(H × W × C)` VGG feature maps severely overfits on `5,800` training samples; factorizing readout weights into a smooth/sparse 2D `(H × W)` spatial mask and a `1D (C)` feature vector is essential for fair architectural comparisons.

## 4. Programmatic Download & Quickstart
```bash
# Clone modeling code and fetch the GIN dataset archive (DOI: 10.12751/g-node.2e31e3)
git clone https://github.com/sacadena/Cadena2019PlosCB.git
datalad install https://gin.g-node.org/ecker-lab/Cadena2019PlosCB.git || \
  echo "Download archive directly from https://doi.org/10.12751/g-node.2e31e3"
```

## 5. Verified Primary References
- **`cadena2019v1`**: Cadena, S. A., Denfield, G. H., Walker, E. Y., Gatys, L. A., Tolias, A. S., Bethge, M., & Ecker, A. S. (2019). *Deep convolutional models improve predictions of macaque V1 responses to natural images*. PLOS Computational Biology (`10.1371/journal.pcbi.1006897`).
