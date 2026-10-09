# 709 Task E — 第二篇论文编辑性待补报告

- 日期：2026-10-09
- 对象：`research/latex/paper2_measurement_drift.tex` + `research/latex/paper2_refs.bib`
- 对应 708 报告的 V2 / V3 / V4 三项编辑性待补。

## 1. PDF 元数据去标识（V2）✅

**改动**（`paper2_measurement_drift.tex`）：
- `\author{Anonymous Author(s)\\Affiliation\\Address\\\texttt{email}}` → **`\author{Anonymous}`**（去掉假机构/地址/邮箱占位）。
- hyperref 之后新增显式文档信息字典：
  ```latex
  \hypersetup{pdfauthor={Anonymous}, pdftitle={The Boundary of Evaluator Auditing: ...},
              pdfsubject={}, pdfkeywords={}, pdfcreator={}, pdfproducer={}}
  ```
- 同时更新文件头「Page discipline」注释以反映 709 的表格/小节移动。

**验证**（重编译后读 PDF 元数据）：
```
META = {'/Title': 'The Boundary of Evaluator Auditing: Identifiability, Correctability and Sample Complexity of Measurement Drift',
        '/Author': 'Anonymous', '/Producer': 'xdvipdfmx (0.1)', '/CreationDate': 'D:202609...'}
```
- **`/Author = Anonymous`**；无 `/Subject`、`/Keywords`、`/Creator` 泄漏；
- `/Producer` 为引擎名（`xdvipdfmx`），**不含作者/路径/机构**；
- ⇒ 元数据去标识 **达成**。

> 注：tectonic/XeTeX 走 xdvipdfmx，`\pdfinfo`（pdflatex 原语）不可用；故用 `\hypersetup` 写 PDF 信息字典，效果等价且可验证。

## 2. 付费墙文献核验（V3）✅（如实标注，不换文献）

对象条目：`lv2026whoevaluates`（*Who Evaluates the Evaluators? A Study on Reflexive Meta-Evaluation Methods for LLMs*, IEEE ICSIPC 2026）。

- 708 已标注 `verified-search only (paywall); RE-VERIFY before camera-ready`；
- **709 重新核验**：该文**已出版且有 DOI**（`10.1109/ICSIPC69751.2026.11583935`）⇒ 属已发表，**不能**标 "to appear"；
- 因此**不换文献**（换成可访问的替代会削弱相关工作覆盖），而是把 bib note 升级为**更精确的核验状态**：
  ```bibtex
  note = {metadata verified via search + publisher DOI; full text paywalled at verification time
          (709 re-check: attempted, not retrieved). Cite the published version; RE-VERIFY before camera-ready}
  ```
- 论文附录 E 已有一句登记（"One entry (lv2026whoevaluates) was seen only behind a paywall and is likewise flagged"）⇒ 一致。

> **诚实边界**：本批**没有**取得该文全文（付费墙），只核验了元数据（作者/标题/会议/DOI）。**"能引用" ≠ "已读全文"**；若审稿人要求，需要可获得全文的机构访问。

## 3. 与第一篇的重叠声明（V4）✅

在 §2 Related Work 末尾（"Relation to our first paper" 段之后）**新增一段**：

> **Overlap with the companion submission.** This paper builds on the experimental framework introduced in
> our companion submission [queyi2027caliber], but focuses on theoretical boundaries rather than empirical
> findings. No experimental results are duplicated: the transition counts, the T1/T5/T6 diagnostics and the
> sample-complexity requirements reported here are recomputed from the same frozen matrices and are either
> new to this paper or reported in a different role. The companion submission is under review; we cite it
> anonymously and claim no priority over it.

- 引用第一篇为 **companion submission（匿名）**——沿用 `\citep{queyi2027caliber}`（该 bib 条目本身即匿名/投稿中口径）；
- 明确 **"No experimental results are duplicated"**（任务书要求的口径）。

## 4. 编译与页数回归确认

```
UNDEF = 0 ; 正文 = 9 页（Conclusion p9 / References p10）；总 23 页；0 error
```

## 5. 诚实边界

- Task E 的三项**都已完成**；但 V5（拆附录为单独 supplementary，视 venue）与 V6（通俗摘要，部分 venue 要求）**本批未做**（708 已标注"视 venue"）。
- 重叠声明的措辞是**事实性声明**（数字按不同角色重算）——其"不重复"的判断依据是 708 §3 的客观 n-gram 检查（≥14 词连续散文复用 = 0）。
- 元数据去标识**只针对第二篇**；第一篇的匿名化检查见 706 Task D（0 泄漏）。

## 6. 产物

- 修改：`research/latex/paper2_measurement_drift.tex`（作者/元数据/重叠声明/头注释）
- 修改：`research/latex/paper2_refs.bib`（`lv2026whoevaluates` note）
- 本报告
