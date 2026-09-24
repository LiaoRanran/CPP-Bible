# 633 E1 · 测试债深化分类与长期方案

> 只针对 **A2 清理后的剩余失败** 做深度分类；**不修改任何测试逻辑**（§八.E1）。

- A2 后剩余失败（`data/633_ci_failures.json` run2）：**54** 项

## 一、slow 测试

标记 `@pytest.mark.slow` 的文件：**6** 个

- `tests/test_mutation_selfcheck_589.py`
- `tests/test_pe_timestamp_caliber_611.py`
- `tests/test_slow_performance_608.py`
- `tests/test_slow_performance_609.py`
- `tests/test_task_queue_stateful.py`
- `tests/test_test_debt_taxonomy_633.py`

→ 长期方案：slow 组独立 job（夜间/手动），CI PR 只跑 `not slow`。

## 二、跨批脆弱型（硬编码批次号断言）

命中：**30** 处

| 文件 | 行 | 断言 |
|---|---|---|
| `tests/test_618_gate.py` | 63 | `assert len(g.CHECK_TOOLS) == 10  # 617 三件 + 618 七件` |
| `tests/test_620_c3.py` | 103 | `assert res["log_entries"] == 418   # 624 D3：622 D1 逐条人审后 Authority 日志 388→418（存量修正）` |
| `tests/test_621_d1.py` | 42 | `assert ids[0] == "prop-621-001"` |
| `tests/test_621_d1.py` | 43 | `assert ids[-1] == "prop-621-030"` |
| `tests/test_621_d2.py` | 79 | `assert res["batch"]["count"] == 418   # 624 D3：622 D1 逐条人审后 Authority 日志 388→418（存量修正）` |
| `tests/test_attack_round8_629.py` | 19 | `assert m["mutation_id"] == f"MUT-629-R8-{i:02d}"` |
| `tests/test_escape_root_cause_v2_623.py` | 43 | `assert len(touched) > 9, f"触达规则应 > 622 的 9，实际 {len(touched)}"` |
| `tests/test_exemption_disposal_616.py` | 15 | `assert len(disp) == len(ex.load_exemptions())     # 624 D3：动态口径` |
| `tests/test_exemption_expiry_615.py` | 14 | `assert len(rows) == len(ex.load_exemptions())     # 624 D3：动态口径（legacy 27 + 624 新增）` |
| `tests/test_high_complexity_sandbox_run_623.py` | 43 | `assert len(touched) > 9, f"应超过 622 的 9 条，实际 {len(touched)}"` |
| `tests/test_human_decision_tracking_616.py` | 25 | `assert len(rows) >= 10                       # 615 七项 + 616 三项` |
| `tests/test_metrics_grounded_status_610.py` | 61 | `assert d608["grounded"]["in"] == 114, "608 的 grounded 走产物 ⇒ 也应是 114"` |
| `tests/test_metrics_grounded_status_610.py` | 82 | `assert called["n"] == 1, "collect() 必须调用 610 采集器一次"` |
| `tests/test_migrate_to_v2_626.py` | 43 | `assert by.get("ITEM_OPEN") == 30                 # 622 授权执行的 30 条` |
| `tests/test_modify_mode_611.py` | 138 | `assert g["solver_recompute"]["in"] == 121          # 610 字段语义未变（= 609 A3 口径）` |
| `tests/test_mutation_fuzz_report.py` | 45 | `assert (variants, blocked, escaped, n_a, strict) == (1188, 729, 227, 232, 615)` |
| `tests/test_pck_upgrade_strategy_625.py` | 41 | `assert os.path.exists(p) and os.path.getsize(p) > 600` |
| `tests/test_poison_exemptions_581.py` | 112 | `assert rep["total"] == 67   # 625 A3：624 B1 后规则数 63→67` |
| `tests/test_run_613_gate.py` | 62 | `assert doc["batch"] == "613"` |
| `tests/test_run_614_gate.py` | 42 | `assert st["batch"] == "614" and st["status"] == "awaiting_review"` |
| `tests/test_run_615_gate.py` | 31 | `assert st["last_completed_batch"] == 615 and st["history"][-1]["verdict"] == "FAIL"` |
| `tests/test_run_623_gate.py` | 54 | `assert rc_batch == 0, "只跑本批会漏检存量债（正是 622 的口径陷阱）"` |
| `tests/test_run_628_gate_628.py` | 89 | `assert status["batch"] >= 628 and status["state"] == "awaiting_review"` |
| `tests/test_run_628_gate_628.py` | 90 | `assert status["last_completed_batch"] >= 628` |
| `tests/test_run_629_gate.py` | 67 | `assert len(B.BASELINE_FAILURES) == 11, "629 修正后的既有失败基线（首测 19 项含 8 项自伤/回归）"` |
| `tests/test_run_629_gate.py` | 87 | `assert p.returncode == 0, "629 不得改动 ci.yml"` |
| `tests/test_slow_performance_609.py` | 44 | `assert got == 100, f"max_examples 被改成 {got}（应为 608 D1 定的预算下限 100）"` |
| `tests/test_stale_test_triage_630.py` | 45 | `assert tri["total"] >= 11, f"629 基线 11 项，实测 {tri['total']}"` |
| `tests/test_stat_bounds.py` | 193 | `assert blk["numerator"] == 615 and blk["denominator"] == 956` |
| `tests/test_test_debt_taxonomy_633.py` | 11 | `assert m.BATCH_HARD_RE.search("assert batch == 629") is not None` |

→ 长期方案：改为动态读 baseline/status（见 §五.1）。

## 三、环境依赖型

含 skipif 或环境判断的测试文件：**117** 个

| 文件 | skipif 数 |
|---|---|
| `tests/conftest.py` | 0 |
| `tests/test_585_attack_regression_601.py` | 0 |
| `tests/test_618_gate.py` | 0 |
| `tests/test_619_a1.py` | 0 |
| `tests/test_619_a2.py` | 0 |
| `tests/test_619_a3.py` | 0 |
| `tests/test_619_b2.py` | 0 |
| `tests/test_619_b3.py` | 0 |
| `tests/test_619_b4.py` | 0 |
| `tests/test_619_gate.py` | 0 |
| `tests/test_620_a2.py` | 0 |
| `tests/test_620_a3.py` | 0 |
| `tests/test_620_a4.py` | 0 |
| `tests/test_620_b3.py` | 0 |
| `tests/test_620_c2.py` | 0 |
| `tests/test_620_c3.py` | 0 |
| `tests/test_620_gate.py` | 0 |
| `tests/test_621_a2.py` | 0 |
| `tests/test_621_a3.py` | 0 |
| `tests/test_621_a4.py` | 0 |
| `tests/test_621_b1.py` | 0 |
| `tests/test_621_c2.py` | 0 |
| `tests/test_621_c3.py` | 0 |
| `tests/test_621_d1.py` | 0 |
| `tests/test_621_d2.py` | 0 |
| `tests/test_621_d3.py` | 0 |
| `tests/test_621_gate.py` | 0 |
| `tests/test_622_a1.py` | 0 |
| `tests/test_622_a2.py` | 0 |
| `tests/test_622_a3.py` | 0 |
| `tests/test_622_a4.py` | 0 |
| `tests/test_622_a5.py` | 0 |
| `tests/test_622_c1.py` | 0 |
| `tests/test_622_c2.py` | 0 |
| `tests/test_622_c3.py` | 0 |
| `tests/test_622_d1.py` | 0 |
| `tests/test_622_d2.py` | 0 |
| `tests/test_622_e1.py` | 0 |
| `tests/test_622_e2.py` | 0 |
| `tests/test_622_gate.py` | 0 |
| `tests/test_adversarial_loop_round5_624.py` | 0 |
| `tests/test_atom_evidence_replay.py` | 0 |
| `tests/test_attack_round8_629.py` | 0 |
| `tests/test_attack_surface_axes_630.py` | 0 |
| `tests/test_authority_v2_switch_627.py` | 0 |
| `tests/test_autoimmune_auto_fill_631.py` | 0 |
| `tests/test_autoimmune_diagnose_630.py` | 0 |
| `tests/test_autoimmune_framework_629.py` | 0 |
| `tests/test_autoimmune_human_queue_631.py` | 0 |
| `tests/test_autoimmune_probe_629.py` | 0 |
| `tests/test_baseline_630.py` | 0 |
| `tests/test_baseline_631.py` | 0 |
| `tests/test_blind_review_backfill_627.py` | 0 |
| `tests/test_blind_review_v1_626.py` | 0 |
| `tests/test_build_reproducibility_603.py` | 0 |
| `tests/test_build_reproducibility_608.py` | 2 |
| `tests/test_ccache_prefix.py` | 1 |
| `tests/test_ci_pytest_fix_625.py` | 1 |
| `tests/test_ci_pytest_triage_631.py` | 0 |
| `tests/test_cli_tools_check_624.py` | 0 |

→ 长期方案：`conftest.py` 统一 skipif 工厂（见 §五.2）。

## 四、快照测试

引用快照的测试文件：**25** 个

- `tests/conftest.py`
- `tests/test_618_c2.py`
- `tests/test_618_c4.py`
- `tests/test_618_gate.py`
- `tests/test_artifact_snapshot.py`
- `tests/test_backup.py`
- `tests/test_debt_inventory_633.py`
- `tests/test_doc_lint.py`
- `tests/test_golden_classify.py`
- `tests/test_golden_lock_proposal_613.py`
- `tests/test_governance_supply_chain_610.py`
- `tests/test_learner_mastery_update_613.py`
- `tests/test_learner_twin_gate_628.py`
- `tests/test_metrics_collector_curves.py`
- `tests/test_metrics_grounded_status_610.py`
- `tests/test_mutation_fuzz.py`
- `tests/test_mutation_shape_588.py`
- `tests/test_observability.py`
- `tests/test_output_snapshots.py`
- `tests/test_pack_review_zip_626.py`
- `tests/test_pollution_guard_session_632.py`
- `tests/test_review_pack_v2_626.py`
- `tests/test_snapshot_integrity_ci_626.py`
- `tests/test_snapshot_manifest.py`
- `tests/test_toolchain_regressions.py`

→ 长期方案：`--update-snapshots` 触发式更新（见 §五.3）。

## 五、长期方案（设计，不落地）

1. **跨批脆弱型 → 动态读基线**：把断言里的硬编码旧数字改为从 `_auto/status.json`、`data/<batch>_baseline.json` 或被测工具自身输出动态取值；改造点集中在 `tests/test_*_6[01]*.py` 中含 `== 6XX` 的断言行（见下清单）。
2. **环境依赖型 → conftest.py 统一 skipif**：在 `tests/conftest.py` 定义 `requires(*paths)` 与 `requires_tool(*names)` 工厂，返回 `pytest.mark.skipif`；各测试改用装饰器而非 内联 os.path.exists 判断，统一 reason 文案，避免逐个漂移。
3. **快照测试 → 定期更新机制**：给 `test_output_snapshots` 加 `--update-snapshots` 触发（pytest 自定义选项），CI 默认只比不更；触发条件：被快照对象的工具语义版本变更后由人手动跑。
4. **slow 测试 → 分层**：CI `-m 'not slow'` 已隔离；slow 组加独立 job（夜间/手动触发），避免拖慢 PR 反馈。

## 六、诚实登记

1. 本工具**只静态分类**，不运行测试、**不改任何测试**；
2. slow/环境依赖/snapshot 判定为**正则启发式**（可能漏判）；
3. 跨批脆弱清单按「assert 行含 6[12]X 数字」口径，是**上界**（含合法引用旧批号者）；
4. 长期方案**只写设计**，是否实施交 634/人。
