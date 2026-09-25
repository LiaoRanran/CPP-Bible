# 635 V26-3 · 证据通道字段 + 污染传播演练

## 一、证据通道字段定义

| 通道 | 控制方 | 含义 |
|---|---|---|
| direct_experiment | self | 本系统直接实验观测 |
| standard_textbook | external | 标准/教科书 |
| cppreference | external | cppreference 原文 |
| ai_generated | self | AI 生成 |
| human_review | self | 人审确认 |
| external_audit | external | 外部独立审核 |

## 二、现有 57 张证据卡的通道分布

- 通道：`{'direct_experiment': 6, 'standard_textbook': 23, 'cppreference': 2, 'external_audit': 23, 'human_review': 3}`
- 控制方：`{'self': 9, 'external': 48}`

## 三、污染传播演练

- **演练对象**：`ATOM-CONC-FENCE-001`（诚实：仓库无 `status: disputed/refuted` 的卡，取 623 演练中**暴露过问题的卡**）；
- **下游引用本卡的卡**：2 张 ⇒ `['atoms/conc/ATOM-CONC-LOCK-001.md', 'atoms/conc/ATOM-CONC-RACE-001.md']`
- **taint 建议**：`True`（若 ATOM-CONC-FENCE-001 被判错 ⇒ 引用它的下游卡应标 tainted（需独立来源复核））

### 三阀门检查

| 阀门 | 判断 |
|---|---|
| 独立来源 | ❌ 下游卡多引用同一卡的证据链 ⇒ 无独立来源（同源污染不自动暴露） |
| 必然发现 | ⚠️ 若下游同时被 gate 的 EV 引用规则覆盖则可发现；否则不必然 |
| 善意 | ✅ 无造假动机（内部流水线），属**善意错误**而非投毒 |

## 四、建议的自动污染传播规则

1. **引用即建边**：卡 A 引用卡 B ⇒ 建 `taint_edge(A→B)`；
2. **B 判错 ⇒ A 标 tainted**，且 A 须**独立来源**复核才能清除 tainted；
3. **控制方=external 的通道**（标准/cppreference/外部审计）可用作独立来源；`self` 通道不能自我洗白；
4. 本批**只出规则建议，不改任何判决逻辑**（§零.1）。

## 诚实登记

1. 仓库**无正式 disputed 卡**，演练对象为「演练暴露卡」，如实登记；
2. 通道分类为**内容关键词启发式**；
3. 下游引用计数为**文本级**（非语义引用图）；
4. 本工具**只读**。
