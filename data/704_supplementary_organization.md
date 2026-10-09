# 704-A · 补充材料包整理 · 执行报告

**批次**：704（大杂活批次） · **任务**：A — 补充材料包整理
**仓库**：`C:/CodeLearnling/note/note/C++/CPP-Bible`
**红线遵守**：未改 `research/latex/queyi_neurips2027_v1.1.tex`、未改 `queyi_refs.bib`、未 push、未跑新 `detect()`、未改检测器/样本/冻结矩阵；产出仅写入 `supplementary/` 与 `data/704_*`。

## 1. 做了什么

1. 创建 `supplementary/` 目录（此前不存在）。
2. 从论文 tex（`\appendix` 起始于第 665 行，附录正文约 1705 行）中提取全部 **35 个 `app:*` 附录标签**，按主题分为 **理论 / 实验 / 数据 / 工程** 四组，写入 `supplementary/README.md`。
3. 汇总 676f–703 批次报告与冻结 JSON 的关键数字，做成 `supplementary/all_numbers.md`，每个数字标注「来源批次 + 文件 + 复算状态」。
4. 自动提取 `tools/` 下全部 **745 个 `.py`** 脚本的模块 docstring 首行，生成 `supplementary/scripts_index.md`；其中 A 节为「复现关键脚本」表（输入/输出/怎么跑），B 节为完整索引。

## 2. 产出文件

| 文件 | 行数 | 说明 |
|---|---|---|
| `supplementary/README.md` | — | 包说明 + 附录 35 标签四组分类 + 文件索引 + 诚实边界 |
| `supplementary/all_numbers.md` | — | 关键数字总表（A–F 六节，标注来源批次/文件/复算状态） |
| `supplementary/scripts_index.md` | 776 | A 节复现关键脚本 + B 节 745 脚本完整 docstring 索引 |
| `data/704_supplementary_organization.md` | 本文件 | 本执行报告 |

## 3. 关键数字抽样复算（详见 704-D）

本任务 A 的数字表与 704-D 联动：+24.03pp、38.4%、59.09%、60.07%→24.74%、κ=0.727 均已在 704-D 用冻结产物实际复算并通过。

## 4. 偏差与诚实声明

- **`scripts/minimal_repro.sh` 的落点**：704 红线 6 规定「所有产出只写 `data/704_*` / `supplementary/` / `docker/`」。原 prompt 任务 B 写 `scripts/minimal_repro.sh`，但 `scripts/` 不在红线允许目录内，且本仓库既有复现脚本目录为 `Scripts/`（大写 S，存在 `reproduce_all.sh` / `verify_environment.sh`）。为遵守红线 6，最小复现脚本改为落在 **`docker/minimal_repro.sh`**（见 704-B）。若作者坚持放 `scripts/`，需先放宽红线 6。
- **`676l` 旧口径**：`all_numbers.md` C 节明确标注 94.21% 基于旧冻结矩阵（674/473），当前矩阵为 640/507，引用以 704-D 当前口径为准。
- 附录标题由脚本从 tex 自动抽取（去 LaTeX 命令后的人读标题），未逐字核对每个标题的语义准确性；如需精确标题以 tex 原文为准。

## 5. 验收对照（704 验收标准 #1）

| 标准 | 状态 |
|---|---|
| supplementary/ 目录完整，有 README + 所有声明文件 | ✅ README 完成；声明文件见 704-C |
| 复现指南完整，有最小复现脚本 | ✅ 见 704-B |
| 5 份投稿声明全部写好 | ✅ 见 704-C |
| 数字审计清单完整，10 个关键数字抽样复算 | ✅ 见 704-D |
| 不修改论文正文 / bib | ✅ 遵守 |
| DCO 提交 3–4 个，只含本批文件，未 push | 见 704-E |
| 验收报告覆盖全部 5 个任务 | ✅ 见 704-E |
