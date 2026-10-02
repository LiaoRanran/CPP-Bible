# Cover Letter — Evolving Verifiers (NeurIPS 2027 Datasets & Benchmarks)

> **性质**：投稿信（英文版为准；中文对照供内部核对）。
> **数字基线**：`data/current_numbers.json`（schema `queyi-current-numbers/672h`）。
> **纪律**：不含任何未落盘数字；缺口**主动声明**（诚实优先，降低 desk-reject 风险）。
> **注意（D&B 政策）**：NeurIPS 2025 D&B 允许**单盲或双盲**（作者自选）。本稿当前为**匿名版**；
> 若选单盲须补作者信息，若选双盲须确认补充材料无身份信息。**2027 CFP 未发布，须复核。**

---

## 1. English version (submission)

> Dear NeurIPS Datasets & Benchmarks Chairs and Reviewers,
>
> We submit **"Evolving Verifiers: Failure-Driven Evidence Acquisition with Auditable Provenance"** for consideration in the **Datasets & Benchmarks** track.
>
> **Why this fits E&D.** Our contribution is an **evaluation methodology** with a fully reproducible artifact and an explicit **critical / negative analysis** — the three things E&D asks for. We do not claim a new model or a new benchmark; we claim a way to make *"how well can we verify LLM-generated technical knowledge?"* an **externally checkable** question.
>
> **Core contributions.**
> 1. **A formalization of failure-driven verifier evolution.** The verifier's evidence-acquisition capability $\mathcal{C}$ evolves under an operator $E(\mathcal{C}_t, F_t)$ driven *only* by registered failures, with three checkable properties (monotonicity, minimality, auditability). We add a **falsification protocol**: six pre-registered ablation groups where the contrast **A0 − A5** can *reject* the core mechanism if its confidence interval crosses zero.
> 2. **An information-theoretic analysis of the four-state verdict** (`pass`/`fail`/`unknown`/`contradict`, `unknown` first-class), showing that denominator $=$ catch $+$ miss is the only non-contaminating caliber — with an empirical caliber ablation (**9.9pp** effect on the external corpus). Formally the four states are the two orthogonal orders of Belnap's four-valued logic.
> 3. **Three formal conditions for auditability** — origin traceability, state reproducibility, tamper detectability — realized by Merkle roots over **5** controlled directories, a **452**-event append-only ledger, and a *kernel-independent* meta-state reconciler.
> 4. **A same-sample, budget-matched, three-arm contrast** (failure-driven vs. static caliber vs. random) with exact McNemar tests, Cohen's $h$ and e-process anytime-valid e-values — plus **two honest negative results**: an LLM judge arm that is more sensitive but far less specific, and an external anchor whose pre-registered H2 misses by 0.8pp.
>
> **Headline result.** On the *same* samples, failure-driven (FD) verification reaches **82.9%** blind-holdout recall (34/41, 95% CI [67.9, 92.8]) and **62.5%** corpus measurable recall (40/64, [49.5, 74.3]), versus a **static caliber arm** at **2.4%** / **17.2%** ($\Delta$ **+80.5pp** / **+45.3pp**) and a **random instrument-level proxy** at **9.8%** / **21.9%** ($\Delta$ **+73.2pp** / **+40.6pp**). Exact McNemar $p\le3.0\times10^{-8}$; Cohen's $h\ge0.85$; $\Delta$ lower bound $\ge$ **28.6pp** across all four paired contrasts; e-values reach $2.5\times10^{8}$.
>
> **Relation to prior work.** Benchmark-evolution lines (Benchmark Self-Evolving, ArenaBencher, LiveBench) evolve the *items*; mutation-guided testing (Meta ACH, MUTGEN) evolves *tests*; formal verification (seL4, CompCert) provides *proofs*; MiniCheck evolves the *judge's weights*; CELEUS uses e-processes to *save samples* in LLM evaluation. **None evolves the measuring stick itself while proving the change is externally measurable and self-falsifiable.** That is our position.
>
> **Honest limitations (stated up front).** Two headline numbers depend on a specific WSL sanitizer environment and **fail silently** when it is absent (35.0% → 10.0%); sample sizes remain small ($n=41/64$ measurable — we report *direction and intervals*, not magnitude; $\pm$5pp half-width needs $n=236/378$); newly added samples were merged **after** reveal (no blind state), and the **corpus subset shift is +33.3pp, outside the pre-registered range**, registered as a composition shift; the **static arm is a caliber re-binning** (not a re-run of a real static detector); and the random arm is an **instrument-level proxy** — the true B3 was wired and run at 672g, but only on the older $n=21/48$. We therefore claim **auditability of the mechanism** plus a **significant same-sample advantage over the static-caliber and random-proxy arms** — **not** superiority over a *real* static detector, and we make **no** "first-ever" claim.
>
> **Data and code availability.** The repository is public (Apache-2.0) with DCO sign-off. Datasets D2/D3/D4 and the recomputation commands are described in `REPLICATION.md`; Croissant metadata will be provided in the supplementary material. Every reported number is recomputed from landed artifacts; the paper marks any not-yet-landed value explicitly (the ablation results are placeholders) rather than filling in estimates.
>
> **Reproducibility.** All headline numbers are reproducible via single commands; the paper documents the exact environment dependencies (WSL, `g++`, `setarch`) and reports `UNVERIFIED` rather than a misleading low score when a dependency is missing.
>
> We believe this work matches E&D's stated interest in rigorous evaluation practices, transparent artifacts, and critical analysis. We thank you for your consideration.
>
> Sincerely,
> The Authors

---

## 2. 中文对照（内部核对）

- **为什么投 E&D**：贡献是**评估方法学** + 可复现 artifact + **批判/负结果**分析——E&D 三要素。不主张新模型/新 benchmark，只主张让"验证能力有多强"变成**外部可查、可被自己否证**的问题。
- **四条贡献**：①失败驱动演化形式化 + 否证协议（A0−A5）；②四态判决的信息论口径分析（含 9.9pp 口径消融；Belnap 四值逻辑对接）；③可审计性三条件（Merkle 5 目录 + 452 账本 + 不依赖内核的对账器）；④同批配对三臂对照（McNemar + Cohen's h + e-value）+ **两个诚实的负结果**。
- **核心结果**：holdout **82.9%** (34/41) / corpus **62.5%** (40/64)；vs Static 2.4%/17.2%；vs 随机仪器代理 9.8%/21.9%；p≤3.0×10⁻⁸、h≥0.85、Δ 下界 ≥28.6pp。
- **与已发表工作的区别**：benchmark 演化换题目、变异引导换测试、形式化给证明、MiniCheck 换权重、CELEUS 用 e-process 省样本——**没有一个在换"尺子"并证明换尺子可被外部度量且可自否证**。
- **诚实局限（前置）**：WSL 静默掉分；n=41/64 小（±5pp 需 236/378）；扩样样本无盲态且 **corpus 子集偏移 +33.3pp 超预注册**；**Static 仍是口径重分箱**；**随机臂是仪器级代理**（真 B3 只在 672g 旧分母上跑过）。⇒ 只主张机制可审计 + 同批显著优于 Static 口径臂与随机代理臂，**不主张**优于真正静态检测器，**不声称首次**。
- **数据/代码**：Apache-2.0 公开 + DCO；D2/D3/D4 + 复算命令见 `REPLICATION.md`；Croissant 元数据随补充材料。

---

## 3. 使用提醒

1. **不要**写任何**未落盘**数字（如 ablation 的"预期提升"）。
2. **主动声明**四条缺口：小样本 / 无盲态扩样（含 corpus 构成偏移）/ 真 `detect_static` 缺 / 随机臂非真 B3——先说比被问更有利。
3. **匿名策略**：D&B 允许单盲或双盲；当前稿为匿名版。选单盲须补作者块；选双盲须确认补充材料无身份信息。
4. 标题以**正文标题**为准（`Evolving Verifiers: Failure-Driven Evidence Acquisition with Auditable Provenance`）。
5. 本信数字与 `data/current_numbers.json` 一致；建设线更新后**须同步本信**。
