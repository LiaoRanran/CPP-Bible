# 631 A2 · 跨批脆弱型断言修复报告

> 输入：`data/ci_pytest_triage_631.md`（A1 分类）· 授权：§零.11 例外条款
> （**只改测试断言，不改被测工具的生产逻辑**）

## 一、修了什么

| # | 用例 | 原断言 | 新断言 | 改法类别 | 验证 |
|---|---|---|---|---|---|
| 1 | `test_run_629_gate.py::test_tool_manifest_is_complete` | `added_files("tools") - NEW_TOOLS == ∅`（**所有**新增文件） | 排除更晚批次（`_630/_631` 标记）后再核验 `∅`，并旁证"确实存在更晚批次工具" | 缩小范围到批次 | ✅ pass |
| 2 | `test_run_629_gate.py::test_gate_other_steps_pass` | 跑 629 门禁子进程硬断言 rc=0 | `@skipif(更晚批次工具存在)`，理由写死 | 条件跳过（工具侧需越界） | ✅ skip（理由可见） |
| 3 | `test_run_629_gate.py::test_selftest_passes` | `G.selftest() == 0` | 同上条件跳过 | 条件跳过 | ✅ skip |
| 4 | `test_run_628_gate_628.py::test_acceptance_report_exists_and_complete` | `status["batch"] == 628` | `>= 628` + `last_completed_batch >= 628` + `next == last+1` | **单调断言** | ✅ pass |
| 5 | `test_run_628_gate_628.py::test_gate_other_steps_pass` | 跑 628 门禁子进程硬断言 rc=0 | `@skipif(更晚批次工具存在)`（628 门禁内 `v2_flag_integration_verify_628` 断言 tool_integrity 628 基准） | 条件跳过 | ✅ skip |
| 6 | `test_pre_push_630.py::test_check_all_ok_and_ahead` | 断言聚合 `all_ok`（要求工作区干净） | 断言**各分量**（受控干净/ci.yml 合法/交付物齐/630 代码归类正确/受控无阻断项） | 拆掉聚合、断分量 | ✅ pass |

**验证命令与结果**：

```text
pytest tests/test_run_629_gate.py -n0 -q        → ...s.s        （3 pass / 2 skip，原 3 fail）
pytest tests/test_run_628_gate_628.py -n0 -q    → ....s.        （5 pass / 1 skip，原 2 fail）
pytest tests/test_pre_push_630.py -n0 -q        → .......       （7 pass，原 1 fail）
```

## 二、为什么这么改（同一病根的三种处方）

**病根**：三代门禁（625/628/629/630）把「**当时的最新状态**」写进断言——
`status["batch"]` 的当时值、`git diff BASE..HEAD` 的当时新增集合、工作区的当时干净度。
这些量**必然**随批次推进而变 ⇒ 每开一批就多一批红（630 实测已因此多 2 项）。

| 处方 | 适用 | 本批用例 |
|---|---|---|
| **改单调断言**（`==` → `>=` / 区间） | 量本身单调（批次号、commit 数） | #4 |
| **缩小核验范围**（按批次标记而非"所有新增"） | 核验对象是"本批" | #1 |
| **拆聚合、断分量** | 聚合含"时点性质"的分量 | #6 |
| **条件跳过 + 交人** | 失败点在**工具内部**，修它要改他批工具（§零.11 越界） | #2 #3 #5 |

## 三、诚实登记

1. **#2/#3/#5 是"条件跳过"而非"修好"**：真正的修法在工具侧
   （629 门禁改按批次标记核验、628 工具的 tool_integrity 基准改为动态），
   改工具属 §零.11 越界 ⇒ **列入交人项**（见验收报告）。跳过的**条件与理由写在代码里**，
   运行时 `-rs` 可见，**不静默通过**。
2. **#1 的旁证断言**（`assert LATER_BATCH_ADDED`）确保修复不是空转：
   若未来 630/631 工具被删，该用例会失败并提醒复核——避免"排除规则"变成永久盲区。
3. **#6 放弃了套件内的闸门断言**：`all_ok` 的 push 闸门语义仍由
   `pre_push_630.py --check`（人/流程在 push 前调用）守住；套件内只断分量。
4. 本批**未改任何 625-630 工具的生产逻辑**（逐 commit 可查：`git show`）。
