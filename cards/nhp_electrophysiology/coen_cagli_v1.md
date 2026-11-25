# Coen-Cagli-Kohn Macaque V1 Contextual Natural Images & Gratings (`CRCNS:pvc-8` / *Nature Neuroscience* 2015)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Canonical neurophysiology benchmark for **flexible divisive normalization, surround suppression, and probabilistic center-surround inference** in primate primary visual cortex (`Coen-Cagli, Kohn & Schwartz, Nature Neuroscience, 2015`; hosted openly for registered researchers as **`CRCNS:pvc-8`**, `10.6080/K0SB43P8`).
- **Center-Surround Natural Image Design**:
  - Tests the normative prediction that V1 surround suppression is dynamically gated by statistical homogeneity between center and surround: `270` static grayscale natural image patches and synthetic/grating controls are flashed both **windowed to the classical receptive field (`1°` diameter)** and **extended across the extraclassical surround (`3°–6.7°` diameter)** (`540` natural image conditions × `20` pseudorandom repeats per session, `100 ms` ON + `200 ms` blank ISI).
  - Accompanied within every session by drifting/flashed sinusoidal gratings characterizing orientation tuning, spatial frequency, receptive-field position, and classical size-tuning curves.

## 2. Recording Specifications & Preprocessing
- **Electrophysiology**: `96`-channel Utah microelectrode arrays (`400 μm` spacing, `1 mm` electrode length) implanted in parafoveal/near-peripheral `V1` (`~2°–6°` eccentricity) across `3` sufentanil-anesthetized, paralyzed adult macaques (`10` session files: `01.mat`–`10.mat`).
- **Released Tensors**: Each `.mat` archive provides `1 ms`-binned spike trains across stimulus onset/offset windows, exact grayscale stimulus pixel arrays presented in that session, RF mapping coordinates, and single-unit vs. multi-unit waveform isolation metrics.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Group-stratified K-fold cross-validation by **base natural image index** (`270` scenes) so both the `1°` center-only condition and the `3°–6.7°` surround condition of any held-out scene are predicted purely out-of-sample; evaluate spike-count $R^2$ / Poisson log-likelihood over `[50, 150] ms` and surround modulation index (`SMI`) accuracy.
- **Critical Modeling Pitfalls**:
  1. **Strict RF-in-Window Inclusion Filter**: Because a `10 × 10` Utah array spans `~4 × 4 mm` of V1 visuotopic map, peripheral array channels have RF centers near or outside the `1°` inner aperture border. Attempting to compute surround suppression on off-center neurons conflates direct classical-RF stimulation with extraclassical modulation—filter units using the included RF center coordinates (`distance < 0.25°–0.35°`) just as in Coen-Cagli et al. (2015).
  2. **Anesthesia-Induced Shared Gain Fluctuations**: Sufentanil anesthesia eliminates eye-movement confounds (giving sub-pixel RF stability across all `20` repeats) while introducing slow global gain fluctuations (`<2 Hz` up/down states) across the Utah array—explicitly model shared multiplicative latent gain when evaluating single-trial noise correlations.
  3. **Transient vs. Sustained Surround Dynamics**: Surround gating evolves rapidly between the early feedforward transient (`50–80 ms`) and delayed horizontal/feedback suppression (`80–150 ms`); `1 ms` bin resolution enables millisecond dynamical testing beyond static rate models.

## 4. Programmatic Download & Quickstart
```bash
# Register a free academic account at https://crcns.org, then authenticate & fetch pvc-8 (.mat files 01.mat..10.mat)
# Dataset landing page & documentation: https://crcns.org/data-sets/vc/pvc-8 (DOI: 10.6080/K0SB43P8)
wget --user="$CRCNS_USER" --ask-password -r -np -nH --cut-dirs=3 \
  https://portal.nersc.gov/project/crcns/download/pvc-8/
```

## 5. Verified Primary References
- **`coencagli2015v1`**: Coen-Cagli, R., Kohn, A., & Schwartz, O. (2015). *Flexible gating of contextual influences in natural vision*. Nature Neuroscience (`10.1038/nn.4128`).
