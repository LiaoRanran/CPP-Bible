# OUT 7 MIS 人工复核清单（H1 债务预标注）

> 生成时间：2026-09-20 · 来源：data/grounded_labels_w2.json + data/human_attack_edge_annotations.jsonl
> W2 全量人审后判决：IN114/OUT7/UNDEC0 · OUT 的 7 个 MIS 全部攻击边为 modify（保持 low 置信度）

## 关键发现

这 7 个 MIS 之所以被 W2 判为 OUT（被击败），**不是因为它们的攻击被拒绝**，而是因为它们的所有攻击边都被标记为 **modify**（保持 low 置信度）。

在 W2 可信度加权击败模型中：
- **approve**（升到 medium）：攻击边有足够可信度，可能击败命题
- **modify**（保持 low，默认口径）：攻击边可信度不足，无法击败命题，反而被命题的辩护链击败 ⇒ MIS 被判 OUT

**裁决问题**：这 7 个 MIS 的攻击边是否应该从 modify 改为 approve？
- 如果改为 approve（升到 medium），这些 MIS 可能从 OUT 变为 IN，W2 判决会改变
- 如果保持 modify（保持 low），这些 MIS 继续是 OUT，当前判决不变

## 7 个 OUT MIS 明细

### MIS-LANG-001

- **W2 判决**：OUT（被击败）
- **置信度**：low（credibility=1）
- **攻击边数**：6（全部 action=modify）
- **辩护者**：
- **被击败的攻击者**：
- **裁决建议**：需人审判断该 MIS 的攻击是否真实成立。若真实成立，建议将 modify 改为 approve（升到 medium）；若攻击不成立或证据不足，保持 modify

### MIS-MEM-001

- **W2 判决**：OUT（被击败）
- **置信度**：low（credibility=1）
- **攻击边数**：6（全部 action=modify）
- **辩护者**：MIS-MEM-002, MIS-MEM-004, MIS-MEM-005, MIS-MEM-012, MIS-MEM-017, MIS-MEM-019
- **被击败的攻击者**：
- **为什么 OUT**：被 6 个辩护者（IN 命题/MIS）的辩护链击败；攻击边保持 low 置信度，不足以突破辩护
- **裁决建议**：需人审判断该 MIS 的攻击是否真实成立。若真实成立，建议将 modify 改为 approve（升到 medium）；若攻击不成立或证据不足，保持 modify

### MIS-MEM-003

- **W2 判决**：OUT（被击败）
- **置信度**：low（credibility=1）
- **攻击边数**：6（全部 action=modify）
- **辩护者**：MIS-MEM-002, MIS-MEM-004, MIS-MEM-005, MIS-MEM-012, MIS-MEM-017, MIS-MEM-019
- **被击败的攻击者**：
- **为什么 OUT**：被 6 个辩护者（IN 命题/MIS）的辩护链击败；攻击边保持 low 置信度，不足以突破辩护
- **裁决建议**：需人审判断该 MIS 的攻击是否真实成立。若真实成立，建议将 modify 改为 approve（升到 medium）；若攻击不成立或证据不足，保持 modify

### MIS-UB-001

- **W2 判决**：OUT（被击败）
- **置信度**：low（credibility=1）
- **攻击边数**：4（全部 action=modify）
- **辩护者**：MIS-CONC-001, MIS-UB-002, MIS-UB-003, MIS-UB-012, MIS-UB-013, MIS-UB-015
- **被击败的攻击者**：
- **为什么 OUT**：被 6 个辩护者（IN 命题/MIS）的辩护链击败；攻击边保持 low 置信度，不足以突破辩护
- **裁决建议**：需人审判断该 MIS 的攻击是否真实成立。若真实成立，建议将 modify 改为 approve（升到 medium）；若攻击不成立或证据不足，保持 modify

### MIS-UB-004

- **W2 判决**：OUT（被击败）
- **置信度**：low（credibility=1）
- **攻击边数**：4（全部 action=modify）
- **辩护者**：MIS-CONC-001, MIS-UB-002, MIS-UB-003, MIS-UB-012, MIS-UB-013, MIS-UB-015
- **被击败的攻击者**：
- **为什么 OUT**：被 6 个辩护者（IN 命题/MIS）的辩护链击败；攻击边保持 low 置信度，不足以突破辩护
- **裁决建议**：需人审判断该 MIS 的攻击是否真实成立。若真实成立，建议将 modify 改为 approve（升到 medium）；若攻击不成立或证据不足，保持 modify

### MIS-UB-008

- **W2 判决**：OUT（被击败）
- **置信度**：low（credibility=1）
- **攻击边数**：4（全部 action=modify）
- **辩护者**：MIS-CONC-001, MIS-UB-002, MIS-UB-003, MIS-UB-012, MIS-UB-013, MIS-UB-015
- **被击败的攻击者**：
- **为什么 OUT**：被 6 个辩护者（IN 命题/MIS）的辩护链击败；攻击边保持 low 置信度，不足以突破辩护
- **裁决建议**：需人审判断该 MIS 的攻击是否真实成立。若真实成立，建议将 modify 改为 approve（升到 medium）；若攻击不成立或证据不足，保持 modify

### MIS-UB-014

- **W2 判决**：OUT（被击败）
- **置信度**：low（credibility=1）
- **攻击边数**：4（全部 action=modify）
- **辩护者**：MIS-CONC-001, MIS-UB-002, MIS-UB-003, MIS-UB-012, MIS-UB-013, MIS-UB-015
- **被击败的攻击者**：
- **为什么 OUT**：被 6 个辩护者（IN 命题/MIS）的辩护链击败；攻击边保持 low 置信度，不足以突破辩护
- **裁决建议**：需人审判断该 MIS 的攻击是否真实成立。若真实成立，建议将 modify 改为 approve（升到 medium）；若攻击不成立或证据不足，保持 modify

## 裁决影响预估

如果将这 7 个 MIS 的全部攻击边从 modify 改为 approve（升到 medium）：
- W2 判决可能从 IN114/OUT7 变为 IN121/OUT0（所有 MIS 都变为 IN）
- 这意味着没有任何误解被判定为'被击败'，论证框架的区分度下降
- 建议**不要全部改为 approve**，而是逐条人审，只对真实成立的攻击改为 approve

## 人审操作指南

1. 逐条阅读每个 MIS 的攻击边（见 data/human_attack_edge_annotations.jsonl）
2. 判断该攻击是否真实成立（即该 MIS 是否真的驳斥了对应命题）
3. 若真实成立：使用 attack_edge_review.py approve 命令将 modify 改为 approve
4. 若不成立或证据不足：保持 modify
5. 全部裁决后，重新运行 weighted_af_solver.py 生成新的 W2 判决

## 注意

- 这是人审权力，系统不自动裁决
- modify 口径冲突（keep-low vs upgrade-medium）是 610 发现的 P0 待裁决项，本清单按默认 keep-low 口径分析
- 建议先裁决 modify 口径冲突，再做 OUT 复核
