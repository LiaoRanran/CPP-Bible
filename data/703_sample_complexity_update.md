# 703-C · 700 信息论下界写进论文 —— 具体改动

- **批次**：703 ｜ **任务**：C ｜ **日期**：2026-10-09
- **被改文件**：`research/latex/queyi_neurips2027_v1.1.tex`
- **落点**：① 附录新增 `\subsection{Sample complexity, and why the protocol needs a second design}`
  （`\label{app:samplecomplexity}`）+ 新表 `tab:samplecomplexity`；
  ② 正文 §3.4 新增 `\paragraph{Design requirement.}`
- **diff hunk**：`@@ -1384,0 +1420,85 @@` 的**后半部分**（与任务 B 同一 hunk）
  ＋ `@@ -359,0 +360,7 @@`（正文 7 行，纯插入）
- **复算**：`python tools/compute_700_sample_complexity.py` → `data/700_sample_complexity.json`
- **红线**：`detect_calls = 0`；未改检测器/样本/冻结矩阵；未改 `queyi_refs.bib`。

---

## 1. 加了什么

### 1.1 附录（主体）

```
\subsection{Sample complexity, and why the protocol needs a second design}
\label{app:samplecomplexity}
  · 形式化：配对设计 + 符号检验；ε = ψ(2π−1)；
    m ≥ (z_{1-α/2}√(1/4) + z_{1-β}√(π(1−π)))² / (π−1/2)²，n = m/ψ
  · Table 1（tab:samplecomplexity）：四型 ψ / 配对 n / KL 地板 n
  · 两个结论：(i) 成本由 ψ（承载样本数）主导，不由效应量主导；
             (ii) Type III/IV 的 ψ=0 ⇒ 任何逐样本检验功效恒为 0
  · ⇒ Step 3 改为"双设计"：样本级配对（I/II）+ 设计级对照（III/IV）
  · 与 698-D 的 5 步协议对齐（Step 3 原被当作通用步骤）
  · 诚实边界 3 条
```

### 1.2 正文 §3.4（7 行）

```
\paragraph{Design requirement.}
Paired controls identify only Types I and II. Types III and IV leave every per-sample verdict
unchanged, so their discordance rate is zero and no per-sample test---paired or not---can see
them; the protocol therefore pairs a \emph{sample-level} control (I/II) with a
\emph{design-level} contrast (III/IV) and reports the sample size the paired step needs
(Appendix~\ref{app:samplecomplexity}).
```

**位置理由**：任务书说"5 步审计协议的 Step 3 改为'双设计'"。论文里**没有**独立的"5 步协议"节
（那是 698-D 的表述）；论文的对应物是 §3.3 Falsification procedure + §3.4 Four audit outcomes。
把"设计要求"挂在 §3.4 之后，语义上最贴近"协议的一步要改设计"。

---

## 2. 样本量表格（论文 vs 700 报告）

| 型 | 口径变化 | $\psi$ | **配对 $n$** | KL 地板 $n$ | 700 报告 | 一致 |
|:--:|---|---:|---:|---:|---|---|
| **I** | 剔除 3 个退化资产 | 0.0071 | **849** | 329 | `700_information_theory.md` §2：0.0071 / **849** / 329 | ✅ |
| **II** | 环境 E1→E2 | 0.3534 | **17** | 7 | §2：0.3534 / **17** / 7 | ✅ |
| **III** | 标签词表变化 | 0.0000 | **∞** | — | §2：0.0000 / **∞（配对设计不可检出）** | ✅ |
| **IV** | 聚合规则变化 | 0.0000 | **∞** | — | §2：0.0000 / **∞（配对设计不可检出）** | ✅ |

**公式与参数**：论文写的 $\alpha{=}0.05$、power $0.8$、$m\ge(\cdot)^2/(\pi-1/2)^2$、$n=m/\psi$、
$\varepsilon=\psi(2\pi-1)$ 与 700 报告 §1 表格**逐项一致**。

**两个结论的对照**：

| 论文 | 700 报告 |
|---|---|
| "(i) Audit cost is driven by *how many samples carry the drift* ($\psi$), not by how large it is: a $-35$pp drift is detected with $17$ paired samples, while a $0.71$pp drift needs $849$." | 结论 C2："**审计成本由'漂移被多少个样本承载'决定，而不是由'漂移有多大'决定**。一个看起来很大的漂移（如 −35pp）可能很便宜；一个很小的漂移（0.71pp）可能很贵。" ✅ |
| "(ii) Types III and IV are not ``hard to detect'' but *undetectable by any per-sample test* … the power of any paired test (McNemar, permutation, bootstrap) is *identically zero*." | 结论 C1："Type III 与 Type IV 不是'难'，而是'用这套设计根本检不出'…… 任何基于逐样本裁决的检验（包括配对 McNemar、置换检验、bootstrap）**功效恒为 0**。" ✅ |
| "The protocol's Step 3 must therefore be a **dual design**: sample-level pairing identifies Types I/II, while Types III/IV require a **design-level** contrast---two label vocabularies or two aggregation rules applied to the *same* raw adjudications and compared on grouped statistics rather than on verdicts." | 结论 C3："**协议应改写为'双设计'**：样本级配对（I/II）+ 设计级对照（III/IV）" ✅ |
| "This refines the five-step audit protocol of the extended framework, in which Step 3 was stated as a generic paired experiment; the pairing step is valid only on the asset and environment axes." | 结论 C3："698-D 的 5 步协议把 **Step 3（配对实验）** 当作通用步骤。本批证明它**只对 $A$ 轴（组件撤除）与 $E$ 轴（环境）有效**。" ✅ |

---

## 3. 与 698-D 的通用审计框架对齐

任务书要求"和 698-D 的通用审计框架对齐"。本批的落点方式：

| 698-D 的表述 | 论文的对应物 | 本批动作 |
|---|---|---|
| 5 步协议，Step 3 = 配对实验（**通用步骤**） | 论文 §3.3 Falsification procedure 的 (i)–(v)（**未编号为 Step 1–5**） | **不新增**"5 步协议"节（避免与 698-D 的编号体系在论文里凭空出现）；改为在 §3.4 后加 "Design requirement" 段，说明配对只覆盖 I/II |
| 8 类失败模式 → 识别信号 | 论文 §3.2 的 8 类失败模式 | 不动 |
| 四态审计结果 | 论文 §3.4 Four audit outcomes | 在其后追加设计要求 |

⇒ **对齐方式 = 语义对齐 + 显式引用附录**，而非复制 698-D 的编号。

---

## 4. 复算与核验命令

```bash
python tools/compute_700_sample_complexity.py                 # 重算四型 ψ 与 n
grep -n "tab:samplecomplexity\|app:samplecomplexity" research/latex/queyi_neurips2027_v1.1.tex
grep -n "849\|only \$17\$\|\\infty" research/latex/queyi_neurips2027_v1.1.tex | head
cd research/latex && tectonic --keep-logs --keep-intermediates queyi_neurips2027_v1.1.tex
grep -c "undefined" queyi_neurips2027_v1.1.log   # 0
```

---

## 5. 诚实边界

1. 论文把 700 报告的**策略模拟**（均匀/分层/Neyman 三策略、$B$ 预算曲线）**未搬进论文** ——
   它与"双设计"结论正交，且会显著增加篇幅；只在附录末以一句"strategy simulations …
   ran only on Queyi's 566 samples and one environment pair"登记其**适用边界**。
2. 论文未复述 700 报告的**一般网格表**（$\varepsilon/\psi$ 五档）——同上，属篇幅取舍。
3. 三条诚实边界（正态近似在小 $\psi$ 退化 / KL 地板偏乐观 / 模拟只覆盖 566 条 + 一个环境对）
   已**写进论文**。
4. 本批**未**重跑 `compute_700_sample_complexity.py`；数字以 `700_sample_complexity.json` 与
   `700_information_theory.md` 为准。

---

*文件生成：2026-10-09 ｜ 批次 703 任务 C ｜ `detect_calls` = 0 ｜ 未 push*
