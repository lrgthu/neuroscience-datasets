# THINGS Core Database, 4.7M Odd-One-Out (`SPoSE`) & `THINGSplus`

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Anchors every neural dataset in the THINGS ecosystem (`THINGS-fMRI`, `THINGS-MEG`, `THINGS-EEG1`, `THINGS-EEG2`, `CNeuroMod-THINGS`, `Alljoined-1.6M`, and macaque `TVSD`) to a shared, densely measured **human psychological & semantic ground truth**:
  1. **THINGS Image Database (`Hebart et al., PLoS ONE, 2019`)**: `26,107` curated natural object photographs spanning `1,854` concrete, picturable American English object concepts (`>=12` exemplars/concept).
  2. **`4.70M` Odd-One-Out Behavioral Triplets & `SPoSE` (`Hebart et al., Nature Human Behaviour, 2020`; expanded in `Hebart et al., eLife, 2023`)**: `4,701,960` crowdsourced *"which object is the odd one out?"* judgments (`N = 12,340` participants), yielding `49–66` sparse, non-negative, human-nameable dimensions (`animacy`, `food`, `metallic/tool`, `round`, `water-related`, etc.) that predict human similarity choices near the behavioral noise ceiling (`~64.6%` vs `67.2%` ceiling).
  3. **`THINGSplus` (`Stoinski et al., Behavior Research Methods, 2023`)**: `53` concept-level norms (real-world size, graspability, man-made, valence, arousal, age-of-acquisition, typicality, nameability) + `1,854` license-free **CC0** public-domain images.
  4. **`THINGS-Memorability` (`Kramer, Hebart, Baker & Bainbridge, Science Advances, 2023`)**: Empirical recognition-memory hit/false-alarm memorability scores for **all `26,107` individual THINGS images** (`>1` million continuous-recognition trials across `13,946` participants).

## 2. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Noise-Ceiling Triplet Split**: Evaluate zero-shot DNN / VLM alignment (`THINGSvision`, `gLocal` transform) on the dense `48`-concept fully sampled triplet test matrix (`17,296` unique triplets × `>=20` human repeats).
- **Critical Modeling Pitfalls**:
  1. **Preventing Concept Leakage in Encoding**: `SPoSE` weights fit on all `1,854` concepts incorporate human behavioral triplets involving the `100`/`200` neural test concepts; re-fit or project out-of-sample when making strict zero-shot claims.
  2. **Separating Visual Typicality vs. Memorability in IT**: Combining `THINGS-Memorability` with `TVSD` (`IT` firing rates) and `THINGS-fMRI` separates category-prototype distance (`SPoSE` norm) from image-specific memorability gain.

## 4. Programmatic Download & Quickstart
```bash
# Inspect and download behavioral triplets, SPoSE embeddings, THINGSplus TSVs, and memorability scores
uvx osfclient -p jum2f list
# Extract aligned DNN features on THINGS via official THINGSvision toolkit:
# uv pip install thingsvision
```

## 5. Verified Primary References
- **`hebart2020spose`**: Hebart, M. N., Zheng, C. Y., Pereira, F., & Baker, C. I. (2020). *Revealing the multidimensional mental representations of natural objects underlying human similarity judgements*. Nature Human Behaviour (`10.1038/s41562-020-00951-3`).
- **`stoinski2023thingsplus`**: Stoinski, L. M., Perkuhn, J., & Hebart, M. N. (2023). *THINGSplus: New norms and metadata for the THINGS database of 1854 object concepts and 26,107 natural object images*. Behavior Research Methods (`10.3758/s13428-023-02110-8`).
- **`kramer2023memorability`**: Kramer, M. A., Hebart, M. N., Baker, C. I., & Bainbridge, W. A. (2023). *The features underlying the memorability of objects*. Science Advances (`10.1126/sciadv.add2981`).
- **`hebart2019thingsdb`**: Hebart, M. N., Dickter, A. H., Kidder, A., et al. (2019). *THINGS: A database of 1,854 object concepts and more than 26,000 naturalistic object images*. PLoS ONE (`10.1371/journal.pone.0223792`).
