# 613 收工验收报告（F3 门禁）

> 生成：`python tools/run_613_gate.py` ｜ 时间：2026-09-21T00:11:56
> 模式：quick（仅工具 --check）

## 一、613 工具 --check（结论项）

**18/18 通过**

| 工具 | exit | 耗时(s) | 末行 |
|---|---|---|---|
| `613_baseline` | 0 ✅ | 1.7 | [613_baseline] ✅ 自验证通过 |
| `liveness_priority_613` | 0 ✅ | 0.2 | [A1] ✅ 自验证通过 |
| `liveness_completion_613` | 0 ✅ | 0.2 | [A2] ✅ 自验证通过 |
| `golden_lock_proposal_613` | 0 ✅ | 0.2 | [A3] ✅ 自验证通过 |
| `quality_gate_613` | 0 ✅ | 0.2 | [B3] ✅ 自验证通过 |
| `learner_behavior_ingest` | 0 ✅ | 0.2 | [C1] ✅ 自验证通过 |
| `learner_mastery_update_613` | 0 ✅ | 0.3 | [C2] ✅ 自验证通过 |
| `learner_path_graph_613` | 0 ✅ | 0.2 | [C3] ✅ 自验证通过 |
| `learner_twin_dashboard_613` | 0 ✅ | 0.2 | [C4] ✅ 自验证通过 |
| `bridge_edge_proposal_613` | 0 ✅ | 0.2 | [D1] ✅ 自验证通过 |
| `argument_fragmentation_613` | 0 ✅ | 0.4 | [D2] ✅ 自验证通过 |
| `defense_chain_deep_613` | 0 ✅ | 0.2 | [D3] ✅ 自验证通过 |
| `ots_anchor_613` | 0 ✅ | 0.2 | [E1] ✅ 自验证通过 |
| `in_toto_link` | 0 ✅ | 0.2 | [E2] ✅ 自验证通过 |
| `merkle_proof_613` | 0 ✅ | 1.7 | [E3] ✅ 自验证通过 |
| `escape_rate_honest_613` | 0 ✅ | 0.2 | [F1] ✅ 自验证通过 |
| `metrics_613` | 0 ✅ | 2.0 | [F2] ✅ 自验证通过 |
| `d5_source_integrity` | 0 ✅ | 0.5 |     _bench_d5_ch50_demo.cpp <- Book\part05_oo\ch50_multiple_inheritance.md |

## 结论

- **✅ 门禁全绿，可收工**

> 门禁只覆盖工具自验证与卫生/回归/零污染；**不代替** golden accept（人审权）
> 与活性锚落卡（受控目录，需授权）。
