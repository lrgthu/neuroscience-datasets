# FALCON Benchmark for Few-Shot Intracortical BCI Stability (`FALCON-BCI` / `DANDI:000941–001046`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Directly targets **multi-week/multi-month neural non-stationarity**—the #1 clinical barrier preventing plug-and-play intracortical BCIs—across **five standardized NWB datasets** spanning human clinical participants, rhesus macaques, and vocalizing songbirds (`Karpowicz, Ye, ..., Pandarinath, NeurIPS Datasets & Benchmarks, 2024`):
  1. **`H1` (`DANDI:000954`, Univ. of Pittsburgh RNEL)**: Human `7-DoF` robotic arm reach-to-grasp velocity decoding (`Utah arrays`, motor/somatosensory cortex).
  2. **`H2` (`DANDI:000950`, Stanford NPTL)**: Human attempted handwriting sequence decoding (`Utah arrays`, ALS participant copy-typing sentences).
  3. **`M1` (`DANDI:000941`, Univ. of Kansas Rouse Lab)**: Macaque multi-object reach-to-grasp forelimb `EMG` decoding (`floating microelectrode arrays`, `M1-A` & `M1-B`).
  4. **`M2` (`DANDI:000953`, Univ. of Michigan Chestek Lab)**: Macaque `2-DoF` individuated index/middle-ring-small finger-group velocity decoding (`Utah arrays`).
  5. **`B1` (`DANDI:001046`, UC San Diego Gentner & Gilja Labs)**: Zebra finch (*Taeniopygia guttata*) vocal motor nucleus `RA` chronic **Neuropixels** recordings predicting continuous song spectrograms.

## 2. Recording Specifications & Preprocessing
- **Unified NWB Tokenization**: Multi-unit threshold crossings across `64–256` channels standardized into **`20 ms` (`50 Hz`)** NWB `TimeSeries` tables alongside synchronized behavioral targets (`7D`/`2D` velocities, `EMG` envelopes, character transcripts, or spectral envelopes), with `falcon-challenge` Python evaluators handling causal windowing.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Held-In vs. Held-Out Day Protocol**: Models train freely on chronological **Held-In** sessions, then adapt to **Held-Out** future days using only a tiny **`few-shot` calibration slice** (`~1–3 minutes` of labeled/unlabeled data), evaluated against both a **Zero-Shot Frozen** lower bound and a **Full-Day Supervised** upper ceiling.
- **Critical Modeling Pitfalls**:
  1. **No Transductive Leakage on Evaluation Blocks**: Do not compute session-wide mean/variance or unsupervised manifold alignment (`CycleGAN`, `NoMAD`, `CCA`) over the held-out evaluation split simultaneously; any unsupervised recalibration on test blocks must operate strictly causally or strictly on the designated `few-shot` split.
  2. **Modality-Specific Drift Dynamics**: Floating arrays (`M1`) and chronic Neuropixels (`B1`) experience sharper discrete neuron-identity shifts than chronically stabilized Utah arrays (`H1/H2/M2`); subspace-alignment methods that assume fixed linear readouts from a conserved latent ring/torus must allow day-specific input observation matrices (`POYO`, `NDT2`, `NoMAD`).

## 4. Programmatic Download & Quickstart
```bash
# Download all 5 FALCON NWB Dandisets and install official evaluator
uvx dandi download DANDI:000954 DANDI:000950 DANDI:000941 DANDI:000953 DANDI:001046
uv pip install falcon-challenge
```

## 5. Verified Primary References
- **`karpowicz2024falcon`**: Karpowicz, B. M., Ye, J., Fan, C., Tostado-Marcos, P., Rizzoglio, F., Washington, C., et al. (2024). *Few-shot Algorithms for Consistent Neural Decoding (FALCON) Benchmark*. Advances in Neural Information Processing Systems (`10.52202/079017-2439`).
- **`willett2021handwriting`**: Willett, F. R., Avansino, D. T., Hochberg, L. R., Henderson, J. M., & Shenoy, K. V. (2021). *High-performance brain-to-text communication via handwriting*. Nature (`10.1038/s41586-021-03506-2`).
