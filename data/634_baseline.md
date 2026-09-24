# 634 开工快照（任务0）

## §一 Standing Baseline（8 维度）

| 指标 | 当前值 |
|---|---|
| coverage | 60%（21/35 攻击向量） |
| horizon | 复杂度 60 断崖，60-80 桶检出 0% |
| na_rate | 11.24%（179/1593） |
| autoimmune_rate | 14.3%（4/28 卡缺 signed_by） |
| tools_no_check | 79 |
| fragile_asserts | 30 |
| snapshot_stale | 25 |
| pytest_side_effect | 会重写 data/ + 追加生产日志 |

## 目录/计数快照

| 项 | 值 |
|---|---|
| tools/*.py | 376 |
| tests/test_*.py | 388 |
| git commit 数 | 1807 |
| 无 --check 工具（复算）| 79 |
| 工作区脏文件 | 69 |

## git status --short（全量）

```
 M _adv_v80/probes/p57.cpp
 M data/629_baseline.md
 M data/630_baseline.json
 M data/630_baseline.md
 M data/631_baseline.json
 M data/631_baseline.md
 M data/authority_v2_mode.json
 M data/autoimmune_dashboard_629.html
 M data/autoimmune_diagnose_630.json
 M data/autoimmune_diagnose_630.md
 M data/autoimmune_fix_proposal_630.json
 M data/autoimmune_fix_proposal_630.md
 M data/autoimmune_human_queue_631.jsonl
 M data/autoimmune_human_queue_631.md
 M data/autoimmune_rate_baseline.md
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
?? _arch_v24_brief.md
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
?? tests/test_baseline_634.py
?? tools/baseline_634.py
?? tools/queyi_core_interface_design_625.py
?? tools/queyi_core_trigger_check_625.py
```
