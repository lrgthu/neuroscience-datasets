# Stringer & Pachitariu Brain-Wide Spontaneous Behavior (`Stringer-Spont` · *Science* 2019)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Establishes that **"spontaneous" cortical and forebrain neural activity is neither unstructured noise nor low-dimensional arousal alone**, but encodes a **high-dimensional (`>100`D) behavioral state** driven by multidimensional orofacial and body movements (`Stringer, Pachitariu, Steinmetz, Reddy, Carandini & Harris, Science, 2019`), and proves that incoming visual stimuli add onto ongoing behavioral activity in **nearly orthogonal population subspaces** (save for `1–2` shared multiplicative gain/arousal dimensions).
- **Explicit Distinction from `stringer_mouse_v1` (*Nature* 2019)**:
  - **`stringer_mouse_v1` (`10.1038/s41586-019-1346-5`, Figshare `6845348`)**: `2,800` static natural images (`× 2` repeats) in V1 `2P` to measure the sensory `cvPCA` power law ($\alpha \approx 1.04$).
  - **`stringer_spontaneous_2019` (`10.1126/science.aav7893`, Figshare `6163622` + `7739750`)**: Prolonged (`1–2 h`) **spontaneous darkness / gray-screen** recordings paired with `500-D` infrared face-motion SVD (`Facemap`), including **(a) `8` simultaneous Neuropixels 1.0 probes** spanning visual, sensorimotor, frontal cortex, hippocampus, striatum, thalamus, and midbrain (`krebs`, `waksman`, `robbins`, `~2,200–3,000` simultaneous single units per mouse), **(b) `~10,000`-neuron `11`-plane `2P` V1 spontaneous sessions**, and **(c) interleaved `32`-image high-repeat visual + spontaneous sessions** testing sensory–behavioral subspace orthogonality.

## 2. Recording Specifications & Preprocessing
- **Two Complementary Modalities in `10.25378/janelia.6163622`**:
  1. **8-Probe Simultaneous Neuropixels (`ephys`)**: `30 kHz` Kilosort spike times across `8` chronically/acutely inserted probes (`~3,072` active recording sites simultaneously!), paired with `probeLocations.mat` (`10.25378/janelia.7739750`) mapping every electrode channel to 3D Allen `CCFv3` coordinates, `50 Hz` face-motion SVDs (`motionSVD`), running speed, and pupil area.
  2. **10,000-Neuron Volumetric 2-Photon (`2P`)**: `11`-plane `2.5–3.0 Hz` `GCaMP6s` recordings in `VISp` (`Suite2p` deconvolved activity), with spatial `3D` `(x, y, z)` coordinates enabling axial/lateral checkerboard splits that avoid shared neuropil fluorescence bleed-through during peer prediction.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Contiguous multi-minute temporal block cross-validation (`10`–`20` blocks with `5–10 s` guard bands) for reduced-rank regression (`RRR`) from `500-D` `motionSVD` to neural populations; spatial checkerboard holdout (`75%` peer neurons $\to$ `25%` target neurons separated by `≥70 µm` laterally / `≥30 µm` axially) to define the single-trial shared-variance ceiling.
- **Critical Modeling Pitfalls**:
  1. **Never Use Random Frame Splits**: Facial motion energy, pupil dilation, locomotion, and `GCaMP6s` transients are strongly autocorrelated over seconds—i.i.d. frame splits leak slow state trajectories and severely overestimate `R²`.
  2. **Fluorescence Contamination in Peer Prediction**: Adjacent `2P` ROIs share out-of-focus neuropil/axial PSF overlap; always enforce spatial exclusion zones when predicting target neurons from simultaneous peers (`Shared Variance Component Analysis`, `SVCA`).

## 4. Programmatic Download & Quickstart
```bash
# Inspect Janelia Figshare archives (6163622: main 2P + 8-probe Neuropixels; 7739750: CCF probe locations)
python3 -c "
import json, urllib.request
for art_id in (6163622, 7739750):
    with urllib.request.urlopen(f'https://api.figshare.com/v2/articles/{art_id}') as r:
        meta = json.load(r)
    print(art_id, meta['title'], '| files:', len(meta['files']))
"
```

## 5. Verified Primary References
- **`stringer2019spontaneous`**: Stringer, C., Pachitariu, M., Steinmetz, N. A., Reddy, C. B., Carandini, M., & Harris, K. D. (2019). *Spontaneous behaviors drive multidimensional, brainwide activity*. Science, 364(6437), eaav7893 (`10.1126/science.aav7893`).
