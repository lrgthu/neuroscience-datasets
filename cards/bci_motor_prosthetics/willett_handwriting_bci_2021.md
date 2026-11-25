# Stanford Imagined Handwriting Brain-to-Text BCI (`Willett-Handwriting` / `Dryad:10.5061/dryad.wh70rxwmv`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Demonstrated that decoding dexterous, time-varying **attempted handwriting** from motor cortex yields dramatically more separable neural trajectories than 2D point-to-point cursor control, achieving **`90 characters/min`** online (`94.1%` raw accuracy; `>99%` with language-model autocorrect) in BrainGate2 participant `T5` (`C4` spinal cord injury) (`Willett et al., Nature, 2021`).
- **Task Components (`10.7 hours` total)**:
  1. **Continuous Sentence Copy-Writing & Free-Response**: `1,000` sentences (`~43,501` characters) across `10` multi-day sessions over a `31`-character alphabet (`a–z`, `>`, `~`, `,`, `'`, `?` representing space and punctuation).
  2. **Isolated Single-Character & Straight-Line Stroke Calibration**: Instructed-delay trials of individual characters and radial straight-line reaches enabling direct geometric comparison of neural manifold separability (`t-SNE` / time-warped `PCA`) and linear pen-tip velocity reconstruction.

## 2. Recording Specifications & Preprocessing
- **Microelectrode Arrays**: Two `96-channel` (`10 × 10`) intracortical Utah arrays (`192` channels total) chronically implanted in the **hand-knob region of left precentral gyrus (`M1`)**.
- **Binned Spike Features**: Multi-unit threshold crossings (`-4.5 × RMS`) extracted from `30 kHz` broadband signals and binned at **`10 ms` (`100 Hz`)** per session `.mat` file, bundled with block-wise mean/SD normalization statistics, prompted target strings, and online RNN decoder outputs.

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Alignment-Free Decoding & Evaluation**: Evaluated via **Character Error Rate (`CER`)** and **Word Error Rate (`WER`)** on held-out sentence blocks per session (and adopted downstream in `FALCON H2` for few-shot cross-day drift benchmarking).
- **Critical Modeling Pitfalls**:
  1. **Unlabelled Character Boundaries in paralyzed BCI**: Because `T5`'s hand is paralyzed, continuous sentence trials lack physical pen-tip coordinates or ground-truth letter-onset timestamps. Train sequence decoders either with **CTC loss** or with the two-stage **iterative forced-alignment / dynamic time-warping (`DTW`)** label-inference pipeline in `fwillett/handwritingBCI`.
  2. **Preserve `10–20 ms` Temporal Resolution**: Handwriting discriminability relies on rapid multiphasic velocity reversals within `~400–700 ms` per character; coarse temporal binning (`>50 ms`) collapses distinct letter strokes onto overlapping mean firing rates.
  3. **Day-Specific Input Layers + Synthetic Snippet Augmentation**: Splicing isolated/segmented character snippets into synthetic training sentences alongside per-day `192 × 192` linear input layers prevents overfitting on low-trial recalibration days.

## 4. Programmatic Download & Quickstart
```bash
# Download full Dryad handwriting BCI dataset (CC0-1.0) and official TensorFlow/Python code
curl -L "https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.wh70rxwmv/download" \
  -o willett_handwriting_bci_2021.zip
git clone https://github.com/fwillett/handwritingBCI.git
```

## 5. Verified Primary References
- **`willett2021handwriting`**: Willett, F. R., Avansino, D. T., Hochberg, L. R., Henderson, J. M., & Shenoy, K. V. (2021). *High-performance brain-to-text communication via handwriting*. Nature (`10.1038/s41586-021-03506-2`).
