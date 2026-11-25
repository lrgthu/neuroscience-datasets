# LibriBrain & LibriBrain100 (`50–100+ Hour` Speech MEG · Oxford PNPL)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Breaks the `1–2 hour` per-subject ceiling that historically bottlenecked non-invasive speech BCIs (`Özdoğan et al., NeurIPS, 2025`; `Mantegna et al., arXiv:2608.25204` *LibriBrain100*). By recording **`>50–80 hours` in a single primary participant** plus **`>20 hours` across `32` additional participants** (`>100 hours` total) listening to *Sherlock Holmes* LibriVox audiobooks, `LibriBrain` enables log-linear neural scaling-law studies from `1 hour` to `80 hours`—analogous to invasive intracortical speech BCIs, but completely non-invasive!

## 2. Recording Specifications & Preprocessing
- **Hardware & Python Loader**: `306`-channel MEGIN Triux Neo whole-head MEG (`1,000 Hz`, preprocessed `MaxFilter` + `250 Hz` HDF5 shards hosted on Hugging Face `pnpl/LibriBrain`) with plug-and-play PyTorch `Dataset` loaders in `pip install pnpl` for **Speech vs. Silence Detection**, **Phoneme Classification**, and **Word/Segment Retrieval**.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Critical Modeling Pitfalls**:
  1. **Use `MaxFilter` Head-Position Alignment + Session Embeddings**: Over `50–100` hours spanning months, millimeter shifts in helmet position rotate sensor leadfields; combine `SSS` head-coordinate transformation with lightweight per-session affine/adapter layers.
  2. **Strict Chapter-Disjoint Splits**: Adhere strictly to `pnpl` train/val/test chapter splits to avoid sliding-window leakage across adjacent `100 ms` phonemes.

## 4. Programmatic Download & Quickstart
```bash
# Install official PyTorch loader (`pnpl`) which automatically streams/caches Hugging Face splits
uv pip install pnpl
```

## 5. Verified Primary References
- **`ozdogan2025libribrain`**: Özdoğan, M., Landau, G., Elvers, G., Jayalath, D., Somaiya, P., Mantegna, F., Woolrich, M. W., & Parker Jones, Ō. (2025). *LibriBrain: Over 50 hours of within-subject MEG to improve speech decoding methods at scale*. Advances in Neural Information Processing Systems (`10.52202/085713-0511` / `arXiv:2506.02098`).
- **`mantegna2026libribrain100`**: Mantegna, F., Jayalath, D., Elvers, G., et al. (2026). *LibriBrain100: One hundred hours of broad and deep MEG data for neural speech decoding at scale*. arXiv (`arXiv:2608.25204`).
