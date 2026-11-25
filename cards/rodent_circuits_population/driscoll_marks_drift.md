# Chronic Multi-Week Representational Drift Benchmarks (`Driscoll 2017` & `Marks-Goard 2021`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Pairs the two foundational longitudinal 2-photon calcium imaging datasets that defined **representational drift across cortical hierarchy**:
  1. **Association Cortex Cognitive Drift (`Driscoll, Pettit, Minderer, Chettih & Harvey, Cell, 2017` — `Dryad:10.5061/dryad.gqnk98sjq`)**: Tracks hundreds of `L2/3` **posterior parietal cortex (`PPC`)** neurons daily across `4–8` weeks while mice perform a learned visual-cue delayed-choice virtual T-maze task (plus novel cue-association learning), revealing continuous single-neuron tuning reorganization alongside preserved daily population Fisher information.
  2. **Primary Visual Cortex Stimulus-Dependent Drift (`Marks & Goard, Nature Communications, 2021` — `Dryad:10.25349/D9M606`)**: Tracks `~2,900+` `L2/3` **`V1` (`VISp`)** excitatory (and inhibitory) neurons weekly across `5–7` weeks (`35–49` days in `12` awake mice) viewing interleaved **full-field drifting gratings** and **naturalistic movies** within the exact same sessions—proving that `V1` orientation/direction tuning to gratings remains rock-stable over a month whereas responses to natural movies progressively drift in the very same cells!

## 2. Recording Specifications & Preprocessing
- **Driscoll et al. (`Dryad:10.5061/dryad.gqnk98sjq`)**: Chronic cranial window `2P` imaging (`GCaMP6s`) in `PPC` paired with air-supported spherical treadmill kinematics (`forward/lateral velocity`, `virtual y-position`, `heading angle`, `visual cue identity`, `left/right turn choice`), cross-day non-rigid ROI registration, and `ΔF/F` + deconvolved activity matrices across consecutive weeks.
- **Marks & Goard (`Dryad:10.25349/D9M606`)**: Chronic `10 Hz` `2P` imaging in `Thy1-GCaMP6s` (and `Gad2-NLS-mCherry` inhibitory-labeled) mice across `5–7` weekly timepoints (`Session 1..7`), presenting `12`-direction drifting gratings (`8–10` repeats) and `30 s` natural movie clips (`20–30` repeats) per session alongside infrared pupil tracking and running-wheel speed. *(Repository disambiguation note: use `Dryad:10.25349/D9M606`—`DANDI:000049` is an unrelated single-session Allen Institute `TF × SF` dataset).*

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Quantify **Lag-Dependent Generalization ($\Delta t$ Curve)**:
  - Fit ridge/logistic decoder or canonical correlation / Procrustes subspace on `Session i` (`train` fold) and evaluate on `Session j = i + Δt`, normalized by the target day's within-session split-half reliability ceiling ($\text{CC}_{\text{norm}}(\Delta t) = \text{CC}(i, j) / \sqrt{\text{CC}(i, i) \cdot \text{CC}(j, j)}$).
  - Test unsupervised **manifold alignment** (`Procrustes`, `CCA`, `Cycle-Consistent AE`, `NoMAD`) using unlabeled neural statistics on `Day j` to rescue frozen `Day 1` decoders without task labels.
- **Critical Modeling Pitfalls**:
  1. **Always Normalize by Within-Session Split-Half Reliability**: Raw cross-day tuning correlation `< 1.0` mixes true multi-day drift with finite-trial Poisson/calcium noise; dividing by $\sqrt{r_{i,\text{split}} \cdot r_{j,\text{split}}}$ isolates genuine longitudinal drift (`Δt > 0` slope).
  2. **Exploit Marks & Goard's Built-In Optical Stability Control**: Any physical `z`-drift of the focal plane would degrade *both* drifting gratings and natural movies equally within the same session; restricting to ROIs with high cross-week morphological correlation and stable grating orientation selectivity guarantees that natural-movie drift reflects circuit/recurrent reorganization rather than imaging registration error.
  3. **Kinematic Stratification in `PPC` (`Driscoll 2017`)**: `PPC` neurons multiplex spatial progress and body/ball angular velocity; regress or stratify by matched ball-velocity trajectories across weeks before measuring pure representational drift.

## 4. Programmatic Download & Quickstart
```bash
# Both datasets are released under permissive CC0-1.0 public-domain dedication on Dryad:
# 1. Driscoll et al. (2017) PPC Virtual T-Maze Drift:
curl -sLI https://doi.org/10.5061/dryad.gqnk98sjq | grep -iE "^(http|location)"

# 2. Marks & Goard (2021) V1 Gratings vs. Natural Movies Drift:
curl -sLI https://doi.org/10.25349/D9M606 | grep -iE "^(http|location)"
```

## 5. Verified Primary References
- **`driscoll2017dynamic`**: Driscoll, L. N., Pettit, N. L., Minderer, M., Chettih, S. N., & Harvey, C. D. (2017). *Dynamic reorganization of neuronal activity patterns in parietal cortex*. Cell, 170(5), 986–999.e16 (`10.1016/j.cell.2017.07.021`).
- **`marks2021stimulus`**: Marks, T. D., & Goard, M. J. (2021). *Stimulus-dependent representational drift in primary visual cortex*. Nature Communications, 12, 5169 (`10.1038/s41467-021-25436-3`).
