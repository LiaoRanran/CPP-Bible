# 611 C2 · 桥接攻击边候选（只读 · 不执行人审）

> 候选生成依据：MIS `related_atoms` 关联 + 主题相似度 + 证据卡关联。候选**只作补边提示**，不写权威边文件、不执行人审。

## 一、总览

- 候选桥接边 **98** 条：strong（共享原子）**0** · medium（共享证据）0 · weak（同主题）98
- 涉及 **7** 对跨分量节点 · 当前图 11 个连通分量（C1 锁定：11 / 最大 80 / 覆盖 66.1%）
- 生成命令：`tools/bridge_edge_candidates.py --write`

## 二、候选明细（节选 Top 30）

| 优先级 | 候选边 | 连接分量 | 共享原子 | 共享证据 | 同主题 |
|---|---|---|---|---|---|
| weak | `bridge-MIS-CONC-001->MIS-CONC-003` | 4↔9 | — | — | 是 |
| weak | `bridge-MIS-MEM-001->MIS-MEM-011` | 8↔10 | — | — | 是 |
| weak | `bridge-MIS-MEM-001->MIS-MEM-013` | 7↔10 | — | — | 是 |
| weak | `bridge-MIS-MEM-001->MIS-MEM-014` | 7↔10 | — | — | 是 |
| weak | `bridge-MIS-MEM-001->MIS-MEM-015` | 6↔10 | — | — | 是 |
| weak | `bridge-MIS-MEM-002->MIS-MEM-011` | 8↔10 | — | — | 是 |
| weak | `bridge-MIS-MEM-002->MIS-MEM-013` | 7↔10 | — | — | 是 |
| weak | `bridge-MIS-MEM-002->MIS-MEM-014` | 7↔10 | — | — | 是 |
| weak | `bridge-MIS-MEM-002->MIS-MEM-015` | 6↔10 | — | — | 是 |
| weak | `bridge-MIS-MEM-003->MIS-MEM-011` | 8↔10 | — | — | 是 |
| weak | `bridge-MIS-MEM-003->MIS-MEM-013` | 7↔10 | — | — | 是 |
| weak | `bridge-MIS-MEM-003->MIS-MEM-014` | 7↔10 | — | — | 是 |
| weak | `bridge-MIS-MEM-003->MIS-MEM-015` | 6↔10 | — | — | 是 |
| weak | `bridge-MIS-MEM-004->MIS-MEM-011` | 8↔10 | — | — | 是 |
| weak | `bridge-MIS-MEM-004->MIS-MEM-013` | 7↔10 | — | — | 是 |
| weak | `bridge-MIS-MEM-004->MIS-MEM-014` | 7↔10 | — | — | 是 |
| weak | `bridge-MIS-MEM-004->MIS-MEM-015` | 6↔10 | — | — | 是 |
| weak | `bridge-MIS-MEM-005->MIS-MEM-011` | 8↔10 | — | — | 是 |
| weak | `bridge-MIS-MEM-005->MIS-MEM-013` | 7↔10 | — | — | 是 |
| weak | `bridge-MIS-MEM-005->MIS-MEM-014` | 7↔10 | — | — | 是 |
| weak | `bridge-MIS-MEM-005->MIS-MEM-015` | 6↔10 | — | — | 是 |
| weak | `bridge-MIS-MEM-011->MIS-MEM-012` | 8↔10 | — | — | 是 |
| weak | `bridge-MIS-MEM-011->MIS-MEM-013` | 7↔8 | — | — | 是 |
| weak | `bridge-MIS-MEM-011->MIS-MEM-014` | 7↔8 | — | — | 是 |
| weak | `bridge-MIS-MEM-011->MIS-MEM-015` | 6↔8 | — | — | 是 |
| weak | `bridge-MIS-MEM-011->MIS-MEM-016` | 8↔10 | — | — | 是 |
| weak | `bridge-MIS-MEM-011->MIS-MEM-017` | 8↔10 | — | — | 是 |
| weak | `bridge-MIS-MEM-011->MIS-MEM-018` | 8↔10 | — | — | 是 |
| weak | `bridge-MIS-MEM-011->MIS-MEM-019` | 8↔10 | — | — | 是 |
| weak | `bridge-MIS-MEM-011->MIS-MEM-020` | 8↔10 | — | — | 是 |
| … | 其余 68 条见 `data/bridge_edge_candidates_611.jsonl` | | | | |

## 三、口径与边界

- **只读**：不写 `data/attack_edges_candidates.jsonl`、不执行人审；候选落库须另行开批；
- **方向未定**：`mis_to_mis` 候选的可能攻击方向（谁攻谁）由人裁定；
- **不保证成立**：关联只说明「可能」有攻击关系，真正成立与否需人审 + replay 证据；
- 与 C1 同源（`argument_audit.detect_isolated_subgraphs` + `defense_chain` 真源）；论证图一变（如真补了桥）即须重看碎片化是否改善（C3）。
