# 612 B3 · 活性锚补全 what-if（只读 · 假设，不跑 gate）

> **假设**：50 条缺锚 observation 全部补全（A/B 补合格符号 / C 改标 inference）。本工具按规则逻辑静态分析，**不跑 gate**、不改任何文件。

## 一、OBSERVATION-LIVENESS warn 消除预测

| 场景 | 处理条数 | warn 前 | warn 后 | 按类 |
|---|---|---|---|---|
| 全量补全 | 50 | 50 | 0 | {'A': 9, 'B': 26, 'C': 15} |
| --partial 0 | 0 | 50 | 50 | {} |

- 缺锚命题总数 **50**（A 9 / B 26 / C 15）；优先级 A→B→C。
- 每条已处理命题恰消除 1 条 OBSERVATION-LIVENESS warn（该规则对命题单点告警）。

## 二、边界（诚实）

- **只分析 OBSERVATION-LIVENESS 一条规则**：不声称「补全后 gate 一定全绿」；
  C 类改标 inference 后仍可能触发 inference 相关规则（需 gate 实测，本工具不跑）；
- **覆盖率**：OBSERVATION-LIVENESS 非 poison 攻击面上的攻击类型 ⇒ **诚实覆盖率口径不变**（假设，非实测）；
- A/B 类补的符号须真正出现在引用卡的工件断言中，否则 gate 仍报（本工具按「补对」假设）。
