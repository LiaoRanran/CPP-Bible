# 634 任务0 · pytest 数据副作用审计

## 一、现象（633 F1 发现）

全量 `pytest -m 'not slow'` 会：(1) 重写 `data/` 多个文件；(2) 向生产透明日志
`data/transparency_log.jsonl` 追加条目；(3) 工作区脏文件 60→74、失败数 32→54 非稳定。

## 二、被修改文件（633 已观测，均在 `data/`）

`629_baseline.*` · `630_baseline.*` · `631_baseline.*` · `autoimmune_diagnose_630.*` ·
`autoimmune_fix_proposal_630.*` · `autoimmune_recalc_630.*` · `autoimmune_threshold_630.*` ·
`autoimmune_human_queue_631.*` · `coverage_probe_*_631.*` · `snapshot_integrity_*_626.*` ·
`metrics_612.md` · `third_party_audit_demo_628.*` · `transparency_log.jsonl` 等。

## 三、根因分类

| 类 | 判据 | 命中 |
|---|---|---|
| a) 测试调工具默认写**生产路径**（`write_report()` 无 tmp 重定向）| 见下表 write_call | **47** 处 |
| b) 工具被测试调用时副作用泄漏（工具 `main()` 默认写 data/）| 见下表 prod_path_write | **0** 处 |
| c) fixture 无 teardown（module fixture 跑真实 e2e 并写文件）| `test_e2e_attestation_629.py` | 1 |

### 3.1 直接调用写方法（类 a/c）

| 文件 | 行 | 片段 |
|---|---|---|
| `test_attack_mapping_629.py` | 44 | `p = M.write_report()` |
| `test_attack_round8_629.py` | 60 | `p = R.write_report()` |
| `test_attack_surface_axes_630.py` | 56 | `p = A.write_report()` |
| `test_attack_taxonomy_629.py` | 44 | `p = T.write_report()` |
| `test_authority_v2_e2e_627.py` | 11 | `r = B.run_e2e()` |
| `test_authority_v2_e2e_627.py` | 18 | `r = B.run_e2e()` |
| `test_authority_v2_e2e_627.py` | 24 | `r = B.run_e2e()` |
| `test_autoimmune_auto_fill_631.py` | 101 | `res = F.apply(dry_run=True)` |
| `test_autoimmune_diagnose_630.py` | 68 | `p = D.write_report()` |
| `test_autoimmune_fix_proposal_630.py` | 81 | `p = P.write_report()` |
| `test_autoimmune_framework_629.py` | 53 | `p = A.write_report()` |
| `test_autoimmune_probe_629.py` | 62 | `p = P.write_report()` |
| `test_autoimmune_recalc_630.py` | 75 | `p = R.write_report()` |
| `test_autoimmune_threshold_630.py` | 50 | `p = T.write_report()` |
| `test_baseline_629.py` | 50 | `p = B.write_report()` |
| `test_baseline_630.py` | 61 | `p = B.write_report()` |
| `test_baseline_631.py` | 62 | `p = B.write_report()` |
| `test_bridge_edge_proposal_613.py` | 49 | `d1.main(["--apply"])` |
| `test_bridge_edge_proposal_613.py` | 51 | `d1.main(["--apply"])` |
| `test_ci_pytest_triage_631.py` | 56 | `p = T.write_report()` |
| `test_coverage_gap_631.py` | 59 | `md = G.write_report()` |
| `test_coverage_metric_630.py` | 51 | `p = C.write_report()` |
| `test_coverage_probe_l1_2_631.py` | 56 | `md = P.write_report()` |
| `test_coverage_probe_l8_4_631.py` | 43 | `md = P.write_report()` |
| `test_e2e_attestation_629.py` | 19 | `d = E.run_e2e()` |
| `test_e2e_attestation_629.py` | 56 | `p = E.write_report()` |
| `test_human_review_report_610.py` | 84 | `hr.write_report(hr.generate_report(hr.load_annotations()), rep)` |
| `test_independence_static_629.py` | 57 | `p = I.write_report()` |
| `test_learner_twin_gate_628.py` | 85 | `p = M.write_report()` |
| `test_loop_metrics_629.py` | 61 | `p = L.write_report()` |
| `test_m1_tce_analysis_609.py` | 64 | `assert m1.main(["--write", "--out", str(out)]) == 0` |
| `test_metrics_honesty_609.py` | 96 | `assert mh.main(["report", "--write", "--out", str(out_file)]) == 0` |
| `test_mutation_m6_optimizer_609.py` | 72 | `assert m6.main(["--write", "--out", str(out)]) == 0` |
| `test_poison_attack_type.py` | 118 | `"跑 `python tools/poison_drill.py --write-surface-map`")` |
| `test_poison_attack_type.py` | 139 | `"增删毒样例后须重跑 --write-surface-map（否则 --by-type 会撒谎）")` |
| `test_pollution_bisect_631.py` | 58 | `md = P.write_report()` |
| `test_pre_push_630.py` | 75 | `p = P.write_report()` |
| `test_queyi_core_interface_v02_631.py` | 60 | `T.write_report()` |
| `test_stale_test_triage_630.py` | 68 | `p = T.write_report()` |
| `test_third_party_audit_demo_628.py` | 39 | `return D.run_e2e(write_report=True)` |
| `test_transparency_anchor_632.py` | 27 | `out = ta.write_anchor(log, vsa)` |
| `test_transparency_anchor_632.py` | 48 | `ta.write_anchor(log, vsa)` |
| `test_transparency_anchor_632.py` | 56 | `ta.write_anchor(log, vsa)` |
| `test_transparency_anchor_632.py` | 65 | `ta.write_anchor(log, vsa)` |
| `test_transparency_verify_632.py` | 67 | `ta.write_anchor(log, vsa)` |
| `test_trust_root_upgrade_631.py` | 53 | `md = T.write_report()` |
| `test_uncovered_surfaces_629.py` | 54 | `p = U.write_report()` |

### 3.2 写生产路径（类 b）

| 文件 | 行 | 片段 |
|---|---|---|

## 四、根因结论

**主因**：相当数量的测试**直接调用被测工具的默认写方法**（`write_report()` /
`run_e2e()`），而这些方法默认写到**生产 `data/` 路径**（未参数化重定向到 tmp）。
其次：`test_e2e_attestation_629.py` 的 module fixture 跑真实 e2e 并 `write_report()`。

**注意**：`transparency_log.jsonl` 的追加**不是** e2e 测试所致（该测试有
`test_production_log_zero_drift` 断言不写生产链）——追加来自**其它**调用
`transparency_log_628` 写路径的测试/工具（A1 以全量还原 fixture 兜住）。

## 五、修复方案（交 A1 执行）

1. **conftest.py 会话级写保护 fixture**：会话开始快照 `data/` 全量文件（路径 + 内容），
   会话结束对**被改文件还原**、对**会话新建文件删除** ⇒ pytest **净引入 0 改动**；
2. **透明日志显式保护**：对 `data/transparency_log.jsonl` 记录行数 + sha256，会话后断言/还原；
3. **新测试规范**：写文件一律用 `tmp_path`（不得写 `data/`）；工具写方法必须支持显式路径参数；
4. 验收：全量 pytest 前后 `git status --short data/` **集合不变**（净 0 改动）。
