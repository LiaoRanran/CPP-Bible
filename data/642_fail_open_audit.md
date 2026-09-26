# 642 B3 · fail-closed 全量审计（**只审计，不修复**）

> 对照口径：641 D 线「信任根缺失 ⇒ FAIL」。本模块扫描**缺失 ⇒ warning / 异常 ⇒ 通过 / 默认值 ⇒ 通过 / 校验失败 ⇒ 仅记录** 四类 fail-open。
> **本文件不修改任何被审计代码**（修复留 643 或经人授权）。

## 一、已知点复核（**可复现实测**）

| # | 位置 | 实测证据 | fail-open | 严重度 |
|---|---|---|---|---|
| FO-A | `tools/tool_integrity.py::verify_supply_chain` | `{"changed": [], "warnings": ["data/__nope_xyz__.json：不存在 ⇒ 跳过（该产出尚未生成，如任务1/2 的 Merkle 根/layout）"], "exit_code": 0}` | ⚠️ 是 | **中** |
| FO-B | `tools/decision_event_v2_626.py::DecisionEvent.from_dict` | `{"empty_dict_accepted": true, "result": "APPROVE", "review_method": "BATCH_AUTH", "decision_origin": "human_observed", "validate_errors": ["target_id ` | ⚠️ 是 | **高** |

### 1.1 逐条影响与修复建议

| # | 影响 | 为什么这个严重度 | 修复建议 |
|---|---|---|---|
| FO-A | 信任根数据文件（毒样例豁免台账 / 覆盖率台账 / 治理 manifest / Merkle 根 / in-toto layout）缺失时**不失败**；在完整检出里等于放弃判别力 | 设计理由是'仓库副本/部分检出下无判别力'，属**有理由的取舍**，但缺少'完整仓库下必须钉住'的分支 ⇒ 仍是 fail-open | 增加 `--require-supply-chain`（或按 `.tool_checksums` 是否已含 supply_chain 节判定）：**节存在但文件缺失 ⇒ exit 1**；仅当节整体缺失（旧格式基准）才降级为 warning |
| FO-B | 空/残 JSON 被补成 **result=APPROVE + review_method=BATCH_AUTH + decision_origin=human_observed** —— 恰好是最'信任假设'的组合；`validate()` 能抓 `target_id` 必填，但**不抓 result 使用了默认值**；另外**未知键被静默丢弃**（拼错字段名等于没写） | — | ① `from_dict` 增加 `strict=True`：**缺失必填字段 ⇒ 抛错**（而不是补默认）；② 记录哪些字段来自默认值（`_defaulted` 集）并在 `validate()` 里报错；③ 未知键 ⇒ 抛错（fail-loud） |

## 二、全量 AST 模式扫描

- 扫描文件：**452** 个 `tools/*.py`
- 命中：**145** 条；按规则分布 `{'FO-3': 38, 'FO-1': 100, 'FO-2': 4, 'FO-4': 3}`

| 规则 | 名称 | 严重度 | 修复建议 |
|---|---|---|---|
| FO-1 | 异常 ⇒ 通过 | 高 | 区分'可容忍异常'与'无法判定'：后者必须抛错或返回 UNKNOWN（四态），不得返回成功 |
| FO-2 | 缺失 ⇒ 通过 | 中 | 缺失应映射为 UNKNOWN/FAIL；若确为可选产物，需在文档与常量里显式声明白名单 |
| FO-3 | 关键字段默认值 ⇒ 通过 | 中 | 关键字段缺失应抛错；确需默认时必须显式标注来源（`_defaulted`）并在校验时报错 |
| FO-4 | 警告不影响退出码 | 中 | 为'警告'提供严格模式开关（如 --strict-supply-chain）：严格模式下警告即失败 |

### 2.1 命中清单（逐条，按文件聚合便于复核）

> **注意**：上表严重度是**规则类**的严重度，不等于每个命中的实例严重度 —— 命中在 CLI 容错里可能无害，落在判决/信任路径上才是真缺陷（需逐条人核）。

| 规则 | 文件:行 | 代码 | 含义 |
|---|---|---|---|
| FO-3 | `tools/612_baseline.py:134` | `m.get('evidence', [])` | 关键字段 'evidence' 缺省即补默认（可能让坏东西通过） |
| FO-1 | `tools/abstain_classifier_621.py:168` | `return {}` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/anti_windup_636.py:36` | `return 0` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/anti_windup_642.py:60` | `return []` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/artifact_version_stamp.py:61` | `return {}` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/atom_evidence_replay.py:571` | `return ''` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/atom_evidence_replay.py:588` | `return ''` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/atom_evidence_replay.py:1010` | `return False` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/atom_evidence_replay.py:1046` | `return False` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/atom_evidence_replay.py:1051` | `return False` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/atom_evidence_replay.py:1053` | `return True` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/atom_evidence_replay.py:1094` | `return False` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/atom_evidence_replay.py:2321` | `return {}` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-3 | `tools/authority_log_620.py:126` | `e.get('prev_hash', GENESIS)` | 关键字段 'prev_hash' 缺省即补默认（可能让坏东西通过） |
| FO-3 | `tools/authority_log_620.py:129` | `e.get('self_hash', GENESIS)` | 关键字段 'self_hash' 缺省即补默认（可能让坏东西通过） |
| FO-2 | `tools/authority_log_620.py:139` | `if os.path.exists(src): return 0` | 文件缺失 ⇒ 返回成功（fail-open） |
| FO-2 | `tools/authority_pending_621.py:202` | `if os.path.exists(path): return 0` | 文件缺失 ⇒ 返回成功（fail-open） |
| FO-1 | `tools/autoimmune_probe_629.py:146` | `return False` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-3 | `tools/autoimmune_rate_framework.py:58` | `meta.get('status', '')` | 关键字段 'status' 缺省即补默认（可能让坏东西通过） |
| FO-1 | `tools/baseline_632.py:70` | `return False` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/baseline_635.py:45` | `return ''` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/baseline_635.py:111` | `return 0.0` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/baseline_636.py:41` | `return ''` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/baseline_636.py:81` | `return 0.0` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/baseline_636.py:89` | `return 0.0` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/baseline_636.py:115` | `return 0` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/blind_protocol_642.py:134` | `return []` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/blind_protocol_642.py:143` | `return ''` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-3 | `tools/blind_protocol_642.py:151` | `r.get('review_method', '')` | 关键字段 'review_method' 缺省即补默认（可能让坏东西通过） |
| FO-3 | `tools/blind_protocol_642.py:152` | `r.get('decision_origin', '')` | 关键字段 'decision_origin' 缺省即补默认（可能让坏东西通过） |
| FO-3 | `tools/blind_review_v1_626.py:75` | `d.get('status', 'pass_a_pending')` | 关键字段 'status' 缺省即补默认（可能让坏东西通过） |
| FO-3 | `tools/book_atom_sync.py:59` | `fm.get('status', 'unknown')` | 关键字段 'status' 缺省即补默认（可能让坏东西通过） |
| FO-1 | `tools/boundary_fields_635.py:45` | `return ''` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/calibration_tracker_636.py:33` | `return []` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/calibration_tracker_636.py:72` | `return 0` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/calibration_tracker_642.py:59` | `return []` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-3 | `tools/calibration_tracker_642.py:68` | `r.get('result', '')` | 关键字段 'result' 缺省即补默认（可能让坏东西通过） |
| FO-1 | `tools/candidate_generator_637.py:100` | `return {}` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/contamination_drill_635.py:39` | `return ''` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/contamination_tracker_636.py:29` | `return []` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-3 | `tools/cost_benefit_637.py:49` | `a.get('severity', '')` | 关键字段 'severity' 缺省即补默认（可能让坏东西通过） |
| FO-1 | `tools/cost_benefit_637.py:83` | `return {}` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/coverage_probe_batch_634.py:73` | `return ''` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/coverage_probe_l1_2_631.py:65` | `return []` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/coverage_probe_l2_3_632.py:54` | `return {}` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/debt_inventory_633.py:83` | `return ''` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/debt_inventory_633.py:91` | `return ''` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/error_detector_637.py:103` | `return {}` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-3 | `tools/error_rate_collector_638.py:95` | `e.get('result', '')` | 关键字段 'result' 缺省即补默认（可能让坏东西通过） |
| FO-3 | `tools/error_rate_collector_638.py:99` | `e.get('verdict', '')` | 关键字段 'verdict' 缺省即补默认（可能让坏东西通过） |
| FO-1 | `tools/escape_rate_trend.py:80` | `return {}` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/escape_root_cause_622.py:43` | `return {}` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/evolution_memo_637.py:50` | `return {}` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/exception_review_635.py:52` | `return 0` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/fail_closed_audit_642.py:126` | `return []` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-4 | `tools/fail_closed_audit_642.py:181` | `if "if changed else" in line and "1" in line:` | 仅内容变更算失败；缺失/未钉只警告（fail-open） |
| FO-3 | `tools/fail_closed_audit_642.py:215` | `kp.get('severity', '低')` | 关键字段 'severity' 缺省即补默认（可能让坏东西通过） |
| FO-3 | `tools/fail_closed_audit_642.py:231` | `kp.get('evidence', {})` | 关键字段 'evidence' 缺省即补默认（可能让坏东西通过） |
| FO-3 | `tools/fail_closed_audit_642.py:235` | `kp.get('severity', '?')` | 关键字段 'severity' 缺省即补默认（可能让坏东西通过） |
| FO-1 | `tools/four_questions_635.py:36` | `return ''` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-3 | `tools/four_questions_635.py:62` | `r.get('decision_origin', '?')` | 关键字段 'decision_origin' 缺省即补默认（可能让坏东西通过） |
| FO-1 | `tools/four_state_verdict_638.py:93` | `return False` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/gate_engine.py:1658` | `return ''` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/gate_engine.py:2778` | `return {}` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/gate_engine.py:3162` | `return {}` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/gen_metrics.py:74` | `return ''` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/golden_lock.py:199` | `return ''` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/golden_lock.py:206` | `return ''` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/grounding_inventory_635.py:38` | `return []` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/horizon_634.py:33` | `return []` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/horizon_634.py:41` | `return {}` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-3 | `tools/horizon_634.py:62` | `r.get('verdict', '?')` | 关键字段 'verdict' 缺省即补默认（可能让坏东西通过） |
| FO-3 | `tools/human_review_confirm.py:138` | `edge.get('evidence', a['evidence_preview'])` | 关键字段 'evidence' 缺省即补默认（可能让坏东西通过） |
| FO-3 | `tools/independent_verifier_628.py:105` | `e.get('target_id', '')` | 关键字段 'target_id' 缺省即补默认（可能让坏东西通过） |
| FO-1 | `tools/kernel_minimality_audit_642.py:80` | `return []` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/knowledge_graph.py:131` | `return {}` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/knowledge_graph.py:162` | `return {}` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/learner_behavior_ingest.py:61` | `return False` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-3 | `tools/ledger_rule_backfill_639.py:88` | `d.get('self_hash', '')` | 关键字段 'self_hash' 缺省即补默认（可能让坏东西通过） |
| FO-3 | `tools/liveness_completion_plan.py:60` | `e.get('evidence', [])` | 关键字段 'evidence' 缺省即补默认（可能让坏东西通过） |
| FO-1 | `tools/loop_rerun_638.py:86` | `return {}` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/loop_tuning_638.py:120` | `return {}` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/mdl_trial_636.py:38` | `return []` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/mdl_trial_636.py:47` | `return {}` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/metrics_snapshot.py:131` | `return ''` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-3 | `tools/metrics_snapshot.py:287` | `r.get('status', '?')` | 关键字段 'status' 缺省即补默认（可能让坏东西通过） |
| FO-1 | `tools/mutation_fuzz.py:672` | `return []` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/mutation_fuzz.py:815` | `return False` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/mutation_fuzz.py:1098` | `return 1` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/mutation_generator_621.py:207` | `return []` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/mutation_generator_621.py:398` | `return True` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-3 | `tools/na_rate_634.py:47` | `r.get('verdict', '')` | 关键字段 'verdict' 缺省即补默认（可能让坏东西通过） |
| FO-1 | `tools/oracle_priority.py:37` | `return {}` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-3 | `tools/oracle_priority.py:79` | `m.get('evidence', [])` | 关键字段 'evidence' 缺省即补默认（可能让坏东西通过） |
| FO-3 | `tools/oracle_verification_plan.py:77` | `p['by_kind'].get('evidence', 0)` | 关键字段 'evidence' 缺省即补默认（可能让坏东西通过） |
| FO-3 | `tools/oracle_verification_plan.py:108` | `p['by_kind'].get('evidence', 0)` | 关键字段 'evidence' 缺省即补默认（可能让坏东西通过） |
| FO-3 | `tools/oracle_verification_plan.py:109` | `p['by_kind'].get('evidence', 0)` | 关键字段 'evidence' 缺省即补默认（可能让坏东西通过） |
| FO-3 | `tools/oracle_verification_plan.py:136` | `plan['by_kind'].get('evidence', 0)` | 关键字段 'evidence' 缺省即补默认（可能让坏东西通过） |
| FO-1 | `tools/path_config_625.py:38` | `return {}` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-3 | `tools/pck_certificate_verifier_619.py:99` | `ha.get('review_method', '')` | 关键字段 'review_method' 缺省即补默认（可能让坏东西通过） |
| FO-3 | `tools/pck_hash_renewal_628.py:87` | `data.get('evidence', [])` | 关键字段 'evidence' 缺省即补默认（可能让坏东西通过） |
| FO-3 | `tools/pck_hash_renewal_628.py:135` | `data.get('evidence', [])` | 关键字段 'evidence' 缺省即补默认（可能让坏东西通过） |
| FO-3 | `tools/pck_renderer_619.py:36` | `cert.get('evidence', [])` | 关键字段 'evidence' 缺省即补默认（可能让坏东西通过） |
| FO-3 | `tools/pck_upgrade_strategy_625.py:61` | `(c.get('claim') or {}).get('verdict', '')` | 关键字段 'verdict' 缺省即补默认（可能让坏东西通过） |
| FO-2 | `tools/pollution_bisect_631.py:45` | `if os.path.exists(p): return True` | 文件缺失 ⇒ 返回成功（fail-open） |
| FO-1 | `tools/protector_rollout_642.py:88` | `return ''` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/queyi_core_cpp_641.py:48` | `return ''` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/queyi_core_cpp_641.py:62` | `return False` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/queyi_core_cpp_641.py:282` | `return 0` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/queyi_core_cpp_641.py:316` | `return False` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/queyi_core_interface_v02_631.py:340` | `return True` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/queyi_core_interface_v02_631.py:342` | `return False` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/queyi_core_interface_v03_632.py:48` | `return {}` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/queyi_core_interface_v03_632.py:344` | `return True` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/queyi_core_interface_v03_632.py:346` | `return False` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/queyi_core_toy_641.py:59` | `return ''` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/queyi_core_v10_641.py:79` | `return ''` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-3 | `tools/queyi_core_v10_641.py:265` | `d.get('result', '')` | 关键字段 'result' 缺省即补默认（可能让坏东西通过） |
| FO-3 | `tools/queyi_core_v10_641.py:267` | `d.get('target_id', '')` | 关键字段 'target_id' 缺省即补默认（可能让坏东西通过） |
| FO-1 | `tools/queyi_core_v10_641.py:619` | `return []` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/queyi_core_v10_641.py:753` | `return True` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/replay_invariants.py:63` | `return []` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/replay_invariants.py:256` | `return True` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-3 | `tools/replay_invariants.py:411` | `entry.get('verdict', '')` | 关键字段 'verdict' 缺省即补默认（可能让坏东西通过） |
| FO-1 | `tools/roadmap_align_640.py:54` | `return {}` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/rr_conflict_classifier_638.py:53` | `return []` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/rr_conflict_classifier_638.py:126` | `return []` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/run_621_gate.py:77` | `return False` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/run_622_gate.py:72` | `return False` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/run_624_gate.py:65` | `return False` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/run_633_gate.py:122` | `return {}` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/self_observer_637.py:99` | `return 0.0` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/self_observer_637.py:116` | `return 0` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/self_observer_637.py:124` | `return 0` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/soft_baseline_634.py:38` | `return {}` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-3 | `tools/stale_test_triage_630.py:144` | `f.get('evidence', '')` | 关键字段 'evidence' 缺省即补默认（可能让坏东西通过） |
| FO-1 | `tools/test_debt_taxonomy_633.py:77` | `return []` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-4 | `tools/tool_integrity.py:284` | `return changed, warnings, (1 if changed else 0)` | 仅内容变更算失败；缺失/未钉只警告（fail-open） |
| FO-3 | `tools/trust_root_status_check.py:146` | `sec['merkle_root'].get('sha256', '-')` | 关键字段 'sha256' 缺省即补默认（可能让坏东西通过） |
| FO-2 | `tools/v2_regression_627.py:56` | `if os.path.exists(path): return False` | 文件缺失 ⇒ 返回成功（fail-open） |
| FO-1 | `tools/verification_horizon_622.py:47` | `return {}` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/verifier_admissibility_635.py:35` | `return []` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/vsa_asymmetric_signer_629.py:125` | `return False` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-1 | `tools/vsa_asymmetric_signer_629.py:132` | `return False` | 异常 ⇒ 返回成功/空集（fail-open） |
| FO-4 | `tools/whitespace_fix.py:121` | `sys.exit(1 if changed else 0)` | 仅内容变更算失败；缺失/未钉只警告（fail-open） |

## 三、严重度汇总（含已知点）

- 高：**1**；中：**1**；低：**0**

## 四、修复优先级建议（**不执行**）

1. **高**：FO-B（`DecisionEvent.from_dict` 默认值 ⇒ APPROVE + human_observed）——它直接决定'信任账本里的一条事件是否可信'；
2. **中**：FO-A（supply_chain 缺失不失败）——加严格模式开关即可，改动面小；
3. **中**：FO-3 命中项逐条复核（多数是「读外部数据时的容错」，需区分「可容忍」与「不可判定」）；
4. **低**：FO-1/FO-2 的命中多为工具自身容错，需按'该工具是否参与判决'分级。

## 诚实登记

1. **只审计不修复**（§七.5）：本批**未改动** `tool_integrity.py` / `decision_event_v2_626.py` 等任何被审计代码；
2. **扫描是启发式**：AST 四条规则**高精度低召回** —— 漏判一定存在（如'异常被 pass 后靠后续默认值通过'这类跨语句模式未覆盖）；
3. **命中 ≠ 缺陷**：需要按'该代码是否参与判决/信任'逐条人核，本报告给出的是**线索清单**，不是判决；
4. 实测两处**均为可复现**（不是纸面推断）：FO-A 实测 `exit_code=0`，FO-B 实测空 dict ⇒ `result='APPROVE'`；
5. **fail-open 的严重度不按出现次数**，按'能否让坏东西通过'分级。
