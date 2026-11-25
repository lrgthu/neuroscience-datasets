# Stanford 128-Channel Randomized Object Category ERP EEG (`Stanford-OCED`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Published by `Kaneshiro et al. (PLOS ONE, 2015)` (`SDR:bq914sc3730`), **Stanford-OCED** is the classic dense-array (`128-channel`) visual ERP dataset demonstrating single-trial `6`-category and `72`-exemplar object decoding and millisecond-resolved Representational Similarity Analysis (`N170` / occipitotemporal hierarchy), while serving as the primary methodological control proving why **randomized trial interleaving** is mandatory in EEG decoding.
- **Stimulus Design & Timing**:
  - `72` color photographs isolated on a neutral gray background across **`6` semantic categories** (`12` exemplars/category): **Human Body (`HB`)**, **Human Face (`HF`)**, **Animal Body (`AB`)**, **Animal Face (`AF`)**, **Fruit/Vegetable (`FV`)**, and **Inanimate Object (`IO`)**.
  - Each trial presents one image centrally (`~7.0° × 6.5°`) for `500 ms` followed by a `750 ms` uniform gray screen (`1,250 ms` SOA).
  - Every subject completed `2` sessions × `3` blocks/session × `864` **fully pseudorandomized** trials/block = **`5,184` trials/subject** (`72` repeats per individual image!).
- **Subject Cohort**: `10` neurologically healthy adults (`S1–S10`).

## 2. Recording Specifications & Preprocessing
- **Acquisition Hardware & Resolution**: `128`-channel EGI HydroCel Geodesic Sensor Net (`1,000 Hz` vertex-referenced recording inside an electrically shielded room).
- **Released Derivatives (`purl.stanford.edu/bq914sc3730`)**:
  - Per-subject MATLAB `.mat` files (`S1.mat` to `S10.mat`): high-pass `1 Hz`, low-pass `25 Hz` zero-phase filtered, Infomax ICA ocular-artifact removed, converted to average reference across **`124` clean scalp electrodes**, epoched (`32` timepoints at `62.5 Hz`, `~0–500 ms` post-stimulus), with integer category (`Y`, `1–6`) and exemplar (`1–72`) labels.

## 3. Methodological Gold Standard & The Block-Design Confound Warning
> **Why `Stanford-OCED` / `THINGS-EEG` Must Be Used Instead of `EEG-ImageNet40` (`Spampinato et al., CVPR 2017`)**:
> In `Li, Johansen, Ahmed, Ilyevsky, Wilbur, Bharadwaj, & Siskind (IEEE TPAMI, 2021)`, systematic replication and re-collection revealed that `Spampinato et al. (2017)` presented all `50` images of a given ImageNet class **contiguously in a single 25-second block** without interleaving. Slow electrode impedance drift, baseline wander, and filter ringing uniquely fingerprint each `25 s` block—allowing classifiers to achieve `80–95%+` "accuracy" even on blank inter-block rest intervals while collapsing to **`~2.5%` chance** when tested on held-out blocks or randomized presentations!
> By contrast, **`Stanford-OCED`** randomizes all `72` exemplars uniformly within every block (`~29–40%` genuine single-trial `6`-way accuracy; `>65–80%` when averaging small pseudo-trials), providing an unconfounded benchmark alongside `THINGS-EEG1`, `THINGS-EEG2`, and `Alljoined`.

- **Critical Modeling Pitfalls**:
  1. **`1–25 Hz` Bandpass Ceiling**: Released `.mat` tensors are already low-pass filtered at `25 Hz` and downsampled to `62.5 Hz`; do not apply beta/gamma (`30–100 Hz`) spectral filterbanks to `S1–S10.mat`.
  2. **Segmented Gray Backgrounds**: Stimuli control mean luminance and contrast on a uniform gray field; low-level silhouette/aspect-ratio differences still drive early (`80–120 ms`) occipital ERPs before `150–220 ms` animate/face divergence.

## 4. Programmatic Download & Quickstart
```bash
# Direct unauthenticated HTTPS download of all 10 subjects from Stanford Digital Repository
for s in $(seq 1 10); do
  curl -L -O "https://stacks.stanford.edu/file/druid:bq914sc3730/S${s}.mat"
done
```

## 5. Verified Primary References
- **`kaneshiro2015stanfordeeg`**: Kaneshiro, B., Perreau Guimaraes, M., Kim, H.-S., Norcia, A. M., & Suppes, P. (2015). *A representational similarity analysis of the dynamics of object processing using single-trial EEG classification*. PLOS ONE (`10.1371/journal.pone.0135697`).
- **`li2021blockdesign`**: Li, R., Johansen, J. S., Ahmed, H., Ilyevsky, T. V., Wilbur, R. B., Bharadwaj, H. M., & Siskind, J. M. (2021). *The perils and pitfalls of block design for EEG classification experiments*. IEEE TPAMI (`10.1109/TPAMI.2020.2973153`).
