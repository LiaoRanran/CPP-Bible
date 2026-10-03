# 673s · Rebuttal 预演（Rebuttal Preparation）

- 批次：673s（论文卓越打磨 —— rebuttal 预演）
- 仓库：`C:\CodeLearnling\note\note\C++\CPP-Bible`
- 目标稿件：`research/latex/queyi_neurips2027_v1.1.tex`（英文稿）+ `research/paper_shturl.md`（中文稿）
- 权威数字源：`data/current_numbers.json`（schema `queyi-current-numbers/672h`）、`data/experiments/reveal_update_672h.json`、`data/experiments/a5_673p.json`

## 0 · 使用纪律（三步走）

1. **三段式**：每问都写成 `Concede（承认点） / Already addressed（已做修订） / Plan（未来工作）`。英文段落可直接粘贴进 rebuttal；中文是策略提示，不投出去。
2. **不含新数字**：除 Q1 的探索性派生集结果（标 `exploratory`、有 artifact）外，rebuttal 不得引入正文与 672h 权威源之外的任何数字。红线：**不把未做的实验写成已做**。
3. **诚实优先**：凡是论文已自认的缺口（A5 未跑、标签零复核、scope 0/26、历史钉定不完整），rebuttal 一律先说"我们同意"，再给已落地修订，最后给路线图——**不要辩护式反驳**。评审对"承认 + 已修 + 路线"的接受度远高于"辩解"。

## 1 · 评审已知事实（写 rebuttal 时的事实底座）

| 项目 | 现值（672h 口径） | 出处 |
|---|---|---|
| holdout（expanded） | 82.9% (34/41) [67.9, 92.8] | `reveal_update_672h.json::holdout.after` |
| holdout（primary pre-reveal blind） | 81.0% (17/21) [58.1, 94.6] | 同上 `holdout.primary_blind` |
| corpus（measurable） | 62.5% (40/64) [49.5, 74.3] | `reveal_update_672h.json::corpus.after` |
| corpus（all-sample） | 52.6% (40/76) | 同上 |
| static arm | 2.4% / 17.2%（**caliber re-binning，非重跑**） | 同上 `static` |
| random† proxy | 9.8% / 21.9%（**instrument-level proxy，非真 B3**） | 同上 `random_proxy` |
| Δ(static→FD) | +80.5pp / +45.3pp | 同上 |
| exact McNemar | p ≤ 3.0×10⁻⁸（最低下界（Δ）≥ 28.6pp） | 同上 |
| 派生集探索（**exploratory**） | holdout FD 85.0% (17/20) vs random 10.0% (2/20)；corpus FD 87.5% (14/16) vs random 37.5% (6/16) | `a5_673p.json::exploratory_derivation_split` |
| 样本量要求 | Δ=15pp 需 n≈138（paired）/170（independent）；±10pp 需 n≈104；±5pp 需 n≈236/378 | `tab:samplesize` |
| VC / 变异 | 31/42 = 73.8% [58.0, 86.1]；core 96.5% (110/114) / all-scope 81.8% (130/159) | `current_numbers.json` |

---

# Part I · Q1–Q5（14 点评审的主问题）

## Q1 · "核心主张（failure-driven 优于同预算随机）没有被检验：A5 没有跑。"

**Concede.** We agree, and we state it in the paper rather than hide it: the core mechanism is *not* confirmation-tested. §6.4, §7 and §10 record A5 as **BLOCKED**, with two independent reasons: (i) sample size — at n=41/64 the contrast cannot yield an interpretable Δ; (ii) instrument fidelity — a confirmatory A5 requires the split-repo verifier to expose a **true asset pool**, whereas this repository offers only an instrument-level proxy, and our own protocol forbids reading a main-repository Δ as confirmatory. Running it here could not license the very claim it tests.

**Already addressed.** The falsifier is *pre-registered with a decision rule*: "if the CI of Δ(A0−A5) crosses 0, then 'failure-driven beats same-budget random' does not hold" (§6.4). The paper's E1 contrasts are explicitly labelled as **directional** (static = caliber re-binning; random† = instrument-level proxy), not as the A0−A5 result. §10 lists A0−A5 as the top future-work item, and Table `tab:e4` carries per-group hypotheses with `{{TODO_ablation_*}}` placeholders instead of invented numbers.

**Plan / preliminary evidence.** The A5 design is frozen and versioned (`data/673p_a5_preregistration.json`; runner `tools/run_a5_experiment_673p.py`): same-sample, **budget-matched** (anchor = the 4 assets FD actually used on catches, cost-matched), 2000-seed distribution for the random arm, exact McNemar for the paired contrast, single-attribution replay with a declared *bias direction*. As *preliminary and explicitly non-confirmatory* evidence we additionally ran an **exploratory derivation split** (`a5_673p.json::exploratory_derivation_split`): derive the failure-hits asset set on the **old** samples, then evaluate on the **new** samples — turn FD into a genuine predictor. On holdout: FD-derived **85.0% (17/20)** vs random **10.0% (2/20)** (Δ=75pp, exact McNemar p=6.1×10⁻⁵, h=1.70); on corpus: **87.5% (14/16)** vs **37.5% (6/16)** (Δ=50pp, p=7.8×10⁻³). **We label this `exploratory`, not confirmatory**: derivation and evaluation are a time split from the same fixture policy, and the resulting distribution drift is exactly what our H4 subset check already registers (corpus +33.3pp, outside the pre-registered range). It is evidence *about direction*, and we do not place it in the claim table.

> 中文要点：先认（A5 没跑，论文已写 BLOCKED），再亮已落地（预注册 + 决策规则 + 占位符诚实），最后给"设计 + 探索性初步证据"。派生集结果是本批唯一的"新弹药"，务必每次带 `exploratory / non-confirmatory` 标签与 artifact 路径。

## Q2 · "82.9% 不是 blind：41 个 holdout 里只有 21 个是严格盲的。"

**Concede.** Correct, and v1.1 already splits it: only **21** samples are strictly pre-reveal blind; the remaining **20** were merged *after* reveal and carry **no blind state**. The headline 82.9% (34/41) must not be read as a blind rate.

**Already addressed.** The abstract, §6.1, Table `tab:e1`, the Threats table (External layer) and Table `tab:claim` all carry the same split: **primary pre-reveal blind 81.0% (17/21, [58.1, 94.6])** vs **expanded 34/41 = 82.9% [67.9, 92.8]**, with the 20 post-reveal additions named. The expansion is read as **composition change, not capability gain**: `81.0→82.9` is decomposed into new-subset (17/20) vs historical (17/21), and the pre-registered **H4 subset-consistency check passes for holdout (+4.0pp) but fails for corpus (+33.3pp)** — the latter is registered as a composition shift rather than quietly absorbed. The same discipline applies to corpus: 62.5% (40/64) measurable is reported alongside 52.6% (40/76) all-sample, never merged.

**Plan.** Future expansions will be **irreversibly blinded before reveal** (a fresh split, since a revealed holdout cannot be re-blinded), and the **primary blind subset will be the main estimand** with the expanded sample reported as a sensitivity. Blinding state per sample is already stored in the artifact (Denominator/caliber fields), so this is a protocol change, not a re-engineering.

> 中文要点：Q2 是"最容易翻车"的一问——评审已经点破，所以绝不能把 82.9% 说成 blind。一定要主动引 81.0%（17/21）这个 primary blind 数，并强调 H4 corpus 失败已登记（这一步能大幅加分，因为它证明我们在自查）。

## Q3 · "Belnap 形式化是装饰性的，甚至范畴错误。"

**Concede.** We agree the *encoding itself* is not novel, and v1.0's framing mixed two different things (a truth pair *and* detector availability). The paper now says so explicitly: "we claim no novelty in the four-state encoding itself" and "we give no theorems and no proofs" (Contribution 2 / §3).

**Already addressed.** v1.1 rewrites the four states as a **Belnap state (support, refutation) over registered evidence**: `pass=(1,0)`, `fail=(0,1)`, `unknown=(0,0)`, `contradict=(1,1)` — i.e. `contradict ≡ Both`, `unknown ≡ None` in Belnap's four-valued logic. **Detector availability is demoted to separate per-item metadata**, not part of the Belnap state. This is stated identically in Contribution (2), §3 ("Why four states"), the formal definitions (§4) and Definition 4. The three evolution properties (monotonicity / minimality / auditability) are presented as **checkable design constraints we have not verified rule-by-rule**, not as proven theorems.

**Plan.** The concrete testable content is the *caliber consequence*, and that is fully reported: because `unknown` is `(0,0)`, merging it into `miss` pollutes the denominator and merging it into `pass` manufactures false confidence, so the primary estimand conditions on measurable samples — and we report **all three denominators** (62.5% / 54.8% / 52.6%) so readers can see the 9.9pp swing rather than pick one.

> 中文要点：不要辩护"形式化很有价值"——直接让步"编码不新颖"，把价值锚在可检验的口径后果上（三口径全报）。评审讨厌"用数学装饰"，喜欢"数学导致一个可检验的后果"。

## Q4 · "Auditability 号称可重演，但历史状态其实不可重演。"

**Concede.** Agreed. Current-state auditability holds; **historical** auditability does not. The 452 ledger events do not carry a ruleset hash, so reconstructing a historical verdict assumes the ruleset was unchanged; and the guard compares artifacts to the frontend **without re-running detectors**, so the 81.2% incident can recur.

**Already addressed.** v1.1 downgrades the claim *consistently* in the abstract, Contribution (3), §4 and §8: origin traceability / state reproducibility / tamper detectability are met "**for the current state** only", with the pinning gap stated in the same sentence. Appendix `app:pinning` gives the measured state (`rules_manifest_sha256` exists, version 1.0.0, 67 rules; **the 452 events do not yet carry the field**), and Appendix `app:future` lists "make the guard re-run detectors" as an explicit item. The paper also records the 81.2% incident as an *observed* failure rather than a hypothetical.

**Plan / roadmap (ruleset hash into the ledger).** The manifest hash is already computed and archived append-only; the remaining work is mechanical: (1) backfill the 452 events to **double-reference** `rules_manifest_sha256` and the evidence-toolchain snapshot; (2) make each event pin the hash *at verdict time*, so a third party reconstructs the exact ruleset; (3) add a **fail-loud** environment/self-check to the reproduction scripts so a wrong environment raises instead of silently degrading 15 samples to `unknown`; (4) make the guard re-run detectors so caliber/measurement divergence cannot stay green. Until (1)–(2) land, we keep the claim at "current state reproducible, historical pinning partial" — we do not upgrade it.

> 中文要点：这是"你已经在论文里修了、只需在 rebuttal 里指路"的一问。路线图要**具体到可执行步骤**（回填 hash、verdict-time pin、fail-loud、guard 重跑），并把"不升级主张"这句话说出来——评审会注意到这种节制。

## Q5 · "新颖性不足：已有工作也在演化评估器 / 度量。"

**Concede.** We agree and say so in the paper: "**we do not claim to be the first to evolve an evaluator.**" Prior lines evolve the items (Benchmark Self-Evolving, ArenaBencher, LiveBench), the tests (ACH, MUTGEN, Cleverest), the proofs (seL4, CompCert), the judge (MiniCheck), the metric (*Who Grades the Grader?*), or agent harnesses with gates (*Self-Evolving Agents with Anytime-Valid Certificates*).

**Already addressed.** v1.1 adds §2(6) on program analysis / symbolic execution / property testing — explicitly conceding that "**driving evidence acquisition from failure or non-coverage is therefore not our invention**" (KLEE/SymCC by uncovered branches; QuickCheck/Hypothesis by counterexamples; abstract interpretation as a lattice element) — and §2(7) on the two closest 2026 works: **Who Grades the Grader? (arXiv:2607.12790)**, which evolves the *metric* against Goodhart drift via anchors/external audits, and **Self-Evolving Agents with Anytime-Valid Certificates (arXiv:2607.00871)**, a versioned harness with an anytime-valid auditable gate.

**Our specific boundary.** Our claim is narrower than "evolving an evaluator": we evolve the verifier's **evidence-acquisition capability C** in an **executable C++ assertion setting**, and we keep three things **explicitly separated** that prior work couples — (a) **detector availability** (metadata, never a verdict), (b) **semantic scope** vs **provenance** (forced split), and (c) the recomputable **failure → rule → re-test** chain. We also position eight works along five dimensions (Table `tab:positioning`): prior lines evolve items/tests/proofs/judge/metric; we evolve evidence-acquisition capability and require each step to be externally measurable. We do **not** claim superiority over real static detectors (our comparison is a *cross-regime stress test*, E9) or over a true budget-matched random baseline (A5 unrun).

> 中文要点：新颖性答辩的关键不是"我是第一个"，而是"我把哪三件事**显式分离**了、演化的对象具体是什么"。用"更窄但更清晰"换"更大但更脆"的 claim。E9 的定位（互补缺陷区间，非全面优于）必须在这一问里重申，否则会被连环追问。

---

# Part II · 额外 10 问（可预期追问）

## Q6 · "为什么不用 LLM judge？LLM 不是更敏感吗？"

**Concede.** It is more sensitive: on the paired arm GLM-4 caught **12/12** errors vs FD's 6/12, and exact McNemar favours the LLM (b=0, c=6, p=0.031).

**Already addressed.** But it produced **4/8 false positives (50%)** on controls — *more sensitive, far less specific*; **all four pre-registered hypotheses failed**. We also refuse the stronger claim: some samples carry `answer_leak_risk`, the arm is one model on one prompt, and we **removed its significance test** because n=20 on a non-random subset with p=0.031 does not support the word "significant". Architecturally, the LLM may **propose** candidates but its output **never becomes a verdict** (T15) — otherwise judge and judged share a failure domain.

**Plan.** An LLM arm can be added as a *proposer* whose suggestions must pass the same programmatic gate; the paper's claim boundary does not depend on it.

> 中文要点：这一问评审想确认"你不是不会用 LLM，而是有意不用"。要主动引 E7 的 50% FPR 和"LLM 只 propose、永不 verdict"的架构规则，并主动交代 `answer_leak_risk` 这个瑕疵。

## Q7 · "为什么选 C++？结论能推广到别的语言吗？"

**Concede.** It cannot be assumed to transfer, and we say the evidence does **not** support generalization (Table `tab:claim`: "not supported — other languages").

**Already addressed.** C++ is chosen because its UB/deep-semantics errors are *numerous, plausible and quietly wrong*, and because they are **detector-friendly** — which is also the honest limitation: because C++ UB is among the most instrument-visible problem classes, our rates **will likely not transfer** to languages without a comparable sanitizer/UB story. The environment dependence is fully disclosed: the local MinGW-w64 toolchain ships **no UBSan runtime**, so both headline rates were produced inside WSL; macOS has no `setarch` at all.

**Plan.** The method is language-agnostic in principle (assertion = decidable statement + boundary triple; evidence = replayable observation), so transferring it requires a language-specific evidence-acquisition layer, not a new framework. We flag this as an open external-validity question rather than a claim.

> 中文要点：把"为什么 C++"答成两段——(1) 因为 UB 类错误天然符合"多/貌似对/悄悄错"；(2) **也正因为 UB 好抓，所以别指望外推**。后者是加分项。

## Q8 · "主口径条件于'可测样本'，这隐含了 missingness 与缺陷类型无关——这个假设成立吗？"

**Concede.** We agree this is an assumption, and v1.1 states it explicitly rather than hiding it (P1-6 revision): conditioning on measurable samples assumes the `unknown` set is not systematically different in defect type from the measured set. If it is, the estimate is biased, and we do not know its direction.

**Already addressed.** The paper (a) names the assumption in Contribution (2)/§4, (b) reports **all three denominators** so the reader can see the whole admissible range (holdout 82.9/81.0/81.0; corpus **62.5/54.8/52.6**, a 9.9pp swing), and (c) frames the alternative denominators as answering *different questions* rather than as universally wrong.

**Plan.** A direct test is cheap and pre-registerable: compare the defect-type composition of `unknown` vs measured samples; if the layers differ, report a **stratified** estimate per defect layer (we already report sanitizer/compiler-warn/cross-compile layers separately) and treat the marginal rate as a weighted average with an explicit missingness model. Until then the marginal rate is conditional, and the caliber travels with every number in the artifact.

> 中文要点：这是一问"统计学素养探测"。答法：承认假设 → 用"三口径 + 分层"证明我们已经把风险可读化 → 给一个便宜的可证伪测试。

## Q9 · "n 太小，这些百分比没有意义。"

**Concede.** We agree: n=41/64 measurable is small, CIs are wide (a ≈12pp half-width), and we explicitly forbid reading magnitudes as exact ("read direction first, magnitude second").

**Already addressed.** The paper carries the recomputed power table (`tab:samplesize`): Δ=15pp needs n≈138 (paired, ψ=0.4) / ≈170 per group (independent); ±10pp needs n≈104; ±5pp needs n≈236/378. The pre-registered rule is *if the difference CI crosses 0 the mechanism does not hold*, and all four Δ CIs are strictly positive (lowest bound **28.6pp**). McNemar's small-sample fragility is stated: significance rests on the extreme **c=0** structure, and a few reverse pairs would inflate p quickly — indeed E9 supplies 8 reverse pairs against static tools on corpus, where FD only **ties** cppcheck (Δ=+7.8pp, CI crosses 0).

**Plan.** Expansion toward n≥100 is future work item (i); the target is stated in the same units the criticism uses (n, not adjectives). We would rather report a wide CI than a narrow claim.

> 中文要点：**主动报出功效表**是这一问的杀手锏——评审说"样本小"，你若先给出"我们算过需要多少 n"就赢了。务必带 E9 的 8 个 reverse pairs 与 corpus 打平，证明我们不是只挑赢的场子报。

## Q10 · "标签是谁标的？有几人复核？"

**Concede.** Labels are **self-produced with zero second annotators** (41 holdout + 64 corpus); there is no IRR, and the bias direction is unknown. This is registered as **T17**, the largest threat to the recall numbers.

**Already addressed.** v1.1 adds T17 explicitly, states it in the abstract's limitations and in the Threats section, and explains why it is upstream of everything: a mislabelled sample moves a rate silently in either direction, and the shared-criterion $F_1{=}1.0$ case is an **upper bound** by construction.

**Plan.** A pre-registered two-annotator re-label of a random 25% subsample (10/41, 16/64) with the original annotator blinded, and κ<0.6 escalating to a 100% third-party re-review — **before any "verified" claim**. Machine cards are already `needs_review=true` and never counted as verified; `verified` is human-signed only.

> 中文要点：不要试图说"标签没问题"。把 T17 与"已验证状态只由人签"的机制连起来，然后给**预注册的复核方案**（含 κ 阈值）。

## Q11 · "结果依赖特定 WSL 环境，这不等于不复现吗？"

**Concede.** Effectively yes, **today it is conditional reproduction**: without the specific WSL environment, 15 samples degrade to `unknown` and external recall falls **35.0%→10.0%** while the guard stays **green** — because the guard compares artifacts to the frontend, not to a real machine. A replicator could obtain 10% and write it into a review with nothing warning them.

**Already addressed.** This is stated as an *observed* failure (not a residual): Analysis (2), the Threats table (Temporal/External layers), and the Claim Boundary's "Not reproducible" row. The `app:humanize` section documents why WSL is required (MinGW-w64 has no UBSan runtime; macOS lacks `setarch`) and the CRLF/437-file hash-drift incident.

**Plan.** A **fail-loud environment self-check** in the reproduction scripts (raise on wrong environment instead of degrading silently), plus explicit macOS / Windows-native non-reproducibility statements, is future-work item (vii). We do not claim the numbers reproduce anywhere but in the declared environment.

> 中文要点：这是"可复现性"最硬的一击。诚实答法：**"我们的复现是条件复现"**——然后给出 fail-loud 自检这一具体修法。注意别把 35.0→10.0 说成"小问题"，它是一条能毁掉整篇论文的复现链。

## Q12 · "和 clang-tidy / cppcheck 的对比公平吗？"

**Concede.** It is **not** a same-environment, apples-to-apples capability ranking, and the paper says so: clang-tidy (LLVM 22.1.8) runs Windows-native and syntax-level, cppcheck 2.13.0 runs under WSL, FD uses WSL g++ **runtime** evidence — three different environments. The pre-registered main caliber **failed** (100% recall *and* 100% FPR on holdout, zero discrimination), and the reported StrictA caliber is **chosen after results**, hence exploratory.

**Already addressed.** E9 is retitled a **cross-regime external stress test** and its conclusion is "the two families cover **complementary** defect regimes", with an explicit denial: "not evidence that FD generally outperforms static analysis". On corpus FD only **ties** cppcheck (54.7%, p=0.383), and the **8 reverse pairs** (compile-time-visible / path-not-executed defects) are named individually in `app:clangtidy` rather than summarised away.

**Plan.** A true comparison requires a common environment and a pre-registered caliber; we treat that as future work and do not use E9 as evidence of superiority. (This also connects to Q5: E9 is a positioning stress test, not our headline.)

> 中文要点：这一问的正确答案几乎全是"承认"。**主动列出 8 个 reverse pair 和 corpus 打平**是可信度来源——评审会因为你敢报逆例而下调敌意。

## Q13 · "缺陷是你们自己植入的，这不是自己出考卷吗？"

**Concede.** Yes — this is the "setting your own exam" circularity, registered as **T2** and **T17**, and it is why we do not claim generalization to unseen error types: all samples are same-source and semantic scope backfill is **0/26**.

**Already addressed.** Three externalization layers exist even if each is imperfect at these sizes: **D2 blind holdout** (planted defects invisible pre-reveal), **D3 external corpus** (real statements from outside the repo), and the **E8 external anchor** (official C++ Core Guidelines, 44.0% over 50 snippets, with the verbatim subset at 28.6% *expected* to be low because most guideline text is stylistic advice). We report where each layer is weak (post-reveal additions; reconstructed UB subset is our own and therefore an upper bound).

**Plan.** Third-party-authored defect sets and a language-agnostic replay are future work; the construct-validity gap (higher VC ⇏ better verdicts) is listed under "believed but not adequately verified".

> 中文要点：把"自造缺陷"与"scope 0/26"绑在一起承认，然后展示三层外化（D2/D3/E8）**并各自交代弱点**。评审最反感的是"用外部集洗白"，所以要说清 E8 的 28.6% 是**预期低**而非失败。

## Q14 · "分母是不是可以随便挑？挑完对你们有利。"

**Concede.** Denominator choice moves the corpus number by up to **9.9pp** (62.5% / 54.8% / 52.6%), so a rate without its caliber is genuinely uninterpretable — that is the paper's own point, and the risk cuts both ways.

**Already addressed.** We pre-commit to the caliber **in the artifact, not in prose**: every rate carries a `denominator` and `caliber` (opt_levels, env); the three-arm caliber ablation is reported as a table; the pre-registered rule that a crossing-zero CI voids the mechanism is stated *before* the results; and all four Δ CIs are strictly positive regardless of the choice (the choice changes magnitude, not sign). We forbid Wald intervals at small n and use Clopper–Pearson as primary with Wilson as sensitivity.

**Plan.** No change needed to the estimand; the discipline (caliber travels with the number, alternative denominators reported alongside) is the answer, and it is enforced by the gate rather than by goodwill.

> 中文要点：这一问其实是在夸我们的方法论——把"口径必须随数字走"这条规则亮出来，并指出**四个 Δ 的 CI 无论口径都不跨 0**（挑口径改变量级、不改符号），这句最有说服力。

## Q15 · "82.9% 比旧稿的 81.0% 高——是不是又'改善'了？"

**Concede.** No. The rise is an **expanded-sample re-estimate**, and both movements are reported as measured without "correction" (holdout 81.0→82.9 up; corpus 54.2→62.5 up). The 81.0% here is a *different* subset (primary pre-reveal blind, 17/21), so "82.9 > 81.0" is **not** a before/after comparison at all.

**Already addressed.** The paper decomposes each rise into **composition change vs within-layer change** (holdout new-subset 17/20 vs historical 17/21; corpus new-subset 14/16), and the pre-registered **H4 subset-consistency check fails for corpus (+33.3pp, outside the pre-registered range)**, registered as a composition shift. We also keep the history honest: 66.7%→87.5% was a **caliber change** (old value voided), and **81.2% never landed in any artifact** and is marked hollow.

**Plan.** Independently of the numbers, the mechanism that caused the 81.2% incident (changed code, no rerun) is still open and is future work item (v): make the guard re-run detectors. Until then, treat every cross-batch comparison as *not* a capability curve.

> 中文要点：这一问测的是"你会不会把扩样当成绩"。答案必须是否定的，并且要展示"我们连 H4 失败都登记了"。这与 Q2 同源，但角度不同：Q2 问 blind，Q15 问"数字变大是否等于变强"。

---

## 附录 A · 一句话弹药库（One-line armory）

- **A5**：设计已冻结并预注册，未跑；阻塞是双重的（样本量 + 仪器保真度），不是"忘了做"。探索性派生集：85.0% vs 10.0%（标 exploratory）。
- **blind**：只有 21 个样本严格盲；主估计量是 **81.0% (17/21)**，扩样值 82.9% (34/41) 明标含 20 个 reveal 后并入。
- **Belnap**：`(support, refutation)`；`pass=(1,0)`…`contradict=(1,1)`；detector availability 是独立 metadata；我们不声称编码新颖。
- **auditability**：当前状态成立；历史钉定不完整（452 事件无 ruleset hash）；路线图 = hash 入账本 + guard 重跑探测器 + fail-loud 自检。
- **novelty**：不声称第一个演化评估器；边界 = executable C++ assertion setting + detector availability 显式分离 + failure→rule→re-test 链。
- **LLM judge**：12/12 敏感但 50% FPR；LLM 只 propose，永不 verdict。
- **C++**：UB 好抓是优点也是外推限制；WSL/MinGW/macOS 差异已披露。
- **caliber**：三口径全报（62.5/54.8/52.6）；四个 Δ 的 CI 均不跨 0。
- **标签**：零第二标注者（T17）；已预注册 25% 双标注 + κ<0.6 全复核。
- **E9**：跨缺陷区间压力测试；corpus 与 cppcheck 打平；8 个 reverse pair 逐条列出。

## 附录 B · 三条应答纪律（回复技巧）

1. **先同意再补充**：每条回复第一句用 "We agree…" / "Correct, and…" 开场，把评审的担忧复述一遍再给已做修订。评审在 rebuttal 里最先找的是"有没有听进去"。
2. **指路标，不复述全文**：每条回复用 "already stated in §X / Table Y / Appendix Z" 的指针，而不是重抄正文；篇幅留给 *新的* 信息（路线图、探索性证据、8 个逆例）。
3. **不升级主张**：凡论文已降级的表述（directional、exploratory、current-state-only、cross-regime stress test），rebuttal 一律沿用同一降级词，绝不借机升格。宁可窄而可信，不可宽而可疑。
