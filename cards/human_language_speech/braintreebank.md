# Brain Treebank (`BrainTreebank` / NeurIPS 2024)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Bridges **multi-hour intracranial depth electrophysiology (`sEEG`, `2,048 Hz`)** and **formal computational linguistics** (`Wang, Barbu et al., NeurIPS Datasets & Benchmarks, 2024`). Provides `43.3` cumulative hours across `10` pediatric/young-adult epilepsy patients (`~4.3 hours` per subject) watching full-length Hollywood movies, paired with spectrogram-verified manual word onsets (`>223,000` words, `>38,000` sentences) and **Universal Dependencies (`UD`)** syntactic parse trees.

## 2. Recording Specifications & Preprocessing
- **Acquisition**: Clinical stereoelectroencephalography (`sEEG`) depth probes (`2,048 Hz`, `~168` contacts/patient, `~1,688` total contacts) localized to `MNI` coordinates and Desikan-Killiany / Destrieux cortical & subcortical parcels (strong coverage of deep sulcal `STS`, `insula`, `hippocampus`, `amygdala`, `STG/MTG`, and `IFG`).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Contiguous temporal chunks (`>= 5 min` blocks) within each subject's `2–4` movies, with generous guard intervals (`>= 5 s`) around split boundaries.
- **Critical Modeling Pitfalls**:
  1. **Bipolar Re-Referencing for sEEG**: Unlike surface ECoG grids, depth contacts pass through white matter and deep nuclei—apply **local bipolar referencing** (`contact[i] - contact[i+1]` along each probe shaft) and discard seizure-onset-zone (`SOZ`) or purely white-matter channels when targeting local cortical high-gamma (`70–150 Hz`).
  2. **Audiovisual Confounds in Feature Films**: Dialogue onset frequently coincides with speaker face cuts and soundtrack ducking; control for RMS audio energy and visual optical flow/cuts.

## 4. Programmatic Download & Quickstart
```bash
# Inspect and fetch subject HDF5 bundles + Universal Dependencies parse trees
open "https://braintreebank.dev/"
```

## 5. Verified Primary References
- **`wang2024braintreebank`**: Wang, C., Yaari, A., Singh, A., et al. (2024). *Brain Treebank: Large-scale intracranial recordings from naturalistic language stimuli*. Advances in Neural Information Processing Systems (`10.52202/079017-3060` / `arXiv:2411.08343`).
