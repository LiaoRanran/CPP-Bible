# 684 · C3 论文修改清单（逐节逐行：旧文 → 新文 → 理由）

- **批次**：684 ｜ **对象**：`research/latex/queyi_neurips2027_v1.1.tex`（v1.3 / 677d）
- **重要前提**：本清单**只给建议，不改论文**（683 可能并行改附录）。行号基于 684 读取时快照；合并前必须与 683 最终版本对齐（用 `git diff` 复核行号后再落地）。所有新增数字须引用 `data/684_*.json` 作为权威来源。

---

## 1. Abstract（L76–99）

| 行 | 当前旧文（摘）| 建议新文 | 理由 |
|---|---|---|---|
| L94–96 | 「FD 54.6% vs Random 30.6% (+24.0pp full pool) … excluding degenerate assets Random draws the same four at k=4」 | 在句首补：「Asset selection is formalized as submodular maximization; the greedy choice carries a $(1-1/e)$ guarantee. 」并把领起数字改为「the non-degenerate selection effect is +7–12pp (the full-pool +24.0pp is dominated by degenerate-asset avoidance)」 | 兑现 C2：把形式化承诺前置；避免 +24pp 锚定（诊断 Claim A 残留风险）|
| L97–98 | 「A5 isolates 'do not fund assets that cannot inform,' not 'a smarter ranking'.」 | 保留，并补：「—a result we now ground in submodular theory (greedy attains the optimum on this instance).」 | 与 A1/A2（greedy=optimal）呼应，强化「非更聪明排序」的严谨性 |

## 2. Contributions（L145–167）

| 行 | 当前旧文 | 建议新文 | 理由 |
|---|---|---|---|
| L145–151 (贡献1) | 「(1) A definition and three checkable properties of failure-driven verifier evolution」 | 保留，但把「evolution operator E(...)」表述从「novel operator」语气改为「an operator instantiation …」 | 诊断 Claim B：operator 须降级为 instantiation |
| L164–167 | 「A runnable instantiation … We give no theorems … we claim no novelty in the four-state encoding.」 | 在 L167 后**新增贡献**：「(4) *A formalization of asset selection as submodular maximization* (\S method): we show FD's greedy/frequency choice is the standard greedy algorithm for monotone submodular maximization under a cardinality constraint, carries the $(1-1/e)$ approximation guarantee (Nemhauser et al., 1978), and attains the optimum on our 1137-sample instance; we further derive a closed form for the Random-selection expectation and a degenerate-asset gap formula.」 | 本批主体贡献（A1–A4）；把「formalize」而非「novel」作为卖点 |

## 3. Method — Formal definitions（L1012–1052）

| 行 | 当前旧文 | 建议新文 | 理由 |
|---|---|---|---|
| L1052 之后 | （Evolution operator 段落结束）| **新增段落**「Selection as submodular maximization.」：$f(S)=\left|\bigcup_{a\in S}C_a\right|$ 定义；声明 $f$ 单调子模（A2 全枚举 0 违反）；FD greedy/frequency ≡ 标准贪心（A1）；给出 $(1-1/e)$ 保证并注明实测 greedy=optimal（比值 1.0）。 | A1/A2/A3 的论文落地；使 Claim C 的「formalize」兑现 |
| L1042–1044 | 「The literal specification collapses: novel ≡ failure …」 | 保留，并在 L1044 后补一句：「Consequently the operator is mathematically a submodular greedy (see Selection-as-submodular paragraph); we therefore do not claim a novel selection algorithm.」 | 衔接形式化，堵死「novel operator」误读 |

## 4. Experiments（新增段落，建议置于 A5 结果段之后）

| 位置 | 建议新增 | 理由 |
|---|---|---|
| A5 节末 | 一段「Theoretical vs.\ empirical approximation.」：给出闭式 $\mathbb{E}[f(S^{\text{rand}}_k)]=\sum_s(1-\binom{8-r_s}{k}/\binom{8}{k})$（k=4 ⇒ 42.1%），与贪心 58.5%/最优 58.5% 对照；澄清 $(1-1/e)=63.2\%$ 是比值地板而非覆盖率目标（A3 §5）。 | 把 A3 的「63.2% vs 54.6% 量纲混淆」正本清源落到论文 |

## 5. Related Work（L174–205）

| 位置 | 建议新增 | 理由 |
|---|---|---|
| L205 之后 | 补三条方向：(i) submodular maximization（Nemhauser 1978, Krause & Golovin 2014, data subset selection）；(ii) active testing / adaptive evaluation（active learning, sequential analysis）；(iii) evaluation governance / Goodhart（见 D 节 15+ 文献）。 | 支撑新贡献 2 与治理框架 |

## 6. Conclusion

| 位置 | 当前旧文（倾向）| 建议新文 | 理由 |
|---|---|---|---|
| 结论段 | 避免出现「FD is a better/smarter selector」措辞 | 改为「FD is a *robust, submodular-greedy* selector that reliably avoids zero-information assets; its selection effect is directional, and its value is governance, not a detection gain.」 | 与全文方向性 claim 一致，闭合 Claim A/B/C |

---

## 7. 合并纪律（与 683 协调）

- 本清单所有修改**不在此批提交**（红线：只 add `data/684_*` + 本批 research 建议文件；不改 `research/*.tex`）。
- 待 683 完成附录修订后，由统一批次（建议 685/合并批）按本清单落地，落地前用 `git diff` 复核行号漂移。
- 所有新增数字必须从 `data/684_submodularity_test.json` / `684_approximation_guarantee.md` / `684_degenerate_assets_theory.md` 取，**不得手写**，防止与矩阵脱节。
