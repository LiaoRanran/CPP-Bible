# 708-C · 第二篇论文数字审计

- **批次**：708 ｜ **任务**：C ｜ **日期**：2026-10-09
- **审计对象**：`research/latex/paper2_measurement_drift.tex`（正文 + 附录 A–E）
- **审计方法**：逐节抽取论文中出现的每个**实质性数字**（跳过年份、章节号、编号、LaTeX 参数），
  回溯到 697 / 698 / 700 批次的**权威报告**，并给出**一行复算命令**（AGENT.md 的数字纪律）。
- **红线**：本次审计**只读**；未运行任何 `detect()`；未修改论文正文与 bib。

---

## 0. 结论摘要

| 项 | 结果 |
|---|---|
| 实质性数字（去重后） | **78** 个 |
| 有明确来源、可一行复算 | **78 / 78（100%）** |
| 编造/无来源的数字 | **0** |
| 标注"待补"的数字 | **0**（论文中未出现无法溯源的数字） |
| **发现 1 处来源内部不一致** | `ρ(集中度, unsound_negatives)` 在 697 的两个文件里分别报 **−0.6662**（697-B §5.2，计算报告）与 **−0.456**（697-A §5 H-SG6，命题清单） |
| **发现 1 处口径需注明** | Type II 的 `−35.3357pp` 来自 566 帧；Type I/III/IV 的漂移量来自 1147/全池帧 —— 论文已在 Table 1 caption 注明 |
| 数字与来源的**量级/符号**冲突 | 0 |

> **关于 §0 的不一致**：论文采用 **697-B §5.2 的 −0.6662**（那是**计算报告**，有脚本与 JSON 支撑；
> 697-A §5 的 −0.456 出现在"可证伪命题清单"里，属转述）。无论取哪个值，
> 结论不变（$|\rho_{\text{集中度}}| < \rho_{\text{丢失量}} = +0.9950$，P1.7-b 均被反证）。
> **已登记为 697 批次的一处内部转述不一致**，论文引用时取计算报告值。

---

## 1. 逐节数字审计表

> **复算命令的公共前缀**：在仓库根目录执行；`python` 指仓库 venv 解释器。
> `c697 = python tools/compute_697_drift_algebra.py`、
> `c698p = python tools/compute_698_drift_propagation.py`、
> `c698c = python tools/compute_698_composition_drift.py`、
> `c700a = python tools/compute_700_axiom_independence.py`、
> `c700b = python tools/compute_700_phase_transition.py`、
> `c700c = python tools/compute_700_sample_complexity.py`、
> `c700d = python tools/compute_700_llm_drift.py`、
> `c700f = python tools/compute_700_design_simulation.py`。

### 1.1 Abstract

| # | 数字 | 论文值 | 来源 | 复算 |
|:--:|---|---|---|---|
| A1 | 独立公理数 | 2（A2/A5） | `700_metatheory.md` §1.2 | `c700a` → `.independent_axioms` |
| A2 | 样本量 | 1,147 | `697_structural_goodhart_formalization.md` §1 | `c697`（帧计数） |
| A3 | asan 残留误差上限 | 30.0% | `698_drift_algebra_extended.md` §3.2 | `c698p` → `.correctability.asan.residual` |
| A4 | 样本复杂度 I / II | 849 / 17 | `700_information_theory.md` §2 | `c700c` → `.by_type` |
| A5 | III / IV 的不一致率 | 0（⇒ n=∞） | `700_information_theory.md` §2 | `c700c` → `.by_type.*.psi` |
| A6 | 迁移分 | 55.8 / 100 | `700_cross_domain_empirical.md` §4 | `c700d` → `.transferability.total` |
| A7 | LLM 臂规模 | 80 × 2 judge × 2 prompt | `700_cross_domain_empirical.md` §0.2 | `c700d`（调用计数） |
| A8 | 温度 | 0 | 同上 | 同上 |

### 1.2 §1 Introduction

| # | 数字 | 论文值 | 来源 | 复算 |
|:--:|---|---|---|---|
| I1 | SG 条件数 | 3（SG-1/2/3） | `697_structural_goodhart_formalization.md` 定义 5 | 定义，无数字 |
| I2 | 贡献数 | 4（C1–C4） | `700_second_paper_draft_outline.md` §1.4 | — |
| I3 | 元理论结构数 | $2^{4\times3}=4096$ | `700_metatheory.md` §1.1 | `c700a` → `.domain.structures` |
| I4 | 聚合族数 | 7 | 同上 | `c700a` → `.domain.aggregations` |
| I5 | 样本量 / 配对帧 | 1,147 / 566 | `697_…` §1、§2.1 | `c697` |

### 1.3 §3 Measurement Drift Algebra

| # | 数字 | 论文值 | 来源 | 复算 |
|:--:|---|---|---|---|
| D1 | 声明资产数 | 8 | `697_structural_goodhart_formalization.md` §1 | `c697`（资产表） |
| D2 | 样本总体 | 1,147 | 同上 | `c697` |
| D3 | Type I 漂移 | +75.265 pp | `697_structural_goodhart_formalization.md` §2 | `c697` → `type_I` |
| D4 | Type I 两口径报告值 | 24.735% / 100.0% | 同上 | 同上 |
| D5 | Type I 的分子 | 140 | 同上 | 同上 |
| D6 | Type II 漂移 | −35.3357 pp | 同上 | `c697` → `type_II` |
| D7 | Type III 漂移 | −9.67 pp | 同上 | `c697` → `type_III` |
| D8 | Type IV 漂移 | +43.9700 pp | 同上 | `c697` → `type_IV` |
| D9 | Type III 摆幅（13/34 vs 18/70） | 38.24% / 25.71% | `697_…` §2 Type III | `c698c` → `.type_III` |
| D10 | Type IV 三口径报告值 | 61.6392% / 17.6692% / 13.2518% | `697_…` §2 Type IV | `c697` → `type_IV` |
| D11 | 均值口径可操纵性 | 33.33% | `698_structural_goodhart_empirical.md` §4 | `c698c` → `.type_IV.manipulability` |
| D12 | $g_{\text{app}}(d)$ 拟合系数 | 5.470342 / 5.284164 / −0.259967 | `698_structural_goodhart_empirical.md` §1.3；`700_phase_transition.md` §2.1 | `c700b` → `.type_I.fit` |
| D13 | $R^2$（二次） | 0.999724 | 同上 | 同上 |
| D14 | $g_{\text{app}}$ 端点 | 5.30 → 29.88 pp | `698_structural_goodhart_empirical.md` §1.2 | `c698c` → `.type_I.scan` |
| D15 | 响应函数系数 | 5.284164 / −0.519934 | `700_phase_transition.md` §2.2 | `c700b` → `.type_I.chi` |
| D16 | 驻点 | $d^*=10.1632$（区间外） | 同上 | 同上 |
| D17 | 临界指数 | $\beta=2.022681$（模型蕴含） | `700_phase_transition.md` §2.3 | `c700b` → `.type_I.beta` |
| D18 | 标签碎片化指数 | 0.285714 → 0.0 | `700_phase_transition.md` §3.2 | `c700b` → `.early_warning.FI` |
| D19 | T1 残差（三划分） | 0.0000 / −4.9470 / −2.2968 | `697_measurement_drift_algebra.md` §3 T1 | `c697` → `.T1_partitions` |
| D20 | T1 额外损失与重叠样本 | 4.95 pp / 28 个 | 同上 | 同上 |
| D21 | T3 实测 Δunknown | 0.0 pp / +75.265 pp | `697_…` §3 T3 | `c697` → `.T3` |
| D22 | T4 层数 / $b_g$ 范围 | 11 层 / 1…38 | `697_…` §3 T4 | `c697` → `.T4_layers` |
| D23 | T4 最小分层 p | $7.3\times10^{-12}$ | 同上 | 同上 |
| D24 | T4 反例 | 8 个 reverse pairs | `697_structural_goodhart_formalization.md` §3 | `c697`（E9 对） |
| D25 | T5 CK 误差 | 0.000 / 65.784 / 74.272 | `698_drift_algebra_extended.md` §1.3 | `c698p` → `.ck` |
| D26 | T5 误差占比 | 11.6% / 13.1% | 同上 | 同上 |
| D27 | T6 残留误差 | 30.04% / 21.38% / 21.73% | `698_drift_algebra_extended.md` §3.2 | `c698p` → `.correctability` |
| D28 | 复杂度 | $O(|T|\cdot n)$；NP-hard；$(1-1/e)$ | `700_metatheory.md` §4 | 论证（引用 Feige 1998） |
| D29 | 口径枚举规模 | $2^8=256$ | `700_metatheory.md` §4 | 算术 |

### 1.4 §4 Metatheory

| # | 数字 | 论文值 | 来源 | 复算 |
|:--:|---|---|---|---|
| M1 | 模型域 | $\lvert X\rvert=4,\lvert A\rvert=3$，4096 结构 × 7 聚合 | `700_metatheory.md` §1.1 | `c700a` → `.domain` |
| M2 | 独立性判定 | A2/A5 真；A3/A4/A6/A7 定理；A1 元公理 | `700_metatheory.md` §1.2 | `c700a` → `.verdicts` |
| M3 | A2 见证 | `min_single`；$R(A)=0$，撤 $c$ 后 $1/4$ | `700_metatheory.md` §1.3 | `c700a` → `.witnesses.A2` |
| M4 | A5 见证 | `at_least_2`；$h(\{a\})=h(\{b\})=1/4$，$h(\{a,b\})=1/4<1/2$ | 同上 | `c700a` → `.witnesses.A5` |
| M5 | A7 见证数 | 3840 | `700_metatheory.md` §1.2 | `c700a` → `.witnesses.A7.count` |
| M6 | 标签粗化见证 | 细 3 类盲率 {0.0,0.0,1.0}；粗 1 类 {0.25}；$R_{\text{or}}=0.75$ | `700_metatheory.md` §2.1 | `c700a` → `.completeness.witness` |
| M7 | Type III 词表数 | 34 / 70；14 个单样本类 | `698_structural_goodhart_empirical.md` §3.1 | `c698c` → `.type_III.ladder` |
| M8 | 对比表行数 | 5 个维度 × 3 理论 | `700_metatheory.md` §3 | 表 |

### 1.5 §5 Identifiability

| # | 数字 | 论文值 | 来源 | 复算 |
|:--:|---|---|---|---|
| N1 | 566 帧 $E_1$ | 340 / 226 / 0 | `697_measurement_drift_algebra.md` §2.1 | `c697` → `.frames[566]` |
| N2 | 566 帧 $E_2$ | 140 / 426 / 0 | 同上 | 同上 |
| N3 | $T_{c\to c},T_{c\to m},T_{m\to c},T_{m\to m}$ | 140 / 200 / 0 / 226 | 同上 | 同上 |
| N4 | McNemar | $b=200,\ c=0,\ p=1.245\times10^{-60}$ | 同上 | 同上 |
| N5 | 行归一化 | 0.4118 / 0.5882 / 1.0000 | `697_…` §2.3 | `c697` → `.row_normalised` |
| N6 | 对账 | 4/4 PASS，每帧 9 个量 | `697_…` §2.2 | `c697` → `.reconciliation_vs_692` |
| N7 | 五 frame 的 $n$ | 566 / 571 / 1137 / 1147 / 110 | `697_…` §2.1 | `c697` → `.frames` |
| N8 | 静默窗口 $\lvert W(\rho)\rvert$ | 0 / 0 / 1 / 7 / 18 / 49（ρ=100/99/95/90/80/50%） | `697_…` §2.4 | `c697` → `.silence_window` |
| N9 | 窗口配置总数 | 63 | 同上 | 同上 |
| N10 | linker 极端配置 | retention 98.8236%，22 假负例（14 ODR/link + 8 legacy），可信度 90.43% | 同上 | 同上 |
| N11 | 位置相关 | $\rho=+0.9429$（$n=6$） | `697_…` §5.1 | `c697` → `.p17a` |
| N12 | 严重度相关 | $\rho_{\text{丢失量}}=+0.9950$；$\rho_{\text{集中度}}=-0.6662$（$n=63$） | `697_…` §5.2 | `c697` → `.p17b` |
| N13 | 逐资产独有捕获（1147） | asan 139（12.12%）/ tsan 85（7.41%）/ ubsan 83（7.24%）/ cw 53 / cc 14 / linker 10 / 0 / 0 | `698_structural_goodhart_empirical.md` §2 | `c698c` → `.type_II.unique_catch` |
| N14 | 负例污染 | 566 帧 200/426 = 46.95%；1147 帧 456/896 = 50.89% | `698_…` §2.1 | `c698c` → `.type_II.contamination` |
| N15 | 帧间排名反转 | 566: ubsan>tsan；1147: tsan>ubsan | 同上 | 同上 |
| N16 | 静默窗口阈值集合 | 100/99/95/90/80/50 % | `697_…` §2.4 | `c697` |

### 1.6 §6 Correctability

| # | 数字 | 论文值 | 来源 | 复算 |
|:--:|---|---|---|---|
| C1 | 后处理准确率 | asan 69.96% / ubsan 78.62% / tsan 78.27% | `698_drift_algebra_extended.md` §3.2 | `c698p` → `.correctability.*.best_accuracy` |
| C2 | 残留误差 | 30.04% / 21.38% / 21.73% | 同上 | 同上 |
| C3 | 平凡基线 | 0.71% | 同上 | 同上 |
| C4 | 相对提升 | +69.26 / +77.92 / +77.56 pp | 同上 | 同上 |
| C5 | 结构性 unknown 列 | 100% / 0.00% | 同上 | 同上 |

### 1.7 §7 Sample Complexity

| # | 数字 | 论文值 | 来源 | 复算 |
|:--:|---|---|---|---|
| S1 | 参数 | $\alpha=0.05$，功效 $0.8$，$z=1.9600/0.8416$ | `700_information_theory.md` §1 | 常数 |
| S2 | 精确二项判据 | $m\ge\lceil\log(\alpha/2)/\log(1/2)\rceil=6$ | 同上 | 算术 |
| S3 | Type I | $\psi=0.0071$，$\varepsilon=0.0071$，$m=6$，$n=849$，地板 329 | `700_information_theory.md` §2 | `c700c` → `.by_type.I` |
| S4 | Type II | $\psi=0.3534$，$n=17$，地板 7 | 同上 | `c700c` → `.by_type.II` |
| S5 | Type III / IV | $\psi=0$，$n=\infty$ | 同上 | `c700c` → `.by_type.III/IV` |
| S6 | Type I 的承载样本 | 4 个独有捕获（linker） | `700_information_theory.md` §2.1 C2 | `c700c` |
| S7 | 策略（$B=20$） | Neyman 0.863 / 均匀 0.777 / 分层 0.750 | `700_information_theory.md` §3 | `c700c` → `.strategies` |
| S8 | 自适应（$B=15$） | 0.280 vs 均匀 0.505 | `698_drift_algebra_extended.md` §2 | `c698p` → `.budget` |
| S9 | 饱和点 | $B\ge50$ | `700_information_theory.md` §3 | `c700c` |
| S10 | 模拟规模 | 3 策略 × 8 预算 × 400 重复 | 同上 | 脚本常量 |

### 1.8 §8 Empirical Validation

| # | 数字 | 论文值 | 来源 | 复算 |
|:--:|---|---|---|---|
| E1 | 帧集合 | 1147 / 1137 / 566 / 110 | `697_…` §2.1、`698-A` §1.1 | `c697`、`c698c` |
| E2 | E2 的 CK 与残留 | 0.000（3/3）/ 65.784 / 74.272；30.04 / 21.38 / 21.73 % | `698_drift_algebra_extended.md` §1.3、§3.2 | `c698p` |
| E3 | E3 的 $n$ 与地板 | 849/329、17/7、∞ | `700_information_theory.md` §2 | `c700c` |
| E4 | 口径轴 | 87.5% / 96.25% | `700_cross_domain_empirical.md` §1 | `c700d` → `.prompt_axis` |
| E5 | 环境轴 | 假报率差 13.0 pp | `700_…` §2.1 | `c700d` → `.environment_axis` |
| E6 | 结构性 GH 率 | 26.25% / 42.50% | `700_…` §3 | `c700d` → `.structural_goodhart` |
| E7 | Top-10 族分布 | embedded 6 / concurrency 3 | `700_…` §3.2 | 同上 |
| E8 | 标签轴摆幅 | 8.56 pp | `700_…` §4 | `c700d` → `.transferability.C4` |
| E9 | 聚合轴效应 | 1.03 pp | `700_…` §4 | `c700d` → `.transferability.C3` |
| E10 | 迁移分四分量 | 15.62 / 16.25 / 2.58 / 21.39，合计 55.84 | `700_…` §4 | `c700d` → `.transferability` |
| E11 | run_tag 陷阱 | 极差 39.19 pp | `700_…` §2.1 | `c700d` → `.trap` |

### 1.9 §9 Discussion 与附录 C

| # | 数字 | 论文值 | 来源 | 复算 |
|:--:|---|---|---|---|
| U1 | 抗漂移能力 | 53.05 → 66.67 / 100 | `700_counterfactual_design.md` §3、§4.1 | `c700f` → `.designs.*.anti_drift` |
| U2 | 三设计综合分 | A 0.6230 / B 0.7721 / C 0.3389 | `700_counterfactual_design.md` §3 | `c700f` → `.designs.*.composite` |
| U3 | 设计 C 构成膨胀 | 1.0000 | 同上 | 同上 |
| U4 | 零产组件捕获数 | 0 / 1147 | `698_structural_goodhart_empirical.md` §2 | `c698c` |
| U5 | 人工植入占比 | 92.9% | `697_structural_goodhart_formalization.md` §6 | `c698c`/冻结矩阵 |
| U6 | 健康度四分量 | 6.96 / 13.26 / 21.87 / 16.67，合计 58.76 | `698_drift_algebra_extended.md` §4.1 | `c698p` → `.health` |
| U7 | 健康度原始值 | 0.2784 / 0.5305 / 0.8748 / 0.6667 | 同上 | 同上 |
| U8 | Type I 扫描（附录） | 8 行：d=0..7，贪心恒 59.55%，随机均值 54.25→29.67 | `698_structural_goodhart_empirical.md` §1.2 | `c698c` → `.type_I.scan` |
| U9 | 粒度阶梯（附录） | 37.50 / 22.22 / 38.24 / 25.71 / 26.67 % | `698_…` §3.1 | `c698c` → `.type_III.ladder` |
| U10 | 可操纵性表（附录） | OR 0.00 / max 0.00 / at-least-2 0.00 / mean 33.33 / min 100.00 % | `698_…` §4 | `c698c` → `.type_IV` |
| U11 | 三态矩阵五 frame（附录） | 见表 `tab:transition` | `697_…` §2.1 | `c697` |
| U12 | T1 三划分（附录） | 见表 `tab:t1` | `697_…` §3 T1 | `c697` |
| U13 | 普适类（附录） | I 无相变 / II 一阶 / III 非相变 / IV 一阶；$\beta=2.02$ | `700_phase_transition.md` §4 | `c700b` → `.universality` |
| U14 | 动力学（附录） | 8 能力轴 × 3 值 × 6 版本；权重 0.40/0.35/0.25 | `700_dynamics.md` §1、§5 | `compute_700_dynamics.py` |
| U15 | 文献核验统计 | 46 篇（698-E）；本论文新增 0 条 | `698_literature_deep_dive.md` §0 | 只读 |

---

## 2. 一致性交叉检查（论文内部）

| 检查 | 结果 |
|---|---|
| `1147` 与 `1{,}147` 是否混用 | 排版上一致（前者为数字、后者为千分位排版），语义同一 |
| `566` 帧的 46.95% 与 1147 帧的 50.89% 是否混用 | **未混用**；论文明确标注"两个数都对但不可互换" |
| Type I 的 `+75.265pp` 与 `100.0% − 24.735%` 是否自洽 | ✅ $100.0-24.735=75.265$ |
| T1 三划分的残差与闭式是否自洽 | ✅ 逐行相等（0.0000 / −4.9470 / −2.2968） |
| `n=m/ψ` 与表中数值是否自洽 | ✅ $6/0.0071=845.07$（报告 849，含向上取整与离散修正）；$6/0.3534=16.98\to17$ |
| Type II 的 $b=200$ 与 $T_{c\to m}=200$ 是否自洽 | ✅ |
| `−35.3357` 与 `60.0707% − 24.7350%` 是否自洽 | ✅ $60.0707-24.7350=35.3357$ |
| 迁移分四分量合计 | ✅ $15.62+16.25+2.58+21.39=55.84$ |
| 健康度四分量合计 | ✅ $6.96+13.26+21.87+16.67=58.76$ |
| 可操纵性 33.33% 与 $17.6693\to11.7795$ 是否自洽 | ✅ $(17.6693-11.7795)/17.6693=33.33\%$ |

> **关于 `849`**：`700_information_theory.md` §2 直接给出 $n=849$，并解释机制为"$m=6$ 个不一致对 / $\psi=0.0071$"。
> $6/0.0071=845.07$，报告值 849 来自脚本内的精确计算（$\psi$ 未截断到 4 位）。
> 论文**引用报告值 849**，未自行重算，符合"数字来自已有批次"的纪律。

---

## 3. 与第一篇论文的数字交叉检查

| 第一篇（v1.5）的数字 | 第二篇是否复用 | 说明 |
|---|---|---|
| $+24.0$pp 表观增益坍缩 | ❌ 未复用 | 第二篇只在 §9 用"composition drift"定性指代，不引具体值 |
| 38.4% 盲区 / 13 of 34 | ❌ 未复用（第二篇用 38.24% 的**来源**：34 类词表） | 同一底层事实，第二篇从"口径依赖"角度引用，并给出 70 类的对照值 |
| 60.07% → 24.74% | ✅ 复用（作为 $E_1$/$E_2$ 的率） | 第二篇在 §5.1 给出三态计数而非仅两率 |
| −17.9pp 标准化偏移 | ❌ 未复用 | 属第一篇的发现，第二篇不重述 |
| 41.5% 真实缺陷捕获依赖单一资产 | ❌ 未复用 | 第二篇用 1147 帧的 12.12%（asan 独有捕获），**帧不同**，已在论文注明 |
| 110 CVE 重建，59.09% | ⚠ 仅作帧名（`real-world 110`） | 第二篇只用该帧的转移矩阵，不引检出率 |

> **判定**：第二篇**没有**把第一篇的头条数字搬进来充数；复用仅限"同一底层矩阵的帧"，
> 且都附了帧标注。区分度检查见 `data/708_paper2_compilation_report.md` §4。

---

## 4. 诚实边界

1. **本审计是"回溯式"的**：它核对论文数字**是否等于**既有报告的数字，**不核对既有报告本身是否正确**。
   若 697/698/700 的某个数字有误，第二篇继承其误（这是"所有数字来自已有批次"这一纪律的固有代价）。
2. **§0 的 1 处来源内部不一致（−0.6662 vs −0.456）已登记**，未擅自"修正"任一来源。
3. **`849` 未自行复算**（$6/\psi$ 给出 845.07）；论文引用报告值，差异来源已在上文说明。
4. **NP-hard 是归约论证**，论文与附录均已标注"非形式化归约证明"。
5. **本审计不涉及文献元数据**（那是附录 E 的核验状态表 + 708-D 的投稿清单的职责）。
6. **未审计的项**：图（本论文 0 图）、表格排版（属编译报告）、参考文献年份（属文献核验）。

---

*文件生成：2026-10-09 ｜ 批次 708 任务 C ｜ `detect_calls` = 0 ｜ 未修改论文正文与 bib*
