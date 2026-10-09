# 703-B · 700 元理论写进论文 —— 具体改动

- **批次**：703 ｜ **任务**：B ｜ **日期**：2026-10-09
- **被改文件**：`research/latex/queyi_neurips2027_v1.1.tex`
- **落点**：附录 `\section{Measurement Drift Algebra: Three-State Transition Model}`
  （`\label{app:driftalgebra}`）内**新增 1 个 subsection**
- **diff hunk**：`@@ -1384,0 +1420,85 @@`（**纯插入 85 行，0 删除**）
- **复算**：`python tools/compute_700_axiom_independence.py` → `data/700_axiom_independence.json`
- **红线**：`detect_calls = 0`；未改检测器/样本/冻结矩阵；未改 `queyi_refs.bib`。

---

## 1. 加了什么

在 `\paragraph{Conservation checks.}`（原 §末尾）之后插入：

```
\subsection{A metatheory: which axioms are actually independent}
\label{app:metatheory}
  …（有限模型检查 / 最小公理集 / A2·A5 是真正的约束 / 诚实边界）
\paragraph{Incompleteness: the missing A8.}
  …（标签粗化见证 / Type III 不可表达 / 登记 A8 标签轴闭包 / 与 34 vs 70 类实测非单调一致）
\paragraph{Complexity of caliber arbitrage.}
  …（最大覆盖归约 ⇒ NP-hard；贪心 (1-1/e)；与 684 的贪心保证同源）
```

**位置理由**：论文正文 §3（Evaluator-Audit Protocol）已满 9 页预算，
且任务书明确"这些放在附录，不占正文页数"。`app:driftalgebra` 是论文里唯一
讲"漂移代数 + Type III/IV"的附录节 ⇒ 元理论放在这里与上下文同轴。

---

## 2. 逐条对照：写进论文的数字 vs 700 报告

| 论文新增表述 | 700 报告原文 | 一致性 |
|---|---|---|
| "a finite model check ($|X|{=}4$, $|A|{=}3$, **all** $2^{4\times3}{=}4096$ coverage structures, **seven** aggregation families)" | `700_metatheory.md` §1.1：样本数 4 / 资产数 3 / 覆盖结构数 $2^{4\times3}=\mathbf{4096}$（全部穷举）/ 聚合族 **7 种** | ✅ |
| "**only two of the seven are independent**: A2 … and A5" | §1.2 结论表：A2 ✅真公理、A5 ✅真公理 | ✅ |
| "A3 (idempotence), A4 (commutativity/closure), A6 (irreversibility) and A7 (observability stratification) follow from defining $\tau$ as column deletion" | §1.2：A3/A4/A6/A7 判定 🔷**定理**，"由 $\tau_G=$ 列删去直接推出" | ✅ |
| "A1 … is a **meta-axiom** that constrains the language rather than the structure" | §1.2：A1 **元公理**，"约束语言/分类法，不是结构性质" | ✅ |
| "minimal system is $\{$A1 meta$\}\cup\{$A2, A5 structural$\}$, with $\{$A3, A4, A6, A7$\}$ as theorems" | §1.4 方框：元公理 {A1}、结构公理 {A2, A5}、定理 {A3, A4, A6, A7} | ✅ |
| "mean calibers violate A5 … and min calibers violate A2" | §1.4："**均值口径违反 A5**（掺入零产资产即改变报告值），**min 口径违反 A2**" | ✅ |
| "Honest boundary: ``identically true'' … means true **within** this finite domain (4096 structures, seven aggregation families), not a proof for arbitrary domains; and A2 and A5 could not be separated within this family, so A2's independence is registered as **not strictly established**" | §5 诚实边界 1/2/3："'恒真'只对该域成立"、"聚合族只有 7 种 ⇒ 不能排除第 8 种"、"A2 与 A5 在本域内未能分离 ⇒ A2 那一行的独立性未严格建立" | ✅ |
| 标签粗化见证：$C_a{=}\{0,1\}$, $C_b{=}\{2\}$, $C_c{=}\varnothing$；$V{=}(c,c,c,m)$；$R_{\mathrm{or}}{=}0.75$；分组盲区率 $\{0,0,1\}\to\{0.25\}$ | §2.1 见证表：固定 $C_a=\{0,1\},C_b=\{2\},C_c=\varnothing$，裁决 $V=(c,c,c,m)$；$R_{\text{or}}=0.75$ 恒定；$t_3$ 盲区率 100% → 全局 25% | ✅ |
| "Type III … is thus **inexpressible**: $\lambda$ is not in the caliber signature $(D,A,E,\Theta,P)$" | §2.1："$\lambda$ **不在口径签名里**（697 的签名是 $(A,E,\Theta,P)$，**没有标签槽**）" | ✅ |
| "**A8 (label-axis closure)**: the signature must become $(D,A,E,\Theta,P,\lambda)$ … statistics without a declared $\lambda$ are not comparable" | §2.1 候选表述：口径签名扩为 $(D,A,E,\Theta,P,\lambda)$；未声明 $\lambda$ 的统计量**不可比较** | ✅ |
| "the measured non-monotonicity of the high-blindness share (38.24% under 34 classes vs. 25.71% under 70)" | §2.1：Type III 的"高盲类占比"在 34 类下 **38.24%**、70 类下 **25.71%**，**非单调**且**不能换算** | ✅ |
| "Within this finite domain we found no gap other than A8, and we do not claim there is none" | §2.2："本批**未发现**除 A8 之外的缺口；**不排除**（4096 结构的域有限，聚合族只 7 种）" | ✅ |
| "maximum coverage, hence NP-hard, with the greedy algorithm attaining $(1-1/e)$" | §4：口径套利 **NP-hard**（由最大覆盖归约；Feige 1998 的 $(1-1/e)$ 不可近似性）；近似算法**贪心达 $(1-1/e)$** | ✅ |
| "the submodular guarantee used for asset selection (Appendix~\ref{app:submodular687}) is therefore the approximation algorithm for caliber arbitrage" | §4："**684 的贪心保证在元理论层就是'口径套利最优化的近似算法'**" | ✅ |
| "this is a reduction argument … **not a formal proof here**, and at Queyi's scale ($|A|{=}8$) the problem is trivial by enumeration" | §4 警告框：**归约论证**，**本批未做形式化归约证明**；$|A|=8$ 时**平凡** | ✅ |

⇒ **论文里没有一个数字超出 700 报告**；700 报告的全部"诚实边界"（§5 的 8 条）中，
与本段相关的 6 条已**逐条搬进论文**（域有限 / 聚合族有限 / A2 独立性未严格建立 /
A6 依赖 $\tau$ 定义 / A7 检验范围 / NP-hard 是归约论证）。

---

## 3. 为什么**没有**把 §3（与其他测量理论对比）和 §5 的 8 条边界全搬进论文

| 700 报告内容 | 处置 | 理由 |
|---|---|---|
| §3 与量子测量 / 计量经济学 / 心理测量学 CTM·IRT 的 4 列对比表 | **未搬** | 类比密集且需大量解释；任务书只要求"公理独立性 + 不完备性 + 复杂性"三条 |
| §3.1 三条类比（A6↔坍缩、A5↔子模、A8↔DIF） | **未搬** | 同上；且 IRT/DIF 会引入新的引用需求（`queyi_refs.bib` 本批红线不动） |
| §4 的"实践规模 $2^8=256$ 可穷举" | **已浓缩**为 "at Queyi's scale ($|A|{=}8$) the problem is trivial by enumeration" | 保留最关键的规模限定 |

---

## 4. 复算与核验命令

```bash
python tools/compute_700_axiom_independence.py                     # 重算 4096 结构域
git diff -U0 research/latex/queyi_neurips2027_v1.1.tex | grep "^@@"
# @@ -1384,0 +1420,85 @@  ⇒ 纯插入 85 行
grep -n "app:metatheory" research/latex/queyi_neurips2027_v1.1.tex  # 1 处（label 定义）
```

---

## 5. 诚实边界

1. 本批**未重跑** `compute_700_axiom_independence.py`（其产物 `700_axiom_independence.json`
   已在 700 批次落盘，本批只**引用**）；论文数字以该 JSON + `700_metatheory.md` 为准。
2. 论文表述把 700 报告的**表格**改写成**散文**，未逐格复制；§2 的对照表是**逐条**核验过的。
3. "A2 与 A5 不可分离"这一**诚实缺口**被**写进了论文**（未隐藏）。
4. 本段**未**引入任何新引用 ⇒ `queyi_refs.bib` 未改（符合红线）。

---

*文件生成：2026-10-09 ｜ 批次 703 任务 B ｜ `detect_calls` = 0 ｜ 未 push*
