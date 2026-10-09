# 702 · Cover Letter 检查报告

> 受检文件：`research/latex/cover_letter.tex`（**只读，未修改**）
> 检查时间：2026-10-09｜方法：通读 + 字数脚本（`cover_wc.py`，剔除 LaTeX 命令/数学符）
> ⚠ **重要**：本文件在 702 批次执行期间被**并发的 703 批次**改写为 **v1.7（全重写）**
> （mtime 2026-10-09 10:35）。本报告基于 **v1.7 当前状态**，非会话之初的 v1.6。

---

## 1. 四项必查项

| 检查项 | 结果 | 说明 |
|---|---|---|
| **标题** | ✅ 一致 | 正文使用新题名 *"Caliber Drift and Capability Boundaries: An Audit Protocol for Software-Verification Evaluation"*，与 691/692 题名纪律一致。封面注释也明确"TITLE unchanged from the paper (v1.5/691)"。 |
| **贡献数** | ✅ 现为 **4** 条 | v1.7 将 v1.6 的 "Three contributions" 重构为 **"Four contributions"**（测量漂移代数 / 结构性被动 Goodhart / 能力边界地图 / 真实 CVE 验证）。**注意**：旧版是 3 条，新版是 4 条——若任何配套材料（README、rebuttal、摘要）仍写"three contributions"，需同步。 |
| **字数** | ✅ 461 词（≤500） | 叙述体（"To the NeurIPS" → "The Authors"）剔除命令/数学符后 **461 词**，满足 v1.7 注释声明的 "≤500 words"。 |
| **作者** | ✅ 双盲合规 | 署名 "The Authors"，无具名作者列表；与 E&D 通常双盲一致。 |

---

## 2. 一致性交叉核对（额外发现）

- **与 README §2 数字一致**：38.4% 盲区、13/34 类 >50%、60.07%→24.74%、+24.03pp、110 CVE @ 59.09% 均与根 README 五核心发现一致。✅
- **诚实声明齐备**：human IAA=0、公理系统 incomplete（A8 缺失）、22 个 OSS 项目未编译，均显式声明。✅
- **⚠ 残留旧题名风险**：根 `README.md` §6 的 BibTeX 仍用旧题名 *"Evolving Verifiers: Failure-Driven Portfolio Evolution for C++ Defect Detection"*（见 `702_readme_improvement_suggestions.md`）。封面/论文已改新题名，README 引用未同步——投稿前必须修。
- **⚠ "three contributions" 措辞残留**：搜索全仓 "Three contributions" / "three contributions" 可能在 rebuttal_prep、preview 包等旧文档出现，需逐一确认已改为 4 条（见 `702_pre_submission_checklist.md`）。

---

## 3. 结论

Cover letter v1.7 在**标题 / 贡献数 / 字数 / 作者 / 数字一致性 / 诚实声明**六项均**通过**。
唯一需在投稿前处理的是**跨文档旧题名与"三条贡献"措辞的残留**（属仓库级一致性，非本文件问题）。

> 本检查未改动 `cover_letter.tex` 任何字节（红线）。
