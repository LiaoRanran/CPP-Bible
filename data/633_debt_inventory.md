# 633 任务0 · 全量债务盘点（静态扫描）

> 只做静态扫描，不跑 pytest（留给 A2）。本表是 633 后续所有清理任务的输入。

## 一、化债前快照（量化指标）

| 指标 | 值 |
|---|---|
| 工作区脏文件数 | 65 |
| 工具总数 | 370 |
| 无 --check 工具数 | 82 |
| TODO/FIXME 总数 | 35 |
| 密钥文件数 | 1 |
| 死链接数 | 0 |
| 待 push commit 数 | 47 |

## 二、汇总矩阵（类别 × 严重度）

| 类别 | P0 | P1 | P2 | P3 | 小计 |
|---|---|---|---|---|---|
| CI/测试债 | 0 | 24 | 0 | 14 | 38 |
| 工具债 | 0 | 77 | 29 | 240 | 346 |
| 数据债 | 0 | 0 | 35 | 0 | 35 |
| 安全债 | 0 | 1 | 1 | 0 | 2 |
| 文档债 | 0 | 9 | 0 | 0 | 9 |
| git债 | 0 | 1 | 1 | 0 | 2 |
| 协议债 | 0 | 2 | 1 | 1 | 4 |
| **合计** | 0 | 114 | 67 | 255 | 436 |

## 三、各维度债务明细

### CI/测试债（38 项）

| ID | 严重度 | 描述 | 位置 | 根因 | 处置建议 | 工作量 |
|---|---|---|---|---|---|---|
| CI-001 | P1 | 硬编码批次号断言：assert len(g.CHECK_TOOLS) == 10  # 617 三件 + 618 七件 | `tests/test_618_gate.py:63` | 断言绑定当时最新批次 | 改相对断言或从 status.json/baseline 动态读 | S |
| CI-002 | P1 | 硬编码批次号断言：assert res["log_entries"] == 418   # 624 D3：622 D1  | `tests/test_620_c3.py:103` | 断言绑定当时最新批次 | 改相对断言或从 status.json/baseline 动态读 | S |
| CI-003 | P1 | 硬编码批次号断言：assert ids[0] == "prop-621-001" | `tests/test_621_d1.py:42` | 断言绑定当时最新批次 | 改相对断言或从 status.json/baseline 动态读 | S |
| CI-004 | P1 | 硬编码批次号断言：assert ids[-1] == "prop-621-030" | `tests/test_621_d1.py:43` | 断言绑定当时最新批次 | 改相对断言或从 status.json/baseline 动态读 | S |
| CI-005 | P1 | 硬编码批次号断言：assert res["batch"]["count"] == 418   # 624 D3：622  | `tests/test_621_d2.py:79` | 断言绑定当时最新批次 | 改相对断言或从 status.json/baseline 动态读 | S |
| CI-006 | P1 | 硬编码批次号断言：assert m["mutation_id"] == f"MUT-629-R8-{i:02d}" | `tests/test_attack_round8_629.py:19` | 断言绑定当时最新批次 | 改相对断言或从 status.json/baseline 动态读 | S |
| CI-007 | P3 | 含 skipif（环境依赖，可能 CI 不成立） | `tests/test_build_reproducibility_608.py` | 依赖本地文件/编译器/网络 | 登记；E1 统一到 conftest.py skipif | M |
| CI-008 | P3 | 含 skipif（环境依赖，可能 CI 不成立） | `tests/test_ccache_prefix.py` | 依赖本地文件/编译器/网络 | 登记；E1 统一到 conftest.py skipif | M |
| CI-009 | P3 | 含 skipif（环境依赖，可能 CI 不成立） | `tests/test_ci_pytest_fix_625.py` | 依赖本地文件/编译器/网络 | 登记；E1 统一到 conftest.py skipif | M |
| CI-010 | P1 | 硬编码批次号断言：assert len(disp) == len(ex.load_exemptions())     # | `tests/test_exemption_disposal_616.py:15` | 断言绑定当时最新批次 | 改相对断言或从 status.json/baseline 动态读 | S |
| CI-011 | P1 | 硬编码批次号断言：assert len(rows) == len(ex.load_exemptions())     # | `tests/test_exemption_expiry_615.py:14` | 断言绑定当时最新批次 | 改相对断言或从 status.json/baseline 动态读 | S |
| CI-012 | P3 | 含 skipif（环境依赖，可能 CI 不成立） | `tests/test_governance_doc_guard_591.py` | 依赖本地文件/编译器/网络 | 登记；E1 统一到 conftest.py skipif | M |
| CI-013 | P3 | 含 skipif（环境依赖，可能 CI 不成立） | `tests/test_governance_self_hash_601.py` | 依赖本地文件/编译器/网络 | 登记；E1 统一到 conftest.py skipif | M |
| CI-014 | P1 | 硬编码批次号断言：assert len(rows) >= 10                       # 615  | `tests/test_human_decision_tracking_616.py:25` | 断言绑定当时最新批次 | 改相对断言或从 status.json/baseline 动态读 | S |
| CI-015 | P3 | 含 skipif（环境依赖，可能 CI 不成立） | `tests/test_json_output.py` | 依赖本地文件/编译器/网络 | 登记；E1 统一到 conftest.py skipif | M |
| CI-016 | P1 | 硬编码批次号断言：assert called["n"] == 1, "collect() 必须调用 610 采集器一次" | `tests/test_metrics_grounded_status_610.py:82` | 断言绑定当时最新批次 | 改相对断言或从 status.json/baseline 动态读 | S |
| CI-017 | P1 | 硬编码批次号断言：assert by.get("ITEM_OPEN") == 30                 #  | `tests/test_migrate_to_v2_626.py:43` | 断言绑定当时最新批次 | 改相对断言或从 status.json/baseline 动态读 | S |
| CI-018 | P1 | 硬编码批次号断言：assert g["solver_recompute"]["in"] == 121           | `tests/test_modify_mode_611.py:138` | 断言绑定当时最新批次 | 改相对断言或从 status.json/baseline 动态读 | S |
| CI-019 | P1 | 硬编码批次号断言：assert (variants, blocked, escaped, n_a, strict) == | `tests/test_mutation_fuzz_report.py:45` | 断言绑定当时最新批次 | 改相对断言或从 status.json/baseline 动态读 | S |
| CI-020 | P3 | 含 slow 标记测试 | `tests/test_mutation_selfcheck_589.py` | 运行耗时长 | 登记；E1 评估优化 | M |
| CI-021 | P3 | 含 skipif（环境依赖，可能 CI 不成立） | `tests/test_pe_timestamp_caliber_611.py` | 依赖本地文件/编译器/网络 | 登记；E1 统一到 conftest.py skipif | M |
| CI-022 | P3 | 含 slow 标记测试 | `tests/test_pe_timestamp_caliber_611.py` | 运行耗时长 | 登记；E1 评估优化 | M |
| CI-023 | P1 | 硬编码批次号断言：assert rep["total"] == 67   # 625 A3：624 B1 后规则数 63 | `tests/test_poison_exemptions_581.py:112` | 断言绑定当时最新批次 | 改相对断言或从 status.json/baseline 动态读 | S |
| CI-024 | P3 | 含 skipif（环境依赖，可能 CI 不成立） | `tests/test_replay_invariants_605.py` | 依赖本地文件/编译器/网络 | 登记；E1 统一到 conftest.py skipif | M |
| CI-025 | P1 | 硬编码批次号断言：assert doc["batch"] == "613" | `tests/test_run_613_gate.py:62` | 断言绑定当时最新批次 | 改相对断言或从 status.json/baseline 动态读 | S |
| CI-026 | P1 | 硬编码批次号断言：assert st["batch"] == "614" and st["status"] == "aw | `tests/test_run_614_gate.py:42` | 断言绑定当时最新批次 | 改相对断言或从 status.json/baseline 动态读 | S |
| CI-027 | P1 | 硬编码批次号断言：assert st["last_completed_batch"] == 615 and st["hi | `tests/test_run_615_gate.py:31` | 断言绑定当时最新批次 | 改相对断言或从 status.json/baseline 动态读 | S |
| CI-028 | P1 | 硬编码批次号断言：assert rc_batch == 0, "只跑本批会漏检存量债（正是 622 的口径陷阱）" | `tests/test_run_623_gate.py:54` | 断言绑定当时最新批次 | 改相对断言或从 status.json/baseline 动态读 | S |
| CI-029 | P1 | 硬编码批次号断言：assert status["batch"] >= 628 and status["state"] = | `tests/test_run_628_gate_628.py:89` | 断言绑定当时最新批次 | 改相对断言或从 status.json/baseline 动态读 | S |
| CI-030 | P1 | 硬编码批次号断言：assert status["last_completed_batch"] >= 628 | `tests/test_run_628_gate_628.py:90` | 断言绑定当时最新批次 | 改相对断言或从 status.json/baseline 动态读 | S |
| CI-031 | P1 | 硬编码批次号断言：assert len(B.BASELINE_FAILURES) == 11, "629 修正后的既有失 | `tests/test_run_629_gate.py:67` | 断言绑定当时最新批次 | 改相对断言或从 status.json/baseline 动态读 | S |
| CI-032 | P1 | 硬编码批次号断言：assert p.returncode == 0, "629 不得改动 ci.yml" | `tests/test_run_629_gate.py:87` | 断言绑定当时最新批次 | 改相对断言或从 status.json/baseline 动态读 | S |
| CI-033 | P3 | 含 skipif（环境依赖，可能 CI 不成立） | `tests/test_s1_s6.py` | 依赖本地文件/编译器/网络 | 登记；E1 统一到 conftest.py skipif | M |
| CI-034 | P3 | 含 skipif（环境依赖，可能 CI 不成立） | `tests/test_sandbox_apply_622_d2_632.py` | 依赖本地文件/编译器/网络 | 登记；E1 统一到 conftest.py skipif | M |
| CI-035 | P1 | 硬编码批次号断言：assert tri["total"] >= 11, f"629 基线 11 项，实测 {tri['t | `tests/test_stale_test_triage_630.py:45` | 断言绑定当时最新批次 | 改相对断言或从 status.json/baseline 动态读 | S |
| CI-036 | P1 | 硬编码批次号断言：assert blk["numerator"] == 615 and blk["denominator | `tests/test_stat_bounds.py:193` | 断言绑定当时最新批次 | 改相对断言或从 status.json/baseline 动态读 | S |
| CI-037 | P3 | 含 skipif（环境依赖，可能 CI 不成立） | `tests/test_supply_chain_chain_601.py` | 依赖本地文件/编译器/网络 | 登记；E1 统一到 conftest.py skipif | M |
| CI-038 | P3 | 含 skipif（环境依赖，可能 CI 不成立） | `tests/test_task_queue.py` | 依赖本地文件/编译器/网络 | 登记；E1 统一到 conftest.py skipif | M |

### 工具债（346 项）

| ID | 严重度 | 描述 | 位置 | 根因 | 处置建议 | 工作量 |
|---|---|---|---|---|---|---|
| TOOL-001 | P3 | 命名不符合 *_6XX.py 批次规范 | `tools/612_baseline.py` | 命名约定不统一 | 登记；不重命名（引用成本高） | L |
| TOOL-002 | P3 | 命名不符合 *_6XX.py 批次规范 | `tools/613_baseline.py` | 命名约定不统一 | 登记；不重命名（引用成本高） | L |
| TOOL-003 | P1 | CLI 无 --check（被引用，仍在使用） | `tools/adversarial_regression.py` | 旧工具未补只读自检 | 加 --check（只读，见 B2） | S |
| TOOL-004 | P3 | 命名不符合 *_6XX.py 批次规范 | `tools/adversarial_regression.py` | 命名约定不统一 | 登记；不重命名（引用成本高） | L |
| TOOL-005 | P3 | 命名不符合 *_6XX.py 批次规范 | `tools/argument_audit.py` | 命名约定不统一 | 登记；不重命名（引用成本高） | L |
| TOOL-006 | P3 | 命名不符合 *_6XX.py 批次规范 | `tools/argument_graph_analysis.py` | 命名约定不统一 | 登记；不重命名（引用成本高） | L |
| TOOL-007 | P1 | CLI 无 --check（被引用，仍在使用） | `tools/artifact_version_stamp.py` | 旧工具未补只读自检 | 加 --check（只读，见 B2） | S |
| TOOL-008 | P3 | 命名不符合 *_6XX.py 批次规范 | `tools/artifact_version_stamp.py` | 命名约定不统一 | 登记；不重命名（引用成本高） | L |
| TOOL-009 | P1 | CLI 无 --check（被引用，仍在使用） | `tools/asm_prepush_guard.py` | 旧工具未补只读自检 | 加 --check（只读，见 B2） | S |
| TOOL-010 | P3 | 命名不符合 *_6XX.py 批次规范 | `tools/asm_prepush_guard.py` | 命名约定不统一 | 登记；不重命名（引用成本高） | L |
| TOOL-011 | P1 | CLI 无 --check（被引用，仍在使用） | `tools/asm_regen.py` | 旧工具未补只读自检 | 加 --check（只读，见 B2） | S |
| TOOL-012 | P3 | 命名不符合 *_6XX.py 批次规范 | `tools/asm_regen.py` | 命名约定不统一 | 登记；不重命名（引用成本高） | L |
| TOOL-013 | P1 | CLI 无 --check（被引用，仍在使用） | `tools/asm_repro_spotcheck.py` | 旧工具未补只读自检 | 加 --check（只读，见 B2） | S |
| TOOL-014 | P3 | 命名不符合 *_6XX.py 批次规范 | `tools/asm_repro_spotcheck.py` | 命名约定不统一 | 登记；不重命名（引用成本高） | L |
| TOOL-015 | P3 | 命名不符合 *_6XX.py 批次规范 | `tools/atom_coverage_map.py` | 命名约定不统一 | 登记；不重命名（引用成本高） | L |
| TOOL-016 | P3 | 超过 500 行的巨型文件（2443 行） | `tools/atom_evidence_replay.py` | 职责未拆分 | 登记；不拆分（风险高） | L |
| TOOL-017 | P3 | 命名不符合 *_6XX.py 批次规范 | `tools/atom_evidence_replay.py` | 命名约定不统一 | 登记；不重命名（引用成本高） | L |
| TOOL-018 | P3 | 命名不符合 *_6XX.py 批次规范 | `tools/attack_edge_generator.py` | 命名约定不统一 | 登记；不重命名（引用成本高） | L |
| TOOL-019 | P2 | 标记：print("用法：review-group MIS-XXX --props '卡id::prop-1,卡id:: | `tools/attack_edge_review.py:463` | 历史遗留未决项 | 逐条评估：能修则修，否则登记 | M |
| TOOL-020 | P3 | 超过 500 行的巨型文件（562 行） | `tools/attack_edge_review.py` | 职责未拆分 | 登记；不拆分（风险高） | L |
| TOOL-021 | P3 | 命名不符合 *_6XX.py 批次规范 | `tools/attack_edge_review.py` | 命名约定不统一 | 登记；不重命名（引用成本高） | L |
| TOOL-022 | P3 | 命名不符合 *_6XX.py 批次规范 | `tools/attack_surface_taxonomy.py` | 命名约定不统一 | 登记；不重命名（引用成本高） | L |
| TOOL-023 | P2 | 标记：只能当 TODO 债清单。</div></div>""" | `tools/autoimmune_dashboard_629.py:122` | 历史遗留未决项 | 逐条评估：能修则修，否则登记 | M |
| TOOL-024 | P2 | 标记："**TODO 债清单**（列「还差哪些字段」），不是质量评级。", | `tools/autoimmune_rate_framework.py:191` | 历史遗留未决项 | 逐条评估：能修则修，否则登记 | M |
| TOOL-025 | P3 | 命名不符合 *_6XX.py 批次规范 | `tools/autoimmune_rate_framework.py` | 命名约定不统一 | 登记；不重命名（引用成本高） | L |
| TOOL-026 | P1 | CLI 无 --check（被引用，仍在使用） | `tools/backup.py` | 旧工具未补只读自检 | 加 --check（只读，见 B2） | S |
| TOOL-027 | P3 | 命名不符合 *_6XX.py 批次规范 | `tools/backup.py` | 命名约定不统一 | 登记；不重命名（引用成本高） | L |
| TOOL-028 | P3 | 命名不符合 *_6XX.py 批次规范 | `tools/bkt_solver.py` | 命名约定不统一 | 登记；不重命名（引用成本高） | L |
| TOOL-029 | P1 | CLI 无 --check（被引用，仍在使用） | `tools/book_asm_freshness.py` | 旧工具未补只读自检 | 加 --check（只读，见 B2） | S |
| TOOL-030 | P3 | 命名不符合 *_6XX.py 批次规范 | `tools/book_asm_freshness.py` | 命名约定不统一 | 登记；不重命名（引用成本高） | L |
| TOOL-031 | P2 | 标记：3. 孤儿原子引用：Book 中 <atom>XXX</atom> 指向不存在的原子 → block | `tools/book_atom_sync.py:7` | 历史遗留未决项 | 逐条评估：能修则修，否则登记 | M |
| TOOL-032 | P2 | 标记：python tools/book_atom_sync.py --atom XXX   # 检查某颗原子的同步状态 | `tools/book_atom_sync.py:12` | 历史遗留未决项 | 逐条评估：能修则修，否则登记 | M |
| TOOL-033 | P3 | 命名不符合 *_6XX.py 批次规范 | `tools/book_atom_sync.py` | 命名约定不统一 | 登记；不重命名（引用成本高） | L |
| TOOL-034 | P3 | 命名不符合 *_6XX.py 批次规范 | `tools/bridge_edge_candidates.py` | 命名约定不统一 | 登记；不重命名（引用成本高） | L |
| TOOL-035 | P3 | 命名不符合 *_6XX.py 批次规范 | `tools/bridge_edge_impact.py` | 命名约定不统一 | 登记；不重命名（引用成本高） | L |
| TOOL-036 | P3 | 命名不符合 *_6XX.py 批次规范 | `tools/bridge_edge_pre_annotate.py` | 命名约定不统一 | 登记；不重命名（引用成本高） | L |
| TOOL-037 | P3 | 命名不符合 *_6XX.py 批次规范 | `tools/bridge_edge_review.py` | 命名约定不统一 | 登记；不重命名（引用成本高） | L |
| TOOL-038 | P3 | 命名不符合 *_6XX.py 批次规范 | `tools/build_reproducibility_deep.py` | 命名约定不统一 | 登记；不重命名（引用成本高） | L |
| TOOL-039 | P2 | 标记："""章节内出现最多的完整 [实现·XXX] 引注，作为实现徽章的限定词投票。""" | `tools/caption_truncation_audit.py:160` | 历史遗留未决项 | 逐条评估：能修则修，否则登记 | M |
| TOOL-040 | P3 | 命名不符合 *_6XX.py 批次规范 | `tools/caption_truncation_audit.py` | 命名约定不统一 | 登记；不重命名（引用成本高） | L |
| TOOL-041 | P1 | CLI 无 --check（被引用，仍在使用） | `tools/chapter_compile_check.py` | 旧工具未补只读自检 | 加 --check（只读，见 B2） | S |
| TOOL-042 | P3 | 命名不符合 *_6XX.py 批次规范 | `tools/chapter_compile_check.py` | 命名约定不统一 | 登记；不重命名（引用成本高） | L |
| TOOL-043 | P1 | CLI 无 --check（被引用，仍在使用） | `tools/chapter_lint.py` | 旧工具未补只读自检 | 加 --check（只读，见 B2） | S |
| TOOL-044 | P2 | 标记：- 有没有遗留 TBD/TODO/FIXME/XXX 标记？ | `tools/chapter_lint.py:16` | 历史遗留未决项 | 逐条评估：能修则修，否则登记 | M |
| TOOL-045 | P2 | 标记：LOW  = 3   (长代码块零注释、TODO/XXX 标记) | `tools/chapter_lint.py:36` | 历史遗留未决项 | 逐条评估：能修则修，否则登记 | M |
| TOOL-046 | P2 | 标记：TODO_RE = re.compile(r"\b(TBD|TODO|FIXME|XXX)\b") | `tools/chapter_lint.py:73` | 历史遗留未决项 | 逐条评估：能修则修，否则登记 | M |
| TOOL-047 | P3 | 命名不符合 *_6XX.py 批次规范 | `tools/chapter_lint.py` | 命名约定不统一 | 登记；不重命名（引用成本高） | L |
| TOOL-048 | P1 | CLI 无 --check（被引用，仍在使用） | `tools/check_citations.py` | 旧工具未补只读自检 | 加 --check（只读，见 B2） | S |
| TOOL-049 | P3 | 命名不符合 *_6XX.py 批次规范 | `tools/check_citations.py` | 命名约定不统一 | 登记；不重命名（引用成本高） | L |
| TOOL-050 | P1 | CLI 无 --check（被引用，仍在使用） | `tools/ci_local_precheck.py` | 旧工具未补只读自检 | 加 --check（只读，见 B2） | S |
| TOOL-051 | P3 | 命名不符合 *_6XX.py 批次规范 | `tools/ci_local_precheck.py` | 命名约定不统一 | 登记；不重命名（引用成本高） | L |
| TOOL-052 | P1 | CLI 无 --check（被引用，仍在使用） | `tools/clean_root_artifacts.py` | 旧工具未补只读自检 | 加 --check（只读，见 B2） | S |
| TOOL-053 | P3 | 命名不符合 *_6XX.py 批次规范 | `tools/clean_root_artifacts.py` | 命名约定不统一 | 登记；不重命名（引用成本高） | L |
| TOOL-054 | P3 | 命名不符合 *_6XX.py 批次规范 | `tools/codeblock_style.py` | 命名约定不统一 | 登记；不重命名（引用成本高） | L |
| TOOL-055 | P1 | CLI 无 --check（被引用，仍在使用） | `tools/collect_reports.py` | 旧工具未补只读自检 | 加 --check（只读，见 B2） | S |
| TOOL-056 | P3 | 命名不符合 *_6XX.py 批次规范 | `tools/collect_reports.py` | 命名约定不统一 | 登记；不重命名（引用成本高） | L |
| TOOL-057 | P1 | CLI 无 --check（被引用，仍在使用） | `tools/comment_blocks.py` | 旧工具未补只读自检 | 加 --check（只读，见 B2） | S |
| TOOL-058 | P3 | 命名不符合 *_6XX.py 批次规范 | `tools/comment_blocks.py` | 命名约定不统一 | 登记；不重命名（引用成本高） | L |
| TOOL-059 | P1 | CLI 无 --check（被引用，仍在使用） | `tools/compile_all.py` | 旧工具未补只读自检 | 加 --check（只读，见 B2） | S |
| TOOL-060 | P3 | 超过 500 行的巨型文件（553 行） | `tools/compile_all.py` | 职责未拆分 | 登记；不拆分（风险高） | L |
| … | | 另有 286 项（见 JSON） | | | | |

### 数据债（35 项）

| ID | 严重度 | 描述 | 位置 | 根因 | 处置建议 | 工作量 |
|---|---|---|---|---|---|---|
| DATA-001 | P2 | 未跟踪的大文件（753936KB） | `data/logs/2026-09-18.jsonl` | 运行时产物未清理 | 登记；按 §零.17 移至 data/_archive_633/ | S |
| DATA-002 | P2 | 未跟踪的大文件（751474KB） | `data/logs/2026-09-19.jsonl` | 运行时产物未清理 | 登记；按 §零.17 移至 data/_archive_633/ | S |
| DATA-003 | P2 | 未跟踪的大文件（64012KB） | `data/logs/2026-09-20.jsonl` | 运行时产物未清理 | 登记；按 §零.17 移至 data/_archive_633/ | S |
| DATA-004 | P2 | 未跟踪的大文件（18668KB） | `data/logs/2026-09-21.jsonl` | 运行时产物未清理 | 登记；按 §零.17 移至 data/_archive_633/ | S |
| DATA-005 | P2 | 未跟踪的大文件（55139KB） | `data/logs/2026-09-22.jsonl` | 运行时产物未清理 | 登记；按 §零.17 移至 data/_archive_633/ | S |
| DATA-006 | P2 | 未跟踪的大文件（242235KB） | `data/logs/2026-09-23.jsonl` | 运行时产物未清理 | 登记；按 §零.17 移至 data/_archive_633/ | S |
| DATA-007 | P2 | 未跟踪的大文件（134160KB） | `data/logs/2026-09-24.jsonl` | 运行时产物未清理 | 登记；按 §零.17 移至 data/_archive_633/ | S |
| DATA-008 | P2 | JSON 引用不存在的文件：evidence/hist/EV-MEM-003.md | `data/pck_hash_drift_627.json` | 引用漂移 | 登记；交 C2/D 线核对 | M |
| DATA-009 | P2 | JSON 引用不存在的文件：atoms/_t_x.md | `data/test_dependency_graph.json` | 引用漂移 | 登记；交 C2/D 线核对 | M |
| DATA-010 | P2 | JSON 引用不存在的文件：data/golden_state.json | `data/backups/2026-09-14-212013/MANIFEST.json` | 引用漂移 | 登记；交 C2/D 线核对 | M |
| DATA-011 | P2 | JSON 引用不存在的文件：data/golden_state.json | `data/backups/2026-09-14-215711/MANIFEST.json` | 引用漂移 | 登记；交 C2/D 线核对 | M |
| DATA-012 | P2 | JSON 引用不存在的文件：data/golden_state.json | `data/backups/2026-09-14-220446/MANIFEST.json` | 引用漂移 | 登记；交 C2/D 线核对 | M |
| DATA-013 | P2 | JSON 引用不存在的文件：data/golden_state.json | `data/backups/2026-09-14-221517/MANIFEST.json` | 引用漂移 | 登记；交 C2/D 线核对 | M |
| DATA-014 | P2 | JSON 引用不存在的文件：data/golden_state.json | `data/backups/2026-09-14-225340/MANIFEST.json` | 引用漂移 | 登记；交 C2/D 线核对 | M |
| DATA-015 | P2 | JSON 引用不存在的文件：data/golden_state.json | `data/backups/2026-09-14-231249/MANIFEST.json` | 引用漂移 | 登记；交 C2/D 线核对 | M |
| DATA-016 | P2 | JSON 引用不存在的文件：data/golden_state.json | `data/backups/2026-09-14-233428/MANIFEST.json` | 引用漂移 | 登记；交 C2/D 线核对 | M |
| DATA-017 | P2 | JSON 引用不存在的文件：data/golden_state.json | `data/backups/2026-09-15-000140/MANIFEST.json` | 引用漂移 | 登记；交 C2/D 线核对 | M |
| DATA-018 | P2 | JSON 引用不存在的文件：data/golden_state.json | `data/backups/2026-09-15-112627/MANIFEST.json` | 引用漂移 | 登记；交 C2/D 线核对 | M |
| DATA-019 | P2 | JSON 引用不存在的文件：data/golden_state.json | `data/backups/2026-09-15-113432/MANIFEST.json` | 引用漂移 | 登记；交 C2/D 线核对 | M |
| DATA-020 | P2 | JSON 引用不存在的文件：data/golden_state.json | `data/backups/2026-09-15-114415/MANIFEST.json` | 引用漂移 | 登记；交 C2/D 线核对 | M |
| DATA-021 | P2 | JSON 引用不存在的文件：data/golden_state.json | `data/backups/2026-09-15-115121/MANIFEST.json` | 引用漂移 | 登记；交 C2/D 线核对 | M |
| DATA-022 | P2 | JSON 引用不存在的文件：data/golden_state.json | `data/backups/2026-09-15-115838/MANIFEST.json` | 引用漂移 | 登记；交 C2/D 线核对 | M |
| DATA-023 | P2 | JSON 引用不存在的文件：data/golden_state.json | `data/backups/2026-09-15-120605/MANIFEST.json` | 引用漂移 | 登记；交 C2/D 线核对 | M |
| DATA-024 | P2 | JSON 引用不存在的文件：data/golden_state.json | `data/backups/2026-09-15-122042/MANIFEST.json` | 引用漂移 | 登记；交 C2/D 线核对 | M |
| DATA-025 | P2 | JSON 引用不存在的文件：data/golden_state.json | `data/backups/2026-09-19-151319/MANIFEST.json` | 引用漂移 | 登记；交 C2/D 线核对 | M |
| DATA-026 | P2 | JSON 引用不存在的文件：data/golden_state.json | `data/backups/2026-09-19-151957/MANIFEST.json` | 引用漂移 | 登记；交 C2/D 线核对 | M |
| DATA-027 | P2 | JSON 引用不存在的文件：data/golden_state.json | `data/backups/2026-09-19-160136/MANIFEST.json` | 引用漂移 | 登记；交 C2/D 线核对 | M |
| DATA-028 | P2 | JSON 引用不存在的文件：data/golden_state.json | `data/backups/2026-09-19-164729/MANIFEST.json` | 引用漂移 | 登记；交 C2/D 线核对 | M |
| DATA-029 | P2 | JSON 引用不存在的文件：data/golden_state.json | `data/backups/2026-09-20-154048/MANIFEST.json` | 引用漂移 | 登记；交 C2/D 线核对 | M |
| DATA-030 | P2 | JSON 引用不存在的文件：data/golden_state.json | `data/backups/2026-09-20-194029/MANIFEST.json` | 引用漂移 | 登记；交 C2/D 线核对 | M |
| DATA-031 | P2 | JSON 引用不存在的文件：data/golden_state.json | `data/backups/2026-09-20-194801/MANIFEST.json` | 引用漂移 | 登记；交 C2/D 线核对 | M |
| DATA-032 | P2 | JSON 引用不存在的文件：data/golden_state.json | `data/backups/2026-09-20-195428/MANIFEST.json` | 引用漂移 | 登记；交 C2/D 线核对 | M |
| DATA-033 | P2 | JSON 引用不存在的文件：data/golden_state.json | `data/backups/2026-09-20-200018/MANIFEST.json` | 引用漂移 | 登记；交 C2/D 线核对 | M |
| DATA-034 | P2 | JSON 引用不存在的文件：data/golden_state.json | `data/backups/2026-09-20-201021/MANIFEST.json` | 引用漂移 | 登记；交 C2/D 线核对 | M |
| DATA-035 | P2 | JSON 引用不存在的文件：data/golden_state.json | `data/backups/2026-09-20-201038/MANIFEST.json` | 引用漂移 | 登记；交 C2/D 线核对 | M |

### 安全债（2 项）

| ID | 严重度 | 描述 | 位置 | 根因 | 处置建议 | 工作量 |
|---|---|---|---|---|---|---|
| SEC-001 | P1 | 密钥文件（已忽略，未入库） | `data/vsa_secret.key` | 明文密钥落盘 | 备份 + 评估影响（C1）；确认 ignore 覆盖 | S |
| SEC-002 | P2 | 疑似硬编码机密赋值（值已脱敏） | `tools/doc_lint.py:105` | 可能与密钥/令牌相关 | 人工核对；确认是真实机密则轮换 | M |

### 文档债（9 项）

| ID | 严重度 | 描述 | 位置 | 根因 | 处置建议 | 工作量 |
|---|---|---|---|---|---|---|
| DOC-001 | P1 | 死链接 → ATOM-MEM-PERF-001.md | `References/architecture_架构演进/306_原子知识图谱与关系网络架构调研_从扁平列表到可导航知识体系.md` | 目标文件被删除/重命名 | 更新为新路径或标注『已迁移』（D2） | S |
| DOC-002 | P1 | 死链接 → ATOM-MEM-UNIQUE-002.md | `References/architecture_架构演进/306_原子知识图谱与关系网络架构调研_从扁平列表到可导航知识体系.md` | 目标文件被删除/重命名 | 更新为新路径或标注『已迁移』（D2） | S |
| DOC-003 | P1 | 死链接 → ATOM-MEM-PERF-003.md | `References/architecture_架构演进/306_原子知识图谱与关系网络架构调研_从扁平列表到可导航知识体系.md` | 目标文件被删除/重命名 | 更新为新路径或标注『已迁移』（D2） | S |
| DOC-004 | P1 | 死链接 → file:///C:/CodeLearnling/note/note/C++/CPP-Bible/tools | `References/architecture_架构演进/368_独立红队对抗报告.md` | 目标文件被删除/重命名 | 更新为新路径或标注『已迁移』（D2） | S |
| DOC-005 | P1 | 死链接 → file:///C:/CodeLearnling/note/note/C++/CPP-Bible/tools | `References/architecture_架构演进/368_独立红队对抗报告.md` | 目标文件被删除/重命名 | 更新为新路径或标注『已迁移』（D2） | S |
| DOC-006 | P1 | 死链接 → file:///C:/CodeLearnling/note/note/C++/CPP-Bible/tools | `References/architecture_架构演进/368_独立红队对抗报告.md` | 目标文件被删除/重命名 | 更新为新路径或标注『已迁移』（D2） | S |
| DOC-007 | P1 | 死链接 → file:///C:/CodeLearnling/note/note/C++/CPP-Bible/tools | `References/architecture_架构演进/368_独立红队对抗报告.md` | 目标文件被删除/重命名 | 更新为新路径或标注『已迁移』（D2） | S |
| DOC-008 | P1 | 死链接 → file:///C:/CodeLearnling/note/note/C++/CPP-Bible/tools | `References/architecture_架构演进/368_独立红队对抗报告.md` | 目标文件被删除/重命名 | 更新为新路径或标注『已迁移』（D2） | S |
| DOC-009 | P1 | 死链接 → file:///C:/CodeLearnling/note/note/C++/CPP-Bible/tools | `References/architecture_架构演进/368_独立红队对抗报告.md` | 目标文件被删除/重命名 | 更新为新路径或标注『已迁移』（D2） | S |

### git债（2 项）

| ID | 严重度 | 描述 | 位置 | 根因 | 处置建议 | 工作量 |
|---|---|---|---|---|---|---|
| GIT-001 | P2 | 工作区残留 24 项（§零.12 禁提交） | `git status` | 前批次调研/临时产物未清理 | 登记；F1 收工时确认不提交；D 线评估是否归档 | M |
| GIT-002 | P1 | 其余工作区改动 41 项（需逐项判定假脏/真脏） | `git status` | 前批次运行时产物 / 真脏未提交 | B1 逐项 git diff 判定：假脏还原，不确定登记 | M |

### 协议债（4 项）

| ID | 严重度 | 描述 | 位置 | 根因 | 处置建议 | 工作量 |
|---|---|---|---|---|---|---|
| PROTO-001 | P1 | _auto/status.json last_commit=29888f8f 与实际 HEAD=45c414cf 不一致 | `_auto/status.json` | 批次收工时未更新 status | F1 更新 status（last_completed_batch=633, next=634） | S |
| PROTO-002 | P1 | last_completed_batch=631 落后于实际（632 已完成） | `_auto/status.json` | 状态文件滞后 | F1 更新 | S |
| PROTO-003 | P3 | inbox 最新 633.md / outbox 最新 631.md | `_auto/{inbox,outbox}` | 批次对齐检查 | F1 产出 outbox/633.md | S |
| PROTO-004 | P2 | 625-632 验收报告含交人/待裁决关键词约 67 处 | `data/*_acceptance_report.md` | 历史交人项散落 | D1/D 线汇总为统一清单（633_handoff.md） | M |

## 四、本批可清理清单（P0+P1）

共 **114** 项。

| ID | 类别 | 严重度 | 描述 |
|---|---|---|---|
| CI-001 | CI/测试债 | P1 | 硬编码批次号断言：assert len(g.CHECK_TOOLS) == 10  # 617 三件 + 618 七件 |
| CI-002 | CI/测试债 | P1 | 硬编码批次号断言：assert res["log_entries"] == 418   # 624 D3：622 D1 逐条人审后 Auth |
| CI-003 | CI/测试债 | P1 | 硬编码批次号断言：assert ids[0] == "prop-621-001" |
| CI-004 | CI/测试债 | P1 | 硬编码批次号断言：assert ids[-1] == "prop-621-030" |
| CI-005 | CI/测试债 | P1 | 硬编码批次号断言：assert res["batch"]["count"] == 418   # 624 D3：622 D1 逐条人审后 A |
| CI-006 | CI/测试债 | P1 | 硬编码批次号断言：assert m["mutation_id"] == f"MUT-629-R8-{i:02d}" |
| CI-010 | CI/测试债 | P1 | 硬编码批次号断言：assert len(disp) == len(ex.load_exemptions())     # 624 D3：动态 |
| CI-011 | CI/测试债 | P1 | 硬编码批次号断言：assert len(rows) == len(ex.load_exemptions())     # 624 D3：动态 |
| CI-014 | CI/测试债 | P1 | 硬编码批次号断言：assert len(rows) >= 10                       # 615 七项 + 616 三 |
| CI-016 | CI/测试债 | P1 | 硬编码批次号断言：assert called["n"] == 1, "collect() 必须调用 610 采集器一次" |
| CI-017 | CI/测试债 | P1 | 硬编码批次号断言：assert by.get("ITEM_OPEN") == 30                 # 622 授权执行的  |
| CI-018 | CI/测试债 | P1 | 硬编码批次号断言：assert g["solver_recompute"]["in"] == 121          # 610 字段语义 |
| CI-019 | CI/测试债 | P1 | 硬编码批次号断言：assert (variants, blocked, escaped, n_a, strict) == (1188, 72 |
| CI-023 | CI/测试债 | P1 | 硬编码批次号断言：assert rep["total"] == 67   # 625 A3：624 B1 后规则数 63→67 |
| CI-025 | CI/测试债 | P1 | 硬编码批次号断言：assert doc["batch"] == "613" |
| CI-026 | CI/测试债 | P1 | 硬编码批次号断言：assert st["batch"] == "614" and st["status"] == "awaiting_rev |
| CI-027 | CI/测试债 | P1 | 硬编码批次号断言：assert st["last_completed_batch"] == 615 and st["history"][-1 |
| CI-028 | CI/测试债 | P1 | 硬编码批次号断言：assert rc_batch == 0, "只跑本批会漏检存量债（正是 622 的口径陷阱）" |
| CI-029 | CI/测试债 | P1 | 硬编码批次号断言：assert status["batch"] >= 628 and status["state"] == "awaitin |
| CI-030 | CI/测试债 | P1 | 硬编码批次号断言：assert status["last_completed_batch"] >= 628 |
| CI-031 | CI/测试债 | P1 | 硬编码批次号断言：assert len(B.BASELINE_FAILURES) == 11, "629 修正后的既有失败基线（首测 19  |
| CI-032 | CI/测试债 | P1 | 硬编码批次号断言：assert p.returncode == 0, "629 不得改动 ci.yml" |
| CI-035 | CI/测试债 | P1 | 硬编码批次号断言：assert tri["total"] >= 11, f"629 基线 11 项，实测 {tri['total']}" |
| CI-036 | CI/测试债 | P1 | 硬编码批次号断言：assert blk["numerator"] == 615 and blk["denominator"] == 956 |
| TOOL-003 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-007 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-009 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-011 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-013 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-026 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-029 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-041 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-043 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-048 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-050 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-052 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-055 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-057 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-059 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-062 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-064 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-066 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-071 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-074 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-078 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-081 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-084 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-088 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-090 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-095 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-097 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-103 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-114 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-116 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-118 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-122 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-124 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-127 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-130 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-138 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-141 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-144 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-146 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-152 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-163 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-172 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-174 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-184 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-187 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-197 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-203 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-208 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-216 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-220 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-223 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-231 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-235 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-238 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-241 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |
| TOOL-244 | 工具债 | P1 | CLI 无 --check（被引用，仍在使用） |

## 五、交人清单（P2+P3）

共 **322** 项。

| ID | 类别 | 严重度 | 描述 |
|---|---|---|---|
| CI-007 | CI/测试债 | P3 | 含 skipif（环境依赖，可能 CI 不成立） |
| CI-008 | CI/测试债 | P3 | 含 skipif（环境依赖，可能 CI 不成立） |
| CI-009 | CI/测试债 | P3 | 含 skipif（环境依赖，可能 CI 不成立） |
| CI-012 | CI/测试债 | P3 | 含 skipif（环境依赖，可能 CI 不成立） |
| CI-013 | CI/测试债 | P3 | 含 skipif（环境依赖，可能 CI 不成立） |
| CI-015 | CI/测试债 | P3 | 含 skipif（环境依赖，可能 CI 不成立） |
| CI-020 | CI/测试债 | P3 | 含 slow 标记测试 |
| CI-021 | CI/测试债 | P3 | 含 skipif（环境依赖，可能 CI 不成立） |
| CI-022 | CI/测试债 | P3 | 含 slow 标记测试 |
| CI-024 | CI/测试债 | P3 | 含 skipif（环境依赖，可能 CI 不成立） |
| CI-033 | CI/测试债 | P3 | 含 skipif（环境依赖，可能 CI 不成立） |
| CI-034 | CI/测试债 | P3 | 含 skipif（环境依赖，可能 CI 不成立） |
| CI-037 | CI/测试债 | P3 | 含 skipif（环境依赖，可能 CI 不成立） |
| CI-038 | CI/测试债 | P3 | 含 skipif（环境依赖，可能 CI 不成立） |
| TOOL-001 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-002 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-004 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-005 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-006 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-008 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-010 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-012 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-014 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-015 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-016 | 工具债 | P3 | 超过 500 行的巨型文件（2443 行） |
| TOOL-017 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-018 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-019 | 工具债 | P2 | 标记：print("用法：review-group MIS-XXX --props '卡id::prop-1,卡id::prop-2' -- |
| TOOL-020 | 工具债 | P3 | 超过 500 行的巨型文件（562 行） |
| TOOL-021 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-022 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-023 | 工具债 | P2 | 标记：只能当 TODO 债清单。</div></div>""" |
| TOOL-024 | 工具债 | P2 | 标记："**TODO 债清单**（列「还差哪些字段」），不是质量评级。", |
| TOOL-025 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-027 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-028 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-030 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-031 | 工具债 | P2 | 标记：3. 孤儿原子引用：Book 中 <atom>XXX</atom> 指向不存在的原子 → block |
| TOOL-032 | 工具债 | P2 | 标记：python tools/book_atom_sync.py --atom XXX   # 检查某颗原子的同步状态 |
| TOOL-033 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-034 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-035 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-036 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-037 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-038 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-039 | 工具债 | P2 | 标记："""章节内出现最多的完整 [实现·XXX] 引注，作为实现徽章的限定词投票。""" |
| TOOL-040 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-042 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-044 | 工具债 | P2 | 标记：- 有没有遗留 TBD/TODO/FIXME/XXX 标记？ |
| TOOL-045 | 工具债 | P2 | 标记：LOW  = 3   (长代码块零注释、TODO/XXX 标记) |
| TOOL-046 | 工具债 | P2 | 标记：TODO_RE = re.compile(r"\b(TBD|TODO|FIXME|XXX)\b") |
| TOOL-047 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-049 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-051 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-053 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-054 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-056 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-058 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-060 | 工具债 | P3 | 超过 500 行的巨型文件（553 行） |
| TOOL-061 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-063 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-065 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-067 | 工具债 | P3 | 超过 500 行的巨型文件（608 行） |
| TOOL-068 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-069 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-070 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-072 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-073 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-075 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-076 | 工具债 | P3 | 超过 500 行的巨型文件（864 行） |
| TOOL-077 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-079 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-080 | 工具债 | P3 | 超过 500 行的巨型文件（573 行） |
| TOOL-082 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-083 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-085 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-086 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-087 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-089 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |
| TOOL-091 | 工具债 | P3 | 命名不符合 *_6XX.py 批次规范 |

## 六、诚实登记

1. 本盘点为**静态启发式**：批次号断言/死链接/交人项均为正则+关键词口径，非人工精读，存在漏判/误判（每条明细已给定位，可复核）；
2. **未跑 pytest**：CI 实测失败项由 A2 采集，本表 CI/测试债为静态估计；
3. 数据债的 JSON 引用检查为**抽样**（限 200 个文件、每题只报首处）；PCK hash 漂移未在此深查（交由 C2/D 线与既有 628 A2 方法）；
4. 命名不合规工具**不重命名**（318 处引用成本≫收益，624 已评估）；巨型文件**不拆分**；这两类只登记；
5. §零.12 残留（_arch_v2x / queyi_core 等）**登记不提交**，处置交人。
