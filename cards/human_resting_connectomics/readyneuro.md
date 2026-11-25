# ReadyNeuro — Native-Space 22,083-Hour OpenNeuro 4D fMRI Foundation Corpus

## 1. Overview & Motivation ("The Bitter Lesson" for 4D fMRI Pretraining)

**ReadyNeuro** (Liu et al., *NeurIPS 2026 Workshop on Foundation Models for the Brain and Body*, Spotlight, `OpenReview:rLMKAJCLc1`; Sophont / MedARC) is a **`15.88 TB`**, **`CC0-1.0`** training-ready 4D volumetric fMRI corpus aggregating **`817` active OpenNeuro studies** (`~30,160` subjects packaged into **`30,222` WebDataset `.tar` shards**, **`22,083 h` of training BOLD**, and **`>1,300` distinct task labels**), accompanied by a **`500 GB` curated subset (`medarc/ReadyNeuro`, `672` studies, `672` subjects, `5,493` runs, `725 h` BOLD)** on Hugging Face and **`CortexMAE-ReadyNeuro`** (~`300M`-parameter 4D ViT-L masked autoencoder).

Whereas traditional pipelines (`fMRIPrep` + `FreeSurfer`) require `~2–5 h/subject` for cortical surface reconstruction and nonlinear template warping—making all `~37,000` usable OpenNeuro subjects prohibitively expensive (~`190–1,000` days on a 64-core server)—ReadyNeuro tests **"the bitter lesson"** for neuroimaging:
- **Minimal Native-Space Preprocessing (`~15 min/subject` on `1` CPU core, `~6 days` on `64` cores)**: Head-motion correction + **6-DOF rigid registration (`SynthMorph`)** onto a shared `2 mm` orientation grid (`MNI152NLin2009cAsym`, `97 × 115 × 97` voxels, rotating/translating each brain **without** nonlinearly deforming its native anatomy), temporal interpolation to **`1.0 s/frame` (`1.0 Hz`)**, QC filtering (`>=60%` brain coverage + grey-matter voxel floor), and run-wise per-voxel z-scoring quantized to `int8`.
- **Empirical Finding**: Controlled `HCP-YA` ablations holding subjects, ViT-L architecture, and `200k`-step schedule fixed show native-space pretraining matches nonlinear template-space pretraining within `<=1.5 pp` across all 7 `Brainmarks` tasks (even though downstream `Brainmarks` evaluation uses template-warped scans!). Scaling ReadyNeuro from `747 h` to `22,373 h` surpasses template-space `HCP-YA` on age (`57.2%`), NSD image category, and PPMI Parkinson's classification.

---

## 2. Architecture Comparison: `ReadyNeuro` vs. `Open-fMIND`

| Dimension | **ReadyNeuro (`readyneuro`)** | **Open-fMIND (`open_fmind`)** |
| :--- | :--- | :--- |
| **Spatial Representation** | **4D Native-Space Voxels** (`97×115×97` at `2 mm`, 6-DOF rigid alignment only + `bold_cortical_gm` masks + continuous mm rotary coords) | **2D Parcellated ROI Timeseries** (`fMRIPrep 25.2.3` nonlinear MNI warp projected onto `52` cortical/subcortical atlases) |
| **Released Scale** | **`817` OpenNeuro studies**, `~30,160` subjects (`30,222` shards), **`22,083 h` BOLD** (`15.88 TB` R2 + `500 GB` HF subset) | **`322` OpenNeuro studies**, `11,379` subjects (`45,731` runs), **`6,044 h` BOLD** |
| **Temporal Grid** | Resampled uniformly to **`1.0 s/frame` (`1.0 Hz`)**, run-wise z-scored `int8` + `float` `mean`/`std` | Native `RepetitionTime` preserved (`quasiraw` vs. `FD > 0.5 mm` scrubbed + `0.01–0.1 Hz` `preproc`) |
| **Best Suited For** | 4D volumetric / patch ViT foundation models (`12 mm × 4 s` cortical patches), coordinate-conditioned encoders, scaling-law studies | Graph / parcel-token transformers, functional connectome fingerprinting, fast lightweight multi-atlas experimentation |

---

## 3. Shard Layout, Splits & Programmatic Access

### A. Full `15.88 TB` Public Corpus (`Cloudflare R2`, Zero AWS Account / Egress Fees)
- **Shards (`Schema v3`)**: `30,222` subject `.tar` shards across `b0` (`openneuro-pretrain-shards-v6/train/native/`) and `b1`–`b30` (`29,256` training shards across `816` studies) plus **`b31` (`966` held-out validation shards)**. *(Note: `21` OpenNeuro studies withdrawn after the paper's `837`-study / `22,373 h` run—totaling `498` shards / `290 h`—are flagged in `manifests/corpus_manifest.tsv` and omitted from the public bucket, yielding `22,083 h` across `6` nested configs: `737`, `1,502`, `2,946`, `5,836`, `11,674`, and `22,083 h`.)*
- **Inside Each `<accession>__<subject>.tar`**:
  1. **Sample 0 (Subject Bundle)**: `1 mm` `T1w`, `.npy` geometry tar members (`bold_idx`, `bold_gm`, `bold_cortical_gm`, `bold_affine`), and demographics JSON (`age`, `sex`).
  2. **Samples `1..K` (BOLD Runs, `<subject>__func_<task>_<i>`)**: `values.npy` (`int8` array shaped `[voxels, frames]` at `1.0 s/frame`, transposed at load time), per-voxel `mean.npy` / `std.npy`, and run metadata JSON (`scale`, acquired `TR`, task).

```bash
# 1. Configure read-only Cloudflare R2 profile (`openneuro-public`, AWS CLI >= 2.13)
curl -fsS https://openneuro.sophont.med/clients/aws-setup.sh -o openneuro-aws-setup.sh
sh openneuro-aws-setup.sh
aws --profile openneuro-public s3 ls s3://openneuro/v1/
# Sync held-out validation batch b31 (skipping zero-byte *.done markers):
aws --profile openneuro-public s3 sync \
  s3://openneuro/v1/openneuro-pretrain-shards-v6-b31/ \
  ./readyneuro-b31/ --exclude '*.done'

# 2. Or download the 500 GB / 672-study HCP-decontaminated subset from Hugging Face:
uvx --from huggingface_hub hf download medarc/ReadyNeuro subset_manifest.tsv --repo-type dataset
```

---

## 4. Critical Evaluation Pitfalls & Exact Upstream-Downstream Overlap Map

1. **Exact Overlap With Major OpenNeuro Benchmarks (`corpus_manifest.tsv` Audit)**:
   Cross-checking ReadyNeuro's `manifests/corpus_manifest.tsv` confirms that `b0`–`b30` training shards **directly contain**:
   - **Vision & Multimodal Video**: `ds004192` (**THINGS-fMRI**, `train=3` — all 3 subjects!), `ds001499` (**BOLD5000**, `train=4`), `ds001506` (**DeepRecon**, `train=3`), `ds004496` (**NOD**, `train=24`), `ds004488` (**HAD**, `train=24`), `ds005165` (**BMD / Algonauts-2021**, `train=6, val=1`), `ds001132` (**Sherlock**, `train=16`), `ds000113` (**StudyForrest**, `train=10`), `ds003017` (**Budapest**, `train=22`), `ds002837` (**NNDb**, `train=68, val=3`), `ds000228` (**Partly-Cloudy**, `train=132, val=5`).
   - **Language & Speech**: `ds003020` (**UT-Speech**, `train=8` — all 8 subjects!), `ds002345` (**Narratives**, `train=273, val=12`), `ds003643` (**LPP**, `train=87, val=4`), `ds004718` (**LPPHK**, `train=38, val=5`), `ds002322` (**Alice**, `train=23`), `ds003688` (**Utrecht Film**, `train=26, val=1`).
   - **Cohorts & Deep Phenotyping**: `ds000224` (**Midnight Scan Club**, `train=9, val=1`), `ds002685`/`ds000244` (**IBC**, `train=21, val=2`), `ds002785/2790/3097` (**AOMIC**, `train=1,090, val=31`), `ds000221` (**LEMON**, `train=265, val=8`).
   - **Guardrail**: Never claim zero-shot/out-of-distribution transfer of `CortexMAE-ReadyNeuro` onto any OpenNeuro benchmark without first checking `corpus_manifest.tsv` (or training on a filtered shard list)!
2. **HCP-YA Subject & Task-Stimulus Contamination (`eval_overlap`)**:
   Four studies in the full R2 corpus are flagged in `eval_overlap`: `ds003452` (`DMCC13benchmark`, `12` train) and `ds003465` (`DMCC55B`, `48` train + `1` val, **31 of whom are actual HCP-YA participants!**), plus `ds000244` & `ds002685` (**IBC**, re-administering the HCP `task21` battery). Exclude all four if evaluating on `HCP-YA` (the `medarc/ReadyNeuro` 500 GB HF subset already excludes them).
3. **NSD `shared1000` Image Leakage in `src/readyneuro/nsd.py` (`265` Leaked Images)**:
   ReadyNeuro's NSD evaluation builder keeps `shared1000` trials held out by `Brainmarks` (`35,184 / 5,857 / 5,794` clips vs. `32,539 / 5,418 / 5,390`), causing **`265` images to appear in both train and test**. Filter on `split` in `subject_run_clips` when comparing against `Brainmarks` baseline rows!
4. **Native-Space Geometry & Heterogeneous WebDataset Loader**:
   Because brains are only 6-DOF rigidly oriented, voxel indices `(i, j, k)` are **not** anatomically homologous across individuals, and generic Hugging Face `datasets` WebDataset readers fail on mixed subject-bundle + run-sample `.tar` schemas.

---

## 5. Key Citations

- **`liu2026readyneuro`**: Liu, X. C., Lane, C., Muhammad, H., Abraham, T. M., & Scotti, P. S. (2026). *Scaling fMRI Foundation Models with Native-Space Data from Heterogeneous Public Studies*. NeurIPS 2026 Workshop on Foundation Models for the Brain and Body (Spotlight, `OpenReview:rLMKAJCLc1`).
- **`lane2026scaling`**: Lane, C., et al. (2026). *Scaling Vision Transformers for Functional MRI with Flat Maps* (`CortexMAE` & `Brainmarks`). ICML 2026 (`arXiv:2510.13768`).
- **`markiewicz2021the`**: Markiewicz, C. J., et al. (2021). *The OpenNeuro resource for sharing of neuroscience data*. *eLife*, 10, e71774 (`10.7554/elife.71774`).
- **`hoffmann2021synthmorph`**: Hoffmann, M., et al. (2021). *SynthMorph: Learning Contrast-Invariant Registration Without Acquired Images*. *IEEE TMI* (`10.1109/tmi.2021.3116879`).
