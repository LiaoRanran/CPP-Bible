# 703-A · Cover Letter 重写 changelog

- **批次**：703 ｜ **任务**：A ｜ **日期**：2026-10-09
- **文件**：`research/latex/cover_letter.tex`（v1.6/692 → **v1.7/703**）、
  `research/cover_letter.md`（镜像同步 v1.7/703）
- **编译**：`cd research/latex && tectonic cover_letter.tex` ⇒ **0 错**（仅 1 条 Overfull hbox 警告）
- **词数**：叙述体 **495 词** ≤ 500（从 "To the NeurIPS" 到 "The Authors"，去 LaTeX 命令后计数）
- **红线**：未 push；未跑 `detect()`；未改检测器/样本/冻结矩阵；未改论文正文与 bib。

---

## 1. 为什么重写

703 任务书给出的背景是"当前 CL 还是旧版本（Evolving Verifiers 定位）"。
**实测该前提已过时**：`research/latex/cover_letter.tex` 在 689/691/692 已随论文重构到
"Caliber Drift and Capability Boundaries" 定位，**不是** "Evolving Verifiers"。

但任务书的**实质要求仍然成立**：v1.6 的信**只以"实证审计"为主线**，
没有把 700 批次的**理论发现**（公理独立性 / 不完备性 / 信息论下界 / 双设计）
与 699/700-D 的**跨领域证据**写进去。⇒ **按任务书的实质意图，完全重写**（不是改错别字）。

---

## 2. 逐项改动

| # | 改动 | 依据 |
|---|---|---|
| 1 | **主线从"实证审计"改为"四条贡献"**：①测量漂移代数 ②结构性 Goodhart 四型 ③能力边界地图 ④真实 CVE 验证 | 703 任务书 §A "核心贡献" 列表 |
| 2 | 新增"**只有 2 条公理独立**（单调 A2 / 超可加 A5）、4 条是定理、1 条是元公理" | `data/700_metatheory.md` §1.4 |
| 3 | 新增"**系统不完备、缺 A8（标签轴闭包）**" | `data/700_metatheory.md` §2.1 |
| 4 | 新增"**口径套利 NP-hard + 贪心 $(1-1/e)$ 近似**" | `data/700_metatheory.md` §4 |
| 5 | 新增"**Type III/IV 不改变任何逐样本裁决**" | `data/698_structural_goodhart_empirical.md`、700-B §1.2 |
| 6 | 新增"**配对设计对 Type III/IV 功效恒为 0（$\psi=0$）⇒ Step 3 改双设计**"；Type I $n\approx849$、Type II $n=17$ | `data/700_information_theory.md` §2、结论 C1–C3 |
| 7 | 关键数字补 **+24.03pp 在 $k=4$ 塌缩为 0.00pp（$p=1.0$）** | 论文 F1；`data/a5_676f_results.json` |
| 8 | 关键数字补 **60.07% → 24.74%，Δunknown 0.00pp（unaware）vs 75.27pp（aware）** | `data/696_transition_matrix.json`；本批 703-E 复算一致 |
| 9 | 关键数字补 **演化算子全档 Δ=0（≡ greedy set-cover）** | 论文 F5；700-E/F |
| 10 | 贡献③写死 **38.4%（440/1147）/ 13 of 34 / 41.5%** | 论文 F2；`data/blindspot_676g_stats.json` |
| 11 | 贡献④写死 **110 条 CVE 重构 / 59.09%** | 论文 F3；`data/external_corpus_reveal_672h.json` |
| 12 | **诚实声明扩充**：新增"公理系统不完备（缺 A8）"与"699 的 **22 个原始项目均未编译**" | `data/700_metatheory.md` §2.1；`data/699_批次完成报告.md` §诚实声明 |
| 13 | 保留并强化"**human IAA = 0**、κ 全部为 AI self-consistency、145 条标注包**未执行**" | 论文 T1；`data/689_human_annotation_protocol.md` |
| 14 | 删除旧版独立的小节式罗列（F1–F5 五条"Quantitative findings"），改为**四条贡献 + 关键数字**两段 | 任务书要求"完全重写" |
| 15 | 删去独立 `thebibliography` 块（4 条引用） | 引用改为**行内点名**（DeepFact / 指标协同演化 / 可证证书自演化 / SV-COMP），省 ~40 词，避免与论文 bib 双份维护 |

---

## 3. 关于题名（**必须记录的偏差**）

任务书写：*"标题：不再强调 'Evolving Verifiers'，改为 'Auditing the Evaluator'"*。

**本批未采用 "Auditing the Evaluator"**，理由：

1. 该题名是 **v1.4(689) 的工作题名**，已在 **v1.5(691) 主动退役**——
   2026 年撞名核查发现 "Auditing the Evaluators"（PROPOR 2026）、
   "Evaluator Stress Test"（ACL Findings 2026）、DeepFact 的 "audit-then-score"、
   BabelJudge 的 "reliability audit framework" 已占据该命名区（见 `research/latex/VERSION.md` §1）。
2. 投稿信**必须携带论文自己的题名（verbatim）**；论文题名是
   *Caliber Drift and Capability Boundaries: An Audit Protocol for Software-Verification Evaluation*。
3. ⇒ 任务书"不再强调 Evolving Verifiers"的**实质意图已满足**（v1.6 起即不含该措辞），
   但**具体题名以论文 version of record 为准**。

---

## 4. 数字一致性核对（CL ↔ 论文 ↔ 数据源）

| 数字 | CL v1.7 | 论文 v1.1.tex | 数据源 |
|---|---|---|---|
| +24.03pp / $k{=}4$ 塌缩 | ✅ | F1（+24.03pp, 0.00pp, p=1.0） | `a5_676f_results.json` |
| 机制级残留 +7.4–11.3pp | ✅ | F1（+7.42pp） | 同上 |
| 60.07% → 24.74% | ✅ | 附录 `app:driftalgebra`（566 帧） | `696_transition_matrix.json` |
| Δunknown 0.00 / 75.27pp | ✅ | 同上 | 同上；703-E 复算一致 |
| 38.4% = 440/1147 | ✅ | F2 | `blindspot_676g_stats.json` |
| 13 of 34 | ✅ | F2 | 同上 |
| 41.5% 单资产 | ✅ | F2 | 同上 |
| 110 / 59.09% | ✅ | F3 | `external_corpus_reveal_672h.json` |
| 演化 Δ=0 全档 | ✅ | F5 | 附录 `app:operator683` |
| 849 / 17 | ✅ | 本批新增（任务 C） | `700_sample_complexity.json` |

---

## 5. 诚实边界

1. 本批**未做**任何新实验：CL 里每个数字都来自**已落盘的冻结产物**（700 批次 + 论文 F1–F5 + 本批 703-E 复算）。
2. "495 词"是按 `research/cover_letter.md` §3 的口径（去 LaTeX 命令）计数的**本批实测值**；
   换计数脚本（如把 `$k{=}4$` 算成 3 个 token）会得到 495–504 的不同值 ⇒ 已同时给出
   "naive split() = 469" 作对照。
3. 题名与任务书建议不一致，已在 §3 **显式登记**，未静默二选一。
4. 旧版 CL 的 `thebibliography` 块被删除 ⇒ 若评审要求 CL 自带参考文献，需在投稿前补回。

---

*文件生成：2026-10-09 ｜ 批次 703 任务 A ｜ 编译 0 错 ｜ 未 push*
