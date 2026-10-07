# Cover Letter — Caliber Drift and Capability Boundaries (NeurIPS 2027 Evaluations & Datasets)

> **性质**：投稿信（英文版为准；中文对照供内部核对）。
> **版本**：**v1.5 (691 corrected-and-enhanced)** —— version of record 见 `research/latex/VERSION.md`。
> **691 变更（相对 689/690）**：①**题名**改为 *Caliber Drift and Capability Boundaries: An Audit
> Protocol for Software-Verification Evaluation*（撞名核查：2026 年已有 "Auditing the Evaluators"
> (PROPOR 2026) 与 "Evaluator Stress Test" (ACL Findings 2026)，DeepFact 机制名 "audit-then-score"，
> BabelJudge 自述 "reliability audit framework" ⇒ 退出 audit 命名拥挤区，改用自有术语）；
> ②**公式改称符号消歧**（`E[J]=kd/n` 本就是超几何精确均值，`n` 指资产池；改名 `k|D|/|A|` 只为与样本量
> `n` 区分，非纠错）；③**"三池验证"更正**（Pool B≡C，实为 2 个不同池 / 9 个不同块，唯一改进档 k=4
> 被三个池标签重复计数）；④**证据搬运**（机制级 k=1 +11.31pp, p=6.0e-8 等到 §5.1；四个 κ 全报告，
> 含未报告过的 expected_verdict 0.437 / severity 0.157；治理计数 452 事件/67 规则进 §2）；
> ⑤**内容减法**（删 67 规则清单节、压缩 673c 材料与方案类附录；全稿 36→35 页，附录 23 页）。
> **v1.4（689）**：结构性重构（Auditing the Evaluator 方向、5 发现、3 贡献）——骨架保留。
> **689 变更（相对 677d/687）**：题名与叙事**结构性重构**——从"演化验证器"改为"审计评估器"；
> 贡献 4→3（审计协议 / 实证审计 / 量化发现）；新增 §3 Evaluator-Audit Protocol；
> 5 个发现重组（+24pp 改述为**测量池构成效应**；**演化假设失败列为 Finding 5**）；
> 统计补全（TOST 未过 / 双向标准化 / 环境三组件）；旧题名、VC 73.8%、EE 1.9pp/rule 全部退役。
> **数字基线**：`data/current_numbers.json`（含 `reframed_689` 段）+ `data/689_*.json{md}`；
> 全部新数字由 `tools/equivalence_689.py` 与 `tools/environment_metrics_689.py` 从冻结矩阵确定性复算。
> **纪律**：不含任何未落盘数字；缺口**主动声明**（诚实优先）。
> **模板说明**：正文暂用 `neurips_2025.sty` 作 **placeholder**（第三方文件，不改）；其默认页脚
> "Submitted to 39th Conference … (NeurIPS 2025)" 已在 tex 端覆盖为中性 "Under review" 占位；
> 2027 E&D 正式样式发布后迁移。
> **人类标注状态**：方案 + 去标签材料包（145 条）已备；**执行待人类完成，human IAA = 0**；
> 现有 κ 一律为 AI self-consistency，不得当人类一致性引用。
> **arXiv 时序提示**：实名版已同步并打包（`queyi_arxiv_v1.5_realname.tar.gz`）；
> 双盲评审期公开实名版存在时序风险，发布时机由作者决策。

---

## 1. English version (submission)

> Dear NeurIPS Evaluations & Datasets Chairs and Reviewers,
>
> We submit **"Caliber Drift and Capability Boundaries: An Audit Protocol for Software-Verification Evaluation"** for the **Evaluations & Datasets (E&D)** track (targeting the 2027 edition, typically double-blind).
>
> **Why E&D.** This is an **evaluation-methodology paper with a reproducible artifact and a substantial negative result**. We claim no new detector and no algorithmic superiority. Our question: *how often can an apparently convincing evaluation result survive an audit of the evaluator that produced it?*
>
> **Three contributions.**
> 1. **An auditable protocol for evaluating evaluators.** Every quantitative claim declares a measurement caliber $Q=(D,A,E,\Theta,P)$ (dataset, asset set, environment set, configuration set, protocol); eight failure modes provide identification signals; each headline claim is re-measured under adversarial controls that change no malicious behavior, and receives one of four audit outcomes (**survives / weakened / collapses / unresolved**).
> 2. **A systematic empirical audit** of a software-verification apparatus: **1147 self-authored samples $\times$ 8 assets** plus **110 source-derived CVE reconstructions** (all CVEs NVD-verified), with clone-aware splitting and explicit environment profiles.
> 3. **Quantitative findings on what survives.** (F1) A $+24.0$pp selection gain is **mostly measurement-pool composition**; removing degenerate assets leaves $+7.4$--$11.3$pp. (F2) The instrument is **blind to 38.4\%** of its corpus in a family-structured way; severity does not predict detection; 41.5\% of real-defect catches ride on a single asset. (F3) **Environment is part of the measurement**: without the declared WSL profile, real-defect detection falls **59.09\%$\to$23.64\%** with *no* unknown increase and no warning. (F4) Synthetic and source-derived corpora **do not reach TOST equivalence at $\pm10$pp** (90\% CI $[-10.61,+5.52]$pp), and standardization shows the similar headline rates hide a **$-17.9$pp composition offset**. (F5) Failure-driven evolution yields **no measurable recall gain** over frequency selection (identical selections in 14/14 tier checks; best $+1.41$pp, $p{=}0.302$)---reported as an audit finding, not a contribution.
>
> **What we deliberately do not claim.** No priority ("first to audit an evaluator"---DeepFact, metric co-evolution, certified self-evolution and SV-COMP's witness validation are active neighbours); no superiority over mature verifiers (our cross-tool comparison is **observational**, and the pre-registered caliber failed at chance level); no semantic verification (a `catch` is acquired evidence within a boundary); **no human label validation** (human IAA = 0; the $\kappa$ values are AI self-consistency; a de-identified 145-sample annotation package with pre-registered thresholds is prepared and awaiting execution).
>
> **Assets, statistics and reproducibility.** Apache-2.0, DCO; fail-loud reproduction scripts; all headline numbers recomputed from frozen matrices by two new deterministic scripts (equivalence/standardization; environment metrics); the annotation package ships as supplementary material. Known limits: WSL-bound primary profile (native profile's sanitizer absence is an architectural inference; clang-cl/MSVC not tested); template-clone dependence (design effect $\approx4.2$); $\sim$5\% per-cell run instability; eight-asset instrument scope.
>
> We hope the E&D community finds the **audit protocol and the negative findings** useful beyond C++ verification.
>
> We thank you for your consideration.
>
> Sincerely,
> The Authors

---

## 2. 中文对照（内部核对）

- **为什么投 E&D**：评估方法学 + 可复现 artifact + **结构性负结果**。不主张新检测器、不主张算法更优。核心问题：*一个看似令人信服的评估结果，在评估器本身被审计后还能幸存多少？*
- **三条贡献**：①**评估器审计协议**（claim 携带口径 $Q=(D,A,E,\Theta,P)$；8 类失败模式；对抗控制下重测；4 态审计结果 survives/weakened/collapses/unresolved）；②**系统性实证审计**（1147 自造 × 8 资产 + 110 真实 CVE 重构；clone-aware；环境 profile 显式化）；③**量化发现**（F1 +24pp 主要是池构成效应，机制级 +7.4–11.3pp；F2 38.4% 盲区按缺陷家族结构化、严重度不预测检出、41.5% 真实捕获押在单资产；F3 去掉 WSL profile 使真实检出 59.09%→23.64%、unknown 不升、无任何告警；F4 TOST（±10pp）未过、90% CI [−10.61,+5.52]pp、标准化显示整体率相似掩盖 −17.9pp 构成偏移；F5 演化算子无召回增益（14/14 同选、p=0.302）——按审计发现报告）。
- **主动不主张**：不主张"首个审计评估器"（DeepFact / 指标协同演化 / 可证证书自演化 / SV-COMP witness validation 均为活跃近邻）；不主张优于成熟验证器（跨工具对比为**观察性**，预注册口径在 chance 水平失败）；不主张语义验证（`catch` 是边界内获得的证据）；**不主张人类标签验证**（human IAA = 0；κ 全部为 AI self-consistency；145 条去标签标注包 + 预注册阈值已备、待执行）。
- **复现**：Apache-2.0 + DCO；fail-loud 复现脚本；头条数字由两个新增确定性脚本从冻结矩阵复算；标注包随补充材料发布。
- **已知限制**：WSL 主 profile 绑定（native sanitizer 缺失为架构推断，clang-cl/MSVC 未实测）；模板克隆依赖（design effect ≈4.2）；逐格 ~5% 跑间不稳定；8 资产仪器范围。

---

## 3. 使用提醒

1. **不要**写任何**未落盘**数字（尤其不得复活 VC 73.8% / EE 1.9pp/rule / 旧题名 / 18-of-70 口径）。
2. **主动声明**缺口：human IAA = 0 / WSL 硬依赖 / native 推断 / 克隆依赖 / ~5% 跑间不稳定 / 8 资产范围 / E9 观察性。
3. **口径纪律**：1147（数据集与盲区地图，去重前）与 1137（A5，去重后）是**同一池的两套计数**，不得相减；三回合头条率（82.9%/62.5%）与单回合 A5（54.6%）不得相减；TOST **未过**、不得写成"等价"；+24.0pp 与 +7.4–11.3pp 必须**并排**出现。
4. **词数口径**：§1 英文叙述体（含编号列表）≤500 词；`cover_letter.tex` 与本文数字**逐字一致**。
