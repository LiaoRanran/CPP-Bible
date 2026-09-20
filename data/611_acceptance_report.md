# 611 验收报告（收工 · 全绿）

> 完成时间：2026-09-20 · 批号 611 · 关联 `data/611_baseline.md`（任务0 只读基线）
> 口径纪律：所有数字来自 611 各工具同源复算；冻结数据与图结构下可逐字节复算。
> 门禁：`tools/run_611_gate.py` 全绿（exit 0）⇒ 逐工具 `--check` + `metrics_collector` + `tool_integrity --check` + `pytest tests/test_611_tools.py` 全过。

## 0. 任务总览与完成情况

| 线 | 任务 | 状态 | 交付物 | 关键数字 |
|---|---|---|---|---|
| A | A1–A3（verify_append_only 字节前缀 / review_seconds 口径 / PE 时间戳） | ✅（前期批完成） | `supply_chain_verify.py` 等 | 末行无换行文件可字节级追加；人审 0 条 `review_seconds`；PE 跨窗口差 2 字节时间戳 |
| B | B1 modify 双模式 / B2 影响分析 | ✅（前期批完成） | `weighted_af_solver` + `modify_mode_analysis_611.md` | keep-low = 入库权威口径（IN114/OUT7）；upgrade-medium 得 IN121/OUT0 |
| C | C1 连通分量分析 | ✅ | `argument_graph_analysis.py` | **11 分量 / 孤立 4 / 最大 80 / 覆盖 66.1%** |
| C | C2 桥接攻击边候选 | ✅ | `bridge_edge_candidates.py` + `data/bridge_edge_candidates_611.jsonl` | **98 条候选**（strong 0 / medium 0 / weak 98，全为同主题跨分量 MIS 对） |
| C | C3 碎片化修复 what-if | ✅ | `fragmentation_repair_analysis.py` | 加 98 候选 ⇒ 分量 **11→7**、覆盖 **66.1%→80.2%**、**判决变化 0**（候选皆 low，不构成击败） |
| D | D1 OUT 7 MIS 复核支撑 | ✅ | `out_mis_review_support.py` | 7 个 OUT MIS 全员在位；全部攻击边为 modify（保持 low） |
| D | D2 活性锚补全计划 | ✅ | `liveness_completion_plan.py` | 缺锚 observation 命题 **50** 条 |
| D | D3 oracle 验证计划 | ✅ | `oracle_verification_plan.py` | **83 张卡（56 证据 + 27 原子）/ 已验 0** |
| E | E1 metrics_611 | ✅ | `metrics_611.py` + `metrics_collector.py` 挂载 | `metrics_611` 嵌套含 5 类只读指标 |
| E | E2 人审质量深化 | ✅ | `human_review_quality_deepen.py` | 评审者 **1** 人；仅 modify 的 MIS **7**；混合 verdict MIS 数已列 |
| E | E3 辩护链推理深化 | ✅ | `defense_chain_deepen.py` | 节点 121；承重 107；**最大级联仅 1**（图局部稳定，无深度级联） |
| Z | Z1 收工门禁 / Z2 验收报告 | ✅ | `run_611_gate.py` + 本报告 + `outbox/611.md` | 门禁全绿 |

## 1. 各新工具 `--check` 锁定数字（论证图/卡数据冻结前不变）

- C1 `argument_graph_analysis --check`：11 分量 / 孤立 4 / 最大 80 / 覆盖 66.1%
- C2 `bridge_edge_candidates --check`：98 条（strong 0 / medium 0 / weak 98）
- C3 `fragmentation_repair_analysis --check`：加桥后分量 7 / 最大 97 / 覆盖 0.8017 / 判决变化 0
- D1 `out_mis_review_support --check`：7 个 OUT MIS 全部在位
- D2 `liveness_completion_plan --check`：缺锚 observation 命题 50 条
- D3 `oracle_verification_plan --check`：83 卡 / 已验 0 / 证据 56 / 原子 27
- E2 `human_review_quality_deepen --check`：评审者 1 / 仅 modify MIS 7
- E3 `defense_chain_deepen --check`：节点 121 / 承重 107 / 最大级联 1

## 2. metrics_611（新增嵌套指标，不动扁平 27 项）

`metrics_collector --json --no-heavy` 现含 `metrics_611`：
- `argument_graph_fragmentation`：{components:11, isolated:4, largest_size:80, coverage:0.6612, nodes:121, edges:388}
- `bridge_candidates`：{total:98, by_priority:{strong:0, medium:0, weak:98}}
- `out_mis_review`：{out_mis_count:7, …}
- `liveness_missing`：{missing_observation:50, needs_review:0, ok:0, total_observation:50}
- `oracle_verification`：{cards_total:83, verified:0, unverified:83, by_kind:{atom:27, evidence:56}}

## 3. 口径偏差与诚实登记（任务书 → 实测 → 处置）

1. **任务书"83 张证据卡"**：证据卡实为 **56**；83 = 56 证据卡 + 27 原子卡（已核实；D3 显式写分母常量 `83（56+27）`）。
2. **A1 `verify_append_only.py` 不存在**：实现在 `supply_chain_verify.py:123`，已在该支加字节前缀快路径（末行无换行也能行级追加）。
3. **收工门禁"跑 gate/poison/replay"**：与同文件禁止条款冲突 ⇒ 按**禁止**执行（它们是监工的事，且会改基线）；611 门禁只跑自己的 `--check` + `tool_integrity --check` + `pytest`。
4. **A2 读 `human_review_confirm.py`**：该文件是并行会话未跟踪文件，本批自有工具在 `human_review_cli.py`。
5. **B1"默认 keep-low"**：现 `weighted_af_solver.reviewed_edges` 默认 = keep-low（609 A3 是 upgrade-medium），口径分歧由 610 D1 显形、611 E1 持续监控。

## 4. 遗留 / 交人项（未裁决，本批不改判决口径）

- **P0 人审 modify 口径冲突**：610 已显形 `divergence`；引用 W2 数字必须标明用的哪一档（611 B1/E1 已强制并列呈现）。
- **单人评审风险**：388 条人审来自单一 reviewer（E2 实测），建议引入第二位交叉抽检。
- **论证图碎片化**：C2/C3 已给出补桥候选与改善幅度，但**落库为真实攻击边 + 重跑 W2 是人审权**，本批未执行。
- **活性锚 / oracle 验证**：50 条 observation 缺 `liveness`、83 张卡 0 张 `verified_by_oracle` ⇒ 全量待补；本批只出计划，不补字段（人审权）。

## 5. 验收结论

611 全部任务完成；8 个新工具 + 门禁脚本均 `--check` 锁定已知数字、`tool_integrity --check` 绿、`pytest tests/test_611_tools.py` 全绿。所有修复动作（补桥、补锚、重验、改人审）均**未擅自执行**，留作人审/后续批。建议监工按协议验收后开 612。
