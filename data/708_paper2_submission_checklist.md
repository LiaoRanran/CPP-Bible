# 708-D · 第二篇论文投稿清单

- **批次**：708 ｜ **任务**：D ｜ **日期**：2026-10-09
- **论文**：*The Boundary of Evaluator Auditing: Identifiability, Correctability and Sample Complexity of Measurement Drift*
- **目标 venue**：**TMLR**（rolling、无页数上限）或 **NeurIPS 2027 Evaluations & Datasets（E&D）**
- **性质**：**草稿状态**的投稿清单。清单区分「**已具备**」「**待补**」「**本批不做**」三态，
  未完成的项**不假装完成**（对应任务书"诚实边界"）。

---

## 1. 状态总览

| 类别 | 项数 | 已具备 | 待补 | 本批不做 |
|---|---:|---:|---:|---:|
| A 稿件文件 | 4 | 4 | 0 | 0 |
| B 编译与质量 | 6 | 5 | 1 | 0 |
| C 匿名与合规 | 5 | 4 | 1 | 0 |
| D 数据与复现 | 5 | 3 | 1 | 1 |
| E 投稿系统材料 | 6 | 4 | 1 | 1 |
| F 编辑性风险 | 5 | 0 | 5 | 0 |
| **合计** | **31** | **20** | **9** | **2** |

> **一句话成熟度**：**草稿完成，可投 TMLR 的 rolling 通道（需先做 §F 的 5 项编辑性修补）；
> 不可直接投 NeurIPS E&D（正文超页 4 页，需执行压缩清单 P1–P6）。**

---

## 2. A · 稿件文件

| # | 材料 | 路径 | 状态 |
|:--:|---|---|:--:|
| A1 | 论文正文（匿名版） | `research/latex/paper2_measurement_drift.tex` | ✅ 已具备 |
| A2 | 参考文献 | `research/latex/paper2_refs.bib`（66 条，全部被引用） | ✅ 已具备 |
| A3 | 投稿信（≤500 词，实测 **499 词**） | `research/latex/paper2_cover_letter.tex` | ✅ 已具备 |
| A4 | 独立摘要（供投稿系统单独提交，**235 词**，与正文逐字一致） | `research/latex/paper2_abstract.tex` | ✅ 已具备 |
| A5 | 编译产物 PDF | `research/latex/paper2_measurement_drift.pdf`（22 页） | ✅ 已具备（**不入版本库**，`.gitignore:12 *.pdf`） |

---

## 3. B · 编译与质量

| # | 检查 | 结果 | 状态 |
|:--:|---|---|:--:|
| B1 | 编译 0 error | ✅ tectonic 0.17.0 | ✅ |
| B2 | 0 undefined references | ✅ 日志中 `undefined` 计数 = 0 | ✅ |
| B3 | 0 undefined citations | ✅ 同上 | ✅ |
| B4 | 引用完整性 | ✅ 66 引用键 = 66 bib 条目（0 未引用 / 0 缺失） | ✅ |
| B5 | Overfull hbox | ⚠ 1 处，1.51 pt（附录 D 的 `verbatim` 注释行） | ✅ 可接受 |
| B6 | **正文页数 ≤ 8–9** | ❌ 实测 **≈13 页**（超 4 页） | ❌ **待补**（见 §F） |

---

## 4. C · 匿名与合规

| # | 项 | 状态 | 说明 |
|:--:|---|:--:|---|
| C1 | 正文无作者名/单位/邮箱 | ✅ | 作者块为 `Anonymous Author(s)`；`paper2_abstract.tex` 同样匿名 |
| C2 | 无自引暴露身份 | ✅ | 第一篇以 `\citep{queyi2027caliber}` 匿名引用（bib 条目 `author = {{Anonymous}}`） |
| C3 | 无致谢/基金/数据出处暴露 | ✅ | 全文无致谢节；无机构名 |
| C4 | 中性 notice 字符串 | ✅ | 覆盖 `neurips_2025.sty` 默认串为 `Under review (anonymized). Do not distribute.` |
| C5 | **PDF 元数据去标识** | ❌ **待补** | 未检查 PDF 的 `Author`/`Producer` 字段；相机就绪前必须清空（属投稿批次） |

---

## 5. D · 数据与复现

| # | 项 | 状态 | 说明 |
|:--:|---|:--:|---|
| D1 | 每个数字一行复算命令 | ✅ | 附录 D + `data/708_paper2_number_audit.md`（78 行取数表） |
| D2 | 数字全部来自既有批次 | ✅ | 78/78 可溯源；0 编造；0 "待补" |
| D3 | 未跑新 `detect()` | ✅ | 本批 `detect_calls = 0` |
| D4 | **代码/数据可用性声明** | ❌ **待补** | 第二篇未含 Data/Code Availability 节；第一篇有（`research/latex/tmlr/data_availability_statement.tex`）⇒ 复用并改写 |
| D5 | 冻结矩阵再发布 | ⛔ **本批不做** | 需脱敏与体积评估（第一篇已有相应流程）；本批红线禁止改冻结矩阵 |

---

## 6. E · 投稿系统材料

| # | 材料 | 状态 | 说明 |
|:--:|---|:--:|---|
| E1 | Cover Letter | ✅ | `paper2_cover_letter.tex`（499 词 ≤ 500） |
| E2 | Abstract（纯文本可粘贴） | ✅ | `paper2_abstract.tex`（235 词） |
| E3 | 关键词 | ✅ | 见本文件 §7（6 个） |
| E4 | 推荐审稿人 / 回避名单 | ⛔ **本批不做** | 需与第一篇统一口径，属投稿批次 |
| E5 | **与第一篇的关系说明** | ❌ **待补** | 投稿系统常问"是否与在投论文重叠"⇒ 需一段 ≤120 词的声明（草稿见 §8） |
| E6 | Supplementary / 附录上传方式 | ⚠ 待定 | 附录已内嵌在正文 PDF（A–E 节）；若 venue 要求单独 supplementary，需拆分 |

---

## 7. 关键词（6 个）

`evaluation methodology` · `measurement drift` · `Goodhart's law` ·
`identifiability` · `sample complexity` · `evaluator auditing`

---

## 8. 与第一篇的重叠声明（草稿，≤120 词，待补项 E5）

> This submission is the second of two papers by the same authors. The first paper is a case study
> that audits one C/C++ verification apparatus and reports five empirical findings. This paper is a
> theory paper: it asks what an audit can establish in principle, and proves three boundary results
> (identifiability, correctability, sample complexity). The two papers share a frozen dataset and a
> terminology; they share no headline numbers, and this paper restates none of the first paper's
> arguments. A text-level n-gram check finds no shared prose sequence of 14 or more consecutive words
> between the two manuscripts (see `data/708_paper2_compilation_report.md` §3).

---

## 9. F · 编辑性风险（**投稿前必须处理**）

| # | 风险 | 严重度 | 处理 |
|:--:|---|:--:|---|
| F1 | **正文超页 4 页**（NeurIPS E&D 会 desk-reject） | 🔴 | 执行 `data/708_paper2_compilation_report.md` §2.2 的压缩清单 P1–P6（预计省 ≈2.7 页）；若仍超，再把 §4 元理论整体移入附录 |
| F2 | 9 条 bib 条目的 `note` 标 `unverified-memory` / `paywall` 已被**移出 bib**，但正文引用的 `lv2026whoevaluates` 仍标 `verified-search only (paywall)` | 🟡 | 相机就绪前**必须**自行核验该条元数据（附录 E 已登记） |
| F3 | Type I 的 $\beta=2.02$ 是**模型蕴含值** | 🟡 | 论文已两处标注（§3.3 + 附录 C 表注）；投稿前再确认无别处把它当"发现" |
| F4 | 相变语言是**类比** | 🟡 | 论文已降级为"描述性框架"；确认摘要与 cover letter 未出现"phase transition"式主张（✅ 已确认：两处均无） |
| F5 | LLM 臂**无模型快照 id**、人类 IAA = 0 | 🟡 | 论文 §8.4 已写为 limitation；投稿前确认 venue 的 LLM 使用政策（是否要求披露 prompt/模型版本） |

---

## 10. 交付物清单（本批 D 任务）

| 文件 | 状态 |
|---|:--:|
| `research/latex/paper2_cover_letter.tex` | ✅ 新建 |
| `research/latex/paper2_abstract.tex` | ✅ 新建 |
| `data/708_paper2_submission_checklist.md` | ✅ 本文件 |

---

## 11. 诚实边界

1. **本清单不声称"已可投稿"**：§B6（页数）、§C5（PDF 元数据）、§D4（可用性声明）、
   §E5（重叠声明）、§F1–F5 共 **9 项待补 + 2 项本批不做**。
2. **Cover Letter 与 Abstract 均已编译通过**（cover letter 2 页、abstract 1 页），
   但**未**做与正文的数字二次核对（Cover Letter 的 4 个数字 `4096 / 30.0% / 849 / 17 / 55.84`
   已在 `708_paper2_number_audit.md` 的审计范围内，✅ 一致）。
3. **推荐审稿人与回避名单未准备**（E4）：这需要作者对同行的判断，不是可自动生成的项。
4. **本清单未覆盖**：投稿系统的字数硬限制（各 venue 不同）、图（本文 0 图）、
   以及 venue 特有的 LLM 使用披露表。

---

*文件生成：2026-10-09 ｜ 批次 708 任务 D ｜ `detect_calls` = 0 ｜ 未修改论文正文与 bib*
