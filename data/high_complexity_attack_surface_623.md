# 623 E1 · 高复杂度带攻击面分析

> 工具：`tools/high_complexity_attack_surface_623.py`（基于 622 E2 Horizon 结论 + 623 A2/R3 实跑数据）

---

## 一、核心结论（复现并坐实 622 E2）

622 E2 Horizon 曲线指出：**高复杂度带（complexity 60-80+/80-100）只触发 warn 级规则**（M9 cross_reference → 仅 `EV-SERVES-EXIST`(warn)，0% 被拦）。
623 A2 实跑**完整复现**该结论：

| 622 E2 指出的"高复杂度带只 warn"规则 | 623 A2 是否命中 | severity |
|---|---|---|
| `EV-SERVES-EXIST` | ✅ 命中 | warn |
| `ATOM-REL-TARGET` | ✅ 命中 | warn |
| `ATOM-REL-UNKNOWN` | ✅ 命中 | warn |

⇒ 高复杂度带"**无 block 级结构规则兜底**"的薄弱点**确凿存在**，攻击面在该带是弱点。

## 二、攻击面量化（623 A2+R3 全量）

| 指标 | 值 |
|---|---|
| gate 规则总数 | 63（block 40 / warn 16 / advice 7） |
| 闭环触达规则 | 26（block 21 / warn 5） |
| 高复杂度带触发的 warn 级规则（薄弱点清单） | `ATOM-REL-TARGET` / `ATOM-REL-UNKNOWN` / `ATOM-VERIFY-REASON` / `CARD-PATH-NOT-CANONICAL` / `EV-SERVES-EXIST` |
| **attack-surface 评分** | **87.5**（高复杂度相关 block 触达 21 / 相关规则 24） |

## 三、薄弱点根因

高复杂度 mutation（H1-H4）主要构造**跨卡引用 / 关系 / 占位符 / 编译链**类攻击，这些攻击面在 gate 里只对应 **warn 级**规则：
- `EV-SERVES-EXIST`：serves 指向不存在目标 → warn
- `ATOM-REL-TARGET` / `ATOM-REL-UNKNOWN`：relations 目标/类型非法 → warn
- 无任何 **block 级**规则在"高复杂度带"对"跨卡引用不一致"说不。

→ 攻击者可构造**复杂度高但仅被 warn 记债、不被阻断**的提交，闭环在该带是"软"的。

## 四、加固建议（指向 E2）

为高复杂度带补 **block 级结构规则**，把上述 warn 级攻击面升格为 block 兜底。623 E2 据此新增 4 条
高复杂度带 block 级规则（见 `data/gate_rules_high_complexity_block_623.yaml`）：
将 `EV-SERVES-EXIST` / `ATOM-REL-TARGET` / `ATOM-REL-UNKNOWN` / `CARD-PATH-NOT-CANONICAL`
在**高复杂度上下文**提升为 block 级（或新增 block 级变体）。

## 五、局限性声明

1. 攻击面评分基于 A2/R3 触达数据，受 gate-only 单卡 field-edit 载体上限影响（见 A5）。
2. "高复杂度相关规则"以 622 E2 三点 + 本批触达 block 规则并集近似，非严格拓扑划分。
3. E2 规则定义为独立规则定义文件，接入 gate_engine.py 属 CORE_TOOLS 改动（铁律禁止），由人审/624 接线。
