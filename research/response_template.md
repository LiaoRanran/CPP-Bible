# Response to Reviewers — Template (Queyi, NeurIPS 2027 E&D) · v1.4 (689 reframed)

> **用法**：引用审稿人原话（`Reviewer:`），再给回复（`Response:`），并标出改动位置（`Change:`）。
> **纪律**：不辩解、不回避；**承认的缺口原样承认**（与论文立场一致）。
> **数字基线**：`data/current_numbers.json`（含 `reframed_689` 段）+ `data/689_*.json`（TOST/标准化/环境三组件）+ `data/a5_676f_results.json` + `data/blindspot_676g_stats.json`。**回复中不得出现未落盘数字。**
> **689 口径（回复时必须一致）**：① 题名 = **"Caliber Drift and Capability Boundaries: An Audit Protocol for Software-Verification Evaluation"**（不得再用 "Evolving Verifiers"）；② 贡献 **3 条**（审计协议 / 实证审计 / 量化发现），演化与子模**不是**贡献；③ **5 个发现**：F1 +24.0pp 主要为**池构成效应**（机制级 +7.4–11.3pp）、F2 38.4% 盲区（instrument-boundary；13/34 类 >50%）、F3 环境（59.09%→23.64%，Δunknown=0）、F4 **TOST 未过**（90% CI [−10.61,+5.52]pp）+ 标准化 −17.92pp、F5 **演化假设失败**（14/14 同选；p=0.302）；④ **VC 73.8% 与 EE 1.9pp/rule 已删除**；⑤ static 臂 = **calibration arm**；⑥ §7 五类威胁 T1–T5；⑦ **human IAA = 0**（方案+材料包已备、待执行）；κ 一律 AI self-consistency；⑧ Track 名为 **E&D**，通常双盲；模板 2025 placeholder（页脚已覆盖为 Under review）。版本 of record：`research/latex/VERSION.md`。

---

## Summary of changes（修订摘要，按实际改动填）

- 同步全部数字至 **672h/673u/676f/676g** 权威源（holdout **82.9%** (34/41)、corpus **62.5%** (40/64)、**对照 FPR 0.0% (0/11)**——一个早期草案曾报 2 例对照假阳性，系 `wunsequenced` 恒 catch 缺陷所致，673u 已修复，头条率逐位不变）。
- **A5 已在全量池上跑完，并已复核（677b/677c）**（1137 样本 × 8 资产 = 9096 次真实 detect；派生 571 / 评估 566，k=4）：FD **54.6%** vs Random **30.6%**（Δ **+24.0pp**，p=2.3×10⁻⁴¹）vs Static **24.7%**（+29.9pp）；并列分析 k=4 仍归零（Δ=0.0pp，p=1.0）⇒ **direction-only**，**不是** "FD > Random"。**677c**：严格非退化池（5 资产）上 k=1/2/3 仍显著（最优 **+11.31pp**，p=6.0×10⁻⁸），**k=4 归零是选集碰撞（1/C(5,4)=0.2）**，退化资产贡献 +24.03pp/+12.81pp ⇒ **选择效应 ≈ +7~12pp**。**677b**：clone-aware 重切分（474 家族 / strict 420 分量、克隆对跨越=0）后主端点与并列归零**均不变** ⇒ 模板泄漏**已排除**；家族级 cluster bootstrap ⇒ **有效 n≈133–140**、A5 区间须按 **1.78–2.10×** 放宽。
- 新增 **检测器能力边界地图**（676g）：1147×8 矩阵，检出 **61.6%**、盲区 **38.4%**、**13/34** 类 >50%；**逐格 ~5% 跑间不稳定**（676f 自证）一并登记。
- 随机臂在 672h 为**仪器级代理**；A5 的全量预算匹配对照已补上，**Static 臂仍为口径重分箱**。
- 全部率值补 Clopper–Pearson 95% CI；配对对比补精确 McNemar + Cohen's $h$ + Δ CI。
- 明确 `UNVERIFIED` 协议（缺依赖时报未验证，不报误导性低分）。
- 新增/强化威胁：LLM 通道不可信（prompt injection）、小样本投毒、peeking、检测器能力边界（T20）。
- 补引用：Cohen (1988)、Connor (1987)、Belnap (1977)、CELEUS、QuickCheck/Hypothesis/KLEE。
- **689 结构性重构**：题名改为 "Auditing the Evaluator…"；贡献 4→3；新增 §3 审计协议（claim 口径 / 8 失败模式 / 证伪流程 / 4 态结果）；正文重组为 5 个审计发现；+24.0pp 改述为测量池构成效应（机制级 +7.4–11.3pp）；**演化假设失败列为 Finding 5**；删除 VC 73.8% / EE 1.9pp/rule；static → calibration arm；Merkle 改述为 tamper-evident 当前态完整性 + 威胁模型；E9 改述为观察性对比；页脚 NeurIPS 2025 占位被 tex 覆盖。
- **691 止损与增强**：①题名再改为 **"Caliber Drift and Capability Boundaries: An Audit Protocol for Software-Verification Evaluation"**（撞名核查：PROPOR 2026 "Auditing the Evaluators"、ACL Findings 2026 "Evaluator Stress Test"、DeepFact "audit-then-score"、BabelJudge "reliability audit framework"）；②**公式改称"符号消歧"而非"修正"**（`E[J]=kd/n` 是超几何精确均值，`n`=资产池；`k|D|/|A|` 仅为消歧）；③**"三池验证"更正为两池**（Pool B≡C，9 个不同块；唯一改进档 k=4 被重复计数为 3/14）；④**证据搬运**：机制级 k=1 **+11.31pp (p=6.0e-8)**、k=2/k=3 +7.42pp 进 §5.1；四个 κ 全部报告（含未报告的 expected_verdict **0.437**、severity **0.157** 接近随机）；治理计数（**452** 事件 / **67** 规则 / 钉住 ruleset hash）进 §2；⑤**内容减法**：删 67 规则清单节、压缩 673c 材料与方案类附录，全稿 **36→35 页**（附录 23 页）。
- **689 统计补全**（仅确定性复算，无新 detect 运行）：TOST ±10pp **未过**（90% CI [−10.61,+5.52]pp；最小通过 margin 10.61pp）；双向标准化（正向 −17.92pp / 反向 +1.70pp / 类型级 −13.52pp）；环境三组件（真实 59.09%→23.64%、Δunknown=0；clang↔g++ 93.5%、κ=0.864/0.843）。
- **689 人类标注**：去标签材料包 145 条 + 校准集 10 条 + 预注册阈值（verdict κ≥0.8）已备；**human IAA = 0，待执行**（投稿前第一人工项）。
- **689 页数/摘要**：正文 8 页（References 起第 8 页）≤9；全稿 36 ≤36；摘要 245 词 / 1776 字符。

---

## Reviewer 1

**R1.1** `Reviewer: "The paper claims a new evaluation paradigm, but the empirical support is thin."`
**Response:** We agree the first submission was thin on baselines. The revised version reports a **same-sample three-arm contrast**: failure-driven (FD) vs. a static caliber arm vs. a **random-proxy arm**, recomputed by a single script from landed artifacts. Separately, the **budget-matched control (A5) has now run at full scale** (1137 samples × 8 assets = 9096 real `detect` calls; derivation 571 / evaluation 566): FD **54.6%** vs Random **30.6%** (Δ **+24.0pp**, exact McNemar **p=2.3×10⁻⁴¹**, b=136/c=0) and vs Static **24.7%** (+29.9pp) — but the pre-registered parallel analysis collapses to Δ **0.0pp**, so we register it as **direction-only**, not a superiority claim (see "On A5" below).
- FD holdout **82.9%** (34/41) vs. Static **2.4%** (1/41) vs. Random **9.8%** (4/41);
  FD corpus **62.5%** (40/64) vs. Static **17.2%** (11/64) vs. Random **21.9%** (14/64).
- Exact McNemar $p\le3.0\times10^{-8}$; Cohen's $h\ge0.85$; all four paired $\Delta$ CIs strictly positive ($\Delta$ lower bound $\ge$ **28.6pp**). (An e-process layer exists but is **exploratory** — not pre-registered, not used for confirmatory claims — and we no longer quote its e-values as evidence strength.)
- We also state explicitly (§Claim Boundary) which claims remain **unsupported**.
**Change:** §Experiments (Table E1, E5); §Claim Boundary.

**R1.2** `Reviewer: "Why is mutation score not treated as defect detection?"`
**Response:** Because they measure different things. Internal mutation core is **96.5%** (110/114; all-scope **81.8%**, 130/159) — *a repair is in progress (676i: 96.5% → 97.3%), so this reply keeps 96.5% until that lands* — while external corpus measurable recall is **62.5%** (40/64; 52.6% all-sample). We cite Just et al. (FSE 2014), who show mutants are correlated with, but not equivalent to, real faults, and we keep mutation as an **internal self-justification metric only**.
**Change:** §Analysis item 4; §Threats (Construct).

**R1.3** `Reviewer: "The static arm is weak; is this a straw man?"`
**Response:** We agree the static arm is *not* a real static detector, and we say so. It is a **caliber re-binning** (the same raw catches, runtime evidence removed), and the two detection sets' true errors are overwhelmingly visible only through sanitizer (runtime) evidence. So the low static number reflects the **detection sets' dependence on instrumentation**, not the weakness of static analysis. We explicitly refuse to claim "we beat a static detector"; the real `detect_static` interface lives in a split repository and remains missing.
**Change:** §Experiments (§E1 bullet); §Threats (Construct).

---

## Reviewer 2

**R2.1** `Reviewer: "Reproducibility is unclear; the numbers depend on an undeclared environment."`
**Response:** We now declare the **WSL + g++ + `setarch`** dependency in the abstract, §Claim Boundary, and the reproduction appendix, and require a verdict of `UNVERIFIED` (not a misleading low score) when a dependency is missing. We also report the observed silent-drop failure mode (35.0% → 10.0% without WSL) as a *real* threat rather than a residual one.
**Change:** Abstract; §Claim Boundary; Appendix (Reproduction Commands).

**R2.2** `Reviewer: "How does this differ from benchmark-evolution work?"`
**Response:** Benchmark evolution changes the **items**; mutation-guided testing changes the **tests**; formal verification produces **proofs**; MiniCheck changes the **judge's weights**. We change the **verifier's evidence-acquisition capability** itself, and require each step of that change to be **externally measurable and third-party recomputable** — and, uniquely, **self-falsifiable** (ablation A0 − A5).
**Change:** §Related Work (positioning table); §Experiments (ablation protocol).

**R2.3** `Reviewer: "The paper says the random baseline is blocked — then how do you claim an advantage over random?"`
**Response:** The random arm in the **headline two-rate contrast** is an **instrument-level proxy** (holdout **9.8%** (4/41), corpus **21.9%** (14/64); exact McNemar $p=1.9\times10^{-9}$ / $3.0\times10^{-8}$; Cohen's $h=1.65$ / $0.85$). The blocker is now **resolved**: the budget-matched random control (**A5**) has been run at full scale — 1137 samples × 8 assets, FD **54.6%** vs Random **30.6%**, Δ **+24.0pp** (exact McNemar **p=2.3×10⁻⁴¹**, b=136/c=0). We still report a **directional** conclusion rather than a controlled magnitude, but the reason has changed: it is no longer "the arm is missing" but that the effect is **pool composition** — the pre-registered parallel analysis collapses to Δ **0.0pp (p=1.0)**, triggering the `uninterpretable` clause (see "On A5").
**Change:** §Experiments (Table E1/E5); §Analysis (§7.2); §Threats (External).

---

## Reviewer 3

**R3.1** `Reviewer: "Small sample sizes undermine the statistical claims."`
**Response:** We agree, and we now say so in the abstract and §Claim Boundary rather than in a footnote. The measurable sizes are holdout **$n=41$** and corpus **$n=64$**; $\pm$5pp of CI half-width needs $n=236/378$ ($\pm$10pp needs 61/97); a $\Delta=15$pp paired contrast needs $n\approx103$–173, an independent one $\approx170$ per group. We therefore report **direction, intervals and effect sizes**, and explicitly refuse to report magnitude **for the two headline rates**. For the budget-matched A5 contrast the power gap is now **closed**: A5 has been run at **n=566** (≫ the $n\approx138$ paired requirement; see "On A5"), so its magnitude is readable; what remains for A5 is a **non-degenerate pool with $1<k<|A|-1$**, not more samples.
**Change:** Abstract; §Statistical (§7.3); Appendix (sample-size table).

**R3.2** `Reviewer: "McNemar significance rests on an extreme structure (c=0)."`
**Response:** Correct, and we state it. All four contrasts have $c=0$ (the opponent's catches are a subset of FD's), so the significance is carried by the extreme discordant structure; a few reverse pairs would inflate $p$ quickly. We flag this as a residual statistical threat.
**Change:** §Statistical (Table E5 note); §Threats (Statistical).

**R3.3** `Reviewer: "Minor: terminology is inconsistent."`
**Response:** Fixed. We use "detector" throughout; `unknown` and `miss` are kept strictly separate; `Random†` keeps its dagger as an **instrument-level proxy** (the *true* budget-matched B3 now also runs at full scale as A5 — 1137 samples, Δ +24.0pp, p=2.3×10⁻⁴¹ — but the dagger marks that the **reported headline arm** is still the proxy, not that the arm is missing).
**Change:** Whole manuscript.

---

## Standard reusable replies

### On "sample size is too small"
We agree and say so up front. Measurable $n=41$ (holdout) / $n=64$ (corpus); $\pm$5pp half-width needs $n=236/378$; $\Delta=15$pp paired needs $n\approx103$–173. We report **direction** ($\Delta$ lower bound $\ge$ **28.6pp**; exact McNemar $p\le3.0\times10^{-8}$) and **refuse to report magnitude** for the two headline rates. For the budget-matched A5 contrast the expansion has **already happened** ($n=566 \gg 138$), so the remaining limitation there is pool geometry, not power.

### On "the baseline is not strong enough"
Partly correct, and we label precisely. The **static arm is a caliber re-binning**, not a re-run of a real static detector (split-repo `detect_static` still missing) — this is marked and excluded from conclusions. The **random arm in the headline two-rate contrast is an instrument-level proxy**; the *true* budget-matched control (**A5**) has now been **run at full scale** (1137 samples; Δ +24.0pp, p=2.3×10⁻⁴¹), so that item is no longer open — it is reported as **direction-only** because its effect is pool composition. The missing `detect_static` remains an **open item** rather than being substituted by an approximation.

### On "why not evaluate on SWE-bench"
Because our object of study is not code repair but **verification of knowledge claims**. SWE-bench measures whether a model can patch an issue; we measure whether a claim is true under an explicit boundary triple. Adapting SWE-bench would change the construct (Construct validity). We cite the SWE-bench contamination line as **motivation** for external-sample-first design.

### On "reproducibility"
Every headline number is recomputed from landed artifacts by a single command; the environment dependency (WSL + g++ + `setarch`) is declared; a missing dependency yields `UNVERIFIED`. Code is Apache-2.0 with DCO sign-off. Croissant and Responsible-AI metadata are **generated and self-checked** (13/13, `data/682_metadata_selfcheck.json`); the 2027 metadata specification is not yet released, so the shipped form is 2026-conformant.

### On "how do you handle untrusted LLM input / prompt injection"
We register this as an explicit threat (T15). Architectural mitigation: **LLM output never becomes a verdict directly** — every LLM-produced candidate passes a deterministic schema check (field allow-list) before entering the ledger, and ML-based detection only **warns, never blocks**. Prompt-injection can pollute *evidence processing* but not *verdict recomputation*, because verdicts are fully programmatic and checked by a kernel-independent reconciler. We cite a real CVE (CVE-2025-59145, CVSS 9.6) as evidence the threat is live.

### On "data provenance / ethics of the external corpus"
We add an Ethics & Data Provenance note: the external corpus is drawn from public technical sources; we declare its origin, license, and de-identification; human-signed `verified` cards are produced by N annotators with stated compensation; **IRR was not computed (second annotator: 0)** and we register this as the **single largest validity threat** (§7). We have now **pre-registered a remediation protocol**: a two-annotator re-label of a random 25% subsample (10/41 holdout, 16/64 corpus) with the original annotator blinded to the second; agreement measured by **Cohen's κ**, and if κ < 0.6 on any layer we escalate to a **100% re-review**; every disagreement is adjudicated and re-fed into the detection-rate recomputation. It is specified in §7 and will be executed before any "verified" claim. We also note potential dual-use (the system could be studied to evade verification) and argue layered reporting makes evasion more detectable, not less.

### On "9-page limit"
The main text is compressed to the E&D 9-page target (references and appendix excluded). If the camera-ready overflows, we move the sample-size table and the related-work table into the supplement, and merge the two ablation tables (protocol + experiment).

---

### On "label validity / inter-rater reliability (IRR)"
We agree and now say so explicitly in §7 (Threats to Validity), where we name **unreviewed labels** as the **single largest validity threat** to the recall numbers. The 41 holdout + 64 corpus labels were authored by a single annotator and have **no** second-annotator check yet (IRR = 0). We have pre-registered a remediation protocol: a two-annotator re-label of a **random 25% subsample** (10/41 holdout, 16/64 corpus) with the original annotator blinded to the second; agreement measured by **Cohen's κ**, and if κ < 0.6 on any layer we escalate to a **100% re-review** of that layer by a third party. Every disagreement is adjudicated and re-fed into the detection-rate recomputation; the before/after rate delta is reported as a validity residual. This protocol is specified in §7 and will be executed before any claim of "verified" status. Until it runs, all detection rates carry this unresolved residual.

### On "A5 / the core-mechanism falsification experiment"
A5 (random-budget control) has now **run at full scale** (1137 samples; derivation 571 / evaluation **566 ≫ 138**): at k=4 over the full 8-asset pool, FD **54.6% (309/566)** vs. Random **30.6% (173/566)** vs. Static **24.7% (140/566)**; Δ(FD−Random) **+24.0pp** (CI [+20.5, +27.5], exact McNemar **p=2.3×10⁻⁴¹**, b=136/c=0, h=0.49) and Δ(FD−Static) **+29.9pp** (p=1.9×10⁻³¹); FD is strictly better than the single-seed draw in **97.6%** of 2000 resamples. **But it still does not license "FD beats Random":** the effect is **pool composition** — 2 of 8 assets (`wunsequenced`, `compile-time`) are constant-`unknown` over all 1137 samples, so half of Random's budget is spent on zero-information assets; in the pre-registered *parallel* analysis excluding them the **Δ collapses to 0.0pp (p=1.0)** while the **Static gap grows to +30.6pp (p=8.1×10⁻³⁴)** — i.e. what A5 identifies is "do not fund assets that cannot inform," **and the `uninterpretable` clause is triggered again**. The parallel analysis is nonetheless significant at k=1–3 (+11.31/+7.42/+7.42pp), pinning the *selection* effect at **≈ +7–12pp**. **Two follow-up analyses (677b/677c) are now in the paper.** (i) *Template leakage*: our samples are not independent — 1137 samples fall into **474 template families** (420 connected components), and under the original split **64.5% of evaluation samples had a family sibling in the derivation split**; re-splitting at the family level (three strategies, including a strict variant with **zero** clone pairs crossing) leaves the endpoint **unchanged** (+23.0 to +26.7pp, p ≤ 4.1×10⁻²⁹) and the parallel analysis at ≈0 — so leakage is **not** driving it — while a family-level cluster bootstrap gives a design effect of **≈4.1–4.3**, i.e. an **effective n≈133–140** and Δ cluster CIs of [+16.6,+30.4] / [+18.3,+33.4]pp (1.78–2.10× wider, still excluding 0); with the random arm also re-drawn, the lower bound reaches 0 (Δ≤0 in 2.2–3.0% of replicates), which is why we keep the claim directional. (ii) *Degenerate assets*: on the strict non-degenerate pool (5 assets, none pre-registered degenerate) the effect **survives at k=1/2/3** (best k=1: 33.04% vs 21.73%, **+11.31pp**, p=6.0×10⁻⁸), the **k=4 zero is a set collision** (both arms must draw the same four of five, probability 0.2 — not evidence against the mechanism), and the degenerate assets account for **+24.03pp** of the single-point k=4 Δ (**+12.81pp** vs the 2000-draw mean), leaving an isolated selection effect of **≈ +7–12pp**. We therefore still write no "FD > Random" sentence; we now report **+24.0pp (full pool) and +7–12pp (degenerate-free) side by side**. Roadmap (changed): the power gap is **closed** and the non-degenerate pool **has run**; what remains is **A0–A4** plus multi-round (modal) verdicts, and reporting A5 intervals at the cluster width (effective n≈133–140). Separately, we now publish a **capability-boundary map** of our own instrument (1147 samples; blind-spot ratio **38.4%**; **18 of 70** types >50% blind; family gradient memory 15.2% → link/ODR 67.7%), so every recall number is explicitly scoped to the *visible* region — and we register a measured **~5% run-to-run flip rate** on single-cell verdicts as a first-class limitation.

## 落款

> We thank the reviewers again; the revised version addresses every point, and every remaining gap is registered rather than hidden.

---

## 高频审稿问题（5 条，676f 版）

### Q1. Sample size is still small (41/64)
We agree and say so up front. Measurable $n=41$ (holdout) / $n=64$ (corpus); $\pm$5pp half-width
needs $n=236/378$, and a $\Delta=15$pp paired contrast needs $n\approx103$–173. Beyond intervals we
add an **e-process** layer: cumulative e-values multiply per item and stay anytime-valid, so the
expansion protocol does not need re-calibration. It is **exploratory** (μ₀, alternative grid and
mixing prior not pre-registered) and we therefore do **not** use e-values as evidence strength; the
layer is reported in an appendix marked as such. We report **direction** and **refuse to report
magnitude** for the two headline rates. For the budget-matched A5 contrast the expansion has
**already happened** ($n=566 \gg 138$; Δ +24.0pp, p=2.3×10⁻⁴¹), so the remaining limit there is
pool geometry, not power.

### Q2. The LLM arm result contradicts your expectation
Correct, and we register it as a **negative result**. GLM-4 caught 12/12 errors (vs. FD's 6/12 on the
same subset) but produced **4/8 false positives (50%)** on controls: *more sensitive, far less
specific*. All four pre-registered hypotheses failed. Two caveats are stated: some samples carry
`answer_leak_risk`, and it is a single model on a single prompt. The result is exactly why our
architecture keeps "LLM output never becomes a verdict".

### Q3. The external anchor's H2 did not pass
Yes — **H2 misses by 0.8pp** and is registered as **not passed**: H2 required the reconstructed-UB
subset (80.0%) to differ from the corpus historical reference (54.2%) by **< 25pp**, but the observed
difference is **25.8pp**. The two subsets are reported separately because their targets differ:
verbatim guideline snippets 28.6% (most guideline text is stylistic advice, so "no detection" is
expected) and reconstructed UB fragments 80.0% (our own reconstruction, hence an upper bound). A
harness was added post-registration and the deviation is logged. (The 50-snippet total rate of
**44.0%** belongs to H3, which passed at ≥30%.)

### Q4. How does this differ from related work?
Benchmark evolution changes the **items**; mutation-guided testing changes the **tests**; formal
verification produces **proofs**; MiniCheck changes the **judge's weights**; CELEUS uses e-processes
to **save samples**. We change the verifier's **evidence-acquisition capability** and require each
step to be externally measurable and **self-falsifiable** (A0 − A5). The four-state verdict is the
information-theoretic projection of Belnap's four-valued logic, and auditability rests on Merkle
roots plus a kernel-independent reconciler.

### Q5. Reproducibility
Every headline number is recomputed from landed artifacts by a single command; the environment
dependency (WSL + g++ + `setarch`) is declared and a missing dependency yields `UNVERIFIED` rather
than a misleading low score. Statistical plans were pre-registered before the reveals, results were
recomputed through two independent paths (differences < 0.1pp), and the repository is Apache-2.0
with DCO sign-off. Croissant and Responsible-AI metadata are generated and self-checked (13/13,
`data/682_metadata_selfcheck.json`).
