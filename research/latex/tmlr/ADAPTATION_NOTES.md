# TMLR 适配说明（678 批次 · C2）

> 本目录是 Queyi 论文向 **TMLR（Transactions on Machine Learning Research）** 投稿的**备选（backup）材料包**。
> 与 NeurIPS E&D 主线并行准备；在 E&D 被拒或用户选择期刊轨道时启用。

## 1. TMLR 政策要点（来源：jmlr.org/tmlr 主页 + author-guide.html，2026 抓取）

| 项 | TMLR 政策 | 对 Queyi 的影响 |
|----|-----------|----------------|
| 评审方式 | **双盲（double-blind）**，强制匿名化；补充材料也须匿名 | 当前 v1.3 已按 NeurIPS 双盲匿名化，可复用；但需清除 `data/`/`research/` 等内部路径泄露（见下） |
| 稿件长度 | **无硬页数限制**（"any length"），但正文（不含附录）异常长会拖慢审稿；鼓励会议式短篇 | 建议正文 9–12 页；当前 v1.1 正文 8 页 + 参考文献起第 9 页，符合 |
| 模板 | **必须使用 TMLR LaTeX 样式文件**（PDF 由其生成） | 需从 TMLR 作者指南/OpenReview 获取 `tmlr.sty`（第三方文件，**不纳入本仓、不修改**）；本包只给适配层与增量段 |
| 评审周期 | 官方强调 "shortened review period / fast turnarounds / rolling submission"，**未给具体月数** | 通常快于传统期刊；滚动投稿，随时可投 |
| 代码/数据 | 补充材料 ≤**100MB**（PDF 或 ZIP），**匿名**，**鼓励但非强制**；审稿人酌情查看 | 提供匿名快照（见数据可用性声明） |
| 复现清单 | 指南页**无强制 checklist**，但鼓励上传代码/数据提升可复现性 | 本包附 `reproducibility_checklist.md`（标准 ML 复现项 + Queyi 专属项） |
| 预印本 | 允许随时投 arXiv（匿名或具名），但 **TMLR 投稿本身不得链接到含作者姓名的版本** | arXiv v1.3 已匿名上传；TMLR PDF 内不回链具名 arXiv |

## 2. 生成 TMLR 版 tex 的机械步骤（待用户/工程批次执行）

1. 从 TMLR 作者指南下载 `tmlr.sty` 与 `tmlr.bst`（或样例 `tmlr_sample.tex`），放入 `research/latex/tmlr/`。
2. 以 `queyi_neurips2027_v1.1.tex`（version of record）为内容源，新建 `queyi_tmlr.tex`：
   - 头部：`\documentclass[anonymous]{tmlr}`（替换 `\documentclass{article}` + `\usepackage{neurips_2025}`）；
   - 删除 NeurIPS 专属宏/页脚占位（"Submitted to 39th Conference…" 伪影随样式自动消失）；
   - 保留全部正文、图表、附录内容（逐字节沿用 v1.1，不改科学结论）。
3. 在正文末、附录前插入两段（见本目录增量 `.tex`）：
   - `reproducibility_checklist.tex`（复现清单）
   - `data_availability_statement.tex`（数据可用性声明）
4. 匿名化复核：跑 `tools/anonymity_check_670c2.py` 须 0 命中（当前 v1.1 主文有 2 处 `data/`/`research/` MAIN 命中待清，见 678 验收报告 §A3）。
5. 编译验证：`tectonic queyi_tmlr.tex`（需 `tmlr.sty` 在场；CI 不在本仓跑论文编译，本地验证即可）。

## 3. 红线

- 不修改 `neurips_2025.sty`（第三方，禁止修改）——TMLR 版改用 `tmlr.sty`，两份样式文件并存、互不改写。
- 不改动实验数字与结论（仅换样式 + 增量声明段）。
- 双盲：TMLR 投稿 PDF 不得出现作者姓名、机构、`CPP-Bible` 仓库名、内部绝对路径。
