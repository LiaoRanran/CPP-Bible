# 614 G5 · data/ 目录派生物整理记录

> 原则：**移动前必查引用；有引用即不移动**（任务 G5 明确警示）。时间 2026-09-21。

## 一、分类盘点（data/ 共 447 文件）
| 类别 | 数量（近似） | 代表 | 处置建议 |
|---|---|---|---|
| **权威数据** | — | `mutation/full_baseline_v7.json`、`grounded_labels_w2.json`、`human_attack_edge_annotations.jsonl`、`supply_chain/*` | **保留原位** |
| **工具配置** | — | `governance_docs_manifest.json`、`oracle_registry.json`、`kc_inventory_612.json` | **保留原位** |
| **一次性报告** | `*_report_*.md` 10 + `*_61*.md` 43（`data/*.md` 共 107） | `613_acceptance_report.md`、`argument_audit_report.md` … | **暂不移动**（见二） |
| **历史基线** | 7（v1–v7） | `mutation/full_baseline_v1..v7.json` | **暂不移动**（见二） |

## 二、引用核查（移动可行性）
| 拟移动对象 | 引用方（`git grep`） | 结论 |
|---|---|---|
| `full_baseline_v4.json` / `v5.json` | **`tests/test_escape_rate_trend_610.py`**（**遍历 v1–v7 全部基线**）+ **`tools/metrics_collector.py`** | ❌ **移动即断裂** |
| `data/*_report_*.md` | `tools/learner_mastery_update_613.py`、`tools/oracle_verifier.py`（硬编码 data/ 报告路径） | ❌ **移动即断裂** |

## 三、决定：**本批不做物理移动**
- 任务 G5 步骤 3/4 要求"移动后更新所有引用路径"——但引用方为**工具与回归测试**（非文档），改其路径属**跨工具重构**，
  风险高且与"一任务一commit"冲突；且 `full_baseline_v4.json` 是**长期 CRLF 假脏**（铁律：勿提交/勿还原）⇒
  移动会制造 CRLF 变更（违铁律）。
- ⇒ 按"引用密集时不移动"的**安全优先**原则，本批**仅分类、不移动**；整理方案**交人裁决**。

## 四、交人建议（若确需整理）
1. 先改 `test_escape_rate_trend_610.py` 与 `metrics_collector.py` 的基线路径为**扫描 `data/mutation/full_baseline_v*.json`**（而非硬编码 v4/v5），
   再把 v1–v5 移入 `data/mutation/archive/`。
2. 先改 `learner_mastery_update_613.py` / `oracle_verifier.py` 的报告路径解析，再把 `*_report_*.md` 移入 `data/reports/`。
3. **`full_baseline_v4.json`（CRLF 假脏）单独评估**：先决定其 CRLF 归属，再做任何移动。
4. 每次移动后必须复跑相关 `--check` + pytest（回归锁）。

## 五、边界
- 未移动/未删除任何 data/ 文件；未改任何工具路径。仅产出本分类记录。
