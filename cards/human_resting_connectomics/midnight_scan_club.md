# Midnight Scan Club (`MSC` · `ds000224` · Gordon et al. *Neuron* 2017)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Launched the **Precision Functional Mapping (`PFM`)** movement (`Gordon et al., Neuron, 2017`), proving that topological network variants previously dismissed as "group-average noise" are in fact **stable, idiosyncratic, task-aligned anatomical features of individual human brains** once `>60–150 minutes` of clean fMRI are collected per person.
- **Per-Subject Protocol (`N = 10`, `MSC01–MSC10`)**: `10` functional sessions (`30 min` rs-fMRI + motor, incidental memory, Glass/dot visual coherence, and noun/verb semantic cue-switching tasks per session) + `4` `T1w` + `4` `T2w` + `MRA/MRV` vascular scans (explicitly mapping large draining veins!).

## 2. Recording Specifications & Preprocessing
- **Derivatives Included in `ds000224`**: Surface-mapped `32k fsLR` CIFTI timeseries (`derivatives/surface_pipeline`), temporal censoring masks (`FD < 0.2 mm`), individualized Infomap network parcellations, and neuropsychological/personality batteries.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Odd vs. Even sessions (`5` vs. `5`) or First-5 vs. Last-5 sessions (`2.5 hours` each) per individual.
- **Critical Modeling Pitfalls**:
  1. **Exclude or Flag `sub-MSC08`**: As documented in `Gordon et al. (2017)`, `MSC08` repeatedly fell asleep and moved excessively, leaving insufficient clean frames for high-precision parcellation.
  2. **Use the Included `MRV` Venograms for Vein Masking**: Large dural sinuses and pial veins create local false-positive network borders that `MSC`'s unique `MRA/MRV` angiograms allow you to mask out!

## 4. Programmatic Download & Quickstart
```bash
datalad install https://github.com/OpenNeuroDatasets/ds000224.git
```

## 5. Verified Primary References
- **`gordon2017msc`**: Gordon, E. M., Laumann, T. O., Gilmore, A. W., et al. (2017). *Precision functional mapping of individual human brains*. Neuron (`10.1016/j.neuron.2017.07.011`).
