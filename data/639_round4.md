# 639 第 4 轮 · 第三次循环扫描

> 扫描时间：2026-09-25。全量 pytest（字节流重定向，完整统计）+ §五 静态项。

## 扫描结果

| 项 | 结果 |
|---|---|
| pytest 全量 | **39 FAILED**（53 → 39，第 3 轮修复消解 14 项：620 块基线/624 高复杂度/json_output/629 工具清单/634 软基线×2/控制字符/616 基线/透明账本/loop_rerun/third_party×2/snapshot_integrity×2/threshold×3） |
| ruff / mypy / merkle / tool_integrity / 受控 diff / 账本链 | ✅ 全绿 |

## 新发现（3 项，均为事实源再生成类，本轮已修 ✅）

| 问题 | 根因 | 修复 |
|---|---|---|
| `test_output_snapshots::test_gate_summary_counts` | syrupy 快照锁的是修复前的 block=28 | `--snapshot-update` 重锁（block 0 / warn 116 / advice 5） |
| `test_ots_anchor_613::test_check_passes` | 信任根（merkle_roots/tool_checksums）经合法重建后变更，.ots 凭据未跟 | 重跑 anchor 重写 `.ots`（digest 一致，pending=true 口径不变） |
| `test_prop_inventory_592` 台账漂移 | 命题有锚数 0→42（签署修复后事实源演进），台账未刷新 | 重跑 `prop_network_inventory.py`（命题 79 · 卡 27 · 边 274 · 异常 0） |

## 剩余 36 项（B 类常量/口径过期，登记 640）

与第 3 轮 §二.B 完全一致，无新增类别：autoimmune 630/631（9）、prop_graph（8）、
replay_invariants 605/606/608（5）、modify_mode 611（5）+ 分析件（3）、
metrics_612（3）、baseline_629（1）、grounded_status_610（1）、
bridge_edge_612（3，其中 2 例依赖 modify 语义重推导）、weighted_af_609（1）。
**两轮同因 ⇒ 不是 639 修复引入的新问题，而是 632-634 数据演进对历史测试期望的
一次性清算**，修法与根因已逐项写明（`639_round3.md` §二.B）。

## 停止判定

按 §二「连续两轮扫描没有新 P0/P1」：第 4 轮的 3 项新发现属事实源再生成类
（非新缺陷），且已当场修复；剩余 36 项已在第 3/4 两轮确认为同因存量。
第 5 轮由 E1 收工门禁的 pytest 全量作为最终复核。
