# Miller Lab Multi-Session Macaque M1/PMd/Area2 Reaching & Perturbation Archive (`Perich-Miller` / `DANDI:000688`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Consolidates over `100` multi-year chronic macaque electrophysiology sessions (`Chewie`, `Mihili`, `Jaco`, `MrT`) from Lee E. Miller's laboratory at Northwestern University into standardized **NWB** format (`DANDI:000688`), anchoring two foundational discoveries in systems neuroscience and large-scale neural foundation modeling:
  1. **Rapid Motor Learning via Preparatory Subspace Realignment (`Perich, Gallego, & Miller, Neuron, 2018`)**: Simultaneous `PMd + M1` population recordings across curl-field force perturbations and visuomotor rotations (`Baseline → Adaptation → Washout`).
  2. **Multi-Year Stability of Latent Cortical Manifolds (`Gallego et al., Nature Neuroscience, 2020`)**: Longitudinal recordings spanning up to `>700 days` demonstrating stable low-dimensional population dynamics (`CCA`) across `M1`, `PMd`, and somatosensory `Area 2` despite continuous single-neuron turnover.

## 2. Recording Specifications & Preprocessing
- **Arrays & Behavioral Rig**: `96-channel` Utah arrays implanted in `M1`, `PMd`, and/or `Area 2` while monkeys controlled a `2-link` planar robotic manipulandum (`center-out` 8-target delayed reaching, `random-target` pursuit, and `mechanical bump` perturbations), recording spike-sorted single units alongside continuous handle position, velocity, interaction forces, and forelimb `EMG`.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Foundation-Model & Manifold Splits**: Adopted alongside `Sabes-Indy-Loco` as the core multi-animal pretraining benchmark in **`POYO`** (`Azabou et al., 2023`), evaluating both within-session trial holdouts (`velocity R^2`) and cross-day / cross-animal latent manifold alignment (`CCA` / `few-shot R^2`).
- **Critical Modeling Pitfalls**:
  1. **Filter by Behavioral Epoch Metadata (`BL` vs. `AD` vs. `WO`)**: Perturbation sessions intentionally break the mapping between neural drive, handle force, and visual cursor feedback during the `Adaptation` (`AD`) block; always inspect the NWB trial table epoch column before training stationary kinematic decoders!
  2. **Null-Space Preparatory Activity During Instructed Delays**: During center-hold / delay periods prior to the `Go` cue, `PMd` and `M1` evolve along output-null preparatory dimensions while hand velocity is strictly zero (`0 cm/s`)—include delay intervals in training windows so decoders learn output-null orthogonality.

## 4. Programmatic Download & Quickstart
```bash
# Download standardized NWB macaque M1/PMd reaching sessions from DANDI
uvx dandi download DANDI:000688
```

## 5. Verified Primary References
- **`perich2018rapid`**: Perich, M. G., Gallego, J. Á., & Miller, L. E. (2018). *A Neural Population Mechanism for Rapid Learning*. Neuron (`10.1016/j.neuron.2018.09.030`).
- **`gallego2020longterm`**: Gallego, J. Á., Perich, M. G., Chowdhury, R. H., Solla, S. A., & Miller, L. E. (2020). *Long-term stability of cortical population dynamics underlying consistent behavior*. Nature Neuroscience (`10.1038/s41593-019-0555-4`).
- **`azabou2023poyo`**: Azabou, M., Arora, V., Ganesh, V., Mao, X., Nachimuthu, S., Mendelson, M., et al. (2023). *A Unified, Scalable Framework for Neural Population Decoding*. NeurIPS (`arXiv:2310.16046`).
