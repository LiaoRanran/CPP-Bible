# 715 · 任务 1.3：Related Work 升级报告

- 批次：715 ｜ 任务：Part 1.3 ｜ 日期：2026-10-10
- 修改文件：`research/latex/queyi_neurips2027_v1.1.tex`、`research/latex/paper2_measurement_drift.tex`、
  `research/latex/queyi_refs.bib`、`research/latex/paper2_refs.bib`

---

## 1. 升级前的实测状态（可复跑）

| 先行工作 | bib 键 | 论文 1 正文 | 论文 2 正文 |
|---|---|---|---|
| Li et al., *Auditing the Audit* | `li2026auditingaudit` | ❌ 只在一个从句里（"Validity audits now audit the audit itself"） | ❌ 只在并列从句里（"Adjacent negative results include audit failure modes"） |
| Chen et al., *A Judge Should Know What Changed* | `chen2026judge` | ❌ **全文未引**（而它的"表面特征预测器复现 55–67% 标注"与本文 T1 的 $\kappa{=}0.437/0.157$ 直接呼应） | ✅ 已引且写得好 |
| Freiesleben & Zezulka, *The Benchmarking Epistemology* | `freiesleben2025…` | ❌ 只在附录锚点清单出现一次 | ⚠️ 一个从句 |
| "非系统检索"声明 | — | ❌ 无 | ❌ 无（只有 no-priority，未覆盖检索方式） |

---

## 2. 已落地的修改

### 2.1 Li et al. 升级为完整段落（两篇，各按侧重）

**论文 1**（新增 `\paragraph{The most adjacent work, and how the objects differ.}`）：

- 完整交代其五类**管线级**失效模式 F1–F5 与六点 due-diligence gate；
- 核心分野（任务卡要求的第 2 点）：**他们的五模式是"单次审计管线的横截面实现缺陷（bug）"，我们的八失效模式是"跨测量的口径变化（决策）"**——一句话点题："A no-op perturbation is a defect; a changed denominator is a decision."；
- 立场差异：他们的输出是**扣留协议**（不给效度判决），我们给**四态分级**；
- 明写"shared goal + form"（同做审计的审计、同为"分类法 + 闸门"形态），避免读成抢功。

**论文 2**（新增独立段落）：同一骨架，但把第 2 点落在 **F5（metric-archetype mismatch）↔ Type IV 聚合漂移** 这一条真正相邻的轴上。

> 按 714 §3.5 的提醒：两篇**没有**写完全相同的对比文字——论文 1 侧重"失效模式 vs 八模式"，论文 2 侧重"管线缺陷 vs 跨测量漂移 + F5 ↔ Type IV"。

### 2.2 Chen et al. 补入论文 1 的 §T1 标签效度（任务卡第 3 点）

落点：T1 段（`expected_verdict $\kappa{=}0.437$`、`severity $\kappa{=}0.157$`）之后，新增：

> This pattern has a direct published analogue: \citet{chen2026judge} find that surface-only predictors reproduce 55%–67% of labels across five public label sets, including 67.4% of MT-Bench human votes, and conclude that a validation set must itself be audited. Both results say the same thing—a substantial share of what a verdict or label records is predictable from surface features rather than from the construct—and both argue for auditing the validation set itself, not only the evaluator.

bib：`chen2026judge` 从 `paper2_refs.bib` 复制进 `queyi_refs.bib`（**新增 13 行**），note 里补上了 55–67% / 67.4% 这两个被正文引用的数字，便于审稿人按 note 复核。

### 2.3 Freiesleben & Zezulka 升级为定位段（两篇）

论文 1 新增 7 行、论文 2 新增 7 行，同一论点：**caliber 五元组是他们对"benchmark 作为测量工具"的效度条件在更细粒度上的操作化**——"where they ask whether a score licenses an inference about *progress or predictability*, we ask whether a rate survives *a change in how it was measured*"；并明确"**不主张他们的条件不充分**，只主张在组件可配置的装置上这些条件**没有声明的 caliber 就无法检查**"。

**bib 键统一**：`freiesleben2025benchmarkingepistemology` → `freiesleben2026benchmarkingepistemology`（期刊版年份为 2026，而条目里 `year` 本来就写 2026，键名是笔误）。4 处（两 tex + 两 bib）全部替换，实测 0 残留。

### 2.4 "非系统检索"声明（两篇）

论文 1 接在 Li 段之后；论文 2 接在 `Scope and honesty` 段之后：

> *Scope of our literature search:* our 2026 references were located by general web search, not by a systematic review (no Scopus / DBLP / ACM DL full-text search), so adjacency claims should be read as "we did not find a closer work", not as "no closer work exists".

这条同时回应 714 诚实性复查 O-23 的"据我们所知首次"问题：**把"我们没找到"与"不存在"分开**。

---

## 3. 未做（诚实登记）

| 项 | 原因 |
|---|---|
| `huang2026deepfact` 从 `@misc` 升为 ACL 2026 `@inproceedings` | 714 列为 P1/P2；本批未取到正式出处（venue 页），**不凭记忆改 bib** |
| `beyer2026svcomp` 正文措辞改"the SV-COMP 2026 report" | P2；本批未动 |
| `sengupta2026anytimevalid` 措辞复核 | P2；本批未动 |
| `2607.02577`（Bhat）与 `2607.02586`（Li）是否串号 | 714 已核为**两个不同条目**；本批未复检 |
| 两篇 bib 的重复条目比例与 `unverified-memory` 清单 | 714 未完成项 5，本批未动 |

**为什么不做**：这四条都属于"camera-ready 前完成即可"（714 §5 的原话），而本批的红线是"论文修改必须编译验证"——在拿不到一手出处的条件下改 bib，风险大于收益。
