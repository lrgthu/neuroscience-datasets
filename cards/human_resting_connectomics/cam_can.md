# Cam-CAN Lifespan Multimodal Repository (`Cam-CAN` · `Ages 18–88`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Uniquely samples the **entire healthy adult lifespan (`ages 18–88`, ~100 participants per decade, `N = 653`)** with **both `3T` MRI/fMRI AND `306`-channel MEG** in the exact same individuals (`Shafto et al., BMC Neurology, 2014`; `Taylor et al., NeuroImage, 2015/2017`). Serves simultaneously as:
  1. The flagship pretraining corpus for **continuous MEG foundation models** (`MEG-GPT`, `BrainOmni`),
  2. The canonical benchmark for **naturalistic event segmentation across aging** (`8-min` edited Alfred Hitchcock suspense film *Bang! You're Dead*, `Campbell et al. / Ben-Yakov & Henson`), and
  3. The gold-standard testbed for **decoupling vascular aging from electrophysiological neural aging**.

## 2. Recording Specifications & Preprocessing
- **MRI (`3T` Siemens Trio)**: `T1w`, `T2w`, `Magnetization Transfer (MT)`, `Diffusion Kurtosis Imaging (DKI)`, `rfMRI` (`8 min 40 s`, `TR = 1.97 s`), audiovisual sensorimotor task, and **5-echo multi-echo `Movie` fMRI** (`8 min`, `TR = 2.47 s`).
- **MEG (`306`-ch Elekta Neuromag VectorView, `1,000 Hz`)**: `~9 min` resting-state, passive audio-visual, and active sensorimotor tasks with continuous head-position indicator (`cHPI`) coils (`MaxFilter` `tSSS` cleaned BIDS).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Critical Modeling Pitfalls**:
  1. **Vascular vs. Neural Aging Confound**: Never attribute BOLD amplitude/connectivity changes across `18 → 88` years purely to neural computation without controlling for vascular reactivity (`RSFA`) or verifying preservation/change in the paired `MEG` oscillatory bands.
  2. **Magnetometer vs. Planar Gradiometer Unit Scaling**: In `306-ch` Elekta MEG, magnetometers (`~10^-12 T`) and gradiometers (`~10^-11 T/m`) differ by $\sim 10\text{–}100\times$ in numeric units—apply noise-covariance spatial whitening (`mne.Evoked/Raw` whitening) or separate sensor-type projections.

## 4. Programmatic Download & Quickstart
```bash
# Request BIDS archive access via MRC CBU Cam-CAN portal (supported directly in mne-bids)
open "https://camcan-archive.mrc-cbu.cam.ac.uk/dataaccess/"
```

## 5. Verified Primary References
- **`taylor2015camcan`**: Taylor, J. R., Williams, N., Cusack, R., et al. (2015/2017). *The Cambridge Centre for Ageing and Neuroscience (Cam-CAN) data repository: Structural and functional MRI, MEG, and cognitive data from a cross-sectional adult lifespan sample*. NeuroImage (`10.1016/j.neuroimage.2015.09.018`).
- **`shafto2014camcan`**: Shafto, M. A., Tyler, L. K., Dixon, M., et al. (2014). *The Cambridge Centre for Ageing and Neuroscience (Cam-CAN) study protocol: a cross-sectional, lifespan, multidisciplinary examination of healthy cognitive ageing*. BMC Neurology (`10.1186/s12883-014-0204-1`).
