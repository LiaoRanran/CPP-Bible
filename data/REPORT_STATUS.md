# 626 A2 · 派生报告状态与快照血缘（REPORT_STATUS）

> 判据 11「所有派生报告带 source digest」+ 判据 12「stale report 自动失效」的落地台账。
> 状态取值：`VALID` / `STALE` / `SUPERSEDED` / `INVALID`
> 自动检测：`tools/snapshot_integrity_ci_626.py --check`（`stale_report_detection` 项）

## 一、当前快照血缘（source_snapshot）

| 项 | 值 |
|---|---|
| git_sha（本报告生成时） | `e4a710638c4abbf18e1d2f6eb4bf9ea72b18566a` |
| generated_at | 2026-09-22T15:36:44Z |
| `data/human_attack_edge_annotations.jsonl` | sha256 `027dff3aaaa6247f04541968b988fc90…`（121,374 B，388 条） |
| `data/authority/authority_log.jsonl` | sha256 `01b17c520cde75f869d2620dd88d64c8…`（267,921 B，418 条） |
| `data/attack_edges_candidates.jsonl` | sha256 `d44fcc8f7b3dc9bcf1b839f34fef37a3…`（227,094 B，388 条） |

## 二、派生报告状态表

| 报告 | 状态 | 问题 / 说明 | 修正批次 |
|---|---|---|---|
| `human_review_deep_analysis_20260920.md` | **STALE** | MIS 分组 `MEM14/UB12/LANG6/CONC4/HIST3/OTHER3` 与当前 388 条真实分布 `MEM27/UB9/HIST3/CONC2/LANG1` 不符 ⇒ 数据血缘缺陷 | 626 A2（已加 STALE 标注） |
| `human_review_quality_report_20260920.md` | VALID | MIS 分布引用与真实前缀一致（仅列 OUT7 的 MIS），无污染 | — |
| `human_review_honesty_615.md` | VALID | 626 A1 修正 median 75→**67.5** | 626 A1 |
| `human_review_item_by_item_624.md` | VALID | 626 A1 加唯一性说明：记录 110 / **唯一 93** | 626 A1 |
| `human_review_item_by_item_30_615.md` | VALID | 30 条唯一 edge ID（与 624 overlap 17） | — |
| `exemption_expiry_615.md` | VALID | 626 A1 明确 **31 = 27 legacy + 4 HC** | 626 A1 |
| `SNAPSHOT_MANIFEST.json` | **STALE** | 冻结于 2026-09-22T05:51（head `192d7d98`）；其 `gate.rules=63` 已过时（624 B1 后为 **67**） | 留 627 重生成 |
| `624_acceptance_report.md` / `625_acceptance_report.md` | VALID | 已加「110 记录 / 93 唯一」说明 | 626 A1 |
| `626_baseline.md` | VALID | 626 任务 0 基线 | 626 任务0 |
| 其余 `*_20260920.md` 报告 | **UNREVIEWED** | 未在 626 逐份复核血缘（时间所限），默认不得作为当前事实引用 | 留 627 |

## 三、STALE 判定规则

1. 报告声称的数据源（条数/时间范围）与当前 `source_snapshot` 不一致 ⇒ **STALE**
2. 报告内部分组/统计与按真实 ID 重算结果不一致 ⇒ **STALE**（如 deep_analysis 的 MIS 分布）
3. 报告被后续批次的修正覆盖 ⇒ **SUPERSEDED**
4. 报告含不可恢复的错误（如控制字符损坏且无法还原）⇒ **INVALID**

## 四、控制字符清洗记录（626 A2）

`tools/control_char_cleaner.py --fix` 对 `data/` 扫描：**9 个文件、删除 339 个控制字符**，rescan = 0。
涉及（含 `0x00/0x07/0x08/0x09/0x0B/0x0C/0x13/0x1A/0x1B`）：
`612_batch_progress_20260920.md`、`atom_verdict_extraction_622.md`、`build_reproducibility_report.md`、
`escape_zero_analysis_622.md`、`pck_abstain_sync_report_621.md`、`pck_authority_sync_report_620.md`、
`pck_status_report_620.md`、`verification_horizon_curve_622.md`、`vfdr_realtime_620.md`。

> 其中 PCK 报告的 `0x08`/`0x0B` 正是外部大模型指出的「`verifier` 文本字符损坏」来源，已清洗。
