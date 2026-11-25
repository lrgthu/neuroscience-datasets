# Kar-DiCarlo Macaque IT Recurrent Challenge-Image Latency Benchmark (`Kar2019-OST` / *Nature Neuroscience* 2019)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Provided direct causal and millisecond-resolved population evidence that **recurrent ventral-stream circuits**—not purely feedforward sweeps—solve occluded, cluttered, scale-extreme, and naturalistic core object recognition (`Kar, Kubilius, Schmidt, Issa & DiCarlo, Nature Neuroscience, 2019`).
- **Challenge vs. Control Paradigm (`1,320` Images across `10` Object Categories)**:
  - Evaluates `1,320` photographs from **MS-COCO / natural scenes** and **synthetic 3D renders** spanning `10` basic-level categories (`bear, elephant, person, car, dog, apple, chair, plane, bird, zebra`), presented for `100 ms` (`8°` subtense) during passive fixation and active delayed-match-to-sample behavioral testing.
  - Contrasts **Feedforward-Control images** (solved equally well by AlexNet/ResNet and primates) against **Challenge images** (large behavioral performance gap where primates vastly outperform standard feedforward CNNs at matched category priors).

## 2. Recording Specifications & Preprocessing
- **Electrophysiology**: Chronic `96`-channel Utah microelectrode arrays across anterior, central, and posterior `IT` (`424` reliable IT multi-unit sites + `V4` sites in `2` awake rhesus macaques, `~30–50` trial repeats per image).
- **Object Solution Time (`OST`) Definition**: Sliding `10 ms` linear classifiers fit at every lag $t \in [70, 250]\text{ ms}$ post-onset determine the exact millisecond at which IT population linear decodability (`d'`) first reaches the monkey's behavioral `I1` accuracy for each individual image (`~30 ms` later on Challenge images than behavioral-accuracy-matched Control images).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Brain-Score `dicarlo.Kar2019-ost` Evaluation**: Maps recurrent model unrolling steps $k = 1, \dots, K$ linearly to cortical time bins (`ms`), fits cross-validated linear category decoders at each step, extracts model image-by-image `OST`, and computes noise-ceiling-normalized Spearman/Pearson correlation against macaque IT `OST`.
- **Critical Modeling Pitfalls**:
  1. **Static Models Score Undefined on `Kar2019-ost`**: Feedforward networks with a single static output step lack temporal trajectory dynamics and cannot predict image-by-image solution latency variance; evaluating recurrent architectures (`CORnet-S`, `BLT`, `Linsley hGRU`, `Koopman/SSM` vision backbones) requires exposing per-timestep hidden states.
  2. **Handle `NaN` / Right-Censored `OST` Entries Safely**: Use negated range/finiteness masks (`np.isfinite(ost)`) when computing correlations, as images whose neural trajectory never crosses the behavioral target threshold have undefined (`NaN`) solution times.
  3. **Category-Balanced Cross-Validation**: When training linear `I1` population decoders on `1,320` (`660` natural + `660` synthetic) images, stratify folds jointly by **category (`10`) × domain (`natural/synthetic`)** to avoid background-statistics bias on MS-COCO crops.

## 4. Programmatic Download & Quickstart
```bash
# Score or inspect the Kar2019 IT Object Solution Time benchmark via brainscore_vision
uv run python -c "import brainscore_vision as bsv; bench = bsv.load_benchmark('Kar2019-ost'); print(type(bench))"
```

## 5. Verified Primary References
- **`kar2019recurrent`**: Kar, K., Kubilius, J., Schmidt, K., Issa, E. B., & DiCarlo, J. J. (2019). *Evidence that recurrent circuits are critical to the ventral stream’s execution of core object recognition behavior*. Nature Neuroscience (`10.1038/s41593-019-0392-5`).
