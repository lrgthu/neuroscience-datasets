# NSD-Imagery (`7T` Mental Imagery Decoding Benchmark · CVPR 2025)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Extends the `7T` Natural Scenes Dataset from externally driven visual perception to **internally generated visual mental imagery** across **all `8` core NSD participants** (`Kneeland, Scotti, St-Yves, Breedlove, Kay & Naselaris, CVPR, 2025`). Enables rigorous testing of modern diffusion/CLIP fMRI decoders (`MindEye2`, `Brain-Diffuser`, `Takagi & Nishimoto`) without requiring massive imagery training sets.
- **Three Hierarchical Target Sets (`6` stimuli × `3` sets = `18` targets, `8` imagery repeats each)**:
  1. **`Simple`**: High-contrast geometric shapes and oriented bars (tests retinotopic low-level imagery).
  2. **`Complex`**: Naturalistic photographs (including `shared1000` scenes) and artworks memorized prior to imagery blocks.
  3. **`Conceptual`**: Open-ended object/scene word concepts imagined without a single memorized reference photograph.

## 2. Recording Specifications & Preprocessing
- **Voxel Alignment**: Co-registered directly to each participant's `func1pt8mm` and `nsdgeneral` cortical masks with `GLMsingle` single-trial betas (`nsdimagerybetas_fithrf_GLMdenoise_RR`).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Pure **perception-to-imagery cross-decoding** (train on core NSD perception trials; evaluate on z-scored, repeat-averaged NSD-Imagery trials via CLIP retrieval, PixCorr, SSIM, AlexNet-2/5, Inception, and human behavioral ratings).
- **Critical Modeling Pitfalls**:
  1. **Exclude Memorized `shared1000` Targets from Perception Training**: When evaluating `Complex` imagery targets drawn from `shared1000`, ensure your perception training split (`unique9000`) never saw those target images.
  2. **Low-Level V1 Bottleneck in Dual-Path Reconstructors**: Pixel-level VAEs trained on perception rely heavily on high-SNR V1/V2 feedforward signals that are attenuated or inverted during top-down imagery—semantic CLIP alignment generalizes substantially better than raw V1 pixel latents.
  3. **Mask Out Auditory Cortex**: Because trials use auditory cues to keep eyes closed/fixated during imagery, whole-brain masks can classify the acoustic cue word from `STG` rather than decoding visual imagery!

## 4. Programmatic Download & Quickstart
```bash
# Inspect NSD-Imagery GLMsingle betas on the public NSD AWS S3 bucket
aws s3 ls --no-sign-request s3://natural-scenes-dataset/nsddata_betas/ppdata/subj01/func1pt8mm/nsdimagerybetas_fithrf_GLMdenoise_RR/
```

## 5. Verified Primary References
- **`kneeland2025nsdimagery`**: Kneeland, R., Scotti, P. S., St-Yves, G., Breedlove, J. L., Kay, K., & Naselaris, T. (2025). *NSD-Imagery: A benchmark dataset for extending fMRI vision decoding methods to mental imagery*. CVPR (`10.1109/cvpr52734.2025.02687`).
