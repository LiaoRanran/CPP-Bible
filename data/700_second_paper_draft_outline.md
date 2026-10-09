# 700-G · 第二篇论文完整草稿框架

- **批次**：700 ｜ **任务**：G ｜ **日期**：2026-10-09
- **性质**：**详细到每节每段的框架 + 全部实验结果**（不是全文）。
- **上游**：`698_second_paper_prestudy.md`（选题收敛）、`700_metatheory.md`（A）、`700_phase_transition.md`（B）、
  `700_information_theory.md`（C）、`700_cross_domain_empirical.md`（D）、`700_dynamics.md`（E）、
  `700_counterfactual_design.md`（F）
- **红线**：`detect_calls = 0`；**0 处**论文正文/bib 修改。

---

## 1. 论文定位

### 1.1 Title（3 个候选）

| # | 题目 | 侧重 | 风险 |
|:--:|---|---|---|
| **T1** | **Measurement Drift Algebra: When Evaluation Numbers Change but Nothing Measured Does** | 代数 + 结构性 Goodhart 的直觉 | 副标题较长 |
| **T2** | **The Boundary of Evaluator Auditing: Identifiability, Correctability and Sample Complexity of Measurement Drift** | 三条边界（识别性/可纠错性/样本复杂度） | 稍学术化 |
| **T3** | **Structural Goodhart: Measurement Drift Without Optimization Pressure** | 新概念 | 与 Goodhart 文献划界成本高 |

**推荐 T2**：它精确对应本批的三条硬结论（700-A 的不可识别、698-B T6 的可纠错边界、700-C 的样本复杂度），
且**不依赖"首次提出"的叙事**（698-E 已明确不能声称首次）。

### 1.2 Abstract（250 词，草稿）

> Evaluation numbers are treated as facts about the systems they measure. We show that a large class of
> evaluation failures requires **no optimization pressure** at all: the number changes because the
> *caliber* of measurement changed, while the capability being measured does not. We call this
> **structural (passive) Goodhart**, and we build an algebra for it.
>
> We present a seven-axiom system for measurement drift, and prove that only **two** of these are
> genuinely independent: idempotence, commutativity, non-invertibility and observability-stratification
> are **theorems** of the framework, and enumerability is a meta-requirement. We show the system is
> **incomplete**: label-vocabulary drift (Type III) cannot be expressed, and we propose an eighth axiom
> closing the label axis.
>
> We prove three boundary results. (i) **Identifiability**: structural vs. real drift is not decidable
> from paired data alone; under nested calibers it is. (ii) **Correctability**: post-hoc repair is
> possible exactly when the drift acts on the post-measurement layer; acquisition-layer drift requires
> re-measurement, with residual error up to 30.0%. (iii) **Sample complexity**: the paired design is
> *powerless* against label and aggregation drift (discordance rate zero ⇒ infinite samples), while
> component-removal drift costs 849 paired samples versus 17 for environment drift — cost is governed by
> the discordance rate, not the effect size.
>
> We instantiate the framework on a C/C++ verification apparatus (1,147 samples) and, partially, on
> LLM-as-a-judge evaluation, obtaining a migration score of 55.8/100. We release four audited artifact
> families and a counterfactual design study.

### 1.3 核心 claim（一句话）

> **测量漂移是一个有代数结构的对象；它的可识别性、可复合性与可纠错性由口径的层结构决定，
> 而这三条边界决定了评估器审计在原理上能做到什么、做不到什么。**

**必须写的 scope 约束**（与第一篇一致）：
- **不声称**普适（数据来自 C/C++ 验证装置 + 一个 LLM judge 臂）；
- **不声称**"首次提出 Goodhart 变形"（698-E 结论 E1：Manheim–Garrabrant 2018 已有 4 变体分类）；
- **不声称**"首次形式化测量漂移"（698-E 结论 E2：最近邻 = arXiv:2608.24419 的 $S/R$ 剖面）。

### 1.4 贡献声明（4 条）

| # | 贡献 | 证据 |
|:--:|---|---|
| **C1** | **测量漂移代数**：7 公理 + 6 定理（T1–T6），并给出**元理论**：仅 A2/A5 独立，A3/A4/A6/A7 是定理，A1 是元公理；系统不完备（缺 A8） | 700-A |
| **C2** | **结构性 Goodhart 的相变理论**：四型**不属于同一普适性类**；II/IV 是一阶相变，I 无临界点（$\beta$ 为模型蕴含值 2.02），III 非单调 | 700-B |
| **C3** | **审计的信息论下界**：配对设计对 III/IV **功效恒为 0**；Type I 需 849 样本 vs Type II 17；成本由 $\psi$ 主导 | 700-C |
| **C4** | **跨领域实证 + 反事实设计**：LLM 迁移分 55.84/100（聚合轴不可迁移）；设计 B 综合分 0.7721 > 现状 0.6230，且前三条改进**零成本** | 700-D / 700-F |

---

## 2. Related Work（与 698-E 的 46 篇对齐）

| 节 | 段落 | 引用的文献（698-E 编号） | 写法要点 |
|---|---|---|---|
| 2.1 Goodhart 与其变体 | ① 经典根（Goodhart 1975、Strathern 1997）② 4 变体分类（#1 Manheim–Garrabrant）③ 形式化（#2 Majka–El-Mhamdi、#3 Karwowski）④ 过度优化（#4 Gao） | #1–#6 | **必须明确**：全部以"被优化/被利用"为前提 ⇒ 本工作的 SG-3 是**去掉前提**后的子类 |
| 2.2 构念效度与测量不变性 | ① 心理测量学经典（#18 MTMM、#19 Messick、#21 Meredith）② 迁移到 ML（#14 $S/R$ 剖面、#15 NeurIPS 2025 综述、#16、#17） | #14–#21 | **主动划界**：#14 的 $S/R$ 是**概率剖面**（judge 稳不稳），我们回答**可纠错性**（能否事后修） |
| 2.3 不可判定性与检测极限 | ① Rice 定理（#28）② 静态分析不可判定（#25 Landi、#26 Ramalingam）③ 充分性准则的公理排除法（#27 Weyuker） | #25–#28 | 承认 #27 是**方法论先例**（公理排除"完美准则"），我们做的是"完美检测器" |
| 2.4 评估器审计与元评估 | ① 元评估（#35 On Meta-Evaluation、#37 Audit-of-Audits、#38）② judge 可靠性（#39、#40 JudgeBench、#41 RewardBench）③ 报告模板（#45、#46）④ 对抗性审计（#12 HackDetect） | #35–#46 | 五条既有路线 → 我们是**第六条**（口径漂移的代数化） |
| 2.5 与第一篇的关系 | 引用 Queyi（第一篇）作为 **case study** | — | 只引"发现了什么"，**不重述** F1–F5 |

---

## 3. Measurement Drift Algebra（7 公理 + T1–T6）

### 3.1 节的段落级提纲

| 段 | 内容 | 来源 |
|---|---|---|
| §3.1 装置与口径 | 五元组 $M=(D,A,E,\Theta,P)$；口径 $Q$；报告率 $\hat R$ vs 机制量 $R^*$ | 697-A §1 |
| §3.2 漂移生成元与漂移量 | $\tau: M\to M'$，$D_\tau = \hat R(\tau M)-\hat R(M)$；四型分类 | 697-A §2 |
| §3.3 **公理系统** | A1–A7 陈述 | 697-B §1 |
| §3.4 **元理论**（本批新增） | **仅 A2/A5 独立**；A3/A4/A6/A7 是定理；A1 是元公理；**穷举 4096 结构 × 7 聚合**的验证 | **700-A** |
| §3.5 **不完备性与 A8** | 标签粗化的见证（逐样本裁决不变、分组统计变）⇒ 缺 A8（标签轴闭包） | **700-A §2** |
| §3.6 定理 T1 | 超可加性 + 闭式残差 $-\lvert C_A\cap C_L\setminus C_B\rvert/n$；三划分实测吻合 | 697-B §3 |
| §3.7 定理 T2 | 不可逆性 ⇒ 漂移不可事后校正 | 697-B §3 |
| §3.8 定理 T3 | 静默性是 $(\tau,\text{记账})$ 二元组的性质 | 697-B §3 |
| §3.9 定理 T4 | 单向性判据 $c_g=0$（11 层实测） | 697-B §3 |
| §3.10 定理 T5 | 漂移链的 CK 充要条件（嵌套 ⟺ 纯撤除） | 698-B §1 |
| §3.11 定理 T6 | 可纠错边界 + 残留误差（asan 30.04% / ubsan 21.38% / tsan 21.73%） | 698-B §3 |
| §3.12 计算复杂性 | 口径枚举 $O(\lvert T\rvert n)$；结构性不可判定；口径套利 **NP-hard**（最大覆盖归约）+ 贪心 $(1-1/e)$ | **700-A §4** |

### 3.2 表：公理独立性（论文用）

| 公理 | 判定 | 反例聚合 | 备注 |
|:--:|:--:|---|---|
| A1 | **元公理** | — | 约束语言，非结构性质 |
| A2 | **真公理** | `min_single` | 见证：$C_a=C_b=\{0\},C_c=\varnothing$ ⇒ 撤 $c$ 反而升率 |
| A3 | 定理 | 无 | 由 $\tau$ = 列删去直接推出 |
| A4 | 定理 | 无 | 同上 |
| A5 | **真公理** | `at_least_2` | 见证：同结构 ⇒ $h(\{a,b\})=1/4<1/4+1/4$ |
| A6 | 定理 | 无 | 列删去 ⇒ 多对一 |
| A7 | 定理 | 无 | 3840 个见证；等价于 698-B T3 |

---

## 4. Structural Goodhart（4 型 + 相变理论）

| 段 | 内容 | 来源 |
|---|---|---|
| §4.1 定义 SG-1/2/3 | 漂移非零 / 机制量不变 / **无优化者** | 697-A §1 |
| §4.2 四型与实测 | I：$g_{\text{app}}(d)=5.47+5.28d-0.26d^2$（$R^2{=}0.9997$）；II：−35.34pp；III：13/34 vs 18/70；IV：均值口径可被拉低 33.33% | 698-A |
| §4.3 **相变模型**（本批新增） | 控制参数 / 序参量 / 响应函数；**类比而非等同**的声明 | **700-B §1** |
| §4.4 **临界条件与指数** | 驻点 $d^*=10.1632$ **在数据区间之外** ⇒ 观测区间内**无临界点**；$\beta = 2.02$（**模型蕴含**，非独立测量） | **700-B §2** |
| §4.5 **预警指标** | 临界慢化类指标**失效**（增量方差与自相关不升反降）；可用的是**结构性指标**（零产组件数、标签碎片化指数 FI） | **700-B §3** |
| §4.6 **普适性类** | 四型**不属于同一类**（无相变 / 一阶 / 非相变 / 一阶） | **700-B §4** |
| §4.7 与经典 Goodhart 的关系 | 对比表 + "经典处方无效"的推论（可证伪） | 697-A §4 |

---

## 5. Empirical Studies

### 5.1 实验 1 · 四型结构性 Goodhart 的系统演示（**已完成**）

| 项 | 内容 |
|---|---|
| 设置 | Queyi 冻结矩阵：676g（1147）+ A5（1137）+ 692 配对（566）+ 683（110） |
| 方法 | $d{=}0..7$ 注入扫描；8 资产全部 255 个非空子集的精确枚举；5 档粒度阶梯；5 种聚合口径的可操纵性表 |
| **结果** | ① $g_{\text{app}}(d)$：5.30 → 29.88 pp，单调且凹（二次 $R^2 = 0.99972$，优于 684 的线性 $\mathbb{E}[J]$ 模型 0.98955）；② 1137 帧复现 684 的 58.49%/42.52%/15.97pp（贪心**逐位相同**）；③ 逐资产环境敏感度：asan 独有捕获 **139 = 12.12%** 最高；④ 粒度**非单调**（34 类 38.24% vs 70 类 25.71%）；⑤ OR 对掺零产资产**免疫（0%）**，均值口径可被拉低 **33.33%** |
| 分析 | 四型各自有独立的控制轴；**不能用单一"漂移幅度"概括** |

### 5.2 实验 2 · 定理 T5/T6 的验证（**已完成**）

| 项 | 内容 |
|---|---|
| 设置 | A5 evaluation 566 的配对裁决；5 条漂移链（3 嵌套 + 2 非嵌套） |
| **T5 结果** | 嵌套链 CK 最大绝对误差 **0.000**（3/3）；非嵌套链 **65.784 / 74.272**（占 566 的 11.6% / 13.1%），误差**质量守恒**（CK 把样本从 catch→catch 挪到 catch→miss 并凭空造出 miss→catch） |
| **T6 结果** | 被撤 sanitizer 列的**最佳后处理残留误差**：asan **30.04%**、ubsan **21.38%**、tsan **21.73%**；结构性恒 unknown 列残留 **0**（先验已知） |
| 分析 | 生成元层复合恒成立、观测层不可复合 ⇒ **审计者不能用"分段测量 + 矩阵相乘"** |

### 5.3 实验 3 · 跨领域迁移（**部分完成**）

| 项 | 内容 |
|---|---|
| 设置 | **699 未完成** ⇒ 用 692 的 LLM 臂（80 样本 × 2 judge × 2 prompt，温度 0） |
| **结果** | ① 口径轴：prompt 不变性 87.5% / 96.25%；② 环境轴：假报率跨模型差 **13.0 pp**；③ **结构性 Goodhart 率 26.25% / 42.50%**（Top 10 集中在 `embedded` 6 例、`concurrency` 3 例）；④ 标签轴摆幅 8.56 pp；⑤ 聚合轴效应仅 **1.03 pp** |
| **迁移分** | **55.84 / 100** ⇒ 可迁移，但**聚合轴几乎不可迁移（2.58/25）** |
| **本批发现的测量陷阱** | 原始 jsonl **缺 `run_tag`**，靠 token 量级推断轮次 ⇒ 环境轴一致率**极差 39.19 pp** ⇒ **该轴不可靠估计**（改用已发布聚合量） |
| 分析 | 陷阱本身印证 **T6**：获取层元数据缺失**不可事后纠正** |

### 5.4 实验 4 · 信息论下界的验证（**已完成**）

| 项 | 内容 |
|---|---|
| 设置 | 566 配对样本；3 种采样策略 × 8 个预算 × 400 次重复 |
| **结果** | ① **Type III/IV 的 $\psi = 0$ ⇒ 配对设计下 $n = \infty$**；② Type I：$\psi = 0.0071 \Rightarrow n = 849$（KL 地板 329）；③ Type II：$\psi = 0.3534 \Rightarrow n = 17$（地板 7）；④ 策略：$B{=}20$ 时 Neyman（真值）0.863 > 均匀 0.777 > 分层 0.750 |
| 分析 | **成本由 $\psi$ 主导而非 $\varepsilon$**；Type I 比 Type II 难 **50 倍**；**5 步协议的 Step 3 需改写为"双设计"** |

---

## 6. Audit Protocol（5 步 + 信息论下界）

| 段 | 内容 | 来源 |
|---|---|---|
| §6.1 Declare | 口径签名必须扩为 **6 元组** $(D,A,E,\Theta,P,\lambda)$（由 A8） | 700-A |
| §6.2 Enumerate | 8 类失效模式；**穷尽性检查**（不允许留空） | 698-D |
| §6.3 Pair（**需改写**） | **双设计**：样本级配对（I/II）+ **设计级对照**（III/IV，因 $\psi = 0$） | **700-C** |
| §6.4 Quantify | 单向性 $c$ / 静默性 / 效应量 CI / 可纠错判定 / **链式不可复合** | 697-B + 698-B |
| §6.5 Report | R1–R5（口径随附 / 三组件 / 四态 / context_id / 反证条件） | 692 + 698-D |
| §6.6 **成本规划** | $n = m/\psi$；**按"承载样本数"而非"效应量"做预算**；每多一个检测器最多 +0.87 pp | **700-C** |

---

## 7. Discussion

| 段 | 内容 |
|---|---|
| §7.1 三条边界 | 识别性（A1）、可纠错性（T6）、样本复杂度（C）—— **决定了审计能做到什么** |
| §7.2 与第一篇的关系 | 第一篇讲**发现**，第二篇讲**工具**；第一篇的 F1–F5 是本文四型的实例 |
| §7.3 局限 | 单一领域（C/C++）+ 一个 LLM judge 臂；$n_{\text{env}} = 2$；92.9% 人工植入；公理"恒真"结论仅限 4096 结构域 |
| §7.4 未来工作 | ① A8 的形式化；② 非配对设计的样本复杂度；③ 第三环境对（容器）；④ 等边际替换设计；⑤ 跨领域完整实证（JudgeBench/RewardBench） |

---

## 8. Conclusion

> 我们证明：评估数字的改变**不需要任何优化压力**；它由口径的层结构决定。
> 我们给出了这个结构的代数（7 公理，其中只有 2 条独立）、它的三条边界
> （识别性、可纠错性、样本复杂度），并在一台 C/C++ 验证装置与一个 LLM judge 臂上量化了它们。
> 最有实践价值的结论是：**三条最有效的改进（移除零产组件、改用 aware 记账、声明聚合规则）
> 的总成本约为零**，却能把抗漂移能力从 53.05 提到 66.67（满分 100）。

---

## 9. 投稿计划

| 项 | 内容 |
|---|---|
| **目标 venue** | **ICML 2027 / NeurIPS 2027 主会（方法论轨）**；备选 AISTATS / UAI / TMLR |
| **时间线** | **3 个月**（M1 理论收口 + 实验 1/2 成稿；M2 补实验 3/4；M3 写作 + 投稿） |
| **与 698-F 的差异** | 从 6 个月缩短到 3 个月，因为**实验 1/2/4 已完成**（698-A/B + 700-C） |

### 9.1 风险与应对

| # | 风险 | 严重度 | 应对 |
|:--:|---|:--:|---|
| R1 | 被说"给已有做法起名字" | 🔴 | 公理必须**排除**具体做法：A2 排除 min 类口径、A5 排除均值类口径、T6 排除"事后校正" —— 放 **Intro** 而非 §3 |
| R2 | 只有 2 个环境对 | 🔴 | 补容器 profile；拿不到就**主动降级**并写死 |
| R3 | 跨领域只有部分实证（699 未完成） | 🟡 | 如实标注"部分"；用公开榜单做只读分析 |
| R4 | 与 arXiv:2608.24419 撞车 | 🟡 | **主动引用并划界**（概率剖面 vs 可纠错性） |
| R5 | $\beta = 2.02$ 被质疑 | 🟡 | 明确写"模型蕴含值，非独立测量"（700-B §2.3） |
| R6 | 公理"恒真"只在 4096 结构域内验证 | 🟡 | 明确写"域内证据"，不外推 |
| R7 | 与第一篇自我重叠 | 🟡 | 只引"发现了什么"，不重述 F1–F5 |
| R8 | LLM 结论复现期短 | 🟡 | 记录模型快照 id；把"复现期"写成 limitation |

---

## 10. 与第一篇论文的关系图

```
        ┌──────────────────────────────────────────────┐
        │ 第一篇（Queyi）：领域审计案例研究              │
        │ 对象：C/C++ 验证装置                          │
        │ 产出：F1–F5 五个发现 + 四态记账 + context_id  │
        └──────────────────┬───────────────────────────┘
                           │ 作为 case study 被引用（只引"发现了什么"）
                           ▼
        ┌──────────────────────────────────────────────┐
        │ 第二篇：通用方法论                            │
        │ 对象：任意评估器的**口径**                    │
        │ 产出：7 公理（2 独立）+ T1–T6 + 三条边界      │
        │       + 双设计审计协议 + 反事实设计            │
        └──────────────────┬───────────────────────────┘
                           │ 反过来解释第一篇的发现
                           ▼
   F1（+24pp 坍缩）  = Type I 构成漂移（相变：无临界点）
   F3（60%→24.7%）   = Type II 环境漂移（相变：一阶）
   F4（−17.92pp）    = Type III 标签漂移（配对设计不可检出）
   "38.4% 盲区"      = Type IV 聚合口径的后果（可操纵性 33.33%）
```

---

## 11. 诚实边界

1. **本文件是框架，不是全文**；Abstract 是草稿（250 词），各节是段落级提纲。
2. **实验 1/2/4 已完成**（有数据）；**实验 3 只有部分**（699 未完成，用 692 臂）；
   **没有实验是"预期结果"** —— 本批的 §5 全部是**已得结果**。
3. **贡献 C2（相变理论）是本批最弱的一环**：只有 6–8 个数据点，$\beta$ 是模型蕴含值，
   且"相变"是**类比**。**建议在论文中降级为"一个描述性框架"**，而非"理论"。
4. **贡献 C4 的跨领域部分是部分的**：只有 2 个 judge、2 个 prompt、80 个样本。
5. **不声称任何"首次"**（698-E §5.1 三条）。
6. **时间线（3 个月）依赖"实验 1/2/4 已完成"**；若 M2 需要新实验，会拉长。
7. **本文件未做**：投稿信、rebuttal 预案（那需要 697-E 的弹药库 + 700 的新结果，属未来工作）。

---

*文件生成：2026-10-09 ｜ 批次 700 任务 G ｜ `detect_calls` = 0 ｜ 未修改论文正文与 bib*
