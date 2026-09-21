# 613 · golden_lock 处理提案（A3）

> 生成：`python tools/golden_lock_proposal_613.py` ｜ 时间：2026-09-21T10:11:23
> **本文件是提案，不是执行**。golden accept 属人审权力，本批**未执行、也不会执行**。
> 本工具未跑 `gate_engine.py --check` / `golden_lock.py check`（监工类，铁律禁止）。

## 一、锁定快照 vs 当前

| 项 | 锁定值 | 当前 | 差 |
|---|---|---|---|
| block_findings | 0 | 0 | 0 |
| warn_findings | 186 | 186 | **+0** |
| 快照时间 | 2026-09-21（commit dd5b029） | — | — |
| 快照 dirty 标记 | True | — | — |

> 当前值来源：golden_state.json 快照（613 不跑 golden_lock --check，铁律禁止）。

## 二、归属与状态（**提案已被采纳**）

OBSERVATION-LIVENESS 规则（607 引入、612 实测 50 条 observation 命题缺 `liveness` 活性锚）产生的 50 条 warn，已于 **commit dd5b029 按本提案方案② 分类为 `legacy`** 并写入锁定基线（136 → 186）。

- 即：本 A3 提案（分类接受 OBSERVATION-LIVENESS=legacy）**已被 golden_lock 正式采纳**；
- 613 线A 仍在推进锚落卡（人审 41 条 medium/high）与 low 9 条补全，完成后该 legacy 债可清零；
- 该规则要求 observation 命题带 `liveness: {kind: fixture_symbol, symbol: <真实符号>}`；补全后 warn 可 **50 ⇒ 0**（612 B3 what-if 已证）。

## 三、若未来需清零（供人审，仍可用方案①）

| 方案 | 做法 | 代价 | 推荐度 |
|---|---|---|---|
| ① 清零（首选） | 落地 A2 补丁（low 9 条）+ 人审 medium/high 41 条锚 | 需人审 41 条 | **高** |
| ② 分类接受（**已采纳**） | `--classify OBSERVATION-LIVENESS=legacy` | 快照基线抬到 186 | 已完成 |
| ③ 整体 accept | `check --accept` 抬基线至 186，不分类 | 违反 warn 会计制度（530 任务5：无分类一律 exit≠0） | **不可行** |

分类语义（`tools/golden_lock.py` 定义）：
- `real` 真实债务需修 ｜ `false_positive` 误报 ｜ `legacy` 历史遗留（口径迁移期，约定清零期限）
  ｜ `accepted` 已接受长期现状。

## 四、现有分类表（快照）

```json
{
  "ATOM-CLAIM-CONCEPT-NORMALIZED": "legacy",
  "INFERENCE-NOT-MACHINE-VERIFIED": "legacy",
  "EV-MATRIX-UNBACKED": "accepted",
  "EV-OUT-UNDECLARED-KEY": "real",
  "EV-FALSIFICATION-QUANT": "real",
  "EV-ASSERT-SYMBOL-MAPPED": "real",
  "ATOM-REL-TARGET": "legacy",
  "EV-SERVES-EXIST": "legacy",
  "OBSERVATION-LIVENESS": "legacy"
}
```

> 注：本提案的任何方案**都不改变** atoms/ 等受控目录；方案①的落卡同样需人审授权。
