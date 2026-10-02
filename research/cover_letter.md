# Cover Letter — Evolving Verifiers (NeurIPS 2027 Datasets & Benchmarks)

> **性质**：投稿信（英文版为准；中文对照供内部核对）。
> **数字基线**：`data/current_numbers.json`（schema `queyi-current-numbers/672h`）。
> **纪律**：不含任何未落盘数字；缺口**主动声明**（诚实优先，降低 desk-reject 风险）。
> **注意（D&B 政策）**：NeurIPS 2025 D&B 允许**单盲或双盲**（作者自选）。本稿当前为**匿名版**；
> 若选单盲须补作者信息，若选双盲须确认补充材料无身份信息。**2027 CFP 未发布，须复核。**
> **v1.1（673i）**：第 5 条贡献（外部工具对比 clang-tidy/cppcheck，E9）；局限补充 E9 为事后/探索性、corpus 打平。
> **673k 精简**：英文正文压至 ≤500 词（贡献点与数字全保留，仅删冗余铺垫）。

---

## 1. English version (submission)

> Dear NeurIPS Datasets & Benchmarks Chairs and Reviewers,
>
> We submit **"Evolving Verifiers: Failure-Driven Evidence Acquisition with Auditable Provenance"** for the **Datasets & Benchmarks** track.
>
> **Why E&D.** This is an **evaluation methodology** with a reproducible artifact and explicit **negative analysis**; we claim no new model or benchmark, only a way to make *"how well can we verify LLM-generated technical knowledge?"* externally checkable.
>
> **Five contributions.**
> 1. **Formalized failure-driven verifier evolution.** The verifier's evidence-acquisition capability $\mathcal{C}$ evolves under an operator driven *only* by registered failures, with three checkable properties (monotonicity, minimality, auditability) and a **falsification protocol**: six pre-registered ablations where **A0 − A5** can *reject* the core mechanism if its interval crosses zero.
> 2. **Information-theoretic analysis of the four-state verdict** (`pass`/`fail`/`unknown`/`contradict`, `unknown` first-class): denominator $=$ catch $+$ miss is the only non-contaminating caliber (**9.9pp** external-corpus effect); the four states are the two orthogonal orders of Belnap's four-valued logic.
> 3. **Three formal auditability conditions** — origin traceability, state reproducibility, tamper detectability — realized by Merkle roots over **5** controlled directories, a **452**-event append-only ledger, and a *kernel-independent* reconciler.
> 4. **Same-sample, budget-matched three-arm contrast** (failure-driven vs static caliber vs random) with exact McNemar, Cohen's $h$, and anytime-valid e-values, plus **two negative results**: an LLM judge arm (more sensitive, far less specific) and an external anchor missing H2 by 0.8pp.
> 5. **Honest external-tool comparison (E9)** against clang-tidy and cppcheck on the same 41/64 samples: under the only defensible caliber FD beats clang-tidy on holdout (82.9\% vs 48.8\%, $p{=}1.2\times10^{-4}$, $c{=}0$) but only *ties* cppcheck on corpus (62.5\% vs 54.7\%, $p{=}0.383$); 8 named reverse pairs expose FD's blind spot (compile-time-visible and path-not-executed defects). Our pre-registered main caliber is reported as a *failed* control (100\% recall, 100\% FPR); the defensible caliber is post-hoc/exploratory.
>
> **Headline.** Failure-driven verification reaches **82.9\%** blind-holdout recall (34/41, CI [67.9, 92.8]) and **62.5\%** corpus recall (40/64, [49.5, 74.3]), vs static caliber **2.4\%**/**17.2\%** ($\Delta$ **+80.5pp**/**+45.3pp**) and random proxy **9.8\%**/**21.9\%** ($\Delta$ **+73.2pp**/**+40.6pp**); exact McNemar $p\le3.0\times10^{-8}$, Cohen's $h\ge0.85$, e-values to $2.5\times10^{8}$.
>
> **Prior work and limitations.** Benchmark-evolution evolves *items*, mutation-guided testing evolves *tests*, formal verification gives *proofs*, MiniCheck evolves *judge weights* — **none evolves the measuring stick while proving the change externally measurable and self-falsifiable.** Headline numbers depend on a WSL sanitizer environment and fail silently without it (35.0\%$\to$10.0\%); $n{=}41/64$ is small ($\pm$5pp needs $n{=}236/378$); added samples were merged post-reveal (corpus subset shift +33.3pp, registered); the static arm is a caliber re-binning; the random arm an instrument-level proxy (true B3 only at 672g on $n{=}21/48$). E9 is post-hoc and ties cppcheck on corpus. We therefore claim **auditability** plus a same-sample advantage over the static-caliber and random-proxy arms — **not** superiority over a *real* static detector — and make **no** "first-ever" claim.
>
> **Data and code.** Public (Apache-2.0, DCO). D2/D3/D4 and recomputation commands in `REPLICATION.md`; Croissant metadata in supplementary material. Every number recomputes from landed artifacts; un-landed values (ablations) are marked as placeholders.
>
> We thank you for your consideration.
>
> Sincerely,
> The Authors

---

## 2. 中文对照（内部核对）

- **为什么投 E&D**：贡献是**评估方法学** + 可复现 artifact + **批判/负结果**分析。不主张新模型/新 benchmark，只主张让"验证能力有多强"变成**外部可查、可被自己否证**的问题。
- **五条贡献**：①失败驱动演化形式化 + 否证协议（A0−A5）；②四态判决的信息论口径分析（含 9.9pp 口径消融；Belnap 四值逻辑）；③可审计性三条件（Merkle 5 目录 + 452 账本 + 不依赖内核对账器）；④同批配对三臂对照（McNemar + Cohen's h + e-value）+ **两个诚实的负结果**；⑤**外部工具对比（clang-tidy / cppcheck，E9）**：holdout 82.9% vs 48.8%（p=1.2e-4, c=0），corpus 62.5% vs 54.7%（p=0.383 打平）；8 条反向对点名 FD 短板（编译期可见 / 路径未执行缺陷）；主口径失败（100% 召回 + 100% FPR），StrictA 为事后口径。
- **核心结果**：holdout **82.9%** (34/41) / corpus **62.5%** (40/64)；vs Static 2.4%/17.2%；vs 随机仪器代理 9.8%/21.9%；p≤3.0×10⁻⁸、h≥0.85、e-value 至 2.5×10⁸。
- **与已发表工作的区别 + 诚实局限**：benchmark 演化换题目、变异引导换测试、形式化给证明、MiniCheck 换权重——**没有一个在换"尺子"并证明换尺子可被外部度量且可自否证**。WSL 静默掉分；n=41/64 小（±5pp 需 236/378）；扩样样本无盲态且 **corpus 子集偏移 +33.3pp 超预注册**；**Static 仍是口径重分箱**；**随机臂是仪器级代理**（真 B3 只在 672g 旧分母跑过）；**E9 事后/探索性且 corpus 打平 cppcheck**。⇒ 只主张机制可审计 + 同批显著优于 Static 口径臂与随机代理臂，**不主张**优于真正静态检测器，**不声称首次**。
- **数据/代码**：Apache-2.0 公开 + DCO；D2/D3/D4 + 复算命令见 `REPLICATION.md`；Croissant 元数据随补充材料；未落盘值（ablation）标为占位符。

---

## 3. 使用提醒

1. **不要**写任何**未落盘**数字（如 ablation 的"预期提升"）。
2. **主动声明**四条缺口：小样本 / 无盲态扩样（含 corpus 构成偏移）/ 真 `detect_static` 缺 / 随机臂非真 B3——先说比被问更有利。
3. **匿名策略**：D&B 允许单盲或双盲；当前稿为匿名版。选单盲须补作者块；选双盲须确认补充材料无身份信息。
4. 标题以**正文标题**为准（`Evolving Verifiers: Failure-Driven Evidence Acquisition with Auditable Provenance`）。
5. 本信数字与 `data/current_numbers.json` 一致；建设线更新后**须同步本信**。