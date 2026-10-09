# 706 Task 0 — Cover Letter 编译状态报告

- 批次：706（投稿前最后工程批次）
- 日期：2026-10-09
- 文件：`research/latex/cover_letter.tex`（v1.7）
- 引擎：Tectonic 0.17.0 (XeTeX)

## TL;DR（诚实结论）

**当前仓库状态下，Cover Letter 编译 0 error，无需修复。** 任务书假设的“CL 现在编译不过”在实测中**不成立**。我未对 `cover_letter.tex` 做任何内容改动（红线：只修报错，不重写）。

## 实测证据

1. **全新编译（先删 aux/out/log/pdf 强制从零）**：
   ```
   cd research/latex && tectonic cover_letter.tex --keep-logs --print
   → Output written on cover_letter.xdv (2 pages, 6396 bytes)
   ```
   无 error，仅 1 类 warning（`Overfull \hbox (6.16pt too wide)` 排版警告，非错误）。
2. **严格错误扫描**（`cover_letter.log`）：
   - `^!`（TeX 错误标记）：**0**
   - `LaTeX Error` / `Undefined control sequence` / `Runaway` / `Emergency stop`：**0**
   - 唯一 `Warning` 为 `inputenc package ignored with utf8 based engines`（XeTeX 下的无害提示）。
3. **git 状态**：`cover_letter.tex` 工作树**干净**（无未提交改动），当前即提交 `c7446d60`（703-A 全量重写）的版本。即：703-A 引入的 CL 本身就能编译。
4. **内容仍为 v1.7**：含四贡献段、新题名
   “Caliber Drift and Capability Boundaries: An Audit Protocol for Software-Verification Evaluation”。
5. **字数**：正文（“To the NeurIPS…” → “The Authors”）= **477 词 ≤ 500**（脚本 `cl_wordcount.py` 去除注释/命令后统计）。

## 对“报错”假设的排查

| 假设 | 排查 | 结论 |
|------|------|------|
| LaTeX 语法错误 | 全新编译 0 error | 否 |
| 引用错误（`\cite`/`\ref`） | CL 内**无任何** `\cite`/`\ref` | 否 |
| 包冲突 | 仅 `inputenc`/`fontenc`/`geometry`/`hyperref`/`parskip`，无冲突命令 | 否 |
| 中文字符混入 | 全文英文，无 CJK | 否 |
| CRLF 换行问题 | tectonic 正常处理 | 否 |
| 另一个 CL（arxiv 等） | `arxiv_submission/` 只有论文 tex；`build.ps1` 不编译 CL | 否 |

## 结论与建议

- 验收标准 #0（“CL 编译 0 error，字数 ≤500，内容仍是 v1.7”）**已满足**。
- **建议**：任务书所依据的“编译报错”可能来自 703 重写过程中的某个**中间态**（其后已被提交 `c7446d60` 覆盖），或来自非 tectonic 的另一种阅卷路径。若用户侧确实能在某环境复现错误，请提供该环境的**第一处 error 原文**，我据此定位；当前证据下**无可修之处**，强行“改动”反而违反“只修报错、不动内容”的红线。
- 未改动文件：`research/latex/cover_letter.tex`（保持 0 变更）。
