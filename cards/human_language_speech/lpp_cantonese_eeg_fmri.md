# Le Petit Prince Hong Kong (`LPPHK` · `ds004718` / Momenian et al. 2024)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Extends the multilingual *Le Petit Prince* (`LPP`) neurolinguistic ecosystem (`Li et al., 2022`, `ds003643`) along **three previously missing axes simultaneously** (`Momenian et al., Scientific Data, 2024`):
  1. **Healthy Cognitive Aging**: `52` older native speakers (`65–78` years, mean `69.12 ± 3.52` yr; `40` female, `12` male), addressing the severe young-undergraduate skew of NLP-brain benchmarks.
  2. **Complex Lexical-Tone Typology (Hong Kong Cantonese)**: `6` contrastive lexical tones (`jyutping` / character-level alignments), testing tonal vs. intonational pitch dissociation beyond 4-tone Mandarin and non-tonal Indo-European languages.
  3. **Paired Within-Subject `3T fMRI` + `64-Ch EEG` + Cognitive Battery**: Every participant completed task fMRI, resting-state fMRI, structural `T1w` MRI, `64`-channel scalp EEG, and executive/linguistic assessments (`LHQ3`, digit span, Flanker inhibitory control, verbal fluency, and picture naming).

## 2. Recording Specifications & Preprocessing
- **Multimodal BIDS Archive (`OpenNeuro:ds004718`)**: `3T` Siemens MAGNETOM Prisma whole-brain functional (`4` Cantonese audiobook sections totaling `~20 minutes`) and resting-state EPI + `T1w` MPRAGE (`TR = 2,500 ms`), paired with `64`-channel EEG time-locked to the identical `4` Cantonese story sections, preprocessed derivatives, acoustic `F0`/intensity envelopes, and word/character tokenization tables.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: `4-fold` leave-one-run-out across the `4` story sections (`run-1`..`run-4`) with `>=20 s` fMRI boundary trims, or cross-age / cross-Sinitic transfer against young Mandarin `LPP` (`ds003643`, `N = 35`) at matched sentence boundaries.
- **Critical Modeling Pitfalls**:
  1. **Disentangle Vascular Aging from Neural Aging Using Paired EEG**: Cerebral arterial stiffening in adults aged `65+` alters BOLD `HRF` peak latency and SNR; cross-check any putative age-related drop in LLM alignment on the **paired within-subject `64`-ch EEG** and use flexible `FIR` (`0–12 s`) bases in fMRI!
  2. **Cantonese Word Segmentation & 6-Tone Pitch Controls**: Written Chinese lacks spaces and Cantonese spoken syntax/particles (`句末助词`) differ markedly from书面 Mandarin; use Cantonese-specific tokenizers/forced alignments provided in `ds004718` and include `F0` + acoustic envelope nuisance features.
  3. **Cross-Visit Story Repetition**: Account for modality session order (`fMRI` first vs. `EEG` first) when comparing predictive surprisal effects across the two visits.

## 4. Programmatic Download & Quickstart
```bash
# Install complete multimodal fMRI + EEG + behavioral BIDS repository from OpenNeuro
datalad install https://github.com/OpenNeuroDatasets/ds004718.git
```

## 5. Verified Primary References
- **`momenian2024lpphk`**: Momenian, M., Ma, Z., Wu, S., Wang, C., Brennan, J., Hale, J., Meyer, L., & Li, J. (2024). *Le Petit Prince Hong Kong (LPPHK): Naturalistic fMRI and EEG data from older Cantonese speakers*. Scientific Data, 11, 991 (`10.1038/s41597-024-03745-8`).
- **`li2022lpp`**: Li, J., Bhattasali, S., Zhang, S., Franzluebbers, B., Luh, W.-M., Spreng, R. N., Brennan, J., Yang, Y., Pallier, C., & Hale, J. (2022). *Le Petit Prince multilingual naturalistic fMRI corpus*. Scientific Data, 9, 530 (`10.1038/s41597-022-01625-7`).
