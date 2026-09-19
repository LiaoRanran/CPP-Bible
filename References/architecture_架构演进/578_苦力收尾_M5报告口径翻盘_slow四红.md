# 578 · 苦力收尾批：M5 报告口径翻盘 + slow 四红（一任务一 commit）

> 基线锚点（开工前必须实跑核对，勿凭记忆）：HEAD = `a10c6e0`（575 命题级活性锚）；
> `gate --check` = 63 规则 / 191 命中（block=0 warn=186 advice=5）；poison 118/118；
> **`pytest -m slow -n0` 当前红 5 个**（本批任务 2 修其中 4 个，第 5 个 golden 待人 accept，不许自签）。
> 权威解释器 `.venv\Scripts\python.exe`（无 pyyaml 会静默漏拦，禁 workbuddy/uv python）。

## 为什么有这一批（监工已独立验收 575）
575 的闸门设计对——命题级活性锚让 M5 不再蹭卡级放行（监工探针实测：现状 escaped29，并入文案后 escaped0）。
但它**没跑 slow 就收工**，slow 暴露 4 个收尾遗漏 + 1 个预期债务。本批不建新规则，只收口。

---

## 任务 1：修 `_findings_key` 吞告警，让 M5 在报告口径翻盘（下批第一件事）

**位置**：`tools/mutation_fuzz.py:88` `_findings_key()`，现返回 `(rule_id, severity, target)` 三元组。
**bug**：同一张卡上第二条同规则告警，因三元组不含文案/pid，被 `new = _snapshot() - baseline` 集合差吞掉。
M5 正是此形：基线已有 prop-1 的 OBSERVATION-LIVENESS warn，变异给 prop-2 再添一条同规则同卡 warn ⇒ 三元组相同 ⇒ 判 escaped。

**修法（监工已独立探针验证方向成立）**：把文案并入键 → 四元组 `(rule_id, severity, target, message)`。
监工探针 `_adv_v96/probe_m5_findings_key.py` 实测：三元组 escaped29 → 四元组 escaped0、warn_only29/strict0。

**必须同步改的解包点（别只改函数，否则 classify 崩）**：
1. `classify()` 内约 486–487 行：`new_block = sorted({f"{r}:{t}" for r, s, t in new if s=="block"})` 和 `new_warn` 的三元组解包——改成兼容四元组（`for r,s,t,*_ in new`，或按 `k[0],k[1],k[2]` 索引）。
2. 两条 548 用例（它们自己造假 new 集、按 3 元组解包）——改成四元组断言，不要为省事把它们删了或改成恒真。

**验收数字（以你重跑 v5 实测为准，别照抄监工/监工自报任何一方）**：
- 重跑 `mutation --cards all --operators M5 --limit 999`，落 `data/mutation/full_baseline_v5.json`。
- 必须见到 M5 escaped=0；strict/warn_only 真实分布你自己报（监工探针是 warn_only29/strict0；上一批苦力自报 warn_only27/strict2——**两处对不上，你重跑后给唯一真值**，并说明 strict 那几条是哪条规则、为何是 block 不是 warn）。
- metrics_collector 升 v5（v1–v4 保留不覆盖），逃逸率口径沿 565b（可判分母、n_a 不进、M5 不填 0）。
- 把工作树那 6 行 `_findings_key` 修法注释（现未提交）和代码改动**同 commit** 带上。

---

## 任务 2：补 slow 四红（都是小修，不改设计）

### 2.1 `tests/test_gate_engine.py::test_observation_liveness_live_observation_passes`
夹具 `_OBS_PROP` 是 observation 命题但没带新的命题级 `liveness` 字段，被 575 新规则 warn。
**修法**：给这个正例命题补 `liveness: {kind: fixture_symbol, symbol: spin_plain}`——证据卡 `symbol_map` 里本就有 `spin_plain: _Z10spin_plainv`，补锚后 `_prop_liveness_ok` 过，走到卡级三条件（有夹具符号+量化）⇒ 放行 ⇒ 测试 `== []` 重新成立。

### 2.2 `tests/test_gate_engine.py::test_observation_liveness_skips_when_no_artifact_assertion`
这个边界测试的本意是"证据卡连工件断言都没有时，本规则不重复报警（交 OBSERVATION-NEEDS-ARTIFACT block）"。
575 后命题级锚检查在最前，共享 `_OBS_PROP` 若按 2.1 补了锚，就不再测到原语义。
**修法**：把该测试的命题改造成**带合法 liveness 锚、但证据卡无 artifact_assert**——这样 `_prop_liveness_ok` 过，才轮到"无工件断言⇒跳过"分支。别偷懒把断言删掉了事。

### 2.3 `tests/test_poison_attack_type.py` 两红（台账过期）
P74/P75/P76 在 `poison_drill.py:2052` **已正确映射 A3**，但落盘 `data/mutation` 或 surface_map 台账是加映射前的旧版（P74 记成 `A?`、A3 台账 18 < 静态 20）。
**修法**：重跑 `python -m tools.poison_drill --write-surface-map` 刷新台账。然后这两测自然转绿；若 A3 计数仍不一致，按 `test_surface_map_not_stale` 的断言（台账 >= 静态登记、覆盖性一致）对到实测数字，不要改测试凑数。

### 2.4 `test_json_output.py::test_golden_lock_json`
warn 136→186 是 575 暴露的存量债务（50 条 observation 缺命题锚），**预期红、不许你 --accept、不许改测试**。本批保持它红，交监工/人审。

---

## 任务 3：收工门禁（fresh，串行，全跑）
1. `pytest -m "not slow" -n auto` exit 0；
2. **`pytest -m slow -n0` exit 0，仅允许 test_golden_lock_json 这 1 个预期红**（其余 4 个必须转绿）；
3. `tool_integrity.py --check` exit 0（改了 gate_engine/poison_drill 才重钉；本批若只动 mutation_fuzz + 测试 + 台账，按 CORE_TOOLS 清单判断要不要重钉）；
4. `gate --check` 仍 63/191 block=0 warn=186（本批不该变命中数）；poison 118/118（重写台账后只多不少）；replay confirm=56；
5. `git diff --quiet -- atoms/ evidence/` 受控目录零真实改动（EV-CONC-001 行尾 stat 假 M 除外）。

## 铁律（重申）
- 一任务一 commit（任务1、任务2.1-2.2、任务2.3 各自 commit）；新规则 warn 起步、存量零误伤；护栏不许裸 except，其"绿"必须有可证伪测试。
- 不编数字：v5 逃逸率/strict 分布用重跑实测值，别照抄任何旧账。
- golden accept 权、机器给卡面填锚权都在人；你只跑工具、改测试、重写台账，不碰卡面命题内容。
- 停在 T 边界：做不完就把精确施工点写进 `_worklog_578.md`，不留半成品。
