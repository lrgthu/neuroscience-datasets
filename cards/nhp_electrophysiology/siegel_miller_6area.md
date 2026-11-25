# Siegel-Buschman-Miller Simultaneous 6-Area Cortical Decision Hierarchy (`SiegelMiller6Area` / *Science* 2015)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Landmark **simultaneous six-area cortical recording dataset** (`MT`, `V4`, `IT`, `LIP`, `dlPFC`, `FEF` across `2` awake rhesus macaques, `2,694` multi-unit & LFP sites) tracing millisecond-by-millisecond sensorimotor transformation from dorsal/ventral visual cortex through parietal/frontal executive networks (`Siegel, Buschman & Miller, Science, 2015`).
- **Flexible Context-Dependent Categorization Task**:
  - On every trial, a visual rule cue (`2` distinct shapes per rule to control for low-level cue appearance) instructs the monkey to categorize a subsequent colored, moving random-dot patch along either **motion direction** (`up` vs. `down` across `4` directions) or **color** (`red` vs. `green` across `4` hues), followed by a binary saccadic choice (`left`/`right`).
  - Uniquely spans **dorsal visual (`MT`)**, **ventral visual (`V4`, `IT`)**, **posterior parietal (`LIP`)**, **prefrontal (`dlPFC`)**, and **oculomotor premotor (`FEF`)** stages simultaneously within the same behavioral trials—making it a premier testbed for multi-region RNNs (`mRNNs`, `CURBD`) and inter-areal Granger/subspace causality.

## 2. Recording Specifications & Preprocessing
- **Electrophysiology**: Acute custom high-density multi-electrode arrays lowered daily across `6` craniotomy chambers/targets (`dlPFC: 1,020` sites; `LIP: 807`; `FEF: 532`; `V4: 155`; `MT: 123`; `IT: 57`), capturing simultaneous broadband spikes and local field potentials (`LFP` at `1 kHz`).
- **Statistical Metric (`ω²` Bias-Corrected PEV)**: Uses debiased omega-squared (`ω²`) percentage of explained variance with permutation null baselines to prevent positive sample-size bias when tracking onset latencies of cue (`IT/V4 -> PFC/LIP`), stimulus (`MT/V4 -> LIP/FEF/PFC`), and choice (`PFC/LIP -> FEF -> MT/V4` top-down feedback).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Cross-cue rule generalization (`train on Cue Set 1`, `test on Cue Set 2`) + condition-stratified trial splits across the `32` (`2 rules × 4 motion × 4 color`) factorial stimulus-task combinations.
- **Critical Modeling Pitfalls**:
  1. **Cross-Cue Generalization Is Mandatory for Rule Subspaces**: Within a single cue shape, `V4` and `IT` appear strongly "rule-selective" immediately after cue onset purely due to visual shape tuning; true abstract task-set variance (`PFC` / `LIP` sustained delay coding) only emerges when evaluating across paired cue shapes signaling the same rule!
  2. **Subsample Equal Population Sizes Across the 6 Areas**: Naive population decoders show `PFC > LIP > FEF >> V4 > MT > IT` simply because `1,020` `dlPFC` sites were recorded versus `57` `IT` sites; always apply matched-$N$ neuron subsampling (`e.g., 50 units × 500 resamples`) and debiased `ω²`.
  3. **Eye-Movement Artifact Guard in Choice Epoch**: Saccadic execution triggers corollary discharge and retinal slip across visual areas (`MT`, `V4`, `IT`); censor or separately model windows post-saccade onset when isolating pre-saccadic choice buildup.

## 4. Programmatic Download & Quickstart
```bash
# Dataset archived at Centre for Integrative Neuroscience (University of Tübingen) & MIT Picower Miller Lab
# Inspect author manuscript & protocol metadata via MIT DSpace (request data archive via Siegel / Miller Labs):
open "https://dspace.mit.edu/handle/1721.1/102482"
```

## 5. Verified Primary References
- **`siegel2015sixarea`**: Siegel, M., Buschman, T. J., & Miller, E. K. (2015). *Cortical information flow during flexible sensorimotor decisions*. Science (`10.1126/science.aab0551`).
