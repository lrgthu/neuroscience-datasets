# FlyWire Adult *Drosophila* Whole-Brain Synaptic Connectome (`FAFB v783` · `Codex`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Delivers the first complete synaptic-resolution wiring diagram of an entire adult central brain beyond *C. elegans* (`~302` neurons) and larval *Drosophila* (`3,016` neurons)—reconstructing all **`139,255` neurons** and **`~54.5 million` chemical synapses** across both hemispheres and both optic lobes of an adult female *Drosophila melanogaster* (`Dorkenwald et al., Nature, 2024`; `Schlegel et al., Nature, 2024`).
- **AI + Citizen/Expert Community Scale**: Built on the `FAFB` (`Full Adult Fly Brain`, `Zheng et al., Cell, 2018`) serial-section TEM volume via deep convolutional flood-filling/affinity segmentation (`Macrina et al.`), automated synapse & neurotransmitter prediction (`Buhmann et al.`; `Eckstein et al., Cell, 2024`), and `>33` person-years of human proofreading coordinated through CAVE (`Connectome Annotation Versioning Engine`).
- **Whole-Brain Mechanistic Simulation**: Directly parameterizes leaky integrate-and-fire (`LIF`) whole-brain models (`Shiu et al., Nature, 2024`) with **zero free connectivity weights**, accurately predicting gustatory feeding and antennal grooming sensorimotor circuits from `root_id` topology + predicted neurotransmitter signs alone.

## 2. Structural & Annotation Specifications (`Materialization v783`)
- **Physical Volume & Resolution**: `~950 × 500 × 430 µm³` adult female brain imaged at **`4 × 4 × 40 nm`** (`7,062` serial TEM sections), containing **`149.2 meters`** of total neuronal cable partitioned into **`78` canonical brain neuropils** (`Ito et al.` nomenclature).
- **Rich Multi-Layered Annotations (`Schlegel et al., Nature, 2024`)**:
  - **`8,453` Annotated Cell Types**: `4,581` types cross-matched `1:1` to prior `Hemibrain` nomenclature plus `3,872` newly defined types (especially bilateral optic lobes, subesophageal zone `SEZ`, and ascending/descending neck-connective neurons).
  - **Hierarchical Flow Classes**: Intrinsic brain neurons (`118,000+`), visual centrifugal/projection neurons (`~8,000` per optic lobe), sensory afferents (`~16,000+` photoreceptors, mechanosensory, olfactory, gustatory, auditory), descending neurons (`~1,300` `DNs` projecting to VNC), ascending neurons (`~1,800` `ANs`), and neurosecretory/endocrine cells.
  - **Synapse-Level Neurotransmitter Predictions (`Synister`)**: Deep-learning classification from `4 nm` ultrastructure into `Acetylcholine` (excitatory), `GABA` (inhibitory), `Glutamate` (**often inhibitory via `GluClα` in insects!**), `Dopamine`, `Serotonin`, and `Octopamine`.

## 3. Canonical Splits, Stereotypy Ceilings & Modeling Pitfalls
- **Standard Evaluation Splits**:
  1. **Left vs. Right Hemisphere Generalization**: Train GNNs, spectral graph embeddings, or motif classifiers on the Left hemisphere (`~69k` neurons) and evaluate zero-shot cell-type or functional-role transfer on the Right hemisphere.
  2. **Cross-Individual Connectome Alignment (`FlyWire FAFB` ↔ `Janelia Hemibrain`)**: Benchmark graph-matching and stereotypy across two distinct female brains (`Schlegel et al. 2024` show edges with `≥10` synapses replicate with `>95%` probability across individuals).
- **Critical Modeling Pitfalls**:
  1. **Glutamate Is Frequently Inhibitory in *Drosophila* Central Circuits!**: Vertebrate modelers routinely hard-code `Glutamate = +1 (excitatory)`, which **inverts circuit sign** across the fly brain (where `GluClα` glutamate-gated chloride channels mediate widespread inhibition, e.g., in the optic lobe, antennal lobe, and central complex—just as `Shiu et al. 2024` assign negative weights to glutamatergic synapses by default!).
  2. **Filter `1–4` Synapse Edges When Analyzing Core Pathways**: Roughly `~70%` of raw `1`-synapse pairs reflect automated synapse-assignment spillover or developmental contact noise; apply the standard **`syn_count ≥ 5`** threshold (`connections.feather` / `connections_princeton.csv.gz`) unless explicitly studying weak-tail topology.
  3. **Pin `v783` Root IDs (`64-bit integers`, never `float64`!)**: FlyWire `root_id`s (`e.g. 720575940610453042`) exceed `2^53` (`IEEE-754 float64` integer precision limit = `9.007e15`)! Reading CSVs in Python/Pandas/R/JS without explicit `dtype={'pre_root_id': 'int64', 'post_root_id': 'int64'}` (or `'string'`) **silently corrupts the last 3 digits of every neuron ID!**
  4. **Unobserved Gap Junctions & Neuromodulation**: Electrical synapses (`shakB` innexins, crucial in giant-fiber escape and visual LPTC circuits) and extrasynaptic neuropeptide cotransmission are invisible in `4 × 4 × 40 nm` ssTEM.

## 4. Programmatic Download & Quickstart
```bash
# Download flat v783 Parquet/Feather/CSV connectome & cell-type tables directly from Zenodo (zero credentials!)
curl -L "https://zenodo.org/records/10676866/files/classification.csv.gz?download=1" -o flywire_v783_classification.csv.gz
curl -L "https://zenodo.org/records/10676866/files/connections.csv.gz?download=1" -o flywire_v783_connections.csv.gz

# CRITICAL: Always parse 64-bit root_ids as int64/uint64 (NEVER float64!)
uv run --with pandas python -c "
import pandas as pd
df = pd.read_csv('flywire_v783_classification.csv.gz', dtype={'root_id': 'int64'})
print('Total proofread FlyWire v783 neurons:', len(df))
"
```

## 5. Verified Primary References
- **`dorkenwald2024flywire`**: Dorkenwald, S., Matsliah, A., Sterling, A. R., et al. (2024). *Neuronal wiring diagram of an adult brain*. Nature (`10.1038/s41586-024-07558-y`).
- **`schlegel2024flywiretypes`**: Schlegel, P., Yin, Y., Bates, A. S., et al. (2024). *Whole-brain annotation and multi-connectome cell typing of Drosophila*. Nature (`10.1038/s41586-024-07686-5`).
- **`shiu2024flywiremodel`**: Shiu, P. K., Sterne, G. R., Spiller, N., et al. (2024). *A Drosophila computational brain model reveals sensorimotor processing*. Nature (`10.1038/s41586-024-07763-9`).
