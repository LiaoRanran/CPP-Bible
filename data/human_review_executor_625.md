# 625 D3 · 人审执行框架（只准备，不代签）

> 工具：`tools/human_review_executor_625.py`
> 铁律：**Authority 日志更新函数只定义不调用**；本批**不代签**任何一条人审判决。

---

## 一、框架设计

| 函数 | 作用 | 本批是否调用 |
|---|---|---|
| `build_entry(edge_id, power, decision, authorized_by, reason, prev_hash, source)` | 纯函数，构造一条带**哈希链**的 Authority 日志条目 | ✅ 自检中调用（仅构造，不写盘） |
| `append_entry(path, entry)` | 实际写盘（追加一行 JSONL） | ❌ **定义但本批绝不调用** |
| `_chain_hash(prev, entry)` | 哈希链：本条 hash = SHA256(prev \| payload) | 内部 |
| `_read_last_hash(path)` | 读日志末条 hash 作为链前驱 | 内部 |

## 二、不代签的硬约束（本批）

1. `--check` 自检**只构造样例条目**，随后断言 `Authority 日志 size 不变` ⇒ 证明未写盘。
2. `main()`（无 `--check`）只打印「框架就绪」提示，**不调用** `append_entry`。
3. 所有判决必须由**人**执行并标注 `authorized_by`（来源）；机器不替人做 approve/reject/abstain。

## 三、后续（交人/626）

- 人审执行时，由人调用 `build_entry` → 复核 `prev_hash` 链 → 确认后调用 `append_entry`。
- 建议：执行脚本增加 `--dry-run`（默认）与 `--apply`（需显式 `--i-am-human` 二次确认），防误签。
- 624 E2 生成的 80 条复核清单（`human_review_item_by_item_624.md`）即为此框架的待办输入。

## 四、验证

| 项 | 结果 |
|---|---|
| `selftest` | ✅ 5/5（含「未代签」断言） |
| `build_entry` 哈希链格式 | ✅ 64 位 hex |
| 非法 `power` 抛 `ValueError` | ✅ |
| Authority 日志未被修改 | ✅ |
