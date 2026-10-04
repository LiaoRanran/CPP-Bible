# Cover Letter — Evolving Verifiers (NeurIPS 2027 Evaluations & Datasets)

> **性质**：投稿信（英文版为准；中文对照供内部核对）。
> **版本**：**v1.3 (677d)** —— version of record 见 `research/latex/VERSION.md`。
> **数字基线**：`data/current_numbers.json`（schema `queyi-current-numbers/672h`）+ A5 全量 `data/a5_676f_results.json`（**+ 677b clone-aware/cluster bootstrap：`data/677b_cluster_bootstrap.json` + 677c 非退化池：`data/677c_a5_nondegenerate_results.json`**）+ 盲区地图 `data/blindspot_676g_stats.json`。
> **纪律**：不含任何未落盘数字；缺口**主动声明**（诚实优先，降低 desk-reject 风险）。
> **⚠️ 政策更新（677a）**：NeurIPS **2026 起 D&B 更名为 E&D（Evaluations & Datasets）**，
> 且**通常要求双盲**（不再是"D&B 允许单盲或双盲、作者自选"）。本稿按 **2027 E&D track** 准备：
> **当前为匿名版**，提交前须确认补充材料无身份信息。**2027 CFP 未发布 ⇒ 模板与规范须在 CFP 发布后复核。**
> **模板说明**：正文暂用 `neurips_2025.sty` 作 **placeholder**（第三方文件，不改），PDF 页脚的
> "Submitted to 39th Conference … (NeurIPS 2025)" 是 placeholder 伪影；2027 E&D 样式发布后迁移。
> **待办登记（只登记不实现，2027 规范未定）**：Croissant metadata、RAI metadata 须在投稿前生成。
> **v1.2（677a）**：全文术语统一为 **evidence-acquisition verifier**（pass ≠ 语义真值）；盲区 38.4% 加
> instrument-boundary 口径；VC 73.8% 去掉无抽样基础的 CI；e-process 降级为 **exploratory**；
> `planted=false` 表述改为 **source-derived reconstruction**；盲区高盲类型数统一为 **18/70**。
> **v1.1（673i）**：外部工具对比（clang-tidy/cppcheck，E9）；局限补充 E9 为事后/探索性、corpus 打平。
> **676j 同步**：正文贡献表重构为 5 条（方法 / 大规模实证 / A5 全量 / 盲区地图 / 开源复现），数字全部对齐 **676f** 与 **676g**。英文正文 **496 词**（≤500）。
> **口径提醒**：数据集/盲区地图用 **1147**（去重前），A5 用 **1137**（去重后，派生 571 / 评估 566）；两套数字**不得相减**。

---

## 1. English version (submission)

> Dear NeurIPS Evaluations & Datasets Chairs and Reviewers,
>
> We submit **"Evolving Verifiers: Failure-Driven Evidence Acquisition with Auditable Provenance"** for the **Evaluations & Datasets (E&D)** track (renamed from Datasets & Benchmarks in 2026; we target the 2027 edition, typically **double-blind**).
>
> **Why E&D.** This is an **evaluation methodology** with a reproducible artifact and explicit **negative analysis**: we claim no new model or benchmark, only to make *"how well can we verify LLM-generated technical knowledge?"* externally checkable. Throughout, *"verifier" is used in the evidence-acquisition sense*: a `pass` verdict means no acquired evidence contradicts the assertion within our capability boundary, **not** that the assertion is semantically true.
>
> **Template note.** The 2027 CFP is not yet released; this draft uses the official `neurips_2025` style as a **placeholder** (the style file is third-party and unmodified), and will migrate to the 2027 E&D style upon release. Croissant and Responsible-AI metadata are registered as pre-submission TODOs.
>
> **Five contributions.**
> 1. **Formalized failure-driven verifier evolution.** The verifier's evidence-acquisition capability $\mathcal{C}$ evolves under an operator driven *only* by registered failures, with three checkable properties and a **falsification protocol**: six pre-registered ablations where **A0 − A5** can *reject* the mechanism. Auditability: Merkle roots over **5** controlled directories, a **452**-event ledger, a *kernel-independent* reconciler (current state; historical pinning partial).
> 2. **A large, caliber-audited empirical asset.** **1147** samples over **70** defect types, in **7 expansion batches** (expA–G). Provenance is three-valued: **968** `self-authored`, **74** `source-derived-reconstruction` (single-file teaching reconstructions of real CVEs/GitHub issues — **not** original production code), **0** `original-external-artifact`. Rates carry a four-state caliber (`unknown` first-class): the denominator alone moves the corpus rate by **9.9pp**.
> 3. **A full-scale falsification experiment (A5), with its robustness measured.** **1137 samples × 8 assets = 9096 real `detect` calls** (derivation 571 / evaluation 566, $k{=}4$): FD **54.6\%** vs Random **30.6\%** ($\Delta$ **+24.03pp**, $p{=}2.3\times10^{-41}$) and vs Static **24.7\%** (**+29.9pp**). The pre-registered parallel analysis collapses to $\Delta$ **0.0pp**, so we register it as **direction-only** (`uninterpretable`) with the *selection* effect at **≈ +7–12pp**; a **clone-family re-split** leaves the endpoint unchanged (**+23.0–+26.7pp**), excluding template leakage, while a **family-level bootstrap** gives an **effective $n\approx133$–140**.
> 4. **A capability-boundary map of the instrument.** On the **1147 × 8** matrix, sample-level detection is **61.6\%** and the blind spot **38.4\%**; **18 of 70** types exceed 50\% blind (deadlock 94.3\%, endianness 89.3\%; family gradient memory 15.2\% → link/ODR 67.7\%). This is an **instrument-boundary** statistic measured on our corpus with our 8-asset pool — it does **not** claim that 38.4\% of real-world C++ defects are undetectable — and it scopes every headline number to the *visible* region.
> 5. **Open artifact and reproducible pipeline.** Apache-2.0, DCO-signed; a fail-loud `docker/paper/run_all.sh` and `REPRODUCE.md`; one-command recomputation. (Croissant and Responsible-AI metadata are registered as pre-submission TODOs, since the 2027 metadata spec is not yet released.)
>
> **Headline.** Failure-driven verification reaches **82.9\%** blind-holdout recall (34/41, CI [67.9, 92.8]) and **62.5\%** corpus recall (40/64, [49.5, 74.3]), vs static caliber **2.4\%**/**17.2\%** ($\Delta$ **+80.5pp**/**+45.3pp**) and random proxy **9.8\%**/**21.9\%** ($\Delta$ **+73.2pp**/**+40.6pp**); exact McNemar $p\le3.0\times10^{-8}$, Cohen's $h\ge0.85$; the e-process layer is **exploratory** (not pre-registered, not used for confirmatory claims) and is reported in an appendix.
>
> **Prior work and limitations.** Benchmark-evolution evolves *items*, mutation-guided testing evolves *tests*, formal verification gives *proofs*, MiniCheck evolves *judge weights* — **none evolves the measuring stick while proving the change externally measurable and self-falsifiable.** Headline numbers depend on a WSL sanitizer environment and fail silently without it (corpus 35.0\%$\to$10.0\%, now checked by the reproduction script); $n{=}41/64$ is small for the two headline rates, though A5 carries a nominal $n{=}566$ (**effective $\approx133$–140** after clone-aware re-splitting); **38.4\%** of samples are structurally invisible to our assets; added samples were merged post-reveal (corpus shift +33.3pp, registered); the static arm is a caliber re-binning and the random arm an instrument-level proxy; single-cell verdicts carry **~5\%** run-to-run instability; our external-tool stress test (E9) ties cppcheck on corpus. We therefore claim **auditability** plus a same-sample advantage over the static-caliber and random-proxy arms — **not** superiority over a *real* static detector — and **no** "first-ever" claim.
>
> **Data and code.** Public (Apache-2.0, DCO); D2/D3/D4 recomputation commands in `REPLICATION.md`; A0–A4 remain design-only placeholders (A5 has run).
>
> We thank you for your consideration.
>
> Sincerely,
> The Authors

---

## 2. 中文对照（内部核对）

- **为什么投 E&D**：贡献是**评估方法学** + 可复现 artifact + **批判/负结果**分析。不主张新模型/新 benchmark，只主张让"验证能力有多强"变成**外部可查、可被自己否证**的问题。
- **术语口径（677a）**：全文 "verifier" 一律指 **evidence-acquisition 装置**——`pass` 只表示"在当前能力边界内未获得与之矛盾的证据"，**不是**语义正确性判断。
- **五条贡献**：①失败驱动演化形式化 + 否证协议（A0−A5）+ 可审计性三条件（Merkle 5 目录 + 452 账本 + 不依赖内核对账器，当前状态；历史钉定部分）；②大规模实证资产（**1147** 样本 × **70** 缺陷类型，**7 批扩样** expA–G；**provenance 三分类**：**968** self-authored / **74** source-derived-reconstruction（真实 CVE/issue 的**单文件教学化重构**，**非**原始生产代码）/ **0** original-external-artifact；四态口径，口径选择本身移动 corpus 率 **9.9pp**）；③**A5 全量否证实验**（**1137 × 8 = 9096 次真实 detect**，派生 571 / 评估 566，k=4：FD 54.6% vs Random 30.6%，Δ **+24.03pp**，p=2.3e-41，b=136/c=0；vs Static 24.7%，+29.9pp；并列分析 Δ=**0.0pp** ⇒ direction-only + 选择效应 **≈+7~12pp**（非退化池 k≤3 显著、k=4 为选集碰撞）；clone-aware 重切分后不变、**有效 n≈133–140**）；④**检测器能力边界地图**（1147×8：检出 61.6%、盲区 **38.4%**、**18/70** 类 >50%、家族金字塔 memory 15.2% → link/ODR 67.7%；**instrument-boundary 统计，非 C++ 普适结论**）；⑤**开源 + 可复现**（Apache-2.0 + DCO、fail-loud `docker/paper/run_all.sh`、`REPRODUCE.md`、单命令复算；Croissant/RAI 元数据**登记为投稿前待办**，2027 规范未定故未生成）。
- **核心结果**：holdout **82.9%** (34/41) / corpus **62.5%** (40/64)；vs Static 2.4%/17.2%；vs 随机仪器代理 9.8%/21.9%；p≤3.0×10⁻⁸、h≥0.85；e-process 为 **exploratory**（未预注册，不进 confirmatory claim）。
- **与已发表工作的区别 + 诚实局限**：benchmark 演化换题目、变异引导换测试、形式化给证明、MiniCheck 换权重——**没有一个在换"尺子"并证明换尺子可被外部度量且可自否证**。WSL 静默掉分；n=41/64 小（±5pp 需 236/378），但 A5 已达 n=566；**38.4% 结构性盲区**；扩样样本无盲态且 **corpus 子集偏移 +33.3pp 超预注册**；**Static 仍是口径重分箱**；**随机臂是仪器级代理**；**逐格判定 ~5% 跑间不稳定**；**E9 事后/探索性且 corpus 打平 cppcheck**。⇒ 只主张机制可审计 + 同批显著优于 Static 口径臂与随机代理臂，**不主张**优于真正静态检测器，**不声称首次**。
- **数据/代码**：Apache-2.0 公开 + DCO；D2/D3/D4 + 复算命令见 `REPLICATION.md`；A0–A4 标为设计占位符（A5 已跑）；Croissant / RAI 元数据**待办**（见 `research/latex/VERSION.md` §5）。

---

## 3. 使用提醒

1. **不要**写任何**未落盘**数字（如 A0–A4 的"预期提升"）。
2. **主动声明**缺口：小样本（头条率）/ 无盲态扩样（含 corpus 构成偏移）/ 真 `detect_static` 缺 / 随机臂非真 B3 / 38.4% 盲区 / ~5% 跑间不稳定——先说比被问更有利。
3. **口径纪律**：1147（数据集、盲区地图，去重前）与 1137（A5，去重后）是**同一池的两套计数**，A5 矩阵是 **1 回合**、头条率 82.9%/62.5% 是 **3 回合**——**三组数字互不可相减**。
4. **匿名策略（677a 更新）**：2026 起 **E&D 通常要求双盲**（D&B 时代"单盲/双盲自选"的政策已过时）。当前稿为匿名版，提交前须确认补充材料无身份信息。
5. **模板**：仍用 `neurips_2025.sty` 作 placeholder（第三方文件，**禁止修改**）；PDF 页脚 "NeurIPS 2025" 是 placeholder 伪影；**2027 CFP 发布后**迁移到 2027 E&D 样式。
6. **待办**：Croissant metadata / RAI metadata（2027 规范未定，只登记不实现）；`research/submission_checklist.md` 的 D&B 政策条目仍待更新。
7. 标题以**正文标题**为准（`Evolving Verifiers: Failure-Driven Evidence Acquisition with Auditable Provenance`）。
8. 本信数字与 `data/current_numbers.json` + `data/a5_676f_results.json` + `data/blindspot_676g_stats.json` 一致；建设线更新后**须同步本信**（含 `research/latex/cover_letter.tex` 的 LaTeX 孪生版）。
