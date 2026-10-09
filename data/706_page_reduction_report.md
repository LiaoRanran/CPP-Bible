# 706 Task A — 减页报告（40 页 → 36 页）

- 日期：2026-10-09
- 论文：`research/latex/queyi_neurips2027_v1.1.tex`
- 目标：全稿 ≤36 页（NeurIPS E&D），且正文 ≤9 页、编译 0 错、0 未定义引用、**只移动不删除**。

## 结果

| 指标 | 减页前 | 减页后 |
|------|--------|--------|
| 全稿页数 | **40** | **36** ✅ |
| 正文页数（page:endmain） | 9 | 9 ✅ |
| 编译错误 | 0 | 0 ✅ |
| 未定义引用 | 0 | 0 ✅ |
| paper_quality_gate | — | **6/6 PASS** ✅ |

## 移出的 4 节（移动到 `supplementary/paper_appendix_extras.tex`，逐字不改）

| 标签 | 标题 | 原 tex 行（1-based，含节前注释横幅） | 行数 |
|------|------|--------------------------------------|------|
| `app:humanize` | Humanization Material (full versions; 673c) | 1505–1577 | 73 |
| `app:a5full` | A5 at Full Scale (676f): 1137 Samples | 1579–1756 | 178 |
| `app:bench676l` | Detector Depth Benchmark (676l) | 1843–1890 | 48 |
| `app:incidents` | Engineering Incident Log | 1937–1964 | 28 |

合计移出 **327 行**；tex 从 2369 行 → 2041 行（另有 1 行因跨行 `\ref` 合并而减少）。

## 移动顺序与页数变化

1. 移 `app:humanize` + `app:a5full` + `app:incidents` → 40 → **37 页**（仍超 1 页）。
2. 再移 `app:bench676l`（选择它因其**外部引用数 = 0**，最安全） → 37 → **36 页** ✅。
3. 在正文原位置补 3 处指针注释 `\paragraph{Moved to Supplementary Material.}` → 仍 **36 页** ✅。

## 引用完整性处理（关键：\ref 不能断）

被移出的 3 个顶层标签有 **5 处正文外部引用**（`app:bench676l` 无外部引用），已改写为文字引用，未断链：

| 位置（原行） | 原文 | 改为 |
|--------------|------|------|
| 274 | `(Appendix~\ref{app:humanize})` | `(Supplementary Material)` |
| 302 | `(Appendix~\ref{app:tables}, \ref{app:incidents})` | `(Appendix~\ref{app:tables}; Supplementary Material)` |
| 322 | `(Appendix~\ref{app:a5full})` | `(Supplementary Material)` |
| 425–426 | `(Appendices~\ref{app:a5full},\n\ref{app:reframe689})` | `(Appendix~\ref{app:reframe689} and Supplementary Material)` |
| 1879 | `Same lesson as Appendix~\ref{app:a5full}:` | `Same lesson as in the full-scale A5 record (Supplementary Material):` |

移动后正文/附录内**无未定义引用**（gate 检查：`undefined 条目 0`）。

## 内容零损失验证（红线：只用移动，不能删除）

用脚本 `verify_706.py` 从 `git HEAD` 重建“期望的减页后 tex”（= HEAD − 4 个移出区间 − 5 处引用改写），与工作树逐行 diff：

```
exp_lines=2042  work_lines=2042
DIFF lines: 0
extras contains humanize (73 lines): True
extras contains a5full   (178 lines): True
extras contains bench676l (48 lines): True
extras contains incidents (28 lines): True
ALL_BLOCKS_PRESENT= True
```

**DIFF = 0** ⇒ 除“移出 4 节 + 改写 5 处引用”外，**论文正文逐字未变，无任何误删**；4 节内容在 extras 中逐字完整保留。

> 过程备注（诚实）：第 2 个移动脚本因 Python `%` 格式符 bug 在**移除后、写 extras 前**报错，导致 `bench676l` 一度未写入 extras；已立即从 `git HEAD` 原文第 1843–1890 行**逐字恢复**并重验（上表 `bench676l: True`）。最终状态无损。

## 产物

- 修改：`research/latex/queyi_neurips2027_v1.1.tex`（−4 节，+3 处指针注释，5 处引用改写）
- 新增：`supplementary/paper_appendix_extras.tex`（345 行，含 4 节全文 + 头注释）
- 更新：`supplementary/README.md`（新增 extras 条目 + 706 更新说明 + 4 标签标注）
