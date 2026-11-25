# Princeton *Sherlock* Movie & Spoken Free-Recall fMRI (`Sherlock`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Published by `Chen et al. (Nature Neuroscience, 2017)` and extended by `Baldassano et al. (Neuron, 2017)`, **Sherlock** (`OpenNeuro:ds001132`) is the landmark benchmark for **cortico-hippocampal narrative event segmentation**, **perception-to-recall memory reinstatement**, and **LLM episodic memory alignment**.
- **Stimulus Design & Timing**:
  - **Movie Viewing (`2` runs, `~48 min` total)**: Subjects watched the first `48` minutes of BBC's *Sherlock* Series 1 Episode 1 (*"A Study in Pink"*), split into Part 1 (`~23 min`, `946` movie TRs) and Part 2 (`~25 min`, `1,030` movie TRs), segmented by human raters into **`48–50` discrete narrative scenes** with rich second-by-second visual, semantic, character, location, and transcript annotations.
  - **Uncued Spoken Free Recall (`1` continuous scan, `10–45 min`)**: Immediately afterward, subjects verbally recounted the plot from memory in chronological detail into an optical noise-canceling microphone while fMRI continued without visual cues.
- **Subject Cohort**: `17` healthy English-speaking participants (`N = 17` in Princeton DataSpace; `N = 16` in `OpenNeuro:ds001132` after excluding one participant missing terminal movie TRs).

## 2. Recording Specifications & Preprocessing
- **Acquisition Hardware & Resolution**: `3T` Siemens Skyra (Princeton Neuroscience Institute), `20`-channel head coil, whole-brain T2*-weighted EPI at `3.0 × 3.0 × 4.0 mm` (resampled to `3.0 mm` isotropic MNI152; `TR = 1.5 s`, `TE = 28 ms`, flip angle `64°`).
- **Released Derivatives**: Raw BIDS volumes (`ds001132`), MNI-normalized/detrended `.mat`/NIfTI time-series (`Princeton DataSpace`), timestamped spoken recall transcripts mapped onto the `50` canonical movie scenes, and Hidden Markov Model (`BrainIAK` EventSegment) tutorials.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Protocols**:
  1. **Temporal / Narrative Split**: Fit Shared Response Models (`SRM`) or LLM/VLM encoding weights on Part 1 (`scenes 1–26`, `946` TRs) and evaluate on Part 2 (`scenes 27–50`, `1,030` TRs), and vice versa.
  2. **Perception → Recall Reinstatement**: Correlate `[50 × V]` scene-averaged movie perception patterns with `[50 × V]` scene-averaged spoken recall patterns within and across subjects (`PMC`, `angular gyrus`, `mPFC`).
- **Critical Modeling Pitfalls**:
  1. **Strip Pre-Movie Cartoon TRs**: Both movie runs start with a `~30 s` (`20 TRs`) *Let's All Go to the Lobby* warmup clip to absorb scanner onset transients; verify exact `1,976`-TR alignment against official scene boundary tables before fitting encoding or HMM boundary models.
  2. **`N = 16` (`ds001132`) vs. `N = 17` (`DataSpace`)**: Always report which cohort count is evaluated when comparing numerical ISC or recall identification accuracy against 2017 benchmarks.
  3. **Overt Speech Motion**: Free-recall scans contain continuous vocalization; apply nuisance regression (6-DOF motion + derivatives + CSF/WM CompCor) and evaluate on temporal scene averages rather than unsmoothed single TRs.

## 4. Programmatic Download & Quickstart
```bash
# Install BIDS dataset (N=16 complete subjects) from OpenNeuro via DataLad
datalad install https://github.com/OpenNeuroDatasets/ds001132.git

# Or fetch preprocessed MNI scene matrices & transcripts from Princeton DataSpace / BrainIAK
aws s3 ls --no-sign-request s3://openneuro.org/ds001132/
```

## 5. Verified Primary References
- **`chen2017sherlock`**: Chen, J., Leong, Y. C., Honey, C. J., Yong, C. H., Norman, K. A., & Hasson, U. (2017). *Shared memories reveal shared structure in neural activity across individuals*. Nature Neuroscience (`10.1038/nn.4450`).
- **`baldassano2017events`**: Baldassano, C., Chen, J., Zadbood, A., Pillow, J. W., Hasson, U., & Norman, K. A. (2017). *Discovering event structure in continuous narrative perception and memory*. Neuron (`10.1016/j.neuron.2017.06.041`).
