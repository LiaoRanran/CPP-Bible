# 611 E3 · 辩护链推理深化（全图敏感性 · 只读）

> 对每个节点做 demote(压 low) / escalate(升 high) 压力测试，量化其「承重程度」。所有翻转只存在于内存重算，不改仓、不裁决。

## 一、总览

- 节点 **121** 个；有 107 个节点被推翻时会引起其它判决翻转；最大级联 **1** 个节点。
- OUT MIS 升 medium 的聚合影响：翻转 **7** 个节点（详见 §三）。

## 二、承重 Top 10

### demote（压到 low 后翻转的节点数）

| 节点 | 翻转数 |
|---|---|
| `ATOM-CONC-RACE-001::prop-1` | 1 |
| `ATOM-CONC-RACE-001::prop-2` | 1 |
| `ATOM-CONC-RACE-001::prop-3` | 1 |
| `ATOM-HIST-AUTOPTR-001::prop-1` | 1 |
| `ATOM-HIST-AUTOPTR-001::prop-2` | 1 |
| `ATOM-HIST-AUTOPTR-001::prop-3` | 1 |
| `ATOM-HIST-AUTOPTR-001::prop-4` | 1 |
| `ATOM-MEM-ALIGN-001::prop-1` | 1 |
| `ATOM-MEM-ALIGN-001::prop-2` | 1 |
| `ATOM-MEM-ALIGN-001::prop-3` | 1 |

### escalate（升到 high 后翻转的节点数）

| 节点 | 翻转数 |
|---|---|
| `MIS-MEM-031` | 12 |
| `MIS-MEM-019` | 9 |
| `MIS-MEM-024` | 9 |
| `MIS-MEM-026` | 9 |
| `MIS-MEM-027` | 9 |
| `MIS-MEM-028` | 9 |
| `MIS-MEM-005` | 8 |
| `MIS-MEM-017` | 8 |
| `MIS-MEM-020` | 7 |
| `MIS-MEM-021` | 7 |

## 三、OUT MIS 升 medium 的聚合影响（D1 全局版）

- 目标 7 个：`MIS-LANG-001, MIS-MEM-001, MIS-MEM-003, MIS-UB-001, MIS-UB-004, MIS-UB-008, MIS-UB-014`
- 翻转节点 **7** 个：`MIS-LANG-001, MIS-MEM-001, MIS-MEM-003, MIS-UB-001, MIS-UB-004, MIS-UB-008, MIS-UB-014`
- 含义：若人审把这些 MIS 的 modify 全部改 approve（升 medium），论证图会按此规模重排；是否采纳是**人审权力**（工具只呈现后果）。

## 四、口径与边界

- 复用 610 B1 `defense_chain.what_if` 全量重算内核（节点级可信度 + W2 grounded）；
- 承重 = 单点压力测试下的级联规模，是「脆弱性」指标而非「重要性」判决；
- **不改仓**：本分析不写 `human_attack_edge_annotations.jsonl` / `grounded_labels_w2.json`。
