# 703-F · 论文已知问题修复报告

- **批次**：703 ｜ **任务**：F ｜ **日期**：2026-10-09
- **被修文件**：`research/latex/queyi_neurips2027_v1.1.tex`
- **编译**：`tectonic --keep-logs --keep-intermediates queyi_neurips2027_v1.1.tex` ⇒ **0 错**
- **diff 规模**：`122 insertions(+), 2 deletions(-)`（B/C/D 的新增内容 + 本任务的 1 处改写）
- **红线**：未 push；未跑 `detect()`；未改检测器/样本/冻结矩阵；未改 `queyi_refs.bib`。

---

## 0. 一句话

> 任务书列的 5 类问题里，**2 类在本批开始前已修复**（措辞过强、页脚），
> **2 类确认已满足**（TODO 清零、数字一致性），**1 类本批修复**（匿名化：主文里唯一的
> `data/682\_kappa.json` 路径命中）。全部改动**逐行 git diff 核验：只有 2 行删除，均为本批有意改写**。

---

## 1. TODO 清零 —— ✅ 已满足（0 处）

```
$ grep -c "TODO" research/latex/queyi_neurips2027_v1.1.tex
0
$ grep -n "TODO\|FIXME\|HACK" research/latex/queyi_neurips2027_v1.1.tex
（无输出）
```

`paper_quality_gate_670c2.py` 第 7 项（无 TODO/FIXME/HACK 残留）**PASS**：
"仅已登记占位（TODO{670a} 宏 + 0 个 ablation 占位）"。
本批新增的 B/C/D 三段文字**未引入**任何 TODO/FIXME/HACK（复检为 0）。

---

## 2. 数字一致性 —— ✅ 已满足（逐条核验）

### 2.1 `13/34` vs `18/70`

| 位置 | 内容 | 状态 |
|---|---|---|
| 正文 line 455 | `\textbf{13 of 34} normalized types exceed $50\%$ blindness` | ✅ 正确口径 |
| 正文 line 851（claim 表） | `13/34 normalized types $>50\%$ blind` | ✅ |
| 附录 line 1651 / 1707 | `13 of 34` / `13 of 34` | ✅ |
| 附录 line 1888 | `13/34 types $>50\%$` | ✅ |
| 文件头 line 37（**注释**） | `18/70 -> 13/34` | ✅ 仅作为"已修复"的历史记录 |

⇒ 全文**统一用 13/34**；`18/70` **只出现在文件头注释**里，是修复记录，不构成不一致。
（`verify_paper_numbers.py` 128 条检察 **0 硬不一致**。）

### 2.2 `1137` vs `1147`

正文 line 373–375 有显式解释：

> "A 10-sample counting-caliber difference between the A5 matrix ($n{=}1137$, after
> de-duplication) and the blind-spot map ($n{=}1147$, pre-de-duplication superset) is documented
> as **two counting calibers of one population, not a contradiction**."

⇒ 口径说明**在正文**（不是埋在附录），符合任务书"确保脚注解释清楚"。

### 2.3 `+24.03pp` vs `+7–12pp`（全池 vs 控制后）

| 位置 | 表述 | 是否说清口径 |
|---|---|---|
| F1（line 429–437） | `+24.03pp at $k{=}4$`（全池）… `removing degenerate assets` 后 `$k{=}4$: $0.00$pp`；`$k{=}1$: +11.31pp`、`$k{=}2/3$: +7.42pp`（degenerate-free Pool A） | ✅ 明确"全池 / 控制后" |
| claim 表（line 870） | `mostly pool composition ($+24.0$pp collapsing to $0.0$pp at $k{=}4$), and what survives is the mechanism effect on the degenerate-free pool (+11.31pp, $k{=}1$; $\approx +7$–$12$pp)` | ✅ |
| 附录 line 1687 | `degenerate assets are worth $+24.03$pp of the single-point $\Delta$ ($+12.81$pp vs. the 2000-draw mean)` | ✅ |
| 摘要 line 108 | `A $+24.0$pp selection gain is mostly measurement-pool composition: removing degenerate assets leaves $+7.4$--$11.3$pp` | ✅ 并排出现 |

⇒ 三个数**并排出现且各自标注口径**，符合 `research/cover_letter.md` §3 的口径纪律。

---

## 3. 措辞过强 —— ✅ 本批开始前已修复（复检确认）

| 任务书要求 | 实测 | 结论 |
|---|---|---|
| "首次提出" → "据我们所知" | 全文**无** "we are the first to …" 断言；只有 line 169 的**否定式** `\textbf{We do not claim to be the first to audit an evaluator}`；`first-class` 的 5 处均指"一等公民"（first-class object / field / state），非优先权主张 | ✅ 已满足 |
| "证明了" → "在本数据集上观察到" | 全文**无** `we prove` / `proves that` / `we establish` / `demonstrates that` 类断言；line 891 的 `toolchain proves itself` 是**威胁 T1 的条目名**（描述"自证"这一风险），非本文结论 | ✅ 已满足 |
| "静默指纹" → "单一环境对上的候选特征" | 正文 line 481–485 已改为 `We report the absence of an unknown increase as a \emph{candidate signature on a single environment pair} ($n_{\text{env}}{=}1$), \emph{not} a sufficient \emph{fingerprint} of silent degradation` | ✅ 已满足 |

> **本批新增文字的自检**：新增的 B/C/D 段落**未**使用 "prove / first / fingerprint" 类措辞；
> 元理论段用 `a finite model check … shows that …` 并附 `Honest boundary: ``identically true''
> here means true within this finite domain`。

---

## 4. 页脚修复 —— ✅ 本批开始前已修复（本批**实测**确认）

`neurips_2025.sty` 的默认 notice 是
`Submitted to \@neuripsordinal\/ Conference on Neural Information Processing Systems (NeurIPS \@neuripsyear). Do not distribute.`
（即 "NeurIPS 2025"）。论文源码 line 77–81 用 `\renewcommand{\@noticestring}` 覆盖为中性串。

**本批从编译产物 `queyi_neurips2027_v1.1.pdf` 抽取文本实测**：

```
'Submitted': 0     'Do not distribute'（单独出现）: 0     'Thirty': 0
footer 实际内容: "Under review (anonymized). Do not distribute."
title block 实际内容: "Anonymous Author(s) Affiliation Address email"
```

⇒ 页脚**不是** "NeurIPS 2025"，而是 "Under review (anonymized). Do not distribute."；
6 处 `NeurIPS` 字样**全部来自参考文献**（`NeurIPS 2025 Datasets and Benchmarks Track`、
`NeurIPS 2019 reproducibility program`、`NeurIPS dataset management practices`、
`Advances in Neural Information Processing Systems (NeurIPS ...)`、`NeurIPS Dataset Review`、
`NeurIPS 2026`）——属**引用**，不是本文投稿年份声明。

---

## 5. 匿名化 —— 🔧 **本批修复 1 处**

**修复前**：`tools/anonymity_check_670c2.py` ⇒ `[anonymity] STRICT 命中 0，MAIN 命中 1` → **FAIL**

```
[HIT] MAIN_ONLY(main text) line 594: /(?<![\w/])data// -> 'data/'
```

命中源：T1 段里主文**唯一**的仓库路径 `(\texttt{data/682\_kappa.json})`。

**修复**（1 行改写，无语义损失）：

```diff
-instrument-side reading; the two lowest values were unreported before this batch
-(\texttt{data/682\_kappa.json}). A
+instrument-side reading; the two lowest values were unreported before this batch (the
+per-field $\kappa$ artifact is listed in Appendix~\ref{app:reframe689}). A
```

**修复后**：`[anonymity] STRICT 命中 0，MAIN 命中 0` ⇒ **PASS**。
（附录里的 `data/...` 路径**不**被判为泄漏——检查器把 `\appendix` 之后视为允许区。）

---

## 6. 逐行 git diff 核验（红线 6）

```
$ git diff --stat research/latex/queyi_neurips2027_v1.1.tex
 1 file changed, 122 insertions(+), 2 deletions(-)

$ git diff -U0 … | grep "^-" | grep -v "^---"
-instrument-side reading; the two lowest values were unreported before this batch
-(\texttt{data/682\_kappa.json}). A
```

⇒ **全文只有 2 行被删除**，且正是 §5 里本批**有意**改写的那两行。
**没有任何误删**（B/C/D 的新增全部是插入）。

---

## 7. 复算命令（每条一行）

```bash
grep -c "TODO" research/latex/queyi_neurips2027_v1.1.tex                      # 0
grep -n "13 of 34\|13/34" research/latex/queyi_neurips2027_v1.1.tex          # 5 处，全部 13/34
grep -n "18/70" research/latex/queyi_neurips2027_v1.1.tex                    # 仅文件头注释 1 处
python tools/anonymity_check_670c2.py                                        # PASS（0 命中）
python tools/paper_quality_gate_670c2.py                                     # 6/6 PASS
python tools/verify_paper_numbers.py --no-cmd                                # missing 0
cd research/latex && tectonic --keep-logs --keep-intermediates queyi_neurips2027_v1.1.tex
```

---

## 8. 诚实边界

1. 本批**只修复了 1 处**真实缺陷（匿名化命中）；其余 4 类**在本批开始前已满足**，
   本批做的是**复检 + 出具证据**，不是"修了 5 类"。
2. 页脚与措辞的"已修复"是**实测**结论（从 PDF 抽文本 / 全文 grep），不是沿用上游报告。
3. `verify_paper_numbers.py` 的"未归类 token"从 **161 → 174**（本批新增 13 个数字 token，
   主要是 4096 / 849 / 17 / 55.84 / 44.17 等新数字）——这是**覆盖度报告**，不是不一致。
4. 本批**未**为 `tools/compute_703_zero_cost_validation.py` 新增 pytest 测试
   （700 批次的同类 `compute_700_*.py` 亦未加）；`fast_gate` 的 pytest 档因此无本批用例。
5. 论文**全稿页数 39 → 40**（正文仍 9 页）；**已超任务书的"全稿 ≤36 页"目标，且本批开始前即已超标（39）**，
   见 `data/703_final_validation.md` §2。

---

*文件生成：2026-10-09 ｜ 批次 703 任务 F ｜ 编译 0 错 ｜ 未 push*
