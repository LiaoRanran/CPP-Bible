# 670d · Cover Letter 草稿

> **性质**：草稿（供人类作者定稿）。**英文版为投稿用**，中文版供内部核对。
> **注意**：本稿**不含**未落盘数字；baseline 缺口在信中**主动声明**（诚实优先，也降低被 desk-reject 风险）。

---

## 1. 英文版（投稿用）

> Dear NeurIPS Datasets & Benchmarks Chairs and Reviewers,
>
> We submit **"Queyi: Making Verification Capability Independently Auditable"** for consideration in the Datasets & Benchmarks track.
>
> **Why E&D.** Our contribution is an **evaluation methodology** with a fully reproducible artifact and an explicit **critical/negative analysis** — the three things E&D asks for. We do not claim a new model or a new benchmark; we claim a way to make *"how well can we verify LLM-generated technical knowledge"* an **externally checkable** question.
>
> **Core contributions.**
> 1. **A verification system** built on a four-state verdict (`pass/fail/unknown/contradict`, with `unknown` a first-class citizen), a forced split of provenance vs. semantic scope, and a **kernel-independent meta-state reconciler** (anti-self-justification).
> 2. **An evaluation protocol** with a five-layer dataset (D0–D4), budget-matched baselines, a six-group ablation with pre-registered hypotheses, and a **frozen statistical caliber** (Clopper–Pearson primary, Fisher/Boschloo, exact McNemar, BH/Holm).
> 3. **An open artifact**: a Merkle-anchored supply chain, a 452-event authority ledger, per-sample detail artifacts, and single-command recomputation entry points.
>
> **Relation to prior work.** Benchmark-evolution lines (Benchmark Self-Evolving, ArenaBencher, LiveBench) evolve the *items*; mutation-guided testing (Meta ACH, MUTGEN) evolves *tests*; formal verification (seL4, CompCert) provides *proofs*. **None evolves the measuring stick itself while proving the change is externally measurable.** That is our position.
>
> **Honest limitations (stated up front).** Two headline numbers depend on a WSL sanitizer environment and **fail silently** when it is absent (35.0% → 10.0%); sample sizes are small (n = 16 / 40); and **budget-matched baselines are not yet run** — we therefore claim **auditability of the mechanism**, **not** superiority over existing methods. We include this analysis as part of the contribution.
>
> **Data & code availability.** The repository is public (Apache-2.0) with DCO sign-off. Datasets D2/D3/D4 and the recomputation commands are described in `REPLICATION.md`; Croissant metadata will be provided in the supplementary material.
>
> We believe this work fits E&D's stated interest in rigorous evaluation practices and transparent, auditable artifacts. We thank you for your consideration.
>
> Sincerely,
> The authors

---

## 2. 中文对照（内部核对）

- **为什么投 E&D**：贡献是**评估方法学** + 可复现 artifact + **批判/负结果**分析——正好是 E&D 三要素。不主张新模型/新 benchmark，只主张让"验证能力有多强"变成**外部可查**的问题。
- **三条贡献**：①四态判决 + provenance/semantic-scope 拆分 + 反自证对账器；②五层数据集 + budget-matched baseline + 六组 ablation（预写假设）+ 冻结统计口径；③开放 artifact（Merkle + 452 账本 + 逐样本明细 + 单命令复算）。
- **与已发表工作的区别**：benchmark 演化类换题目、变异引导类换测试、形式化类给证明——**没有一个在换"尺子"并证明换尺子可被外部度量**。
- **诚实局限（前置）**：两个核心数字依赖 WSL 且**静默掉分**；样本量小；**baseline 未跑** ⇒ 只主张机制可审计，不主张优于现有方法。
- **数据/代码**：Apache-2.0 公开 + DCO；D2/D3/D4 + 复算命令见 `REPLICATION.md`；Croissant 元数据随补充材料提供。

---

## 3. 使用提醒

1. **不要**在信中写任何**未落盘**数字（如 baseline 的"预期提升"）。
2. **主动声明 baseline 缺口**——E&D 审稿人必问，先说比被问更有利。
3. 匿名版：信末签名与仓库 URL 在**双盲阶段**须替换为占位符。
