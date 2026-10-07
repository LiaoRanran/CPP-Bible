# Rebuttal Prep v2 —— Queyi（Evolving Verifiers）E&D 投稿

> **版本**：v2（680 批次，2026-10-07）｜ v1 之后新增：677b/677c 数据、680 数据集审计发现的前瞻披露
> **用途**：针对外部大模型评审（综合 6.5–7/10；因果识别 4.5–5.5、外部效度 4–5、单标注者）的六大核心问题预案
> **纪律**：所有数字可追溯到产物（`data/current_numbers.json` + 原始 JSON）；不辩解、不防御、主动承认局限；**不主张超过证据的结论**
> **数字口径**：1147（数据集/盲区地图，去重前）与 1137（A5，去重后）是同一池的两套计数，**不得相减**

---

## 0. 回应总原则（措辞建议）

1. **先承认，再给出已完成的测量**：每一条批评都先明确"这是真实的局限"，然后给出"我们已经量化了它"的证据。
2. **区分三件事**：机制可审计性（auditability）／同批显著优势（same-sample advantage）／是否优于真实静态检测器（superiority over real static detectors）。我们只主张前两者。
3. **不新增未落盘数字**：任何回应只用已落盘产物中的数字；缺口主动声明。
4. **承认工程管理问题就是承认**：版本分裂是工程债，已通过 678/679 批次系统性清理，不找借口。
5. **拒绝把"未见证据"写成"已确认无"**：例如不要把"未观察到模板泄漏影响"写成"已证明无泄漏"，而要写"clone-aware 重切分后端点不变（+23.0–+26.7pp）"。

---

## 1. 问题一：A5 主实验因果识别未闭合

**评审意见（原文要点）**：+24pp 主要来自退化资产；排除后 k=4 时 FD 与 Random 选集相同 Δ=0；因果识别未闭合。

**回应要点（承认 → 证据 → 界位）**
1. **承认**：这是当前实验的核心局限，我们在论文正文（Threats to Validity, "Instrument boundary; A5's remaining gaps"）中把它列为**未闭合的 identification**，而不是悄悄略过。
2. **给出已完成的三层量化**：
   - 全池（k=4）：FD **54.6%** vs Random **30.6%**（Δ **+24.03pp**，$p{=}2.3\times10^{-41}$，b=136/c=0）；vs Static **24.7%**（**+29.9pp**）。
   - 退化资产剥离（677c 非退化池）：k=1 时 Δ **+11.31pp**（$p{=}6.0\times10^{-8}$）；k≤3 保持 **+7.4 ～ +11.3pp** 且显著 → **选择效应 ≈ +7–12pp**（机制级估计）。
   - k=4 的 Δ=0 是**选集碰撞**：非退化资产仅 5 个、需选 4 个，两个选择器的组合数同为 $1/\binom{5}{4}=0.2$，即"两个策略在只剩 5 个候选时选到同一集合"是**组合必然**，不是机制反证。
3. **我们的定位（已在论文与摘要中写明）**：A5 隔离的是 **pool composition**（"不要把预算给无法提供信息的资产"），**不是"更聪明的排序"**；因此我们只主张 **direction-only evidence + mechanism auditability**。
4. **未来工作**：扩充非退化资产池（目标 ≥3 倍于 k）、学习型 ranking、information-gain baseline、oracle upper bound。

**引用证据**：`data/677c_a5_nondegenerate_results.json`、`data/677c_asset_pools.json`、`data/a5_676f_results.json`、论文 Appendix `app:a5full`。

---

## 2. 问题二：Derivation/evaluation split 不是 clone-aware

**评审意见（原文要点）**：克隆率高（约 62%–75%），模板家族可能跨 split，A5 的 n=566 有效信息量远低于名义值。

**回应要点**
1. **承认**：原始 676f split 确实不是 clone-aware；模板家族会跨 split，名义 $n{=}566$ 不等于有效样本量。
2. **已完成的分析（677b，论文 v1.3 已并入）**：
   - 家族识别：474 个家族（1137 样本；同一源结构的归一化 token 判克隆），最大族 21；克隆对 3124 对；跨批家族 21 个。
   - **clone-family-aware 重切分**（3 种变体：family_random / family_stratified / strict_stratified 连通分量单位）：端点 **Δ 不降反略升**，落在 **+23.0 ～ +26.7pp**，CI 分别为 **[+16.6, +30.4]** 与 **[+18.3, +33.4]**，均排除 0 → **模板泄漏对端点的贡献 ≈ 0**。
   - **family-level cluster bootstrap**：design effect **4.1–4.3** → **有效 $n \approx 133$–$140$**（不是 566）；所有 A5 区间需按 **1.8–2.1×** 放宽。论文已按此改写区间读法。
3. **我们主动承认**：有效样本量仍然偏小（133–140），这是**当前语料的固有属性**（模板复用），不因重切分而消失。
4. **未来工作**：提高结构多样性（每模板仅留 1–2 个代表）、跨语言/跨项目扩样；在方法上把"家族"作为一等公民纳入设计。

**引用证据**：`data/677b_clone_families.json`、`data/677b_cluster_bootstrap.json`、`data/677b_split_*.json`、论文 Appendix "Clone-aware re-split and cluster bootstrap (677b)"。

---

## 3. 问题三：Ground-truth labels 由项目自身产生，无独立人工标注

**评审意见（原文要点）**：单标注者；AI second pass κ=0.77 不是人类 IAA；recall 应表述为 "under project-authored labels"。

**回应要点**
1. **承认（最强威胁）**：这是**最大的 validity threat**，论文已把它升级为 **T17（最大未解威胁）**，并在摘要中写明 "Labels have AI self-consistency only ($\kappa{=}0.77$)"。
2. **明确不混淆口径**：κ=0.77 是 **AI 自我一致性**，**不是人类标注者间一致性（IAA）**，不能替代独立标注；论文不使用"verified labels"一类的措辞。
3. **缓解措施（已落盘）**：
   - 头条率一律带 CP95 区间（82.9% (34/41) [67.9, 92.8]；62.5% (40/64) [49.5, 74.3]），不做点估计断言。
   - 论文 Limitations 与 Data statement 明确标注率依赖项目自建标签。
   - **预注册的独立标注计划**：随机 **25%** 子样本（holdout 10/41 + corpus 16/64）由**第二标注者盲法重标**；若 $\kappa<0.6$ 则升级为 **100% 第三方复审**（在出现任何 "verified" 主张之前执行）。
4. **未来工作**：多标注者 IAA、跨机构复审、把标签与判定分离的外部数据（如 OSS-Fuzz/CVE 回填）。
5. **措辞模板**："All rates are reported *under project-authored labels*; we do not claim independently verified ground truth."

**引用证据**：论文 §Threats to Validity（"Biggest unresolved threat: unreviewed labels"）、`data/676k_*`（κ 分析）、`data/676m_sample_manifest_corrected.json`。

---

## 4. 问题四：Evolution operator 不够算法化，更像 governance framework

**评审意见（原文要点）**：$E(\mathcal{C}_t, F_t)$ 的具体算法内容不足，更像"失败驱动的工程哲学"。

**回应要点**
1. **承认 + 展示（677c 已算法化并写入论文）**：算子已给出**可执行形式**：
   $\mathrm{score}(a_j\mid F_t,\mathcal{C}_t)=w_1\,\text{failure\_coverage}+w_2\,\text{novel\_coverage}-w_3\,\text{cost}-w_4\,\text{redundancy}$，$a^\ast=\arg\max$，$\mathcal{C}_{t+1}=\mathcal{C}_t\cup\{a^\ast\}$；默认权重 $(0.3,0.4,0.1,0.2)$ **未学习**。
2. **两项主动披露（比评审想象得更严格的自我否证）**：
   - **字面定义塌缩**：$F_t$ 按定义就是 $\mathcal{C}_t$ 漏掉的集合 ⇒ "novel coverage" 退化为 failure coverage（$\text{novel}\equiv\text{failure}$），此时算子与 greedy 残差覆盖基线只差 cost/redundancy 惩罚项；我们报告了 exploratory 的 unique-novel 变体，而非偷偷改写参照集。
   - **当前 FD 臂是 frequency-only 特例**（$w_1{=}1$ 全局派生 fail-hit 排序），所以"frequency ≡ FD"是**实现属性**，不是对机制的陈述。
3. **消融结果（诚实报数）**：3 个池 × $k$ 档共 **3/14** 档 full operator 优于 676f FD 选择（最好情况：非退化池 $k{=}4$，56.01% vs 54.59%，$+1.41$pp，$p{=}0.302$）—— **不显著**。
4. **价值声明**：把 $E$ 变成可执行形式的**即期价值是"可证伪"**，不是检出提升（论文原句："The immediate value of making $E$ executable is falsifiability, not a detection gain."）。我们同意它仍是**初步版本**；论文核心贡献在 framework + auditability + empirical study。
5. **未来工作**：学习权重、information-gain baseline、oracle upper bound、把 operator 与 auditor 分离。

**引用证据**：`data/677c_evolution_operator_results.json`、`data/677c_baseline_results.json`、论文 Appendix "Non-degenerate pools, baselines and an executable operator (677c)"。

---

## 5. 问题五：外部效度窄

**评审意见（原文要点）**：约 93% planted、74 条 real-source reconstruction、全部 C++、单一工具链 → 结果难以外推。

**回应要点**
1. **承认并给出精确成分（以计数而非"比例"表述，避免精度暗示）**：
   - A5 口径：**1063 `planted=true` / 74 `planted=false`**（1137）。
   - provenance 三分类（扩样 1042）：**968 `self-authored` / 74 `source-derived-reconstruction` / 0 `original-external-artifact`**。
   - **74 条 `planted=false` 是"从真实 CVE/GitHub issue 重写而来的单文件教学化重构"**，**不是生产代码**；论文在 §Scope restrictions 与 Data statement 明确区分（**不使用 "real-world defects" 表述**）。
   - 我们**没有**原始外部产物（0 条），因此本库**不能**用于估计真实世界缺陷分布。
2. **盲区是仪器边界统计**：38.4%（440/1147）是"**在我们 1147 样本语料 + 我们的 8 资产池**"下的仪器边界，**不蕴含"38.4% 的真实 C++ 缺陷不可检"**；`pass` 只表示"在能力边界内未取得与之矛盾的证据"。
3. **定位**：本工作主张的是 **evaluation methodology + instrument-boundary analysis**，不是 universal defect-detection benchmark，也不是新的 C++ 缺陷分类法。
4. **未来工作**：多语言（Rust/Go）、真实生产代码回填、多工具链对比（clang-analyzer/cppcheck 已做 E9 压力测试：**corpus 打平 cppcheck**，属事后/探索性，论文已登记）。

**引用证据**：`data/676m_sample_manifest_corrected.json`（provenance 派生）、`data/blindspot_676g_stats.json`、论文 Appendix `app:datasheet` / `app:blindspot`。

---

## 6. 问题六：投稿包版本不一致

**评审意见（原文要点）**：包内存在版本分裂（v1.0/v1.1/v1.3 数字并存、用 NeurIPS 2025 模板投 2027）。

**回应要点**
1. **承认**：这是**工程管理债**（多批次并行产出导致），已系统性清理，不辩解。
2. **已完成的清理（678/679 批次）**：
   - 旧 canonical tex 归档，构建入口改指 **version of record**（`research/latex/VERSION.md` 定义；`build.ps1` 与 5 个门禁脚本的路径常量已同步到 v1.1 文件名 = v1.3 内容）。
   - `data/current_numbers.json` 为**唯一数字事实源**；论文/投稿信的数字全部指向同一 release。
   - Cover letter 双版本（LaTeX/Markdown）升级到 **v1.3 (677d)**，贡献 3→5 条对齐，逐数字交叉核对 100% 一致。
   - 论文数字可追溯性审计：**105 项 active 检查全部一致，0 处数值不一致**（`tools/verify_paper_numbers.py`）。
3. **模板问题的既定立场**：2027 CFP 未发布 ⇒ 使用官方 `neurips_2025.sty` 作 **placeholder**（第三方文件，未改）；**2027 E&D 样式发布后迁移**；PDF 页脚的 "NeurIPS 2025" 是 placeholder 伪影，已在 cover letter 的 Template note 声明。
4. **Croissant / Responsible-AI 元数据**：**登记为投稿前待办**（2027 元数据规范未定），不假装已生成。

**引用证据**：`research/latex/VERSION.md`、`data/679_cover_letter升级报告.md`、`data/678_验收报告.md`（如已归档）、`tools/verify_paper_numbers.py` 报告。

---

## 7. 次要问题清单（预期会被追问）

| # | 问题 | 预备回答要点 |
|---|---|---|
| S1 | e-process 层口径 | 明确 **exploratory**：$\mu_0$ 与备择网格未预注册，**不支持任何 confirmatory 主张**；论文有独立 Appendix "E-Process (exploratory)"，并在正文重复声明 |
| S2 | VC 73.8% 的置信区间 | 677a 起**已移除**基于该口径的外推 CI（无抽样基础），只作为描述性系统统计呈现 |
| S3 | 模板 placeholder | 见问题六第 3 点；不把 placeholder 当 2027 合规 |
| S4 | ~5% 逐格判定跑间不稳定 | 已在 Limitations 登记（676f 自证）；**单格结论不作主张**，只作分布级结论 |
| S5 | 死锁类样本的"预期 miss" | 自旋/CV 永久等待 → sanitizer 超时无报告，按 H1 口径归 `miss`（**不是**"检测不到缺陷"）；34 条挂起样本属口径内 |
| S6 | 未运行的 A0–A4 消融 | 论文以 `\{\{TODO_ablation_A0..A4\}\}` 显式标记为 **design-only placeholder**，并说明 "A5 has run"；不把设计当结果 |
| S7 | 历史值 62.5%（30/48，变异 core） | 已标注 **un-pinned 历史值**（无现存产物可复现，676h 已加脚注）；不得当可复现结果引用 |
| S8 | 66.7%（-O1 单档） | 口径**已退休**，仅作为"当时口径下读到的数"引用 |
| S9 | corpus 64 条无磁盘源文件 | `input_mode=code_materialized`（内联装载）**属设计**；因此文本层去重/真实性无法覆盖这 64 条，已在 676k/680 审计中诚实登记 |
| S10 | **（680 审计新增）"70 defect types" 的标签口径** | **主动披露**：70 是**运行矩阵的标签取值数**，其中含原始批次的 legacy 标签（未按 34 项规范词表归一）；样本级 38.4%/61.6% 与标签无关，**类型级统计（18/70）需在规范化标签上重算**——我们把它登记为数据修复项，而非隐瞒。见 `data/680_数据质量深度审计报告.md` §11 |
| S11 | **（680 审计新增）expA/expC 命名空间重名** | 100 组 `sample_XXX` 在 expA 与 expC 间重名（`uid` 唯一）；已登记为数据卫生问题，修复批次将按 `(batch, sample_id)` 复合键处理 |

---

## 8. 数字引用速查表（rebuttal 用）

| 数字 | 值 | 来源产物 |
|---|---|---|
| 头条 holdout recall | 82.9% (34/41), CP95 [67.9, 92.8] | `current_numbers.json:holdout` |
| 头条 corpus recall | 62.5% (40/64), CP95 [49.5, 74.3] | `current_numbers.json:corpus` |
| Static 口径臂 | 2.4% / 17.2%；Δ +80.5 / +45.3pp；$p$=2.3e-10 / 3.7e-9；$h\ge$0.97 | `current_numbers.json:comparisons` |
| Random 仪器代理臂 | 9.8% / 21.9%；Δ +73.2 / +40.6pp；$p$=1.9e-9 / 3.0e-8 | 同上 `*_fd_vs_random` |
| A5 全池 | FD 54.6% vs Random 30.6%（+24.03pp, $p$=2.3e-41）vs Static 24.7%（+29.9pp）；1137×8=9096 detect；派生 571 / 评估 566 | `a5_676f_results.json`、`677b_a5_results_*.json` |
| A5 非退化池 | k=1 +11.31pp（$p$=6.0e-8）；k≤3 +7.4~+11.3pp；k=4 Δ=0.0（组合碰撞 1/C(5,4)=0.2） | `677c_a5_nondegenerate_results.json` |
| clone-aware 重切分 | +23.0~+26.7pp；CI [+16.6,+30.4] / [+18.3,+33.4] | `677b_a5_results_family_*.json` |
| 有效样本量 | $n\approx$133–140；design effect 4.1–4.3；区间放宽 1.8–2.1× | `677b_cluster_bootstrap.json` |
| 克隆结构 | 1137 → 474 家族；最大族 21；克隆对 3124 | `677b_clone_families.json` |
| 盲区地图 | 38.4%（440/1147）；检出 61.6%（707/1147）；18/70 类 >50%；deadlock 94.3%、endianness 89.3%；memory 15.2% → link/ODR 67.7% | `blindspot_676g_stats.json` |
| provenance | 968 self-authored / 74 source-derived-reconstruction / 0 original-external-artifact | `676m_sample_manifest_corrected.json` |
| A5 planted 构成 | 1063 true / 74 false（1137） | `a5_676f_sample_manifest.json` |
| 标注一致性 | AI 自一致性 κ=0.77（非人类 IAA）；T17 最大威胁 | 论文 §Validity、`676k` κ 分析 |
| 可审计性 | Merkle roots over 5 dirs；452-event ledger；67 rules；42 real cards（31 带证据锚） | 论文 §System、`governance_docs_manifest.json` |
| FPR（控制样本） | 0/11 = 0.0% | `current_numbers.json:control_false_positive` |
| 论文数字审计 | 105 active checks 一致 / 0 不一致；9 项已解释 missing | `tools/verify_paper_numbers.py` |
| 数据审计（680） | 结构完整性 100%；抽样 229：FAIL 0；跨源标签不一致 363 行 | `data/680_数据质量深度审计报告.md` |

---

## 9. 不能说的话（红线）

- ❌ "We prove superiority over static detectors" → ✅ "same-sample advantage over the *static-caliber* and *random-proxy* arms; not over a *real* static detector"
- ❌ "real-world defects" → ✅ "source-derived reconstructions of real CVEs/issues（单文件教学化）"
- ❌ "verified labels / ground truth" → ✅ "project-authored labels, AI self-consistency κ=0.77"
- ❌ "38.4% of C++ defects are undetectable" → ✅ "38.4% of *our 1147 samples* are blind spots *with our 8-asset instrument*"
- ❌ "first ever" → ✅ 无首次主张
- ❌ "the operator improves detection" → ✅ "the operator's immediate value is falsifiability; the ablation is not significant (3/14 tiers, p=0.302)"
