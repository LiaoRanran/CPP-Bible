# 611 E3 · 辩护链推理深化（全图敏感性 · 只读）

> 对每个节点做 demote(压 low) / escalate(升 high) 压力测试，量化其「承重程度」。所有翻转只存在于内存重算，不改仓、不裁决。

## 一、总览

- 节点 **121** 个；有 0 个节点被推翻时会引起其它判决翻转；最大级联 **0** 个节点。
- OUT MIS 升 medium 的聚合影响：翻转 **0** 个节点（详见 §三）。

## 二、承重 Top 10

### demote（压到 low 后翻转的节点数）

| 节点 | 翻转数 |
|---|---|
| `ATOM-CONC-FENCE-001::prop-1` | 0 |
| `ATOM-CONC-FENCE-001::prop-2` | 0 |
| `ATOM-CONC-LOCK-001::prop-1` | 0 |
| `ATOM-CONC-LOCK-001::prop-2` | 0 |
| `ATOM-CONC-RACE-001::prop-1` | 0 |
| `ATOM-CONC-RACE-001::prop-2` | 0 |
| `ATOM-CONC-RACE-001::prop-3` | 0 |
| `ATOM-HIST-AUTOPTR-001::prop-1` | 0 |
| `ATOM-HIST-AUTOPTR-001::prop-2` | 0 |
| `ATOM-HIST-AUTOPTR-001::prop-3` | 0 |

### escalate（升到 high 后翻转的节点数）

| 节点 | 翻转数 |
|---|---|
| `MIS-CONC-001` | 1 |
| `MIS-CONC-003` | 1 |
| `MIS-HIST-001` | 1 |
| `MIS-HIST-002` | 1 |
| `MIS-HIST-003` | 1 |
| `MIS-LANG-001` | 1 |
| `MIS-MEM-001` | 1 |
| `MIS-MEM-002` | 1 |
| `MIS-MEM-003` | 1 |
| `MIS-MEM-004` | 1 |

## 三、OUT MIS 升 medium 的聚合影响（D1 全局版）

- 目标 7 个：`MIS-LANG-001, MIS-MEM-001, MIS-MEM-003, MIS-UB-001, MIS-UB-004, MIS-UB-008, MIS-UB-014`
- 翻转节点 **0** 个：`—`
- 含义：若人审把这些 MIS 的 modify 全部改 approve（升 medium），论证图会按此规模重排；是否采纳是**人审权力**（工具只呈现后果）。

## 四、口径与边界

- 复用 610 B1 `defense_chain.what_if` 全量重算内核（节点级可信度 + W2 grounded）；
- 承重 = 单点压力测试下的级联规模，是「脆弱性」指标而非「重要性」判决；
- **不改仓**：本分析不写 `human_attack_edge_annotations.jsonl` / `grounded_labels_w2.json`。
