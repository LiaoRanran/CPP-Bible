# 709 Task A — CITATION.cff 旧题名修复报告

- 日期：2026-10-09
- 文件：`CITATION.cff`（根）
- 背景：706 只改了 README §6，CITATION.cff 仍写旧题名 `Evolving Verifiers`（706 已登记待办）。

## 1. 改了什么

| 字段 | 旧 | 新 |
|------|----|----|
| `title`（库标题） | `Queyi: Failure-Driven Verifier Evolution for C++ Defect Detection (datasets, benchmark, and tooling)` | `Caliber Drift and Capability Boundaries: An Audit Protocol for Software-Verification Evaluation` |
| `preferred-citation.title` | `Evolving Verifiers: Failure-Driven Portfolio Evolution for C++ Defect Detection` | 同上（现行题名） |
| `abstract` | 以 `failure-driven evolution of C++ defect detector portfolios` 开头（**已退役框架**） | 改为**审计框架**：`reproducible audit toolchain for software-verification evaluation` + 两个数据集（冻结矩阵 / 真实靶场）保留 |
| `authors` / `year` / `repository-code` | Liao Ran / 2027 / github.com/LiaoRanran/CPP-Bible | **核对无需修改**（作者、目标年份、仓库 URL 均现行有效） |

> 说明：`abstract` 的刷新属「同类陈旧定位」一并修复（与 706 在 README 登记的「旧框架残留」同类）；已在本报告登记。

## 2. 验证

```
YAML_OK
title= Caliber Drift and Capability Boundaries: An Audit Protocol for Software-Verification Evaluation
pref_title= 同上
authors= ['Liao']   year= 2027   url= https://github.com/LiaoRanran/CPP-Bible
```
- `yaml.safe_load` 解析通过（CFF 1.2.0 结构未破坏）。
- `grep "Evolving Verifiers"` → **0 命中**（旧题名清零）。

## 3. 诚实边界

- 本任务**只改 CPP-Bible 源仓库**的 CITATION.cff（含作者信息，符合该仓库定位）；**新仓库 queyi-audit 的 CITATION.cff 另行匿名化**（见 709 Task G）。
- 未改 `version` / `date-released`（`1.0.0` / `2026-10-07` 仍准确）。
- 未声称 CITATION.cff 的 `abstract` 与论文摘要逐字一致（它描述的是**仓库/研究线**，不是论文摘要）。

## 4. 产物

- 修改：`CITATION.cff`（title / preferred-citation.title / abstract）
- 本报告
