# SingleWordProductionDutch-iBIDS (`OSF:nrgx6` / Verwoert et al. 2022)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: One of the most widely adopted open-access **overt speech production intracranial electrophysiology (`sEEG`)** benchmarks for direct neural speech synthesis (`Verwoert et al., Scientific Data, 2022`). Whereas classic speech neuroprosthesis studies rely on non-penetrating lateral cortical `ECoG` grids or intracortical `Utah` arrays restricted to a single clinic, `SingleWordProductionDutch-iBIDS` demonstrates speech-waveform and mel-spectrogram decoding from **volumetric stereotactic depth electrodes (`sEEG`)** sampling sulcal depths, insula, Heschl's gyrus, and deep white-matter pathways across `10` patients.
- **Task & Stimulus Design**: Each participant (`sub-01`..`sub-10`) read aloud `100` individual Dutch words and number phrases selected from the phonetic IFA corpus (`~2 s` stimulus prompt + overt articulation, `1,000` word-production trials total across the cohort), enabling direct neural-to-acoustic vocoder training (`Griffin-Lim` / `HiFi-GAN` / unit-selection synthesis).

## 2. Recording Specifications & Preprocessing
- **iBIDS & NWB Distribution (`OSF:nrgx6`)**: `1,103` total platinum-iridium `sEEG` contacts recorded on clinical Micromed SD LTM amplifiers (`1,024 Hz` or `2,048 Hz`) hardware-synchronized with `48 kHz` microphone speech audio, complete with MNI-warped 3D contact coordinates and `FreeSurfer` anatomical parcellation labels (`Desikan-Killiany` / `Destrieux`) in `*_electrodes.tsv` (plus ready-to-load `NWB` / Python baseline scripts in `GitHub:neuralinterfacinglab/SingleWordProductionDutch`).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: `10-fold` non-overlapping cross-validation (`10` test words per fold) within each patient, reporting Pearson correlation (`r`) across log-mel spectrogram bins and Mel-Cepstral Distortion (`MCD`) against chance label-swap permutations.
- **Critical Modeling Pitfalls**:
  1. **Audit Airborne Acoustic Contamination & Feedback vs. Feedforward Windows**: Overt speech synthesis models integrating simultaneous `[0, +500 ms]` high-gamma (`70–170 Hz`) mix motor efference, auditory self-hearing in `STG`, and potential piezoelectric cable microphonics (`Roussel et al., 2020`). Verify zero-lag audio-sEEG coherence (`Verwoert et al. Technical Validation`) and explicitly benchmark **causal pre-speech (`[-400, 0 ms]`)** vs. **closed-loop (`[-200, +200 ms]`)** windows!
  2. **Suppress Articulatory Jaw/Facial `EMG` via Bipolar Shaft Referencing**: Overt speaking contracts temporalis and masseter muscles (`20–200 Hz`); subtract adjacent depth contacts along each shaft (`bipolar` montage) to reject superficial cranial `EMG` pickup.
  3. **Out-of-Vocabulary Generalization**: Because each word prompt occurs once per patient (`100` unique Dutch words), `10-fold` CV inherently tests **unseen-word (`zero-shot lexical`)** acoustic synthesis!

## 4. Programmatic Download & Quickstart
```bash
# Clone open iBIDS + NWB speech sEEG archive and official synthesis baseline scripts
uvx osfclient -p nrgx6 clone ./single_word_speech_ieeg
git clone https://github.com/neuralinterfacinglab/SingleWordProductionDutch.git
```

## 5. Verified Primary References
- **`verwoert2022speech`**: Verwoert, M., Ottenhoff, M. C., Goulis, S., Colon, A., Wagner, L., Tousseyn, S., van Dijk, J. P., Kubben, P., & Herff, C. (2022). *Dataset of speech production in intracranial electroencephalography*. Scientific Data, 9, 434 (`10.1038/s41597-022-01542-9`).
