# 614 G2 · 根目录历史 worklog 与临时文件清理记录

> 只读盘点 + 安全判定；**未删除任何被引用文件**。时间 2026-09-21。

## 一、盘点结果（根目录 `_*`）
| 类别 | 实测 | 结论 |
|---|---|---|
| `_worklog_*.md` | **0 个**（根目录） | 无待清理 |
| `_c589` / `_temp` / `probe*` | **不存在** | 无待清理 |
| 根 `_*` 文件 | 仅 `_arch_v19_brief.md`、`_book_asm_freshness.json` | 均为在用 |
| 根 `_*` 目录 | `_adv_*(6)` `_archive` `_arch_v18` `_arch_v19` `_asm_demo` `_auto` `_bypass_test` `_emp_bench` | 见下 |

## 二、历史 worklog 已在此前批次归档
- `_archive/worklogs/`：**56 份**历史 worklog（`_worklog_403.md` … `_worklog_580b.md`）。
- `_worklog_600/610/612/613/614`：**不存在**（该批未落 worklog，无从归档）。
- ⇒ 任务 G2 步骤 3「移动 `_worklog_580..612` 到 `_archive/worklogs/`」：**上游 580 已在该处**，其余从未存在 ⇒ **无需动作**。

## 三、剩余 `_*` 目录安全判定（未删/未移）
| 目录 | 跟踪 | gitignore | 引用检查 | 判定 |
|---|---|---|---|---|
| `_auto/` | 部分 | — | 协议态（status/outbox/inbox） | **保留**（当前协议必需） |
| `_archive/` | ✅ 1320+ | 仅 observability_logs | 归档库 | **保留** |
| `_arch_v18/` `_arch_v19/` | ✗ | v18 忽略 / v19 未忽略 | 最新两轮调研 | **保留**（G1 明确留根） |
| `_adv_v80/v90/v95/v95b/v96/critique` | ✗ | 忽略 | 独立对抗调研 | **保留** |
| `_asm_demo/`（177 文件） | ✗ | `_asm_demo/` | **被 Book/Examples/tools 大量引用**（book_asm_freshness、ch2x…） | **保留**（在用） |
| `_emp_bench/`（14 文件） | ✗ | `_emp_bench/` | 被 Book/审计引用 | **保留** |
| `_bypass_test/`（27 文件） | ✗ | `_bypass_test/` | 被审计文档引用 | **保留** |

- 判定依据：`git grep -E '_asm_demo|_emp_bench|_bypass_test'` 命中 Book（20+ 章）、Examples、`tools/book_asm_freshness.py`、`tools/data_sanity_audit.py`、`ci.yml`、`AGENT.md` 等 ⇒ **删除会断链**。
- 三者均 **gitignored、0 跟踪** ⇒ 对 git 面无影响；按任务「不确定则保留」纪律**保留**。

## 四、结论
- 根目录**历史 worklog 清理已由上游批次完成**；本批**无安全可删项**。
- 未执行任何删除/移动（避免误伤被引用工件）；两条 CRLF 假脏按铁律保留。
- 附：`data/underscore_dirs_inventory_20260920.md`（60920 盘点）可对照。
