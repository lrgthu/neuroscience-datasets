# THINGS-EEG1 (`ds003825` · 50-Subject Rapid RSVP EEG)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Captures **population-wide (`N = 50`) millisecond visual object representations** across the entire `1,854`-concept THINGS hierarchy (`Grootswagers, Zhou, Robinson, Hebart & Carlson, Scientific Data, 2022`). Together with `THINGS-EEG2` (`N = 10` × `4` sessions), the pair forms an ideal controlled experimental design for studying **sample breadth ($N=50$ subjects) vs. per-subject depth ($4\times$ trials)** in neural decoding and foundation pretraining.
- **Stimulus Timing**: `22,248` training images (`1` repeat) + `200` test images (`12` repeats) presented in `20`-image RSVP bursts at `10 Hz` (`50 ms` image ON + `50 ms` blank screen = `100 ms` SOA; `~24,648` trials per subject in a single `~1 hour` recording).

## 2. Recording Specifications & Preprocessing
- **Hardware**: `64`-channel BrainVision actiCHamp (`1,000 Hz`, referenced to `Cz`), released in clean BIDS format on OpenNeuro (`ds003825`) with epoched `250 Hz` derivatives on OSF (`hd6zk`).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**:
  1. **Within-Subject Zero-Shot**: `22,248` train → `200` (`12`-repeat) test images.
  2. **Cross-Subject Generalization**: Train on `40` subjects, evaluate zero-shot or few-shot on `10` held-out subjects.
  3. **Group-Level Concept RSA (`1,854 × 1,854`)**: Pool single-trial concept averages across `50` subjects (`50 × 12 = 600` trials per concept!) to construct high-SNR millisecond RDMs for comparing against `TVSD` macaque V1/V4/IT and `THINGS-MEG`.
- **Critical Modeling Pitfalls**:
  1. **Do Not Mix `THINGS-EEG1` (`50 ms` ON, `12` test repeats) and `THINGS-EEG2` (`100 ms` ON, `80` test repeats)** in tables without explicit protocol tags—test-set noise ceilings are substantially higher in `EEG2` due to $80$ vs. $12$ repeats!
  2. **Remove Target-Detection Motor Epochs**: Exclude catch sequences containing inverted target stimuli so button-press readiness potentials do not contaminate late temporal windows.

## 4. Programmatic Download & Quickstart
```bash
# Clone BIDS dataset from OpenNeuro via DataLad
datalad install https://github.com/OpenNeuroDatasets/ds003825.git
```

## 5. Verified Primary References
- **`grootswagers2022thingseeg1`**: Grootswagers, T., Zhou, I., Robinson, A. K., Hebart, M. N., & Carlson, T. A. (2022). *Human EEG recordings for 1,854 concepts presented in rapid serial visual presentation streams*. Scientific Data (`10.1038/s41597-021-01102-7`).
