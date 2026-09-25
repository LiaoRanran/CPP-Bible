# 635 任务0 · 开工快照 + 全量基线测量

> 实测时间：2026-09-25。工具：`tools/baseline_635.py`（只读，不跑监工四门禁）。

## 一、§一 指标实测（不抄表）

| 指标 | §一 表值 | 实测 | 一致 |
|---|---|---|---|
| gate 规则数 | 67 | 67 | ✅ |
| coverage | 100%（35/35） | 100.0% | ✅ |
| 自身免疫率（缺 signed_by 卡） | 0 | 0 | ✅ |
| N/A 率 | 11.24% | 11.24% | ✅ |
| Horizon 60-80 桶 | 100% | 1.0 | ✅ |
| 工具数 | ~450 | 397 | ⚠️ 表为估值 |
| 测试数 | ~500 | 396 | ⚠️ 表为估值 |
| commits | ~1900+ | 1824 | ⚠️ 表为估值 |
| 本地 ahead | 29 | 29 | ✅ |

> 逃逸率 1/1406（0.071%）取 616 统计（本批不跑监工门禁）。

## 二、补充实测

- atom 卡：**28**（verified **23**）
- `data/*baseline*` 文件：**34** 个
- 全系统「例外/豁免/白名单」线索命中：**991** 处（V26-4 深挖用）
- 工作区脏文件：**78**

## 三、`git status --short`（全量）

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
?? _arch_v24/
?? _arch_v24_brief.md
?? _arch_v25/
?? _arch_v25_brief.md
?? _arch_v26/
?? _arch_v26_brief.md
?? _arch_v26_handoff.md
?? data/635_baseline.json
?? data/635_baseline.md
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
?? tests/test_baseline_635.py
?? tools/baseline_635.py
?? tools/queyi_core_interface_design_625.py
?? tools/queyi_core_trigger_check_625.py
```

## 四、最近 5 个 commit

```
1b1a11ed 634 [E1]：_auto/status.json 更新为 634 收工(awaiting_review,last_completed_batch=634,next=635,last_commit=b7edbdd7)+ outbox/634.md 完成报告
b7edbdd7 634 [E1]：收工门禁+三份报告+7维度对比——run_634_gate PASS(新工具20/20+A2老工具79/79+ruff+mypy 0+受控零污染+pytest数据隔离data/零改动+coverage 100%+自身免疫0);生成634_acceptance_report/634_debt_clearance/634_construction;附修horizon_634的mypy;--check只读+6例单测
e3a94ad4 634 [B3]：N/A 率根因分类——616源(179/1593=11.24%)仅存聚合,逐行原因未落盘无法全量分类(登记);对622+623的130条有reason样本分类:judged79/载体型25/other26,清洁率(移出载体型)24.76%;结论N/A主因是载体天花板非infra;--check只读+6例单测
9acbfcdf 634 [B2]：Horizon 复算+登记——实测 §一「60-80桶0%」为陈旧基线(622曲线v1起即100%),80条高复杂度攻击触达17条新block规则,两目标均达成;634不重复造轮子,如实登记基线陈旧与残留4逃逸/2infra;--check只读+6例单测
f49b2d1f 634 [C2]：快照测试更新+.pytest_tmp 处置——syrupy 5快照2失败(block 0->28/warn 186->116,核 rules 未变属合法演进)非盲目更新后5/5绿;.pytest_tmp 已 gitignore(不入库),物理删除被环境 safe-delete 拦截(>500)交人;登记633 E1'25快照'口径偏大(实为1文件5快照)
```

## 五、baseline 报告文件清单

- `609_baseline.md`
- `611_baseline.md`
- `612_baseline.md`
- `613_baseline_argumentation.md`
- `613_baseline_ci.md`
- `613_baseline_d5_debt.md`
- `613_baseline_learner_twin.md`
- `614_baseline.md`
- `615_baseline.md`
- `616_baseline.md`
- `617_baseline.md`
- `618_baseline.md`
- `619_baseline.md`
- `620_baseline.md`
- `621_baseline.md`
- `622_baseline.md`
- `623_baseline.md`
- `624_baseline.md`
- `625_baseline.md`
- `626_baseline.md`
- `627_baseline.md`
- `628_baseline.md`
- `629_baseline.md`
- `630_baseline.json`
- `630_baseline.md`
- `631_baseline.json`
- `631_baseline.md`
- `632_baseline.md`
- `634_baseline.md`
- `634_soft_baseline.json`
- `635_baseline.json`
- `635_baseline.md`
- `autoimmune_rate_baseline.md`
- `ev_matrix_dual_impl_baseline_616.json`

## 六、诚实登记

1. 工具/测试/commits 的 §一 表值（~450/~500/~1900+）为**估值**，实测见上（397/396/1824）；
2. 逃逸率取 616 统计，**未重跑** mutation（§零.4）；
3. 本工具**只读**：不写任何监控对象文件，只写本报告。
