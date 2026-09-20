# grounded 标注实测与对照报告（596 任务3 · W2 模型）

> **只读生成**：`.venv\Scripts\python.exe tools\grounded_audit.py`（`--check` 校验本文件与事实源一致）。
> 数据源：`data/grounded_labels_w2.json`（`weighted_af_solver.py solve` 的派生结果）+ 卡面 `claim_structured` + `data/attack_edges_candidates.jsonl`。
> 本文件是**人审清单**，不参与任何判决；异常项以 ❌ 标出，出现异常时生成器 exit 2（fail-loud）。

## §1 grounded 标注总览

- 节点 **121** = 命题 79 + 误解 42
- **IN 114 / OUT 7 / UNDEC 0**（in_propositions 79 · in_misconceptions 35）
- 击败边 17/388 · 不动点 **3 轮**收敛（上限 100）
- 模型 `W2_credibility_weighted_grounded` · 可信度档 {'high': 3, 'low': 1, 'medium': 2}

## §2 与 `claim_type` 对照

| claim_type | 节点数 | IN | OUT | UNDEC |
|---|---|---|---|---|
| inference | 29 | 29 | 0 | 0 |
| observation | 50 | 50 | 0 | 0 |

## §3 与 replay verdict 对照

来源：**build/replay_manifest.json（replay 实跑，56 张）**（实测 refute=0）

| 引用卡 replay 归类 | 节点数 | IN | OUT | UNDEC |
|---|---|---|---|---|
| confirm | 79 | 79 | 0 | 0 |

MIS 侧对照（误解的 `refutations` 条数 vs 其 grounded 判决——误解全部 OUT，与其被多少条命题反驳无关，判决由可信度决定）：

- 误解 `refutations` 条数分布：{1: 2, 2: 28, 3: 9, 4: 3}

## §4 辩护链示例（按攻击者数量取前 3 个 IN 命题）

- 命题 `ATOM-UB-GRAY-001::prop-1`（observation，可信度 2）判 **IN**：它击败了全部 10 个攻击它的误解（严格可信度优势）
  - 攻击者 `MIS-CONC-001`（误解，可信度 2）判 **IN**：被 0 条命题击败，如 `（无）` 等
  - 攻击者 `MIS-UB-001`（误解，可信度 1）判 **OUT**：被 2 条命题击败，如 `ATOM-UB-GRAY-001::prop-1` 等
  - 攻击者 `MIS-UB-002`（误解，可信度 2）判 **IN**：被 0 条命题击败，如 `（无）` 等
  - 攻击者 `MIS-UB-003`（误解，可信度 2）判 **IN**：被 0 条命题击败，如 `（无）` 等
  - 攻击者 `MIS-UB-004`（误解，可信度 1）判 **OUT**：被 2 条命题击败，如 `ATOM-UB-GRAY-001::prop-1` 等
  - 攻击者 `MIS-UB-008`（误解，可信度 1）判 **OUT**：被 2 条命题击败，如 `ATOM-UB-GRAY-001::prop-1` 等
  - 攻击者 `MIS-UB-012`（误解，可信度 2）判 **IN**：被 0 条命题击败，如 `（无）` 等
  - 攻击者 `MIS-UB-013`（误解，可信度 2）判 **IN**：被 0 条命题击败，如 `（无）` 等
  - 攻击者 `MIS-UB-014`（误解，可信度 1）判 **OUT**：被 2 条命题击败，如 `ATOM-UB-GRAY-001::prop-1` 等
  - 攻击者 `MIS-UB-015`（误解，可信度 2）判 **IN**：被 0 条命题击败，如 `（无）` 等

- 命题 `ATOM-UB-GRAY-001::prop-2`（inference，可信度 2）判 **IN**：它击败了全部 10 个攻击它的误解（严格可信度优势）
  - 攻击者 `MIS-CONC-001`（误解，可信度 2）判 **IN**：被 0 条命题击败，如 `（无）` 等
  - 攻击者 `MIS-UB-001`（误解，可信度 1）判 **OUT**：被 2 条命题击败，如 `ATOM-UB-GRAY-001::prop-1` 等
  - 攻击者 `MIS-UB-002`（误解，可信度 2）判 **IN**：被 0 条命题击败，如 `（无）` 等
  - 攻击者 `MIS-UB-003`（误解，可信度 2）判 **IN**：被 0 条命题击败，如 `（无）` 等
  - 攻击者 `MIS-UB-004`（误解，可信度 1）判 **OUT**：被 2 条命题击败，如 `ATOM-UB-GRAY-001::prop-1` 等
  - 攻击者 `MIS-UB-008`（误解，可信度 1）判 **OUT**：被 2 条命题击败，如 `ATOM-UB-GRAY-001::prop-1` 等
  - 攻击者 `MIS-UB-012`（误解，可信度 2）判 **IN**：被 0 条命题击败，如 `（无）` 等
  - 攻击者 `MIS-UB-013`（误解，可信度 2）判 **IN**：被 0 条命题击败，如 `（无）` 等
  - 攻击者 `MIS-UB-014`（误解，可信度 1）判 **OUT**：被 2 条命题击败，如 `ATOM-UB-GRAY-001::prop-1` 等
  - 攻击者 `MIS-UB-015`（误解，可信度 2）判 **IN**：被 0 条命题击败，如 `（无）` 等

- 命题 `ATOM-MEM-MOVE-002::prop-1`（observation，可信度 2）判 **IN**：它击败了全部 8 个攻击它的误解（严格可信度优势）
  - 攻击者 `MIS-MEM-001`（误解，可信度 1）判 **OUT**：被 3 条命题击败，如 `ATOM-MEM-MOVE-002::prop-1` 等
  - 攻击者 `MIS-MEM-002`（误解，可信度 2）判 **IN**：被 0 条命题击败，如 `（无）` 等
  - 攻击者 `MIS-MEM-003`（误解，可信度 1）判 **OUT**：被 3 条命题击败，如 `ATOM-MEM-MOVE-002::prop-1` 等
  - 攻击者 `MIS-MEM-004`（误解，可信度 2）判 **IN**：被 0 条命题击败，如 `（无）` 等
  - 攻击者 `MIS-MEM-005`（误解，可信度 2）判 **IN**：被 0 条命题击败，如 `（无）` 等
  - 攻击者 `MIS-MEM-012`（误解，可信度 2）判 **IN**：被 0 条命题击败，如 `（无）` 等
  - 攻击者 `MIS-MEM-017`（误解，可信度 2）判 **IN**：被 0 条命题击败，如 `（无）` 等
  - 攻击者 `MIS-MEM-019`（误解，可信度 2）判 **IN**：被 0 条命题击败，如 `（无）` 等

## §5 异常检测（fail-loud）

### ❌❌ 异常【必须人审，不得静默通过】❌❌

- ❌ 命题被判 **OUT**（0 条，理论应为 0——命题该全 IN）：[]
- ❌ 误解被判 **IN**（35 条，理论应为 0——误解该全 OUT）：['MIS-CONC-001', 'MIS-CONC-003', 'MIS-HIST-001', 'MIS-HIST-002', 'MIS-HIST-003', 'MIS-MEM-002', 'MIS-MEM-004', 'MIS-MEM-005', 'MIS-MEM-011', 'MIS-MEM-012']
- ❌ **UNDEC** 节点（0 个，理论应为 0——出现即攻击边不完整）：命题 0 / 误解 0；样例 []

## §6 与 594 实证对账

| 指标 | 594 实证 | 本批实测 | 一致？ |
|---|---|---|---|
| IN | 79 | 114 | ❌ |
| OUT | 42 | 7 | ❌ |
| UNDEC | 0 | 0 | ✓ |
| 节点数 | 121（79 命题 + 42 误解） | 121 | ✓ |

另注：**4 条命题没有任何误解攻击**（其所属卡的 MIS 关联记在**原子卡侧** `misconceptions` 字段，本批按任务书只读 MIS 侧 `related_atoms` ⇒ 不产边，偏差 D5）——它们无攻击者 ⇒ 立即 IN，不影响 IN/OUT 总数。

