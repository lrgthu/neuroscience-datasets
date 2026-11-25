# Adult *Drosophila* Pan-Neuronal Whole-Brain Two-Photon & Volumetric Functional Atlases (`Brezovec et al., 2024` & `Aimon et al., 2019`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Supplies the indispensable **live whole-brain functional counterpart** to the static `FlyWire` (`139,255` neurons) and `Hemibrain` (`~25,000` neurons) electron-microscopy connectomes in adult *Drosophila melanogaster*:
  1. **Clandinin Lab Whole-Brain Walking Two-Photon Atlas (`Brezovec et al., Current Biology, 2024` · `DANDI:000727` & `Dryad:10.5061/dryad.8pk0p2nx1`)**: High-SNR volumetric resonant two-photon `nSyb-GCaMP6f` + `tdTomato` imaging spanning the **entire adult *Drosophila* central brain** during tethered spherical-treadmill (`FicTrac`) locomotion, aligned via **`BIFROST`** into the shared **Functional *Drosophila* Atlas (`FDA`)** (`~2 µm` registration accuracy, bridgeable directly into `JRC2018` / `FlyWire` neuropil space!). Reveals that ~`40%` of the brain encodes 3D walking kinematics, organized into continuous topographic maps of forward vs. angular velocity (`Lateral Accessory Lobe`, `Wedge`, `Protocerebral Bridge`, `Posterior Slope`) whose population trajectories sweep ahead to anticipate upcoming turns.
  2. **Greenspan / Sejnowski / Deisseroth Fast Pan-Neuronal Whole-Brain Benchmark (`Aimon et al., PLOS Biology, 2019` · `CRCNS:fly-1`)**: Pioneered pan-neuronal (`nsyb-GAL4`) and broad `GAL4`/`TH-GAL4`/`Tdc2-GAL4` whole-brain functional imaging (`up to 20–200 Hz` light-field + `2P` validation across `>50` flies) during rest, walking, grooming, and odor/visual flashes—discovering brain-wide behavioral state switching and resting-state functional neuropil networks in insects.

## 2. Recording Specifications & Atlas Registration Bridge
- **Volumetric Two-Photon (`Brezovec et al., DANDI:000727`)**:
  - Piezo-driven resonant `2P` z-stacks across the full anterior–posterior central brain (`~1.8–2.8 Hz` volume rate) with simultaneous `GCaMP6f` (functional) and myristoylated `tdTomato` (anatomical motion/registration channel), paired with `50–100 Hz` optical ball-tracking (`forward`, `rotational`, and `sideways` walking velocities).
  - **`BIFROST` (`Brain Registration into `FDA` → `JRC2018` → `FAFB`/`FlyWire`)**: Enables direct voxel-by-voxel comparison between functional `2P` correlation/encoding maps and aggregated `FlyWire` / `Hemibrain` synaptic projection density!

## 3. Canonical Splits, Connectome-Function Comparison & Modeling Pitfalls
- **Standard Modeling Tasks**:
  1. **Structure–Function Connectome Benchmarking**: Aggregate `FlyWire v783` synapse density (`78` Ito neuropils or `FDA` supervoxels) and test how graph Laplacian eigenmodes, communicability, or `Shiu et al.` whole-brain spiking simulations predict empirical `2P` functional connectivity (`Turner, Mann, Clandinin et al.`) during quiescence vs. walking.
  2. **Continuous 3D Velocity & Turn-Initiation Forecasting**: Decode `(v_fwd, v_rot)` and pre-turn state transitions across `Leave-One-Fly-Out` (`LOFO`) splits in `FDA` supervoxel space.
- **Critical Modeling Pitfalls**:
  1. **Invertebrate Unipolar Morphology (`Neuropil` != `Somata`)**: Unlike mammalian or zebrafish brains where `GCaMP` ROIs correspond to `1` cell body, insect neurons are unipolar—their passive cell bodies sit in an outer rind while **all synaptic integration occurs in dense interior neuropil**. Pan-neuronal `nSyb-GCaMP` supervoxels therefore measure **local synaptic/neurite population ensembles**, not isolated single-cell spikes!
  2. **Dominant Locomotor State Shifts**: Just as running/whisking dominates mouse cortex (`Stringer et al., 2019`), walking onset triggers global neuromodulatory/octopaminergic/dopaminergic surges across ~half the fly brain—always stratify resting vs. walking epochs and regress `FicTrac` kinematic kernels (`±5 s` lag window) before attributing covariance to intrinsic resting circuits.
  3. **Correct Non-Rigid Esophageal/Proboscis Brain Motion**: Gut/proboscis pulsations through the esophageal foramen warp ventral neuropils (`SEZ`, `AMMC`); always use the companion `tdTomato`-warped or `BIFROST` motion-corrected `NWB` series rather than unaligned raw fluorescence stacks.

## 4. Programmatic Download & Quickstart
```bash
# 1. Download standardized NWB whole-brain 2P + FicTrac walking datasets from DANDI (zero auth!)
uvx dandi download DANDI:000727 --output-dir ./drosophila_brezovec_2p

# 2. Fetch FDA / BIFROST template atlases from Dryad (10.5061/dryad.8pk0p2nx1) or CRCNS fly-1 (crcns.org)
```

## 5. Verified Primary References
- **`brezovec2024drosophila`**: Brezovec, B. E., Berger, A. B., Hao, Y. A., Chen, F., Druckmann, S., & Clandinin, T. R. (2024). *Mapping the neural dynamics of locomotion across the Drosophila brain*. Current Biology (`10.1016/j.cub.2023.12.063`).
- **`aimon2019drosophila`**: Aimon, S., Katsuki, T., Jia, T., et al. (2019). *Fast near-whole–brain imaging in adult Drosophila during responses to stimuli and behavior*. PLOS Biology (`10.1371/journal.pbio.2006732`).
