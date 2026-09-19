# 566 · Part 3 补丁（schema 自愈）+ 命题图人审交接视图（pending/backlog）

承接 `4c3250d`（565b 已被监工独立验收通过）。解释器只用 `.venv\Scripts\python.exe`；一个任务一个 commit；不 push、不 golden accept。**先读 `_worklog_565b.md`。**

## 任务 0（必修，监工验收抓出的真 bug）：prop_graph build 对旧库不自愈
**现象（监工复现）**：正式 `data/propositions.db` 是加 `anchor_source` 列**之前** build 的（15 列、无该列）；代码已加该列，但 `build` 对已存在的库不重建表 ⇒ 测试用新临时库全绿、用户直接跑 `prop_graph.py stats` 却崩 `sqlite3.OperationalError: no such column: anchor_source`。监工手动 `build` 重跑后才恢复。
**处方（二选一，选更简单的）**：
1. `build` 开头先检测：若 `props` 表已存在但缺关键列（`anchor_source` / 或任意代码中声明的列），**就 DROP 整个 propositions.db 或 DROP props 表再重建**——命题图是**纯派生视图**，随时可重建、丢历史无损，不要做保留旧行的 ALTER 迁移（徒增复杂度）；
2. 或在 `meta` 表存 `schema_version`，build 时发现版本不符就整库重建。
**回归锁（必须新增）**：测试里手工造一个"缺 anchor_source 列的旧 schema 库"→ 跑 build → `stats`/`query` 都不崩、列齐全、命题数仍 79。**这就是监工踩到的场景，不许只测新库。** 独立 commit。

## 任务 1：命题图人审交接视图（pending / backlog）
命题图现在只是"能查"。本批把它推进成**人审工作队列**——把积压从人肉 grep 变成一条命令。纯加法，不改卡、不改任何既有查询语义。
1. `prop_graph.py query --pending-signoff`：列出**未人签**的命题（当前实测 `unsigned` 3 条，即三张红队卡 ATOM-MEM-ALLOC-002 / LEAK-002 / PERF-004 的解释性论断），每条打印：命题 id、所属卡、claim_type、statement 摘要、evidence/external_basis、当前签署态。末尾输出**可直接复制粘贴的人签命令**（按你仓库既有的签署接口写，别新造协议）。
2. `prop_graph.py query --backlog`：列出**总原子卡中还没有 claim_structured 命题**的卡（待回填清单），打印卡 id、当前状态、一句话为什么还没回填；总数 = 总原子卡 − 带命题卡（当前带命题 27 张）。**只列清单，不自动回填、不自动改卡。**
3. 两个视图都要在命题数为 0 / 空结果时 fail-soft（打印"无待办"不崩）；输出口径与 `stats` 一致（card_signed / prop_signed 概念不混）。
4. **测试**：pending 视图能查到那 3 条 unsigned、backlog 条数 = 总原子卡 − 27、空结果不崩、build 后 git status 受控目录零差异。独立 commit。

---
## 收工验收（fresh）
- 任务 0 的旧库自愈测试必过（这是本批核心）；
- `prop_graph.py stats` / `query --pending-signoff` / `query --backlog` 三个真实 CLI 入口都要实跑一遍贴输出（监工要看真入口，不只看 pytest）；
- gate 61/141（block=0 warn=136）· poison 107/107 · replay confirm=56 · pytest fast -n auto 全绿；
- 受控目录 evidence/atoms/判定核心 tools 零改动；写 `_worklog_566.md`（偏差表 + 真入口输出 + 交人项）。做不完停在 Part 边界。

## 本批不做
564 meta 加固（等 trae 续跑）、560 B2 golden 并行、M3 单点互斥、ruff 债、真去回填那 26 张卡/人签那 3 条（本批只列清单交人，不动手）。
