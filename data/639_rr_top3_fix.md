# 639 D3 · RR 冲突 top 3 修复报告

> 生成：2026-09-25T10:31:53。方法：**代码级 co-fire 复核**（类型域以 `gate_engine` 常量为准，机器可查）。

## 一、逐对复核（top3）

| 对 | 638 判 | 能否 co-fire | 证明 | 结论 | 处置 |
|---|---|---|---|---|---|
| ATOM-REL-CONFLICT ↔ ATOM-REL-UNKNOWN | P0 | 否 | CONFLICT 域 ['conflicts_with', 'contradicts'] ⊆ KNOWN；UNKNOWN 只在 ∉ KNOWN 触发 ⇒ 域不相交 | 误报（撤销 P0） | 无需改规则 |
| ATOM-REL-DAG ↔ ATOM-REL-UNKNOWN | P0 | 否 | DAG 域 ['evolved_from', 'prerequisite', 'realizes', 'specializes'] ⊆ KNOWN；UNKNOWN 只在 ∉ KNOWN 触发 ⇒ 域不相交 | 误报（撤销 P0） | 无需改规则 |
| ATOM-REL-TARGET ↔ ATOM-REL-CONFLICT | P0 | 是 | 同卡同边可同时触发（构造样例见 JSON） | 真实 co-fire 但无判决歧义：block 支配 warn，门禁终判=block，warn 为附加定位信息 | 维持现状 + 登记支配关系（不改 block，不弱化判决力） |

## 二、机器证明摘要

- `DAG_REL ∪ CONFLICT_REL ⊆ REL_TYPES_KNOWN`：**True**；
- ⇒ (CONFLICT, UNKNOWN) 域不相交：**True**；
- ⇒ (DAG, UNKNOWN) 域不相交：**True**；
- TARGET↔CONFLICT 的 co-fire 构造样例见 JSON（`cofire_example`）。

## 三、结果

- P0：**3 → 0**（两对误报撤销，一对支配关系登记）；
- 24 对高置信中其余 21 对：其余 21 对（type2/type3）留 640；type3 的 -HC 派生即优先级机制本身。

## 四、对 638 B2 的修正

> 638 的 type1 启发式（同前缀族 + severity 相反）**高估**了冲突面：同前缀 ≠ 同一事实。本批以类型域不相交证明撤销 2 个 P0；第三对为真实 co-fire 但 block 支配 warn，无判决歧义。638 报告作为历史产物保留，修正以本报告为准（诚实登记，不回改 638 产物）。
