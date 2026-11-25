# Intraoperative Human Cortical Neuropixels Single-Unit Recordings (`Dryad:10.5061/dryad.d2547d840` / `DANDI:000397`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Bridges the `100×` density gap between animal systems neuroscience and human clinical neurophysiology by deploying thickened-shank **Neuropixels (`384` active channels spanning `3.84 mm` cortical depth at `20 µm` spacing)** intraoperatively in human cortex, isolating **`100–300+` single units simultaneously from a single cortical column**:
  1. **Foundational Cortical Microcircuitry & Sterile OR Protocol (`Paulk et al., Nature Neuroscience, 2022`; `Coughlin et al., Nature Protocols, 2023`)**: `9` neurosurgical patients (`dlPFC` and lateral temporal cortex; open data on `Dryad:10.5061/dryad.d2547d840` and `DANDI:000397`), characterizing regular-spiking putative excitatory pyramidal cells vs. narrow-spiking inhibitory interneurons and putative monosynaptic cross-correlograms across cortical depths.
  2. **Laminar Speech Perception & Production Extensions (`Leonard et al., Nature, 2023/2024`; `Khanna et al., Nature, 2024`)**: Awake intraoperative Neuropixels recordings in superior temporal gyrus (`STG`, `N = 8`) during natural speech listening and prefrontal cortex (`dlPFC`, `N = 5`) during natural spoken sentence planning,syllabification, and articulation.

## 2. Recording Specifications & Preprocessing
- **Dual-Band Silicon Probe Streams**: `30 kHz` action-potential (`AP`, `300 Hz–10 kHz`) and `2.5 kHz` local field potential (`LFP`, `0.5–500 Hz`) streams across `384` staggered contacts, paired with spike-sorted Kilosort/Phy clusters, extracellular waveform trough-to-peak durations, and vertical depth drift trajectories.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Critical Modeling Pitfalls**:
  1. **Mandatory Non-Rigid Motion De-Drifting Before Spike Sorting or LFP CSD**: Human heartbeat (`~1 Hz`) and mechanical ventilation/speech breathing (`~0.2–0.3 Hz`) displace cortex vertically by `50–400 µm` along the probe shank. Always verify motion-registered spike rasters (checking that firing rates are not phase-locked to the `1 Hz` ballistocardiogram artifact!) and register LFP channels prior to computing laminar Current Source Density (`CSD`).
  2. **Stratify Awake vs. Anesthetized Cohorts**: Propofol/sevoflurane anesthesia profoundly suppresses superficial-layer firing and induces slow-wave (`<1 Hz`) UP/DOWN states—never mix anesthetized and awake insertions when benchmarking baseline cortical criticality or E/I balance.

## 4. Programmatic Download & Quickstart
```bash
# Download NWB LFP/neurophysiology files from DANDI and spike-sorted Dryad archive
uvx dandi download DANDI:000397
curl -L "https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.d2547d840/download" \
  -o paulk_human_neuropixels.zip
```

## 5. Verified Primary References
- **`paulk2022neuropixels`**: Paulk, A. C., Kfir, Y., Khanna, A. R., Mustroph, M. L., Trautmann, E. M., Soper, D. J., et al. (2022). *Large-scale neural recordings with single neuron resolution using Neuropixels probes in human cortex*. Nature Neuroscience (`10.1038/s41593-021-00997-0`).
- **`coughlin2023neuropixels`**: Coughlin, B. F., Muñoz, W., Kfir, Y., Young, M. J., Meszéna, D., Jamali, M., et al. (2023). *Modified Neuropixels probes for recording human neurophysiology in the operating room*. Nature Protocols (`10.1038/s41596-023-00871-2`).
- **`leonard2023neuropixels`**: Leonard, M. K., Gwilliams, L., Sellers, K. K., Chung, J. E., Xu, D., Mischler, G., et al. (2023). *Large-scale single-neuron speech sound encoding across the depth of human cortex*. Nature (`10.1038/s41586-023-06839-2`).
- **`khanna2024neuropixels`**: Khanna, A. R., Muñoz, W., Kim, Y. J., Kfir, Y., Paulk, A. C., Jamali, M., et al. (2024). *Single-neuronal elements of speech production in humans*. Nature (`10.1038/s41586-023-06982-w`).
