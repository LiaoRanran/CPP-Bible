# 613 收工验收报告（F3 门禁）

> 生成：`python tools/run_613_gate.py` ｜ 时间：2026-09-21T00:21:48
> 模式：full（含卫生/回归/零污染/监工记录）

## 一、613 工具 --check（结论项）

**18/18 通过**

| 工具 | exit | 耗时(s) | 末行 |
|---|---|---|---|
| `613_baseline` | 0 ✅ | 1.9 | [613_baseline] ✅ 自验证通过 |
| `liveness_priority_613` | 0 ✅ | 0.2 | [A1] ✅ 自验证通过 |
| `liveness_completion_613` | 0 ✅ | 0.2 | [A2] ✅ 自验证通过 |
| `golden_lock_proposal_613` | 0 ✅ | 0.2 | [A3] ✅ 自验证通过 |
| `quality_gate_613` | 0 ✅ | 0.2 | [B3] ✅ 自验证通过 |
| `learner_behavior_ingest` | 0 ✅ | 0.2 | [C1] ✅ 自验证通过 |
| `learner_mastery_update_613` | 0 ✅ | 0.3 | [C2] ✅ 自验证通过 |
| `learner_path_graph_613` | 0 ✅ | 0.2 | [C3] ✅ 自验证通过 |
| `learner_twin_dashboard_613` | 0 ✅ | 0.2 | [C4] ✅ 自验证通过 |
| `bridge_edge_proposal_613` | 0 ✅ | 0.2 | [D1] ✅ 自验证通过 |
| `argument_fragmentation_613` | 0 ✅ | 0.3 | [D2] ✅ 自验证通过 |
| `defense_chain_deep_613` | 0 ✅ | 0.2 | [D3] ✅ 自验证通过 |
| `ots_anchor_613` | 0 ✅ | 0.2 | [E1] ✅ 自验证通过 |
| `in_toto_link` | 0 ✅ | 0.2 | [E2] ✅ 自验证通过 |
| `merkle_proof_613` | 0 ✅ | 1.7 | [E3] ✅ 自验证通过 |
| `escape_rate_honest_613` | 0 ✅ | 0.2 | [F1] ✅ 自验证通过 |
| `metrics_613` | 0 ✅ | 1.8 | [F2] ✅ 自验证通过 |
| `d5_source_integrity` | 0 ✅ | 0.5 |     _bench_d5_ch50_demo.cpp <- Book\part05_oo\ch50_multiple_inheritance.md |

## 二、卫生与回归（结论项）

| 项 | exit | 耗时(s) | 末行 |
|---|---|---|---|
| ruff | 0 ✅ | 0.2 | All checks passed! |
| mypy | 1 ❌ | 0.8 | Found 10 errors in 7 files (checked 196 source files) |
| pytest | 1 ❌ | 428.9 | FAILED tests/test_supply_chain_chain_601.py::test_chain_verify_with_real_inspections |

## 三、零污染（受控目录）

- ✅ 干净

## 四、监工类（**仅记录，不作结论**）

| 工具 | exit | 耗时(s) | 末行 |
|---|---|---|---|
| tool_integrity | 0 | 1.4 | [tool_integrity] OK：目录级 Merkle 根与当前内容一致（警告 0 条） |
| gate_engine | 0 | 5.6 |            ↳ 在命题项内补 `liveness: {kind: fixture_symbol, symbol: <夹具特有符号>}`；该符号须真实出现在本命题引用卡的工件断言中且非通用符号。若本命题无法被单一 |
| poison_drill | 0 | 8.9 | [poison] legacy 豁免(单列、不计入诚实口径, 27): ATOM-AUDIENCE, ATOM-DAL-MATCH, ATOM-FM-REQUIRED, ATOM-GRAY-ZONE, ATOM-ID-F |
| atom_evidence_replay | 124 | 120.0 | TIMEOUT(>120s) |

> 铁律：这些是监工的事；F3 例外只作记录，其 exit **不影响**本门禁结论。

## 结论

- **❌ 门禁未通过**

> 门禁只覆盖工具自验证与卫生/回归/零污染；**不代替** golden accept（人审权）
> 与活性锚落卡（受控目录，需授权）。
