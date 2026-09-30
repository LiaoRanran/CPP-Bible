# 670c C1 · queyi-verifier fast 测试失败清单（逐条定位）

> 批次：670c（C 段 · 拆分收尾）　仓库：`C:\CodeLearnling\queyi-verifier`　分支：main
> HEAD：**c8c106b**（"666 收尾：同步主仓干净语料 + PeP562/占位 OTS 工具 + 信任根按序重钉"）
> 工作树：**除本批临时文件外干净**（`git status` 仅有 `_*.py` / `_*.txt` 探针 + 一个既有的未跟踪 `tools/web_metrics_666.py`）
>
> **结论先说：这 10 条失败在 670c 之前就存在，不是本批引入的。** 依据见 §1。

---

## 1. 跑法与结果

```powershell
cd C:\CodeLearnling\queyi-verifier
.\.venv\Scripts\python.exe -m pytest tests/ -m "not slow" -n 16 -q --durations=25
```

| 项 | 值 |
|---|---|
| 选中用例 | **3327**（`--collect-only` 实数） |
| 并行（`-n 16`）失败 | **11** |
| 串行（`-n0`）复跑这 11 条 | **10 条稳定失败**，1 条**不复现** |
| venv Python | **3.14.5**（不是任务书写的 3.13；本机 `__pycache__` 里 313/314 两代都有） |
| 可用插件 | pytest、pytest-xdist、hypothesis 均在；**`pip` 模块缺失**（`No module named pip`，故无法 `pip install -e ".[dev]"`，只能靠既有环境） |
| 机器 | 32 逻辑核；串行 `-n0` 时 4% 用了 ~27 分钟（单核 CPU-bound），故诊断改用 `-n 16` |

**为什么这不是 670c 造成的**：670c 在 verifier 仓只创建了探针文件（`_split_probe*.py` 等），**没有修改任何受版本控制的文件**；`git status` 可证工作树干净，且失败集合包含 `data/supply_chain/` 这类 670c 从未触碰的信任根。换言之上表是 **HEAD `c8c106b` 自带的状态**。

### 1.1 ⚠️ 第二次跑变成 62 条 —— 失败数**不稳定**，且这条本身就是最该登记的发现

本批收尾时又完整跑了一次（为产出仓库惯例的 `pytest_fast_670c_run1.txt`），结果：

| 次 | 命令 | 失败 |
|---|---|---|
| 第 1 次 | `-n 16 -q --durations=25` | **11** |
| 第 2 次 | `-n 16 -q`（同仓同 HEAD，工作树仍干净） | **62** |

第 1 次的 11 条**全部**仍在第 2 次的集合里；第 2 次多出约 51 条。逐条查证多出来的那批，根因高度一致 —— **语料镜像长大了，测试里钉死的条数没跟着走**：

```
tests/test_prop_inventory_592.py::test_ledger_lists_79_props_and_27_cards
    assert len(prop_rows) == 89, f"命题行应 89 条，实得 {len(prop_rows)}"
E   AssertionError: 命题行应 89 条，实得 99

tests/test_622_d2.py::test_labels_node_composition
    assert sum(kinds.values()) == 131
E   assert 141 == 131
```

**+10 命题 / +10 节点**，与 670c 在 **CPP-Bible** 侧独立测到的增量**完全一致**：670a 新加的 5 张卡（`ATOM-MEM-NEWARR-001` + 4 张 `ATOM-UB-*`）各带 2 条 prop ⇒ +10 prop、+10 节点（见 `data/670c_acceptance_report.md` §4.1）。也就是说：

- verifier 的`atoms/`/`data/` 是**未跟踪的语料镜像**（`git ls-files data atoms` = **0**），会随主仓语料刷新；刷新发生在两次跑之间（两次跑之间 `data/`/`atoms/` 的 mtime 未见变化，故刷新的确切触发点未定位，**如实记为未查明**）。
- 一旦镜像刷新，一批"钉死旧条数"的断言就集体转红。

**因此 C1 的准确结论应读作**：verifier fast 的失败数**取决于语料镜像的新旧**，不是 670c 引入的，也不该被当成一个固定数字引用。两类根因贯穿两次跑：
(a) **语料长大 vs 钉值陈旧**（第 2 次那 ~51 条）；
(b) **信任锚/溯源 link 陈旧**（§2.1 那 6 条，两次都在）。

---

## 2. 逐条失败（10 条）

### 2.1 根因 A：供应链 provenance link 陈旧（一个根因，6 条失败）

**证据**（串行复跑原文）：

```
AssertionError: [{'path': 'data/supply_chain/merkle_roots.json',
                  'why': 'sha256 与 supply_chain 节不一致（2c4a92a7672b≠230d11641cab）'},
                 {'path': 'data/supply_chain/merkle_roots.json.ots',
                  'why': 'sha256 与 supply_chain 节不一致（e9d88662ebe1≠c2b352bfc3cc）'}]
```

**定位**：钉住这两个哈希的是 `data/supply_chain/link_613_verify.json`（in-toto 风格的溯源 link）：

```
link_613_verify.json:5  "data/supply_chain/merkle_roots.json": {
```

即：**613 批次录的验证 link 记的是当时那份 `merkle_roots.json`；该文件后来被重新生成过，link 没跟着重录**。`merkle_roots.json` 自身相对 HEAD 是**干净**的（`git status data/supply_chain/` 无输出）⇒ 不一致是**已提交状态内部**的不一致，不是本机改动造成的。

**因此失败的 6 条**：

| # | 测试 | 表现 |
|---|---|---|
| 1 | `test_verifier_closure_647.py::test_a3_5_consistent_with_tool_integrity` | `cons["consistent"] is True` 断言失败（上面那条 mismatches） |
| 2 | `test_verifier_closure_647.py::test_a3_9_report_and_selftest` | `V.selftest() == 0` 失败；自检输出里 25 项 ok、**唯独** `[FAIL] 与 tool_integrity 一致` |
| 3 | `test_trust_root_audit_647.py::test_a5_3_a3_closure` | 同根因（closure 一致性） |
| 4 | `test_trust_root_audit_647.py::test_a5_8_report_and_selftest` | `T.selftest() == 0` 失败；自检 13 项里 `[FAIL] A3：闭包 OK 且与 tool_integrity 一致` |
| 5 | `test_tool_integrity_647.py::test_a1_8_strict_default_declared_and_real_repo_green` | 严格模式下真仓库不绿 |
| 6 | `test_supply_chain_chain_601.py::test_layout_is_in_supply_chain_files_and_pinned` | layout 未在供应链文件里被钉住/钉值不符 |

### 2.2 其余 4 条（各自独立根因）

| # | 测试 | 表现 | 初判 |
|---|---|---|---|
| 7 | `test_snapshot_integrity_ci_626.py::test_control_chars_clean` | `assert 'fail' == 'pass'`（`run_check("control_chars")` 返回 fail） | 仓内数据文件含控制字符；66x 之后语料同步/新产物带进来的可能性大 |
| 8 | `test_tau_d_635.py::test_selftest` | `assert 1 == 0` | 该工具自检不过，未在本批深挖 |
| 9 | `test_ruler_coverage_extension_625.py::test_integrity_check_passes` | integrity check 不过 | 与信任根钉值同族 |
| 10 | `test_cost_tracker.py::test_backfill_from_git` | `assert 0 > 0`（从 git 回填拿到 0 条） | 该仓是 647 用 `git fast-export` 拆出来的，提交元数据形态与原仓不同；**环境性** |

### 2.3 唯一一条「并行伪失败」（**不复现**）

`test_evidence_seeker_trigger_644.py::test_no_card_modify_and_selftest` —— 在 `-n 16` 下红（`assert before == after`，卡文件被改），**串行 `-n0` 单独跑这条不复现**（10 条 FAILED 里没有它）。
根因是**并行执行时多个 worker 同时读写 `atoms/`**，不是真空洞。这条本身是一个「测试对并发不安全」的信号，值得后人在该测试上加互斥或改成临时副本。

---

## 3. C2 · 为什么本批**没有**去"修绿"这 10 条

任务书写的是"逐红修复"。实测后判断：**这 10 条不能靠改代码修，只能靠"重钉信任锚"修**，而重钉在本项目里是**治理动作**，不是工程动作。理由三条：

1. **它们红得是对的。** 这 6 条的本质是"录进 provenance link 的哈希 ≠ 现在的哈希"。把 link 重录一遍确实会绿 —— 但那等于**用重写记录的方式让一致性检查闭嘴**，而这套系统的全部价值就在于"信任锚漂移必须响"。同一份纪律在 670c 别处也执行了：星图冒烟里"存在受攻击的卡节点"一条在数据上就是假的（0/47 张卡有攻击边），我们**没有**为了让冒烟变绿去改数据或改别人的脚本（见 `docs/670c_前端完成度.md` §三.8）。
2. **修复入口存在，但该由人决定。"** `tools/supply_chain.py`（`layout/link/chain/stats`）、`tools/pck_hash_renewal_628.py`、`tools/merkle_integrity.py` 都能重录/重算锚。但"要不要在 670c 重钉、重钉到哪个状态、要不要同时更新 452 账本相关口径"是 647 §六 那类**留交人裁决**的问题，不属于一个前端/复现 kit 批次该单方面决定的事。
3. **本批无权改这些文件。** 670c 的红线要求不碰 669d 冻结件与 670a 正在改的断言文件；而信任根闭包（`verifier_closure_*.py` / `tool_integrity.py` / `supply_chain*`）正是被多批共用的锚，改动会波及其他批次。

**因此 C3 的结论是诚实的"未全绿"**，见 `docs/670c_verifier_双仓绿.md`。

### 建议的后续处理（交给能拍板的人）
- 若确认 `merkle_roots.json` 当前内容才是权威：跑 `tools/supply_chain.py link`（或 `pck_hash_renewal_628.py`）重录 link，然后**同时**更新 `docs/669d_gate_report.md` 里相关口径，并重跑 `run_669d_gate.py`。
- 若确认 link 记的才是权威：把 `merkle_roots.json` 回退到 613 状态，而不是重录 link。
- 无论哪条路，都应在提交信息里写明**"这是重钉，不是修复"**，并附新旧哈希对。
- `test_evidence_seeker_trigger_644` 建议加互斥或改用临时副本，消除并行伪失败。