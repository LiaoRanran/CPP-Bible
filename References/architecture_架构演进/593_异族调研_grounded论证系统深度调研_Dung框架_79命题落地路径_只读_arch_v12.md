# 593 异族调研：grounded 论证系统深度调研 —— 从 Dung 框架到 79 命题落地路径

> 你是异族调研者（seed evolving），不是苦力建设者。任务是探明边界，不是写代码、不是给建设建议。
> 全程只读：不修改 tools/evidence/atoms/Examples/tests/data 任何正式文件；不跑 pytest/poison_drill/mutation_fuzz/tool_integrity --update/git commit|checkout|reset|push；可以跑 git log/status/diff/show/--help/只读 --check/python 只读脚本。
> 产出全落 `C:\CodeLearnling\note\note\C++\CPP-Bible\_arch_v12\`。

---

## 调研背景（本仓现状，先核实再用）

本仓有 79 个命题（inference 29 / observation 50），分布在 27 张原子卡上。命题之间通过 `evidence →` 边（命题引用卡、卡引用命题）形成网络。当前命题状态只有三值：`confirmed / refuted / unverified`，没有"全局可接受集"的概念。

590 异族调研（_arch_v11/）已指出：**命题论证层是差距最大的三处之一**，并推荐 R4 grounded 论证层为"只推三维度"的首选。564 调研（_arch_v7/04）已手搓了 79 命题/51 边的纯标准库论证图原型，并核实 clingo 5.8.2 有 cp313-win wheel 可装。

你的任务是**比 564/590 更深一层**：不是"grounded 是什么"，而是"在本仓 79 命题的具体结构下，grounded 标注会给出什么答案、有多少命题会改变状态、复杂度瓶颈在哪、工具链怎么选"。

---

## 12 个调研维度（逐个探测，允许自主发现第 13 维度）

### 维度 1：Dung 框架语义的可计算性实测
- grounded 语义是 P 类（多项式时间可解）——核实这个结论的来源和精确表述
- preferred / stable 是 NP-完全——核实本仓 79 命题规模下，preferred 扩展的枚举是否实际可行
- complete / admissible 的复杂度
- **关键问题**：79 命题 / ~51 边的图，grounded 标注的实际计算时间是多少？（用纯标准库手搓一个 grounded 求解器，在本仓命题图上实跑）
- 590 提到的 ARGUS UAI 2026 复杂度结果——找到原始论文或一手来源，核实"grounded 是 P 类"的精确证明

### 维度 2：本仓命题图的 grounded 标注实测
- 从 `data/propositions.db` 或 `tools/prop_graph.py` 读取 79 命题和边
- 手搓 grounded 求解器（纯标准库，不装 clingo）：
  - 构建攻击关系（注意：本仓的边是"证据支持"还是"攻击"？需要先定义攻击关系从哪来）
  - **核心发现任务**：本仓当前只有"支持"边（evidence →），没有"攻击"边。grounded 框架需要攻击关系。攻击关系从哪来？
    - 候选 1：命题之间的 refutations 字段（卡面的 `refutations:` 列表）
    - 候选 2：inference vs observation 的类型冲突
    - 候选 3：人工标注的 attack 边（当前不存在）
    - 候选 4：从 mutation 逃逸事件反推（被变异攻破的命题攻击其支持卡）
  - **如实回答**：在当前数据下，能否构造非平凡的攻击关系？如果不能，grounded 标注会退化成什么？（全接受？全不接受？）
- 如果能构造攻击关系，跑 grounded 标注，输出：
  - 79 命题中 in / out / undecided 各多少
  - 与当前 confirmed/refuted/unverified 的对照（有多少命题状态会改变）
  - 最大的 grounded 扩展大小

### 维度 3：攻击关系的来源与可靠性
- 本仓卡面的 `refutations:` 字段——80 条 MIS 误解库中有多少条有 refutations？内容质量如何？
- 564 调研指出"MIS 误解库是字段填满、机器没判真伪的无状态第三态"——核实 refutations 字段的真实性
- 攻击关系的"强度"问题：一条 refutation 是"反驳"还是"质疑"？grounded 框架不区分强度，本仓是否需要加权论证框架（Weighted Argumentation Framework）？
- 外部实证：NEJM AI 2026 RCT（automation bias）、CDSS 负向咨询率——这些如何影响"人审标注攻击边"的可靠性？

### 维度 4：AGM 信念修正与 suspect 级联边界
- 564 调研设计了"AGM 最小改变划 suspect 级联边界"——深入调研 AGM 公理（K*1-K*8）在论证框架中的对应
- 当一条新证据加入时，grounded 扩展的变化量如何度量？
- "suspect 级联"：一条命题被推翻时，多少依赖它的命题会变成 undecided？在本仓 79 命题图上实测最大级联大小
- 最小改变原则：在所有满足新证据的扩展中，grounded 是否天然给出最小改变？还是需要额外的修正算子？

### 维度 5：论证系统工具链调研（Windows 可用性实测）
- **clingo / ASP**：564 已核实 5.8.2 cp313-win wheel 可装。深入调研：
  - clingo 表达 grounded 语义的编码方式（标准编码是什么？）
  - 79 命题的 grounding 时间和 solving 时间实测（如果装了的话；如果没装，只调研不安装）
  - clingo 的 --opt-mode / --enum-mode 对 preferred 扩展枚举的支持
- **Tweety**（Java 论证框架库）：Windows 可用性、API、是否支持 grounded/preferred/stable
- **ConArg**（基于约束编程的论证求解器）：Windows 可用性
- **ArgTools / Dung-O-Matic**：老旧工具的现状
- **Netica / GeNIe**（贝叶斯网络工具，与加权论证框架的关系）
- **关键判断**：本仓应该用哪个？纯标准库手搓 vs clingo vs 其他？给出可判定的选择标准

### 维度 6：论证图的可视化与解释
- grounded 扩展的"为什么"解释：给定一个 in 命题，如何展示它的辩护链？
- 本仓 79 命题图的可视化方案（不是画图，是调研用什么工具/格式）
- argument mapping 工具（Argdown、Rationale、OVA）——是否适合本仓？
- 解释性对人审的价值：NEJM AI 2026 的"automation bias"——如果系统只给结论不给理由，人审会 rubber-stamp。grounded 框架的辩护链天然提供理由，这是否能缓解 automation bias？

### 维度 7：与本仓现有三分类（confirm/refute/infra）的关系
- 本仓 replay 的三分类（confirm / refute / infra_error）与论证框架的 in/out/undecided 是什么关系？
- 能否把 replay 的 confirm 映射为"被辩护"、refute 映射为"被攻击"？
- infra_error（基础设施错误）在论证框架中是什么？（undecided？还是需要第四态？）
- golden_lock 的"恶化/改善"与 grounded 扩展的变化是否一致？

### 维度 8：增量更新与收敛
- 当新卡/新命题加入时，grounded 扩展是否需要全量重算？
- 增量论证求解（incremental argumentation solving）的研究现状
- 本仓的 mutation 批次（569-589）每批都在改变命题图——grounded 标注的收敛速度如何？
- "收敛曲线"能否从 grounded 扩展的变化量来定义？（与 573 的 monotone_convergence 判据对接）

### 维度 9：论证框架的概率/模糊扩展
- 本仓的命题有"置信度"吗？（当前没有，但 C-P 统计上界可以转化为概率）
- 概率论证框架（Probabilistic Argumentation Framework, Li 2011 / Dung & Thang 2010）——是否适合本仓？
- 模糊论证框架（Fuzzy Argumentation）——与 warn 级别的"部分接受"是否对应？
- **关键判断**：本仓需要这些扩展吗？还是纯 Dung 框架足够？给出可判定的解冻信号

### 维度 10：论证框架在代码审查/形式化验证中的应用
- 论证框架在软件验证中的应用（用于"为什么这段代码是对的/错的"的论证）
- 与本仓"原子证据卡"的关系：每张卡是一个论证，卡之间的 refutations 是攻击
- 形式化验证中的"反例引导"（CEGAR）与论证框架的"攻击-辩护"循环是否同构？
- 外部实证：CompCert / seL4 / CakeML 的验证方法论中是否用到论证框架？

### 维度 11：人审在论证系统中的角色与边界
- grounded 扩展是"机器可算的唯一答案"——人审还需要做什么？
- 人审的角色：标注攻击边、裁决 undecided 命题、接受/拒绝 grounded 扩展
- 590 指出"9 异族判官≈2 有效独立票"（arXiv:2605.29800）——人审的"独立性"在论证框架中如何体现？
- 人审 rubber-stamp 的防护：grounded 扩展的辩护链是否足够？还是需要"卡绑定判别题"（564 设计的反 rubber-stamp 护栏）？
- **关键判断**：在单用户阶段，grounded 层能减少多少人审工作量？（79 命题中多少会被机器确定 in/out，多少留 undecided 给人审？）

### 维度 12：落地路径与风险
- 从当前 79 命题到完整 grounded 论证系统，需要几步？每步的前置条件是什么？
- 风险清单：
  - 攻击关系不可靠（refutations 字段质量差）
  - grounded 扩展退化为平凡（全接受或全不接受）
  - 复杂度爆炸（如果误用 preferred/stable）
  - 人审不接受机器结论（automation bias 的反面：automation aversion）
  - 与现有三分类/golden_lock 的语义冲突
- **NDW 分类**：
  - N（现在能做，零 Oracle 风险）：手搓 grounded 求解器、在当前命题图上实测、prop_closure（592 已做）
  - D（攒数据）：攻击边标注、refutations 字段质量提升、人审标注 undecided 命题
  - W（等条件）：clingo 主引擎、preferred/stable 语义、概率/模糊扩展、多判官独立投票

---

## 自由探索（第 13 维度及以上）

明确允许你自主发现 12 维度之外的新维度/新攻击面/新技术/新度量/新范式。不要被清单限制。

可能的方向（仅供启发，不是限制）：
- 论证框架与大语言模型的结合（LLM-as-argument-generator）
- 论证框架的因果解释（counterfactual argumentation）
- 论证框架与知识图谱的融合（本仓有 7 类 KG 边）
- 论证框架在"变异测试"中的应用（用攻击关系指导变异算子设计）
- 论证框架的"强度排序"（不是二值 in/out，而是偏序）

---

## 交付物清单（17 件）

1. `00_总览_grounded论证系统在本仓的落地路径与边界.md`——开头两句话贴回
2. `01_Dung框架语义可计算性实测.md`
3. `02_本仓命题图grounded标注实测.md`（含攻击关系构造的核心发现）
4. `03_攻击关系来源与可靠性.md`
5. `04_AGM信念修正与suspect级联边界.md`
6. `05_论证系统工具链调研_Windows可用性.md`
7. `06_论证图可视化与解释.md`
8. `07_与现有三分类confirm_refute_infra的关系.md`
9. `08_增量更新与收敛.md`
10. `09_概率模糊扩展_是否需要.md`
11. `10_论证框架在代码审查形式化验证中的应用.md`
12. `11_人审角色与边界.md`
13. `12_落地路径与风险_NDW分类.md`
14. `13_自由探索_新维度新攻击面.md`
15. `14_路线图_从现在到grounded层上线.md`
16. `probes/`——只读探针及原始输出（grounded 求解器手搓代码、命题图数据、实测时间）
17. `zero_pollution.md`——git 前后状态自证

---

## 00 总览开头两句话（必须写）

完成 17 件交付物后，在 `00_总览` 开头写两句话贴回：

① **grounded 标注在本仓 79 命题上的实测结果是什么？**（in/out/undecided 各多少？与当前状态对照有多少改变？攻击关系能否构造？）最意外的发现是什么？

② **如果只允许再推 3 个维度就能让 grounded 层从"概念"变"可用"，选哪 3 个、为什么？**

---

## 纪律与边界

- 所有判断附证据（文件路径+行号/命令输出/外部链接+检索日期）
- 区分"已查证"和"一方称"，算不出的明说缺什么，不编数字
- 每个维度的"模型上限态"必须是你自己作为 seed evolving 的真实判断，不要抄 564/590 的旧调研结论
- 发现旧调研错了直接指出来附证据
- 全程只读，产出全落 `_arch_v12/`
- 收尾 `git status` 自证仅新增 `_arch_v12/`
- 外部事实按【一手/一方称】逐条标注，未编造任何编号/数字
