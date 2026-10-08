# Rebuttal Prep v3 —— Queyi /「Caliber Drift and Capability Boundaries: An Audit Protocol for Software-Verification Evaluation」E&D 投稿

- 批次：692｜执行：CodeBuddy（AI）｜生成：2026-10-08
- 基线：`research/rebuttal_prep_v2.md`（v2，2026-10-07）｜本版是**增量修订版**：
  **v2 §1–§7 的问答主体仍然有效**（未在本版列出的问答一律以 v2 为准），本版做三件事：
  ① 同步 691 的 8 项变动；② 更新数字速查表；③ 新增 Q19/Q20/Q21（环境感知协议 / 外部对比定位 / LLM 第四臂）。
- **题名已不再是 "Evolving Verifiers"**：任何材料中出现旧题名即为缺陷（见 §5 遗留清单）。

---

## 0. 691 同步的 8 项（rebuttal 里必须与论文一致）

| # | 变动 | rebuttal 里的一致性表述 |
|---|---|---|
| 1 | **题名** | `Caliber Drift and Capability Boundaries: An Audit Protocol for Software-Verification Evaluation`；§3 方法名仍为 *Evaluator-Audit Protocol*（命名不冲突） |
| 2 | **公式定性** | `E[J]=kd/n` **不是错误**，是**符号消歧**（`n` 即资产池规模 8，该式本就是超几何精确均值）；若被追问，"mathematically unchanged; notation clarified" |
| 3 | **池计数** | **不是"三池验证"**：Pool B ≡ Pool C（同 6 资产集，数值逐位相同）⇒ 14 块实为 **9 个不同 (池,k) 块**；"3/14 提升档"实为**同一档**（k=4, +1.41pp, p=0.302）被三个标签重复计数 |
| 4 | **四个 κ 全报告** | **0.727 / 0.789 / 0.437 / 0.157**（n=287/262）；**全部为 AI self-consistency**；严重度标签最不可靠（0.157）⇒ "严重度不预测检出率"既是仪器陈述也是**标签陈述** |
| 5 | **治理具名 + 边界** | **452** ledger 事件 / **67** 规则 / 钉定 `rules_sha256` (v1.0.0)；claim 为"**规则变更可审计**"，**不是** immutable、**不是** tamper-proof；历史重放需假定规则未变 |
| 6 | **标准化为主结果** | −17.92pp 是**实质结果**（构成抵消：正向 −17.92pp / 反向 +1.70pp / 类型级 −13.52pp），TOST 为补充 |
| 7 | **页数/摘要** | 全稿 **35** 页；正文 **8** 页（References 起 p9）；附录 **23** 页（≤26）；摘要 **229** 词 |
| 8 | **数字检查集** | `verify_paper_numbers.py` **130** 条：0 missing / 116 consistent / 14 retired / 0 policy_violation |

---

## 1. 数字速查表（v2 §8 的更新版）

> 未在本表列出的行**沿用 v2 §8**；本表只列 691 变动 + 692 新增。

| 指标 | 值 | 产物 |
|---|---|---|
| A5 全池 | FD 54.6% vs Random 30.6%（+24.03pp）vs Static 24.7%；1137×8=9096 detect；派生 571 / 评估 566 | `a5_676f_results.json` |
| A5 非退化池 | k=1 **+11.31pp**（p=6.0e-8）；k≤3 +7.4~11.3pp；k=4 Δ=0.0 | `677c_a5_nondegenerate_results.json` |
| 演化算子 | 14 块 ≡ **9 个不同块**；最佳 **+1.41pp, p=0.302**（不显著） | `677c_evolution_operator_results.json` |
| 标注一致性 | κ = **0.727 / 0.789 / 0.437 / 0.157**（AI self-consistency；人类 IAA = **0**） | `682_kappa.json` |
| 治理 | **452** ledger / **67** rules / `rules_sha256` v1.0.0 | `governance_docs_manifest.json` |
| **692-A 环境配对（A5 eval 566）** | E1 60.07%（340/566）→ E2 **24.74%**（140/566）；**ΔE = +35.34pp** CI95 [31.40, 39.27]；**ΔU(unaware) = 0.00pp**；ΔU(aware) = −75.27pp；McNemar (b,c)=(200,0)，p=1.24e-60 | `692_environment_paired_experiment.json` |
| **692-A 静默记号** | E1 的 340 次捕获中 **200（58.82%）** 在 E2 丢失；E2 报告的 426 条负例里 **200（46.95%）** 是 E1 能抓到的真阳性 | 同上 |
| **692-A E2 的 conditional recall** | **不可计算**（aware 口径分母为 0）；63 个能力撤退配置中 **62** 个存在不可信负例；保留率 ≥95% 的静默窗口 **1** 个（缺 `linker`：聚合仅 −0.71pp，22 条负例失去可信性） | 同上 |
| **692-A 方向反转（诚实登记）** | 按"能力相关性"筛可信负例时 `conditional_recall` **升到 100%**（极端例：只剩 `linker` 时 catch 0.71% / cond 100%）⇒ 与 `catch_rate` **反向**，单看任一都是错 | 同上 |
| **692-A 真实 110 锚点** | E1 59.09%（65/110）→ E2 23.64%（26/110）；丢失 39（占捕获 60.0%）；**与 688 逐位一致** | `692_environment_paired_experiment.json` |
| **692-B 外部对比（同帧 566 / 538 可跑）** | clang-tidy C-main **94.12% / FP 97.40%**（零判别力，673e 形态复现）；clang-analyzer **34.97% / 13.85%**；cppcheck warning **49.67% / 18.10%**；broad **50.65% / 19.40%**；Queyi OR 参照 **93.79% / 15.57%** | `692_fair_comparison_results.json` |
| **692-B 交叉分歧** | Queyi 命中而 clang-analyzer 静默 **209**（`stl` 60 / `concurrency` 57…）；反向 **30**（`memory_safety` 14 / `language_semantics` 11）；**cppcheck 在本帧 59 条 concurrency 上 0 命中** | 同上 |

---

## 2. Q19（新增）· "You formalize environments, yet still report one headline number for the real corpus — isn't that the very sin you name?"

**回应要点**（产物：`692_environment_paired_experiment.json`、`692_environment_formalization.md`、`692_environment_report.md`）：

> Fair challenge. We now report environments as a **coordinate**, not a caveat, and we report the paired consequence:
>
> (a) A 15-field `EnvironmentProfile` (OS/kernel/arch/compiler/version/stdlib/libc/sanitizer-runtime/linker/
> optimization/compile-flags/runtime-flags/timeout/resource-limits/container-image) plus
> `measurement_context_id = H(sample_hash, asset@version, profile, configuration, protocol_version)`;
> same id $\Rightarrow$ same measurement record, so a conclusion **cannot silently inherit** across a
> profile change.
>
> (b) On the 566-sample evaluation split we ran the **paired, within-sample** comparison between the
> declared profile ($E_1$: WSL g++13.3, 6 catch-capable assets) and the native-minimal profile
> ($E_2$: the three assets that actually run on Windows). Three-component vectors:
> $E_1$ recall **60.07%** / unknown **0.00%**; $E_2$ **24.74%** / **0.00%** under an environment-**unaware**
> protocol, and $24.74\%$ / **$75.27\%$** under an environment-**aware** protocol.
> $\Delta E = +35.34$pp (paired CI $[31.40,39.27]$), **$\Delta$unknown $=0.00$pp**, McNemar $(b,c)=(200,0)$,
> $p=1.2\times10^{-60}$.
>
> (c) The silent-degradation signature: **200 of the 340** catches (58.82%) disappear, and **200 of the 426**
> samples $E_2$ reports as negatives (46.95%) are samples the *same instrument* catches under the declared
> profile. Under the aware protocol the conditional-recall **denominator is empty** --- the honest value is
> "**undefined**", not 0% and not 100%. We swept all 63 capability-retreat configurations: **62** of them
> contain unsound negatives, and the widest *silent* window loses only **0.71pp** in aggregate while 22
> negatives lose their credibility --- no existing guard turns red.
>
> (d) One result we did **not** expect, and report as such: when negatives are filtered by
> capability-relevance, `conditional_recall` moves **opposite** to `catch_rate` and can reach **100%**
> (extreme case: only `linker` available $\Rightarrow$ catch 0.71%, conditional recall 100%). This is why we
> make the three-component vector the minimal sufficient caliber and state the environment with every rate.

## 3. Q20（新增）· "Why is this not yet another SV-COMP verifier leaderboard?"

**回应要点**（产物：`692_fair_comparison_results.json`、`692_fair_comparison_protocol.md`、`692_fair_comparison_report.md`）：

> Because the object audited is the **apparatus**, not the competitors --- and we run the comparison under a
> *single declared caliber* to demonstrate exactly that:
>
> Same frame (the 566-sample evaluation split), same truth labels, same 60s timeout, calibers **declared
> before running** (frame + calibers are frozen in the protocol file, timestamped before any tool call).
> Results: clang-tidy with the pre-registered family (`clang-analyzer-*, bugprone-*, cert-*,
> cppcoreguidelines-*`) gives recall **94.12%** with a **97.40%** false-report rate --- i.e. **no
> discrimination** (the failure 673e saw on 136 samples now reproduces at 4$\times$ the frame with the
> caliber declared in advance). Restricting to `clang-analyzer-*` moves the *same measurement* to
> **34.97% / 13.85%**; cppcheck gives **49.67% / 18.10%** (warning) and **50.65% / 19.40%** (broad).
>
> The scientific content is the **disagreement structure**, not a ranking: concurrency is a static blind
> spot (cppcheck catches **0 of 59** concurrency samples; clang-analyzer catches 2) while the static layer
> reports on 30--39 samples our runtime assets miss, concentrated in `memory_safety` and
> `language_semantics`. No party achieves both high recall and low false-report on this frame.
>
> We claim **no superiority**; the paper's sentence is fixed: *SV-COMP asks which verifier performs well on
> given tasks; we ask whether evaluation results survive an audit of the evaluator.* The most defensible
> demonstration of that difference is internal: on the same samples, moving from caliber $T_1$ to $T_2$
> swings recall from 94.12% to 34.97% --- **the number was never a property of the tool alone.**

---

## 4. 不能说的话（红线；v2 §9 + 692 新增 4 条）

v2 §9 的八条**全部继续有效**（superiority / real-world defects / verified labels / 38.4% 泛化 / TOST 等价 /
演化算子提升 / 已删的工程遥测 / static arm 定性 / human annotation 含糊化）。692 新增：

- ❌ "we outperform cppcheck / clang-tidy" → ✅ "**cross-regime observational comparison (convergent validity)**; calibers declared in advance; no superiority claim"
- ❌ "the environment-aware protocol fixes reproducibility" → ✅ "it makes the omission **syntactically impossible**; `container_image` is still `null`, so reproducibility is **fingerprint-level** (record + re-runnable commands), not **image-level** (sha256)"
- ❌ "conditional recall drops to X% without WSL" → ✅ "under the aware protocol it is **undefined** (empty denominator); and when negatives are filtered by capability relevance it can **rise to 100%** --- the metric must never be quoted alone"
- ❌ "the LLM verifier detects defects" → ✅ "the LLM is a **fourth evidence asset** with a *different* failure topology; we report invariance/calibration/disagreement, **not** accuracy against us, and it is never an oracle"（完整口径见 `data/692_llm_audit_protocol.md` 与报告）

---

## 5. 与 v2 的关系 · 遗留清单

1. **v2 §1–§7、§10 主体未改**：本版不复制其正文；冲突时**以本版数字表为准**（691 变动已同步）。
2. **v2 §8 速查表中被 692 更新的行**已在本文 §1 重列；未列出者沿用 v2。
3. **遗留（不得写成已完成）**：
   - 人类 IAA 仍为 **0**（本版不新增任何人工标注）；
   - `rebuttal_prep.md`（v1）与 `research/rebuttal_prep_v2.md` 的文件头仍含旧题名 "Evolving Verifiers" ——
     v1 为历史记录不动；**v2 的文件头由本版 §0 修正声明覆盖**（若投稿包内保留 v2，建议一并更新其首行标题）；
   - `research/response_template.md/tex` 与 `SUBMISSION_CHECKLIST.md` 中的旧 TODO 状态见 `data/692_submission_checklist_final.md`。
