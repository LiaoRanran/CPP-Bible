# 684 · 论文逐节修改建议（含可粘贴替换文本）

- **批次**：684 ｜ **配套**：`684_framing_proposal.md`、`684_paper_modification_checklist.md`
- **说明**：以下给出**可直接替换的 LaTeX 片段**。行号针对 `research/latex/queyi_neurips2027_v1.1.tex` v1.3；合并前与 683 对齐。本批**不执行**这些修改。

---

## §1 摘要（Abstract，L76–99）

**替换 L94–96 的领起句式**，把形式化前置、把 +24pp 降级：

```latex
% --- 684 建议替换 L94-96 起首 ---
Asset selection is formalized as monotone submodular maximization; the greedy
choice carries a $(1-1/e)$ approximation guarantee (Nemhauser et al., 1978) and
attains the optimum on our 1137-sample instance. The A5 budget-matched control
runs at full scale ($n{=}566$): the non-degenerate selection effect is
$+7$--$12$pp (the full-pool $+24.0$pp is dominated by degenerate-asset
avoidance), while excluding degenerate assets Random draws the same four at
$k{=}4$; clone-aware re-splitting leaves both unchanged (effective
$n\approx133$--$140$). A5 isolates ``do not fund assets that cannot inform,''
not ``a smarter ranking''---a result now grounded in submodular theory.
% -----------------------------------------
```

---

## §2 贡献（Contributions，L145–167）

**在 L167 之后新增第 (4) 条贡献**（本批主体）：

```latex
% --- 684 新增贡献 (4) ---
(4)~\textbf{A formalization of asset selection as submodular maximization}
(\S\ref{sec:method}): we show that failure-driven selection's greedy and
frequency variants are the standard greedy algorithm for monotone submodular
maximization under a cardinality constraint, that the choice therefore carries
the $(1-1/e)$ approximation guarantee, and that on our 1137-sample instance the
greedy attains the optimum (ratio $1.0$). We further derive a closed form for the
Random-selection expectation and a degenerate-asset gap formula
($\Delta\approx c\cdot kd/n$). \textbf{We claim formalization and a guarantee, not
a novel selection algorithm.}
```

同时把 L145–151 贡献 (1) 中「evolution operator」的语气由隐含 novel 改为 instantiation（见 checklist L145–151 行）。

---

## §3 Method — 选择的形式化（新增段落，置于 L1052 之后）

```latex
% --- 684 新增：Selection as submodular maximization ---
\paragraph{Selection as submodular maximization.}
Let $\mathcal{A}$ be the $8$ candidate assets and $C_a$ the set of samples
asset $a$ catches. The coverage objective
$f(S)=|\bigcup_{a\in S}C_a|$ is monotone submodular (union of sets); we verified
this by exhaustively checking all $17{,}496$ triples $(A,B,a)$ with
$A\subseteq B\subseteq\mathcal{A}$, $a\notin B$---zero violations. Failure-driven
selection's frequency ranking and residual-coverage greedy are both the standard
greedy algorithm for this problem (Nemhauser et al., 1978), which guarantees
$f(S^{\text{greedy}}_k)\ge(1-1/e)\,f(S^*_k)$. On our data the greedy attains the
optimum exactly (ratio $1.0$), so FD's value is not a smarter ranking but a
robust avoidance of zero-information assets. The Random-selection expectation has
the closed form
$\mathbb{E}[f(S^{\text{rand}}_k)]=\sum_{s}(1-\binom{8-r_s}{k}/\binom{8}{k})$
($42.1\%$ at $k{=}4$), and the degenerate-asset gap follows
$\Delta\approx c\cdot kd/n$ (see Appendix).
```

---

## §4 Experiments（新增理论-实验对照段）

在 A5 结果段末追加（引用 `684_approximation_guarantee.md` §5）：

```latex
\paragraph{Theoretical vs.\ empirical approximation.}
The $(1-1/e)\approx63.2\%$ figure is a \emph{ratio} floor
(greedy/optimal), not a coverage target. Our greedy reaches $100\%$ of the
optimum ($58.5\%$ coverage), bounded above by the 8-asset OR ceiling $63.0\%$
($92.9\%$ attained at $k{=}4$). The Random expectation ($42.1\%$ at $k{=}4$,
closed form above) sits $16.4$pp below greedy---the same direction as the A5
$\Delta$, explained by degenerate-asset avoidance rather than superior ranking.
```

---

## §5 Related Work（L205 之后补三条）

```latex
\paragraph{(6) Submodular maximization \& data subset selection (the formalism we adopt).}
Nemhauser et al.~\cite{nemhauser1978submodular} give the $(1-1/e)$ greedy bound;
Krause \& Golovin~\cite{krause2014submodular} survey submodular functions in
machine learning and feature/subset selection. We are the first to cast
verifier-asset selection as submodular maximization.
\paragraph{(7) Active testing \& adaptive evaluation.}
Active testing~\cite{golovin2010near} and sequential analysis frame when to stop
and what to measure; our failure-driven selection is an active-testing strategy
under a fixed budget.
\paragraph{(8) Evaluation governance \& Goodhart.}
Goodhart's law~\cite{goodhart1975problems} warns that targets become games; our
Merkle+ledger governance is a structural answer to evaluator self-deception.
```

---

## §6 Conclusion（去「更优」暗示）

将任何「FD is a better/smarter selector」措辞改为：

```latex
Failure-driven selection is a robust, submodular-greedy selector that reliably
avoids zero-information assets; its selection effect is directional, and its
scientific value is governance and auditable provenance, not a detection gain.
```

---

## 验收自检（任务卡验收标准 7–9）

- ✅ C1 逐条 claim 评估有证据（引用 676f/677c/682 + 本批 A/B）。
- ✅ C2 完整新核心表述 + 三贡献重构（治理 / 子模形式化 / 实证）。
- ✅ C3 逐节逐行旧文→新文→理由（本清单 + `paper_modification_checklist.md`）。
- ⚠️ 所有修改**待 683 完成后由统一批次合并**，本批仅产出建议文件。
