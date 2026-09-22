# 624 A3 · 「为什么跨卡攻击也 0 逃逸」深度分析（根因分析 v3）

> 工具：`tools/escape_root_cause_v3_624.py`（跨卡 4 维度根因分类 + 0 逃逸四问分析）
> 输入：`data/cross_card_sandbox_run_624.json`（A2 的 60 条真实判决）
> 结论：**escaped 0 条**（无基线 finding 消失）；新触达 2 条；累计 **28/63**。

---

## 一、跨卡 4 维度根因分类

A2 命中规则的跨卡维度归因：

| 跨卡维度 | 命中规则 | 说明 |
|---|---|---|
| **悬空引用绕过** | ATOM-REL-TARGET · EV-SERVES-EXIST · ATOM-ID-UNIQUE · EV-ARTIFACT-FILE-EXISTS · ATOM-REL-UNKNOWN | 规则只查「目标是否存在」，不查引用语义 |
| **循环引用绕过** | ATOM-REL-DAG | 规则只查 DAG 无环，不查环的性质 |
| **矛盾引用绕过** | ATOM-REL-CONFLICT | 规则有共存前置（关系类型+方向） |
| **跨卡引用盲区** | （gate 无专门跨卡规则族） | 需架构层新增检查族 |

## 二、0 逃逸四问深度分析

### Q1 策略覆盖度（生成策略够强吗？）
- 4 策略均生效：60 条 **0 neutral、0 infra_error**；blocked 47 / nonblock 13。
- **但策略命中的规则高度重叠**（见 Q2）⇒ 问题不在"策略不生效"，而在"可触达的规则本就少"。

### Q2 规则覆盖度（gate 规则已覆盖跨卡吗？）
- 本轮触达 13 条，**相对 623 仅新增 2 条**（ATOM-REL-CONFLICT、EV-ARTIFACT-FILE-EXISTS）⇒ 累计 **28/63**。
- **根因**：`gate_engine.py` **没有专门的跨卡一致性规则族**；X1–X4 只能借用既有**引用类**规则
  （ATOM-REL-TARGET/DAG/UNKNOWN、EV-SERVES-EXIST、ATOM-ID-UNIQUE）触发 ⇒ 大部分与被 623 已触达的规则重合。
- 未被触达的跨卡相关盲区（本轮漏）：`ATOM-MISCONCEPTION-REF`、`S2-EVIDENCE-VERDICT`、
  `OBSERVATION-NEEDS-ARTIFACT`、`ATOM-VERIFIED-BOUND`、`INFERENCE-NOT-MACHINE-VERIFIED` ——
  它们分别检查**嵌套字段**（pedagogy.misconceptions）、**证据 verdict 绑定**、**命题-工件闭环**、**verified 绑定**，
  A1 的 4 策略未针对这些字段构造编辑。

### Q3 沙箱限制（多卡备份还原限制攻击了吗？）
- **0 infra_error、0 restore_failed** ⇒ 多卡沙箱机制**工作正常**，**不是**逃逸成因。
- 自检后受控目录零污染 ⇒ 跨卡修改的原子性（失败回滚 + finally 还原 + 逐卡 sha256）可靠。

### Q4 复杂度校准（复杂度评分准吗？）
- 跨卡攻击复杂度均 >60（X1 66 / X2 72 / X3 78 / X4 70）。
- **但复杂度评分是代理值，与「能否触达规则」无单调关系** ⇒ 评分需与规则触达解耦（评分衡量攻击构造难度，
  不衡量攻击是否打中规则）。

## 三、下一轮生成策略改进建议（→ A4 第五轮）

| 新策略 | 目标规则 | 构造方式 |
|---|---|---|
| **X5 幽灵证据引用** | S2-EVIDENCE-VERDICT | 给 verified 原子 `evidence[]` 追加不存在的 EV id ⇒ 「引用的证据卡不存在」 |
| **X6 观测断链** | OBSERVATION-NEEDS-ARTIFACT | 把 observation 命题 `evidence` 指向不存在的卡 |
| **X7 误解引用孤儿（修正）** | ATOM-MISCONCEPTION-REF | 改**嵌套** `pedagogy.misconceptions` 为不存在 MIS id（A2 X4 误改顶层字段故未触发） |
| **X8 verified 未绑定** | ATOM-VERIFIED-BOUND | 删 verified 原子 `first_hand` 或清空 `superiority` |

## 四、修复建议分类（若未来出现逃逸）

`classify_escape` 已实现四类修复建议：**规则修复**（高复杂度带升 block，即 624 B1/E2）·
**证据修复**（补 artifact/provenance）· **卡面修复**（改引用）· **架构修复**（需 gate 跨卡检查族，P0 交人）。

## 五、局限性声明

1. **本批无真实逃逸**，根因分析为「0 逃逸」性质分析，非逃逸归因。
2. **"gate 无跨卡规则族"是观察结论**（基于规则清单 + check 函数阅读），非穷尽证明。
3. 下一轮策略 X5–X8 为**建议**，其有效性以 A4 沙箱实跑为准。
