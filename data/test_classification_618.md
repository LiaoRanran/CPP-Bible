# 测试分类计数（618 C2 · 落地 617 C1 taxonomy）

> 纯标准库；扫描 tests/ 下 216 个 .py，按文件名 + import 内容特征分类（成员关系计数）。

> 真实验证 = 命中 gate/poison/replay/mutation/evidence/independent_verification/statistics/tooling_integrity 之一；脚本自测 = snapshot/script_self_test（工具链自身，不计入验证覆盖）。

## 一、三向分类（gate/poison/replay 成员关系，可重叠 / 其他=三者均未命中）

- **replay**：30
- **poison**：7
- **gate**：43
- **其他**：150

## 二、primary 全类别计数（单文件归入优先级最高的一类）

- 其他：126
- gate：43
- replay：23
- mutation：8
- statistics：6
- tooling_integrity：6
- independent_verification：3
- snapshot：1

## 三、真实验证 vs 脚本自测

- **真实验证**：89（占比 41.2%）
- **脚本自测**：1（占比 0.5%）
- **未分类（需人工 review）**：126（不匹配任何已知特征）

## 四、未分类文件清单（需人工复核）

- test_611_tools.py
- test_618_a3.py
- test_618_b.py
- test_adversarial_regression.py
- test_append_only_611.py
- test_argument_audit_610.py
- test_argument_audit_advanced_610.py
- test_argument_audit_report_610.py
- test_argument_fragmentation_613.py
- test_argument_graph_analysis_611.py
- test_atom_coverage_map.py
- test_attack_edge_generator_596.py
- test_backup.py
- test_bkt_solver_612.py
- test_bridge_edge_impact_612.py
- test_bridge_edge_pre_annotate_612.py
- test_bridge_edge_proposal_613.py
- test_bridge_edge_review_612.py
- test_build_reproducibility_deep_609.py
- test_ci_config_615.py
- test_ci_local_precheck.py
- test_cost_tracker.py
- test_d5_bench_resolution_613.py
- test_data_dir_organize_615.py
- test_defense_chain_610.py
- test_defense_chain_cli_610.py
- test_defense_chain_deep_613.py
- test_defense_chain_html_610.py
- test_doc_frontmatter.py
- test_doc_lint.py
- test_ev_matrix_dual_impl_615.py
- test_ev_matrix_dual_impl_fix_615.py
- test_ev_matrix_dual_impl_lock_616.py
- test_ev_matrix_rule_def_v2_616.py
- test_ev_matrix_v2_updated_616.py
- test_exemption_disposal_616.py
- test_exemption_expiry_615.py
- test_gen_metrics.py
- test_golden_lock_proposal_613.py
- test_goodhart_metrics_integration_616.py
- test_goodhart_monitor_615.py
- test_governance_auto_update_607.py
- test_governance_doc_guard_591.py
- test_governance_self_hash_601.py
- test_grounded_audit_596.py
- test_grounded_cli_609.py
- test_grounded_visualizer_609.py
- test_grounded_web_609.py
- test_human_decision_tracking_616.py
- test_human_review_cli_609.py
- test_human_review_dashboard_610.py
- test_human_review_export_610.py
- test_human_review_feedback_609.py
- test_human_review_honesty_615.py
- test_human_review_item_by_item_615.py
- test_human_review_quality_609.py
- test_human_review_queue_608.py
- test_human_review_report_610.py
- test_in_toto_link_613.py
- test_independent_verifier_prototype_616.py
- test_intoto_provenance_609.py
- test_json_output.py
- test_kc_inventory_612.py
- test_learner_argument_link_614.py
- test_learner_behavior_ingest_613.py
- test_learner_behavior_logger_614.py
- test_learner_mastery_update_613.py
- test_learner_ood_evaluator_614.py
- test_learner_path_graph_613.py
- test_learner_recommender_612.py
- test_learner_state_612.py
- test_learner_transition_detector_615.py
- test_learner_twin_dashboard_612.py
- test_learner_twin_dashboard_613.py
- test_learner_twin_dashboard_614.py
- test_learner_twin_validation_615.py
- test_liveness_candidate_generator_612.py
- test_liveness_completion_613.py
- test_liveness_impact_612.py
- test_liveness_priority_613.py
- test_liveness_review_612.py
- test_m6_improvement_plan_610.py
- test_merkle_proof_613.py
- test_metrics_612.py
- test_metrics_613.py
- test_metrics_collector.py
- test_metrics_collector_curves.py
- test_metrics_curves_v7_592.py
- test_metrics_defense_chain_stats_610.py
- test_metrics_grounded_status_610.py
- test_metrics_honesty_609.py
- test_metrics_human_review_progress_610.py
- test_metrics_new_indicators_608.py
- test_modify_mode_611.py
- test_modify_mode_analysis_611.py
- test_observability.py
- test_opentimestamps_anchor_609.py
- test_oracle_priority_612.py
- test_oracle_priority_614.py
- test_oracle_verification_614.py
- test_oracle_verifier_612.py
- test_ots_anchor_613.py
- test_patch_blocks.py
- test_prop_asof_583.py
- test_prop_closure_592.py
- test_prop_inventory_592.py
- test_proposition_liveness_audit_607.py
- test_review_seconds_611.py
- test_slow_performance_608.py
- test_slow_performance_609.py
- test_slow_performance_609_b3.py
- test_star_h2_audit.py
- test_stat_bounds.py
- test_supply_chain_601.py
- test_supply_chain_verify_609.py
- test_task_queue.py
- test_task_queue_stateful.py
- test_task_state.py
- test_tool_merge_decision_615.py
- test_toolchain_regressions.py
- test_trace_logger.py
- test_trust_root_status_check_614.py
- test_warn_governance_615.py
- test_warn_governance_workflow_616.py
- test_weighted_af_human_review_609.py
- test_weighted_af_solver_596.py
