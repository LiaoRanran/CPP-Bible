# 670f 批次验收报告

- **批次**：670f（paper_v0.7.md → NeurIPS E&D LaTeX 投稿格式 + 完整投稿准备包）
- **分支**：master　**日期**：2026-09-30　**执行者**：LiaoRanran（DCO）
- **性质**：在 670a/670c 并行期间独立完成；**只在 `research/latex/` 下工作**。
- **来源**：`research/paper_v0.7.md`（670e）。**所有数字与 v0.7 一致，未编造。**

---

## 0. 一句话

> LaTeX 投稿包完成并**真实编译通过**：主文 **7 页（≤9）**、**0 处未定义引用**、**48 条参考文献**全部渲染、**4 张图**（TikZ/pgfplots）全部插入、**匿名化 0 残留**。环境无 TeX 发行版，故自备**自包含引擎 tectonic** 完成编译（其内部执行 BibTeX 通过）。

---

## 1. 交付物（`research/latex/`）

| 文件 | 说明 |
|---|---|
| `queyi_neurips2027.tex` | 主文（§1–§10）+ 附录 A–F；NeurIPS D&B 匿名格式 |
| `queyi_neurips2027.pdf` | 编译产物（13 页 = 主文 7 + 参考文献 + 附录） |
| `queyi_refs.bib` | 48 条 BibTeX 条目（46 逻辑引用；21/32 各拆为两条） |
| `neurips_2025.sty` | **官方** NeurIPS 2025 样式（2026 未发布，见 §7 诚实登记） |
| `cover_letter.tex` / `.pdf` | 英文投稿信，主动声明 baseline 缺口 + 可复现性 |
| `response_template.tex` / `.pdf` | 回复审稿人模板（分点 + 行号） |
| `SUBMISSION_CHECKLIST.md` | 对照 E&D 投稿要求逐项检查 |

---

## 2. 任务 A · LaTeX 排版

- **A1 模板**：`\documentclass{article}` + `\usepackage[dandb]{neurips_2025}`（Datasets & Benchmarks 轨，**默认匿名**）。样式文件为**官方下载**（`media.neurips.cc/Conferences/NeurIPS2025/Styles.zip`）。
- **A2 内容迁移**：§1–§10 + 附录 A–F 全部迁移（见 §6）。
- **A3 四张图**（全部 TikZ/pgfplots，无外部图片依赖）：
  - **Fig.1 系统闭环**：TikZ 流程图，含**失败驱动反馈箭头** + 口径修正旁路（`\ref{fig:loop}`）
  - **Fig.2 数据集分层**：TikZ 分层，红/黄/绿=能否 Claim 外部效度（`\ref{fig:data}`）
  - **Fig.3 核心结果**：pgfplots 柱状图，FD 真实值 87.5/35.0/100；baseline 列标 `\TODO{670a}`（`\ref{fig:core}`）
  - **Fig.4 演化曲线**：pgfplots 折线，660→669，标注口径变更（`\ref{fig:evolution}`）
- **A4 表格**：全部 `booktabs`；四态判决表、D0–D4 分层表、67 规则统计（在附录 A）、Claim 边界表、T1–T12 表、ablation 表、baseline 表。
- **A5 参考文献**：`queyi_refs.bib`，48 条，标题/作者/年份/venue 与 `research/670b_引用核验_终稿.md` 一致；**[API核验]/[已核] 标注未进 bib**（只保留真实引用信息）。

---

## 3. 任务 B · 投稿准备

- **B1 匿名化**：
  - 身份信息（用户名/邮箱/仓库 URL/本地绝对路径/机构名）：**0 命中**。
  - 主文（`\appendix` 之前）仓库路径：**0 命中**。
  - 附录 D 保留复现命令（相对 artifact 根）——按任务 B1「附录可保留仓库链接」。
- **B2 页数**：主文 **7 页 ≤ 9**（依据：`\label{page:endmain}` 落在**第 7 页**，见 §5 编译日志）。
- **B3 cover letter**：英文版，含「baseline experiments are in progress and will be included in the camera-ready」+ 可复现性声明。
- **B4 附录 A–F**：A 67 规则清单 / B 统计口径（CP/Wilson/Fisher/McNemar 公式）/ C 逐样本明细 / D 复现命令 / E AI 使用声明 / F 相关工作详表（七方向）。
- **B5 编译验证**：见 §5。

---

## 4. 任务 C · 辅助文件

- **C1** `response_template.tex`：标准分点回复 + 行号引用 + 「Summary of changes」。
- **C2** `SUBMISSION_CHECKLIST.md`：8 组逐项（格式/页数/参考文献/图表/内容/补充材料/诚信/可复现）。

---

## 5. 编译验证（实测）

**环境约束**：本机**无 TeX 发行版**（`pdflatex`/`bibtex`/`latexmk`/`tectonic` 均不存在）。
**处置**：下载**自包含引擎 tectonic 0.15.0**（GitHub 官方 release），其内置 BibTeX 通过。

```text
$ tectonic queyi_neurips2027.tex
note: Writing `queyi_neurips2027.pdf` (127.51 KiB)
```

| 检查项 | 结果 |
|---|---|
| 编译 | ✅ 成功（生成 PDF，126 KiB） |
| 总页数 | 13 页（主文 7 + 参考文献 + 附录 A–F） |
| **主文页数** | **7 页 ≤ 9** ✅（`\newlabel{page:endmain}{{10}{7}...}` → 第 7 页） |
| 未定义引用/文献 | **0**（log 无 `undefined` / `Citation ... undefined`） |
| 参考文献渲染 | **48 条** `\bibitem` |
| `??` 检查 | **0** |
| 警告 | 仅 1 条无害（`inputenc ignored with utf8 engines`）+ 14 处 Overfull hbox（排版微溢出，非错误） |
| 辅助文件 | `cover_letter.pdf`、`response_template.pdf` 均编译成功 |

> **经典命令**（有 TeX Live/MiKTeX 时）：`pdflatex → bibtex → pdflatex → pdflatex`，见 `SUBMISSION_CHECKLIST.md`。

---

## 6. 内容与数字一致性

- 主文 §1–§10 + 附录 A–F 与 `paper_v0.7.md` **逐章对应**。
- 关键数字**全部沿用 v0.7**：67 规则（block 44 / warn 16 / advice 7）、42 实卡、452 账本、5 Merkle 目录、holdout 87.5%（14/16）[61.7, 98.4]、external 35.0%（14/40）[20.6, 51.7]、可测 43.8%（14/32）[26.4, 62.3]、FPR 11.1%（1/9）、变异 core 97.3%（110/113）/ all 81.5%（128/157）、反事实 F1=1.0（分母 10）、口径消融 Δ(A−C)=+8.8pp、演化 656/660/665/666/668/669。
- **未落盘处**一律 `\TODO{670a}`（红字渲染），未填估计值。

---

## 7. 诚实登记

1. **样式版本**：NeurIPS **2026** 官方样式**尚未发布**（`Conferences/NeurIPS2026/Styles.zip` → 404），故使用**最新的官方 2025 版** `neurips_2025.sty`。2027 CFP/模板发布后**须替换**（checklist 已列 TODO）。
2. **语言**：NeurIPS 为英文投稿，故主文为 v0.7 的**英文迁移**（结构/数字/表格逐项对应，非新增内容）。
3. **编译引擎**：用 **tectonic**（自包含）而非 pdflatex+bibtex——因本机无 TeX 发行版；tectonic 内部完成 BibTeX 通过。经典命令已在 checklist 给出。
4. **48 vs 46 条目**：46 条逻辑引用中有 2 条（Strathern+Goodhart、Cohen+Krippendorff）各含两个工作，故拆为 4 条 → 共 48 条 bib 条目，**全部渲染**。
5. **14 处 Overfull hbox**：宽表微溢出，不影响编译与页数；投稿前可微调列宽。
6. **baseline 仍缺**：Fig.3/E1 的 baseline 列为 `\TODO{670a}`，属**有意保留**（不编造）。

---

## 8. 收工

| 检查 | 结果 |
|---|---|
| `research/latex/` 完整 | ✅ 9 文件（3 PDF） |
| pdflatex/tectonic 编译通过 | ✅ |
| 主文 ≤9 页 | ✅ 7 页 |
| 无 `??` 引用 | ✅ |
| 4 张图 | ✅ TikZ/pgfplots |
| 46（→48）条 bib 全录入 | ✅ |
| 匿名化 0 残留 | ✅ |
| 附录 A–F | ✅ |
| cover letter / response / checklist | ✅ |
| 未碰 670a/670c 与受控目录 | ✅ |
| 提交 | `git commit -s`（DCO），**不 push** |
