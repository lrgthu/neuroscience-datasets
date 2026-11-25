# MICrONS Functional Connectomics & Digital Twin (`MICrONS` · *Nature* 2025)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Bridges **single-synapse anatomical wiring (`EM`)** and **large-scale naturalistic visual coding (`2P`)** in the exact same cortical tissue (`MICrONS Consortium / Bae et al., Nature, 2025`), accompanied by the landmark **mouse visual foundation model ("digital twin")** (`Wang, Fahey, Ding, Sinz & Tolias et al., Nature, 2025`) that predicts single-neuron responses across unseen OOD stimulus domains and predicts anatomical cell types & monosynaptic connectivity from functional embeddings!
- **Two Interlocking Releases**:
  1. **`Cortical MM³` (`minnie65` on `s3://iarpa-microns` & `CAVEclient`)**: `~75,000` functionally imaged `GCaMP6s` excitatory/inhibitory neurons spanning `V1`, `LM`, `AL`, and `RL` (`Layers 2/3–6`) co-registered at micron precision to `>120,000` segmented EM cells and `~500 million` cleft-detected synapses.
  2. **Functional Digital-Twin Cohort (`DANDI:000402` & companion mice)**: Multi-session, multi-mouse 2P recordings (`>135,000` neurons) under diverse cinematic/sports/nature video clips, parametric `Monet` / `Trippy` noise, and OOD grating/dot/image probes with `30 Hz` pupil gaze and locomotion tracking.

## 2. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Fit shared dynamic visual core + per-neuron spatial/feature readouts on single-repeat natural movie blocks; evaluate `CC_norm` (`correlation / oracle ceiling`) on `10`-repeat `Oracle` clips and held-out OOD stimulus classes.
- **Critical Modeling Pitfalls**:
  1. **Filter by `CAVE` Proofreading Status**: Raw automated EM segmentation contains split/merge errors on thin axons—always filter via `caveclient` (`status_axon == 'extended' / 'clean'`) before testing `like-to-like` synaptic rules!
  2. **Include Eye-Position & Pupil-Size Inputs**: Awake mice make saccade-like eye movements that shift `V1` `RF` centers by `5–15°`—shifter networks conditioned on `pupil_x, pupil_y` are essential.

## 4. Programmatic Download & Quickstart
```bash
# 1. Functional NWB recordings from DANDI Archive (Dandiset 000402)
uvx dandi download DANDI:000402

# 2. Petascale EM + coregistration tables on AWS Open Data (or query interactively via CAVEclient)
aws s3 ls --no-sign-request s3://iarpa-microns/minnie/minnie65/
```

## 5. Verified Primary References
- **`bae2025microns`**: The MICrONS Consortium, Bae, J. A., Baptiste, M., et al. (2025). *Functional connectomics spanning multiple areas of mouse visual cortex*. Nature (`10.1038/s41586-025-08790-w`).
- **`wang2025micronsfm`**: Wang, E. Y., Fahey, P. G., Ding, Z., et al. (2025). *Foundation model of neural activity predicts response to new stimulus types*. Nature (`10.1038/s41586-025-08829-y`).
