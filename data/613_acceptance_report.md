# 613 收工验收报告（F3 门禁）

> 生成：`python tools/run_613_gate.py` ｜ 时间：2026-09-21T10:21:21
> 模式：full（含卫生/回归/零污染/监工记录）

## 一、613 工具 --check（结论项）

**18/18 通过**

| 工具 | exit | 耗时(s) | 末行 |
|---|---|---|---|
| `613_baseline` | 0 ✅ | 19.2 | [613_baseline] ✅ 自验证通过 |
| `liveness_priority_613` | 0 ✅ | 0.3 | [A1] ✅ 自验证通过 |
| `liveness_completion_613` | 0 ✅ | 0.2 | [A2] ✅ 自验证通过 |
| `golden_lock_proposal_613` | 0 ✅ | 0.2 | [A3] ✅ 自验证通过 |
| `quality_gate_613` | 0 ✅ | 0.2 | [B3] ✅ 自验证通过 |
| `learner_behavior_ingest` | 0 ✅ | 0.2 | [C1] ✅ 自验证通过 |
| `learner_mastery_update_613` | 0 ✅ | 1.0 | [C2] ✅ 自验证通过 |
| `learner_path_graph_613` | 0 ✅ | 0.2 | [C3] ✅ 自验证通过 |
| `learner_twin_dashboard_613` | 0 ✅ | 0.2 | [C4] ✅ 自验证通过 |
| `bridge_edge_proposal_613` | 0 ✅ | 0.2 | [D1] ✅ 自验证通过 |
| `argument_fragmentation_613` | 0 ✅ | 0.5 | [D2] ✅ 自验证通过 |
| `defense_chain_deep_613` | 0 ✅ | 0.2 | [D3] ✅ 自验证通过 |
| `ots_anchor_613` | 0 ✅ | 0.2 | [E1] ✅ 自验证通过 |
| `in_toto_link` | 0 ✅ | 0.2 | [E2] ✅ 自验证通过 |
| `merkle_proof_613` | 0 ✅ | 13.1 | [E3] ✅ 自验证通过 |
| `escape_rate_honest_613` | 0 ✅ | 0.2 | [F1] ✅ 自验证通过 |
| `metrics_613` | 0 ✅ | 2.1 | [F2] ✅ 自验证通过 |
| `d5_source_integrity` | 0 ✅ | 0.5 |     _bench_d5_ch50_demo.cpp <- Book\part05_oo\ch50_multiple_inheritance.md |

## 二、卫生与 613 自身回归（结论项）

| 项 | exit | 耗时(s) | 末行 |
|---|---|---|---|
| ruff | 0 ✅ | 0.2 | All checks passed! |
| mypy | 0 ✅ | 0.9 | Success: no issues found in 196 source files |
| pytest_613 | 0 ✅ | 43.7 | .........................................................                [100%] |

## 三、零污染（受控目录）

- ✅ 干净

## 四、监工类（**仅记录，不作结论**）

| 工具 | exit | 耗时(s) | 末行 |
|---|---|---|---|
| tool_integrity | 0 | 1.6 | [tool_integrity] OK：目录级 Merkle 根与当前内容一致（警告 0 条） |
| gate_engine | 0 | 6.0 |            ↳ 在命题项内补 `liveness: {kind: fixture_symbol, symbol: <夹具特有符号>}`；该符号须真实出现在本命题引用卡的工件断言中且非通用符号。若本命题无法被单一 |
| poison_drill | 0 | 9.0 | [poison] legacy 豁免(单列、不计入诚实口径, 27): ATOM-AUDIENCE, ATOM-DAL-MATCH, ATOM-FM-REQUIRED, ATOM-GRAY-ZONE, ATOM-ID-F |
| atom_evidence_replay | 124 | 120.0 | TIMEOUT(>120s) |

> 铁律：这些是监工的事；F3 例外只作记录，其 exit **不影响**本门禁结论。

## 五、全量回归（信息项 · 含非 613 既有红灯）

> 全量 `pytest -m "not slow"` 含 601/611 等既有测试；其红灯**非 613 引入**，
> 仅作信息记录，不计入 613 结论。

- pytest_full exit=1（317.1s） 末行：`FAILED tests/test_supply_chain_chain_601.py::test_chain_verify_with_real_inspections`
  - 已知漂移：`tests/test_supply_chain_chain_601.py` 的 `governance_check` manifest 不一致（45 处：新增 `_auto/inbox/614_draft.md` + 删除 `_arch_v2/v3/v4/v5/*`），由其他会话的文档变更引起，**非 613 责任**；修法为独立 化债 chore，不在此批次收口。
## 结论

- **✅ 613 自身门禁全绿，可收工**

> 门禁只覆盖 613 工具自验证与卫生/613 回归/零污染；**不代替** golden accept（人审权）
> 与活性锚落卡（受控目录，需授权）。全量回归中的非 613 红灯见第五节，交人 化债。
