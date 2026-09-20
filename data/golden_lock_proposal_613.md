# 613 · golden_lock 处理提案（A3）

> 生成：`python tools/golden_lock_proposal_613.py` ｜ 时间：2026-09-20T23:34:32
> **本文件是提案，不是执行**。golden accept 属人审权力，本批**未执行、也不会执行**。
> 本工具未跑 `gate_engine.py --check` / `golden_lock.py check`（监工类，铁律禁止）。

## 一、锁定快照 vs 当前

| 项 | 锁定值 | 当前 | 差 |
|---|---|---|---|
| block_findings | 0 | 0 | 0 |
| warn_findings | 136 | 186 | **+50** |
| 快照时间 | 2026-09-16（commit aa6cdb6） | — | — |
| 快照 dirty 标记 | True | — | — |

> 当前值来源：612 C1 oracle_verifier 实测，613 未重测。

## 二、归因

warn +50 **全部来自 `OBSERVATION-LIVENESS` 规则**（607 引入、612 实测 50 条 observation 命题缺 `liveness` 活性锚）。

- 该规则要求 observation 命题带 `liveness: {kind: fixture_symbol, symbol: <真实符号>}`；
- 50 条命题当前均无锚 ⇒ 规则按设计报 warn（**不是回归、不是误报**，是规则上线后的中间态）；
- 612 B3 what-if 已证明：补全后 warn **50 ⇒ 0**（可清零）。

## 三、建议（供人审裁决，三选一）

| 方案 | 做法 | 代价 | 推荐度 |
|---|---|---|---|
| ① 清零（首选） | 落地 A2 补丁（low 9 条）+ 人审 medium/high 41 条锚 | 需人审 41 条 | **高** |
| ② 分类接受（过渡） | `--classify OBSERVATION-LIVENESS=legacy`，约定清零期限 | 快照基线抬到 186 | 中 |
| ③ 整体 accept | `check --accept` 抬基线至 186，不分类 | 违反 warn 会计制度（530 任务5：无分类一律 exit≠0） | **不可行** |

## 四、若采纳方案②，建议命令（**人执行**）

```bash
python tools/golden_lock.py check --accept \
    "613：OBSERVATION-LIVENESS 50 条为 607 规则上线后的活性锚中间态，非回归；
     612 B3 已证补全后 50⇒0，约定 613 线A 完成（含人审 41 条）后清零" \
    --classify "OBSERVATION-LIVENESS=legacy"
```

分类语义（`tools/golden_lock.py` 定义）：
- `real` 真实债务需修 ｜ `false_positive` 误报 ｜ `legacy` 历史遗留（口径迁移期，约定清零期限）
  ｜ `accepted` 已接受长期现状。

## 五、现有分类表（快照）

```json
{
  "ATOM-CLAIM-CONCEPT-NORMALIZED": "legacy",
  "INFERENCE-NOT-MACHINE-VERIFIED": "legacy",
  "EV-MATRIX-UNBACKED": "accepted",
  "EV-OUT-UNDECLARED-KEY": "real",
  "EV-FALSIFICATION-QUANT": "real",
  "EV-ASSERT-SYMBOL-MAPPED": "real",
  "ATOM-REL-TARGET": "legacy",
  "EV-SERVES-EXIST": "legacy"
}
```

> 注：本提案的任何方案**都不改变** atoms/ 等受控目录；方案①的落卡同样需人审授权。
