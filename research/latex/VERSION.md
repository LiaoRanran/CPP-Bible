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
| **论文版本** | **v1.3 (677d)** |
| **基于** | v1.2 (677a) 的表述修订 + **677b（clone-aware A5 + cluster bootstrap）+ 677c（非退化池 + 多 baseline + operator 算法化）的实验结果并入** |
| **677d 性质** | **论文合并批次**（把已完成实验并入论文与投稿材料）：**不做新实验**、不重跑 detect、不改 677b/677c 产物；正文 ≤9 页、摘要 ≤250 词不变 |
| **canonical source** | `research/latex/queyi_neurips2027_v1.1.tex`（文件名保留 v1.1，内部版本号已改为 v1.3/677d） |
| **中文对照稿** | `research/paper_shturl.md`（标题版本已同步为 v1.3 · 677d） |

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
| **A5 clone-aware 稳健性 + cluster bootstrap**：三种切分 Δ **+23.0~+26.7pp**（p ≤ 4.1×10⁻²⁹）；并列仍 −0.53~+0.00pp；**有效 n≈133–140（deff ≈4.05–4.26）**；Δ 的 CI 宽 **1.78–2.10×**；克隆泄漏量化（64.5% 评估样本有同族 sibling） | **677b** | `data/677b_a5_results_{family_random,family_stratified,strict_stratified}.json`、`data/677b_cluster_bootstrap.json`、`data/677b_clone_families.json` | `python tools/analyze_677b_clone_aware.py --stage all` |
| **A5 非退化池 + 多 baseline + operator 算法化**：严格池 k=1/2/3 显著（最优 **+11.31pp**，p=6.02×10⁻⁸）；k=4 归零 = **选集碰撞 0.2**；退化贡献 **+24.03pp（单点）/+12.81pp（对均值）**；frequency≡fd；full vs fd_only 3/14 档（+1.41pp, p=0.302） | **677c** | `data/677c_a5_nondegenerate_results.json`、`data/677c_baseline_results.json`、`data/677c_evolution_operator_results.json` | `python tools/analyze_677c_nondegenerate.py --stage all` |
| **盲区地图**：1147 × 8，catch 707 / miss 440 ⇒ 盲区 **38.4%**（样本级，681 后不变）；**13/34** 类型 >50% 盲（681 归一化重算；旧口径 18/70 已退役）；6 资产并集 61.6% vs 最佳单资产 35.6% | **676g + 681** | 类型级：`data/681_type_stats_normalized.json`（源：681 修复后的 `data/blindspot_676g_detection_matrix.json`）；样本级：`data/blindspot_676g_stats.json` | `python tools/repair_681_labels.py --apply` |
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
| `research/latex/queyi_neurips2027_v1.1.tex` | **v1.3 (677d)** | ✅ current（677d 并入 677b/677c 结果；正文 8 页 + 参考文献起于第 9 页） |
| `research/paper_shturl.md` | **v1.3 (677d)** | ✅ current（677d 已同步 A5 四条限制与 §7.6/§7.7/§9） |
| `research/latex/queyi_neurips2027_v1.1.pdf` | v1.3 (677d) | ✅ 由 677d 重新编译 |
| `research/latex/queyi_refs.bib` | 673c | ✅ current（677a **未新增引用**，避免未定义引用） |
| `research/latex/neurips_2025.sty` | 2025（第三方） | ⚠️ **placeholder，禁止修改**；2027 CFP 发布后迁移 |

### 3.2 投稿包

| 文件 | 版本 | 状态 |
|------|------|------|
| `research/cover_letter.md` | **v1.3 (677d)**（原 677a） | ✅ current（E&D 命名 + 双盲政策 + 677b/677c 结果已并入） |
| `research/latex/cover_letter.tex` | **v1.3 (677d)** | ✅ current（与 md 孪生版同步） |
| `research/rebuttal_prep.md` | **v1.3 (677d)**（原 677a） | ✅ current（新增 0bis-2 与 Q16–Q18：有效样本量 / 退化资产 / 模板泄漏） |
| `research/response_template.md` | **v1.3 (677d)**（原 677a） | ✅ current（A5 段并入 677b/677c，孪生 tex 已同步） |
| `research/latex/response_template.tex` | **v1.3 (677d)** | ✅ current（与 md 孪生版逐条对齐） |
| `research/submission_checklist.md` | 673k + **677a 政策横幅** | ⚠️ 历史清单（产物指向 v1.0 时代）；D&B 政策已标注过时 |
| `research/latex/arxiv_submission/queyi_neurips2027_v1.1.tex` | **v1.3 (677d)** | ✅ current（v1.1 tex 的逐字节拷贝，677d 已同步） |
| `research/latex/arxiv_submission/README.txt` | **v1.3 (677d)** | ✅ current（677d repack 记录；677a/676m 记录标 superseded） |
| `research/latex/queyi_neurips2027.tex` | 旧 canonical | 🟡 **已归档**（678 批次移至 `research/latex/archive/queyi_neurips2027.tex`；build.ps1 现指向 v1.1；若需追溯旧内容见归档副本） |

### 3.3 数据与规范

| 文件 | 版本 | 状态 |
|------|------|------|
| `data/holdout_expansion/SCHEMA.md` | **677a**（基于 676m） | ✅ current（新增 `provenance` 枚举，`planted` 保留兼容） |
| `data/holdout_expansion/DATASHEET.md` | **677a**（基于 676m） | ✅ current（Composition 明确三类 provenance） |
| `data/current_numbers.json` | 672h | ✅ current |
| `data/a5_676f_results.json` | 676f（676m 复核） | ✅ current |
| `data/677b_clone_families.json`、`data/677b_split_*.json`、`data/677b_a5_results_*.json`、`data/677b_cluster_bootstrap.json` | **677b** | ✅ current（A5 稳健性/有效样本量的权威产物） |
| `data/677c_a5_nondegenerate_results.json`、`data/677c_baseline_results.json`、`data/677c_evolution_operator_results.json`、`data/677c_asset_pools.json` | **677c** | ✅ current（非退化池/多 baseline/operator 的权威产物） |
| `data/blindspot_676g_stats.json` | 676g | 🟡 **类型级 superseded（681）**：样本级（707/440/38.4%）仍权威；类型级改引 `data/681_type_stats_normalized.json` |
| `data/blindspot_676g_detection_matrix.json` | **676g + 681 修复** | ✅ current（681：`defect_type`/`expected_verdict` 两列重派生；`per_asset`/`or_verdict_all8` 观测列**零改动**） |
| `data/holdout_expansion/expA/INDEX.json` | **681** | ✅ current（100 条 `defect_type` + 38 条 `expected_verdict` 对齐权威 JSON；`by_type` 重算） |
| `data/676m_sample_manifest_corrected.json` | **676m + 681** | ✅ current（681：expA 100 行标签修正；其余批次本就一致） |
| `data/681_修复计划.md`、`data/681_标签修复日志.json`、`data/681_归一化映射表.md`、`data/681_类型统计重算报告.md`、`data/681_type_stats_normalized.json` | **681** | ✅ current（修复计划/逐条 old→new + 证据/38 项映射表/重算与论文口径建议/结构化统计） |

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
| 高盲区类型 **15/70** | 673c（转录不全） | **18/70**（676g）→ 再经 681 归一化为 **13/34** |
| 类型数 / 高盲区类型数 **70 / 18-of-70**（未归一化标签集，含 38 个 legacy 同义/元标签） | 676g（681 前口径） | **34 / 13**（681：矩阵标签归一化到 34 项闭集后重算；样本级 38.4%/707/440 **不变**） |
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
| `research/submission_checklist.md` 的 D&B 政策条目 | ✅ 已更新 | 677a 续批：顶部加 E&D/双盲政策横幅，§14.5 改写并登记 Croissant/RAI 待办 |
| 摘要词数 ≤250（门禁口径） | ✅ 已达标 | **246 词**（HEAD v1.1 为 367）；所有数字与限定语保留 |

---

## 5bis. 并发批次状态（677a 各次提交时 `git status` / `git log` 实况）

本仓库多 Agent 并行。677a 三次提交期间观察到：

| 批次 | 状态 | 对本 version of record 的影响 |
|---|---|---|
| **677c**（非退化池 + 多 Baseline + Evolution Operator） | **已提交**（`f2a4c442`），仅新增 `data/677c_*` 与 `tools/*_677c*.py` | 无：与 677a 的文件**零交集**（已核 `git show --name-only`） |
| **677b**（clone-family-aware A5 + cluster bootstrap） | **已提交**（`92482d4f` + `3e6e6044` 回填），仅新增 `data/677b_*` 与 `tools/analyze_677b_clone_aware.py` | 无：与 677a 的文件**零交集**；其主端点稳健、并列仍归零、有效样本量 ≈133–140 |

> ✅ **677b/677c 的实验数字已由 677d 并入论文**（2026-10-04）：本文件、英文稿、中文稿、cover letter、
> rebuttal_prep、response_template（.md/.tex）、arXiv 包**同时更新**——按 677a 的纪律，**不存在"只改论文"的版本分裂**。

## 5ter. 677d 变更清单（v1.2 → v1.3，全部为"并入既有实验结果"，无新实验）

| # | 文件 | 变更 |
|---|---|---|
| 1 | `research/latex/queyi_neurips2027_v1.1.tex` | 文件头版本行 → v1.3 (677d)；**主文**：E4 段 + 稳健性句（clone-aware +23.0~+26.7pp / 有效 n≈133–140 / 非退化池 k≤3 +11.31pp、k=4 选集碰撞）、Analysis(5)、Threats（effective sample size + degenerate 贡献 +12pp）、Conclusion（"中心结果 = 方向性：选择效应 ≈+7~12pp"）、方法 §Failure-driven loop 指向可执行 $E$、Future work (iii) 改写；**附录**：新增 **`Clone-aware re-split and cluster bootstrap (677b)`** 与 **`Non-degenerate pools, baselines and an executable operator (677c)`** 两段、app:formal 新增 **`Evolution operator: executable form (677c)`**（score 四分量 + 两处坍缩披露 + 3/14 不显著）、Power 段与威胁附录补有效样本量、Claims 表两行补证据 |
| 2 | `research/paper_shturl.md` | 标题 → v1.3 · 677d；新增"本稿说明（677d）"块；§5.1.1 克隆率限定由"只披露"升级为"已控制 + 有效 n 已量化"；§5.3/§6.2 表与四条限制（原三条 + 新增 ④ 克隆泄漏已排除）；§6.2 本节性质；§7.6 实际读到的结果与红线；§7.7/§7.9/§9 证据边界与未来工作 |
| 3 | `research/cover_letter.md` / `research/latex/cover_letter.tex` | 贡献 3 改"full-scale falsification experiment, **with its robustness measured**"（+23.0~+26.7pp / 有效 n≈133–140 / 选择效应 ≈+7–12pp）；局限段补有效 n；数字基线加 677b/677c 权威产物；版本号 → v1.3 |
| 4 | `research/rebuttal_prep.md` | 新增 **0bis-2（677d 态势表）**；Q1 补"**What 677b/677c add**"整段与路线图；新增 **Q16（有效样本量）/ Q17（退化资产与选集碰撞）/ Q18（模板泄漏）**；附录 A 弹药库更新 |
| 5 | `research/response_template.md` / `.tex` | 同步 A5 数字与两条新增复核（孪生版一致）；A5"on the core-mechanism falsification experiment"段与样本量段改写 |
| 6 | `research/latex/arxiv_submission/` | 用新主 tex 覆盖（逐字节）+ README.txt 追加 677d repack 记录 |
| 7 | `data/677d_合并计划.md` / `data/677d_论文合并报告.md` | 新增（本批计划与总报告） |

**核心数字（v1.3 口径，"并排"是硬要求）**：
`A5 主端点 +24.0pp（全池，k=4）` **必须与** `非退化池选择效应 ≈+7~12pp（k≤3 显著，k=4 为选集碰撞）` 同句出现；
任何 A5 区间须注明 **有效 n≈133–140（deff ≈4.05–4.26）** 与 **1.78–2.10× 放宽**；
`clone-aware 重切分后主端点与并列归零均不变` ⇒ **模板泄漏已排除**（不是"未检验"）。

## 5quater. 681 变更清单（数据修复批次：**标签口径归一化**，无新实验）

| # | 文件 | 变更 |
|---|---|---|
| 1 | `data/blindspot_676g_detection_matrix.json` | `defect_type` **413** 行重派生（308 扩样 ← 权威 JSON；105 原始 ← SCHEMA §3.3/§4.2 证据映射）+ `expected_verdict` **34** 行（expE hung 口径回灌）；**观测列零改动** |
| 2 | `data/holdout_expansion/expA/INDEX.json` | 100 行 `defect_type` + 38 行 `expected_verdict` 对齐权威 JSON；`by_type` 重算 |
| 3 | `data/676m_sample_manifest_corrected.json` | expA 100 行标签修正（↔ 权威 JSON 不一致归零） |
| 4 | `data/current_numbers.json` | 新增 `repair_681` 段；`revision: "681"`；类型级数字 **70/18 → 34/13**（样本级不变） |
| 5 | `tools/repair_681_labels.py` | 新增（幂等修复脚本；dry-run/`--apply`） |
| 6 | `tools/verify_paper_numbers.py` | 检查集 **118 → 122**（D11–D14：677b clone-aware Δ / 有效 n / 677c 选择效应 / 退化贡献） |
| 7 | `data/681_*.md`、`data/681_*.json` | 修复计划 / 修复日志 / 归一化映射表 / 类型统计重算报告 / 结构化统计 |
| 8 | 论文与投稿信（D 任务） | 类型级标签数字由 70/18 更新为 34/13（**仅标签数字与口径说明**，样本级与 A5 数字未动） |

**根因（一次性说明）**：676m 迁移改写了 308/1042 条权威 `defect_type`，但 `blindspot_676g_detection_matrix.json` 生成于 676m 之前且此后未重派生（见 `data/holdout_expansion/SCHEMA.md` §6「改写样本 308/1042」——与审计发现的 308 同数）⇒ 681 把两列重派生并归一化。

**红线声明**：权威逐样本 JSON 与样本源码 `.cpp` **零改动**；`per_asset`/`or_verdict_all8` 观测值 **零改动**（A5 Δ 稳定性差异 **0.00pp**）；样本级 38.4%/61.6% **不变**。

## 6. 677a 的诚实边界

1. 本文件只做版本登记与对齐，**不做新实验**。A5 的 clone leakage、非退化 asset pool 等问题留给 **677b / 677c**。
2. `provenance` 字段**只改 schema 与表述**，**不重新标注 1042 条样本**（那是 677b/677c 的工作）。
   当前所有样本的 `provenance` 由 `planted` 按映射规则**派生**：`true → self-authored`，
   `false → source-derived-reconstruction`；`original-external-artifact` 当前计数为 **0**。
3. NeurIPS 2027 CFP 未发布 ⇒ 模板只能用 2025 作 placeholder，**不猜测 2027 规范**。
4. Croissant / RAI 只登记不实现。
5. 旧草稿（paper_v0.1–v0.9）**未删除、未移动**，只在本文件标注为 superseded。
