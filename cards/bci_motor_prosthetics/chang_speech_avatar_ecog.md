# UCSF High-Density Speech-Motor ECoG Multimodal Avatar Benchmark (`Chang-Speech-Avatar` / `Zenodo:8200782`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Establishes non-penetrating **high-density subdural ECoG (`253` channels, `3 mm` pitch)** as a chronically stable, multimodal neuroprosthetic interface in a participant (`BRAVO3`) with severe brainstem-stroke paralysis and anarthria (`Metzger, Littlejohn, Silva, Moses, ..., Chang, Nature, 2023`; building on `Moses et al., NEJM, 2021`).
- **Simultaneous Tri-Modal Decoding**:
  1. **Text (`78 words/min`)**: Bidirectional RNN + CTC decoding of `39` ARPABET phonemes + beam-search language-model decoding across a `1,024`-word vocabulary (`25.5%` median WER during **silent attempted speech**, `4.9%–8.2%` WER on smaller phrase sets).
  2. **Personalized Intelligible Speech Audio**: Direct ECoG-to-discrete **HuBERT speech unit** prediction synthesized through a voice-cloned HiFi-GAN vocoder personalized to the participant's pre-injury voice.
  3. **3D Orofacial Avatar Control**: Continuous prediction of `Articulatory` jaw/lip/tongue gestures and non-verbal emotional facial expressions (`happy`, `sad`, `surprised`) driving a real-time 3D digital avatar.

## 2. Recording Specifications & Preprocessing
- **Implant Geometry**: Rectangular `253-channel` high-density subdural ECoG array implanted over left **ventral sensorimotor cortex (`vSMC`)**, **precentral/inferior frontal speech motor cortex**, and **superior temporal gyrus (`STG`)** via a percutaneous pedestal connector (`ClinicalTrials.gov NCT03698149`).
- **Dual-Feature Stream (`200 Hz` downsampled to `50 Hz` / `100 Hz`)**: Artifact-rejected, common-median re-referenced ECoG decomposed into **`70–150 Hz` high-gamma analytic amplitude (`HGA`)** and **`0.3–17 Hz` low-frequency signal (`LFS`)**, block-wise $z$-scored against `30 s` sliding or rest baselines.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Access & Reproducibility**: Full PyTorch training, phoneme CTC beam-search, HuBERT unit vocoding, and avatar animation code is open-source (`UCSF-Chang-Lab-BRAVO/multimodal-decoding`), while underlying clinical trial neural recordings are archived on Zenodo (`10.5281/zenodo.8200782`) under **credentialed investigator DUA** for participant privacy protection.
- **Critical Modeling Pitfalls**:
  1. **Never Drop Low-Frequency Cortical Potentials (`LFS`)**: Dual-band `HGA + LFS` fusion consistently outperforms `HGA`-only decoding on subdural ECoG because slow motor-evoked potentials track syllable-rate jaw/lip kinematics complementary to localized gamma bursts.
  2. **Cross-Modal Target Alignment Without Patient Audio**: Because anarthric silent speech attempts produce zero acoustic output, acoustic/avatar targets must be derived from reference speaker audio/articulatory inversion aligned dynamically (e.g., via CTC/DTW) rather than naive linear time-stretching.
  3. **Chronic Stability Without Daily Recalibration**: Unlike intracortical microelectrodes subject to single-unit turnover, `3 mm` surface ECoG grids retain stable somatotopic tuning across months/years—evaluate multi-week frozen-decoder longevity alongside fine-tuned adaptation.

## 4. Programmatic Download & Quickstart
```bash
# Clone open-source multimodal ECoG decoding & speech/avatar synthesis pipeline
git clone https://github.com/UCSF-Chang-Lab-BRAVO/multimodal-decoding.git
# Submit credentialed DUA access request for BRAVO3 neural data on Zenodo:
# https://doi.org/10.5281/zenodo.8200782
```

## 5. Verified Primary References
- **`metzger2023speechavatar`**: Metzger, S. L., Littlejohn, K. T., Silva, A. B., Moses, D. A., Seaton, M. P., Wang, R., et al. (2023). *A high-performance neuroprosthesis for speech decoding and avatar control*. Nature (`10.1038/s41586-023-06443-4`).
- **`moses2021speechbci`**: Moses, D. A., Metzger, S. L., Liu, J. R., Anumanchipalli, G. K., Makin, J. G., Sun, P., et al. (2021). *Neuroprosthesis for Decoding Speech in a Paralyzed Person with Anarthria*. New England Journal of Medicine (`10.1056/nejmoa2027540`).
