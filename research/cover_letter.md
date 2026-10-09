# Cover Letter — Caliber Drift and Capability Boundaries (NeurIPS 2027 Evaluations & Datasets)

> **性质**：投稿信（英文版为准；中文对照供内部核对）。
> **版本**：**v1.7 (703 full rewrite)** —— version of record 见 `research/latex/VERSION.md`。
> **703 变更（相对 v1.6/692）**：**完全重写**。v1.6 的叙事只以"实证审计"为主线；v1.7 改为
> 以论文**现在真正主张的四条**为主线——①**测量漂移代数**（7 公理 + 6 定理；元理论证明**只有 2 条独立**；
> 系统**不完备**、缺 **A8**；口径套利 NP-hard + 贪心 $(1-1/e)$）②**结构性（被动）Goodhart 的四型**
> 分类与实证 ③**能力边界地图**（38.4% 盲区 / 13 of 34 类型 >50% / 41.5% 单资产依赖）
> ④**真实 CVE 验证**（110 条，59.09%）。并折入 700 批次的理论（信息论下界 / 双设计）与
> 699 / 700-D 的跨领域证据。**诚实声明扩充**：公理系统不完备（缺 A8）、699 的 22 个原始项目**未编译**。
> **题名说明**：703 任务书建议的 "Auditing the Evaluator" 是 **v1.4 的旧题名**，已在 v1.5(691)
> 因 2026 年撞名核查（"Auditing the Evaluators" PROPOR 2026 / "Evaluator Stress Test" ACL Findings 2026 /
> DeepFact "audit-then-score" / BabelJudge "reliability audit framework"）**退役**；
> 投稿信必须携带**论文自己的题名**（verbatim），故仍为
> *Caliber Drift and Capability Boundaries: An Audit Protocol for Software-Verification Evaluation*。
> **v1.6（692）**：环境感知配对实验数字；5 发现。
> **v1.5（691）**：题名更换（caliber drift / capability boundaries）；公式改称符号消歧；
> "三池"更正为 2 个不同池 / 9 个不同块。
> **v1.4（689）**：结构性重构（审计方向、3 贡献；演化假设失败列为 Finding 5）。
> **数字基线**：`data/current_numbers.json`、`data/689_*.json{md}`、`data/696_transition_matrix.json`、
> `data/700_*.json{md}`、`data/703_zero_cost_validation.json`。
> **纪律**：不含任何未落盘数字；缺口**主动声明**（诚实优先）。
> **模板说明**：正文暂用 `neurips_2025.sty` 作 **placeholder**（第三方文件，不改）；其默认页脚
> 已在 tex 端覆盖为中性 "Under review" 占位；2027 E&D 正式样式发布后迁移。
> **人类标注状态**：方案 + 去标签材料包（145 条）已备；**执行待人类完成，human IAA = 0**；
> 现有 κ 一律为 AI self-consistency，不得当人类一致性引用。
> **词数口径**：§1 英文叙述体（含编号列表）**495 词** ≤ 500（从 "To the NeurIPS" 到 "The Authors"，
> 去 LaTeX 命令后计数）；`cover_letter.tex` 与本文数字**逐字一致**。

---

## 1. English version (submission)

> To the NeurIPS Evaluations & Datasets Chairs and Reviewers,
>
> We submit **"Caliber Drift and Capability Boundaries: An Audit Protocol for Software-Verification Evaluation"** to the **Evaluations & Datasets (E&D)** track (2027 edition). *Throughout, "verifier" is used in the evidence-acquisition sense*: a `catch` reports refuting evidence acquired within our capability boundary, **not** semantic truth.
>
> **Template note.** The 2027 CFP is unreleased; this draft uses the official `neurips_2025` style as an unmodified placeholder with a neutral "Under review" notice.
>
> **Why this fits E&D.** An *evaluation methodology* with a reproducible artifact and a substantial *negative* result. We claim no new detector and no algorithmic superiority. Our question: *how often can an apparently convincing evaluation result survive an audit of the evaluator that produced it?*
>
> **Four contributions.** (1) **A measurement-drift algebra**: seven axioms and six theorems; our metatheory shows only **two** axioms are independent (monotonicity, super-additivity), four are theorems and one is a meta-axiom, and the system is **incomplete**---label drift (Type III) cannot be expressed, so we register a missing **A8 (label-axis closure)** and prove caliber arbitrage NP-hard with a greedy $(1-1/e)$ approximation. (2) **Structural (passive) Goodhart**, in four types (caliber/composition/label/aggregation), each moving the reported number with *no* optimisation pressure; Types III and IV leave *every* per-sample verdict unchanged. (3) **A capability-boundary map**: the instrument is blind to **38.4%** (440/1147) of its corpus, **13 of 34** defect types exceed 50% blindness, and **41.5%** of real-defect catches ride on one asset. (4) **Real-CVE validation**: **110** NVD-verified CVE reconstructions detect at **59.09%**.
>
> **Key audited numbers.** A $+24.03$pp apparent selection gain *collapses at $k=4$* (0.00pp, $p=1.0$) once degenerate assets are removed, leaving $+7.4$--$11.3$pp. Under the environment-aware protocol the declared profile gives 60.07% and the reduced profile 24.74% (566-sample split), with Δunknown $=0.00$pp unaware versus 75.27pp aware---a *silent* degradation. The evolution operator is Δ$=0$ at *every* tier (identical to greedy set-cover). Paired designs have identically **zero power** against Types III/IV ($\psi=0$), so Step 3 becomes a *dual* design: sample-level pairing for I/II (Type I needs $n\approx849$, Type II only 17), design-level contrast for III/IV.
>
> **What we do *not* claim.** No priority (DeepFact, metric co-evolution, certified self-evolution and SV-COMP witness validation are neighbours); no superiority over mature verifiers; no semantic verification; and **no human label validation**---human IAA is **0**, all $\kappa$ values are AI self-consistency, and a de-identified 145-sample annotation package ships unexecuted. Two gaps stay open: the axiom system is **incomplete** (A8 missing), and of **22** original open-source projects collected for cross-domain validation **none has been compiled** (no network egress); build feasibility is untested.
>
> **Reproducibility.** Apache-2.0, DCO-signed, fail-loud scripts; every headline number recomputed from frozen matrices. Declared limits: a WSL-bound primary profile (the native profile's sanitizer absence is an architectural inference; clang-cl/MSVC untested); template-clone dependence (design effect $\approx4.2$); ~5% per-cell run instability; an eight-asset scope.
>
> We hope the E&D community finds the **audit protocol and negative findings** useful beyond C++ verification.
>
> Sincerely,
> The Authors

---

## 2. 中文对照（内部核对）

- **为什么投 E&D**：评估方法学 + 可复现 artifact + **结构性负结果**。不主张新检测器、不主张算法更优。核心问题：*一个看似令人信服的评估结果，在评估器本身被审计后还能幸存多少？*
- **四条贡献**：①**测量漂移代数**（7 公理 + 6 定理；元理论：只有单调 A2 与超可加 A5 **独立**，4 条是定理、1 条是元公理；系统**不完备**，缺 **A8 标签轴闭包**；口径套利 NP-hard + 贪心 $(1-1/e)$ 近似）；②**结构性（被动）Goodhart 四型**（口径/构成/标签/聚合；无优化压力即可移动报告值；Type III/IV **不改变任何逐样本裁决**）；③**能力边界地图**（盲区 38.4% = 440/1147；**13 of 34** 类型 >50% 盲；**41.5%** 真实捕获押在单资产）；④**真实 CVE 验证**（110 条 NVD 核验重构，检出 **59.09%**）。
- **关键审计数字**：$+24.03$pp 表观增益在移除退化资产后于 $k=4$ **塌缩为 0.00pp（$p=1.0$）**，机制级残留 $+7.4$–$11.3$pp；环境感知协议下声明 profile 60.07% vs 缩减 profile 24.74%（566 帧），Δunknown **0.00pp（unaware）vs 75.27pp（aware）**——**静默**退化；演化算子**全档 Δ=0**（≡ greedy set-cover）；配对设计对 Type III/IV **功效恒为 0**（$\psi=0$）⇒ Step 3 改**双设计**（样本级配对 I/II：Type I 需 $n\approx849$、Type II 仅 17；设计级对照 III/IV）。
- **主动不主张**：不主张"首个审计评估器"（DeepFact / 指标协同演化 / 可证证书自演化 / SV-COMP witness validation 均为近邻）；不主张优于成熟验证器（跨工具对比为 convergent validity，预注册口径在 chance 水平失败）；不主张语义验证（`catch` 是边界内获得的证据）；**不主张人类标签验证**（human IAA = 0；κ 全部为 AI self-consistency；145 条去标签标注包已备、**未执行**）。
- **两条未关闭缺口**：①公理系统**不完备**（缺 A8）；②699 收集的 **22 个原始开源项目均未编译**（构建环境无网络出口），**构建可行性未验证**。
- **复现**：Apache-2.0 + DCO；fail-loud 复现脚本；头条数字全部由确定性脚本从冻结矩阵复算。
- **已知限制**：WSL 主 profile 绑定（native sanitizer 缺失为架构推断，clang-cl/MSVC 未实测）；模板克隆依赖（design effect ≈4.2）；逐格 ~5% 跑间不稳定；8 资产仪器范围。

---

## 3. 使用提醒

1. **不要**写任何**未落盘**数字（尤其不得复活 VC 73.8% / EE 1.9pp/rule / 旧题名 "Auditing the Evaluator" / 18-of-70 口径）。
2. **主动声明**缺口：human IAA = 0 / **A8 缺失（公理系统不完备）** / 699 的 22 个项目未编译 / WSL 硬依赖 / native 推断 / 克隆依赖 / ~5% 跑间不稳定 / 8 资产范围 / E9 观察性。
3. **口径纪律**：1147（数据集与盲区地图，去重前）与 1137（A5，去重后）是**同一池的两套计数**，不得相减；三回合头条率（82.9%/62.5%）与单回合 A5（54.6%）不得相减；TOST **未过**、不得写成"等价"；+24.0pp 与 +7.4–11.3pp 必须**并排**出现。
4. **词数口径**：§1 英文叙述体（含编号列表）≤500 词（703 实测 **495**）；`cover_letter.tex` 与本文数字**逐字一致**。
