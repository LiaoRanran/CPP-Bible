# 689 · 论文重构蓝图（Refactor Blueprint）

- 生成：2026-10-07｜批次：689 究极重构轮｜执行：CodeBuddy（AI）
- 性质：**结构性重构**（不是换标题保留旧叙事）。依据：外部大模型以 NeurIPS E&D reviewer 标准的两轮评审（结论 Weak Reject → 重构蓝图），以及 683–688 各批次的实测产物。
- 输入（只读）：`research/latex/queyi_neurips2027_v1.1.tex`（2120 行 / 35 页 / 687 合并版）、`data/683_*`、`data/684_*`、`data/685_*`、`data/686_*`、`data/688_*`、`data/current_numbers.json`、`data/blindspot_676g_detection_matrix.json`、`data/683_real_world_detection_matrix.json`。
- 本批新增统计：`data/689_equivalence_test.*`、`data/689_standardized_analysis.*`、`data/689_environment_metrics.*`（脚本 `tools/equivalence_689.py`、`tools/environment_metrics_689.py`）。

---

## 1. 为什么要重构（评审结论摘要）

当前 v1.1 的题名承诺"Evolving Verifiers"，但可执行演化算子相对 frequency/fd_only/set-cover greedy 选择：
- 自造语料 16+16 配置消融：`fd_only ≡ set-cover greedy` **14/14 块严格同选**（＝oracle 上界 56.0071%）；literal 模式下 novel≡failure 是数学等价；3/14 (pool,k) 档胜出、最佳 +1.41pp、**p=0.302 不显著**（683-C1）；
- 真实靶场 k=1..7：算子选择与 FD 贪心**完全一致，Δ=0.0pp**（688-B）；
- +24.03pp 的"选择增益"在剔除退化资产后 = 池构成效应（677c：k=4 单点口径全部来自池构成，均值口径约 +12.8pp；k≤3 幸存 +7.4–11.3pp）。

⇒ 评审建议：**不要花力气证明演化有效；删性能声明；把"演化假设失败"变成审计发现；论文重构为"Auditing the Evaluator"**。E&D 明确把严谨负面结果纳入 scope。

**重构后的中心假设（论文的一级主张）**：
> 一个看似令人信服的评估结果，在评估器本身被审计后能否幸存？
> 评估设备可以在**无恶意行为**下产生科学上误导性的结论——通过口径漂移、退化资产、环境依赖、标签错误、测量对象未控变化；Queyi 是一个可执行的审计框架，用于系统性地暴露这些失败。

**三个贡献（严格 3 条，评审指定口径）**：
- C1 可执行的**评估器审计协议**（claim 声明 / 8 类失败模式 / 证伪流程 / 四态审计结果）——§3；
- C2 对一套软件验证设备（C++ 断言检测器组合）的**系统性实证审计**：1147 自造 + 110 真实 CVE 重构样本、clone-aware、环境 profile——§4–§5；
- C3 **哪些结论在对抗性控制下幸存或崩塌的定量发现**（5 个发现，含 1 个阴性发现）——§5。

**不再出现在贡献列表**：演化算子（降为 Finding 5）、子模形式化（降为附录工具 + Finding 5 的解释机制）。

---

## 2. 新旧结构映射表

旧文本（v1.1）→ 新文本（v1.4 reframed）：动作 = **【重写】【压缩】【迁移】【新增】【删除】**

| 旧位置（v1.1 行号） | 内容 | 新位置 | 动作 | 来源/理由 |
|---|---|---|---|---|
| L64 题名"Evolving Verifiers…" | 标题 | 新题名"Auditing the Evaluator: Stress-Testing Evidence-Based Software Verification" | 【重写】 | 评审 P0 |
| L76–101 摘要 | 4 贡献 + 性能叙事 | §0 摘要 | 【重写】 | 新 3 贡献 + 5 发现 + TOST 如实 |
| L104–175 §1 Introduction | 生成/验证不对称 + 4 贡献 | §1 Introduction | 【重写】 | 开场问题改为审计句式；贡献 4→3 |
| L177–222 §2 Related Work | 6 段 | 附录 A11（更新）+ §1 末段 1 句定位 | 【迁移+压缩】 | 新 8 节结构不含 Related；补 DeepFact/Who Grades/Self-Evolving/SV-COMP |
| L225–301 §3 Problem Definition | formalization + 四态 + 19 威胁 | §2 What is Being Evaluated? | 【重写+重组】 | measurement tuple (x,a,e,θ,p,v) + EnvironmentProfile + 观测函数 V；19 威胁→附录 |
| L245–266 fig:belnap | Belnap 方阵图 | §2 保留（缩小） | 【保留】 | 四态仍是核心 |
| L280–301 十九威胁 + 7 焦点威胁 | 威胁枚举 | 附录 A2（全文）+ §7 摘要 | 【迁移】 | 正文 §7 只留 5 类威胁 |
| L304–399 §4 Method | 架构/四态/gate/provenance/reconciler/失败驱动回路/子模/e-process/VC/EE | §3 Audit Protocol（新核心）+ §2（机制）+ 附录 | 【重组】 | 演化回路改为"审计对象与协议"的从属机制；子模/e-process/规则细节→附录 |
| L379–386 子模形式化 | 独立贡献 | 附录 C.7（并入 operator ablation 节） | 【降级】 | 评审：降为工具，解释"演化复杂策略不必要" |
| L393–399 VC 73.8% + EE 1.9pp/rule | 描述性指标 | **删除** | 【删除】 | 评审 P1：工程遥测非科学证据 |
| L402–419 §5 Evaluation Protocol | D0–D4/基线/ablation/指标 | §4 Experimental Design | 【压缩】 | 细节移附录；static 改名 calibration arm |
| L422–579 §6 Experiments（E1–E10） | 结果叙事 | §5 Findings（按失败假设重组）+ §4 | 【重写】 | 5 发现结构；E9→观察性对比；E10→Finding 4 的证据 |
| L462–473 E1 三臂对比 | static/random 对比 | §4（calibration arm 定位）+ §5.1 | 【重写】 | 删除性能对比强调，保留方向性说明 |
| L528–552 E4/A5 | +24pp 全池 | §5.1（审计发现） | 【重写】 | "+24pp 是池构成，不是算法聪明" |
| L553–559 E5 McNemar | 统计 | 附录 C.1（统计节） | 【迁移】 | 正文只留 TOST + 结构化结论 |
| L561–566 E7/E8 LLM/锚 | 负结果 | 附录 A13 | 【迁移】 | 保留为负结果 |
| L568–573 E9 外部对比 | FD vs clang-tidy/cppcheck | §5（观察性对比）+ 附录 C.5 | 【重写】 | 改为 observational / convergent validity |
| L575–579 E10 真实靶场 | 59.09%、p=0.60 | §5.4 + 附录 C.2/C.3 | 【重写】 | 停止 p=0.60 承担"等价"；上 TOST+标准化 |
| L582–598 §7 Analysis（5 条） | 分析 | 吸收进 §5 Findings | 【重组】 | 5 条发现重排为 5 个失败假设 |
| L601–638 §8 Threats | 19 威胁 + 5 层 | §7 Threats（5 类：T1–T5）+ 附录 A2 | 【重组】 | 按 label/external/environment/clustering/detector-scope 五类 |
| L641–653 §9 Claim Boundary | C0 | §7 末（并入）+ 附录 tab:claim | 【压缩】 | 与威胁合并 |
| L656–673 §10 Conclusion | 四机制 + next | §8 Conclusion | 【重写】 | 不写"we built an evolving verifier" |
| L684–2120 附录 A1–A26 | 26 节 | 附录 A 区 + 新 C 区 | 【手术】 | 保留数据权威块；新增 C.1–C.7；编号问题用 subsection 解决 |

**新正文结构（8 节）与页数预算**（正文 ≤9 页硬约束；目标 p.1–8.5）：

| 节 | 标题 | 页预算 | 关键内容 |
|---|---|---|---|
| §1 | Introduction | ≤1 页 | 开场问题 / 中心假设 / 3 贡献 / 不 claim 清单（1 句） |
| §2 | What is Being Evaluated? | ≤1.2 页 | measurement tuple；四态；EnvironmentProfile；V(x,a,e,θ)；measurement_context_id；"verdict without caliber is not a complete observation" |
| §3 | The Evaluator-Audit Protocol | ≤1.8 页 | claim 声明 Q=(D,A,E,Θ,P)；8 失败模式；证伪流程（完整走一遍"+24pp"）；4 审计结果 |
| §4 | Experimental Design | ≤1 页 | datasets / blind holdout discipline / source-derived corpus 命名 / environments / baselines（static=calibration arm）/ 统计口径 / 预注册审计决策 |
| §5 | Findings: What Survives an Audit? | ≤3 页 | F1–F5（见 §3 映射） |
| §6 | Synthesis: Five Rules | ≤0.5 页 | R1–R5 + 可迁移性 |
| §7 | Threats to Validity | ≤0.7 页 | T1–T5 + 五层残差表指针 |
| §8 | Conclusion | ≤0.4 页 | 结论句 + future work 6 项精简 |

---

## 3. 五个发现（Findings）的组织与措辞

| # | 失败假设（被审计的 claim） | Headline（既定口径） | 数据来源 | 关键措辞红线 |
|---|---|---|---|---|
| F1 | "FD 选择显著优于随机/静态（+24pp）" | +24.03pp 全池增益中，退化资产构成贡献单点口径全部、均值口径约 +12.8pp；机制级效应 +7.4–+11.3pp（k≤3），k=4 归零是选集碰撞（P=0.2） | 676f/677b/677c/682/688 | 不把 +24pp 当胜利；"a seemingly very large evaluator improvement was substantially an artifact of measurement-pool composition" |
| F2 | "仪器能测它声称能测的" | 38.4% 盲区（instrument-boundary 口径）；13/34 类型 >50% 盲；家族金字塔 memory 15.7%→link/ODR 67.7%；严重度不预测；41.5% 捕获押在单资产，asan 独占 18；移除 asan 59.09%→42.73% | 681/676g/683/688 | 每处带 instrument-boundary 限定；是 major finding 不是 limitation |
| F3 | "环境只是复现细节" | WSL→native：59.09%→23.64%（−35.45pp），Δunknown=0（静默退化、guard 绿）；跨工具链 clang↔g++ 93.5%（κ=0.864）；三组件指标 | 683-B1/B2、688、`689_environment_metrics` | "environment is part of the measurement"；native 部分标架构推断 |
| F4 | "合成语料与真实缺陷等价（p=0.60）" | TOST（±10pp）**未通过**（90% CI [−10.61,+5.52]，p_TOST=0.064，最小通过 margin 10.61pp）；正向标准化差异 −17.92pp ⇒ **整体率相似是构成抵消**；命名纠正 source-derived reconstruction ≠ naturalistic | `689_equivalence_test`、`689_standardized_analysis`、683、688 | 不称"等价/无差异"；"not significantly different, CI wide, structure differs by family" |
| F5 | "演化算子提供召回增益" | 算子≡fd_only≡set-cover greedy（14/14 块）；真实靶场 k=1..7 Δ=0；3/14 档 p=0.302；"+Δ 来自退化资产"已由 F1 独立解释 | 683-C1、688-B、677c | 不道歉："The apparent need for sophisticated evaluator evolution can disappear once the evaluator-selection problem is correctly formalized."；保留治理价值 |

---

## 4. 硬伤修复清单（P0/P1 汇总，执行时逐条勾）

### P0（必须修）
- [ ] 题名移除"Evolving Verifiers"→ 新题名（全篇/材料/arXiv 同步）
- [ ] 演化算子删除性能 claim；"演化假设失败"成为 Finding 5
- [ ] 公式修正：`E[J]=kd/n` → `E[J]=k·d/|A|`；`Δ≈c·kd/n` → `Δ≈c·k·d/|A|`（L2043；`d`=退化资产数、`|A|`=资产池规模，符号全篇统一）
- [ ] TODO 占位符清零（L721–725 `tab:e4` A0–A4 → 填入真实结果或删除该表）
- [ ] 18/70 残留清零（L890 → 13/34）
- [ ] static → "static calibration arm"（删性能对比统计强调）
- [ ] p=0.60 不得称等价 → TOST 结果 + 标准化分析
- [ ] κ=0.727/0.77 全文 5 处明确 "AI self-consistency, NOT human IAA"
- [ ] Merkle 表述 → "tamper-evident current-state integrity + partial historical reproducibility" + 威胁模型（同一方控制工件与根可重写重算）
- [ ] 环境依赖从"复现细节"升为 measurement tuple 正式组件
- [ ] E9 改为观察性/收敛效度对比，不 claim superiority
- [ ] 1137/1147 脚注（687 已修）逐处核实
- [ ] 页脚 NeurIPS 2025 字样处理（模板占位声明；改注释/检查是否可安全调整）
- [ ] 贡献列表 4→3
- [ ] 子模公式降级为附录工具

### P1（应该修）
- [ ] 删除 Verifier Coverage 73.8%（L85/394/888/1122 + 注释）
- [ ] 删除 Evolution Efficiency 1.9pp/rule（L397/888）
- [ ] e-process 压缩为附录 subsection（L390–391 保留 1 句指针）
- [ ] 67 规则/452 事件细节移附录（已多在附录，正文指针化）
- [ ] Belnap 形式化移附录（正文保留图 + 1 句）
- [ ] 工程事故日志移附录（已在附录 A18，正文指针化）
- [ ] 相关工作补 DeepFact / Who Grades the Grader / Self-Evolving Agents / SV-COMP（联网核验）

---

## 5. 统计与实验方案（本批产物索引）

| 产出 | 文件 | 要点 |
|---|---|---|
| TOST | `data/689_equivalence_test.json` + `_report.md`；`tools/equivalence_689.py` | ±10pp 主分析 + ±5/7/10/12/15 敏感性 + margin 曲线（m∈[0,15]，步长 0.25）+ deff 保守校正 |
| 标准化 | `data/689_standardized_analysis.json` + `_report.md` | 家族级（8 家族）与类型级（9 类型）双向标准化；回答"分布抵消" |
| 环境三组件 | `data/689_environment_metrics.json` + `_report.md`；`tools/environment_metrics_689.py` | 3 profiles × (catch/unknown/cond recall)；Δ 表；分母病理演示 |
| 环境实验设计 | `data/689_environment_experiment_design.md` | Part 1 实测复算 + Part 2（aware vs unaware）方案+判定标准，标"待执行" |
| 人类标注 | `data/689_human_annotation_protocol.md` + `data/annotation_package/` | 方案 + 材料包 + 统计预案；状态=待执行 |
| 公平对比 | `data/689_fair_comparison_protocol.md` + `data/689_svcomp_positioning.md` | 公平性 8 条 + SV-COMP 差异化定位 |

---

## 6. 执行顺序（本批 5 个提交）

1. **提交 1（A+B）**：蓝图 + 统计脚本与结果（本文件 + 3 组 JSON/报告 + 2 脚本）
2. **提交 2（C）**：人类标注方案 + 材料包
3. **提交 3（D）**：公平对比 + SV-COMP 定位
4. **提交 4（E+F+G）**：论文正文重构 + 附录重构 + 相关工作更新（tex + bib）
5. **提交 5（H+I+J）**：投稿材料 + 验证 + 验收报告

红线遵守：不改 `tools/holdout_reveal_661.py`；不改样本源文件；不改 676f–688 既有产物；不用 force push；全部 DCO；只 add 本批文件；正文 ≤9 页；匿名版不泄身份；数字可追溯；不伪造人类标注；p>0.05 不暗示等价；无 TODO。

---

## 7. 预期效果（对照评审投票预测）

| 维度 | 重构前（v1.1） | 重构后（v1.4 reframed） |
|---|---|---|
| 中心叙事 | 演化验证器（证据不支持） | 审计评估器（证据支持） |
| 贡献列表 | 4 条（含演化/子模） | 3 条（协议/实证/发现） |
| +24pp | 领起胜利数字 | 审计发现（构成效应） |
| 演化假设 | 标题承诺 vs p=0.302 张力 | Finding 5（阴性发现，E&D scope） |
| 外部效度 | p=0.60 暗示等价 | TOST（未过，如实）+ 标准化（−17.92pp 构成抵消） |
| 环境 | 复现细节/limitation | measurement tuple 组件 + Finding 3 |
| 预期评审 | Weak Reject | Solid Weak Accept 路径（评审自述） |
