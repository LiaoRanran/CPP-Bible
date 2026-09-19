# _worklog_589 · 确定性自检全算子化 + M2 攻击集注释净化（v7 尺子冻结）

> 基线权威：`data/mutation/full_baseline_v6.json`（588 产出）。本批主改 `tools/mutation_fuzz.py`（非 CORE）。
> 临时探针一律落 `%TEMP%`（不在仓库根堆件）。

## 任务 0 · 开工先量（只读，不单独 commit）

### 0.1 HEAD / 工作树
- HEAD = `55c01c8`（588 收尾 chore）。
- 两条长期 CRLF 假脏仍在且未提交未还原：`data/mutation/full_baseline_v4.json`、`evidence/conc/EV-CONC-001.md`。
- 工作树另有大量历史 untracked（`_worklog_*.md` / `data/mutation/_*.json` / `tools_old558/` / `eval_pack/` 等），**非本包产物**。

### 0.2 fresh 基线（退出码 + 数字）
- `tool_integrity.py --check` → **exit 0**（5 个核心工具与基准一致）。
- `gate_engine.py --check` → **exit 0**，**规则 63 · 命中 191（block=0 warn=186 advice=5）**。
- `poison_drill.py` → **exit 0**，**124/124 · RULE-COVERAGE 39/63 · 表观 100% · 诚实 95.2% · 双指标 100%/100%**。
- `atom_evidence_replay.py --check` → **exit 0**，**confirm=56 refute=0 infra_error=0**。

### 0.3 自检小卡集候选（实跑确认）
- v6 各算子产 blocked 的卡数：M1=56 / M2=47 / M3=41 / M4=56 / M5=27 / M6=83 / M7=83。
- v6 `equivalent_keys` 35 条 = **27 条 M2**（注释伪变异）+ **8 条 M6**（block→flow matrix：EV-HIST-001 / EV-MEM-032..037 / EV-UB-002）。
- 候选小卡集（**13 张**，`%TEMP%\probe589_cards.py` 实跑）：EV-CONC-001/002/003/004/005 · EV-LANG-001 · EV-HIST-001 ·
  ATOM-CONC-RACE-001 · ATOM-CONC-FENCE-001 · ATOM-MEM-PERF-003 · ATOM-MEM-ALLOC-001 · ATOM-HIST-AUTOPTR-001 · ATOM-LANG-INLINE-001。
- 实跑（jobs4）结果：cards=13 variants=245 blocked=206 escaped=1 n_a=31 equivalent=7；
  逐算子 **M1=13 / M2=15 / M3=22 / M4=28 / M5=8 / M6=100(含 eq1) / M7=20** —— **每算子 ≥1 blocked** ✓（M6 含 1 equivalent ✓）。

### 0.4 复现 27 条 M2 注释伪变异（`--operators M2 --cards all --limit 999`）
- M2 全量：variants **195** · blocked **141** · escaped **0**（非等价）· n_a **27** · equivalent **27**。
- 逐条（`%TEMP%\probe589_m2.py`）：**27/27 改动行 `strip()` 均以 `#` 开头**（bad=0），聚合 **9 卡 × 3**（转大写/加./反斜杠）：
  EV-CONC-001 · EV-CONC-002 · EV-MEM-038 · EV-MEM-040 · EV-MEM-041 · EV-MEM-042 · EV-MEM-043 · EV-MEM-044 · EV-MEM-045。
- 这 9 条的注释行均落在 **frontmatter 的 `matrix:` 块内**（`_gate_read_spans` 只划 frontmatter 区间；588 把 `matrix` 加入
  `GATE_READ_KEYS` 后该块成为读取面 ⇒ `_PATHP` 扫到注释里的示意路径）。
- M2 blocked 卡集：**141 条变体 / 47 张卡**（供任务 2 后逐卡对账）。

### 0.5 现状自检墙钟
- **未取到**：`--selfcheck-determinism`（全量 `--limit 999 --jobs 4`）长跑被用户取消执行（未拿到墙钟与退出码）。
  备注：该命令含一次全量跑（v6 冷跑实测 ≈269s）+ 子集重跑，预计 6–9 分钟。
- 任务 1 优化后的对照墙钟待任务 1 实跑补记。

---

## 任务 1（commit `bef65be`）确定性自检覆盖全算子
- `_SELFCHECK_OPS` = `tuple(MUTATORS)`（全 7 算子）；新增固定小卡集 `data/mutation/selfcheck_cards.json`（**8 卡**）
- `selfcheck_determinism` 重跑对象改为「全 7 算子 × 固定小卡集」，与主跑 `--cards/--limit` 解耦；
  jobs>1 仍 jobs=1 串行对账同一小卡集；另与主跑(first)小卡集部分对账
- 覆盖 fail-loud：每算子 ≥1 blocked 否则 `SelfcheckCoverageError`（CLI exit2）
- 实测：串行（jobs=1）小卡集 **85.9s**（< 90s 目标）；13 卡为 139.3s ⇒ 取 8 卡（偏差 D3）
- 测试 `tests/test_mutation_selfcheck_589.py`：ops=全7 / 覆盖 fail-loud / 可证伪偏斜 / CLI exit2 / 真集 clean(slow)，全绿
- 只改自检的算子集与卡集选择；未改 `_variant_index` 比对字段、未改判决路径

## 任务 2（commit `d36d5c8`）M2 攻击集净化
- 新增 `_is_within_yaml_comment(text, idx)`（YAML 口径：`#` 行首 / 前接空白-TAB 才起注释，保守）+ `mut_m2` 跳过注释路径（`continue`）
- 测试 `tests/test_mutation_m2_589.py`：单元 5 条 + 9 卡反例 + v6 blocked 141 正例 + 合成卡正例，全绿
- **实测（--operators M2 --cards all --limit 999 --jobs 4）：变体 195 · blocked 168 · escaped 0 · n_a 27 · equivalent 0**
  —— 与 §4 预测（141/0/27）**不符**，见偏差 D1

## 任务 3（**未冻结 v7**）双跑对账
- 清 `build/replay_manifest.json` 后全量 `--cards all --limit 999 --jobs 4 --selfcheck-determinism --selfcheck-equivalent` 连跑两次：
  - 冷跑 #1 与热跑 #2 **逐变体 0 差异**（only_in=0 / changed=0）；两次 selfcheck（确定性 + 等价保守性）均 **exit0**
  - 两次数字一致：**变体 1593 · blocked 1405 · escaped 1 · n_a 179 · malformed 0 · equivalent 8 · 可判 1406**
  - 逐算子可判：M1 65 · **M2 168** · M3 65 · M4 224 · M5 29 · M6 716 · M7 139
- 与 v6 对账：**恰好 27 条变化**（全部 M2，`escaped→blocked`、`eq True→False`，键集合不变）
- **按 §5.5：数字不符预测 ⇒ 不 commit `full_baseline_v7.json`、保留 v6 为权威**（v6 文件未动）

## §6 偏差表（交监工裁决）

| # | 任务书假设 X | 磁盘实测 Y | 处理 |
|---|---|---|---|
| D1 | 任务 2 修后 M2 = `blocked=141 / eq=0 / n_a=27`（总 168）；§5 表 v7 总 **1566**、blocked **1378**、可判 **1379**、逐算子可判 **65/141/…** 全不变 | 实测 M2 = **168 blocked + 0 eq + 27 n_a = 195（总数不变）**；v7 = 总 **1593**、blocked **1405**、equivalent 8、可判 **1406**、**M2 可判 141→168**。原因：9 卡跳过注释后 `mut_m2` 命中**同串真实 `fixture:` 行**（∈ `gate_engine._PATH_FIELDS`）⇒ 27 条 eq 被 **un-mask 成 blocked**（不是"消失"）。§5 表与 §4 正文"continue 找下一个"不可同时成立 | **停在 Task 3 边界**：未冻结 v7、v6 保持权威；Task 2 的 fix 已按 §4 正文实现（commit d36d5c8）；待监工裁决「认账 un-mask（v7=1405/1593）」，或改 Task 2 口径（跳过注释后若**首命中即注释**则不落到后续真实路径、直接回 out_of_scope —— 但这不是 §4 的 `continue` 语义） |
| D2 | §4 称 9 卡"27/27 全部只改 frontmatter 注释行" | 复核一致；但**注释路径与 `fixture:` 真实路径同串**，故"跳过注释"必然落到真实 `fixture` 行 | 并入 D1 |
| D3 | §3.1「总卡数控制在 **12–18 张**」 | 8 卡（因「jobs=1 串行 < 90s」优先）：13 卡实测 139.3s、8 卡 85.9s | 取 8 卡（满足 <90s 且每算子 ≥1 blocked）；卡数偏离 12–18 |
| D4 | 任务 0.5 现状自检墙钟（对照用） | **未取到**（全量 `--selfcheck-determinism` 长跑被用户取消执行） | 以任务 1 优化后实测替代：串行小卡集 85.9s |
| D5 | 任务 1「只改自检的算子集与卡集选择」（未提上游测试） | 改 `selfcheck_determinism` 后，**579 的 3 条自检测试**（`test_579_selfcheck_passes_on_small_stable_subset` / `_detects_drift` / `_cli_exits_2_on_drift`）依赖旧"重跑传入 cards/ops"语义 ⇒ `-m slow -n0` 实测 **2 条红** | 已按新语义重写这 3 条（改 `monkeypatch _run_jobs` 的合成报告，纯内存、不再占 slow 墙钟），commit `577d57a`；579 的沙箱/工件隔离用例（①②）未动 |

## 任务 4a（commit `859f3d5`）测试依赖图（只读/幂等）
- 新增 `tools/test_dependency_graph.py`（ast 扫 import + 正则扫工件引用）→ `data/test_dependency_graph.md`(+`.json`)
- 结果：测试 **72** · tools 模块 **114**（**无任何测试覆盖 75**）· 被引用工件 **64**；连跑两次 md 逐字相同（SHA256 一致）
- 台账末尾注明"仅为 560-B3 前置数据；跳过判决测试属 W 档，本包不做选择"；未实现选择/跳过、未改 conftest/pyproject/SLOW_MODULES

## 任务 4b（commit `442020f`）pyproject 墙钟注释诚实化（纯注释）
- 实测（32 核，2026-09-19）：fast `-n auto` **87.3s / 86.8s**（464 passed, 2 skipped）；slow `-n0` **644.8s**（334 passed / 1 failed=golden 预期红）
- 第 158-159 行旧 `~10s`/`~140s` → 实测参考区间 `fast ≈ 85–90s`、`slow ≈ 10–11 min`，注明命令/并行度/核数/日期/"会漂移的参考值非契约"
- 只改注释；`addopts`（`-q`）/`markers` 未动（tomllib 解析已核）

## 任务 5（**未做**）cProfile stateful 剖析
- 任务书标注"可选，预算允许才做；否则整任务不做，不算欠账" ⇒ **未做**（本包已用大量预算；不做不欠账）。

## §7 收工总验收（fresh，退出码定论）
1. `tool_integrity.py --check` → **exit 0**（5 核心工具与基准一致；未改 CORE，无需 --update）
2. `gate_engine.py --check` → **exit 0**，**规则 63 · 命中 191（block=0 warn=186 advice=5）逐字不变**
3. `poison_drill.py` → **exit 0**，**124/124 · 39/63 · 表观 100% · 诚实 95.2% · 双指标 100%/100% 逐字不变**
4. `atom_evidence_replay.py --check` → **exit 0**，**confirm=56 refute=0 infra_error=0**
5. 全量 v7：冷跑 #1 与热跑 #2 **逐变体 0 差异**、两次 selfcheck exit0；数字 **1593/1405/1/179/equiv8/可判1406** —— **不符 §5 预测（1566/1378/1379）⇒ 未冻结 v7**（见 §6 D1）
6. 任务 1 新测试：干净态（`test_579_selfcheck_passes_on_stable_small_set`/`test_determinism_clean_synthetic`）exit0 · 注入偏斜（`test_determinism_falsifiable_skew`/`test_579_selfcheck_detects_drift`）报 `(False, diffs)` · 覆盖 fail-loud（`test_coverage_fail_loud_when_op_missing`）报错 · CLI（`test_cli_exit2_on_skew`/`test_cli_exit2_on_coverage_error`/`test_579_selfcheck_cli_exits_2_on_drift`）exit2
7. `pytest -m "not slow" -n auto` → **exit 0**（464 passed, 2 skipped, 5 snapshots passed）
8. `pytest -m slow -n0` → **exit 1**，**唯一红 = `test_json_output.py::test_golden_lock_json`**（golden 预期待人审 accept）；334 passed
9. ruff：589 所有新增/改动 `.py` → **All checks passed**（exit 0）
10. 受控目录零污染：`git diff --quiet -- atoms evidence Examples Book` → **exit 0**；`data/mutation/` 仅新增 `selfcheck_cards.json`（**未创建 v7**）；仓库根无遗留临时探针（探针全程落 `%TEMP%`）
11. 逐 commit 文件边界：5 个 589 commit（`bef65be`/`d36d5c8`/`859f3d5`/`577d57a`/`442020f`）各只带本任务文件；无 CORE 五文件 / poison 台账-快照 / `.env`

## 交人项
1. **v7 冻结裁决（D1）**：Task 2 un-mask 出 27 条真实 blocked（M2 141→168、总 blocked 1378→1405、eq 35→8、可判 1379→1406）。请裁「认账 un-mask（合 v7=1405/1593）」，或改 Task 2 口径（跳过注释后若**首命中即注释**则不落到后续真实路径、直接回 out_of_scope）。
2. **D3**：自检小卡集 **8 卡**（< 任务书 12–18），因 jobs=1 全算子串行须 <90s（13 卡 139.3s）。
3. **D5**：Task 1 行为变更连带更新了 579 的 3 条自检测试（commit `577d57a`）。
4. 588 期遗留 CRLF 假脏两条（`data/mutation/full_baseline_v4.json` / `evidence/conc/EV-CONC-001.md`）仍未提交未还原（本包沿例不动）。


