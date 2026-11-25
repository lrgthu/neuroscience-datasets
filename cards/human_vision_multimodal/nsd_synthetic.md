# NSD-Synthetic (`7T` Out-of-Distribution Vision Benchmark)

## 1. Overview & Experimental Paradigm
- **Core Contribution**: Solves the classic **in-distribution illusion** of natural-image encoding benchmarks (`Gifford, Cichy, Naselaris & Kay, Nature Communications, 2026`). Because all `73,000` core NSD stimuli come from MS-COCO photographs, competing DNNs often tie on `shared1000` by exploiting natural-image texture/context shortcuts. **NSD-Synthetic** scans the **exact same `8` NSD subjects** (`subj01–subj08`) on **`284` parametric & synthetic OOD stimuli**—exposing sharp divergences between task-supervised, self-supervised, and VLM architectures as stimulus distance from the natural training manifold increases.
- **Stimulus Classes (`284` images)**: Spiral/Cartesian gratings, contrast/luminance sweeps, chromatic vs. achromatic natural scenes, line drawings, Mooney two-tone images, phase-scrambled/pink-noise hybrids, isolated objects, and rendered word strings.

## 2. Recording Specifications & Preprocessing
- **Exact Voxel-to-Voxel Correspondence with Core NSD**: Acquired on the identical `7T` `1.8 mm` protocol and co-registered into each participant's exact `func1pt8mm`, `func1mm`, and `fsaverage` grids using `GLMsingle` (`nsdsynthetic_betas_fithrf_GLMdenoise_RR`), allowing **zero-retraining readout transfer** from core NSD!

## 3. Canonical Splits, Noise Ceiling & Modeling Pitfalls
- **Standard Evaluation Split**: Train encoder readouts $W$ on core NSD natural images (`9,000` unique images); evaluate $\hat{Y}_{\text{syn}} = f(X_{\text{syn}}) W$ zero-shot on all `284` NSD-Synthetic conditions stratified by synthetic stimulus subclass.
- **Critical Modeling Pitfalls**:
  1. **Zero Readout Re-Fitting**: Fitting a new ridge regression inside `284` synthetic stimuli measures synthetic expressive capacity, *not* OOD generalization of the natural-scene model.
  2. **Separate Fixation vs. Memory Runs**: NSD-Synthetic interleaves central-fixation luminance-change blocks and 1-back blocks; evaluate or partial out task-condition effects when studying higher-order ventral and parietal ROIs.

## 4. Programmatic Download & Quickstart
```bash
# Inspect NSD-Synthetic stimuli and GLMsingle betas inside the public NSD AWS bucket
aws s3 ls --no-sign-request s3://natural-scenes-dataset/nsddata_stimuli/stimuli/nsdsynthetic/
aws s3 ls --no-sign-request s3://natural-scenes-dataset/nsddata_betas/ppdata/subj01/func1pt8mm/nsdsynthetic_betas_fithrf_GLMdenoise_RR/
```

## 5. Verified Primary References
- **`gifford2026nsdsynthetic`**: Gifford, A. T., Cichy, R. M., Naselaris, T., & Kay, K. (2026). *A 7T fMRI dataset of synthetic images for out-of-distribution modeling of vision*. Nature Communications (`10.1038/s41467-026-69345-9`).
- **`allen2021nsd`**: Allen, E. J., St-Yves, G., Wu, Y., et al. (2021/2022). *A massive 7T fMRI dataset to bridge cognitive neuroscience and artificial intelligence*. Nature Neuroscience (`10.1038/s41593-021-00962-x`).
