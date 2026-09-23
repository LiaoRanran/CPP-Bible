# 629 C2 · V2 Authority 账本接入透明日志

> 工具：`tools/authority_log_integration_629.py`（只读账本 + 追加日志；只读 import `transparency_log_628` 复用其 `_entry_hash` / `verify_log` 口径）

## 一、结果

| 指标 | 值 |
|---|---|
| V2 账本事件（626，只读） | 452 条 |
| 并行链条目 | 452 条 |
| 链完整性（复用 628 `verify_log`） | True（broken=[]） |
| 重复条目（幂等检查） | 0 |
| 未入链事件 | 0 条 |
| 链根 hash | `cffe6b36f13a80d1717cfd99…` |
| 锚定条目已在 628 生产日志 | True（log_index=28） |

## 二、结构

```
decision_event_v2_ledger.jsonl（452 条，**只读不改**）
        │  逐条 canonical JSON → sha256
        ▼
authority_event_chain_629.jsonl（并行链，entry: log_index/event_id/event_hash/
                                  prev_log_hash/entry_hash）
        │  末条 entry_hash = 链根
        ▼
authority_event_chain_629_anchor.json（{events, root_hash, ledger_sha256}）
        │  append_vsa（幂等）
        ▼
data/transparency_log.jsonl（628 生产日志，**+1 条锚定**）
```

## 三、为什么「并行链 + 一行锚定」而不是「452 条直接进 628 日志」

1. **语义**：628 日志的定位是「VSA 凭证日志」；把 452 条事件混进去会让`logged_files_status()` / `unlogged_credentials()` 的语义漂移。
2. **落盘要求**：`append_vsa()` 要求每条都有**真实文件**计算 sha256；逐条入册会凭空产生 452 个派生 JSON 文件入库（噪音），而这些文件并不构成「可独立验证的凭证」。
3. **可验证性不打折**：并行链复用 628 的 `_entry_hash` 与 `verify_log`，**同一套代码可复验**；锚定条目让 452 条事件的最终根 hash 进入生产日志，从而获得与 VSA 凭证同等的溯源地位（跨锚定）。
4. **任务书原文允许二选一**（「与 628 原透明日志的关系（合并还是并行）」），本工具选了并行 + 锚定，并把理由登记在此。

## 四、局限

- 链是**本地线性哈希链**（同 628），无外部见证者 ⇒ 只能证明「本文件内部未被改」，不能证明「没被整段替换」；
- 事件 hash 锚定的是**账本文件内容**，不校验事件签名（DecisionEvent 无签名机制）；
- 452 条事件的「人审合法性」不在本工具范围（`review_method` 只作为字段带过）。
