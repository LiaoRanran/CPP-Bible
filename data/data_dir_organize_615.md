# 615 E2 · data/ 目录整理方案（**仅方案，不移动任何文件**）

> 铁律：**本批不移动/不删除任何文件**；执行须 616 经**人审授权**。承接 614 G5（引用密集 ⇒ 未移动）。

## 一、目标结构
```
data/
├── reports/            # 新增：一次性报告（*_report_*.md 等）
├── mutation/
│   ├── archive/        # 新增：历史基线 v1–v5（保留 v6/v7 在 mutation/）
│   ├── full_baseline_v6.json
│   └── full_baseline_v7.json
├── supply_chain/  governance_docs_manifest.json  metrics.jsonl  …（权威数据，原位）
└── （现有子目录：backups cost flashcards human_review_export logs profiles review tasks traces）
```

## 二、移动清单
| 类别 | 文件 | 目标 |
|---|---|---|
| 一次性报告 | `argumentation_framework_quality_report_20260920.md` / `human_review_batch_report_20260919.md` / `human_review_quality_report_20260920.md` / `knowledge_asset_quality_report_20260920.md` / `mastery_update_report_613.md` / `mechanical_judgment_quality_report_20260920.md` / `metrics_honesty_quality_report_20260920.md` / `oracle_verification_report_612.md` / `project_health_report_20260920.md` / `trust_root_quality_report_20260920.md`（**10 个**） | `data/reports/` |
| 历史基线 | `full_baseline_v1.json` … `full_baseline_v5.json`（**5 个**） | `data/mutation/archive/` |

## 三、引用影响（**移动前必须改**，实测）
| 被移动对象 | 引用方（`git grep`） | 需要的改动 |
|---|---|---|
| `full_baseline_v1/v2/v3` | `tests/test_metrics_curves_v7_592.py`、`tests/test_mutation_fuzz_report.py`、`tests/test_overturned_curves.py`、`tools/metrics_collector.py` | 路径→**扫描 glob** `data/mutation/**/full_baseline_v*.json` |
| `full_baseline_v4/v5` | 同上 + `tests/test_escape_rate_trend_610.py` | 同上 |
| `data/*_report_*.md` | `tools/learner_mastery_update_613.py`、`tools/oracle_verifier.py` | 报告输出路径→`data/reports/` |
| **CRLF 假脏** | `full_baseline_v4.json` 是长期 CRLF 假脏（铁律勿动） | 先定其 CRLF 归属再做任何移动 |

## 四、分阶段计划（风险递增）
| 阶段 | 动作 | 风险 | 验证 |
|---|---|---|---|
| **Phase 0** | 仅**新建** `data/reports/README.md`（索引，纯增量） | 无 | 无引用变化 |
| **Phase 1** | 改 §三 引用方为 glob 路径解析（先改后移） | 中 | 相关 `--check` + pytest 全绿 |
| **Phase 2** | 移动 10 个报告 + v1–v5（v4 单独处理 CRLF） | 中高 | 全量 `--check` + pytest 全绿 + `git status` 核对 |
| **Phase 3** | 观测一期无回归后，收尾引用文档 | 低 | 文档链接检查 |

## 五、回滚
- 每阶段一个 commit；回滚 = `git revert <commit>`（文件移动用 `git mv` 保留历史，可逆）。

## 六、边界
- 本批**仅出方案**：未建 `data/reports/`、未移动任何文件、未改任何工具路径。
- 执行须 **616 人审授权**；`full_baseline_v4.json`（CRLF 假脏）单独评估。
