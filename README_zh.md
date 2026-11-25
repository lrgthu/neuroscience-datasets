# 神经科学数据集知识库 (`neuroscience-datasets`)

[English (`README.md`)](./README.md) | **中文文档** | [**在线交互检索页 (GitHub Pages) ↗**](https://lrgthu.github.io/neuroscience-datasets/)

[![CI](https://github.com/lrgthu/neuroscience-datasets/actions/workflows/ci.yml/badge.svg)](https://github.com/lrgthu/neuroscience-datasets/actions/workflows/ci.yml)
[![Pages](https://github.com/lrgthu/neuroscience-datasets/actions/workflows/pages.yml/badge.svg)](https://lrgthu.github.io/neuroscience-datasets/)
[![License: MIT / CC-BY-4.0](https://img.shields.io/badge/License-MIT%20%2F%20CC--BY--4.0-blue.svg)](./LICENSE)

面向 **神经编码与解码（Neural Encoding & Decoding）**、**跨物种/跨模态表征对齐（Representation Alignment）**、**谱几何与可辨识性分析（Spectral & Identifiability Analysis）** 以及 **神经元群体潜在动力学（Latent Population Dynamics）** 研究的结构化、文献级校验数据集知识库。

不同于简单的链接汇总列表，本仓库为每个数据集维护 **严格校验的 YAML 元数据（`datasets/<category>/<id>.yaml`）** 与 **深度技术卡片（`cards/<category>/<id>.md`）**，重点沉淀：
1. **精确实验规模与时空分辨率**：被试/动物数（$N$）、单被试扫描时长、空间覆盖（体素 / 微电极阵列 / Neuropixels 探针 / 双光子平面）与采样率 / `TR`。
2. **社区标准训练/测试划分与噪声上限（Noise Ceiling）**：官方留出测试集（如 NSD `shared1000`、UT-Speech `wheretheressmoke`、TVSD `100 张 × 30 次重复`、CNeuroMod `Friends S7`）与可解释方差上限公式（`ncsnr`、`SPE`、`cvPCA`、`co-bps`）。
3. **关键建模陷阱与防数据泄漏清单（Pitfalls & Leakage Guards）**：预训练基础模型刺激重叠泄漏、快速语音/RSVP 时间窗重叠泄漏、多模态共线性方差分解、慢变先验漂移伪相关（`pseudosessions`）及 `float64` 谱分解数值精度要求。
4. **一键命令行下载与零幻觉文献溯源**：可直接复制执行的 `DataLad` / `AWS S3` / `DANDI` / `ONE-api` 下载命令，以及 100% 经过 OpenAlex / Crossref 校验的 `references.bib`。

---

## 当前已收录数据集总表

<!-- CATALOG:START -->

### 人类自然视觉与多模态视频（fMRI / MEG / EEG） (`6`)

| 数据集 | 年份 | 物种 / 模态 | 被试数 ($N$) & 规模 | 开放级别 / 入口 | 深度卡片 & 文献 |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **CNeuroMod**<br><sub>Courtois NeuroMod & Algonauts 2025 Multimodal Movie Dataset</sub> | 2025 | human<br>`fMRI_3T`, `MEG`, `Structural_MRI` | `N=6`, ~80 h/subj, 250 stim | `registered` · [CNeuroMod](https://www.cneuromod.ca/) (CNeuroMod:friends) | [卡片](./cards/human_vision_multimodal/cneuromod.md) · [`arXiv:2501.00504`](https://arxiv.org/abs/2501.00504) |
| **THINGS-data**<br><sub>THINGS-data (THINGS-fMRI, THINGS-MEG, THINGS-EEG2)</sub> | 2023 | human<br>`fMRI_3T`, `MEG`, `EEG` | `N=17`, ~12 h/subj, 26,107 stim | `open` · [OpenNeuro](https://things-initiative.org/) (OpenNeuro:ds004192) | [卡片](./cards/human_vision_multimodal/things_data.md) · [`10.7554/eLife.82580`](https://doi.org/10.7554/eLife.82580) |
| **NSD**<br><sub>Natural Scenes Dataset (NSD)</sub> | 2021 | human<br>`fMRI_7T`, `Structural_MRI`, `Diffusion_MRI` | `N=8`, ~38 h/subj, 73,000 stim | `registered` · [AWS Open Data](https://naturalscenesdataset.org/) (AWS:s3://natural-scenes-dataset) | [卡片](./cards/human_vision_multimodal/nsd.md) · [`10.1038/s41593-021-00962-x`](https://doi.org/10.1038/s41593-021-00962-x) |
| **BOLD5000**<br><sub>BOLD5000 (Release 2.0)</sub> | 2019 | human<br>`fMRI_3T`, `Structural_MRI`, `Behavior` | `N=4`, ~15 h/subj, 4,916 stim | `open` · [OpenNeuro](https://bold5000-dataset.github.io/website/) (OpenNeuro:ds001499) | [卡片](./cards/human_vision_multimodal/bold5000.md) · [`10.1038/s41597-019-0052-3`](https://doi.org/10.1038/s41597-019-0052-3) |
| **GOD**<br><sub>Generic Object Decoding (Kamitani ImageNet Perception & Imagery fMRI)</sub> | 2017 | human<br>`fMRI_3T`, `Structural_MRI` | `N=5`, ~14 h/subj, 1,250 stim | `open` · [OpenNeuro](https://github.com/KamitaniLab/GenericObjectDecoding) (OpenNeuro:ds001246) | [卡片](./cards/human_vision_multimodal/kamitani_god.md) · [`10.1038/ncomms15037`](https://doi.org/10.1038/ncomms15037) |
| **StudyForrest**<br><sub>StudyForrest (7T Audio & 3T Audiovisual Movie fMRI + Eye-Tracking)</sub> | 2016 | human<br>`fMRI_7T`, `fMRI_3T`, `Structural_MRI` | `N=20`, ~5 h/subj, 8 stim | `open` · [OpenNeuro](https://www.studyforrest.org/) (OpenNeuro:ds000113) | [卡片](./cards/human_vision_multimodal/studyforrest.md) · [`10.1038/sdata.2016.92`](https://doi.org/10.1038/sdata.2016.92) |

### 人类自然语言、语音与颅内记录（fMRI / MEG / EEG / iEEG-ECoG） (`8`)

| 数据集 | 年份 | 物种 / 模态 | 被试数 ($N$) & 规模 | 开放级别 / 入口 | 深度卡片 & 文献 |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **Podcast-ECoG**<br><sub>The 'Podcast' Intracranial ECoG Natural Language Dataset</sub> | 2025 | human<br>`ECoG_iEEG`, `Structural_MRI` | `N=9`, ~0.5 h/subj, 1 stim | `open` · [OpenNeuro](https://openneuro.org/datasets/ds005574) (OpenNeuro:ds005574) | [卡片](./cards/human_language_speech/podcast_ecog.md) · [`10.1038/s41597-025-05462-2`](https://doi.org/10.1038/s41597-025-05462-2) |
| **BrainTreebank**<br><sub>Brain Treebank (Large-Scale Multimodal Movie Intracranial sEEG)</sub> | 2024 | human<br>`sEEG`, `Structural_MRI` | `N=10`, ~4.3 h/subj, 21 stim | `open` · [BrainTreebank](https://braintreebank.dev/) (BrainTreebank:v1) | [卡片](./cards/human_language_speech/braintreebank.md) · [`10.52202/079017-3060`](https://doi.org/10.52202/079017-3060) |
| **MEG-MASC**<br><sub>MEG-MASC (Millisecond Naturalistic Speech MEG Corpus)</sub> | 2023 | human<br>`MEG`, `Structural_MRI`, `Behavior` | `N=27`, ~2 h/subj, 4 stim | `open` · [OpenNeuro](https://openneuro.org/datasets/ds004078) (OpenNeuro:ds004078) | [卡片](./cards/human_language_speech/meg_masc.md) · [`10.1038/s41597-023-02752-5`](https://doi.org/10.1038/s41597-023-02752-5) |
| **UT-Speech**<br><sub>UT Austin Naturalistic Narrative Speech fMRI (LeBel / Huth)</sub> | 2023 | human<br>`fMRI_3T`, `Structural_MRI` | `N=8`, ~11 h/subj, 95 stim | `open` · [OpenNeuro](https://openneuro.org/datasets/ds003020) (OpenNeuro:ds003020) | [卡片](./cards/human_language_speech/uth_natural_speech.md) · [`10.1038/s41597-023-02437-z`](https://doi.org/10.1038/s41597-023-02437-z) |
| **LPP**<br><sub>Le Petit Prince (LPP) Multilingual Audiobook fMRI Corpus</sub> | 2022 | human<br>`fMRI_3T`, `Structural_MRI` | `N=112`, ~1.7 h/subj, 9 stim | `open` · [OpenNeuro](https://openneuro.org/datasets/ds003643) (OpenNeuro:ds003643) | [卡片](./cards/human_language_speech/lpp_multilingual.md) · [`10.1038/s41597-022-01625-7`](https://doi.org/10.1038/s41597-022-01625-7) |
| **Narratives**<br><sub>Narratives Spoken Story fMRI Dataset</sub> | 2021 | human<br>`fMRI_3T`, `Structural_MRI`, `Behavior` | `N=345`, ~0.6 h/subj, 27 stim | `open` · [OpenNeuro](https://github.com/snastase/narratives) (OpenNeuro:ds002345) | [卡片](./cards/human_language_speech/narratives.md) · [`10.1038/s41597-021-01033-3`](https://doi.org/10.1038/s41597-021-01033-3) |
| **MOUS**<br><sub>MOUS (Mother of Unification Studies — 204-Subject Paired fMRI & MEG)</sub> | 2019 | human<br>`fMRI_3T`, `MEG`, `Structural_MRI` | `N=204`, ~2.5 h/subj, 360 stim | `registered` · [Donders Repository](https://data.donders.ru.nl/collections/di/dccn/DSC_3011020.09_236) (Donders:di.dccn.DSC_3011020.09_236) | [卡片](./cards/human_language_speech/mous.md) · [`10.1038/s41597-019-0020-y`](https://doi.org/10.1038/s41597-019-0020-y) |
| **Broderick-EEG**<br><sub>Broderick Naturalistic Audiobook & Cocktail-Party 128-Ch EEG Suite</sub> | 2018 | human<br>`EEG` | `N=19`, ~1 h/subj, 20 stim | `open` · [Dryad](https://datadryad.org/dataset/doi:10.5061/dryad.070jc) (Dryad:10.5061/dryad.070jc) | [卡片](./cards/human_language_speech/broderick_speech_eeg.md) · [`10.1016/j.cub.2018.01.080`](https://doi.org/10.1016/j.cub.2018.01.080) |

### 非人灵长类多脑区阵列电生理（NHP Arrays） (`3`)

| 数据集 | 年份 | 物种 / 模态 | 被试数 ($N$) & 规模 | 开放级别 / 入口 | 深度卡片 & 文献 |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **TVSD**<br><sub>THINGS Ventral-Stream Spiking Dataset (TVSD)</sub> | 2025 | macaque<br>`Utah_Array`, `Eye_Tracking` | `N=2`, ~15 h/subj, 22,348 stim | `open` · [G-Node GIN](https://gin.g-node.org/paolo_papale/TVSD) (GIN:10.12751/g-node.hc7zlv) | [卡片](./cards/nhp_electrophysiology/tvsd.md) · [`10.1016/j.neuron.2024.12.003`](https://doi.org/10.1016/j.neuron.2024.12.003) |
| **NLB-21**<br><sub>Neural Latents Benchmark '21 (NLB Macaque Motor, Sensory & Frontal Suite)</sub> | 2021 | macaque<br>`Utah_Array`, `Behavior`, `Eye_Tracking` | `N=4`, ~1.5 h/subj, 108 stim | `open` · [DANDI](https://neurallatents.github.io/) (DANDI:000127) | [卡片](./cards/nhp_electrophysiology/nlb_2021.md) · [`arXiv:2109.04463`](https://arxiv.org/abs/2109.04463) |
| **MajajHong2015**<br><sub>Majaj-Hong Macaque V4 & IT Core Object Recognition Benchmark</sub> | 2015 | macaque<br>`Utah_Array`, `Behavior` | `N=2`, ~20 h/subj, 5,760 stim | `open` · [Brain-Score / DANDI](https://www.brain-score.org/) (BrainScore:MajajHong2015.public) | [卡片](./cards/nhp_electrophysiology/majaj_hong_2015.md) · [`10.1523/jneurosci.5181-14.2015`](https://doi.org/10.1523/jneurosci.5181-14.2015) |

### 啮齿类大规模神经环路与群体记录（Neuropixels / 2P） (`3`)

| 数据集 | 年份 | 物种 / 模态 | 被试数 ($N$) & 规模 | 开放级别 / 入口 | 深度卡片 & 文献 |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **IBL-BWM**<br><sub>International Brain Laboratory (IBL) Brain-Wide Map</sub> | 2025 | mouse<br>`Neuropixels`, `Eye_Tracking`, `Behavior` | `N=139`, ~2.5 h/subj, 9 stim | `open` · [DANDI / ONE-API (AWS S3)](https://www.internationalbrainlab.com/data) (DANDI:000409) | [卡片](./cards/rodent_circuits_population/ibl_brain_wide_map.md) · [`10.1038/s41586-025-09235-0`](https://doi.org/10.1038/s41586-025-09235-0) |
| **Allen-Vis**<br><sub>Allen Brain Observatory: Visual Coding (Neuropixels & Two-Photon)</sub> | 2021 | mouse<br>`Neuropixels`, `Two_Photon`, `Eye_Tracking` | `N=500`, ~3 h/subj, 118 stim | `open` · [DANDI / AWS Open Data](https://portal.brain-map.org/circuits-behavior/visual-coding) (DANDI:000021) | [卡片](./cards/rodent_circuits_population/allen_visual_coding.md) · [`10.1038/s41586-020-03171-x`](https://doi.org/10.1038/s41586-020-03171-x) |
| **Stringer-10k**<br><sub>Stringer & Pachitariu 10,000-Neuron Mouse V1 Population Geometry Dataset</sub> | 2019 | mouse<br>`Two_Photon`, `Eye_Tracking`, `Behavior` | `N=7`, ~2.5 h/subj, 2,800 stim | `open` · [Figshare](https://doi.org/10.25378/janelia.6845348) (Figshare:10.25378/janelia.6845348) | [卡片](./cards/rodent_circuits_population/stringer_mouse_v1.md) · [`10.1038/s41586-019-1346-5`](https://doi.org/10.1038/s41586-019-1346-5) |

<!-- CATALOG:END -->

---

## 日常维护与更新工作流

```bash
# 1. 环境同步与完整校验（Ruff 规范 + Pytest + Schema/BibTeX 交叉检查）
uv sync --extra dev
uv run pytest -v

# 2. 终端快速检索数据集（支持按物种、模态或关键词过滤）
uv run python scripts/build_catalog.py --species macaque
uv run python scripts/build_catalog.py --modality MEG --query "speech"

# 3. 新增数据集脚手架（自动生成 YAML 模板与 Markdown 卡片）
uv run python scripts/new_dataset.py \
  --id hcp_7t_movie \
  --category human_vision_multimodal \
  --name "HCP 7T Movie-Watching Dataset" \
  --short-name "HCP-7T-Movie"

# 4. 重新编译 catalog/datasets.{json,csv}、双语 README 总表与 GitHub Pages 数据
uv run python scripts/build_catalog.py
```

### 本地私有集群缓存路径隔离说明
由于本仓库为 **Public 公开仓库**，任何内部服务器主机名、局域网 IP 或私有磁盘缓存路径均**严禁提交至 Git**。如需在本地记录各数据集在计算节点上的缓存位置，请将 `local/mirrors.example.yaml` 复制为 `local/mirrors.local.yaml`（已被 `.gitignore` 永久忽略）。
