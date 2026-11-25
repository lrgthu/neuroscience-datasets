# Fedorenko Cortical ECoG Sentence Meaning Benchmark (`Fedorenko et al., PNAS 2016`)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Provided direct human intracranial (`ECoG`) evidence that broadband high-gamma (`70–170 Hz`) activity across frontotemporal language cortex exhibits a **monotonic sentence-long build-up** exclusively when words compose into coherent sentence meaning—remaining flat or weaker for unstructured word lists, syntactic-only Jabberwocky sentences, and nonword lists (`Fedorenko et al., PNAS, 2016`). Serves as the canonical intracranial electrophysiology benchmark in `Schrimpf et al. (PNAS, 2021)` and `Brain-Score Language` (`Fedorenko2016.ecog`).
- **Four-Condition 2×2 Psycholinguistic Design**: `8`-word (or `12`-word) sequences presented word-by-word via RSVP (`450 ms` or `700 ms` per word) crossing **Lexical Content (`±`)** × **Syntactic Structure (`±`)**:
  1. **Sentences (`+Lex, +Syn`)**
  2. **Word Lists (`+Lex, -Syn`)**
  3. **Jabberwocky (`-Lex, +Syn`)**
  4. **Nonword Lists (`-Lex, -Syn`)**

## 2. Recording Specifications & Preprocessing
- **Subdural Grid Acquisition**: `6` medication-resistant epilepsy patients at Albany Medical Center (`g.USBamp` amplifiers, `1,200 Hz`, subdural platinum-iridium grids). From `>600` implanted contacts, **`97` language-selective electrodes** (`5` subjects with full `52`-sentence × `8`-word = `416`-token coverage in the standardized `Brain-Score` assembly) were identified via an independent `Sentences > Nonword-Lists` screen using Hilbert-analytic `70–170 Hz` high-gamma envelopes (`z`-scored per block and averaged per word window).

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: `5-fold` cross-validation grouped strictly by `sentence_id` across the `52` eight-word sentences (`Schrimpf et al., 2021`), normalized against each electrode's split-half / cross-patient ceiling.
- **Critical Modeling Pitfalls**:
  1. **De-Confound the `1..8` Positional Ramp**: Untrained or randomly initialized transformers with causal attention masks naturally accumulate activation variance from token `1` to token `8` (`Schrimpf et al., 2021`; `Kauf et al., 2024`), mimicking the ECoG build-up curve! Always verify that your model explains **within-position, across-sentence variance** (regressing out one-hot or linear word position `1..8`) and reproduces the `Sentences > Word-Lists > Jabberwocky > Nonwords` ordering.
  2. **Strict Sentence-Grouped Splits**: Splitting the `416` word tokens randomly leaks `7/8` of every test sentence's recurrent context and neural slow-wave state into training.
  3. **Clinical Raw Waveform Scope**: Preprocessed word-level high-gamma assemblies (`xarray`/`netCDF` via `brainscore_language`) are openly downloadable; un-epoch-averaged raw clinical voltage files require IRB coordination with the authors.

## 4. Programmatic Download & Quickstart
```bash
# Load the standardized 97-electrode x 416-word ECoG assembly via Brain-Score Language
uv run --with brainscore_language python -c "
from brainscore_language import load_dataset
assembly = load_dataset('Fedorenko2016.ecog')
print(assembly.shape, assembly.dims)
"
```

## 5. Verified Primary References
- **`fedorenko2016neural`**: Fedorenko, E. G., Scott, T. L., Brunner, P., Coon, W. G., Pritchett, B., Schalk, G., & Kanwisher, N. (2016). *Neural correlate of the construction of sentence meaning*. Proceedings of the National Academy of Sciences, 113(41), E6256–E6262 (`10.1073/pnas.1612132113`).
- **`schrimpf2021neural`**: Schrimpf, M., Blank, I. A., Tuckute, G., Kauf, C., Hosseini, E. A., Kanwisher, N., Tenenbaum, J. B., & Fedorenko, E. G. (2021). *The neural architecture of language: Integrative modeling converges on predictive processing*. Proceedings of the National Academy of Sciences, 118(45), e2105646118 (`10.1073/pnas.2105646118`).
