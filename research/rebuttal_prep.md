# Rebuttal 预演（Rebuttal Preparation）· v1.2 (677a)

- 批次：673s 起草 → **676j 同步 A5 全量（676f）+ 盲区地图（676g）** → **677a 版本统一（见 `research/latex/VERSION.md`）**
- **677a 变更（纯表述，不改数字）**：① "verifier" 一律为 **evidence-acquisition 装置**，`pass` ≠ 语义真值（论文新增 §3 Terminology 段与 Claim Boundary 第一条 C0）；② 盲区 **38.4%** 一律带 **instrument-boundary** 口径限定；③ 高盲区类型数统一为 **18/70**（对齐 `data/blindspot_676g_stats.json`）；④ VC 73.8% **去掉无抽样基础的 95% CI**；⑤ **e-process 降级为 exploratory**（正文压至 2 句，完整内容移附录并标注）；⑥ `planted=false` 表述改为 **source-derived-reconstruction**（provenance 三分类）。**答 rebuttal 时按新表述口径。**
- 仓库：`C:\CodeLearnling\note\note\C++\CPP-Bible`
- 目标稿件：`research/latex/queyi_neurips2027_v1.1.tex`（英文稿）+ `research/paper_shturl.md`（中文稿）
- 权威数字源：`data/current_numbers.json`（schema `queyi-current-numbers/672h`）、`data/experiments/reveal_update_672h.json`、`data/a5_676f_results.json`（**A5 全量重跑，取代 `a5_673p.json`**）、`data/blindspot_676g_stats.json`（**检测器能力边界地图**）

## 0bis · 态势更新（676j，2026-10-04）——引用 A5 前必读

| 项目 | **676j 现值（权威，来自 676f/676g）** | 被取代的旧值 | 出处 |
|---|---|---|---|
| A5 样本规模 | **1137 总样本；571 派生 / 566 评估**（去重 10 条；planted=false 74） | 105（21/48 → 20/16） | `data/a5_676f_results.json::sample_stats` |
| A5 主端点（k=4，全 8 资产池） | FD **54.6% (309/566)** vs Random **30.6% (173/566)** vs Static **24.7% (140/566)** | 90.0%/35.0%/10.0%（holdout） | 同上 `primary_main_8candidates.by_k[k=4]` |
| Δ(FD−Random) | **+24.0pp** CI [+20.5, +27.5]，p=**2.3×10⁻⁴¹**，h=0.49，b=136/c=0 | +55.0pp，p=9.8×10⁻⁴ | 同上 `paired_tests.fd_vs_random` |
| Δ(FD−Static) | **+29.9pp** CI [+25.2, +34.5]，p=**1.9×10⁻³¹**，h=0.62 | corpus +43.8pp（p=0.039） | 同上 `paired_tests.fd_vs_static` |
| **并列分析（剔除 2 个退化资产）** | FD-vs-Random **掉回 0.0pp（p=1.0）**；FD-vs-Static **增至 +30.6pp（p=8.1×10⁻³⁴）** | 旧版仅报 holdout 掉 0、corpus +31.3pp（p=0.125） | 同上 `co_primary_excl_degenerate` |
| 退化资产 | `wunsequenced`、`compile-time`：1137/1137 全 `unknown`（0 catch） | 同 | 同上 `asset_diagnostics.full_pool` |
| **能力边界（676g，新贡献）** | n=**1147**：catch 707 / miss 440 ⇒ **盲区比 38.4%**；6 资产并集 61.6% vs 最佳单资产 35.6%（asan）；**18/70** 类型 >50% 盲；家族金字塔 memory 15.2% → link/ODR 67.7%；planted=true 41.0% [38.0,44.1] vs false 21.6% [13.8,32.3]；TSan 3/180 不稳定 | 无（新增） | `data/blindspot_676g_stats.json` |
| 可复现性入口 | `REPRODUCE.md` + `bash docker/paper/run_all.sh`（fail-loud）；种子审计 `tools/seed_audit_676h.py`：实验类未固定种子 **0** | 无 | 仓库根 / `data/676h_seed_audit.json` |

> **口径纪律不变**：A5 矩阵是 **1 回合**、头条率 82.9%/62.5% 是 **3 回合（任一回合 catch ⇒ catch）**，两套数字**不得相减或比较**。下方 §1 表中标注「**⚠️ 已被 676f 取代**」的行仅作审计轨迹保留（**引用 A5 一律以 0bis 与 Q1 为准**）。

## 0 · 使用纪律（三步走）

1. **三段式**：每问都写成 `Concede（承认点） / Already addressed（已做修订） / Plan（未来工作）`。英文段落可直接粘贴进 rebuttal；中文是策略提示，不投出去。
2. **数字只能来自 artifact**：rebuttal 引入的每个数字都必须可回溯到仓库产物（`current_numbers.json` / `reveal_update_672h.json` / **`a5_676f_results.json`**（取代 `a5_673p.json`）/ `data/blindspot_676g_stats.json` / `data/673r_A5实验报告.md`）。红线：**不把未做的实验写成已做**，也**不把已被推翻的旧数字继续当弹药**。
3. **诚实优先**：凡是论文已自认的缺口（标签零复核、scope 0/26、历史钉定不完整）**以及新出现的受限结果**（A5 主端点显著**但**触发预注册 `uninterpretable`、效应落在池构成层面），rebuttal 一律先说"我们同意 / 我们主动登记"，再给已落地修订，最后给路线图——**不要辩护式反驳**。评审对"承认 + 已修 + 路线"的接受度远高于"辩解"。
4. **态势会随并行批次变化（本批已发生三次）**：本仓库多 Agent 并行。**673r 在预案写作期间提交**，把 A5 从"未跑（BLOCKED）"变成"已跑且主端点不显著"；随后 **673u 修掉 `wunsequenced` 恒 catch**，又把 A5 变成"**主端点显著但触发 `uninterpretable`**"；**676f 把 A5 扩到全量池（1137 样本 / 评估 566）**，主端点以 p≈10⁻⁴¹ 显著、幅度回归 +24.0pp、并列分析仍归零，并首次钉住选择效应 ≈+7~11pp。Q1、附录 A 与「0bis 态势更新」已按**最新产物**重写。任何 rebuttal 预案在发出前**必须重新核对 HEAD 与最新产物**。

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
| **A5 真实逐资产对照（673r 建矩阵 / 673u 重跑）——⚠️ 已被 676f 全量重跑取代，见上方 0bis 与 Q1** | 主预算 k=4、全 8 资产池：holdout FD **90.0% (18/20)** vs Random **35.0% (7/20)** vs Static 10.0%，Δ=**+55.0pp** CI [+33.2, +76.8] **p=9.8×10⁻⁴**（b=11/c=0，h=1.23）；corpus FD **81.3% (13/16)** vs **37.5%**，Δ=**+43.8pp** CI [+13.9, +73.6] **p=0.039**（b=8/c=1，h=0.93）⇒ **主端点首次显著**（`primary_pass` ✓ / `secondary_pass` ✓） | `a5_673p.json::real_attribution`、`673u_wunsequenced修复报告.md` §5 |
| A5 2000 次重采样分布（673u 旧值；⚠️ 已被 676f 的 97.6% 取代） | FD **严格更优 93.75%（holdout）/ 95.8%（corpus）**；holdout 均值 55.0% SD 23.4pp；corpus 均值 53.7% SD 16.0pp | 同上 |
| **A5 并列分析（剔除退化资产）⇒ 关键限制**（⚠️ 已被 676f 取代，见 0bis） | holdout（5 候选）Δ **掉回 0.0pp（p=1.0）⇒ 触发预注册 `uninterpretable`**；corpus（6 候选）Δ=+31.3pp CI [+2.7, +59.8] 同号但 **p=0.125 不显著** | 同上 |
| A5 退化资产（池构成效应的来源）（⚠️ 已被 676f 取代：全量池重算为 `{compile-time, wunsequenced, linker}`） | holdout：`wunsequenced`、`compile-time`、`cross-compile`；corpus：`wunsequenced`、`compile-time`（均 0% catch ⇒ 零信息常量）——主分析里 Random 抽到它们 ⇒ **一半预算花在零信息资产上** | 同上 |
| A5 口径警告 | 本矩阵 = **1 回合**；82.9%/62.5% 头条 = **3 回合**（任一回合 catch ⇒ catch）⇒ **两套数字不得相减或比较** | `673r_A5实验报告.md` §3.1 / `673u` §3 |
| **`wunsequenced` 缺陷修复（673u）** | 恒 catch → 恒 `unknown`（检测器不可用）；**头条率 82.9% / 62.5% 逐位不变**；对照假阳性 **18.2% (2/11) → 0.0% (0/11)** | `673u_wunsequenced修复报告.md` §0 / §3 |
| 派生集探索（**replay 口径**，exploratory） | holdout FD 85.0% (17/20) vs random 10.0% (2/20)；corpus 87.5% (14/16) vs 37.5% (6/16)——**replay 口径、非确证；与真实口径不同，不得混用** | `a5_673p.json::exploratory_derivation_split` |
| 样本量要求 | Δ=15pp 需 n≈138（paired）/170（independent）；±10pp 需 n≈104；±5pp 需 n≈236/378 | `tab:samplesize` |
| VC / 变异 | **31/42 = 73.8%（描述性；677a 已去掉无抽样基础的 95% CI——42 张卡是全枚举而非抽样）**；core 96.5% (110/114) / all-scope 81.8% (130/159) | `current_numbers.json` |
| 术语（677a） | "verifier" = **evidence-acquisition 装置**；`pass` = "边界内未获得矛盾证据"，**不是**语义真值 | 论文 §3 Terminology / §9 C0 |
| 盲区类型数（677a 统一） | **18/70**（旧写 15/70 系转录不全；权威 `by_type` 中 `blindspot_ratio > 0.5` 计数 = 18） | `data/blindspot_676g_stats.json` |
| provenance（677a） | **968** self-authored / **74** source-derived-reconstruction / **0** original-external-artifact | `data/holdout_expansion/SCHEMA.md` §2.1 |
| e-process（677a） | **exploratory**：μ₀ 未冻结、备择网格未冻结、未进 CI ⇒ **不作为证据强度**，不进 Claim 表 | 论文附录 `app:eprocess` |

---

# Part I · Q1–Q5（14 点评审的主问题）+ Q5b（局限总表）

## Q1 · "核心主张（failure-driven 优于同预算随机）检验了吗？结果如何？"

> **态势已变三次，以最新为准（2026-10-04，676f）**：A5 **已在全量样本上重跑**——**1137 样本 × 8 资产 = 9096 次真实 `detect`**（派生 571 / 评估 566，k=4）。主端点 **Δ(FD−Random) = +24.03pp**（p=2.3×10⁻⁴¹，CI [+20.51, +27.55]，b=136/c=0），但**预注册的并列分析仍在 k=4 上归零（Δ=0.00pp，p=1.0）** ⇒ 仍触发 `uninterpretable`，只能答"**方向证据，不是确认性结论**"。旧值（105 样本：holdout +55.0pp / corpus +43.8pp）**作废**（不同样本池，禁止相减）。**论文正文的 A5 段落须由 676h 按 `data/676f_论文更新位置清单.md` 整段改写**（不是换几个数）。

**Concede.** A5 has now run **at full scale**: **1137 samples × 8 assets = 9096 real `detect` calls** (one round; derivation 571 / evaluation 566), with failure-hits estimated *only* on the disjoint derivation split, so FD is a genuine predictor rather than a post-hoc accounting of its own catches. At the pre-registered budget $k{=}4$ over the full 8-asset pool: FD **54.59\% (309/566)** vs Random **30.57\% (173/566)** vs Static **24.74\% (140/566)**; **Δ(FD−Random) = +24.03pp, CI [+20.51, +27.55], exact McNemar p = 2.3×10⁻⁴¹** (b=136, c=0; h=0.49) and **Δ(FD−Static) = +29.86pp, p = 1.9×10⁻³¹** (h=0.62). FD strictly beats the single-seed draw in **97.6\%** of 2000 resamples. The expansion also **closes the old power gap**: $n{=}566$ far exceeds the $n{\approx}138$ paired requirement, so magnitudes are now readable — the +55/+44pp of the $n{=}20/16$ pilot regressed to **+24.0pp**, which is the expected effect-size shrinkage under a 10× larger sample, *not* a sign reversal (significance rose ~12 orders of magnitude).

**Why it is still not a superiority claim (three limits, all written into the paper).** (i) **Pool composition, not selection.** The single-seed Random draw at $k{=}4$ is `{wunsequenced, cross-compile, tsan, compile-time}` — **two of its four slots are zero-information assets** (constant `unknown`; they catch nothing), while the failure-driven ranking avoids them by construction; in the **pre-registered parallel analysis** over the 5 non-degenerate candidates the $k{=}4$ Δ **collapses to 0.00pp (p = 1.0, b = c = 0)** — both arms select the *same* four assets — **triggering our pre-registered `uninterpretable` clause**. The +24pp therefore mostly says "don't waste budget on assets that cannot inform", which is weaker than "failure-driven selection is smarter". **However**, the parallel analysis *is* significantly positive at $k{=}1/2/3$ (**+11.31 / +7.42 / +7.42pp, p ≤ 7.7×10⁻⁵**), which for the first time **pins the selection effect at ≈ +7–11pp**: real, but small. (ii) **Instability.** Single-cell verdicts carry a measured **~5\%** run-to-run flip rate (369 clean re-tested cells → 18 flips; 3-round modal check on concurrent samples, 4/80 flipped at least once), so every one-round number is noisy. (iii) We therefore write **no** "FD > Random" sentence; the $k$-sweep stays exploratory (main pool Δ>0 with $p \le 1.7\times10^{-18}$ for $k{=}1..7$; $k{=}8$ is degenerate).

**What changed, and why we report it as a strength rather than a patch.** The 673u fix turned `wunsequenced` from a *constant catch* (the hit predicate matched the option name inside MinGW's own "unrecognized option" error) into `unknown`; **the headline rates 82.9\% / 62.5\% are bit-identical before and after**, and the only other change is that the **control false-positive count drops from 2/11 to 0/11**. We publish the fix, its regression tests, and its consequences rather than silently repairing the table. **676f adds the ~5\% instability as a first-class limitation of the same kind** — measured, registered, and carried into the paper.

**Roadmap.** (1) The power gap is **closed**; what remains is a **non-degenerate pool with $1 < k < |A|-1$** so the two arms can actually differ; (2) run A0–A4; (3) upgrade single-round cell verdicts to **multi-round modal** verdicts (the instability is now measured, not assumed); (4) keep the round caliber explicit: this matrix is **1 round** while the 82.9\%/62.5\% headline is **3 rounds (any-round catch ⇒ catch)**, so the two must **not** be subtracted or compared.

> 中文要点：Q1 现在是"**全量重跑、主端点以 p≈10⁻⁴¹ 显著、但被自己的预注册条款降级为方向证据**"。答法四步：(1) 先亮全量数字（+24.03pp / 2.3e-41 / CI [+20.51,+27.55]，b=136/c=0；vs Static +29.86pp / 1.9e-31；2000 次里 97.6%）；(2) **主动交代池构成效应**——单点 Random 抽到 2 个零信息资产、并列分析 k=4 Δ 掉回 0.00pp 触发 `uninterpretable`，故**不宣称 superiority**；但并列 k=1~3 显著（+11.31/+7.42/+7.42pp）⇒ **首次钉住选择效应 ≈+7~11pp**；(3) 说明让表可读的前提是修了 `wunsequenced` 恒 catch（**头条率逐位不变**，FPR 2/11→0/11），并主动登记 **~5% 跑间不稳定**；(4) 路线图 = 非退化池 1<k<|A|-1 + A0–A4 + 多回合众数。**全程不得出现 "FD > Random"。**

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

**Our specific boundary.** Our claim is narrower than "evolving an evaluator": we evolve the verifier's **evidence-acquisition capability C** in an **executable C++ assertion setting**, and we keep three things **explicitly separated** that prior work couples — (a) **detector availability** (metadata, never a verdict), (b) **semantic scope** vs **provenance** (forced split), and (c) the recomputable **failure → rule → re-test** chain. We also position eight works along five dimensions (Table `tab:positioning`): prior lines evolve items/tests/proofs/judge/metric; we evolve evidence-acquisition capability and require each step to be externally measurable. We do **not** claim superiority over real static detectors (our comparison is a *cross-regime stress test*, E9) or over a true budget-matched random baseline (A5 has now run; its significant main endpoint is registered as direction-only on pool composition, §6 E4).

> 中文要点：新颖性答辩的关键不是"我是第一个"，而是"我把哪三件事**显式分离**了、演化的对象具体是什么"。用"更窄但更清晰"换"更大但更脆"的 claim。E9 的定位（互补缺陷区间，非全面优于）必须在这一问里重申，否则会被连环追问。

## Q5b · 局限（Limitations）：能力边界 / 测量不稳定 / 标注 / 平台

> **为什么单列**：676f（A5 全量）与 676g（盲区地图）同时把四条**系统级**局限推到台前；它们分属**外部效度 / 测量精度 / 构造效度 / 可复现性**四个不同维度，不是"样本量小"的同义反复。原 Q5 是新颖性问，故本条目单列；评审若问"你们最大的弱点是什么"，用这一条正面回答。（本条目即 676j 规格中"Q5（局限性）"的落点。）

**Concede.** 我们主动承认四条一级局限，且已全部写入论文 / artifact：

1. **检测器能力边界（676g，硬数据）**：全量 **1147 样本 × 8 资产**矩阵上，样本级检出 **61.6%（707/1147）**、**盲区 38.4%（440 全 miss，0 纯 unknown）**；**18/70** 缺陷类型盲区 >50%（死锁 94.3%、volatile 误用 92.9%、端序 89.3%、优先级反转 73.3%、跨 TU UB 70.0%…）；家族金字塔从 memory **15.2%**（n=171）单调升到 link/ODR **67.7%**（n=31）。⇒ 运行时检测器只抓**物理层**错误（内存 / UB / 竞争），语义 / 设计层错误是**结构性盲区**；单资产最高仅 asan **35.6%**，六资产并集 **61.6%** ⇒ **38.4% 是任何资产组合都无法覆盖的天花板**。
2. **逐格判定 ~5% 跑间不稳定（676f 自证，一级局限）**：无竞争条件下重测 369 格有 **18 格翻转（4.9%）**；并发样本 3 轮抽检 **4/80** 出现过翻转；与并发批次交叉核对 1047 格有 42 格不一致（4.0%）。⇒ 每个"单回合"数字都带噪声，**673r 的 105×8 历史矩阵同样受影响**。
3. **planted=true 占比高（外部效度受限）**：A5 池 **1063/1137 = 93.5%** 为植入缺陷（676g 口径 1009/1147 = 88.0%）；唯一的真实缺陷子集是 expG 的 **74 条 planted=false**，其中仅 **34 条**落在评估集 ⇒ 其 Δ=+29.41pp（p=1.95×10⁻³）只能读**方向 + 区间**，不能读幅度。
4. **单标注者、无 κ（构造效度）**：标签由单一标注者产出，**第二标注者 = 0、IRR 未计算**（登记为 T17，对召回数最大的威胁）；已预注册 25% 双标注 + κ<0.6 全复核。
5. **平台依赖（可复现性）**：盲区率与检出率都是**本机工具链**的测量（WSL g++ 13.3 / MinGW g++ 13.1 / clang++ 22.1.8）；x86 容忍未对齐、单机无法暴露端序错误（89.3% 盲）、优先级反转在通用调度器上不发生（73.3% 盲）⇒ 换 ARM / 原生 Linux / MSan，比例会变。

**Already addressed.** 论文侧：(a) 盲区地图以 **T20「检测器能力边界」** 新增进 Threats（`data/676g_论文更新建议.md`，含复算命令）；(b) 不稳定率进入 §E4 与摘要，**单回合 vs 三回合口径已明标**；(c) planted 比例与 expG n=34 已在外部效度段**同句声明**；(d) T17 单标注者已列为首要威胁；(e) 环境依赖已升级为 **fail-loud**：`REPRODUCE.md` + `docker/paper/run_all.sh` 在错误环境下**抛错**而非静默降级（旧的 35.0%→10.0% 静默掉分已封堵）。artifact 侧：每个数字都带 `denominator` / `caliber`；盲区率同时给**批次生成口径**与**676g 检测器矩阵口径**（如死锁 5.7% 挂起观测 vs 94.3% 检测器），并禁止两口径相减 / 混用。

**Plan.** (1) 资产池补短板：MSan 类未初始化读检测（20/20 全盲）、死锁 / 活性 oracle（31/35 死锁样本零 sanitizer 报告）、把 float-cast-overflow / pointer-overflow 纳入固定 `-fsanitize=undefined` 口径（两个**配置缺口**已对照实验证实检查存在但未启用，见 NF-3 / NF-4）；(2) 单回合 → **多回合众数**判定（不稳定率已量化，升级不再是"假设"）；(3) 把「挂起观测」与「检测器判定」拆成两条独立证据通道、两套口径；(4) 平台矩阵化复测（ARM / 原生 Linux）；(5) 预注册的双标注复核（含 κ 阈值）先行。

> 中文要点：这一条是"你最大的弱点是什么"的正面回答。四条局限**分属四个不同维度**（外部效度 / 测量精度 / 构造效度 / 可复现性），比"样本量小"有力得多。**盲区地图必须带口径**（检测器矩阵口径 ≠ 批次生成口径），**不稳定率必须主动报**（本批自证的一级局限），**planted=false 只有 34 条进评估集**不能当幅度用。**全程不得把 38.4% 说成"系统漏报率"**——它是资产池能力边界，不是系统失败率。

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

**Already addressed.** The paper carries the recomputed power table (`tab:samplesize`): Δ=15pp needs n≈138 (paired, ψ=0.4) / ≈170 per group (independent); ±10pp needs n≈104; ±5pp needs n≈236/378. The pre-registered rule is *if the difference CI crosses 0 the mechanism does not hold*, and all four Δ CIs are strictly positive (lowest bound **28.6pp**). McNemar's small-sample fragility is stated: significance rests on the extreme **c=0** structure, and a few reverse pairs would inflate p quickly — indeed E9 supplies 8 reverse pairs against static tools on corpus, where FD only **ties** cppcheck (Δ=+7.8pp, CI crosses 0). Separately, the **A5 budget-matched contrast has now reached n=566** (1137-sample pool; derivation 571 / evaluation 566), i.e. **past the n≈138 paired requirement** — the old "n too small" objection no longer applies to A5 (it applies to the two headline rates, which stay at n=41/64).

**Plan.** The expansion target is **met for the A5 contrast** (n=566 ≫ 138); what remains is a **non-degenerate pool with 1 < k < |A|−1** (Q1) plus multi-round modal verdicts (Q5b). The two headline rates remain n=41/64 and are still read as direction. We would rather report a wide CI than a narrow claim.

> 中文要点：**主动报出功效表**是这一问的杀手锏——评审说"样本小"，你若先给出"我们算过需要多少 n"就赢了。务必带 E9 的 8 个 reverse pairs 与 corpus 打平，证明我们不是只挑赢的场子报。

## Q10 · "标签是谁标的？有几人复核？"

**Concede.** Labels are **self-produced with zero second annotators** (41 holdout + 64 corpus); there is no IRR, and the bias direction is unknown. This is registered as **T17**, the largest threat to the recall numbers.

**Already addressed.** v1.1 adds T17 explicitly, states it in the abstract's limitations and in the Threats section, and explains why it is upstream of everything: a mislabelled sample moves a rate silently in either direction, and the shared-criterion $F_1{=}1.0$ case is an **upper bound** by construction.

**Plan.** A pre-registered two-annotator re-label of a random 25% subsample (10/41, 16/64) with the original annotator blinded, and κ<0.6 escalating to a 100% third-party re-review — **before any "verified" claim**. Machine cards are already `needs_review=true` and never counted as verified; `verified` is human-signed only.

> 中文要点：不要试图说"标签没问题"。把 T17 与"已验证状态只由人签"的机制连起来，然后给**预注册的复核方案**（含 κ 阈值）。

## Q11 · "结果依赖特定 WSL 环境，这不等于不复现吗？"

**Concede.** Effectively yes, **today it is conditional reproduction**: without the specific WSL environment, 15 samples degrade to `unknown` and external recall falls **35.0%→10.0%** while the guard stays **green** — because the guard compares artifacts to the frontend, not to a real machine. A replicator could obtain 10% and write it into a review with nothing warning them.

**Already addressed.** This is stated as an *observed* failure (not a residual): Analysis (2), the Threats table (Temporal/External layers), and the Claim Boundary's "Not reproducible" row. The `app:humanize` section documents why WSL is required (MinGW-w64 has no UBSan runtime; macOS lacks `setarch`) and the CRLF/437-file hash-drift incident.

**Plan.** The **fail-loud environment self-check has now landed**: `REPRODUCE.md` + `docker/paper/run_all.sh` raise on a wrong environment instead of degrading silently (so a replicator can no longer obtain 10\% and write it up with a green guard); explicit macOS / Windows-native non-reproducibility statements ship alongside. The remaining item is to make the *guard* re-run detectors (so caliber/measurement divergence cannot stay green). We still do not claim the numbers reproduce anywhere but in the declared environment — and Q5b adds that even *inside* it, single-cell verdicts carry a measured ~5\% run-to-run flip rate.

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

- **A5（676f 全量，权威）**：**已跑且主端点以 p≈10⁻⁴¹ 显著**（1137 样本 × 8 资产 = **9096 次真实 detect**，派生 571 / 评估 566，k=4：FD 54.59% (309/566) vs Random 30.57% (173/566)，Δ **+24.03pp**，CI [+20.51,+27.55]，p=**2.3×10⁻⁴¹**，b=136/c=0，h=0.49；vs Static 24.74%，Δ **+29.86pp**，p=1.9×10⁻³¹；2000 次分布中 FD 严格更优 **97.6%**）。**但并列分析仍在 k=4 触发预注册 `uninterpretable`**（剔除退化资产后 Δ=**0.00pp**，p=1.0）⇒ **方向证据，不宣称 superiority**；并列 k=1~3 显著（+11.31/+7.42/+7.42pp）⇒ **选择效应首次钉在 ≈+7~11pp**。**三条限制**：① 池构成效应（+24pp 主要是"不浪费预算"）② 逐格 ~5% 跑间不稳定 ③ **不得写 "FD > Random"**。让表可读的前提是修了 `wunsequenced` 恒 catch（**头条率逐位不变**，FPR 2/11 → 0/11）。旧值（holdout +55.0pp / corpus +43.8pp，105 样本）**作废**。
- **能力边界（676g）**：**1147 × 8** 矩阵；检出 **61.6%**、盲区 **38.4%**、**18/70** 类 >50%；家族金字塔 memory 15.2% → link/ODR 67.7%；单资产最高 asan 35.6% vs 六资产并集 61.6% ⇒ **38.4% 是组合天花板**。**不得读作"系统漏报率"**（是资产池能力边界，分母是含难例配额的 1147 个缺陷样本）。
- **测量不稳定（676f）**：逐格 **~5%** 跑间翻转（无竞争重测 369 格 → 18 翻；并发 3 轮抽检 4/80）⇒ 单回合数字带噪声，历史 105×8 矩阵同受影响；路线图 = 多回合众数。
- **blind**：只有 21 个样本严格盲；主估计量是 **81.0% (17/21)**，扩样值 82.9% (34/41) 明标含 20 个 reveal 后并入。
- **Belnap**：`(support, refutation)`；`pass=(1,0)`…`contradict=(1,1)`；detector availability 是独立 metadata；我们不声称编码新颖。
- **auditability**：当前状态成立；历史钉定不完整（452 事件无 ruleset hash）；路线图 = hash 入账本 + guard 重跑探测器 + fail-loud 自检。
- **novelty**：不声称第一个演化评估器；边界 = executable C++ assertion setting + detector availability 显式分离 + failure→rule→re-test 链。
- **LLM judge**：12/12 敏感但 50% FPR；LLM 只 propose，永不 verdict。
- **C++**：UB 好抓是优点也是外推限制；WSL/MinGW/macOS 差异已披露。
- **caliber**：三口径全报（62.5/54.8/52.6）；四个 Δ 的 CI 均不跨 0。
- **标签**：零第二标注者（T17）；已预注册 25% 双标注 + κ<0.6 全复核。
- **E9**：跨缺陷区间压力测试；corpus 与 cppcheck 打平；8 个 reverse pair 逐条列出。

## 附录 A′ · ✅ 论文正文已同步（**675a 完成**）

> ⚠️ **676f 已再次更新 A5**（105 → 1137 样本）⇒ 下表 675a 记录的 A5 数字（+55.0/+43.8pp、n=20/16）**已作废**，正文 A5 段落须由 676h 按 `data/676f_论文更新位置清单.md` **整段改写**（不是换几个数）。本附录保留为历史审计轨迹；**引用 A5 一律以 0bis 与 Q1 为准**。

`queyi_neurips2027_v1.1.tex` 的 A5 段落**已在 675a 改写完毕**（不再是 BLOCKED / not run）：

| 位置 | 现状 |
|---|---|
| Abstract | "the A5 budget-matched control now **runs**, with a significant main endpoint (+55.0pp / 9.8×10⁻⁴; +43.8pp / 0.039) that is nonetheless **direction-only**: the holdout effect is pool composition … triggering our pre-registered `uninterpretable` clause" |
| §6 E4（正文） | "**E4 — Ablation A5 (run): the budget-matched control**"，含设计、主端点、池构成效应、并列分析 Δ=0.0pp、三条限制 |
| §7 (5) | "The A5 budget-matched control has now run … but the holdout effect is **pool composition** … so 'FD beats same-budget random' stays **directional**" |
| §10 Evidence boundary + Future work | 不支持项加入 "FD beats same-budget random"（因池构成 collapse）；未来工作首位改为 "**confirm A5 by expanding to n≥138**"（⚠️ **676f 已达成**：n=566 ≫ 138；余留项改为非退化池 + 多回合众数，见 Q1/Q5b） |
| 表 `tab:e4` | A5 行已填入结果（+55.0pp / +43.8pp + `uninterpretable`） |
| 附录（claim 表 / validity 矩阵 / E4 全文） | 均已更新（含完整 A5 数字、并列分析、退化资产、$k$ 扫描） |
| 中文稿 `paper_shturl.md` | 同步完成（摘要、§5.2/§5.3、§6.2、§7.6、§7.9、§9.2、§9.3、附录） |

**同时登记的两项**：(1) `wunsequenced` 恒 catch 缺陷（**头条率逐位不变**，FPR 2/11 → **0/11**）；(2) 口径警告——本矩阵 **1 回合** vs 头条 **3 回合**，**不得相减或比较**。

> 本附录原为"待下一个论文批次修"的登记项；**675a 已完成该批次**，故改为完成态记录。

## 附录 B · 三条应答纪律（回复技巧）

1. **先同意再补充**：每条回复第一句用 "We agree…" / "Correct, and…" 开场，把评审的担忧复述一遍再给已做修订。评审在 rebuttal 里最先找的是"有没有听进去"。
2. **指路标，不复述全文**：每条回复用 "already stated in §X / Table Y / Appendix Z" 的指针，而不是重抄正文；篇幅留给 *新的* 信息（路线图、探索性证据、8 个逆例）。
3. **不升级主张**：凡论文已降级的表述（directional、exploratory、current-state-only、cross-regime stress test），rebuttal 一律沿用同一降级词，绝不借机升格。宁可窄而可信，不可宽而可疑。
