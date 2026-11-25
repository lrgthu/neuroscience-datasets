# Alljoined1 & Alljoined-1.6M (`NSD` & `THINGS` Million-Trial Visual EEG)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Provides two complementary large-scale visual EEG resources explicitly linked to **NSD (`MS-COCO`)** and **THINGS**:
  1. **`Alljoined1` (`Xu et al., arXiv:2404.05553`)**: `8` participants recorded on research-grade `64`-channel BioSemi ActiveTwo (`512 Hz`, `300 ms` image + `300 ms` blank + jitter) viewing NSD/`shared1000` natural scenes (`>46,000` clean epochs), enabling direct stimulus-matched **7T NSD fMRI ↔ 64-ch EEG** spatiotemporal fusion.
  2. **`Alljoined-1.6M` (`Xu et al., arXiv:2508.18571`)**: Scales to **`>1.67 million` trials across `20` participants** (`~83,000+` trials and multiple sessions per participant) viewing **THINGS** stimuli on an affordable `32`-channel saline/gel wet-electrode headset (`256 Hz`), testing whether million-trial data scaling compensates for consumer BCI sensor noise.

## 2. Recording Specifications & Preprocessing
- **Format**: Hosted openly on Hugging Face (`Alljoined/Alljoined-1.6M`) with both raw `.edf`/`.bdf` recordings and epoched Parquet/tensor splits mapped directly to `THINGS` concept IDs and `NSD/COCO` IDs.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Strictly align with `THINGS-EEG2`'s `1,654` training concepts / `200` disjoint zero-shot test concepts (in `Alljoined-1.6M`) or held-out `shared1000` scenes (in `Alljoined1`).
- **Critical Modeling Pitfalls**:
  1. **Hardware Impedance & Motion Artifacts**: Consumer `32-ch` recordings exhibit higher electrode drift and blink/muscle artifacts across multi-hour sessions than shielded `64-ch` lab caps—session-wise channel standardization and bad-epoch rejection are essential.
  2. **Wireless Trigger Jitter Calibration**: Hardware photodiode/trigger latency alignment must be respected when comparing ERP peak latencies (`P100 / N170`) against wired `THINGS-EEG1/EEG2` benchmarks.

## 4. Programmatic Download & Quickstart
```bash
# Inspect and pull metadata / shards from Hugging Face
uvx --from huggingface_hub hf download Alljoined/Alljoined-1.6M README.md --repo-type dataset
```

## 5. Verified Primary References
- **`xu2025alljoined16m`**: Xu, J., Nunes, U. B., Jiang, W., Ryther, S., Pringle, J., Scotti, P. S., Delorme, A., & Kneeland, R. (2025). *Alljoined-1.6M: A Million-Trial EEG-Image Dataset for Evaluating Affordable Brain-Computer Interfaces*. arXiv (`arXiv:2508.18571`).
- **`xu2024alljoined1`**: Xu, J., Aristimunha, B., Feucht, M. E., et al. (2024). *Alljoined1 — A dataset for EEG-to-Image decoding*. arXiv (`arXiv:2404.05553`).
