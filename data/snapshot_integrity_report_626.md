# 626 D3 · Snapshot Integrity CI 实跑报告

- 总检查 **10** 项：pass **10** / warn **0** / fail **0**
- 结论：**✅ 无 fail**

| # | 检查 | 状态 | 说明 |
|---|---|---|---|
| 1 | `count_consistency` | **pass** | annotations=388 authority=418 ledger=452 review_unique=93 |
| 2 | `id_uniqueness` | **pass** | event_id 重复 0；review_item_id 重复 0 |
| 3 | `hash_chain` | **pass** | Authority Ledger 哈希链完整 |
| 4 | `stale_report_detection` | **pass** | REPORT_STATUS 含 STALE×7、UNREVIEWED×1 |
| 5 | `path_validity` | **pass** | 缺失关键路径 0 |
| 6 | `control_chars` | **pass** | 含控制字符文件 0 |
| 7 | `source_refs` | **pass** | 缺失 source 0 |
| 8 | `cross_report_numerical_consistency` | **pass** | median/union/豁免 三数一致 |
| 9 | `authority_projection_consistency` | **pass** | W2 nodes=519；PCK=83；确定性=True |
| 10 | `review_pack_integrity` | **pass** | 阙疑_人审决策包_20260922_v2.zip: entries=38 backslash=0 manifest=True |

## 证据

- **count_consistency**: expect annotations 388; expect authority 418; expect unique review 93
- **id_uniqueness**: events=452; review_items=93
- **hash_chain**: events=452
- **stale_report_detection**: human_review_deep_analysis_20260920.md = STALE; SNAPSHOT_MANIFEST.json = STALE
- **cross_report_numerical_consistency**: median=67.5; union=93; exemptions=31
- **authority_projection_consistency**: W2 与 grounded_labels 粒度不同（留 627 归一化）
- **review_pack_integrity**: 阙疑_人审决策包_20260922_v2.zip
