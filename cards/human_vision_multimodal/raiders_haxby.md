# Haxby *Raiders of the Lost Ark* Hyperalignment fMRI (`Raiders`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Introduced by `Haxby et al. (Neuron, 2011)`, the **Raiders** dataset demonstrated that high-dimensional, fine-grained cortical representational spaces are shared across human individuals even when anatomical folding and functional topographies misalign, launching **Procrustes Hyperalignment**, **Searchlight/Connectivity Hyperalignment**, and **Shared Response Modeling (`SRM`)**.
- **Dual-Paradigm Design (`Same 11 Subjects`)**:
  1. **Naturalistic Movie (`Raiders of the Lost Ark`)**: Full `~115 min` audiovisual presentation of Steven Spielberg's *Raiders of the Lost Ark* (`1981`), split into `8` contiguous `~14–15 min` runs across `2` scanning sessions.
  2. **Controlled `7`-Category Visual Perception**: `10` slow event-related/block runs viewing static photographs of `7` categories (`female faces`, `male faces`, `monkeys`, `dogs`, `houses`, `chairs`, `shoes`) for out-of-domain between-subject MVPA evaluation.
- **Subject Cohort**: `11` healthy right-handed adults (`4` female, `7` male). *(Later Dartmouth extensions also collected a `3T` Prisma `TR=2.5 s` / `fsaverage` superset hosted via `datasets.datalad.org/labs/haxby/raiders`).*

## 2. Recording Specifications & Preprocessing
- **Acquisition Hardware & Resolution**: `3T` Philips Intera Achieva (`3.0 mm` isotropic whole-brain gradient-echo EPI, `TR = 2.5 s`, `TE = 35 ms`, flip angle `90°`, `8`-channel SENSE head coil).
- **Released Derivatives**: DataLad-tracked BIDS / PyMVPA / FreeSurfer `fsaverage` cortical surface time-series and ventral temporal (`VT`) anatomical masks (`PyMVPA`, `BrainIAK`, and `fmralign` benchmark loaders).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Gold-Standard Out-of-Domain Transfer Split**:
  - **Alignment Fit (`Domain A`)**: Fit subject-to-common-space transformations $\mathbf{R}_i$ (`\mathbf{R}_i^\top \mathbf{R}_i = \mathbf{I}`) exclusively on the `8` *Raiders* movie runs (`zero` category labels!).
  - **Downstream Test (`Domain B`)**: Apply frozen $\mathbf{R}_i$ to the `7`-category static image runs, train a linear SVM/logistic classifier on `N - 1` aligned subjects, and evaluate zero-shot accuracy on the `1` held-out target subject.
- **Noise Ceiling**: Within-subject `10`-fold leave-one-run-out classification accuracy on the `7`-category dataset serves as the individual-brain upper reference.
- **Critical Modeling Pitfalls**:
  1. **Never Leak Test-Task Variance into Alignment**: Fitting `SRM` or Procrustes matrices on the `7`-category runs (even unsupervised!) inflates small-sample geometry alignment; keep alignment strictly restricted to the independent movie runs.
  2. **Trim Inter-Run Movie Overlaps**: When benchmarking movie time-segment (`TR` window) identification across runs `1–4` vs. `5–8`, discard the `~8 TRs` (`20 s`) replayed at run transitions.

## 4. Programmatic Download & Quickstart
```bash
# Clone DataLad superdataset from HaxbyLab or DataLad central hub
datalad install https://github.com/HaxbyLab/raiders_data.git
datalad install ///labs/haxby/raiders
```

## 5. Verified Primary References
- **`haxby2011hyperalignment`**: Haxby, J. V., Guntupalli, J. S., Connolly, A. C., Halchenko, Y. O., Conroy, B. R., Gobbini, M. I., Hanke, M., & Ramadge, P. J. (2011). *A common, high-dimensional model of the representational space in human ventral temporal cortex*. Neuron (`10.1016/j.neuron.2011.08.026`).
