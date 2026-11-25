# Whole-Brain Cell-Identified *C. elegans* Atlases (`Flavell NeuroPAL` `DANDI:000776` & `Zimmer Global Dynamics`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: *Caenorhabditis elegans* is the **only animal in neuroscience** where every individual shares an **invariant, deterministic `302`-neuron lineage** with completely mapped chemical synapses, electrical gap junctions (`White et al., 1986`; `Witvliet et al., Nature, 2021`), and wireless neuropeptidergic GPCR networks—and where **multicolor `NeuroPAL` barcoding (`Yemini et al., Cell, 2021`)** identifies exact named neurons (`AVAL`, `AVAR`, `RIBL`, `NSM`, `AIY`, `RIM`, ...) *in vivo* during whole-brain calcium imaging!
- **Two Landmark Complementary Cohorts**:
  1. **Flavell Lab Freely Moving `NeuroPAL` Whole-Brain Atlas (`Atanas et al., Cell, 2023` · `DANDI:000776` & `wormwideweb.org`)**: Tracks **`~120–180` head neurons (`~60–100+` unambiguously NeuroPAL-identified per animal, covering `186 / 189` head neuron classes across the cohort)** at `1.7 Hz` in **`40+` freely moving, foraging worms** (`16 min` continuous recordings + noxious heat-pulse state transitions), alongside full-body posture kinematics, velocity, head curvature, pharyngeal pumping, defecation, and egg-laying.
  2. **Zimmer Lab Immobilized Global Motor-Command Benchmark (`Kato et al., Cell, 2015` · `OSF:2395t`)**: Foundational `~2.9 Hz` whole-brain `GCaMP5K` recordings (`N = 12` worms: `5` spontaneous + `7` `O₂`-chemosensory stimulated, `~107–131` head neurons/worm) that revealed low-dimensional cyclic neural state-space manifolds embedding forward, reversal, and ventral/dorsal turn command sequences (`rSLDS` / `CEBRA` / `MARBLE` benchmark staple).

## 2. Recording Specifications & Standardized NWB Release
- **Closed-Loop 3D Tracking + Ratiometric `GCaMP7f` + `NeuroPAL` (`Atanas et al., 2023`)**:
  - Real-time `XY/Z` stage tracking keeps the rapidly moving worm head centered inside a spinning-disk confocal volume (`1.7` volumes/s) while dual-channel **`GCaMP7f` / `tagRFP-T`** ratiometry cancels movement-induced fluorescence fluctuations, followed by a multi-spectral `4`-fluorophore **`NeuroPAL`** structural volume at the end of each trial to assign canonical cell names.
  - Released in **Neurodata Without Borders (`NWB`)** on `DANDI:000776` (and interactive JSON/CSV on `wormwideweb.org`), including **`GFP`-only control worms** that empirically bound residual motion artifacts during high-curvature turns!

## 3. Canonical Splits, `1:1` Cell Ceilings & Modeling Pitfalls
- **Unique Machine-Learning Capabilities**:
  1. **Zero-Ambiguity Cross-Subject Stitching (`Exact Cell-ID Tokenization`)**: Unlike mouse/primate/zebrafish population recordings that require learned per-session read-in matrices, *C. elegans* NeuroPAL recordings allow **stitching sparse `189 × T` named-neuron matrices directly across `40+` animals** to pretrain multi-worm foundation models or fit probabilistic behavioral encoding models (`Atanas et al.` exponential-convolved linear-nonlinear kernel model).
  2. **Testing Structure → Function Causality**: Directly compare static `White`/`Witvliet` synaptic + gap-junction adjacency matrices against observed dynamic Granger/state-space coupling.
- **Critical Modeling Pitfalls**:
  1. **Immobilized (`Kato 2015`) != Freely Moving (`Atanas 2023`)**: Microfluidic paralysis suppresses proprioceptive postural feedback and feeding rhythms, artificially concentrating `>65%` of variance into `2–3` global `AVA/RIB` reversal PCs; freely moving worms exhibit richer multi-timescale integration (`from <1 s head swings to >60 s persistent roaming/dwelling/heat-arousal states`) and context-dependent neuron remapping!
  2. **Graded Non-Spiking Potentials**: Almost all *C. elegans* neurons (`except AWA` and a few regenerative plateau cells) compute via **graded analog membrane potentials** rather than `Na+` action-potential spikes—never apply mammalian point-process spike-train Poisson deconvolution (`OASIS` spike thresholding) to *C. elegans* `GCaMP` traces!
  3. **Respect `NeuroPAL` Confidence Scores & Missing-At-Random Cells**: In any single freely moving recording, optical occlusion leaves ~30–40% of tracked ROIs unnamed (`anonymous` trace columns) or partially ambiguous (`L/R` bilateral pair)—mask missing named cells explicitly rather than imputing zeros, and verify effect sizes against the `GFP` motion-artifact control dataset.

## 4. Programmatic Download & Quickstart
```bash
# 1. Download standardized NWB whole-brain + NeuroPAL + behavior sessions from DANDI (zero auth!)
uvx dandi download DANDI:000776 --output-dir ./celegans_flavell_nwb

# 2. Or fetch lightweight preprocessed JSON traces & cell-ID tables directly from WormWideWeb
curl -sL "https://wormwideweb.org/" | head -n 20
```

## 5. Verified Primary References
- **`atanas2023celegans`**: Atanas, A. A., Kim, J., Wang, Z., et al. (2023). *Brain-wide representations of behavior spanning multiple timescales and states in C. elegans*. Cell (`10.1016/j.cell.2023.07.035`).
- **`kato2015celegans`**: Kato, S., Kaplan, H. S., Schrödel, T., et al. (2015). *Global Brain Dynamics Embed the Motor Command Sequence of Caenorhabditis elegans*. Cell (`10.1016/j.cell.2015.09.034`).
- **`yemini2021neuropal`**: Yemini, E., Lin, A., Nejatbakhsh, A., et al. (2021). *NeuroPAL: A Multicolor Atlas for Whole-Brain Neuronal Identification in C. elegans*. Cell (`10.1016/j.cell.2020.12.012`).
