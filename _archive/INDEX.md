# _archive/ 归档目录索引（2026-09-19）

> 自动生成。_archive/ 存放历史临时文件、旧工具、探针脚本、worklog 等，已从仓库根目录和 data/ 归档至此。
> git 跟踪：1621 文件 / 19.3 MB（observability_logs/ 被 gitignore，不跟踪）。

## 目录清单

| 目录 | 文件数 | 大小 | 说明 |
|---|---|---|---|
| `benchmarks/` | 135 | 0.6 MB | _bench_*.cpp 基准测试文件（从根目录 git mv） |
| `early_probes/` | 624 | 2.7 MB | 早期探针目录（_t528base/_t528full/_t528k/_t528t3/_t535_probe 等 5 个目录） |
| `eval_pack/` | 8 | 0.1 MB | 评估包（解压版） |
| `legacy_probes/` | 23 | 0.2 MB | 历史探针脚本（23 个） |
| `logs/` | 53 | 0.2 MB | _*.log 日志文件（从根目录移动，61 个中部分已清理） |
| `old_tools/` | 562 | 7.5 MB | 旧工具备份（tools_old558/ 513 文件 + tools_legacy/ 49 文件） |
| `observability_logs/` | 4 | 176.1 MB | **被 gitignore**。旧 trace 日志（2026-09-14~17，JSONL），data/logs/ 保留最近两天 |
| `probes/` | 6 | 0.5 MB | _probe_* 探针文件（从根目录移动） |
| `root_data/` | 2 | 0 MB | 根目录 _*.json 数据文件（从根目录移动） |
| `scripts/` | 1 | 0 MB | fix_ch36.py（从根目录 git mv） |
| `temp_json/` | 39 | 6.2 MB | data/mutation/ 临时 JSON（39 个，full_baseline_v1.json 已移回） |
| `temp_outputs/` | 101 | 0.2 MB | 临时输出文件（101 个） |
| `worklogs/` | 56 | 0.6 MB | _worklog_*.md 工作日志（580-608，按惯例不入库但已归档） |
| `_arch_free/` | 1 | 0 MB | 免费模型调研 |

## 顶层文件

| 文件 | 大小 | 说明 |
|---|---|---|
| `README.md` | 685 B | _archive/ 目录说明 |
| `eval_pack.zip` | 42 KB | 评估包（压缩版） |

## 归档历史

| 批次 | 归档内容 | 说明 |
|---|---|---|
| 化债6 | legacy_probes/ + README.md | 23 个历史探针脚本 |
| 化债7 | temp_outputs/ | 101 个临时输出文件 |
| 化债10 | early_probes/ + old_tools/ + eval_pack/ + _arch_free/ + temp_json/ | 早期探针 5 目录 + 旧工具 513 文件 + 评估包 + 免费模型调研 + 临时 JSON 39 个 |
| 化债12 | temp_json/ 修正 | full_baseline_v1.json 误归档后移回（Merkle 根 7→6→7） |
| 化债14 | benchmarks/ + logs/ + probes/ + root_data/ + scripts/ | 根目录大规模清理：135 bench cpp + 61 log + 6 probe + 2 json + fix_ch36.py |
| 化债26 | observability_logs/ | 旧 trace 日志归档（9-14~17，176 MB），加入 gitignore 不跟踪 |
| 化债27 | old_tools/tools_legacy/ | tools/legacy/ 49 个旧工具归档（早期脚本已被新工具链替代） |

## 注意事项

- **不要删除**：_archive/ 内的文件是历史资产，可能包含可追溯的早期数据
- **不要还原**：除非明确需要，否则不要把 _archive/ 内的文件移回仓库根目录
- **worklogs/**：_worklog_*.md 按惯例不入库，但已归档在此目录便于追溯
- **old_tools/**：558 批次前的旧工具备份（tools_old558/ 513 文件 + tools_legacy/ 49 文件），7.5MB，不要删除
- **observability_logs/**：被 gitignore，不跟踪。旧 trace 日志（JSONL 格式），data/logs/ 保留最近两天
- **temp_json/**：data/mutation/ 的临时 JSON，full_baseline_v1-v7.json 是权威基线（在 data/mutation/ 下，Merkle 跟踪），不在此目录

---

*数据源：_archive/ 目录实扫（2026-09-19）/ 化债6-27 commit 历史*
