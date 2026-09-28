# 657 D5 · slow 相预存在失败 逐条归因（实跑取证，不是猜）

> 取证方式：把 655 交人项 5 登记的 **48 条** slow 失败用例**原样重跑**
> （`pytest <48 ids> -m slow -q`，2026-09-28，本仓工作区）。
> 结论先行：**38 FAIL + 2 ERROR = 40 条仍红；8 条已经转绿**（不必修）。

## 一、总览

| 归因 | 条数 | 处置 |
|---|---:|---|
| A 写死数字断言过期（650-652 的 27→37 卡 / 121→131 节点 / 79→89 命题同步欠账） | **33** | 属「测试断言过期」，**不是产品 bug**；根治 = 按 655 建议"去写死"，交独立批次 |
| B 凭证 / 哈希过期（VSA 凭证钉住旧版验证器） | **3** | **需重签凭证**（涉及 HMAC 密钥）⇒ 交人，本批不代签 |
| C 环境依赖 / 缺产物（Windows 路径、`build/replay_manifest.json`、快照 fixture） | **4** | 环境类，逐条给理由，不强行修 |
| （转绿，无需处置） | 8 | — |

## 二、A 类：写死数字断言过期（33 条）

| 测试文件 | 条数 | 证据（失败信息） |
|---|---:|---|
| `tests/test_prop_graph.py` | 9 | `assert '命题 79…'`（现值 89 命题 / 131 节点） |
| `tests/test_metrics_613.py` | 3 | `assert 60 == 50`、`assert 21 == 11` |
| `tests/test_620_gate.py` | 3 | `AssertionError: g…`（gate 汇总计数写死） |
| `tests/test_622_gate.py` | 3 | `失败：at…` / `pytest 失…`（门禁聚合写死） |
| `tests/test_646_end_to_end_slow.py` | 2 | 端到端链路里的计数断言 |
| `tests/test_baseline_629.py` | 2 | `test_file_counts_measured` / `test_gate_counts_measured_equals_standing` |
| `tests/test_pre_push_checklist_627.py` | 2 | `test_run_all_aggregates_ok` / `test_tools_all_check_pass` |
| `tests/test_run_625_gate.py` | 1 | `assert 1 == 0` |
| `tests/test_run_634_gate.py` | 2 | `test_autoimmune_zero` / `test_selftest` |
| `tests/test_third_party_audit_demo_628.py` | 2 | e2e 汇总绿断言 |
| `tests/test_json_output.py` | 1 | `test_golden_lock_json` |
| `tests/test_output_snapshots.py` | 2 | **ERROR**（快照 fixture 失效）→ 见 §四 |

**共同根因**：这些断言把「某一时刻的真实计数」写死进了测试。650-652 批次把库从
27 卡扩到 37 卡、W2 从 121 节点扩到 131、命题 79→89，**没有同步这批断言**。
655 交人项 5 的判断（"绝大多数是数字漂移"）被本批实跑**证实**。

**为什么本批不直接改**：① 数量 33 条、横跨 12 个文件，逐条改等于一次大型"改到绿"，
与「不许把测试改绿来交差」的纪律冲突；② 正确修法是"去写死"（让断言从事实源现算），
那需要为每个事实源建立单一权威源 —— 属独立批次（655 已建议）。

## 三、B 类：凭证 / 哈希过期（3 条，交人）

`tests/test_vsa_attestation_628.py`：
- `test_hmac_verify_pass`
- `test_production_dir_not_polluted_by_check`
- `test_traceability_and_independent_verifier` —— 实测：
  `cred["verifier_sha256"]=38e7235e6dee…` ≠ `sha256(independent_verifier_628.py)=731175ea5af9…`

**根因**：628 签发的 VSA 凭证把「验证器文件哈希」钉死在当时版本；此后
`independent_verifier_628.py` 被后续批次（647/655 等）改过，**凭证没有重签**。
这不是测试写错，是**凭证过期**。重签需要 HMAC 密钥（按 628 设计密钥不入库）⇒
**本批不代签**，交人（与"不代签 DCO"同一纪律）。

## 四、C 类：环境依赖 / 缺产物（4 条）

| 测试 | 证据 | 归因 |
|---|---|---|
| `tests/test_run_623_gate.py::test_real_tools_dir_green_after_b2` | `FileNotFoundError` | 依赖本机不存在的中间产物 |
| `tests/test_run_624_gate.py::test_gate_passes` / `test_selftest_passes` | `FileNotFoundError: [Win…` | Windows 路径 / 产物缺失 |
| `tests/test_replay_invariants_608.py::test_i5_manifest_consistency` | `KeyError` | 缺 `build/replay_manifest.json`（= 655 交人项 4：`--rebuild-manifest` 56 卡真编译，耗时，未授权执行） |
| `tests/test_output_snapshots.py` × 2 | **ERROR**（收集/fixture 阶段失败） | 快照 fixture 失效，测试基建问题 |

## 五、转绿的 8 条（无需处置）

`test_guard_hijack_640` ×1、`test_replay_invariants_605` ×3、`test_replay_invariants_606` ×2，
以及 655 清单里已不再红的其余条目 —— 655 之后某批已顺手修好（具体是哪一批未逐一回溯，
诚实登记为"已不红"，不给它安一个没证据的功劳）。

## 六、交人项（本批新增 / 强化）

1. A 类 33 条：是否立项「slow 断言去写死」独立批次（建议与 655 交人项 5 合并）；
2. B 类 3 条：是否授权**重签 VSA 凭证**（需密钥持有人执行，机器不得代签）；
3. C 类 4 条：是否授权 `atom_evidence_replay.py --rebuild-manifest`（655 交人项 4）；
   `test_output_snapshots` 的 fixture 是否修。
