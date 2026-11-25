# Moser Lab Toroidal Topology Grid-Cell Neuropixels Dataset (`Gardner et al., Nature, 2022`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Delivers the first direct population-level proof that **mammalian medial entorhinal cortex (`MEC`) grid cells within an individual module evolve on a 2D continuous toroidal manifold ($\mathbb{T}^2 = S^1 \times S^1$)** with persistent homology Betti numbers $(\beta_0, \beta_1, \beta_2) = (1, 2, 1)$ (`Gardner, Hermansen, Pachitariu, Burak, Baas, Dunn, Moser & Moser, Nature, 2022`), and shows that this intrinsic continuous-attractor topology remains **intact across distinct physical environments and during `REM` and `Slow-Wave Sleep (SWS)`** when external visual/locomotor inputs are absent.
- **Four-Condition Within-Neuron Design (`Figshare:16764508`)**:
  1. **Open-Field Foraging (`OF`)**: Free exploration in a `1.5 m × 1.5 m` square arena chasing food crumbs (used for classical hexagonal `gridness` scoring and spatial module clustering).
  2. **Wagon-Wheel Track (`WW`)**: Constrained navigation on an elevated circular/radial-arm maze with altered geometry and visual landmarks.
  3. **Natural Sleep (`REM` & `SWS`)**: Multi-hour rest box recordings classified into `REM` (strong theta) and `SWS` (non-REM slow waves) via MEC LFP power ratios and head immobility.

## 2. Recording Specifications & Preprocessing
- **Subjects & Probes**: `3` freely moving **Long-Evans rats** (`rat_q`, `rat_r`, `rat_s`) implanted chronically in `MEC` / parasubiculum with **4-shank Neuropixels 2.0** (`rat_r`, `rat_s`) or **Neuropixels 1.0** (`rat_q`) silicon probes, yielding `>2,500` total sorted MEC units and **`6` large co-recorded grid modules** (`R1`, `R2`, `R3`, `Q1`, `Q2`, `S1`, containing `65` to `189` simultaneously recorded pure grid cells per module!).
- **Clean `.npz` Python Packaging**: Hosted openly on Figshare (`16764508`) as lightweight `.npz` files directly consumable by NumPy/Python (`spikes_rat_*.npz`, `tracking_rat_*.npz`, sleep state intervals, and pre-clustered module indices), paired with complete topological data analysis (`Ripser` + circular cohomology decoding) scripts in `erikher/GridCellTorus`.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Unsupervised topological inference (`Ripser` Vietoris–Rips persistent cohomology over $\mathbb{Z}_{47}$) separately within each behavioral state (`OF`, `WW`, `REM`, `SWS`), plus **cross-state manifold transfer** (tuning each neuron's 2D toroidal receptive field `(θ₁, θ₂)` in `REM`/`SWS` sleep and verifying invariant pairwise phase offsets against `Open Field` physical space).
- **Critical Modeling Pitfalls**:
  1. **Never Pool Across Grid Modules**: Rat `r` contains three distinct co-recorded spatial-scale modules (`R1`, `R2`, `R3`) on the same probe; combining `R1 + R2` creates a 4-dimensional product torus ($\mathbb{T}^2 \times \mathbb{T}^2$) where sample complexity prevents `H₂` void recovery. Always analyze one module at a time!
  2. **Normalize Global Population Rate Fluctuations**: Theta rhythm (`~8 Hz`) and `SWS` UP/DOWN states modulate total spike count across all cells simultaneously; divide each time bin's smoothed firing-rate vector by its population sum/norm (or use cosine dissimilarity after `6D` PCA projection) and apply `kNN` density filtering (`top ~15,000` dense states subsampled via `MaxMin` landmarks to `1,200` points) so noisy low-activity points do not fill the central hole of the torus.
  3. **Benchmark Against Cyclic Spike-Train Shuffles**: Always compare `H₁` (two persistent 1D loops) and `H₂` (one persistent 2D cavity) bar lengths against `≥500–1,000` independent circular time-shifted spike-train surrogates that preserve every single neuron's firing rate and temporal autocorrelation while breaking inter-neuronal phase coupling.

## 4. Programmatic Download & Quickstart
```bash
# Inspect Figshare article 16764508 (.npz files) and clone official TDA analysis pipeline
git clone https://github.com/erikher/GridCellTorus.git
python3 -c "
import json, urllib.request
with urllib.request.urlopen('https://api.figshare.com/v2/articles/16764508') as r:
    meta = json.load(r)
for f in meta['files']:
    print(f['name'], round(f['size'] / 1e6, 2), 'MB ->', f['download_url'])
"
```

## 5. Verified Primary References
- **`gardner2022toroidal`**: Gardner, R. J., Hermansen, E., Pachitariu, M., Burak, Y., Baas, N. A., Dunn, B. A., Moser, M.-B., & Moser, E. I. (2022). *Toroidal topology of population activity in grid cells*. Nature, 602, 123–128 (`10.1038/s41586-021-04268-7`).
