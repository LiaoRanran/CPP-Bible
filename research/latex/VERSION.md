# VERSION — Version of Record（677a 起生效）

> **唯一权威**：本文件定义"当前论文版本"（version of record）。
> 任何产物（tex / 中文稿 / cover letter / rebuttal / response / 数据卡 / schema）在引用版本号
> 或数字时，**一律以本文件为准**。发现不一致 ⇒ 以本文件 + 权威产物 JSON 为准，反向修正产物。
> 677a 之前存在 673c → 675a → 676f → 676g → 676j → 676m 多个历史状态同时存在，
> 本文件把它们**全部登记为 superseded**，只保留一条当前链。

---

## 1. 当前版本（VERSION OF RECORD）

| 项 | 值 |
|----|----|
| **论文版本** | **v1.2 (677a)** |
| **基于** | v1.1 (673c) 的全部数字 + **676m 数据修复（H1/H2/M1–M5）+ A5 重算** 的终修 |
| **677a 性质** | **纯表述修订**（framing revision + engineering cleanup）。**不做新实验、不产生新数字、不改科学结论** |
| **canonical source** | `research/latex/queyi_neurips2027_v1.1.tex`（文件名保留 v1.1，内部版本号已改为 v1.2/677a） |
| **中文对照稿** | `research/paper_shturl.md`（标题版本已同步为 v1.2 · 677a） |

> **文件名为什么不改**：`queyi_neurips2027_v1.1.tex` 被 `build.ps1`、`arxiv_submission/`、
> `tools/verify_paper_numbers.py` 等多个脚本硬引用。677a 只改**内部版本号**（文件头 + 正文），
> 不重命名文件，避免打断工具链。重命名留给专门的重构批次。

---

## 2. 数字来源（每个数字对应哪个批次的权威产物）

**纪律**：论文里每个数字都必须能给出一行复算命令（AGENT.md）。下表给出权威产物文件。

| 数字族 | 权威批次 | 权威产物 | 复算入口 |
|--------|---------|---------|---------|
| 头条检出率 holdout **82.9%** (34/41) / corpus **62.5%** (40/64) | **672h** | `data/current_numbers.json`（schema `queyi-current-numbers/672h`） | `python tools/verify_paper_numbers.py` |
| 三臂对照 Δ（+80.5 / +45.3 / +73.2 / +40.6 pp）、精确 McNemar | **672h + 673u** | `data/current_numbers.json::comparisons` | `python tools/baseline_670a.py` |
| 对照 FPR **0.0%** (0/11) | **673u** | `data/current_numbers.json` | 同上（`wunsequenced` 恒 catch 缺陷修复后重算） |
| **A5 全量**：FD 54.6% vs Random 30.6%（Δ **+24.0pp**，CI [+20.5, +27.5]，p=2.3×10⁻⁴¹）／vs Static 24.7%（+29.9pp）；并列分析 Δ=**0.0pp**；n=566 | **676f**（经 **676m** 重算复核，主端点**逐位不变**） | `data/a5_676f_results.json`、`data/a5_676f_detection_matrix.json` | `python tools/...`（见 `data/676m_A5重算报告.md`） |
| **盲区地图**：1147 × 8，catch 707 / miss 440 ⇒ 盲区 **38.4%**；**18/70** 类型 >50% 盲；6 资产并集 61.6% vs 最佳单资产 35.6% | **676g** | `data/blindspot_676g_stats.json` | `python data/blindspot_676g_analysis.py` |
| **检测器深度 Benchmark**：asan 58.5% … linker 1.3%；8 资产并集 94.21%；穷举最佳 k=4 = 92.58% | **676l** | `data/676l_benchmark_results.json` | 见 `data/676l_检测器Benchmark总报告.md` |
| **数据质量**：重复 0 / 近克隆 103 对 / 模板克隆率 62.2% / κ=0.77,0.69,0.71 / 编译抽检 217/217 / 真实来源 74/74 | **676k + 676m** | `data/676k_*.json`、`data/676m_sample_manifest_corrected.json` | 见 `data/676m_总报告.md` |
| Verifier Coverage **31/42 = 73.8%**（描述性，**无 CI**） | 659 / 677a 口径修正 | `tools/counts_659.py` | `python tools/counts_659.py` |
| e-value（$2.5\times10^8$ 等） | **exploratory（677a 降级）** | 无权威预注册产物 | **不得用于 confirmatory claim**；见附录 `app:eprocess` |

> **677a 唯一的数字改动（产物对齐，非结论变化）**：
> 「高盲区类型 **15/70**」→「**18/70**」。旧值 15 是转录不全；权威产物
> `data/blindspot_676g_stats.json` 的 `by_type` 中 `blindspot_ratio > 0.5` 的类型为 **18** 个
> （新增三类名：`logic_error`、`virtual_function`、`condition_variable`）。
> cover_letter / response_template 早已写 18/70，tex 与中文稿写 15/70 ⇒ 属版本分裂，677a 统一到产物。
> 复算：`python -c "import json;d=json.load(open('data/blindspot_676g_stats.json',encoding='utf-8'));print(sum(1 for t in d['by_type'] if t['blindspot_ratio']>0.5))"`

---

## 3. 产物清单（文件 → 版本）

### 3.1 论文主体

| 文件 | 版本 | 状态 |
|------|------|------|
| `research/latex/queyi_neurips2027_v1.1.tex` | **v1.2 (677a)** | ✅ current |
| `research/paper_shturl.md` | **v1.2 (677a)** | ✅ current（677a 已替换 675a 的 A5 旧数字 / 标注历史） |
| `research/latex/queyi_neurips2027_v1.1.pdf` | v1.2 (677a) | ✅ 由 677a 重新编译 |
| `research/latex/queyi_refs.bib` | 673c | ✅ current（677a **未新增引用**，避免未定义引用） |
| `research/latex/neurips_2025.sty` | 2025（第三方） | ⚠️ **placeholder，禁止修改**；2027 CFP 发布后迁移 |

### 3.2 投稿包

| 文件 | 版本 | 状态 |
|------|------|------|
| `research/cover_letter.md` | **v1.2 (677a)**（原 676j） | ✅ current（E&D 命名 + 双盲政策已更新） |
| `research/latex/cover_letter.tex` | **v1.2 (677a)** | ✅ current（与 md 孪生版同步） |
| `research/rebuttal_prep.md` | **v1.2 (677a)**（原 676j） | ✅ current（A5 旧数字已标注 superseded） |
| `research/response_template.md` | **v1.2 (677a)**（原 676f） | ✅ current（盲区 18/70 已对齐、e-value 标注 exploratory） |
| `research/latex/response_template.tex` | 676f | ⚠️ 未同步（677a 未改；如需改动请同批更新） |
| `research/submission_checklist.md` | 673k | ⚠️ 历史（D&B 政策条目已过时，见 §5 待办） |

### 3.3 数据与规范

| 文件 | 版本 | 状态 |
|------|------|------|
| `data/holdout_expansion/SCHEMA.md` | **677a**（基于 676m） | ✅ current（新增 `provenance` 枚举，`planted` 保留兼容） |
| `data/holdout_expansion/DATASHEET.md` | **677a**（基于 676m） | ✅ current（Composition 明确三类 provenance） |
| `data/current_numbers.json` | 672h | ✅ current |
| `data/a5_676f_results.json` | 676f（676m 复核） | ✅ current |
| `data/blindspot_676g_stats.json` | 676g | ✅ current |

### 3.4 Superseded（保留但不引用）

| 文件 | 原版本 | 处置 |
|------|--------|------|
| `research/paper_v0.1.md` … `paper_v0.9.md`、`paper_draft_v0.5.md`、`queyi_neurips2027_v1.0.tex` | v0.x / v1.0 | **superseded**：仅供 git 历史追溯。**未删除、未移动**（677a 不新建 `archive/`，避免与其他并发批次冲突）；如需归档请单独开批次 |
| `research/670d_*.md`、`671b_*`、`669d_*` | 早期设计稿 | **superseded**（设计已被 671b/672h 取代，仅留档） |

---

## 4. 已废弃的旧数字（**不得再引用**）

| 旧值 | 出处批次 | 取代它的当前值 |
|------|---------|---------------|
| A5 Δ **+55.0pp**（p=9.8×10⁻⁴）／**+43.8pp**（p=0.039） | 675a | **+24.0pp**（CI [+20.5, +27.5]，p=2.3×10⁻⁴¹），n=566（676f） |
| A5 评估集 **n=20/16**、FD **90.0% / 81.3%** | 675a | **n=566**，FD 54.6%（676f） |
| A5「FD 严格更优 **93.75% / 95.8%**」 | 675a（673u 旧值） | **97.6%**（676f，2000 次重采样） |
| 高盲区类型 **15/70** | 673c（转录不全） | **18/70**（676g 权威产物） |
| holdout **81.2%**（13/16） | 666 | **从未落盘**；现行为 82.9%（34/41，672h） |
| corpus **43.8%**（14/32）/ **35.0%**（14/40） | 665 | **62.5%**（40/64，672h 扩样后可测口径） |
| 669d 口径消融表（87.5/82.4/82.4 与 43.8/37.8/35.0） | 669d | 分母已变，表**作废**（仅 git 留档） |
| 对照 FPR **18.2%**（2/11） | pre-673u | **0.0%**（0/11，673u 修复后重算） |
| Verifier Coverage 73.8% **95% CI [58.0, 86.1]** | 673c | **73.8%，无 CI**（677a：42 张卡是**全枚举**而非抽样，CI 无抽样基础） |

---

## 5. 投稿政策与待办（2027 CFP 发布前**只登记不实现**）

| 事项 | 状态 | 说明 |
|------|------|------|
| **Track 名称** | ✅ 已更新 | 2026 起 Datasets & Benchmarks (D&B) 更名为 **Evaluations & Datasets (E&D)**。cover_letter 已改用 E&D 表述 |
| **盲审政策** | ✅ 已更新 | 2026 起 E&D **通常要求双盲**（不再是"单盲/双盲自选"） |
| **模板** | ⚠️ placeholder | 仍用 `neurips_2025.sty`（**第三方文件，禁止修改**）。PDF 页脚自动生成的 "Submitted to 39th Conference … (NeurIPS 2025)" 是已知 placeholder 伪影，2027 CFP 发布后迁移 |
| **Croissant metadata** | ⬜ **TODO（未实现）** | 2026 起 dataset submission 需要 Croissant 元数据。**2027 规范未定 ⇒ 677a 只登记不生成**。投稿前必须补 |
| **RAI metadata** | ⬜ **TODO（未实现）** | 同上。2026 起 dataset submission 需要 Responsible AI 元数据 |
| `research/submission_checklist.md` 的 D&B 政策条目 | ⬜ TODO | 仍写"D&B 允许单盲或双盲"，已过时，待下批更新 |

---

## 5bis. 并发批次状态（提交时 `git status` 实况）

本仓库多 Agent 并行。677a 提交时观察到：

| 批次 | 状态 | 对本 version of record 的影响 |
|---|---|---|
| **677b**（clone-aware A5） | 工作树中有未跟踪产物（`data/677b_*.json` / `data/677b_*.md` / `tools/analyze_677b_clone_aware.py`），**未提交** | 无：677a **未** add 这些文件 |
| **677c**（非退化池 + 多 Baseline + Evolution Operator） | **已提交**（`f2a4c442`），仅新增 `data/677c_*` 与 `tools/*_677c*.py` | 无：677c 与 677a 的 11 个文件**零交集**（已核 `git show --name-only f2a4c442`） |

> ⚠️ **677b/677c 的实验数字尚未并入论文**：`VERSION.md` §2 的数字来源表仍以 672h/673u/676f/676g/676l/676m 为准。
> 677b/677c 的结果若进入正文，需由后续"论文更新"批次同时更新本文件、论文、cover letter 与数据卡——
> **不得只改论文**（这正是 677a 要消灭的版本分裂）。

## 6. 677a 的诚实边界

1. 本文件只做版本登记与对齐，**不做新实验**。A5 的 clone leakage、非退化 asset pool 等问题留给 **677b / 677c**。
2. `provenance` 字段**只改 schema 与表述**，**不重新标注 1042 条样本**（那是 677b/677c 的工作）。
   当前所有样本的 `provenance` 由 `planted` 按映射规则**派生**：`true → self-authored`，
   `false → source-derived-reconstruction`；`original-external-artifact` 当前计数为 **0**。
3. NeurIPS 2027 CFP 未发布 ⇒ 模板只能用 2025 作 placeholder，**不猜测 2027 规范**。
4. Croissant / RAI 只登记不实现。
5. 旧草稿（paper_v0.1–v0.9）**未删除、未移动**，只在本文件标注为 superseded。
