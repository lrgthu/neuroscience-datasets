# Steinmetz, Carandini & Harris 42-Region Neuropixels Dataset (`Steinmetz-2019`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: The foundational **multi-probe brain-wide Neuropixels decision-making benchmark** (`Steinmetz, Zatka-Haas, Carandini & Harris, Nature, 2019`), recording `~30,000` neurons across `42` cortical and subcortical brain regions (`39` sessions in `10` mice, `2–3` simultaneous Neuropixels 1.0 probes per session) while head-fixed mice perform a **2AFC + No-Go visual contrast discrimination task**.
- **Task Structure (`16` Contrast Pairs + Passive Replay)**:
  1. **Active Discrimination**: Left and right Gabor gratings appear at contrasts independently drawn from `{0, 0.25, 0.5, 1.0}`. Turning the steering wheel to bring the higher-contrast grating to the center earns a water reward (`50%` random reward when `c_L == c_R > 0`); when both contrasts are zero (`c_L = c_R = 0`), mice must hold the wheel still for `1.5 s` (`No-Go`) to earn reward.
  2. **Post-Task Passive Replay (`10.6084/m9.figshare.9727895`)**: Immediately after task disengagement, visual gratings, auditory go-cue tones, and reward-valve clicks are replayed passively to dissociate pure sensory drive from action and reward expectation on the exact same sorted units.

## 2. Recording Specifications & Preprocessing
- **Format (`ALF` / `.npy` + `.tsv`)**: Distributed on Figshare in the UCL/IBL **Alyx File (`ALF`)** convention (`spikes.times.npy`, `spikes.clusters.npy`, `clusters.brainLocation.tsv`, `clusters._phy_annotation.npy`, `trials.visualStim_contrastLeft.npy`, `wheel.position.npy`, `eye.area.npy`, `licks.times.npy`), with histological electrode tracks registered to **Allen CCFv3**.
- **Anatomical Span**: Covers visual hierarchy (`VISp`, `VISl`, `VISam`, `VISpm`, `VISrl`, `LGd`, `LP`), frontal/premotor & prefrontal cortex (`MOs`, `MOp`, `ACA`, `PL`, `ILA`, `ORB`), basal ganglia (`CP`, `GPe`, `SNr`, `ACB`), midbrain (`SCs`, `SCm`, `MRN`, `PAG`), thalamus (`VPL`, `VPM`, `PO`, `MD`), and hippocampal formation (`CA1`, `CA3`, `DG`, `SUB`).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Trial-stratified `5`-fold CV across the `16` `(c_L, c_R)` conditions (or contiguous trial blocks when modeling slow pre-stimulus engagement state), paired with cross-session / cross-animal generalization across the `39` sessions.
- **Critical Modeling Pitfalls**:
  1. **Deconfound Non-Specific Action Initiation from Signed Choice**: Almost every recorded brain region exhibits a bilateral firing burst around movement onset (`Go` vs. `No-Go`). True lateralized pre-movement choice coding (`Left` vs. `Right` wheel turn) is much sparser and localized to `MOs`, `CP`, `SNr`, `SCm`, and `MRN`—use reduced-rank kernel regression (`Steinmetz et al. 2019`) with separate temporal kernels for visual contrast, non-specific movement onset, and signed choice direction.
  2. **Full Figshare `ALF` Archive vs. Neuromatch `.npz` Subset**: The widely used Neuromatch Academy repackaging (`steinmetz_part0..2.npz`) bins spikes at `10 ms` over `[−0.5 s, +2.0 s]` around stimulus onset and drops `MUA` metadata, raw `30 kHz` spike times, inter-trial intervals, and passive replay; use the primary Figshare `ALF` archive (`9598406` + `9727895`) for point-process, millisecond-lag, or state-space research.
  3. **Unit Quality Filtering**: Filter by `clusters._phy_annotation >= 2` to retain curated single units and exclude noise/artifact clusters.

## 4. Programmatic Download & Quickstart
```bash
# Inspect and stream Figshare ALF archive metadata (Article ID 9598406) via Figshare REST API
python3 -c "
import json, urllib.request
with urllib.request.urlopen('https://api.figshare.com/v2/articles/9598406') as r:
    meta = json.load(r)
print(meta['title'], '| files:', len(meta['files']))
for f in meta['files'][:5]:
    print(' -', f['name'], round(f['size'] / 1e6, 1), 'MB')
"
```

## 5. Verified Primary References
- **`steinmetz2019distributed`**: Steinmetz, N. A., Zatka-Haas, P., Carandini, M., & Harris, K. D. (2019). *Distributed coding of choice, action, and engagement across the mouse brain*. Nature, 576, 266–273 (`10.1038/s41586-019-1787-x`).
