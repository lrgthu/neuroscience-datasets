# Ahrens Lab Multi-Fish Whole-Brain Light-Sheet & Fictive Behavior Atlas (`Chen, Mu et al., Neuron 2018`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Whereas `ZAPBench` (`Lueckmann et al., 2025`) deeply samples a single larval zebrafish (`N = 1`), `Chen, Mu et al. (Neuron, 2018)` (building on `Ahrens et al., Nature Methods, 2013`) provides the premier **multi-individual (`N = 18` fish) whole-brain cellular-resolution calcium imaging + fictive motor behavior atlas** (`Figshare:10.25378/janelia.7272617`), capturing **`~80,000–100,000` single neurons per fish (`>1.5 million` neurons total)** co-registered into the canonical **`Z-Brain` `294`-region anatomical reference atlas**.
- **Convergent Sensorimotor Battery**: Exposes each larva to a multi-task visual-motor suite—hemifield **phototaxis** (`left` vs. `right` brightness), forward/lateral **optomotor gratings (`OMR`)**, sudden **dark flashes** (`O-bend` startle), expanding **looming discs**, and **spontaneous swimming**—revealing how distinct sensory pathways (`optic tectum`, `pretectum`, `habenula`) converge onto shared anterior-hindbrain prepontine/rhombomeric turn oscillators while preserving stimulus-specific history.

## 2. Recording Specifications & `FishExplorer` Data Structure
- **Dual-Beam Light-Sheet Microscopy (`Tg(elavl3:H2B-GCaMP6f)` pan-neuronal nuclear line, `5–7 dpf`)**:
  - Volumetric whole-brain acquisition at **`~2.1 Hz`** (`~40–50` z-planes spanning telencephalon, diencephalon, mesencephalon, cerebellum, and hindbrain) avoiding direct laser illumination of the retinas.
  - **Simultaneous Fictive Motor Readout (`6,000 Hz`)**: Bilateral extracellular suction electrodes on left and right tail motor nerve roots decode forward swim bouts vs. left/right turns in real time to update closed-loop visual projection.
- **Released HDF5 / MATLAB v7.3 Arrays (`18` Subjects + `FishExplorer` GUI/API)**:
  - Single-cell $\Delta F/F$ timeseries (`CellResp`), `3D` native & `Z-Brain` warped `(x, y, z)` soma coordinates, `294` binary anatomical region masks (`MaskDatabase`), stimulus regressors, and decoded left/right fictive swim vigor traces.

## 3. Canonical Splits, Stereotypy & Modeling Pitfalls
- **Standard Evaluation Benchmarks**:
  1. **Multi-Animal Whole-Brain Manifold Alignment**: Train shared dynamical/foundation models (`rSLDS`, `LFADS`, `CEBRA`, multi-session stitched state-space models) on `14` fish and evaluate zero-shot or few-shot readout alignment on `4` held-out fish using `Z-Brain` regional priors.
  2. **Trial-by-Trial Motor Choice & Internal State Decoding**: Predict upcoming left vs. right fictive turn direction during ambiguous/spontaneous intervals from anterior hindbrain (`ARTR` — anterior rhombencephalic turning region) population state.
- **Critical Modeling Pitfalls**:
  1. **Never Assume `1:1` Cell-Index Correspondence Across Fish**: Vertebrate neurogenesis exhibits stochastic cell counts and soma jitter (`~5–15 µm`) within each nucleus; cross-fish models must pool via anatomical `Z-Brain` parcels, functional cluster prototypes (`AutoCluster` in `FishExplorer`), or Procrustes/low-rank latent alignment!
  2. **Account for Closed-Loop Fictive Gain & Missing Proprioception**: Immobilized larvae experience visual reafference without physical body bending or inner-ear acceleration—distinguish efference-copy motor corollary discharge (which lights up large swathes of hindbrain/cerebellum during every swim bout!) from pure visual sensory tuning.
  3. **Slow Nuclear `H2B-GCaMP6f` Filtering**: Nuclear `H2B` tagging eliminates neuropil contamination across `~80,000` tightly packed cells, but introduces a `~1.5–2.5 s` exponential calcium tail; apply nonnegative oasis deconvolution or state-space observation kernels before Granger/directed-lag causal inference.

## 4. Programmatic Download & Quickstart
```bash
# Inspect and download all 18 Z-Brain-registered fish HDF5/.mat archives from Janelia Figshare (CC-BY-4.0)
curl -s "https://api.figshare.com/v2/articles/7272617" | uv run python -c "
import json, sys
meta = json.load(sys.stdin)
for f in meta['files'][:8]:
    print(f['name'], f\"{f['size']/1e9:.2f} GB\", f['download_url'])
"
```

## 5. Verified Primary References
- **`chen2018zebrafish`**: Chen, X., Mu, Y., Hu, Y., et al. (2018). *Brain-wide Organization of Neuronal Activity and Convergent Sensorimotor Transformations in Larval Zebrafish*. Neuron (`10.1016/j.neuron.2018.09.042`).
- **`ahrens2013lightsheet`**: Ahrens, M. B., Orger, M. B., Robson, D. N., Li, J. M., & Keller, P. J. (2013). *Whole-brain functional imaging at cellular resolution using light-sheet microscopy*. Nature Methods (`10.1038/nmeth.2434`).
