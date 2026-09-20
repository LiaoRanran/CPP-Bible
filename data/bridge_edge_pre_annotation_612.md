# 612 A1 · 桥接候选人审预标注（只读 · 建议，不执行人审）

> 三维度：主题相关性（同主题=high）/ 论证关系强度（refutations 词频 Jaccard）/ 分量距离（分量大小）。预标注只是**建议**，最终决策由人审做出；本工具不实际加边、不修数据。

## 一、总览

- 候选 **98** 条；建议置信度：high 38 / medium 60 / low 0
- 建议操作：approve（升 medium）40 · reject（不采纳）58 · modify（升 high）0
- **伪桥接风险**：58 条（主题相关但论证关系弱，加了也不构成击败）

## 二、逐条预标注（节选 Top 30）

| 优先级 | 候选边 | 主题 | 论证 | 分量距离 | 置信度 | 建议操作 |
|---|---|---|---|---|---|---|
| weak | `bridge-MIS-CONC-001->MIS-CONC-003` | high | high | medium | high | approve |
| weak | `bridge-MIS-MEM-001->MIS-MEM-011` | high | medium | medium | high | approve |
| weak | `bridge-MIS-MEM-001->MIS-MEM-013` | high | low | medium | medium | reject |
| weak | `bridge-MIS-MEM-001->MIS-MEM-014` | high | low | medium | medium | reject |
| weak | `bridge-MIS-MEM-001->MIS-MEM-015` | high | low | medium | medium | reject |
| weak | `bridge-MIS-MEM-002->MIS-MEM-011` | high | medium | medium | high | approve |
| weak | `bridge-MIS-MEM-002->MIS-MEM-013` | high | low | medium | medium | reject |
| weak | `bridge-MIS-MEM-002->MIS-MEM-014` | high | low | medium | medium | reject |
| weak | `bridge-MIS-MEM-002->MIS-MEM-015` | high | low | medium | medium | reject |
| weak | `bridge-MIS-MEM-003->MIS-MEM-011` | high | high | medium | high | approve |
| weak | `bridge-MIS-MEM-003->MIS-MEM-013` | high | low | medium | medium | reject |
| weak | `bridge-MIS-MEM-003->MIS-MEM-014` | high | low | medium | medium | reject |
| weak | `bridge-MIS-MEM-003->MIS-MEM-015` | high | low | medium | medium | reject |
| weak | `bridge-MIS-MEM-004->MIS-MEM-011` | high | high | medium | high | approve |
| weak | `bridge-MIS-MEM-004->MIS-MEM-013` | high | low | medium | medium | reject |
| weak | `bridge-MIS-MEM-004->MIS-MEM-014` | high | low | medium | medium | reject |
| weak | `bridge-MIS-MEM-004->MIS-MEM-015` | high | low | medium | medium | reject |
| weak | `bridge-MIS-MEM-005->MIS-MEM-011` | high | low | medium | medium | reject |
| weak | `bridge-MIS-MEM-005->MIS-MEM-013` | high | low | medium | medium | reject |
| weak | `bridge-MIS-MEM-005->MIS-MEM-014` | high | low | medium | medium | reject |
| weak | `bridge-MIS-MEM-005->MIS-MEM-015` | high | low | medium | medium | reject |
| weak | `bridge-MIS-MEM-011->MIS-MEM-012` | high | medium | medium | high | approve |
| weak | `bridge-MIS-MEM-011->MIS-MEM-013` | high | low | low | medium | reject |
| weak | `bridge-MIS-MEM-011->MIS-MEM-014` | high | low | low | medium | reject |
| weak | `bridge-MIS-MEM-011->MIS-MEM-015` | high | low | low | medium | reject |
| weak | `bridge-MIS-MEM-011->MIS-MEM-016` | high | low | medium | medium | reject |
| weak | `bridge-MIS-MEM-011->MIS-MEM-017` | high | low | medium | medium | reject |
| weak | `bridge-MIS-MEM-011->MIS-MEM-018` | high | medium | medium | high | approve |
| weak | `bridge-MIS-MEM-011->MIS-MEM-019` | high | low | medium | medium | reject |
| weak | `bridge-MIS-MEM-011->MIS-MEM-020` | high | low | medium | medium | reject |
| … | 其余 68 条见 JSON / 报告 | | | | | |

## 三、口径与边界

- **只读**：不写 `data/attack_edges_candidates.jsonl`、不修改任何数据文件；
- **不保证成立**：预标注是「可能」的攻击关系，真正成立与否需人审 + replay 证据（见 A2/A3）；
- **伪桥接**：主题相关但论证关系弱的候选，加了也只在结构上连起来，不构成击败（C3 已证加桥判决变化 0）；
- 与 611 C2 同源；论证图一变即须重看。
