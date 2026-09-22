# 626 D3 · Snapshot Integrity CI 规范（10 项检查）

> 工具：`tools/snapshot_integrity_ci_626.py`（纯标准库）
> 判据：11（派生报告带 source digest）、12（stale report 自动失效）

---

## 一、10 项检查

| # | 检查 | 判定 |
|---|---|---|
| 1 | `count_consistency` | annotations 388 / authority 418 / ledger 452 / review unique 93 |
| 2 | `id_uniqueness` | `event_id`、`review_item_id` 全局唯一（重复 ⇒ fail） |
| 3 | `hash_chain` | Authority Ledger `prev_hash`/`self_hash` 连续（断链 ⇒ fail） |
| 4 | `stale_report_detection` | `REPORT_STATUS.md` 存在且标注 STALE |
| 5 | `path_validity` | 关键数据文件路径存在 |
| 6 | `control_chars` | `data/` 无 0x00-0x1F（除 \n\r）控制字符 |
| 7 | `source_refs` | 报告引用的 source 文件存在 |
| 8 | `cross_report_numerical_consistency` | median 67.5 / union 93 / 豁免 31 三数一致 |
| 9 | `authority_projection_consistency` | W2 可编译、PCK 83、确定性成立 |
| 10 | `review_pack_integrity` | Review Pack 可解压、路径分隔符 `/`、含 SNAPSHOT_MANIFEST |

每项返回 `{name, status: pass|fail|warn, details, evidence}`。

## 二、实跑结果（626）

```
总检查 10 项：pass 10 / warn 0 / fail 0  ⇒  ✅ 无 fail
```

| # | 检查 | 状态 | 说明 |
|---|---|---|---|
| 1 | count_consistency | pass | annotations=388 authority=418 ledger=452 review_unique=93 |
| 2 | id_uniqueness | pass | event_id 重复 0；review_item_id 重复 0 |
| 3 | hash_chain | pass | 哈希链完整（452 events） |
| 4 | stale_report_detection | pass | STALE×7、UNREVIEWED×1 |
| 5 | path_validity | pass | 缺失关键路径 0 |
| 6 | control_chars | pass | 含控制字符文件 0（626 A2 已清洗 339 个） |
| 7 | source_refs | pass | 缺失 source 0 |
| 8 | cross_report_numerical_consistency | pass | median 67.5 / union 93 / 豁免 31 一致 |
| 9 | authority_projection_consistency | pass | W2 nodes=519；PCK=83；确定性=True |
| 10 | review_pack_integrity | pass | v2.zip entries=38 backslash=0 manifest=True |

## 三、`--fix` 模式

自动修复可修复项：
- **控制字符清洗**（调用 `control_char_cleaner`）
- 不可修复项（断链、ID 重复、数字不一致）**只报告，不自动改**（需人裁决）

## 四、已知局限

1. `path_validity` **只校验关键数据文件存在性**，不做 PCK `evidence.ref` 的全量引用解析（留 627）。
2. `stale_report_detection` 目前只检查 `REPORT_STATUS.md` 是否标注，**不逐份复核所有报告血缘**
   （`*_20260920.md` 系列多数仍为 UNREVIEWED，留 627）。
3. `review_pack_integrity` 只扫描桌面最新一个 `阙疑_*20260922*.zip`。

## 五、验证

- `--check` → exit 0（10/10 pass）
- `tests/test_snapshot_integrity_ci_626.py` → 12 例全绿（含断链/坏包 fail 场景）
