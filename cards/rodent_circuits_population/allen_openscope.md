# Allen Institute OpenScope Community Observatory Suite (`DANDI:000248`, `000253`, `000037`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Operationalizes an **astronomical-observatory model for systems neuroscience** at the Allen Institute MindScope Program: external theoretical and experimental groups propose targeted mechanistic hypotheses, and Allen's industrial-grade **6-probe Neuropixels** and **multi-plane 2-photon calcium imaging** pipelines collect and release standardized, `CCFv3`-registered **NWB 2.0** Dandisets accompanied by executable Jupyter tutorials in the *OpenScope Databook*.
- **Three Flagship Theory-Testing Benchmarks**:
  1. **Kanizsa Illusory Contours & Sensory Inference (`DANDI:000248`, `78` NWB files, `~186 GB` — `Shin, Ogando, ..., Lecoq & Adesnik, Nature Neuroscience, 2025`)**: Multi-Neuropixels recordings across `V1` and `5` HVAs (`LM`, `RL`, `AL`, `PM`, `AM`) plus `2P` holographic optogenetics testing how recurrent `L2/3` pattern-completion (`IC-encoder`) neurons infer illusory bars across blank luminance-free gaps compared to rotated Pac-Man inducer controls.
  2. **Global/Local Oddball Predictive Processing (`DANDI:000253`, `98` NWB files, `~680 GB`)**: Multi-area 6-probe Neuropixels testing hierarchical predictive coding via nested local (`xxxx` vs. `xxxY`) and global sequence-rule violations across the mouse visual hierarchy, thalamus, and midbrain.
  3. **Multi-Day Apical Dendrite vs. Soma Credit Assignment (`DANDI:000037`, `151` NWB files, `~2.48 TB` — `Gillon et al., J. Neurosci., 2023` & `Scientific Data, 2023`)**: Longitudinal `3`-day `2P` imaging of `L2/3` (`Cux2-CreERT2`) and `L5` (`Rbp4-Cre_KL100`) pyramidal **cell bodies** versus **distal `L1` apical dendrites** under predictable Gabor orientation sequences (`A-B-C-D`) disrupted by unexpected orientation substitutions (`U`) and open-loop visual flow mismatches.

## 2. Recording Specifications & Preprocessing
- **Unified NWB 2.0 Schema**: Every OpenScope Dandiset ships self-contained `NWB` files containing `units` (spike times, waveforms, `AllenSDK` QC metrics, 3D `CCFv3` coordinates) or `ophys` (`DfOverF`, `L0` deconvolved events, ROI masks, multi-day `cell_specimen_id` tracking tables), high-precision stimulus `intervals` tables, `30 Hz` running velocity, and `DeepLabCut`/ellipse eye-tracking (`pupil_x`, `pupil_y`, `pupil_area`).
- **Streamable Cloud Access**: Hosted natively on AWS S3 via the **DANDI Archive**, allowing zero-download lazy slicing in Python via `dandi`, `remfile`, `fsspec`, and `pynwb`.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**:
  - `DANDI:000248`: Contrast `Illusory Contour (IC)` vs. `Rotated Inducer Control (RC)` and `Real Edge` conditions across orientation-matched holdouts on center-RF-isolated neurons.
  - `DANDI:000253`: Contrast local sensory adaptation controls against true global sequence-rule oddballs across cortical layers (`L2/3`, `L4`, `L5/6`) and areas.
  - `DANDI:000037`: Compare `Session 1 -> Session 2 -> Session 3` plasticity trajectories of unexpected-stimulus responses (`U - D`) in `L1` distal apical dendrites vs. `L2/3` and `L5` somata.
- **Critical Modeling Pitfalls**:
  1. **Do Not Swap `DANDI:000248` and `DANDI:000253`**: `DANDI:000248` is the *Illusion (Kanizsa)* project (`Shin et al.`), whereas `DANDI:000253` is the *Global/Local Oddball* project.
  2. **Strict Classical-RF & Gaze Filtering (`DANDI:000248`)**: Illusory contour claims are invalidated if a neuron's classical Gabor RF touches the high-contrast Pac-Man corners or if an unexcluded saccade shifts a corner into the RF—enforce strict gaze-centered RF exclusion (`distance_from_gap_center < threshold` and zero response to individual Pac-Man segments).
  3. **Unpaired Compartments (`DANDI:000037`)**: Apical dendritic ROIs (`L1`) and somatic ROIs (`L2/3` or `L5`) are imaged in separate planes/sessions rather than reconstructed back to identical parent cells—model compartment-specific population statistics and within-ROI multi-day tracking rather than assuming `1:1` soma-to-tuft indexing.

## 4. Programmatic Download & Quickstart
```bash
# List or stream OpenScope NWB Dandisets directly from DANDI without full TB-scale downloads
uvx dandi ls DANDI:000248 | head -n 5   # Kanizsa Illusory Contours (Shin et al. 2025)
uvx dandi ls DANDI:000253 | head -n 5   # Global/Local Oddball (GLO)
uvx dandi ls DANDI:000037 | head -n 5   # Soma vs. Apical Dendrite Credit Assignment (Gillon et al. 2023)
```

## 5. Verified Primary References
- **`shin2025recurrent`**: Shin, H., Ogando, M. B., Abdeladim, L., et al. (2025). *Recurrent pattern completion drives the neocortical representation of sensory inference*. Nature Neuroscience (`10.1038/s41593-025-02055-5`).
- **`gillon2023credit`**: Gillon, C. J., Pina, J. E., Lecoq, J. A., et al. (2023). *Responses to pattern-violating visual stimuli evolve differently over days in somata and distal apical dendrites*. Journal of Neuroscience, 43(47), 8009–8028 (`10.1523/jneurosci.1009-23.2023`).
- **`gillon2023scidata`**: Gillon, C. J., Lecoq, J. A., Pina, J. E., et al. (2023). *Responses of pyramidal cell somata and apical dendrites in mouse visual cortex over multiple days*. Scientific Data, 10, 287 (`10.1038/s41597-023-02214-y`).
