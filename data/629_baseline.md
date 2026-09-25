# 629 §一 基线台账（standing baseline + 开工实测）

> 工具：`tools/baseline_629.py`（纯标准库，只读，不跑监工四门禁）
> HEAD：`48485622`（ahead origin/master **10** commit）
> 口径说明：§四.2 要求『解析 gate_engine --check 输出』，但 §零.1 禁止跑监工门禁；
> 本工具改为只读 `import gate_engine` → `run()`（不写盘，实测见下），与 §一 数字一致。

## 一、standing baseline（§一 原文，629 开工冻结，不修改）

| 指标 | 值 |
|---|---|
| gate_rules | 67 |
| gate_hits | 191 |
| gate_block | 0 |
| gate_warn | 186 |
| gate_advice | 5 |
| poison | 124/124，诚实覆盖率 95.5%（64/67） |
| replay | confirm=56 refute=0 infra=0 |
| tool_integrity | 5 核心工具一致，22 尺子 |
| w2 | IN114/OUT7/UNDEC0（121 节点） |
| pck | 83 张，authorized 27/83 |
| ledger | 452 条唯一事件，93 unique |
| sandbox_touched | 36/67（盲区 31） |
| escape | 1/1406（CS anytime 上界 0.9062%） |
| vsa | 14 张（HMAC） |
| transparency_log | 23 条（GENESIS 起） |
| mirror_edges | 自动证明 76 / sidecar 118 / 总 194 |
| head | 889a3bc8 |
| remote | 793b5c45（624） |

## 二、开工实测

| 指标 | 实测 |
|---|---|
| gate 规则数 | 67（其中自动化 64） |
| gate 命中 | 149（block=25 warn=119 advice=5） |
| gate warn 命中规则数 | 9（有 warn 的规则） |
| ahead origin/master | 10 commit |
| 远端 HEAD | `33e02efb` |
| HEAD | `48485622` 633 [E1]：测试债深化分类与长期方案(不改测试)——slow 6/跨批脆弱30/环境依赖117/快照25(针对A2后剩余54项),给动态基线读/conftest统一skipif/快照触发更新/slow分层四方案设计;--check只读+6例单测 |
| `tools/*.py` | 375 个 |
| `tests/test_*.py` | 387 个 |
| `atoms/**/ATOM-*.md` | 27 张 |
| `data/pck/certificates/*.pck.yaml` | 83 张 |
| VSA 凭证 | 30 张 |
| 透明日志条目 | 41 条 |

## 三、gate warn 按规则名 top10（实测）

| # | 规则 ID | warn 数 |
|---|---|---|
| 1 | `ATOM-CLAIM-CONCEPT-NORMALIZED` | 77 |
| 2 | `EV-MATRIX-UNBACKED` | 16 |
| 3 | `OBSERVATION-LIVENESS` | 8 |
| 4 | `EV-OUT-UNDECLARED-KEY` | 6 |
| 5 | `EV-FALSIFICATION-QUANT` | 4 |
| 6 | `INFERENCE-NOT-MACHINE-VERIFIED` | 3 |
| 7 | `ATOM-REL-TARGET` | 2 |
| 8 | `EV-ASSERT-SYMBOL-MAPPED` | 2 |
| 9 | `EV-SERVES-EXIST` | 1 |

## 四、实测 vs 任务书（差异标注，不修改基线）

| 项 | 任务书 | 实测 | 性质 |
|---|---|---|---|
| gate_hits | 191 | 149 | **不符** |
| gate_block | 0 | 25 | **不符** |
| gate_warn | 186 | 119 | **不符** |
| remote | 793b5c45（624） | 33e02efb | **不符** |
| vsa | 14 张（HMAC） | 30 张（HMAC） | 基线漂移(允许) |
| transparency_log | 23 条（GENESIS 起） | 41 条（GENESIS 起） | 基线漂移(允许) |

**基线漂移说明**：`vsa` / `transparency_log` 的漂移根因是 628 B4 端到端演示与其单测**每次运行都会追加 1 张 VSA 凭证 + 1 条日志**（append-only，只增不减，链仍完整），§一 的 14 张 / 23 条是 628 收工时点值。§十一.3 要求标注而不修改基线。

## 五、recent commits

```
48485622 633 [E1]：测试债深化分类与长期方案(不改测试)——slow 6/跨批脆弱30/环境依赖117/快照25(针对A2后剩余54项),给动态基线读/conftest统一skipif/快照触发更新/slow分层四方案设计;--check只读+6例单测
7e838b10 633 [D2]：文档债清理——修306文档3处裸文件名死链接(改为../../atoms/mem/实际路径,已核实目标存在);368的6处file://为假阳性不改;过期标注0处;登记.pytest_tmp残留652目录(不删)与扫描器file://口径;矛盾描述登记不改
6694b291 633 [D1]：PCK/镜像边/ref_missing 交人项整理——统一清单+P1-P4优先级+处置建议+依赖;登记627/628 ref_missing口径出入(2 vs 1)待核;不代签不自动填充;镜像边194全自动证明其中118条缺ReviewItem属治理决策;PCK authorized 27/83
```

## 六、`pytest -m "not slow"` 既有失败（629 开工冻结，F1 用『无新增失败』口径）

- 实测规模：**2200 例 collected**（414 slow 已 deselect）；修正后既有失败 **11 项**。
- **修正说明（诚实登记）**：开工首测为 19 项，其中 7 项是**自伤**——测量时工作区里存在一个语法未完成的同名新文件 `tools/baseline_629.py`（首版引号错误），使「整目录 ruff/mypy 干净」类断言失败（`test_mypy_fix_625` ×2、`test_pre_push_checklist_627::test_static_clean`、`test_quality_gate_613`、`test_run_623/624/625_gate`）；另有 `test_run_628_gate_628::test_gate_other_steps_pass`是**真实 629 回归**（C2 首版把裸 anchor 追加进 628 日志，破坏 628 B3/B4 的一致性检查），已由 C2 修复（anchor 改确定性）⇒ 该 8 项均从基线剔除。
- 剩余 11 项按根因分四类（均与本批代码无关）：

| 类别 | 项数 |
|---|---|
| (a) 628 数据处置 → 627 断言过期 | 5 |
| (b) 本地未跟踪 _arch_v2x/ → 治理 manifest 不一致（CI 大概率不出现） | 4 |
| (c) 625 阈值过期（type: ignore 28 > 20） | 1 |
| (d) 611 快照口径 | 1 |
| **合计** | **11** |

- **629 不修这些测试**（§零.11：不动 628 工具；测试属他批资产），仅在 F1 登记为既有债 + 交人项（E3 第 12 项）。

| # | 既有失败 nodeid |
|---|---|
| 1 | `tests/test_pck_hash_drift_analyzer_627.py::test_content_drift_56` |
| 2 | `tests/test_pck_hash_drift_analyzer_627.py::test_all_have_gap` |
| 3 | `tests/test_pck_hash_drift_analyzer_627.py::test_root_cause_classifies` |
| 4 | `tests/test_pre_push_checklist_627.py::test_tools_all_check_pass` |
| 5 | `tests/test_pre_push_checklist_627.py::test_run_all_aggregates_ok` |
| 6 | `tests/test_ci_pytest_fix_625.py::test_governance_manifest_verified` |
| 7 | `tests/test_governance_doc_guard_591.py::test_verify_real_manifest_matches` |
| 8 | `tests/test_governance_self_hash_601.py::test_real_manifest_has_valid_self_hash` |
| 9 | `tests/test_supply_chain_chain_601.py::test_chain_verify_with_real_inspections` |
| 10 | `tests/test_mypy_fix_625.py::test_no_bulk_type_ignore` |
| 11 | `tests/test_pe_timestamp_caliber_611.py::test_603_capture_untouched_by_this_batch` |



## 边界三元组 + v26 补充字段（635 1.1 回填）

- `mutation_set_hash`: `d7556d622e92fbf918cf9b49c39d97da0733c88fb686be7e734df7fca294ac57`
- `mutation_count`: 1593
- `generator_version`: `mutation_fuzz@v7`
- `evidence_channel`: `standard_textbook`
- `materiality_flag`: true
