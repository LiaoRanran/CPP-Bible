# 703-G · 最终编译与验证

- **批次**：703 ｜ **任务**：G ｜ **日期**：2026-10-09
- **被验文件**：`research/latex/queyi_neurips2027_v1.1.tex`（论文）、`research/latex/cover_letter.tex`（投稿信）
- **红线**：未 push；未跑 `detect()`；未改检测器/样本/冻结矩阵。

---

## 0. 结果总表

| # | 检查项 | 目标 | 实测 | 判定 |
|:--:|---|---|---|---|
| 1 | tectonic 编译（论文） | 0 错 | `^!` 行 **0**；undefined ref/citation **0** | ✅ |
| 2 | tectonic 编译（cover letter） | 0 错 | 0 错（1 条 Overfull hbox 警告） | ✅ |
| 3 | 正文页数 | ≤ 9 | **9**（`\label{page:endmain}` → 9 页） | ✅ |
| 4 | 全稿页数 | ≤ 36 | **40** | ❌ **超标（见 §2）** |
| 5 | 摘要词数 | ≤ 250 | **229** | ✅ |
| 6 | paper_gate | 6/6 | **6/6 PASS** | ✅ |
| 7 | 匿名化 | 0 泄漏 | STRICT **0** / MAIN **0** | ✅ |
| 8 | verify_paper_numbers | 0 missing | 128 条检察，**missing 0**，consistent 102 | ✅ |
| 9 | fast_gate | PASS | **PASS**（658 / 669d / 671a 三门禁全过） | ✅ |
| 10 | cover letter 叙述体词数 | ≤ 500 | **495** | ✅ |

---

## 1. 逐项证据

### 1.1 编译（论文）

```
$ cd research/latex && tectonic --keep-logs --keep-intermediates queyi_neurips2027_v1.1.tex
$ grep -c "^!" queyi_neurips2027_v1.1.log
0
$ grep -icE "undefined (control sequence|reference|citation)" queyi_neurips2027_v1.1.log
0
$ grep -o "Output written on [^(]*([0-9]* pages" queyi_neurips2027_v1.1.log | tail -1
Output written on queyi_neurips2027_v1.1.xdv (40 pages
```

> **注意**：tectonic 在 Windows 上会打一行 `Fontconfig error: Cannot load default config file`
> 到 **stderr**（字体配置缺失），**不是** TeX 错误——编译成功且 PDF 正常写出。
> 本条已在报告里显式登记，避免把它误计为"编译错误"。

### 1.2 编译（cover letter）

```
$ cd research/latex && tectonic cover_letter.tex
warning: cover_letter.tex:56: Overfull \hbox (6.16481pt too wide) in paragraph at lines 50--56
note: Writing `cover_letter.pdf` (31.7099609375 KiB)
```
⇒ **0 错**，仅 1 条排版警告（Overfull hbox 6.16pt）。

### 1.3 paper_gate 6/6

```
[paper-gate] 6 项检查， 失败 0， 跳过 0
  [OK ] 主文页数≤9                 page:endmain -> 9 页
  [OK ] 0 未定义引用                undefined 条目 0
  [OK ] 所有 \section 有 \label   8 个 section 均有 label
  [OK ] 所有 \ref 有 \label       34 个 ref 全部有 label
  [OK ] 摘要≤250词                摘要英文词数 = 229
  [OK ] 无 TODO/FIXME/HACK 残留   仅已登记占位（TODO{670a} 宏 + 0 个 ablation 占位）
[paper-gate] PASS
```

（`\ref` 数从 33 → **34**：本批新增 3 处 `\ref{app:samplecomplexity}` / `\ref{app:metatheory}`
被去重合并，净增 1 个引用目标。）

### 1.4 匿名化

```
$ python tools/anonymity_check_670c2.py
[anonymity] STRICT 命中 0， MAIN 命中 0
[anonymity] PASS
```

### 1.5 verify_paper_numbers

```
$ python tools/verify_paper_numbers.py --no-cmd
检察 128 条；missing 0；consistent 102
数字 token 1860；未归类 174
692 批次自洽：35/35 PASS
输出：data/676h_number_audit.json / data/676h_number_audit_report.md
```

报告 §1「硬不一致清单（missing + active）」**为空**：
> "论文里已有的数字逐条追到了权威源，且写法一致。"

> **覆盖度变化**：未归类 token 从 **161 → 174**（+13）。这是**新增数字**（4096 / 849 / 17 /
> 55.84 / 44.17 / 0.0071 / 0.3534 等）尚未进检察表所致——**覆盖度指标，不是不一致**。
> 本批**未**改 `tools/verify_paper_numbers.py`（属验证工具，不在本批交付范围）。

### 1.6 fast_gate

```
$ ./.venv/Scripts/python.exe tools/fast_gate.py --skip-frontend
  [PASS] 658 门禁（L0 5/5 + S5/S6）  7.9s
  [PASS] 669d 门禁（六条 P0 规则）  1.0s
  [PASS] 671a guard（三方数字一致）  2.1s
[fast-gate] overall=PASS  总耗时 10.9s（预算 300s）
```

> ⚠ **必须用仓库 venv 的解释器**：用系统/托管 Python 跑会因**缺 pytest** 而让
> `658 门禁 S6 单元测试` 假 FAIL（实测：managed python ⇒ `No module named pytest` ⇒ rc=1）。
> 换成 `./.venv/Scripts/python.exe` 后 **PASS**。这是**环境问题，不是回归**。

---

## 2. 未达标项：全稿页数 40 > 36（**本批开始前即已超标**）

| 时点 | 正文 | 全稿 |
|---|---:|---:|
| 本批开始前（`git stash` 前基线，tectonic 实测） | 9 | **39** |
| 本批结束后 | 9 | **40** |
| 任务书目标 | ≤ 9 | **≤ 36** |

**事实**：任务书的"全稿 ≤ 36 页"目标**在本批开始前已被违反**（基线 39 页）。
`research/latex/VERSION.md` 记录的 v1.5(691) 状态是"全稿 36→35 页"；
其后 **696-A 批次**（`779f8238`，three-state transition matrix + 26 条新引用）把稿子推到 39 页，
**本批再加 1 页**（B/C/D 三段附录 + 2 处正文短句）。

**本批的处置（按任务书"优先放附录"）**：

1. B / C / D 的**主体全部放附录**（`app:driftalgebra` 新增 2 个 subsection；`app:related` 新增 1 段）；
2. 正文只加了 **2 处短句**（§3.4 的 "Design requirement" 1 段、§6 的 "Do the rules travel?" 1 段），
   合计约 **120 词**，**正文仍为 9 页**（page:endmain 未变）；
3. **未**为了压页数删除任何既有内容（红线 6：论文修改必须逐行 git diff 核验，确保没有误删）。

**结论**：**不声称"页数达标"**。要回到 ≤36 页需要**专门的减页批次**（可选项：把
`app:a5full` / `app:humanize` / `app:incidents` 三节移入补充材料），**不在本批范围**。

---

## 3. 复算命令（一键复现本报告）

```bash
cd C:/CodeLearnling/note/note/C++/CPP-Bible
cd research/latex && tectonic --keep-logs --keep-intermediates queyi_neurips2027_v1.1.tex && cd ../..
grep -c "^!" research/latex/queyi_neurips2027_v1.1.log                     # 0
./.venv/Scripts/python.exe tools/paper_quality_gate_670c2.py               # 6/6 PASS
./.venv/Scripts/python.exe tools/anonymity_check_670c2.py                  # PASS
./.venv/Scripts/python.exe tools/verify_paper_numbers.py --no-cmd          # missing 0
./.venv/Scripts/python.exe tools/fast_gate.py --skip-frontend              # PASS
cd research/latex && tectonic cover_letter.tex                             # 0 错
```

---

## 4. 诚实边界

1. **全稿页数未达标（40 > 36）**，且**本批开始前即已超标（39）**；本批**只声明"新增 1 页"**，
   不声称解决页数问题。
2. `fast_gate` 的 **pytest 档**本批**未指定用例**（本批未新增测试）⇒ 报告里显形为
   `[SKIP] pytest（未指定，跳过）`；**fast_gate PASS ≠ 全量回归 PASS**（工具自带说明）。
3. `verify_paper_numbers` 的 **174 个未归类 token** 未逐条归类到检察表（覆盖度缺口，非不一致）。
4. 匿名化检查只覆盖 `tools/anonymity_check_670c2.py` 的正则集合；**不构成**穷尽的身份泄漏证明。
5. 编译验证只在**本机 tectonic 0.17.0**上做过；未在 CI 的 `-m slow` 档或 pdflatex 上复验。

---

*文件生成：2026-10-09 ｜ 批次 703 任务 G ｜ 编译 0 错 ｜ 未 push*
