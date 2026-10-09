# 709 Task I — 新仓库验证报告

- 日期：2026-10-09
- 仓库：`C:\CodeLearnling\queyi-audit`（匿名复现包，389 文件）

## 1. 数字校验 —— PASS（0 missing）

```bash
python tools/verify_paper_numbers.py \
  --tex paper/paper1/queyi_neurips2027_v1.1.tex \
  --tex-extra paper/paper1/supplementary/paper_appendix_extras.tex \
  --out-json data/paper1_numbers.json --out-md data/paper1_numbers_report.md
```
```
检察 124 条；missing 0；consistent 112
692 批次自洽：35/35 PASS
```

**过程中修了两处路径（任务书：修路径而不是放弃）**：
1. `tools/verify_paper_numbers.py::_p()` 增加 **fallback**：`data/<x>` 找不到时依次尝试
   `data/frozen_matrix/<相对路径>` 与 `data/frozen_matrix/<basename>`（本包把冻结产物集中在 `data/frozen_matrix/`）。
2. 补拷 `data/692_environment_report.md` / `data/692_fair_comparison_report.md`（692 自洽组原先 33/35 失败）。

## 2. 测试 —— PASS（7/7）

```bash
python -m pytest tests/ -q      # 7 passed
```
首跑 1 项失败（`test_p3_aggregation_rules_and_validation`，`DataMissingError`）——因为
`tools/utils/data_access.py::load_json_cached` 只认 `data/<name>`。**加了同一 fallback**（`data/frozen_matrix/<name>`）后 **7/7 通过**。

## 3. 两篇论文编译 —— PASS（0 error / 0 undefined）

| 论文 | 命令 | 结果 |
|---|---|---|
| Paper 1 | `cd paper/paper1 && tectonic queyi_neurips2027_v1.1.tex --keep-logs` | 0 error，**0 undefined**，正文 ≤9 页（706 已达成） |
| Paper 2 | `cd paper/paper2 && tectonic paper2_measurement_drift.tex --keep-logs` | 0 error，**0 undefined**，正文 **9 页**（709-D 压页） |

## 4. lint —— ruff PASS / mypy 有**预存**债务（如实记录）

```
ruff check tools/   → All checks passed!   (52 files)
mypy tools/         → 12 errors in 4 files (checked 53)
```

**mypy 的 12 个错误不是本批引入**：在**源仓库**对同样文件跑 mypy 得到**同样的错误**
（`analyze_682_sensitivity.py` ×3、`compute_703_zero_cost_validation.py` ×1，另有 `collect_realworld_683.py`、
`analyze_683_realworld.py`）。即它们是**源仓库既有的类型债**，与本包拆分无关。

处理：
- 属于"匿名化顺带"的一个 ruff 错误（`analyze_682_sensitivity.py:544` 未使用变量 `r2000`）已在**新仓库副本**中删除（行为中性）。
- **未**为了通过 mypy 去改动分析脚本的逻辑（那会改变可复现语义）；登记为**预存债务**，留待后续批次统一清偿。

## 5. 其他

- 新仓库 `git ls-files` = **389**；`__pycache__` 等构建产物提交前已清理（并由 `.gitignore` 排除）。
- 新仓库初始提交：`7442f54`，**1 个** commit，DCO `Signed-off-by: LiaoRanran <1026708211@qq.com>`（署名用于仓库 DCO，不出现在正文/产物）。
- `git grep` 泄漏扫描：**0 命中**。

## 6. 诚实边界

- `docker/` **未实测构建**（源仓库同样未构建）。
- mypy 未全绿（见 §4，预存债务）。
- `verify_paper_numbers` 仅在**传 `--tex-extra`** 时为 0 missing（因为 706/709 把部分内容移到了 supplementary；已于 706 说明该参数的设计）。
- 论文 1 的 `paper_quality_gate` 等 5 项门禁**未在新仓库跑**：它们硬编码到第一篇的 tex/版本，且本篇的红线只要求"编译 0 error + 数字 0 missing + 测试全过"（均已达成）。

## 7. 产物

- `data/paper1_numbers.json` / `data/paper1_numbers_report.md`（新仓库内）
- 本报告
