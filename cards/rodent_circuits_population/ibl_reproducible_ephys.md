# IBL Multi-Lab Reproducible Electrophysiology Repeated-Site Benchmark (`IBL-Repro`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Provides computational neuroscience's **only large-scale, 10-laboratory ground-truth replicate cohort at the exact same stereotaxic brain trajectory** (`International Brain Laboratory / Banga et al., eLife, 2024/2025`), alongside the companion multi-lab behavioral reproducibility benchmark (`DANDI:000045`, `Aguillon-Rodriguez et al., eLife, 2021`).
- **Why `IBL-Repro` Is Distinct from `IBL-BWM` (`ibl_brain_wide_map`)**:
  - **`ibl_brain_wide_map` (`Nature 2025`)** tiles the *entire* brain sparsely (`~2+` insertions per region across `279` areas) for whole-brain functional cartography.
  - **`ibl_reproducible_ephys` (`eLife 2024/2025`, `paper-reproducible-ephys`)** concentrates **`121` independent probe insertions (`82` passing full `RIGOR` QC) across `10` laboratories** onto **one single standardized trajectory** (`AP −2.0 mm`, `ML −2.24 mm`, `4.0 mm` depth at `15°` coronal angle) simultaneously traversing **5 benchmark regions**: anterior visual / posterior parietal cortex (`VISa/PPC`), hippocampal `CA1`, dentate gyrus (`DG`), lateral posterior thalamus (`LP`), and posterior thalamic nucleus (`PO`). This dense `~8–12×/lab` replication makes `IBL-Repro` the premier benchmark for **multi-session stitching (`POYO`, `NDT2`, `CEBRA`, `LFADS`), cross-animal alignment, and institutional batch-effect auditing**.

## 2. Recording Specifications & Preprocessing
- **RIGOR Standardization**: Identical Neuropixels 1.0 hardware, `pykilosort` spike sorting, `IBL-allen` lasing/serial-section two-photon tomography `CCFv3` registration, `3`-camera infrared video (`60 Hz` left/body, `150 Hz` right face), wheel rotary encoder, and standardized `2AFC` visual contrast + `80:20` block-prior decision task.
- **Exact Repository Mapping**:
  1. **Repeated-Site Electrophysiology (`121` sessions / `82` QC-passing)**: Stored in `s3://ibl-brain-wide-map-public` and `DANDI:000409`, indexed specifically via the frozen `ONE-api` tag `2022_Q4_IBL_et_al_RepeatedSite` (and `paper-reproducible-ephys` session lists).
  2. **Behavioral Reproducibility Cohort (`DANDI:000045`, `6,615` NWB files, `~98 GB`)**: Full training-to-expert psychometric trajectories across labs (`Aguillon-Rodriguez et al., eLife, 2021`).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**:
  1. **Leave-One-Laboratory-Out (`LOLO`, `10` folds)**: Train multi-session neural foundation models or cross-animal decoders on `9` labs (`~74` sessions) and test zero-shot or few-shot readout alignment on the held-out `10th` lab.
  2. **Lab-Identity Adversarial / Permutation Audit**: Test whether learned session embeddings predict `laboratory_id` above chance (`permutation test permuting mouse-to-lab assignments`, NEVER permuting neurons within the same mouse!).
- **Critical Modeling Pitfalls**:
  1. **Permute Mice, Never Neurons, When Testing Lab Effects**: Neurons recorded on the same probe share animal-specific anatomy, arousal, and targeting offsets; treating neurons as independent units inflates Type-I false positives massively—always treat **insertion/mouse** as the unit of random-effects or permutation inference (`Banga et al., 2025`).
  2. **Control for Micro-Anatomical `(x, y, z)` Trajectory Offset**: Even with standardized stereotaxic surgery, physical probe tracks vary by `±250–400 µm` across animals; include exact `channels.x, y, z` `CCFv3` coordinates and `Lightning Pose` movement features in regression/encoding models before attributing regional variance to lab drift.
  3. **Use the Official `RIGOR` Filter (`82 / 121` Sessions)**: Unfiltered replicates include sessions intentionally retained to study QC failure modes (high electrical noise, missed histological targets, `<400` trials).

## 4. Programmatic Download & Quickstart
```bash
# 1. Query the exact Repeated-Site Neuropixels cohort via IBL ONE-api (zero credentials needed)
uv run --with ONE-api python -c "
from one.api import ONE
one = ONE(base_url='https://openalyx.internationalbrainlab.org', silent=True)
pids = one.search_insertions(django='session__projects__name__icontains,ibl_neuropixel_brainwide_01',
                             datasets='*2022_Q4_IBL_et_al_RepeatedSite*')
print('Repeated-Site probe insertions:', len(pids))
"

# 2. Companion multi-lab behavioral NWB dataset on DANDI (DANDI:000045)
uvx dandi ls DANDI:000045 | head -n 5
```

## 5. Verified Primary References
- **`ibl2025reproducible`**: International Brain Laboratory, Banga, K., Benson, J., Bhagat, J., et al. (2025). *Reproducibility of in vivo electrophysiological measurements in mice*. eLife, 13, RP100840 (`10.7554/elife.100840.3`).
- **`ibl2021standardized`**: The International Brain Laboratory, Aguillon-Rodriguez, V., Angelaki, D. E., et al. (2021). *Standardized and reproducible measurement of decision-making in mice*. eLife, 10, e63711 (`10.7554/elife.63711`).
