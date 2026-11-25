# TDBRAIN (`Two-Decades Brainclinics Research Archive` · `van Dijk et al., 2022`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Solves the biggest weakness of clinical EEG corpora (extreme amplifier, montage, and protocol drift across hospitals, as in `TUH-EEG`) by releasing **`1,346` BIDS-standardized EEG sessions from `1,274` unique individuals (`ages 5–89`)** collected over `20` years (`2001–2021`) using **one strictly locked hardware/montage/instruction protocol** (`van Dijk et al., Scientific Data, 2022`).
- **Clinical & Normative Composition**:
  - Spans Major Depressive Disorder (**`MDD`, `N = 426`**), Attention-Deficit/Hyperactivity Disorder (**`ADHD`, `N = 271`**), Subjective Memory Complaints (**`SMC`, `N = 119`**), Obsessive-Compulsive Disorder (**`OCD`, `N = 75`**), tinnitus, insomnia, Parkinson's, burnout, dyslexia, and healthy controls—plus longitudinal pre/post clinical trial outcomes (`rTMS` repetitive transcranial magnetic stimulation in `MDD` and neurofeedback in `ADHD`).
  - Widely adopted as a clean clinical downstream probe for modern EEG foundation models (`LaBraM`, `EEGPT`, `BIOT`, `CBraMod`, `NeuroLM`).

## 2. Recording Specifications & Standardized Protocol
- **Hardware-Locked Acquisition (`500 Hz`, `24-bit`, DC-coupled `< 10 kΩ` impedances)**:
  - **`26` Ag/AgCl scalp electrodes** (`Compumedics Quickcap`, `10–10` international positions: `Fp1, Fp2, F7, F3, Fz, F4, F8, FC3, FCz, FC4, T7, C3, Cz, C4, T8, CP3, CPz, CP4, P7, P3, Pz, P4, P8, O1, Oz, O2`, physically referenced to `A1`/`A2` mastoids).
  - **Auxiliary Polygraphy Channels**: `4` bipolar electrooculogram (`VEOG`, `HEOG`), `ECG` (`Erbs` point heart rate), `EMG` (zygomatic/masseter muscle tone), and peripheral autonomic channels.
  - **Core Resting Paradigm**: **`2 min` Eyes-Open (`EO`)** (fixating a red dot on screen) followed immediately by **`2 min` Eyes-Closed (`EC`)**, capturing both state-invariant spectral structure and `EO → EC` Berger alpha reactivity.

## 3. Canonical Splits, Blinded Validation & Modeling Pitfalls
- **Built-In Anti-Overfitting Blind Validation Split**:
  - To combat psychiatric biomarker non-replication, Brainclinics deliberately withheld outcome/diagnostic labels (`formal_status = UNKNOWN`) on a stratified **`30%` replication holdout** of the `MDD rTMS` (`NEO-rTMS`) and `ADHD` treatment cohorts, allowing researchers to submit frozen test predictions to the maintainers for independent verification!
- **Critical Modeling Pitfalls**:
  1. **Never Treat `UNKNOWN` Rows as Healthy Controls**: In `TDBRAIN_participants_V2.tsv`, `formal_status == UNKNOWN` denotes the **blinded test set**, while `indication` vs. `formal_status` separates referral complaints from formal `DSM` diagnoses (`HEALTHY` controls are explicitly labeled!). Mis-parsing `UNKNOWN` corrupts supervised labels.
  2. **Group Splits Strictly by `participants_ID` (`1,274` Subjects vs. `1,346` Sessions)**: `72` longitudinal `ses-2`/`ses-3` follow-up visits share extreme within-person EEG biometric fingerprints (`>95%` subject re-identification accuracy)—session-level random splitting leaks identity directly into validation.
  3. **Severe Age Skew Across Indications (`ADHD` Pediatric vs. `MDD`/`SMC` Adult/Older)**: Median age in `ADHD` is markedly younger than in `MDD` or `SMC` (`50+ yr`). Because `1/f` aperiodic slope and alpha peak frequency shift dramatically from age `5` to `89`, unstratified `ADHD vs. MDD` or `Disease vs. Control` classifiers can achieve high accuracy purely via brain-age! Always evaluate against age/sex-matched subsets or include an `age + sex` baseline.
  4. **`50 Hz` European Mains & Mastoid Reference**: Recorded in the Netherlands (`50 Hz` powerline, unlike `60 Hz` in `TUH-EEG`/`HBN`); re-reference from linked mastoids to `CAR` when aligning with multi-corpus EEG foundation models.

## 4. Programmatic Download & Quickstart
```bash
# 1. Authenticate with free ORCID account and sign GDPR DUA at https://www.brainclinics.com/resources
# 2. Clone official Brainclinics preprocessing & EOG-decontamination toolkit:
git clone https://github.com/Brainclinics/TDBRAIN.git
```

## 5. Verified Primary References
- **`vandijk2022tdbrain`**: van Dijk, H., van Wingen, G., Denys, D., Olbrich, S., van Ruth, R., & Arns, M. (2022). *The two decades brainclinics research archive for insights in neurophysiology (TDBRAIN) database*. Scientific Data (`10.1038/s41597-022-01409-z`).
