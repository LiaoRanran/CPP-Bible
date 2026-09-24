# 634 C2 · 快照测试更新 + .pytest_tmp 处置

## 一、快照测试（syrupy）

- 载体：`tests/test_output_snapshots.py`（**1 个文件 / 5 个快照**），快照存
  `tests/__snapshots__/test_output_snapshots.ambr`。
- 跑前：**3 通过 / 2 失败**（`test_gate_summary_counts`、`test_kg_stats_counts`）。
- **先判正确性再更新**（非盲目）：
  - `test_gate_summary_counts` 实测差异：`rules 67`（不变）、`block 0→28`、`warn 186→116`；
    `block/warn` 的位移来自 **624 block 规则接线 + 631 auto liveness + 634 C1 signed_by 填充**
    的真实演进（`rules` 未变 ⇒ 非规则注册回归）⇒ **属合法漂移**；
  - `test_kg_stats_counts`：卡数/边数随上述卡面变更而变，同属合法演进。
- 动作：`pytest tests/test_output_snapshots.py --snapshot-update` ⇒ **2 更新**；
- 复验：**5/5 通过**。

## 二、`.pytest_tmp/` 处置

| 项 | 结果 |
|---|---|
| 是否已 `.gitignore` | **是**（`.gitignore` 第 559 Part C 段：`.pytest_tmp/`）⇒ **不入库** ✅ |
| 目录数 | 665（633 记 652，测试继续堆积） |
| 收工删除 | **被环境拦截**：`[safe-delete][SAFE_DELETE_BULK_CONFIRM_REQUIRED] count=9999 threshold=500` |

> `tests/conftest.py` 已注明：本环境对 >500 文件的批量删除有拦截层，仓内路径不旁路 ⇒
> `.pytest_tmp` 的**物理清理须人工/CI**（本批不绕过拦截层）。**已 gitignore ⇒ 不影响入库与 git 状态。**

## 三、诚实登记（§八）

1. **633 E1 的「快照测试 25 个」口径偏大**：其 `snapshot_tests()` 统计的是**引用 snapshot 字样的
   测试文件数（25）**，而真正用 syrupy 锁快照的**只有 `test_output_snapshots.py` 的 5 个**；
   本批按**真实快照测试**处置（5 个），并登记口径差异；
2. **快照更新非盲目**：先核 `rules` 未变（排除规则注册回归）再更新 block/warn 计数；
3. **`.pytest_tmp` 未物理删除**：环境 safe-delete 拦截（>500 文件），交人/CI；已 gitignore；
4. 未改任何测试逻辑，仅更新 `.ambr` 快照数据。
