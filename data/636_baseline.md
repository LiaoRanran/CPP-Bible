# 636 任务0 · 开工快照 + 全量基线复测

> 实测时间：2026-09-25。工具：`tools/baseline_636.py`（只读）。

## 一、§一 指标复测（对比 635）

| 指标 | 635 值 | 636 实测 | 一致 |
|---|---|---|---|
| gate_rules | 67 | 67 | ✅ |
| coverage_pct | 100.0 | 100.0 | ✅ |
| na_rate_pct | 11.24 | 11.24 | ✅ |
| grounding_pct | 35.8 | 35.8 | ✅ |
| defeater_coverage_pct | 100.0 | 100.0 | ✅ |
| taint_cards | 8 | 8 | ✅ |
| tau_d_median | 0 | 0 | ✅ |
| daubert_observation | 67 | 67 | ✅ |
| 工具数 | ~407 | 409 | ⚠️ 表为估值 |
| 测试数 | ~406 | 408 | ⚠️ 表为估值 |
| 本地 ahead | 43 | 43 | ✅ |

> 逃逸率 1/1406、自身免疫率 0%、错误代价比、四问结论取 616/634/635 冻结值（本批不跑监工四门禁，§零.4）。

## 二、git status --short（全量）

```
 M _adv_v80/probes/p57.cpp
 M data/authority_v2_mode.json
 M data/autoimmune_dashboard_629.html
 M data/autoimmune_diagnose_630.json
 M data/autoimmune_diagnose_630.md
 M data/autoimmune_fix_proposal_630.json
 M data/autoimmune_fix_proposal_630.md
 M data/autoimmune_human_queue_631.jsonl
 M data/autoimmune_human_queue_631.md
 M data/autoimmune_recalc_630.json
 M data/autoimmune_recalc_630.md
 M data/autoimmune_threshold_630.json
 M data/autoimmune_threshold_630.md
 M data/coverage_probe_l1_2_631.json
 M data/coverage_probe_l1_2_631.md
 M data/coverage_probe_l8_4_631.json
 M data/coverage_probe_l8_4_631.md
 M data/e2e_attestation_629.md
 M data/human_review_dashboard_v2.html
 M data/independence_static_check_629.md
 M data/learner_behavior_events.jsonl
 M data/learner_twin_gate_report_628.md
 M data/pre_push_check_630.json
 M data/pre_push_check_630.md
 M data/snapshot_integrity_626.json
 M data/snapshot_integrity_report_626.md
 M data/third_party_audit_demo_628.json
 M data/third_party_audit_demo_report_628.md
 M data/transparency_log.jsonl
?? _arch_v19/
?? _arch_v19_brief.md
?? _arch_v20/
?? _arch_v20_brief.md
?? "_arch_v21/00_\346\226\271\345\220\221\345\234\260\345\233\276.md"
?? "_arch_v21/01_\351\252\214\350\257\201\345\261\202.md"
?? "_arch_v21/02_\346\262\273\347\220\206\345\261\202.md"
?? "_arch_v21/03_\345\255\246\344\271\240\345\261\202.md"
?? "_arch_v21/04_\347\224\237\346\210\220\345\261\202.md"
?? "_arch_v21/05_\345\237\272\347\241\200\350\256\276\346\226\275\345\261\202.md"
?? "_arch_v21/06_\350\267\250\345\261\202\346\226\260\345\205\264\346\226\271\345\220\221.md"
?? "_arch_v21/07_\347\273\237\350\256\241\345\210\206\346\236\220.md"
?? "_arch_v21/08_\346\216\250\350\215\220\346\267\261\346\214\226Top5.md"
?? _arch_v21/zero_pollution_v21_scan.md
?? _arch_v21_brief.md
?? _arch_v22/
?? _arch_v22_brief.md
?? _arch_v23/
?? _arch_v23_brief.md
?? _arch_v24/
?? _arch_v24_brief.md
?? _arch_v25/
?? _arch_v25_brief.md
?? _arch_v26/
?? _arch_v26_brief.md
?? _arch_v26_handoff.md
?? _arch_v27/
?? _arch_v27_brief.md
?? data/_archive_633/
?? data/queyi_core_interface_design_625.md
?? data/queyi_core_trigger_check_625.md
?? data/vsa/attestation_20260924T055322Z.json
?? data/vsa/attestation_20260924T105250Z.json
?? data/vsa/attestation_20260924T122947Z.json
?? data/vsa/attestation_20260924T125525Z.json
?? data/vsa/attestation_20260924T133120Z.json
?? data/vsa/attestation_20260924T142211Z.json
?? data/vsa/attestation_20260924T144706Z.json
?? data/vsa/attestation_20260924T152721Z.json
?? tests/test_baseline_636.py
?? tools/baseline_636.py
?? tools/queyi_core_interface_design_625.py
?? tools/queyi_core_trigger_check_625.py
```

## 三、最近 5 个 commit

```
f4ac6717 635 [E1]：_auto/status.json 更新为 635 收工(awaiting_review,last_completed_batch=635,next=636,last_commit=4f268ec4)+ outbox/635.md 完成报告
4f268ec4 635 [E1]：收工门禁+三份报告+前后对比——run_635_gate PASS(新工具11/11+ruff+mypy 0/408文件+受控零污染+11交付齐备);生成635_acceptance_report/635_visibility_report/635_next_steps;附修baseline_635两处no-any-return;--check只读+6例单测
797a8e64 635 [V26-5]：验证器准入表(Daubert五问)——68验证器(67规则+mutation生成器)逐条填五问;实测67规则全缺known_error_rate(VFDR只记覆盖率非错误率)=>67条进观察态;生成器有逃逸率1/1406非观察态;仅标记不改判决(落地交人);只读+6例单测
6bcbd45a 635 [V26-4]：例外与豁免条款复审表——7来源(artifact_producer_exempt/verify_reason_exempt/compile_exempt/poison_exemptions/exempt_audit报表/exemption_expiry 615/616)共227条目;每条设下次复审2027-03-25(+180天),无期豁免=0;只读+6例单测
df8eec04 635 [V26-3]：证据通道字段+污染传播演练——6通道定义+控制方(self/external);56证据卡通道分布(direct_experiment6/standard_textbook23/cppreference2/external_audit23/human_review3);演练对象ATOM-CONC-FENCE-001(仓库无正式disputed卡已登记),下游2卡应标tainted,三阀门检查;建议自动污染传播规则(只建议不改判决);只读+6例单测
```

## 四、诚实登记

1. 工具/测试/ahead 的表值为估值，实测见上；
2. 逃逸率/自身免疫率/错误代价比/四问为 616/634/635 **冻结值**，本批未重跑（§零.4）；
3. 本工具**只读**。
