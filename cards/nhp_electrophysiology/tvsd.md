# THINGS Ventral-Stream Spiking Dataset (`TVSD` / Papale et al. *Neuron* 2025)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Unlocks **simultaneous millisecond-resolved population activity across V1, V4, and IT** (`1,024` channels = `16 × 64-channel` chronic Utah arrays per macaque, `Monkey F` and `Monkey N`) over **tens of thousands of natural images** (`Papale, Wang, Self & Roelfsema, Neuron, 2025`). Because TVSD uses the exact **THINGS** image set (`22,248` training images across `1,854` concepts + `100` `30`-repeat test images), it enables **1-to-1 stimulus-matched macaque ↔ human (`THINGS-fMRI`, `THINGS-MEG`, `THINGS-EEG2`)** mechanistic comparisons.
- **Stimulus Timing**: Rapid fixation sequences (`100 ms` image presentation + `100 ms` inter-stimulus blank, typically `4` images per fixation trial) with receptive-field mapping runs providing exact electrode `RF` centers.

## 2. Recording Specifications & Preprocessing
- **Signals Released on G-Node GIN (`10.12751/g-node.hc7zlv`)**:
  - `1,000 Hz` **Envelope Multi-Unit Activity (`MUAe`)** (bandpass `500–5,000 Hz`, full-wave rectified, low-pass filtered at `200 Hz`, downsampled to `1 kHz`, session-normalized) and raw `30 kHz` broadband / spike-sorted units + electrode receptive field maps (`V1`, `V4`, `IT`).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Fit encoders/communication subspaces on the `22,248` training images (splitting internal validation folds **by THINGS concept** to prevent category leakage); evaluate time-resolved (`1 ms` or `10 ms` bins) explainable variance on the `100` `30`-repeat test images.
- **Critical Modeling Pitfalls**:
  1. **Inter-Stimulus Overlap Beyond `200 ms`**: With `200 ms` SOA (`100 ms` ON + `100 ms` OFF), neural dynamics beyond `+200 ms` (plus `~40 ms` retinal-cortical latency $\implies \sim 240\text{ ms}$) reflect overlap with subsequent stimuli in the sequence—crucial when studying sustained intermediate representations or `IT → V4 → V1` recurrent feedback!
  2. **Localized V1/V4 Receptive Fields**: Unlike global IT pooling, V1/V4 sites respond only to contrast/features inside small sub-patches (`<1–3°`) of the image—spatial readout factorizations (or cropping around mapped `RF` centers) dramatically outperform global average-pooled vision features.
  3. **Filter Low-SNR Chronic Sites**: Subset channels by test-set split-half reliability / `SNR` threshold (provided in the GIN metadata tables) as chronic array impedance varies across sites.

## 4. Programmatic Download & Quickstart
```bash
# Install TVSD repository via DataLad from G-Node GIN (fetches lightweight git tree; `datalad get` pulls MAT/HDF5)
datalad install https://gin.g-node.org/paolo_papale/TVSD.git
```

## 5. Verified Primary References
- **`papale2025tvsd`**: Papale, P., Wang, F., Self, M. W., & Roelfsema, P. R. (2025). *An extensive dataset of spiking activity to reveal the syntax of the ventral stream*. Neuron (`10.1016/j.neuron.2024.12.003`).
