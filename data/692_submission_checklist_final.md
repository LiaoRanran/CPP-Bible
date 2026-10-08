# 692-D · 预提交清单（final，权威版）

- 批次：692｜执行：CodeBuddy（AI）｜生成：2026-10-08
- **本文件取代** `research/latex/SUBMISSION_CHECKLIST.md` 作为**状态权威**：
  旧文件是 v1.0/673i 快照（仍引用 `queyi_neurips2027.tex` 无版本名、v0.7/v0.8 段落、
  `\TODO{670a}` 占位、46 条 bib、Croissant 未生成），**已过时**；旧文件保留为历史记录，不再更新。
- 三条状态：✅ 已核实清零 / ⚠️ 合法占位（论文内已声明，不算缺陷）/ ⬜ 仍开放（投稿前必须解决）

---

## 1. ✅ 已核实清零（本批实测，附命令）

| 检查项 | 状态 | 证据（本批实测） |
|---|---|---|
| 正文页数 ≤ 9 | ✅ | `paper_quality_gate_670c2.py`：`page:endmain -> 9 页` **OK** |
| 0 未定义引用 | ✅ | 同上：`undefined 条目 0` **OK** |
| `\ref` 全部有 `\label` | ✅ | 31 个 ref 全部有 label |
| `\section` 全部有 `\label` | ✅ | 8 个 section 均有 label |
| 摘要 ≤ 250 词 | ✅ | 229 词 |
| tex 正文 `TODO/FIXME/HACK` 残留 | ✅ | 逐字节检索：**字符串 "TODO" 在 `queyi_neurips2027_v1.1.tex` 中 0 次出现**（门禁输出"仅已登记占位"为允许项说明，实际占位数为 0） |
| 旧题名 "Evolving Verifiers" | ✅（正文/封面信） | 正文与 `cover_letter.tex` 均使用新题名；该字符串仅存在于**变更日志注释**（tex 第 23 行）与历史文档中 |
| 旧数字 `18/70` | ✅（正文） | 正文改为 **13/34**（681 归一化口径）；`18/70` 仅出现在 tex 第 37 行的变更日志注释里 |
| 匿名性 | ✅ | 匿名版 tex 中 `LiaoRanran` / `1026708211` 均 **0 次出现** |
| 总页数 | ✅ | 实测 PDF **35 页**（`pypdf`） |
| 论文门禁 | ✅ | `paper_quality_gate` **6/6 PASS** |
| 数字检查集 | ✅ | 130 条：0 missing / 116 consistent / 14 retired / 0 policy_violation（691 末态） |

## 2. 本批修复的**陈旧陈述**（发现即修，逐条登记）

| # | 位置 | 原文（陈旧） | 现文（准确） | 为何算缺陷 |
|---|---|---|---|---|
| F1 | `research/latex/response_template.tex` | "Croissant and Responsible-AI metadata are **registered pre-submission TODOs** …, **not yet shipped**" | "**generated and self-checked**（2026-conformant；生成物与其 13 项自检随 artifact 交付）" | Croissant/RAI 已在 **682** 生成并通过自检（`data/croissant.json` + `data/682_metadata_selfcheck.json` verdict=pass）；继续写 TODO 是**事实错误** |
| F2 | `research/response_template.md`（§On "reproducibility"，含"not yet shipped"那句） | 同上 | 同上 | 同上 |
| F3 | `research/response_template.md`（§统计/预注册段） | "…are registered pre-submission TODOs." | "…are generated and self-checked (13/13)" | 同上 |

**未修但已登记**（历史/参考文件，不动）：
- `research/rebuttal_prep.md`（v1）仍含 `18/70` 与旧叙事 —— 历史版本，662 起已由 v2/v3 取代；
- `research/rebuttal_prep_v2.md` 首行标题仍写 "Evolving Verifiers" —— v3（`data/692_rebuttal_v3.md`）§0 作覆盖声明；
  若投稿包内要保留 v2，建议把首行改为新题名（**本批未改，交由统一批次/作者决定**）；
- `research/latex/SUBMISSION_CHECKLIST.md` 全文件过时（见本文件头部）。

## 3. ⬜ 仍开放（投稿前必须解决；不得写成已完成）

| # | 项 | 性质 | 现状 | 阻塞谁 |
|---|---|---|---|---|
| O1 | **人类第二标注（IAA）** | 人工 | **0 执行**；材料包 145 条（41+64+40）+ 预注册阈值（verdict κ≥0.8）已备 | 唯一能改变 T1 定性的项；约半天工作量 |
| O2 | 作者通读（署名版语气/claim 边界复核） | 人工 | 未做 | 作者 |
| O3 | 2027 CFP 发布后模板迁移（`neurips_2027.sty`） | 外部依赖 | 未发布 | 官方 |
| O4 | 独立复现（外部方跑一次） | 人工/外部 | 未做 | 投稿前建议项 |
| O5 | ~~Croissant/RAI 元数据~~ | 工程 | **已在 682 完成**（本清单 §2 修复了残留的旧陈述） | — |
| O6 | 补充材料 zip（代码 + D2/D3/D4 数据 + README） | 工程 | 工作区内有 `preview_package_v2/`（**未纳入本批提交**，红线 8）；正式 supplement 包未生成 | 作者/打包批次 |
| O7 | `opentimestamps` bib 条目定位（协议 vs 论文） | 工程 | 未处置（遗留自 v1.0 清单） | 可选 |
| O8 | clang-cl / MSVC 环境实测、容器化复现 | 工程 | 未做（本机无 Docker/MSVC，687/692-A 已登记） | 可选（列入 future work 即可） |

## 4. ⚠️ 合法占位（**不是缺陷**，论文内已显式声明）

| 项 | 声明位置 | 说明 |
|---|---|---|
| `neurips_2025.sty` 模板 | cover letter §Template note + tex 头注释 | 2027 样式未发布，用官方 2025 样式作 placeholder（第三方文件未改）；页脚 notice 已覆盖为中性 "Under review" |
| OTS 零证明时间锚 | 论文 §Limitations / 威胁表 | 论文**主动**写明"zero-attestation placeholder"，未当作已完成能力 |
| A0–A4 消融未跑 | 论文（标 `not run`） | 689 起已把 TODO 宏改为明确 `not run`；不在正文宣称结果 |
| 环境受限项（Docker / MSVC / clang-cl） | 论文 Threats + README | 已声明为未实测缺口 |

## 5. 复算命令

```powershell
# 论文门禁（6/6）
python tools/paper_quality_gate_670c2.py
# 页数（实测，不信换算）
python -c "from pypdf import PdfReader; print(len(PdfReader('research/latex/queyi_neurips2027_v1.1.pdf').pages))"
# tex 正文 TODO 逐字节检索（应为 0）
python -c "print(open('research/latex/queyi_neurips2027_v1.1.tex',encoding='utf-8').read().count('TODO'))"
```
