# Allen Brain Observatory: Visual Behavior (`DANDI:000711` & `DANDI:000713`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Extends the passive Allen Visual Coding survey (`allen_visual_coding`) into **goal-directed perceptual decision-making, experience-dependent novelty plasticity, and predictive-coding omission signals** (`Garrett et al., eLife, 2020`; `de Vries, Siegle & Koch, eLife, 2023`; `Garrett et al., bioRxiv, 2023`), pairing cell-type-specific multi-plane 2-photon imaging (`DANDI:000711`) and 6-probe simultaneous Neuropixels electrophysiology (`DANDI:000713`) under an identical active **Go/No-Go Visual Change Detection** paradigm.
- **Standardized Behavioral Design**:
  1. **Metronomic Flash Stream (`1.33 Hz`)**: Mice view continuous flashes (`250 ms` image ON, `500 ms` gray screen OFF) drawn from an `8`-image natural scene set (`G` = lifelong familiar; `H` = held-out novel). When image identity switches (`change` trial), licking within `[150, 750] ms` delivers water reward (`Hit`); `catch` trials hold image identity constant to measure `False Alarm` rates and criterion/$d'$.
  2. **Stochastic Stimulus Omissions (`5%`)**: On `5%` of non-change cycles, the expected `250 ms` flash is silently omitted (`extended gray screen`), isolating pure internal temporal expectation and **`VIP` interneuron ramping** signals (`Garrett et al., eLife, 2020`).
  3. **Familiar $\to$ Passive $\to$ Novel Trajectory**: Every cohort progresses across multiple days through `Familiar Active`, `Familiar Passive` (lickspout retracted), `Novel 1` (first-ever exposure to novel image set), and `Novel >1` (habituated novel) sessions.

## 2. Recording Specifications & Preprocessing
- **`Visual Behavior — Optical Physiology` (`DANDI:000711`, `~1.51 TB`, `6,015` NWB files)**: Multi-plane Dual-Beam Mesoscope (`~11 Hz` across `8` coupled cortical planes in `VISp` + `VISl`/`VISal`/`VISpm`, depths `75–375 µm`) and single-plane `31 Hz` Scientifica `2P` imaging across transgenic lines targeting **excitatory pyramidal cells (`Slc17a7-IRES2-Cre`)**, **disinhibitory `VIP` interneurons (`Vip-IRES-Cre`)**, and **dendrite-targeting `SST` interneurons (`Sst-IRES-Cre`)**, with cross-day ROI matching (`cell_specimen_id`).
- **`Visual Behavior — Neuropixels` (`DANDI:000713`, `~4.76 TB`, `4,293` NWB files)**: Up to `6` simultaneous Neuropixels 1.0 probes (`30 kHz` spikes, `2.5 kHz` LFP) recording across `VISp`, `5` higher visual areas (`VISl`, `VISrl`, `VISal`, `VISpm`, `VISam`), visual thalamus (`LGd`, `LP`), hippocampus (`CA1`, `CA3`, `DG`, `SUB`), and midbrain (`SCig`, `MRN`, `APN`) in `54` mice (`153` sessions), co-registered to **Allen CCFv3** with synchronized running speed, pupil area/gaze, and lick timestamps.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Longitudinal cross-day comparison (`Familiar` vs. `Novel 1` vs. `Novel >1` vs. `Passive`) on matched `cell_specimen_id` neurons (`2P`) or `Day 1` (`Familiar`) vs. `Day 2` (`Novel 1`) recordings in the same animal (`Neuropixels`), using contiguous within-session time-block CV for encoding/GLM fits.
- **Critical Modeling Pitfalls**:
  1. **Strictly Separate `Novel 1` from `Novel >1`**: Novelty-driven `SST` suppression, `VIP` phasic excitation, and excitatory gain shifts attenuate sharply after just a single 1-hour session (`Garrett et al., 2023`); pooling `Novel >1` into `Novel` dilutes true novelty effects.
  2. **Isolate Pre-Lick / Non-Change Windows**: Post-change activity (`>150 ms`) mixes visual change detection with motor licking and reward consumption; benchmark pure sensory and expectation coding on `unrewarded non-change` flashes (requiring `≥3` flashes after any lick/reward) and `omitted` flashes.
  3. **Apply `AllenSDK` Unit QC & `presence_ratio`**: Filter Neuropixels units via `isi_violations < 0.5`, `amplitude_cutoff < 0.1`, and `presence_ratio > 0.9` before cross-area latency or hierarchy comparisons.

## 4. Programmatic Download & Quickstart
```bash
# 1. Inspect or stream NWB files from DANDI (000711 = 2P Ophys, 000713 = Neuropixels)
uvx dandi ls DANDI:000711 | head -n 5
uvx dandi ls DANDI:000713 | head -n 5

# 2. Direct passwordless S3 access to AllenSDK metadata tables (.csv) + NWB caches
aws s3 ls --no-sign-request s3://allen-brain-observatory/visual-behavior-2p/project_metadata/
aws s3 ls --no-sign-request s3://allen-brain-observatory/visual-behavior-neuropixels/project_metadata/
```

## 5. Verified Primary References
- **`garrett2020experience`**: Garrett, M., Manavi, S., Roll, K., et al. (2020). *Experience shapes activity dynamics and stimulus coding of VIP inhibitory cells*. eLife, 9, e50340 (`10.7554/elife.50340`).
- **`devries2023sharing`**: de Vries, S. E. J., Siegle, J. H., & Koch, C. (2023). *Sharing neurophysiology data from the Allen Brain Observatory*. eLife, 12, e85550 (`10.7554/elife.85550`).
- **`garrett2023novelty`**: Garrett, M., Groblewski, P. A., Piet, A. T., et al. (2023). *Stimulus novelty uncovers coding diversity in survey of visual cortex*. bioRxiv (`10.1101/2023.02.14.528085`).
