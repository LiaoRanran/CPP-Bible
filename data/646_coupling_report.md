# 646 三层耦合报告（A2，清债 1）

- 耦合链数：**10**（目标 ≥5）
- **证据≠0 的链：10**
- **归因可复核率：1.0**（目标 ≥0.5）
- 打通前（645 token 匹配）：0.0
- 尾端判决分布：{'pass': 10}
- 达成：True

## 逐链（规则 → 匹配卡数 → 证据数 → 判决）
- `ATOM-CLAIM-CONCEPT-NORMALIZED`（low）：卡=27 证据=85 反例=27 → pass
- `EV-MATRIX-UNBACKED`（low）：卡=27 证据=85 反例=27 → pass
- `OBSERVATION-LIVENESS`（low）：卡=27 证据=85 反例=27 → pass
- `EV-OUT-UNDECLARED-KEY`（low）：卡=27 证据=85 反例=27 → pass
- `EV-FALSIFICATION-QUANT`（low）：卡=27 证据=85 反例=27 → pass
- `EV-ASSERT-SYMBOL-MAPPED`（high）：卡=27 证据=85 反例=27 → pass
- `ATOM-REL-TARGET`（low）：卡=24 证据=76 反例=24 → pass
- `EV-ENV-DEPENDENT-KEY`（high）：卡=27 证据=85 反例=27 → pass
- `EV-OUT-STALE-MTIME`（low）：卡=27 证据=85 反例=27 → pass
- `EV-ARTIFACT-PRODUCER`（critical）：卡=27 证据=85 反例=27 → pass
