# Research Protocol v0.1 (658 G)

> 这是**实验宪法**，不是论文草稿。先规定"怎样才算证明"，再跑实验。
> 来源：GPT 第五轮审阅建议 + 658 外部效度四层（A 段）。

## 冻结项（v0.1 锁死，改则升 v1.1，旧版保留）

1. **研究问题 RQ1–RQ4**（见 01_research_questions.md）—— 不搞七八个。
2. **数据集切分 D0–D4**（见 06_datasets.md）—— Development / Historical / Blind / External / Independent。
3. **评估流程 Phase 0–7**（见 05_evaluation_protocol.md）。

## 目录

| 文件 | 内容 |
|---|---|
| 00_problem.md | 研究什么问题 |
| 01_research_questions.md | RQ1–RQ4 |
| 02_hypotheses.md | H0 + H1–H4 |
| 03_system_boundary.md | 系统边界 |
| 04_threat_model.md | 12 类威胁 |
| 05_evaluation_protocol.md | 实验流程 |
| 06_datasets.md | D0–D4 |
| 07_baselines.md | B0–B3 |
| 08_metrics.md | 主/次指标 |
| 09_ablations.md | A0–A4 |
| 10_analysis_plan.md | 结果分析 |
| 11_reproducibility.md | 复现 |
| 12_threats_to_validity.md | 五层威胁 |
| 13_ai_use_and_authorship.md | AI 使用登记 |
| CHANGELOG.md | 变更 |

## 反自证原则
本研究的"发动机"（queyi 验证器）**不得自己证明自己**：
- 元状态由 `tools/status_reconciler_658.py`（不依赖 queyi core）对账；
- 盲化 holdout（A2）一旦 reveal 不可逆；
- 任何语义能力升级须经独立验收边界（658 宪法）。
