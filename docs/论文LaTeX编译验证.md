# 论文 LaTeX 编译验证记录（v1.0 定稿批次 · 任务 G）

> ## ✅ 673a 状态更新（2026-10-02）
> 已产出 **`research/latex/queyi_neurips2027_v1.0.tex`** 并**编译通过**：
> **正文 9 页**（含全部图表，符合 NeurIPS「9 content pages」）、**0 error**、**0 未定义引用**、摘要 247 词。
> 削减手段：合并两张矛盾的 ablation 表、删 `tab:data`、把 7 张表移入附录（label 不变）、正文表格降为 `\footnotesize`、压缩 §1/§3.4/§4/§7/§10。
> 原 §4.3 记录的 `paper_sync_check` 自身过期问题**已修复**（期望值更新到 672h 并 PASS）。

> **批次**：论文 v1.0 定稿 · 任务 G
> **对象**：`research/latex/queyi_neurips2027.tex`（+ `queyi_refs.bib`、`neurips_2025.sty`）
> **日期**：2026-10-01 夜间
> **纪律**：编译在**临时目录**进行（不污染仓库）；未修改任何工程代码。

---

## 0. 一句话结论

**编译成功、0 错误、0 未定义引用** —— 但 **🔴 正文 10 页（文本）+ 4 张表漂移到第 11–13 页，严重超出 NeurIPS 9 页限制**。这是投稿前**最硬的阻塞项**。

---

## 1. 工具链

| 项 | 状态 |
|---|---|
| 本机 `pdflatex` / `xelatex` / `lualatex` / `latexmk` / `tectonic` / MiKTeX | ❌ **全部未安装** |
| 常见安装目录（`/c/texlive`、MiKTeX） | ❌ 不存在 |
| `research/latex/build.ps1` | ⚠ 依赖 `tectonic`，本机无法直接运行 |
| **本批采取的方案** | ✅ 下载 **tectonic 0.15.0**（`x86_64-pc-windows-msvc`，19 MB）到临时目录，编译在 `%TEMP%/paperbuild` 完成 |

> **说明**：编译产物（`.pdf/.aux/.log`）**未写入仓库**，避免提交带有过期数字的 PDF。

## 2. 编译结果 —— ✅ 成功，0 错误

```
note: Writing `queyi_neurips2027.pdf` (160.53 KiB)
```

- **0 error**；仅有 overfull/underfull hbox（排版警告，非错误）。
- **`??` 未定义引用数 = 0**（`grep -c "??" queyi_neurips2027.log` → 0）。
- **未定义 citation / reference = 0**（log 中无 `undefined` 行）。
- 静态检查交叉验证：bib 49 条 = 文内引用 49 条，**0 孤儿、0 未定义**（与 `bib_audit_670c2.py` PASS 一致）。

### 2.1 警告（均为排版级，非阻塞）

| 类型 | 位置 | 说明 |
|---|---|---|
| Overfull hbox 31.16pt | L740–751（Table validity） | 表格略超版心宽 |
| Overfull hbox 16.32pt | L762–783（Table claim） | 同上 |
| Overfull hbox 71.96pt | L946–959（Appendix F 相关工作表） | 同上 |
| **Overfull hbox 500.26pt** | **L924（Appendix D `verbatim` 复现命令块）** | 🟠 复现命令块严重溢出页边（最大一行超 500pt）⇒ **建议改 `listings` 或手动断行** |
| Underfull hbox ×N | L747/766–778 等 | 表格列宽不足导致拉伸，观感问题 |
| `TeX rerun seems needed, but stopping at 6 passes` | 全局 | tectonic 多趟收敛提示；因 `?? = 0`，引用已解析，**无实质影响** |
| `internal consistency problem when checking if .bbl changed` | 全局 | tectonic 已知的 bbl 校验提示，**无实质影响** |

## 3. 🔴 页数 —— 严重超限

从 `.aux` 的 `\newlabel` 提取**实测页码**（权威）：

| 内容 | 页 |
|---|---|
| §1 Introduction | 1 |
| §2 Related Work | 2 |
| §3 Threat Model | 3 |
| §4 Method | 4 |
| §5 Evaluation Protocol | 6 |
| §6 Experiments | 7 |
| §7 Analysis | 8 |
| §8 Threats to Validity | 9 |
| §9 Claim Boundary | 9 |
| §10 Conclusion | 9 |
| `fig:evolution` / `tab:e3` | **10** |
| **`\label{page:endmain}`（正文结束标记）** | **10** |
| `tab:e4` / `tab:e5`（§6 的表） | **11** |
| `tab:validity`（§8 的表） | **12** |
| `tab:claim`（§9 的表） | **13** |
| 参考文献 | 14 |
| 附录 A（Rule Manifest） | 15 |
| 附录 B/C/D/E/F | 15–16 |
| **PDF 总页数** | **16** |

### 判定

| 口径 | 实测 | 限制 | 超出 |
|---|---|---|---|
| **正文文本**（`page:endmain`） | **10 页** | 9 页 | 🔴 **+1 页** |
| **正文 + 其浮动体**（末表 `tab:claim` 在第 13 页） | **13 页** | 9 页 | 🔴 **+4 页** |

> **结论**：无论按哪种口径，**都超出 9 页**。最严重的是 **4 张表（e4/e5/validity/claim）漂移到正文结束标记之后**——
> 这是「浮动体过多」的典型症状（主文 13 表 + 4 图），也是 `SUBMISSION_CHECKLIST.md` 第 2 节
> 那条 `[ ] VERIFY after compile` 待办的真实答案。

### 3.1 削减方案（按性价比排序）

| # | 措施 | 预计省 | 代价 |
|---|---|---|---|
| 1 | **合并 `tab:ablation` + `tab:e4`**（两张 ablation 表内容重复**且互相矛盾**，见任务 B 的 B9） | ~0.5–0.7 页 | 低（顺带修逻辑矛盾） |
| 2 | **删 `tab:data`**（五层数据集表，Fig.2 已完整承载） | ~0.4 页 | 低 |
| 3 | **`tab:samplesize` 移入补充材料** | ~0.3 页 | 低 |
| 4 | **`tab:validity` 由 5 行表改为紧凑段落**（或移附录） | ~0.4 页 | 中 |
| 5 | **§Analysis 6 点压缩为 4 点** | ~0.3 页 | 中（需保留 B6/B7 相关论述） |
| 6 | 修 `verbatim` 溢出（L924）后重排附录 D | 排版 | 低 |

> **建议**：措施 1+2+3 即可省 ~1.2–1.4 页，**大概率把正文拉回 9 页内**。
> **注意**：措施 1 必须在**修完 B9 矛盾之后**做（否则合并的是两张错表）。

## 4. 其他发现

### 4.1 仓库内 PDF 已过期
`research/latex/queyi_neurips2027.pdf` 的 mtime 为 **10-01 01:17**，而 `.tex` 为 **10-01 11:31** ⇒
**仓库里的 PDF 不反映当前 `.tex`**（更不反映 v0.9 数字）。投稿前须重新编译。

### 4.2 `paper_quality_gate_670c2.py` 跳过了页数检查
该门禁本批只读运行结果：
```
[SKIP] 主文页数≤9  缺 .aux（先运行 build）—— 跳过
[SKIP] 0 未定义引用  缺 .log —— 跳过
[OK ] 所有 \section 有 \label   10 个
[OK ] 所有 \ref 有 \label       15 个
[OK ] 摘要≤250词                摘要英文词数 = 249
[OK ] 无 TODO/FIXME/HACK 残留
[paper-gate] PASS
```
⇒ 门禁**跳过了页数与未定义引用**（因缺 `.aux`/`.log`）——本批已用 tectonic 补齐这两项，**结论见 §2/§3**。

### 4.3 🔴 `tools/paper_sync_check_670c2.py` **自身已过期**
该门禁本批只读运行结果 **FAIL**：
```
[BAD] McNemar FD vs Random† corpus  tokens=[['1.2×10⁻⁷']...]   - 缺失于 md
[BAD] 效应量 h random† corpus        tokens=[['1.24']]           - 缺失于 md
[paper-sync] FAIL
```
**根因**：该工具把 **`1.2×10⁻⁷`** 与 **`h=1.24`** 当作**期望值**，
而这两个值正是 **672f 已明确标记「错误并已修复」的旧值**（见 `reveal_update_672f.json::discrepancy_found_and_fixed`）。
⇒ **`paper_v0.9.md` 是对的，工具是错的**。

**给建设线的交接**（论文线不碰 `tools/`）：
> `tools/paper_sync_check_670c2.py` 的期望 token 需从
> `McNemar FD vs Random corpus = 1.2×10⁻⁷` → **`7.6×10⁻⁶`**、
> `h random corpus = 1.24` → **`0.81`**；
> 并同步 `Random† corpus` 的率值 `4.2%` → **`16.7%`**。
> 否则该门禁会**永远 FAIL 在正确的论文上**。

### 4.4 其余门禁（本批只读运行，全 PASS）
| 工具 | 结果 |
|---|---|
| `bib_audit_670c2.py` | ✅ **PASS**（entries=49, cite_keys=49, errors=0, warnings=0） |
| `figure_data_check_670c2.py` | ✅ **PASS**（坐标块 4，通过 8，失败 0） |
| `anonymity_check_670c2.py` | ✅ **PASS**（STRICT 命中 0，MAIN 命中 0） |
| `paper_quality_gate_670c2.py` | ✅ PASS（2 项 SKIP，见 §4.2） |

## 5. 需转 LaTeX 的工作量

**无**——LaTeX 源码已完整存在（962 行，含 4 图 16 表）。**不需要从 Markdown 转 LaTeX**。
本批工作量为：**（a）数字重同步**（任务 A）、**（b）逻辑修补**（任务 B）、**（c）削减页数**（§3.1）。

## 6. 验收对照（任务 G）

- [x] 有 LaTeX 源码 → 已编译验证
- [x] 编译无错误 ✅（0 error）
- [x] 检查无未定义引用 ✅（`??` = 0）
- [x] 检查页数 ✅ → **正文 10 页，超 9 页限制 1 页** 🔴
- [x] 检查字数 ✅（正文散文 3,403 词；摘要 249 词）
- [x] 记录需转 LaTeX 的工作量 → **无**
- [x] 不碰工程代码（编译在临时目录；仅只读运行门禁工具）

---

*本记录仅写 `docs/`；编译产物留在系统临时目录，未写入仓库。*
