# International Brain Laboratory Brain-Wide Map (`IBL-BWM` / `DANDI:000409`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: The most comprehensive **brain-wide single-spike map during cognitive behavior** (`IBL et al., Nature, 2025`), coordinating `12` laboratories to record `699` Neuropixels probe insertions (`>620,000` neurons across `279` Allen CCFv3 brain regions in `139` mice) performing a standardized `2AFC` steering-wheel task combining **graded visual contrast (`0%, 6.25%, 12.5%, 25%, 100%`)** with **hidden-state block prior probabilities (`80:20` vs. `20:80` left/right blocks)**, followed by a **passive sensory replay** block.

## 2. Recording Specifications & Preprocessing
- **Access Modes**:
  1. **`ONE-api` (`ONE(base_url='https://openalyx.internationalbrainlab.org')`)**: Selective lazy-loading of single-session spike trains, `clusters.metrics` (`IBL QC`), `trials` tables, `wheel`, and `Lightning Pose` keypoints in seconds without downloading `50 TB`.
  2. **`DANDI:000409`**: Full standardized NWB files (`~50 TB` total, streamable via `remfile`/`fsspec`).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Block-structured CV + session/animal generalization.
- **Critical Modeling Pitfalls**:
  1. **Mandatory Pseudosession Null Distribution for Block Priors**: Because both neural baseline drift and the `80/20` block prior evolve slowly over tens of trials, naive $t$-tests or trial-shuffled permutations yield massive false-positive rates (`>40%` at $\alpha = 0.05$!). Always compute null distributions against **uncorrelated synthetic pseudosessions** generated from the exact IBL block-switching Markov rule.
  2. **Use `clusters.label == 1`**: Official IBL unit QC (`slidingRefractoryPeriod`, `amp_median`, `noise_cutoff`) is precomputed in `clusters.metrics.pqt`.
  3. **Exploit the Passive Replay Period**: Every session ends with task-disengaged replay of gratings/clicks/valve sounds—ideal internal control for isolating sensory responses from choice/movement signals.

## 4. Programmatic Download & Quickstart
```bash
# Passwordless query via official ONE-api (streams from AWS S3 ibl-brain-wide-map-public)
uv run --with ONE-api python -c "
from one.api import ONE
one = ONE(base_url='https://openalyx.internationalbrainlab.org', silent=True)
eids = one.search(project='ibl_neuropixel_brainwide_01')
print(f'Found {len(eids)} Brain-Wide Map sessions')
"
```

## 5. Verified Primary References
- **`ibl2025brainwidemap`**: International Brain Laboratory, Meshulam, L., Angelaki, D. E., et al. (2025). *A brain-wide map of neural activity during complex behaviour*. Nature (`10.1038/s41586-025-09235-0`).
