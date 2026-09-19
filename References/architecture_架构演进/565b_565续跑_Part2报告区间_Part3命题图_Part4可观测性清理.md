# 565b · 565 续跑：Part 2 报告区间 · Part 3 命题状态图 · Part 4 可观测性与清理

承接 `cad77da`（Part 1 `tools/stat_bounds.py` 已由监工独立验收通过：数学锚点全对、单侧/双侧口径已显式化）。**现在直接做 Part 2 / 3 / 4，不重做 Part 1。** 先读 `_worklog_565.md`（§2.3 口径、§5 施工点是上轮实测备好的，照用，不要另造数）。解释器只用 `.venv\Scripts\python.exe`；一 Part 一 commit；不 push、不 golden accept。

## 纪律前置（Part 1 验收确认的，务必照此取数）
- **区间用双侧 `stat_bounds.cp_interval(k,n,conf)`**（拦截率/处置率/逃逸率这类"k/n"）；
- **"零失效上界"陈述用单侧 `stat_bounds.cp_upper_one_sided(k,n,conf)`**——例：56 卡 0 误伤 = 单侧 0.05209，不是双侧 0.06375；
- 别再用兼容函数 `cp_upper` 当"统一上界"（它 k=0 单侧、k>0 双侧混用，已在 docstring 警告）；
- 报告块统一走 `stat_bounds.proportion()` 出"分子/分母 + 点估计 + 区间"。

---
## Part 2 · 报告口径自洽 + 自动置信区间（改 `tools/mutation_fuzz.py` 报告层 + README）
**只改报告呈现与文档，判决/分类逻辑一字不动。**
1. `data/mutation/README_v1.md` 写死四口径（与基线勾稽，禁止重新生成 `full_baseline_v1.json`）：
   - 可判分母 = 1188 − 232(n_a) − 0(malformed) = **956**；
   - **严格拦截率 = 615/956 = 64.33%**（warn_only 114 永不入严格分子）；
   - 含 warn 处置率 = 729/956 = 76.26%；
   - 全分母率正名为 `treated_all = 729/1188`，**不得叫 strict**。
2. `tools/mutation_fuzz.py` 报告输出统一带 `分子/分母 + 点估计 + C-P95 区间`（调 Part 1）：
   - **分算子 M1–M7** 各自给 率+区间+可判样本数（上轮实测：M1 64/1/27、M2 0/207/14、M3 2/11/75、M4 200/0/33、M5 0/0/83、M6 324/8/0、M7 139/0/0）；
   - **M2**：逃逸 207/207 显式标"活雷，逃逸区间 `cp_interval(207,207) = [98.24%, 100%]`"；
   - **M5**：可判 n=0 ⇒ 标 `insufficient evidence`，**不算率、不填 0**；
   - **M3**：仅 13 可判 ⇒ 标样本不足 + 给"补样至 n≥59"目标；
   - n_a / malformed 单列，永不进拦截率分母。
3. 验收：`tests/test_mutation_fuzz.py` 全绿（**判决相关断言逐字不变**；它已被 559 挂了 `replay_serial`，照常跑）；新增报告含上述区间与 M2/M3/M5 标注；README 口径与基线 JSON 逐值勾稽。独立 commit。

## Part 3 · 命题状态图 `tools/prop_graph.py` + `data/propositions.db`
- 数据源 = 27 卡 frontmatter 的 claim_structured（79 命题：observation 50 / inference 29），**只读抽取，绝不改卡、绝不自动入库新命题**。
- `data/propositions.db` 与 `data/knowledge_graph.db` **分离**——命题≠概念，不碰 concepts 表（525"标签袋"教训）。
- `build` 幂等（连跑两次结果逐行一致）；查询子命令按 id / 卡 / claim_type / 机验状态 / 签署状态检索，输出"命题 → 所属卡 → 证据工件或 external_basis → 裁决/签署状态"。
- 上轮实测底座：**命题级 `signed_by` 当前 0 条（全靠卡级人签兜底）、79 条全有 evidence 字段**——查询要把这两态如实列出（不要假装有命题级签署）。
- `tests/test_prop_graph.py`：总数=79、obs=50/inf=29、按类型/签署查询正确、**重建前后 git status 受控目录零差异**。独立 commit。

## Part 4 · 可观测性修通 + 三曲线埋点 + 卫生清理
- **4a 修 `data/metrics.jsonl` 断流**（最后写入 2026-09-14 21:30）：先定位 metrics_collector 为何停写、修到采集恢复并重新产出；**注意 `data/logs/*.jsonl` 是观测日志（今天还在写），不是 metrics 产物，别修错对象**。加"采集确实落盘"回归锁。
- **4b 三曲线字段**：mutation 逃逸率（接 Part 2 带区间）、`overturned_by_stronger_verifier`（当前预期 0）、逃逸生存时间。**只有 1 个时点，文档/报告必须注明"单调收敛尚不可声称"**，不许画趋势下结论。4a+4b 一个 commit。
- **4c 卫生清理（独立 commit）**：用 `.venv` python 的 `os.remove`/`shutil.rmtree` 通道（shell 删除会被 safe-delete 拦）。删 `_worklog_565.md` §5.6 列明的明确 pattern：`.pytest_tmp/run-*`（已 34+）、`_probe559c.py`/`_probe559d.py`/`_commit_msg_559*.txt`/`_t559*`、仓库根 `_probe_ch132_blk*.exe`、本批 `_probe565t0.py`/`_commit_msg_565p1.txt`。**`_probe559.py`/`_probe559b.py` 留档不删**（Part B 复现探针）。删前后 `git status` 核对，不确定的留清单交人。

---
## 收工总验收（Part 1 未跑，本次必须 fresh 全跑）
`.venv\Scripts\python.exe`：
- `tools/gate_engine.py --check` → 61 规则 / 命中 141（block=0 warn=136 advice=5）；
- poison → 107/107、RULE-COVERAGE 36/61、零 uncovered 攻击面；
- `tools/atom_evidence_replay.py --check` → confirm=56 / refute=0 / infra_error=0；
- `pytest -m "not slow" -n auto`（全绿，约 78s）+ `pytest -m slow -n0`（全绿）；
- 受控目录 evidence/atoms/判定核心 tools 语义零改动（pre-existing `evidence/conc/EV-CONC-001.md` 的 M 除外）。
- 改了被 `.tool_checksums` 钉住的文件就 `tool_integrity.py --update` 重钉；含降级分支的测试断言 severity；不编数字，跑多少报多少。
- 写 `_worklog_565b.md`：每 Part 前后对比、口径取数记录（哪个率用了双侧/单侧）、偏差表、复跑命令、交人清单。做不完停在 Part 边界、不留半成品。

## 本批仍不做
564 C1 供给链 meta 加固、560 B2 golden 并行、B3 测试选择、M3 单点互斥、563 N3 grounded 视图、V5 回填/红队卡人签（交人）、ruff 债。
