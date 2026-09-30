# 670c C3 · 双仓 fast 测试状态（诚实登记，**未全绿**）

> 批次：670c（C 段 · 拆分收尾）
> 跑法：两侧均 `pytest tests/ -m "not slow" -q`（本机 32 逻辑核，诊断用 `-n 16` 并行；验证过的失败再用 `-n0` 串行复跑）

---

## 一、结论速览

| 仓库 | HEAD | fast 选中 | 失败 | 结论 |
|---|---|---|---|---|
| **CPP-Bible** | `465f1f6b`（本批执行期间被 670d/670e 推进过） | 见下注 | **48** | ❌ **未绿**（预存在债务 + 670a 在改 tests/ 与 data/） |
| **queyi-verifier** | `c8c106b`（工作树干净） | **3327** | **10 → 62（两次跑不一致）** | ❌ **未绿**（**全部**为 670c 之前就存在；失败数随语料镜像新旧浮动，见 `docs/670c_verifier_failures.md` §1.1） |
| **670c 本批新增的测试** | — | **60 个用例**（见下） | **0** | ✅ 全绿 |

**670c 新增测试全绿清单**（两侧合计）：
```
tests/test_split_670c.py          14 passed   （拆分完整性）
tests/test_master_gate_670c.py    15 passed   （主门禁）
tests/test_guard_rerun_670c.py    12 passed   （重跑护栏）
tests/test_drift_watch_670c.py     8 passed   （漂移监控）
tests/test_reproduce_670c.py      11 passed   （一键复现器）
────────────────────────────────────────────
合计                              60 passed
```
前端侧另有 **599 条 Node 真求值断言 + 8 页 jsdom 冒烟**，全绿（`cd web && npm test`）。

---

## 二、为什么没有做到"两侧全绿"

### CPP-Bible 侧（48 条）
失败**不是 670c 引入的**。两类原因，都可复算：

1. **语料长大了，快照/钉值没跟着走**（大多数）。典型：
   - `test_rule_card_mapper_646.py::test_card_count_is_27 - assert 42 ...` —— 断言写死 27 张，实际 42 张；
   - `test_pck_hash_renewal_628.py::test_all_83_certs_present` / `test_622_c3.py::test_pck_authority_map_covers_83` / `test_pck_hash_drift_analyzer_627.py::test_scan_count` —— 83 张证书口径；
   - `test_debt_replay_fix_628.py::test_manifest_has_56_entries`、`test_622_d2.py::test_labels_node_composition - assert 141 == 131`、`test_v2_flag_integration_628` 两条 —— 节点/清单条数口径；
   - `test_control_char_cleaner_626.py` / `test_snapshot_integrity_ci_626.py::test_control_chars_clean` —— 仓内数据含控制字符。
   这与 670c **实测**的另两处是同一个病：`web/data/index.json` 记录的哈希与`web/data/` 里的文件在 **HEAD 上就已经对不上**（4 个文件 `HEAD-ALREADY-DRIFTED`，非本批造成），以及 658 门禁 S0 快照记 178 节点而语料已长出 5 张卡。
2. **670a 正在改 `tests/` 与 `data/`**：任务书已注明"670a 在改，等 670a 完成后确认"。工作树里 `tests/test_611_tools.py`、`tests/test_liveness_*`、`tests/test_metrics_612.py` 等仍处于未提交的中间态。

另有预存在 lint 债务：`ruff check tools/` 2 条 F401（`tools/gate_rules_669d.py` 的 os/sys 未使用，**669d 冻结件，红线不许改**）。

### queyi-verifier 侧（第 1 次 10 条 / 第 2 次 62 条 —— **数不稳定，这本身是发现**）
> 两次跑同一 HEAD、同一干净工作树，失败数从 11 涨到 62。多出来的那批根因是**语料镜像刷新后钉值陈旧**：
> `test_prop_inventory_592` 期待 89 条命题、实得 **99**；`test_622_d2` 期待 131 节点、实得 **141** ——
> **+10/+10 恰好等于 670a 新加 5 张卡各带 2 条 prop 的增量**（与 CPP-Bible 侧 §4.1 独立测到的增量一致）。
> verifier 的 `atoms/`/`data/` 是**未跟踪的语料镜像**（`git ls-files` = 0），会随主仓刷新；刷新的确切触发点**未查明，如实登记**。
> 第 1 次的 11 条全部仍在第 2 次集合内。以下为**第 1 次**的 10 条（根因 (b) 类，两次都在）：

**全部**为 670c 之前就存在：670c 在该仓只创建了临时探针文件、未改任何受版本控制的文件，且 `git status` 工作树干净（HEAD `c8c106b`）。根因、逐条清单与"为什么不去修绿"见 `docs/670c_verifier_failures.md`：
- **6 条同一根因**：`data/supply_chain/link_613_verify.json` 这条 in-toto 溯源 link 钉的 `merkle_roots.json` 哈希已陈旧（`2c4a92a7672b ≠ 230d11641cab`）。
- 其余 4 条：控制字符、`tau_d` 自检、ruler coverage integrity、`cost_tracker` 从 git 回填为 0（该仓是 647 用 `git fast-export` 拆出来的，提交元数据形态不同 ⇒ 环境性）。
- `test_evidence_seeker_trigger_644.py::test_no_card_modify_and_selftest` 只在 `-n 16` 下红、`-n0` 不复现 ⇒ **并行伪失败**（多 worker 同时读写 `atoms/`），已登记为"该测试对并发不安全"。

**为什么不修绿**：这 10 条的本质是"信任锚漂移"，把 link 重录一遍确实会绿，但那等于**用重写记录的方式让一致性检查闭嘴**——与这套系统的核心纪律相反。重钉信任锚是治理动作（647 §六 那类"留交人裁决"），不属于一个前端/复现 kit 批次该单方面做的决定。建议处理路径已写在 `docs/670c_verifier_failures.md` §3。

---

## 三、本批**确实做到**的工程纪律

虽然两侧没有全绿，670c 把"发现红 → 定位 → 分清归属 → 不许掩盖"这条链路补齐了：

| 能力 | 工具 | 本批实测 |
|---|---|---|
| 合并主门禁（658 + 669d 六条 + D2 + D3） | `tools/run_master_gate_670c.py` | `overall=PASS  L0 13/13  L1 6/6  未登记BLOCK=0` |
| 「改了代码没重跑产物」护栏 | `tools/guard_rerun_670c.py` | 红路径实测：篡改基线后 `[STALE]` → `overall=RED`, exit=1 |
| 关键数字漂移监控 | `tools/drift_watch_670c.py` | 红路径实测：`cards_total 50→123` → `[DRIFT]` → exit=1 |
| 拆分完整性（wrapper 是否真解析到 canonical / 复制层是否漂移） | `tools/check_split_670c.py` | `overall=PASS`，8 个 wrapper 全部解析到 `queyi-verifier`，10 个复制层文件零漂移（WARN=已知债务） |
| 受控目录零写 | 主门禁 `--check` | 快照 **1910 个文件，写入 0 处** |

> 670c 也**没有**为了让任何检查变绿而改数据、改别人的测试或改冻结件：星图冒烟里"存在受攻击的卡节点"一条在数据上就是假的（0/47 张卡有攻击边），改动前后**同样 FAIL**，保持原样。

---

## 四、两条实测出来的「门禁互斥」（交给能拍板的人）

1. **656 管线 `--check` 要求产物新鲜，658 S0 要求产物等于冻结快照。** 语料长出 5 张卡后二者**不可能同时满足**：跑 `web_data_pipeline_656.py --build` 会让 `web/data/graph.json` 从 178/1093 变成 193/1103，S0 立即 FAIL（L0 5/5 → 4/5）。670c 的选择是**保住 L0 门禁**（`git checkout --` 还原 5 个生成物），把冲突如实登记，而不是替 658 重定快照。
2. **`web/data/index.json` 在 HEAD 上就已经与 `web/data/` 的 4 个文件哈希不符**（`HEAD-ALREADY-DRIFTED`，非本批造成）。所以 `--check` 的 index/drift 一节在 670c 之前就是 FAIL；670c 新增的 3 个数据文件（`baseline.json` / `err_deck_670c.json` / `experiments.json`）只是让这一节多 3 条登记，**没有改变该节的 PASS/FAIL 结论**。

建议的收口动作（一次性）：确认语料权威态 → 跑一次 `web_data_pipeline_656.py --build` → 同时更新 658 S0 快照与相关钉值 → 重跑 `run_658_gate.py --check` 与 `run_master_gate_670c.py --check`。
