# Janelia FlyEM Adult *Drosophila* Connectomes (`Hemibrain`, `Optic-Lobe` & `MANC` via `neuPrint`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Pioneered **isotropic `8 × 8 × 8 nm` Focused Ion Beam Scanning Electron Microscopy (`FIB-SEM`)**, Google Flood-Filling Network (`FFN`) 3D segmentation, and Neo4j graph-database connectomics (`neuPrint`) (`Scheffer et al., eLife, 2020`; `Takemura et al., eLife, 2024`):
  1. **`Hemibrain v1.2.1` (`Scheffer et al., 2020`, Adult Female Central Brain)**: Densely reconstructs **`~25,000` uncropped central-brain neurons** (`~5,000` morphological cell types, **`~20 million` chemical synapses**) across the Mushroom Body (associative learning), Central Complex (`E-PG` / `P-EN` head-direction ring attractor, `Hulse et al., eLife, 2021`), Antennal Lobe, and Lateral Horn.
  2. **`MANC v1.2.1` (`Takemura et al., 2024`, Male Adult Nerve Cord)**: Complete synaptic connectome of the insect spinal-cord analog—**`~23,000` neurons**, **`~10 million` presynaptic T-bars**, **`~74 million` postsynaptic densities (`PSDs`)**, and `44 m` of wiring controlling `6`-leg walking, wing flight/courtship song, halteres, and descending/ascending sensorimotor loops.
  3. **FlyEM Optic-Lobe & Connectome-Constrained Deep Mechanistic Networks (`Lappalainen et al., Nature, 2024`)**: Supplying exact columnar synapse counts and neurotransmitter signs across `64` visual cell types (`T4/T5` motion detectors, `Mi1`, `Tm1–Tm9`), FlyEM enabled `flyvis`—showing that **connectome topology + task optimization (`optic flow` alone, zero neural recording supervision!)** predicts single-cell visual tuning across `24` experimental studies.

## 2. Recording Specifications & `neuPrint` Ecosystem
- **True Isotropic `8 × 8 × 8 nm` 3D Ultrastructure**: Unlike `4 × 4 × 40 nm` serial-section TEM (`FlyWire`/`MICrONS`), milled FIB-SEM eliminates `40 nm` z-axis anisotropy, missing sections, and shear Tears—providing the cleanest ground-truth benchmark for 3D volumetric segmentation (`FFN`) and automated `T-bar` → `PSD` synapse detection.
- **Programmatic Graph Querying (`neuPrint` Neo4j + GCS Tarballs)**:
  - Query complex multi-hop motifs (`e.g. ORN → PN → KC → MBON` or `DN → Premotor → Leg MN`) in milliseconds via Cypher / `neuprint-python`, or download complete static CSV adjacency exports directly from Google Cloud Storage (`gs://flyem-hemibrain/`, `gs://flyem-vnc-2-32-213dba2/`).

## 3. Canonical Splits, Ensemble Determinacy & Modeling Pitfalls
- **Canonical Modeling Paradigms**:
  - **Connectome-Constrained Task Optimization (`flyvis` protocol)**: Fix graph sparsity, synapse counts, and excitatory/inhibitory signs from FlyEM; share single-cell time constants and resting potentials by cell type (`~700` free biophysical parameters total for `45,669` neurons!); train `50` ensemble models on naturalistic Sintel optic flow; cluster ensemble modes and evaluate against two-photon directional/flash tuning.
  - **Analytical Circuit Theory**: Ring-attractor angular velocity integration (`Central Complex`), sparse random expansion coding (`Mushroom Body`), and hexapodal CPG coordination (`MANC`).
- **Critical Modeling Pitfalls**:
  1. **Always Filter `status == "Traced"` AND `cropped == False` in `Hemibrain`**: `Hemibrain` was milled across `~13` hot-knife `20 µm` slabs covering ~1/3 to 1/2 of the whole brain; neurons crossing slab boundaries into unimaged contralateral/ventral tissue have `cropped: true` (`instance` suffixed `_L` or truncated) and severely underestimated degree! (Use `FlyWire v783` when full bilateral brain completeness is required.)
  2. **Distinguish Presynaptic `T-bars` (`pre`) from Postsynaptic `PSDs` (`weight`)**: Because insect synapses are polyadic (`1` T-bar broadcasts to `~5–7` postsynaptic partners), summing `weight` gives total postsynaptic contact count, NOT total presynaptic release sites (`pre`).
  3. **Respect Female (`Hemibrain`) vs. Male (`MANC`) Dimorphism**: Roughly `~5–10%` of descending/VNC neurons (`fru+`/`dsx+` lineages) are sexually dimorphic; match descending neuron (`DN`) types carefully (`Stürner et al.` / `Cheong et al.`) rather than assuming 100% `1:1` isomorphism across sexes.

## 4. Programmatic Download & Quickstart
```bash
# 1. Direct zero-auth download of exported Hemibrain v1.2.1 traced neuron & synapse CSVs from Google Cloud Storage
curl -LO https://storage.googleapis.com/flyem-hemibrain/v1.2/exported-traced-adjacencies-v1.2.tar.gz

# 2. Or query Hemibrain / MANC interactively via neuprint-python (requires free token from neuprint.janelia.org)
uv run --with neuprint-python python -c "
from neuprint import Client, fetch_neurons, NeuronCriteria as NC
# c = Client('neuprint.janelia.org', dataset='hemibrain:v1.2.1', token='<NEUPRINT_TOKEN>')
print('neuprint-python ready; datasets: hemibrain:v1.2.1, manc:v1.2.1, optic-lobe:v1.1')
"
```

## 5. Verified Primary References
- **`scheffer2020hemibrain`**: Scheffer, L. K., Xu, C. S., Januszewski, M., et al. (2020). *A connectome and analysis of the adult Drosophila central brain*. eLife (`10.7554/eLife.57443`).
- **`takemura2024manc`**: Takemura, S.-y., Hayworth, K. J., Huang, G. B., et al. (2024). *A Connectome of the Male Drosophila Ventral Nerve Cord*. eLife (`10.7554/eLife.97769`).
- **`lappalainen2024flyvis`**: Lappalainen, J. K., Tschopp, F. D., Prakhya, S., et al. (2024). *Connectome-constrained networks predict neural activity across the fly visual system*. Nature (`10.1038/s41586-024-07939-3`).
