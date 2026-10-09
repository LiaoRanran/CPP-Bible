# 709 Task F — 新仓库文件复制报告

- 日期：2026-10-09
- 源：`C:\CodeLearnling\note\note\C++\CPP-Bible`（**只读复制**，源仓库零改动）
- 目标：`C:\CodeLearnling\queyi-audit`（新建，`git init` + `git branch -M main`）

## 1. 复制清单（105 项）

| 目标路径 | 内容 |
|---|---|
| `paper/paper1/` | `queyi_neurips2027_v1.1.tex`、`queyi_refs.bib`、`cover_letter.tex`、`neurips_2025.sty` |
| `paper/paper1/supplementary/` | 第一篇 supplementary 目录（含 706 移出的 `paper_appendix_extras.tex`） |
| `paper/paper2/` | `paper2_measurement_drift.tex`、`paper2_refs.bib`、`paper2_cover_letter.tex`、`paper2_abstract.tex`、`neurips_2025.sty` |
| `data/frozen_matrix/` | 冻结矩阵与权威结果 JSON（含从 `verify_paper_numbers.py::SOURCE_FILES` 解析出的全部依赖） |
| `data/annotation_package/` | 人类标注材料包（145 条，去标识） |
| `data/raw_external/` | 40 个真实 CVE 案例库 |
| `tools/` | 论文相关脚本 + `tools/utils/`（以 `verify_paper_numbers.py` 的依赖闭包为准） |
| `Scripts/` | 环境体检 + 一键复现脚本 |
| `docker/` | 容器配方（未实测构建） |
| `tests/test_707.py` | 707 落地工具测试 |
| `LICENSE`, `pyproject.toml`, `.gitignore` | 许可证 / lint 配置 / 构建产物排除 |

**复制结果：`copied = 105`，`skipped = 2`**
- `data/693_type_stats_normalized.json`（源中不存在；权威文件是 `681_type_stats_normalized.json`，已复制）
- `data/blindspot_676g_ckpt_san.jsonl`（SOURE_FILES 依赖探测得到，非本包所需）

## 2. **不复制**（按任务书）

- 学习笔记（`Book/`、`Examples/`、`atoms/`、`evidence/`、`web/` 等书籍线）
- 无关实验脚本：`tools/` 745 个中只取论文相关闭包；另**剔除 5 个书籍线脚本**（见 §3）
- 中间产物：`*.aux`/`*.log`/`*.pdf`/`build/`/`__pycache__/`（`__pycache__` 在提交前已清理）
- 个人配置：`.idea/`、`.vscode/`（未复制）

## 3. 复制后**剔除**的 6 个文件（Task G 一并处理）

| 文件 | 原因 |
|---|---|
| `Scripts/door_check.py` `gen_ch150_examples.py` `push_attempt.py` `repo_status.py` `run_ch150_examples.py` | 书籍线脚本，与论文无关，且含作者标识 |
| `tools/anonymity_check_670c2.py` | 该检查器**以作者真名作为匹配模式** ⇒ 自身即泄漏 |

## 4. 补拷（Task I 过程中按"修路径而不是放弃"补齐）

| 文件 | 触发原因 |
|---|---|
| `tools/audit_676k_dedup.py`、`run_a5_experiment_673p.py`、`selection_strategies_673p.py`、`evolution_operator_677c.py` | mypy `import-not-found`（被分析脚本 import） |
| `pyproject.toml` | 新仓库缺 lint 配置 ⇒ ruff 用默认规则集误报 356 项 |
| `data/692_environment_report.md`、`data/692_fair_comparison_report.md` | `verify_paper_numbers.py` 的 692 自洽组只读这两个报告（自洽组一度 33/35） |

## 5. 最终规模

| 项 | 值 |
|---|---|
| `git ls-files` | **389** 个文件 |
| 顶层结构 | `paper/` `data/` `tools/` `Scripts/` `docker/` `tests/` + `README.md` `REPRODUCTION.md` `CONTRIBUTING.md` `CITATION.cff` `LICENSE` `pyproject.toml` `.gitignore` |
| `.py` 文件 | 58 |

## 6. 诚实边界

- 复制是**文件级**的：没有做"只复制用到的函数"的抽取，`tools/utils/` 是整目录复制。
- `data/frozen_matrix/` 下的文件是**权威产物的副本**；工具通过新加的 fallback（`data/ → data/frozen_matrix/`，含 basename 回退）解析（见 `709_new_repo_validation_report.md`）。
- `docker/` 复制但**未实测构建**（源仓库同样未构建）。

## 7. 产物

- 新仓库 `C:\CodeLearnling\queyi-audit`（389 文件，initial commit `7442f54`）
- 本报告
