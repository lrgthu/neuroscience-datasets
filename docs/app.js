(function () {
  "use strict";

  const catalog = window.NEURO_CATALOG || { datasets: [] };
  const datasets = catalog.datasets || [];

  const CATEGORY_LABELS = {
    en: {
      all: "All Categories",
      human_vision_multimodal: "Human Vision & Multimodal",
      human_language_speech: "Human Language, Speech & iEEG",
      nhp_electrophysiology: "NHP Multi-Area Electrophysiology",
      rodent_circuits_population: "Rodent Circuits & Population",
      human_resting_connectomics: "Human Foundation Corpora & Cohorts",
      bci_motor_prosthetics: "BCI, Human Single-Unit & Prosthetics",
      model_organisms_connectomics: "Whole-Brain Model Organisms & EM",
    },
    zh: {
      all: "全部分类",
      human_vision_multimodal: "人类视觉与多模态视频",
      human_language_speech: "人类语言、语音与颅内脑电",
      nhp_electrophysiology: "非人灵长类电生理与影像",
      rodent_circuits_population: "啮齿类大规模神经环路",
      human_resting_connectomics: "人类脑基础模型语料与群体队列",
      bci_motor_prosthetics: "脑机接口与人类单神经元",
      model_organisms_connectomics: "模式生物全脑成像与连接组",
    },
  };

  let state = {
    lang: "en",
    theme: window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light",
    query: "",
    category: "all",
    species: "all",
    modality: "all",
    domain: "all",
    format: "all",
    access: "all",
    sort: "year_desc",
    selectedIds: new Set(),
  };

  document.documentElement.setAttribute("data-theme", state.theme);

  function escapeHtml(str) {
    return String(str ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function populateSelect(el, values, labelFn) {
    el.innerHTML = values
      .map((val) => `<option value="${escapeHtml(val)}">${escapeHtml(labelFn(val))}</option>`)
      .join("");
  }

  function initFilters() {
    const categories = ["all", ...new Set(datasets.map((d) => d.category))];
    const species = ["all", ...new Set(datasets.flatMap((d) => d.species))].sort();
    const modalities = ["all", ...new Set(datasets.flatMap((d) => d.modalities))].sort();
    const domains = ["all", ...new Set(datasets.flatMap((d) => d.domains || []))].sort();
    const formats = ["all", ...new Set(datasets.flatMap((d) => d.data_formats || []))].sort();
    const access = ["all", "open", "registered", "credentialed"];

    populateSelect(
      document.getElementById("category-select"),
      categories,
      (v) => CATEGORY_LABELS[state.lang][v] || v
    );
    document.getElementById("category-select").value = state.category;

    populateSelect(document.getElementById("species-select"), species, (v) =>
      v === "all" ? (state.lang === "zh" ? "全部物种" : "All Species") : v
    );
    document.getElementById("species-select").value = state.species;

    populateSelect(document.getElementById("modality-select"), modalities, (v) =>
      v === "all" ? (state.lang === "zh" ? "全部模态" : "All Modalities") : v
    );
    document.getElementById("modality-select").value = state.modality;

    populateSelect(document.getElementById("domain-select"), domains, (v) =>
      v === "all" ? (state.lang === "zh" ? "全部任务域" : "All Domains") : v
    );
    document.getElementById("domain-select").value = state.domain;

    populateSelect(document.getElementById("format-select"), formats, (v) =>
      v === "all" ? (state.lang === "zh" ? "全部数据格式" : "All Formats") : v
    );
    document.getElementById("format-select").value = state.format;

    populateSelect(document.getElementById("access-select"), access, (v) =>
      v === "all" ? (state.lang === "zh" ? "全部开放级别" : "All Access Tiers") : v
    );
    document.getElementById("access-select").value = state.access;
  }

  function filterAndSort() {
    const q = state.query.trim().toLowerCase();
    const filtered = datasets.filter((d) => {
      if (state.category !== "all" && d.category !== state.category) return false;
      if (state.species !== "all" && !d.species.includes(state.species)) return false;
      if (state.modality !== "all" && !d.modalities.includes(state.modality)) return false;
      if (state.domain !== "all" && !(d.domains || []).includes(state.domain)) return false;
      if (state.format !== "all" && !(d.data_formats || []).includes(state.format)) return false;
      if (state.access !== "all" && d.access.tier !== state.access) return false;
      if (q) {
        const blob = [
          d.id,
          d.short_name,
          d.name,
          d.summary_en,
          d.summary_zh,
          ...(d.domains || []),
          ...(d.brain_regions || []),
          ...(d.access.accession_ids || []),
          ...(d.modeling.key_pitfalls || []),
          d.modeling.standard_splits,
        ]
          .join(" ")
          .toLowerCase();
        if (!blob.includes(q)) return false;
      }
      return true;
    });

    filtered.sort((a, b) => {
      if (state.sort === "subjects_desc") return b.scale.n_subjects - a.scale.n_subjects;
      if (state.sort === "hours_desc") {
        return (b.scale.hours_per_subject || 0) - (a.scale.hours_per_subject || 0);
      }
      if (state.sort === "name_asc") return a.short_name.localeCompare(b.short_name);
      return b.year - a.year || a.short_name.localeCompare(b.short_name);
    });
    return filtered;
  }

  function renderKpis(filtered) {
    const totalSubjects = filtered.reduce((acc, d) => acc + (d.scale.n_subjects || 0), 0);
    const openCount = filtered.filter((d) => d.access.tier === "open").length;
    const modalitiesCount = new Set(filtered.flatMap((d) => d.modalities)).size;
    const isZh = state.lang === "zh";
    document.getElementById("kpi-strip").innerHTML = `
      <div class="kpi-card">
        <div class="kpi-value">${filtered.length} / ${datasets.length}</div>
        <div class="kpi-label">${isZh ? "当前匹配数据集数" : "Matched Datasets"}</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value">${totalSubjects.toLocaleString()}</div>
        <div class="kpi-label">${isZh ? "累计被试/动物规模 (N)" : "Cumulative Subjects (N)"}</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value">${openCount}</div>
        <div class="kpi-label">${isZh ? "免申请直接开放 (Open)" : "Direct Open-Access"}</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value">${modalitiesCount}</div>
        <div class="kpi-label">${isZh ? "覆盖神经记录模态" : "Recording Modalities"}</div>
      </div>
    `;
  }

  function renderCompareBar() {
    const bar = document.getElementById("compare-bar");
    const count = state.selectedIds.size;
    if (count === 0) {
      bar.classList.add("hidden");
      return;
    }
    bar.classList.remove("hidden");
    const names = datasets
      .filter((d) => state.selectedIds.has(d.id))
      .map((d) => d.short_name)
      .join(" vs. ");
    document.getElementById("compare-summary").textContent =
      state.lang === "zh"
        ? `已选 ${count} 个数据集进行横向对比：${names}`
        : `Selected ${count} dataset(s) for comparison: ${names}`;
  }

  function renderCards(filtered) {
    const grid = document.getElementById("cards-grid");
    const isZh = state.lang === "zh";
    if (filtered.length === 0) {
      grid.innerHTML = `<p>${isZh ? "没有匹配当前筛选条件的数据集。" : "No datasets match the active filters."}</p>`;
      return;
    }
    grid.innerHTML = filtered
      .map((d) => {
        const tierClass = d.access.tier === "open" ? "badge-open" : "badge-registered";
        const summary = isZh ? d.summary_zh : d.summary_en;
        const hrs =
          d.scale.hours_per_subject != null ? `${d.scale.hours_per_subject} h/subj` : "Event-based";
        const checked = state.selectedIds.has(d.id) ? "checked" : "";
        return `
        <article class="dataset-card">
          <div>
            <div class="card-top">
              <div class="badge-row">
                <span class="badge badge-species">${escapeHtml(d.species.join("/"))}</span>
                <span class="badge ${tierClass}">${escapeHtml(d.access.tier)}</span>
                <span class="badge">${d.year}</span>
              </div>
              <strong>${escapeHtml(d.short_name)}</strong>
            </div>
            <h2 class="card-title">${escapeHtml(d.name)}</h2>
            <p class="card-summary">${escapeHtml(summary)}</p>
            <div class="badge-row" style="margin-bottom:10px;">
              ${d.modalities.map((m) => `<span class="badge">${escapeHtml(m)}</span>`).join("")}
            </div>
            <div class="metrics-mini">
              <div><strong>${isZh ? "被试规模" : "Subjects"}</strong>N = ${d.scale.n_subjects} (${escapeHtml(hrs)})</div>
              <div><strong>${isZh ? "数据入口" : "Portal"}</strong>${escapeHtml(d.access.primary_portal)}</div>
              <div style="grid-column: span 2;"><strong>${isZh ? "采样率 / 分辨率" : "Sampling / Resolution"}</strong>${escapeHtml(d.scale.sampling_rate_or_tr)}</div>
            </div>
          </div>
          <div class="card-footer">
            <label class="compare-check">
              <input type="checkbox" data-compare-id="${escapeHtml(d.id)}" ${checked} />
              ${isZh ? "加入对比" : "Compare"}
            </label>
            <div style="display:flex;gap:6px;">
              <a class="btn btn-ghost" href="${escapeHtml(d.access.urls.homepage)}" target="_blank" rel="noopener">Portal ↗</a>
              <button class="btn btn-primary" type="button" data-open-id="${escapeHtml(d.id)}">
                ${isZh ? "深度卡片 & BibTeX" : "Inspect Card"}
              </button>
            </div>
          </div>
        </article>`;
      })
      .join("");
  }

  function openDetailModal(datasetId) {
    const d = datasets.find((item) => item.id === datasetId);
    if (!d) return;
    const isZh = state.lang === "zh";
    document.getElementById("modal-badges").innerHTML = `
      <span class="badge badge-species">${escapeHtml(d.species.join("/"))}</span>
      ${d.modalities.map((m) => `<span class="badge">${escapeHtml(m)}</span>`).join("")}
      <span class="badge">${escapeHtml(d.access.license)}</span>
    `;
    document.getElementById("modal-title").textContent = `${d.name} (${d.short_name}, ${d.year})`;

    const accessions = (d.access.accession_ids || []).join(", ") || "—";
    const pitfallsHtml = (d.modeling.key_pitfalls || [])
      .map((p) => `<li>${escapeHtml(p)}</li>`)
      .join("");

    document.getElementById("modal-body").innerHTML = `
      <div class="detail-section">
        <p style="margin-top:0;">${escapeHtml(isZh ? d.summary_zh : d.summary_en)}</p>
        <div class="metrics-mini" style="grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));">
          <div><strong>Subjects (N)</strong>${d.scale.n_subjects}</div>
          <div><strong>Hours / Subject</strong>${d.scale.hours_per_subject ?? "—"} (Total: ${d.scale.total_hours ?? "—"} h)</div>
          <div><strong>Spatial Scale</strong>${escapeHtml(d.scale.n_channels_or_voxels)}</div>
          <div><strong>Temporal / TR</strong>${escapeHtml(d.scale.sampling_rate_or_tr)}</div>
          <div><strong>Formats</strong>${escapeHtml(d.data_formats.join(", "))}</div>
          <div><strong>Accessions</strong><code>${escapeHtml(accessions)}</code></div>
        </div>
      </div>

      <div class="detail-section">
        <h3>${isZh ? "标准评测划分与噪声上限 (Splits & Noise Ceiling)" : "Canonical Evaluation Split & Noise Ceiling"}</h3>
        <p><strong>Split:</strong> ${escapeHtml(d.modeling.standard_splits)}</p>
        <p><strong>Repeat / Noise Ceiling:</strong> ${escapeHtml(d.modeling.noise_ceiling_or_repeat_structure)}</p>
      </div>

      <div class="detail-section">
        <h3>${isZh ? "关键建模陷阱与防泄漏检查 (Key Modeling Pitfalls)" : "Critical Modeling Pitfalls & Leakage Guards"}</h3>
        <div class="pitfall-box"><ul>${pitfallsHtml}</ul></div>
      </div>

      <div class="detail-section">
        <h3>${isZh ? "命令行快速下载 (Programmatic Download CLI)" : "Programmatic Download CLI"}</h3>
        <div class="code-block-wrap">
          <button class="btn btn-outline copy-btn" data-copy-target="cli-box" type="button">Copy</button>
          <pre id="cli-box" class="code-box">${escapeHtml(d.access.download_cli)}</pre>
        </div>
      </div>

      <div class="detail-section">
        <h3>${isZh ? "已校验 BibTeX 引用 (Verified BibTeX)" : "Verified BibTeX Citation"}</h3>
        <div class="code-block-wrap">
          <button class="btn btn-outline copy-btn" data-copy-target="bib-box" type="button">Copy</button>
          <pre id="bib-box" class="code-box">${escapeHtml(d.resolved_bibtex)}</pre>
        </div>
      </div>
    `;
    document.getElementById("detail-modal").classList.remove("hidden");
  }

  function openCompareModal() {
    const items = datasets.filter((d) => state.selectedIds.has(d.id));
    if (items.length === 0) return;
    document.getElementById("modal-badges").innerHTML = `<span class="badge">Side-by-Side Comparison</span>`;
    document.getElementById("modal-title").textContent = items.map((d) => d.short_name).join(" vs. ");

    const rows = [
      ["Year / Species", (d) => `${d.year} · ${d.species.join("/")}`],
      ["Modalities", (d) => d.modalities.join(", ")],
      ["Subjects & Hours", (d) => `N=${d.scale.n_subjects} (${d.scale.hours_per_subject ?? "—"} h/subj)`],
      ["Spatial Scale", (d) => d.scale.n_channels_or_voxels],
      ["Temporal / TR", (d) => d.scale.sampling_rate_or_tr],
      ["Access & Portal", (d) => `${d.access.tier} · ${d.access.primary_portal} (${d.access.license})`],
      ["Standard Split", (d) => d.modeling.standard_splits],
      ["Noise Ceiling", (d) => d.modeling.noise_ceiling_or_repeat_structure],
      ["Top Pitfall", (d) => (d.modeling.key_pitfalls || [])[0] || "—"],
    ];

    const headerCells = items.map((d) => `<td><strong>${escapeHtml(d.name)}</strong></td>`).join("");
    const bodyRows = rows
      .map(
        ([label, fn]) =>
          `<tr><th>${escapeHtml(label)}</th>${items
            .map((d) => `<td>${escapeHtml(fn(d))}</td>`)
            .join("")}</tr>`
      )
      .join("");

    document.getElementById("modal-body").innerHTML = `
      <table class="compare-table">
        <thead><tr><th>Dimension</th>${headerCells}</tr></thead>
        <tbody>${bodyRows}</tbody>
      </table>
    `;
    document.getElementById("detail-modal").classList.remove("hidden");
  }

  function refreshAll() {
    const isZh = state.lang === "zh";
    document.getElementById("ui-title").textContent = isZh
      ? "神经科学数据集知识库 (Neuroscience Datasets KB)"
      : "Neuroscience Datasets Knowledge Base";
    document.getElementById("ui-subtitle").textContent = isZh
      ? "面向神经编码、解码、跨物种表征对齐与群体动力学的文献级校验数据集目录"
      : "Citation-verified catalog for neural encoding, decoding, alignment & circuit dynamics";
    document.getElementById("lang-toggle").textContent = isZh ? "English" : "中文";
    document.getElementById("theme-toggle").textContent = state.theme === "dark" ? "Light" : "Dark";

    initFilters();
    const filtered = filterAndSort();
    renderKpis(filtered);
    renderCompareBar();
    renderCards(filtered);
  }

  document.getElementById("search-input").addEventListener("input", (e) => {
    state.query = e.target.value;
    refreshAll();
  });
  document.getElementById("category-select").addEventListener("change", (e) => {
    state.category = e.target.value;
    refreshAll();
  });
  document.getElementById("species-select").addEventListener("change", (e) => {
    state.species = e.target.value;
    refreshAll();
  });
  document.getElementById("modality-select").addEventListener("change", (e) => {
    state.modality = e.target.value;
    refreshAll();
  });
  document.getElementById("domain-select").addEventListener("change", (e) => {
    state.domain = e.target.value;
    refreshAll();
  });
  document.getElementById("format-select").addEventListener("change", (e) => {
    state.format = e.target.value;
    refreshAll();
  });
  document.getElementById("access-select").addEventListener("change", (e) => {
    state.access = e.target.value;
    refreshAll();
  });
  document.getElementById("sort-select").addEventListener("change", (e) => {
    state.sort = e.target.value;
    refreshAll();
  });
  document.getElementById("reset-btn").addEventListener("click", () => {
    state.query = "";
    state.category = "all";
    state.species = "all";
    state.modality = "all";
    state.domain = "all";
    state.format = "all";
    state.access = "all";
    state.sort = "year_desc";
    document.getElementById("search-input").value = "";
    document.getElementById("sort-select").value = "year_desc";
    refreshAll();
  });
  document.getElementById("lang-toggle").addEventListener("click", () => {
    state.lang = state.lang === "en" ? "zh" : "en";
    refreshAll();
  });
  document.getElementById("theme-toggle").addEventListener("click", () => {
    state.theme = state.theme === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", state.theme);
    refreshAll();
  });

  document.getElementById("cards-grid").addEventListener("click", (e) => {
    const openBtn = e.target.closest("[data-open-id]");
    if (openBtn) {
      openDetailModal(openBtn.getAttribute("data-open-id"));
      return;
    }
    const check = e.target.closest("[data-compare-id]");
    if (check) {
      const id = check.getAttribute("data-compare-id");
      if (check.checked) {
        if (state.selectedIds.size >= 4) {
          check.checked = false;
          return;
        }
        state.selectedIds.add(id);
      } else {
        state.selectedIds.delete(id);
      }
      renderCompareBar();
    }
  });

  document.getElementById("open-compare-btn").addEventListener("click", openCompareModal);
  document.getElementById("clear-compare-btn").addEventListener("click", () => {
    state.selectedIds.clear();
    refreshAll();
  });

  document.getElementById("modal-close").addEventListener("click", () => {
    document.getElementById("detail-modal").classList.add("hidden");
  });
  document.getElementById("detail-modal").addEventListener("click", (e) => {
    if (e.target.id === "detail-modal") {
      document.getElementById("detail-modal").classList.add("hidden");
    }
    const copyBtn = e.target.closest("[data-copy-target]");
    if (copyBtn) {
      const targetEl = document.getElementById(copyBtn.getAttribute("data-copy-target"));
      if (targetEl && navigator.clipboard) {
        navigator.clipboard.writeText(targetEl.textContent || "");
        copyBtn.textContent = "Copied ✓";
        setTimeout(() => {
          copyBtn.textContent = "Copy";
        }, 1400);
      }
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      document.getElementById("detail-modal").classList.add("hidden");
    }
  });

  if (catalog.input_sha256) {
    document.getElementById("footer-hash").textContent =
      `Catalog SHA-256: ${catalog.input_sha256.slice(0, 12)}`;
  }

  refreshAll();
})();
