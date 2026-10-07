# 684 · A1 子模优化形式化（核心）

- **批次**：684 ｜ **性质**：研究型（数学推导 + 轻量实验）｜ **执行人**：LiaoRanran（DCO 署名，未 push）
- **配套产物**：`data/684_submodularity_test.json`、`data/684_approximation_guarantee.md`、`data/684_degenerate_assets_theory.md`
- **数据来源**：`data/a5_676f_detection_matrix.json`（1137 样本 × 8 资产，真实 `detect`，未修改）
- **红线遵守**：不修改检测器 / 样本 / 论文核心数字 / 677c operator；只读共享产物

---

## 1. 符号定义

令：

- **资产集合** $\mathcal{A} = \{a_1, a_2, \dots, a_8\}$，对应 8 个验证器资产：
  `asan, compile-time, compiler-warn, cross-compile, linker, tsan, ubsan, wunsequenced`。
- **样本集合** $\mathcal{S} = \{s_1, s_2, \dots, s_N\}$，$N = 1137$。
- **判定函数** $\text{detect}(a, s) \in \{\text{catch}, \text{miss}, \text{unknown}\}$，直接取自 676f 判定矩阵（1 回合 OR 聚合口径；`unknown` 绝不当 `miss`）。
- **单资产 catch 集** $C_a \triangleq \{s \in \mathcal{S} : \text{detect}(a, s) = \text{catch}\}$。
- **预算** $k \in \mathbb{N}$，主分析取 $k = 4$（卡片口径），并给出 $k=1..7$ 的延展。
- **选择变量** $S \subseteq \mathcal{A}$，且约束 $|S| \le k$。

**覆盖函数**（唯一需要形式化的目标）：

$$
f(S) \triangleq \left|\left\{ s \in \mathcal{S} \;:\; \exists\, a \in S,\ \text{detect}(a,s) = \text{catch} \right\}\right|
= \left|\bigcup_{a \in S} C_a\right|.
$$

即 $f(S)$ 是「至少被 $S$ 中一个资产 catch 的样本数」。它等价于对 8 个单资产 catch 集合取**并集**后的基数。注意：$f(\varnothing) = 0$，且 $f$ 对 `unknown` 与 `miss` 均不计为覆盖（只有 `catch` 进入并集）。

**优化问题（P）**：

$$
\max_{S \subseteq \mathcal{A},\ |S| \le k} f(S).
$$

这是一个带基数约束（cardinality constraint）的**集合函数最大化**问题。

---

## 2. 问题陈述

我们有 8 个候选验证器资产，预算只允许并行/串行部署其中 $k=4$ 个。目标是最大化「被审计样本中被至少一种方法捕获（catch）的比例」。这是一个典型的**预算受限的资产选择（budget-constrained asset selection）**问题，属于离散优化。

该问题的困难性在于：组合空间 $\binom{8}{4} = 70$（对 $k=4$）可直接穷举最优；但当资产数放大到工业级（数十个 sanitizer / linter / 静态分析规则），穷举不可行，需要多项式时间的近似算法。因此把问题形式化为一个**已知有近似保证的结构**（子模最大化），是把「经验性选择」提升为「有理论背书的选择」的关键一步——这正是本批次对论文 Framing 的核心贡献（见 C2）。

---

## 3. FD 与贪心算法的对应关系

**FD（failure-driven）选择**在 677c 中被严格等价于两类算法：

1. **frequency 选择**（`677c` 证明 `frequency ≡ fd`）：按派生集 catch 计数降序取 top-$k$。
2. **greedy / set-cover 残差选择**（`677c` 证明 `fd_only ≡ greedy`）：迭代地选「当前边际覆盖收益最大」的资产。

我们采用更一般、理论更干净的**标准贪心（standard greedy for submodular maximization）**作为 FD 的形式化对应：

$$
\begin{aligned}
S_0 &\leftarrow \varnothing,\\
S_{t+1} &\leftarrow S_t \cup \left\{ a^*_t \right\},\quad
a^*_t \in \arg\max_{a \notin S_t} \big[\, f(S_t \cup \{a\}) - f(S_t) \,\big],\\
&\text{重复 } k \text{ 次}.
\end{aligned}
$$

即每一步把「边际收益 $\Delta_a(S_t) \triangleq f(S_t \cup \{a\}) - f(S_t)$ 最大」的资产加入集合。这**正是**子模函数最大化教科书的贪心算法（Nemhauser et al., 1978）。因此：

> **核心论断 A1.1**：FD 的 greedy / frequency 选择流程，在数学上等价于子模函数最大化的标准贪心算法。frequency 是 greedy 在「派生集单边计数」这一特定代理目标下的近似实现；当用真正的残差覆盖做代理时，二者在 $k$ 较小时排序一致，$k$ 较大时出现差异（如 $k=4$ 时 greedy 选 `compiler-warn` 而 frequency 选 `cross-compile`，见 A2/A3）。

本批实验（A2）给出：在完整 1137 样本上，greedy 选出的集合为
`{asan, ubsan, tsan, compiler-warn}`，覆盖率 **58.49%**；穷举最优同样是该集合，覆盖率 **58.49%** → greedy 达到**精确最优**（近似比 1.0，见 A2）。

---

## 4. 与 677c evolution operator 的映射

677c 把 FD 算法化为 `evolution_operator_677c.py`，其 `fd_only` 配置被证明与 greedy 等价。映射关系如下：

| 本形式化概念 | 677c operator 实现 | 说明 |
|---|---|---|
| 资产 $a \in \mathcal{A}$ | `assets` 列表（8 项） | 顺序一致（见矩阵 `assets` 字段） |
| 覆盖函数 $f(S)$ | 对派生集逐样本 OR 聚合计数 | 677c 在派生集上计 `fail_hits` |
| 边际 $\Delta_a(S)$ | operator 的 `redundancy` / `coverage` 分量 | 677c score 四分量中的 coverage 即此 |
| 贪心选择 | `fd_only`（= `greedy`，677c 已证等价） | 迭代取最大边际 |
| 频率选择 | `frequency`（= `fd`，677c 已证等价） | 派生集 catch 计数降序 top-$k$ |

**重要诚实声明**：677c 同时发现 `literal novel ≡ failure`（规格字面坍缩），即 operator 的 `novel` 分量与 `failure` 分量退化为同一信号，导致 `fd_novel ≡ fd_only`。这意味着在「真正的算法创新」维度上，当前 operator 并未超越「贪心 + 频率」这一经典子模选择。本批 A1 的形式化**正面承接了这一结论**：FD 的数学本质就是子模贪心，而非某种新颖的选择机制——因此论文的算法 claim 必须降级（见 C1/C2）。形式化的价值不在于「证明 FD 新颖」，而在于「给已有选择流程一个可引用的近似保证（(1−1/e) 及其曲率修正）」。

---

## 5. 子模性的直觉与后文衔接

覆盖函数 $f(S)=\left|\bigcup_{a\in S} C_a\right|$ 在集合论意义上是**单调子模（monotone submodular）**的：增加一个资产带来的边际收益，不会因集合已经很大而变得更大（边际收益递减）。这正是「加第 4 个资产比加第 1 个资产带来的新覆盖更少」的严格表述。

- **A2** 对这一性质做了**全枚举实证检验**（所有 $A\subseteq B\subseteq\mathcal{A}$ 与 $a\notin B$ 的组合，共 17496 组），结论是**成立（0 违反）**。
- **A3** 据此推导 FD 贪心的 $(1-1/e)$ 近似保证，并与 676f/682 的实验值对比。
- **A4** 用同一框架解释 677c 发现的「退化资产」现象（边际收益恒为 0，贪心必然不选）。

---

## 6. 小结（A1）

1. 资产选择问题可无歧义地形式化为带基数约束的子模函数最大化 $\max_{|S|\le k} f(S)$，$f$ 为 OR 覆盖。
2. FD 的 greedy / frequency 选择在数学上等价于该问题的标准贪心算法。
3. 该形式化与 677c 的 `evolution_operator`（特别是 `fd_only ≡ greedy`）严格对齐，且承接了「`novel` 分量坍缩」的诚实结论。
4. 形式化的贡献是**提供近似保证**，而非制造「新颖算法」claim——这一点直接驱动 C 节的 Framing 重构。

> 字数说明：本文件正文（不含代码块/表格）约 1500 字；连同 A2 检验报告、A3 近似保证推导、A4 退化资产理论，共同构成「子模优化形式化」的完整交付（任务 A 总字数 ≥ 3000 字，分散在 4 个文件内，本文件为总纲与符号基底）。
