# NeuroTycho Chronic 128-Channel Whole-Hemisphere Macaque ECoG Archive (`NeuroTycho-ECoG` / *PLOS ONE* 2011)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Pioneering open-science **Multidimensional Recording (`MDR`)** platform created by Naotaka Fujii's group at RIKEN Brain Science Institute (`Nagasaka, Shimoda & Fujii, PLOS ONE, 2011`, `10.1371/journal.pone.0022561`), providing **chronic, gap-free `128`-channel subdural/epidural ECoG coverage spanning an entire macaque cerebral hemisphere** (prefrontal, premotor, primary motor, somatosensory, posterior parietal, visual `V1–V4`, temporal `IT`, plus medial prefrontal/cingulate walls) over months in Japanese macaques (*Macaca fuscata*, including `Chibi`, `George`, `Su`, `Kin2`, `Kuma`).
- **Multi-Task Ecological & Perturbation Suite**:
  1. **Asynchronous 3D Food-Tracking & Reaching**: Continuous unrestrained arm reaching in 3D space tracked via `120 Hz` Vicon optical motion capture (`Shimoda et al., J. Neural Eng., 2012`), enabling multi-month asynchronous BCI stability tests without trial segmentation.
  2. **Consciousness, Sleep & Multi-Drug Anesthesia**: Paired awake (eyes-open / eyes-closed), natural sleep, and controlled induction/recovery under **propofol**, **ketamine-medetomidine**, and **isoflurane**—the canonical empirical testbed for cortical dynamical stability (`eigenvalue criticality`), integrated information (`Φ*`), and directed feedback collapse.
  3. **Visual Gratings, Auditory Oddball & Social Dyadic Interaction**: Synchronized multi-monkey social food competition, video, and eye-tracking streams.

## 2. Recording Specifications & Preprocessing
- **Custom Thin-Film Silicone/Parylene MEMS Grid**: `128` platinum disc electrodes (`0.8–1.0 mm` contact diameter, `5 mm` inter-electrode pitch) surgically implanted over lateral, medial, and ventral cortical surfaces with coregistered 2D/3D cortical X-ray/MRI electrode coordinates (`ECoG_channel` `.mat` files, `1,000 Hz` continuous `ECoGTime` + `ECoGData_ch1..ch128`).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Within-session chronological splits (`first 75%` continuous duration train / `final 25%` test with guard buffer) and **zero-recalibration longitudinal generalization** (`train Day 1`, evaluate `+7` to `+90` days later).
- **Critical Modeling Pitfalls**:
  1. **50 Hz Mains Frequency (Eastern Japan Grid)**: Unlike North American (`60 Hz`) recordings, RIKEN Wako operates on **`50 Hz` AC power**; notch-filter `50, 100, 150, 200 Hz` before extracting high-gamma (`70–150 Hz`) broadband envelopes!
  2. **Mandatory Bipolar Re-Referencing for Network/Causality Claims**: Shared reference potentials inflate whole-hemisphere synchrony; compute nearest-neighbor **bipolar derivations** (`V_i - V_j`) as established in Yanagawa et al. (2013) and Solovey et al. (2015) before estimating spectral Granger causality or autoregressive Jacobian eigenvalues.
  3. **Chewing & Facial EMG Contamination on Ventrolateral Temporal Channels**: During naturalistic food-reaching/eating tasks, jaw-muscle `EMG` bursts inject broadband (`>60 Hz`) power into inferior temporal/frontal electrodes—regress or reject mastication epochs using video/marker timestamps.

## 4. Programmatic Download & Quickstart
```bash
# Browse task-specific MATLAB (.mat) archives openly at NeuroTycho (no account required)
# MNE-Python / FieldTrip tutorial loader: https://www.fieldtriptoolbox.org/tutorial/monkey_ecog/
open "https://neurotycho.org/"
```

## 5. Verified Primary References
- **`nagasaka2011neurotycho`**: Nagasaka, Y., Shimoda, K., & Fujii, N. (2011). *Multidimensional Recording (MDR) and Data Sharing: An Ecological Open Research and Educational Platform for Neuroscience*. PLOS ONE (`10.1371/journal.pone.0022561`).
- **`shimoda2012neurotycho`**: Shimoda, K., Nagasaka, Y., Chao, Z. C., & Fujii, N. (2012). *Decoding continuous three-dimensional hand trajectories from epidural electrocorticographic signals in Japanese macaques*. Journal of Neural Engineering (`10.1088/1741-2560/9/3/036015`).
