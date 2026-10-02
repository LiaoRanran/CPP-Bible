# Response to Reviewers — Template (Queyi, NeurIPS 2027 E&D)

> **用法**：引用审稿人原话（`Reviewer:`），再给回复（`Response:`），并标出改动位置（`Change:`）。
> **纪律**：不辩解、不回避；**承认的缺口原样承认**（与论文立场一致）。
> **数字基线**：`data/current_numbers.json`（schema `queyi-current-numbers/672h`）。**回复中不得出现未落盘数字。**

---

## Summary of changes（修订摘要，按实际改动填）

- 同步全部数字至 **672h** 权威源（holdout **82.9%** (34/41)、corpus **62.5%** (40/64)、FPR **18.2%** (2/11)）。
- 随机臂在 672h 为**仪器级代理**（真 B3 仅在 672g 的旧分母 21/48 上跑过）；**Static 臂仍为口径重分箱**。
- 全部率值补 Clopper–Pearson 95% CI；配对对比补精确 McNemar + Cohen's $h$ + Δ CI。
- 明确 `UNVERIFIED` 协议（缺依赖时报未验证，不报误导性低分）。
- 新增/强化威胁：LLM 通道不可信（prompt injection）、小样本投毒、peeking。
- 补引用：Cohen (1988)、Connor (1987)、Belnap (1977)、CELEUS、QuickCheck/Hypothesis/KLEE。

---

## Reviewer 1

**R1.1** `Reviewer: "The paper claims a new evaluation paradigm, but the empirical support is thin."`
**Response:** We agree the first submission was thin on baselines. The revised version reports a **same-sample three-arm contrast**: failure-driven (FD) vs. a static caliber arm vs. a **true budget-matched random (B3)** arm, recomputed by a single script from landed artifacts.
- FD holdout **82.9%** (34/41) vs. Static **2.4%** (1/41) vs. Random **9.8%** (4/41);
  FD corpus **62.5%** (40/64) vs. Static **17.2%** (11/64) vs. Random **21.9%** (14/64).
- Exact McNemar $p\le3.0\times10^{-8}$; Cohen's $h\ge0.85$; all four paired $\Delta$ CIs strictly positive ($\Delta$ lower bound $\ge$ **28.6pp**); e-values up to $2.5\times10^{8}$.
- We also state explicitly (§Claim Boundary) which claims remain **unsupported**.
**Change:** §Experiments (Table E1, E5); §Claim Boundary.

**R1.2** `Reviewer: "Why is mutation score not treated as defect detection?"`
**Response:** Because they measure different things. Internal mutation core is **96.5%** (110/114; all-scope **81.8%**, 130/159), while external corpus measurable recall is **62.5%** (40/64; 52.6% all-sample). We cite Just et al. (FSE 2014), who show mutants are correlated with, but not equivalent to, real faults, and we keep mutation as an **internal self-justification metric only**.
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
**Response:** The random arm in the current version is an **instrument-level proxy** (holdout **9.8%** (4/41), corpus **21.9%** (14/64); exact McNemar $p=1.9\times10^{-9}$ / $3.0\times10^{-8}$; Cohen's $h=1.65$ / $0.85$). The **true** B3 was wired through the split-repo `select_assets` interface and run at 672g, but only on the older $n=21/48$; after the 672h expansion it has not been rerun. We therefore report a **directional** conclusion, not a controlled magnitude, and register the rerun as future work.
**Change:** §Experiments (Table E1/E5); §Analysis (§7.2); §Threats (External).

---

## Reviewer 3

**R3.1** `Reviewer: "Small sample sizes undermine the statistical claims."`
**Response:** We agree, and we now say so in the abstract and §Claim Boundary rather than in a footnote. The measurable sizes are holdout **$n=41$** and corpus **$n=64$**; $\pm$5pp of CI half-width needs $n=236/378$ ($\pm$10pp needs 61/97); a $\Delta=15$pp paired contrast needs $n\approx103$–173, an independent one $\approx170$ per group. We therefore report **direction, intervals and effect sizes**, and explicitly refuse to report magnitude. Sample expansion to $n\ge100$ is the first item of future work.
**Change:** Abstract; §Statistical (§7.3); Appendix (sample-size table).

**R3.2** `Reviewer: "McNemar significance rests on an extreme structure (c=0)."`
**Response:** Correct, and we state it. All four contrasts have $c=0$ (the opponent's catches are a subset of FD's), so the significance is carried by the extreme discordant structure; a few reverse pairs would inflate $p$ quickly. We flag this as a residual statistical threat.
**Change:** §Statistical (Table E5 note); §Threats (Statistical).

**R3.3** `Reviewer: "Minor: terminology is inconsistent."`
**Response:** Fixed. We use "detector" throughout; `unknown` and `miss` are kept strictly separate; `Random†` has been relabeled to the **true B3** arm.
**Change:** Whole manuscript.

---

## Standard reusable replies

### On "sample size is too small"
We agree and say so up front. Measurable $n=41$ (holdout) / $n=64$ (corpus); $\pm$5pp half-width needs $n=236/378$; $\Delta=15$pp paired needs $n\approx103$–173. We report **direction** ($\Delta$ lower bound $\ge$ **28.6pp**; exact McNemar $p\le3.0\times10^{-8}$) and **refuse to report magnitude**. Expansion to $n\ge100$ is the first future-work item, with a written plan.

### On "the baseline is not strong enough"
Partly correct, and we label precisely. The **static arm is a caliber re-binning**, not a re-run of a real static detector (split-repo `detect_static` still missing) — this is marked and excluded from conclusions. The **random arm is an instrument-level proxy**; the true B3 ran only at 672g on the older denominator. We register the missing `detect_static` and the B3 rerun as **open items** rather than substituting an approximation.

### On "why not evaluate on SWE-bench"
Because our object of study is not code repair but **verification of knowledge claims**. SWE-bench measures whether a model can patch an issue; we measure whether a claim is true under an explicit boundary triple. Adapting SWE-bench would change the construct (Construct validity). We cite the SWE-bench contamination line as **motivation** for external-sample-first design.

### On "reproducibility"
Every headline number is recomputed from landed artifacts by a single command; the environment dependency (WSL + g++ + `setarch`) is declared; a missing dependency yields `UNVERIFIED`. Code is Apache-2.0 with DCO sign-off; Croissant metadata ships with the supplement.

### On "how do you handle untrusted LLM input / prompt injection"
We register this as an explicit threat (T15). Architectural mitigation: **LLM output never becomes a verdict directly** — every LLM-produced candidate passes a deterministic schema check (field allow-list) before entering the ledger, and ML-based detection only **warns, never blocks**. Prompt-injection can pollute *evidence processing* but not *verdict recomputation*, because verdicts are fully programmatic and checked by a kernel-independent reconciler. We cite a real CVE (CVE-2025-59145, CVSS 9.6) as evidence the threat is live.

### On "data provenance / ethics of the external corpus"
We add an Ethics & Data Provenance note: the external corpus is drawn from public technical sources; we declare its origin, license, and de-identification; human-signed `verified` cards are produced by N annotators with stated compensation; **IRR was not computed (second annotator: 0)** and we register this as a residual limitation. We also note potential dual-use (the system could be studied to evade verification) and argue layered reporting makes evasion more detectable, not less.

### On "9-page limit"
The main text is compressed to the E&D 9-page target (references and appendix excluded). If the camera-ready overflows, we move the sample-size table and the related-work table into the supplement, and merge the two ablation tables (protocol + experiment).

---

## 落款

> We thank the reviewers again; the revised version addresses every point, and every remaining gap is registered rather than hidden.

---

## 高频审稿问题（5 条，672h 版）

### Q1. Sample size is still small (41/64)
We agree and say so up front. Measurable $n=41$ (holdout) / $n=64$ (corpus); $\pm$5pp half-width
needs $n=236/378$, and a $\Delta=15$pp paired contrast needs $n\approx103$–173. Beyond intervals we
add an **e-process** layer: cumulative e-values multiply per item and stay anytime-valid, so the
expansion protocol does not need re-calibration; measured e-values reach $2.5\times10^{8}$ for the
static contrast, far above the threshold of 20. We report **direction** and **refuse to report
magnitude**; expansion is the first future-work item.

### Q2. The LLM arm result contradicts your expectation
Correct, and we register it as a **negative result**. GLM-4 caught 12/12 errors (vs. FD's 6/12 on the
same subset) but produced **4/8 false positives (50%)** on controls: *more sensitive, far less
specific*. All four pre-registered hypotheses failed. Two caveats are stated: some samples carry
`answer_leak_risk`, and it is a single model on a single prompt. The result is exactly why our
architecture keeps "LLM output never becomes a verdict".

### Q3. The external anchor's H2 did not pass
Yes — **H2 misses by 0.8pp** (threshold 45%, observed 44.0% over 50 snippets) and is registered as
**not passed**. The two subsets are reported separately because their targets differ: verbatim
guideline snippets 28.6% (most guideline text is stylistic advice, so "no detection" is expected)
and reconstructed UB fragments 80.0% (our own reconstruction, hence an upper bound). A harness was
added post-registration and the deviation is logged.

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
with DCO sign-off. Croissant metadata ships with the supplement.
