# subprocess 审计报告（573 任务 B-2，只审不改）

> 570 刚踩过 subprocess 的坑（_controlled_dirty 用了未导入的 subprocess 且被裸 except 吞掉），
> 故 PLW1510（run 无 check）、S603（subprocess 调用）**一律不改逻辑**——自动加 check=True
> 会把"本就容许失败"的容错路径变成异常。此处只出清单交人，**是否真需容错由人逐处判断**。

生成：uff check tools/ tests/ --select PLW1510,S603 --output-format concise

tests\test_atom_evidence_replay.py:171:5: S603 `subprocess` call: check for execution of untrusted input
tests\test_atom_evidence_replay.py:584:9: S603 `subprocess` call: check for execution of untrusted input
tests\test_json_output.py:21:12: S603 `subprocess` call: check for execution of untrusted input
tests\test_json_output.py:21:12: PLW1510 `subprocess.run` without explicit `check` argument
tests\test_p0g_lock.py:114:11: S603 `subprocess` call: check for execution of untrusted input
tests\test_prop_graph.py:67:15: PLW1510 `subprocess.run` without explicit `check` argument
tests\test_task_queue.py:247:13: S603 `subprocess` call: check for execution of untrusted input
tests\test_tool_integrity.py:22:12: S603 `subprocess` call: check for execution of untrusted input
tests\test_tool_integrity.py:22:12: PLW1510 `subprocess.run` without explicit `check` argument
tests\test_viso_diff.py:412:12: PLW1510 `subprocess.run` without explicit `check` argument
tools\adversarial_regression.py:123:13: S603 `subprocess` call: check for execution of untrusted input
tools\adversarial_regression.py:123:13: PLW1510 `subprocess.run` without explicit `check` argument
tools\asm_prepush_guard.py:89:9: S603 `subprocess` call: check for execution of untrusted input
tools\asm_prepush_guard.py:89:9: PLW1510 `subprocess.run` without explicit `check` argument
tools\asm_regen.py:130:13: S603 `subprocess` call: check for execution of untrusted input
tools\asm_regen.py:130:13: PLW1510 `subprocess.run` without explicit `check` argument
tools\asm_repro_spotcheck.py:64:9: S603 `subprocess` call: check for execution of untrusted input
tools\asm_repro_spotcheck.py:64:9: PLW1510 `subprocess.run` without explicit `check` argument
tools\asm_repro_spotcheck.py:203:17: S603 `subprocess` call: check for execution of untrusted input
tools\asm_repro_spotcheck.py:203:17: PLW1510 `subprocess.run` without explicit `check` argument
tools\asm_repro_spotcheck.py:207:17: S603 `subprocess` call: check for execution of untrusted input
tools\asm_repro_spotcheck.py:207:17: PLW1510 `subprocess.run` without explicit `check` argument
tools\asm_repro_spotcheck.py:210:17: S603 `subprocess` call: check for execution of untrusted input
tools\asm_repro_spotcheck.py:210:17: PLW1510 `subprocess.run` without explicit `check` argument
tools\atom_evidence_replay.py:421:21: S603 `subprocess` call: check for execution of untrusted input
tools\atom_evidence_replay.py:421:21: PLW1510 `subprocess.run` without explicit `check` argument
tools\atom_evidence_replay.py:529:17: S603 `subprocess` call: check for execution of untrusted input
tools\atom_evidence_replay.py:529:17: PLW1510 `subprocess.run` without explicit `check` argument
tools\atom_evidence_replay.py:882:9: S603 `subprocess` call: check for execution of untrusted input
tools\atom_evidence_replay.py:882:9: PLW1510 `subprocess.run` without explicit `check` argument
tools\atom_evidence_replay.py:896:9: S603 `subprocess` call: check for execution of untrusted input
tools\atom_evidence_replay.py:896:9: PLW1510 `subprocess.run` without explicit `check` argument
tools\atom_evidence_replay.py:1391:17: PLW1510 `subprocess.run` without explicit `check` argument
tools\book_asm_freshness.py:98:13: S603 `subprocess` call: check for execution of untrusted input
tools\book_asm_freshness.py:98:13: PLW1510 `subprocess.run` without explicit `check` argument
tools\book_asm_freshness.py:175:19: S603 `subprocess` call: check for execution of untrusted input
tools\book_asm_freshness.py:175:19: PLW1510 `subprocess.run` without explicit `check` argument
tools\chapter_compile_check.py:433:13: S603 `subprocess` call: check for execution of untrusted input
tools\chapter_compile_check.py:433:13: PLW1510 `subprocess.run` without explicit `check` argument
tools\ci_local_precheck.py:110:17: S603 `subprocess` call: check for execution of untrusted input
tools\ci_local_precheck.py:110:17: PLW1510 `subprocess.run` without explicit `check` argument
tools\clean_root_artifacts.py:46:9: S603 `subprocess` call: check for execution of untrusted input
tools\clean_root_artifacts.py:46:9: PLW1510 `subprocess.run` without explicit `check` argument
tools\compile_all.py:159:18: S603 `subprocess` call: check for execution of untrusted input
tools\compile_all.py:159:18: PLW1510 `subprocess.run` without explicit `check` argument
tools\compile_all.py:258:13: S603 `subprocess` call: check for execution of untrusted input
tools\compile_all.py:278:15: S603 `subprocess` call: check for execution of untrusted input
tools\compile_all.py:288:19: S603 `subprocess` call: check for execution of untrusted input
tools\compile_run_sanitize_pipeline.py:205:13: S603 `subprocess` call: check for execution of untrusted input
tools\compile_run_sanitize_pipeline.py:205:13: PLW1510 `subprocess.run` without explicit `check` argument
tools\compile_run_sanitize_pipeline.py:234:12: S603 `subprocess` call: check for execution of untrusted input
tools\compile_run_sanitize_pipeline.py:234:12: PLW1510 `subprocess.run` without explicit `check` argument
tools\compile_run_sanitize_pipeline.py:239:13: S603 `subprocess` call: check for execution of untrusted input
tools\compile_run_sanitize_pipeline.py:239:13: PLW1510 `subprocess.run` without explicit `check` argument
tools\compile_run_sanitize_pipeline.py:278:13: S603 `subprocess` call: check for execution of untrusted input
tools\compile_run_sanitize_pipeline.py:278:13: PLW1510 `subprocess.run` without explicit `check` argument
tools\compile_run_sanitize_pipeline.py:494:23: S603 `subprocess` call: check for execution of untrusted input
tools\compile_run_sanitize_pipeline.py:494:23: PLW1510 `subprocess.run` without explicit `check` argument
tools\cost_tracker.py:250:13: S603 `subprocess` call: check for execution of untrusted input
tools\cost_tracker.py:250:13: PLW1510 `subprocess.run` without explicit `check` argument
tools\cppbible.py:108:12: S603 `subprocess` call: check for execution of untrusted input
tools\cppbible.py:161:21: S603 `subprocess` call: check for execution of untrusted input
tools\cppbible.py:161:21: PLW1510 `subprocess.run` without explicit `check` argument
tools\cppbible.py:381:17: S603 `subprocess` call: check for execution of untrusted input
tools\cppbible.py:381:17: PLW1510 `subprocess.run` without explicit `check` argument
tools\cppbible.py:440:17: S603 `subprocess` call: check for execution of untrusted input
tools\cppbible.py:440:17: PLW1510 `subprocess.run` without explicit `check` argument
tools\d5_appendix_audit.py:69:15: S603 `subprocess` call: check for execution of untrusted input
tools\d5_appendix_audit.py:69:15: PLW1510 `subprocess.run` without explicit `check` argument
tools\d5_compile_gate.py:96:15: S603 `subprocess` call: check for execution of untrusted input
tools\d5_compile_gate.py:96:15: PLW1510 `subprocess.run` without explicit `check` argument
tools\d5_compile_gate.py:106:9: S603 `subprocess` call: check for execution of untrusted input
tools\d5_compile_gate.py:106:9: PLW1510 `subprocess.run` without explicit `check` argument
tools\d5_compile_gate.py:117:9: S603 `subprocess` call: check for execution of untrusted input
tools\d5_compile_gate.py:117:9: PLW1510 `subprocess.run` without explicit `check` argument
tools\d5_runtime_gate.py:121:18: S603 `subprocess` call: check for execution of untrusted input
tools\d5_runtime_gate.py:121:18: PLW1510 `subprocess.run` without explicit `check` argument
tools\d5_runtime_gate.py:129:22: S603 `subprocess` call: check for execution of untrusted input
tools\d5_runtime_gate.py:129:22: PLW1510 `subprocess.run` without explicit `check` argument
tools\d5_source_integrity.py:43:11: S603 `subprocess` call: check for execution of untrusted input
tools\d5_source_integrity.py:43:11: PLW1510 `subprocess.run` without explicit `check` argument
tools\env_check.py:31:15: S603 `subprocess` call: check for execution of untrusted input
tools\env_check.py:31:15: PLW1510 `subprocess.run` without explicit `check` argument
tools\exempt_audit.py:60:15: S603 `subprocess` call: check for execution of untrusted input
tools\exempt_audit.py:60:15: PLW1510 `subprocess.run` without explicit `check` argument
tools\exempt_audit.py:107:15: S603 `subprocess` call: check for execution of untrusted input
tools\exempt_audit.py:107:15: PLW1510 `subprocess.run` without explicit `check` argument
tools\expand_assist.py:371:9: S603 `subprocess` call: check for execution of untrusted input
tools\expand_assist.py:371:9: PLW1510 `subprocess.run` without explicit `check` argument
tools\gate_engine.py:2825:13: S603 `subprocess` call: check for execution of untrusted input
tools\gate_engine.py:2825:13: PLW1510 `subprocess.run` without explicit `check` argument
tools\gen_metrics.py:71:13: S603 `subprocess` call: check for execution of untrusted input
tools\gen_metrics.py:71:13: PLW1510 `subprocess.run` without explicit `check` argument
tools\handover_check.py:58:13: S603 `subprocess` call: check for execution of untrusted input
tools\handover_check.py:58:13: PLW1510 `subprocess.run` without explicit `check` argument
tools\hy3_check.py:44:12: S603 `subprocess` call: check for execution of untrusted input
tools\hy3_check.py:44:12: PLW1510 `subprocess.run` without explicit `check` argument
tools\hy3_check.py:90:18: S603 `subprocess` call: check for execution of untrusted input
tools\hy3_check.py:90:18: PLW1510 `subprocess.run` without explicit `check` argument
tools\hy3_check.py:91:19: S603 `subprocess` call: check for execution of untrusted input
tools\hy3_check.py:91:19: PLW1510 `subprocess.run` without explicit `check` argument
tools\hy3_check.py:178:17: S603 `subprocess` call: check for execution of untrusted input
tools\hy3_check.py:178:17: PLW1510 `subprocess.run` without explicit `check` argument
tools\json_project_gate.py:59:15: S603 `subprocess` call: check for execution of untrusted input
tools\json_project_gate.py:59:15: PLW1510 `subprocess.run` without explicit `check` argument
tools\json_project_gate.py:72:9: S603 `subprocess` call: check for execution of untrusted input
tools\json_project_gate.py:72:9: PLW1510 `subprocess.run` without explicit `check` argument
tools\json_project_gate.py:76:9: S603 `subprocess` call: check for execution of untrusted input
tools\json_project_gate.py:76:9: PLW1510 `subprocess.run` without explicit `check` argument
tools\l2_state.py:34:13: PLW1510 `subprocess.run` without explicit `check` argument
tools\legacy\audit_cpp_warnings.py:106:24: S603 `subprocess` call: check for execution of untrusted input
tools\legacy\audit_cpp_warnings.py:106:24: PLW1510 `subprocess.run` without explicit `check` argument
tools\legacy\auto_include.py:363:18: S603 `subprocess` call: check for execution of untrusted input
tools\legacy\auto_include.py:363:18: PLW1510 `subprocess.run` without explicit `check` argument
tools\legacy\ci_gate.py:54:12: S603 `subprocess` call: check for execution of untrusted input
tools\legacy\ci_gate.py:54:12: PLW1510 `subprocess.run` without explicit `check` argument
tools\legacy\d5_asm_evidence.py:104:9: S603 `subprocess` call: check for execution of untrusted input
tools\legacy\d5_asm_evidence.py:104:9: PLW1510 `subprocess.run` without explicit `check` argument
tools\legacy\exercise_gen.py:717:13: S603 `subprocess` call: check for execution of untrusted input
tools\legacy\exercise_gen.py:717:13: PLW1510 `subprocess.run` without explicit `check` argument
tools\legacy\fast_compile.py:53:18: S603 `subprocess` call: check for execution of untrusted input
tools\legacy\fast_compile.py:53:18: PLW1510 `subprocess.run` without explicit `check` argument
tools\legacy\generate_wg21_tracker.py:62:13: S603 `subprocess` call: check for execution of untrusted input
tools\legacy\generate_wg21_tracker.py:62:13: PLW1510 `subprocess.run` without explicit `check` argument
tools\legacy\module_compile_check.py:73:13: S603 `subprocess` call: check for execution of untrusted input
tools\legacy\module_compile_check.py:73:13: PLW1510 `subprocess.run` without explicit `check` argument
tools\legacy\module_compile_check.py:99:13: S603 `subprocess` call: check for execution of untrusted input
tools\legacy\module_compile_check.py:99:13: PLW1510 `subprocess.run` without explicit `check` argument
tools\legacy\quality_dashboard.py:31:9: S603 `subprocess` call: check for execution of untrusted input
tools\legacy\quality_dashboard.py:31:9: PLW1510 `subprocess.run` without explicit `check` argument
tools\legacy\quality_dashboard.py:48:10: S603 `subprocess` call: check for execution of untrusted input
tools\legacy\quality_dashboard.py:48:10: PLW1510 `subprocess.run` without explicit `check` argument
tools\legacy\test_site_audit_fixture.py:35:9: S603 `subprocess` call: check for execution of untrusted input
tools\legacy\test_site_audit_fixture.py:35:9: PLW1510 `subprocess.run` without explicit `check` argument
tools\legacy\verify_prose_only.py:53:16: S603 `subprocess` call: check for execution of untrusted input
tools\legacy\wave_intake_check.py:162:9: S603 `subprocess` call: check for execution of untrusted input
tools\legacy\wave_intake_check.py:162:9: PLW1510 `subprocess.run` without explicit `check` argument
tools\legacy\wave_intake_check.py:170:11: S603 `subprocess` call: check for execution of untrusted input
tools\legacy\wave_intake_check.py:170:11: PLW1510 `subprocess.run` without explicit `check` argument
tools\mermaid_audit.py:120:17: S603 `subprocess` call: check for execution of untrusted input
tools\mermaid_audit.py:120:17: PLW1510 `subprocess.run` without explicit `check` argument
tools\mermaid_audit.py:145:13: S603 `subprocess` call: check for execution of untrusted input
tools\mermaid_audit.py:145:13: PLW1510 `subprocess.run` without explicit `check` argument
tools\metrics_collector.py:78:13: S603 `subprocess` call: check for execution of untrusted input
tools\metrics_collector.py:78:13: PLW1510 `subprocess.run` without explicit `check` argument
tools\metrics_collector.py:91:13: S603 `subprocess` call: check for execution of untrusted input
tools\metrics_collector.py:91:13: PLW1510 `subprocess.run` without explicit `check` argument
tools\metrics_snapshot.py:127:13: S603 `subprocess` call: check for execution of untrusted input
tools\metrics_snapshot.py:127:13: PLW1510 `subprocess.run` without explicit `check` argument
tools\mutation_fuzz.py:458:13: PLW1510 `subprocess.run` without explicit `check` argument
tools\observability.py:168:13: PLW1510 `subprocess.run` without explicit `check` argument
tools\poison_drill.py:132:27: S603 `subprocess` call: check for execution of untrusted input
tools\poison_drill.py:132:27: PLW1510 `subprocess.run` without explicit `check` argument
tools\poison_drill.py:166:9: S603 `subprocess` call: check for execution of untrusted input
tools\poison_drill.py:166:9: PLW1510 `subprocess.run` without explicit `check` argument
tools\poison_drill.py:168:27: S603 `subprocess` call: check for execution of untrusted input
tools\poison_drill.py:168:27: PLW1510 `subprocess.run` without explicit `check` argument
tools\poison_drill.py:196:9: S603 `subprocess` call: check for execution of untrusted input
tools\poison_drill.py:196:9: PLW1510 `subprocess.run` without explicit `check` argument
tools\poison_drill.py:222:9: S603 `subprocess` call: check for execution of untrusted input
tools\poison_drill.py:222:9: PLW1510 `subprocess.run` without explicit `check` argument
tools\poison_drill.py:248:9: S603 `subprocess` call: check for execution of untrusted input
tools\poison_drill.py:248:9: PLW1510 `subprocess.run` without explicit `check` argument
tools\poison_drill.py:864:9: S603 `subprocess` call: check for execution of untrusted input
tools\poison_drill.py:864:9: PLW1510 `subprocess.run` without explicit `check` argument
tools\poison_drill.py:1874:9: S603 `subprocess` call: check for execution of untrusted input
tools\poison_drill.py:1874:9: PLW1510 `subprocess.run` without explicit `check` argument
tools\poison_drill.py:2116:15: PLW1510 `subprocess.run` without explicit `check` argument
tools\prepush_check.py:67:13: S603 `subprocess` call: check for execution of untrusted input
tools\prepush_check.py:67:13: PLW1510 `subprocess.run` without explicit `check` argument
tools\prepush_check.py:86:13: PLW1510 `subprocess.run` without explicit `check` argument
tools\prepush_check.py:121:13: S603 `subprocess` call: check for execution of untrusted input
tools\run_cpp_assertions.py:139:13: S603 `subprocess` call: check for execution of untrusted input
tools\run_cpp_assertions.py:139:13: PLW1510 `subprocess.run` without explicit `check` argument
tools\run_cpp_assertions.py:187:14: S603 `subprocess` call: check for execution of untrusted input
tools\run_cpp_assertions.py:187:14: PLW1510 `subprocess.run` without explicit `check` argument
tools\run_cpp_assertions.py:200:13: S603 `subprocess` call: check for execution of untrusted input
tools\run_cpp_assertions.py:200:13: PLW1510 `subprocess.run` without explicit `check` argument
tools\run_expected.py:164:17: S603 `subprocess` call: check for execution of untrusted input
tools\run_expected.py:164:17: PLW1510 `subprocess.run` without explicit `check` argument
tools\run_expected.py:177:17: S603 `subprocess` call: check for execution of untrusted input
tools\run_expected.py:177:17: PLW1510 `subprocess.run` without explicit `check` argument
tools\run_expected.py:226:16: PLW1510 `subprocess.run` without explicit `check` argument
tools\run_expected.py:229:15: S603 `subprocess` call: check for execution of untrusted input
tools\run_expected.py:229:15: PLW1510 `subprocess.run` without explicit `check` argument
tools\s10_verify_mark.py:58:11: S603 `subprocess` call: check for execution of untrusted input
tools\s10_verify_mark.py:58:11: PLW1510 `subprocess.run` without explicit `check` argument
tools\snapshot.py:33:9: S603 `subprocess` call: check for execution of untrusted input
tools\snapshot.py:33:9: PLW1510 `subprocess.run` without explicit `check` argument
tools\snapshot.py:49:10: S603 `subprocess` call: check for execution of untrusted input
tools\snapshot.py:49:10: PLW1510 `subprocess.run` without explicit `check` argument
tools\task_queue.py:1314:13: PLW1510 `subprocess.run` without explicit `check` argument
tools\task_queue.py:1417:22: PLW1510 `subprocess.run` without explicit `check` argument
tools\toolchain.py:225:13: S603 `subprocess` call: check for execution of untrusted input
tools\toolchain.py:225:13: PLW1510 `subprocess.run` without explicit `check` argument
tools\verify_compiler_features.py:147:13: S603 `subprocess` call: check for execution of untrusted input
tools\verify_compiler_features.py:147:13: PLW1510 `subprocess.run` without explicit `check` argument
tools\verify_compiler_features.py:153:18: S603 `subprocess` call: check for execution of untrusted input
tools\verify_compiler_features.py:153:18: PLW1510 `subprocess.run` without explicit `check` argument
tools\verify_compiler_features.py:158:15: S603 `subprocess` call: check for execution of untrusted input
tools\verify_compiler_features.py:158:15: PLW1510 `subprocess.run` without explicit `check` argument
tools\verify_exercises.py:50:9: S603 `subprocess` call: check for execution of untrusted input
tools\verify_exercises.py:50:9: PLW1510 `subprocess.run` without explicit `check` argument
Found 203 errors.
