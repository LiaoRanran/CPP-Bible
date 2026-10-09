# 706 Task B — README 旧题名修复报告

- 日期：2026-10-09
- 文件：`README.md`（根）

## 改了什么

§6「引用」的 BibTeX 条目 `@misc{liao2027queyi, ...}`：

| 字段 | 旧 | 新 |
|------|----|----|
| `title` | `Evolving Verifiers: Failure-Driven Portfolio Evolution for C++ Defect Detection`（**已退役题名**） | `Caliber Drift and Capability Boundaries: An Audit Protocol for Software-Verification Evaluation`（**现行题名**） |
| `note` | `NeurIPS 2027 Datasets \& Benchmarks track` | `NeurIPS 2027 Evaluations \& Datasets track` |

其余字段（author `Liao, Ran`、year `2027`、howpublished `https://github.com/LiaoRanran/CPP-Bible`、license `Apache-2.0`）经核对**正确**，未改。

## 验证

- `Select-String README.md "Evolving Verifiers|Failure-Driven Portfolio"` → **0 命中**（旧题名清零）。
- `Select-String README.md "Caliber Drift"` → 1 命中（§6 title 行）。

## 发现但**未改**的过时信息（超出本批 README-only 范围，登记待办）

> 任务书限定“只改 README.md”。以下为检查中发现的**其他文件**里的旧题名/旧框架残留，本批**不动**，登记给后续批次：

1. **`CITATION.cff` 仍用旧题名**（作者身份文件，本次不在范围内）：
   - 第 34 行：`title: "Evolving Verifiers: Failure-Driven Portfolio Evolution for C++ Defect Detection"`
   - 另有数据集 title 行：`"Queyi: Failure-Driven Verifier Evolution for C++ Defect Detection (datasets, benchmark, and tooling)"`
   - **建议**：后续批次同步为现行题名（并注意 CITATION.cff 含作者信息，投稿匿名版不应包含它）。
2. **README 正文框架仍为旧定位**：§1「一句话」、§2 标题仍以“失败驱动演化检测器组合”为主线；现行论文已转向“审计协议 + 负面结果”框架（v1.4 reframe）。本批**未重写**（任务书要求不做全面重写），仅在此登记。

## 产物

- 修改：`README.md`（仅 §6 两行）
- 新增：`data/706_readme_fix_report.md`（本文件）
