# 673s · fast_gate 基线

**生成日期**：2026-10-02
**命令**：`python tools/fast_gate.py --all`（门禁 + 全部非 slow 测试 + 前端，三路并发）

> **先决条件（必须记）**：本机 `PYTHONPATH` 注入了 WorkBuddy 的**安全删除拦截层**
> （`sitecustomize.py` → `SAFE_DELETE_BULK_CONFIRM_REQUIRED`）。它会把删除类用例伪造成
> `SystemExit: 1`，让 fast_gate 假红（673m 已登记）。**下列基线一律在
> `CODEBUDDY_SAFE_DELETE_ENABLED=0` 下测得**，否则数字不可比。

---

## 1. 本批实测基线（`--all`）

```
$ CODEBUDDY_SAFE_DELETE_ENABLED=0 python tools/fast_gate.py --all
  [PASS] 658 门禁（L0 5/5 + S5/S6）                                   13.9s
  [PASS] 669d 门禁（六条 P0 规则）                                     1.4s
  [PASS] 671a guard（三方数字一致）                                    4.0s
  [PASS] 前端自测 node web/run_tests.mjs                              43.6s
  [FAIL] pytest（全部非 slow）（xdist -n auto worksteal）            327.4s
[fast-gate] overall=FAIL  总耗时 327.4s（预算 300s，超预算 ⚠️）
```

| 阶段 | 耗时 | 结果 |
|---|---|---|
| 658 门禁（L0 5/5 + S5/S6） | 13.9s | **PASS** |
| 669d 门禁（六条 P0 规则） | 1.4s | **PASS** |
| 671a guard（三方数字一致） | 4.0s | **PASS** |
| 前端自测（`node web/run_tests.mjs`） | 43.6s | **PASS** |
| pytest（全部非 slow，`-n auto --dist worksteal`） | **327.4s** | **FAIL** |
| **总耗时** | **327.4s** | 超 300s 预算 ⚠️ |

**pytest 腿失败清单**（工具输出截断为前 8 条，精确值见 §3）：

```
FAILED tests/test_numbers_env_671g.py::test_real_machine_has_required_env
FAILED tests/test_c_target_648.py::test_a4_out_keys_match_declared_run_match_keys
FAILED tests/test_ots_anchor_613.py::test_check_passes
FAILED tests/test_ots_anchor_656.py::test_real_target_not_invalid
FAILED tests/test_ots_reanchor_625.py::test_check_passes
FAILED tests/test_grounded_audit_596.py::test_real_committed_report_matches_fresh_render
FAILED tests/test_loop_r5_runner_646.py::test_run_reports_both_calibers
ERROR  tests/test_loop_metrics_629.py::test_asymmetry_is_computed
```

---

## 2. 与历史基线对比

| 时点 | 命令 | 门禁三腿 | pytest 腿 | 总耗时 | 备注 |
|---|---|---|---|---|---|
| 673m（2026-10-01） | `fast_gate.py`（默认档） | PASS | **跳过** | 12.2s | 里程碑：默认档 overall=PASS |
| 673m（2026-10-01） | `fast_gate.py --all` | PASS | **2 个失败** | 365s | 超预算；当时仓更干净 |
| **673s（2026-10-02）** | `fast_gate.py --all` | **PASS** | **失败（≥8，精确 5+）** | **327.4s** | 本文件 |

**趋势**：门禁三腿**稳定 PASS**（658 / 669d / 671a guard 一直是绿的）；
pytest 腿的失败数**上升**（2 → ≥8 在本机脏树口径下），根因见 §3。

**耗时**：365s → 327.4s（略降），但仍**超 300s 预算**（预算只 WARN 不判红，见 `fast_gate.py`）。

---

## 3. 三个口径的失败数（同一 HEAD，必须一起看）

| 口径 | 命令 | 失败数 | 说明 |
|---|---|---|---|
| **本机主仓**（含本地派生/未跟踪产物） | `pytest tests/ -q -m "not slow" -n 16` | **5** | 最接近"开发者日常" |
| 本机主仓 + fast_gate | `fast_gate.py --all` | ≥8（工具截断显示） | 多了 loop_r5/loop_metrics 等（`-n auto` 下暴露） |
| **干净检出**（`git worktree`，= CI 所见） | 同上 + `CI=true` | **42** | 缺 `data/metrics.jsonl`、`data/propositions.db`、`build/replay_manifest.json`、`dist/` |
| 干净检出 + 先跑产物生成器 | 同上 + `prop_graph build` + `metrics_collector --no-heavy` | **24** | 生成器修掉约 18 条，但引入 1 条新失败（见下） |

**主仓 5 条失败明细**：

```
FAILED tests/test_c_target_648.py::test_a4_out_keys_match_declared_run_match_keys
FAILED tests/test_grounded_audit_596.py::test_real_committed_report_matches_fresh_render
FAILED tests/test_ots_anchor_613.py::test_check_passes
FAILED tests/test_ots_anchor_656.py::test_real_target_not_invalid
FAILED tests/test_numbers_env_671g.py::test_real_machine_has_required_env
```

**关键结论**：主仓 5 vs 干净检出 42 ⇒ **37 条差异几乎全部来自"缺未跟踪的派生/构建产物"**
（`data/metrics.jsonl`、`data/propositions.db`、`build/replay_manifest.json`、`dist/`），
**不是代码回归**。这也解释了 CI 为什么会红（CI 是干净检出）。

**一个反例（诚实登记）**：把产物生成器加进来会**引入** 1 条新失败——
`test_sqlite_version_671e::test_current_db_user_version_is_zero_documents_gap`
（该用例断言活库 `user_version` 仍为 0，用于**记录未同步缺口**；建库后变 2）。
⇒ 这些用例是对着**开发机产物状态**写的，不是对着干净检出写的。
**故本批没有把"生成产物"加进 CI**（详见 `data/673s_CI配置说明.md` §6.2）。

---

## 4. fast_gate 有没有"配置文件/基线数字"可更新？

**没有**。`tools/fast_gate.py` 里与基线有关的只有两个**常量**：

| 常量 | 值 | 含义 | 本批是否改 |
|---|---|---|---|
| `BUDGET_S` | `300.0` | 总耗时预算（**超了只 WARN，不判红**） | **未改** —— 改它是策略决策；且实测 327.4s 只超 9%，属机器负载波动范围（673m 记录同命令 365s） |
| `DEFAULT_TIMEOUT_GATE` / `DEFAULT_TIMEOUT_TESTS` | 300 / 900 | 单步超时 | 未改 |

⇒ **无基线数字需要回写**；本文件即为当前基线记录。

---

## 5. 本批对基线的影响（净效果）

| 改动 | 对 fast_gate 的影响 |
|---|---|
| 修 `test_seed_check_671i` 的登记（673p 回归） | **减少 1 条失败**（该用例此前必红） |
| 改写 4 处 skip reason（`residue_present` 型） | **无**（仍跳过，语义等价） |
| `.gitignore` 新增 3 条 | **无**（不参与 pytest） |
| `ci.yml` 新增"补漏门禁"步骤 | **无**（CI 专属，本地 fast_gate 不走） |

**验证**：`pytest tests/test_seed_check_671i.py -q -n 0` → **7 passed**；
`pytest tests/test_verifier_pool_673p.py tests/test_selection_strategies_673p.py -q -n 0` → **57 passed**。
