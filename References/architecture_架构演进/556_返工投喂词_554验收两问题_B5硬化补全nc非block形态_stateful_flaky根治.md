# 556 · 返工投喂词：554 验收两问题 —— B5 硬化补全（nc 非 block 形态）+ stateful flaky 根治

> 背景：554（批次 T）独立验收。信任基线**未被破坏**（554 只动 tests/ 与 dev 依赖，未碰 tools/；gate 规则 61/命中 141/block=0 warn=136 advice=5、poison、replay confirm=56 均不变，已由监工独立复跑确认）。新测试资产成色高（A3/A5/A7 三洞确定性回归、touch 归一、retry cap、deps 门、快照 5 项、parser 差分都在，临时库隔离正确）。
> **但"连续 4 次全绿"自报与磁盘不符**：监工复跑抓到 2 个问题，必须闭环后才算交付。用 `.venv\Scripts\python.exe`。
> 纪律：一问题一 commit；不 push、不 --no-verify、不 golden accept；存量 56 卡零误伤是硬约束。

---

## 问题 1（P0，确定性真盲区）：parser 差分稳定红 —— 553 B5 硬化不完整

**复现（稳定）**：
```
.venv\Scripts\python.exe -m pytest tests/test_parser_differential.py::test_no_gray_state_between_parsers -n0 --tb=short
```
**失败用例（Hypothesis 已 shrink 出）**：`fm = 'negative_controls: 00000000'`
- 自定义 `parse_frontmatter` 把该裸标量解析为字符串 `'00000000'`；
- PyYAML `safe_load` 解析为整数 `0`（YAML 前导零数字）；
- 两解析器对 `negative_controls` 分歧，但硬化层 `blocked=False` ⇒ 断言"分歧必须显式 block"失败。

**根因（先读码确认行号，别照抄）**：553 B5 在 `tools/gate_engine.py` 的 `_fm_hardening_uncached` 里，只用正则 `^\s*negative_controls\s*:\s*\[` 堵了 **flow 列表 `[...]`** 一种形态。`negative_controls` 合法形态只应是**块式序列**（键独占一行、下一行起缩进 `- ` 列表项）。flow `[`、裸标量（`00000000`/`abc`）、inline map（`{...}`）等**一切非块式形态**在 `gate --check` 硬化层仍然沉默——而 gate 不跑 replay 的 schema 校验，于是给出"干净"的假象。这与 B5 当初堵 flow 的理由完全同构，属同一洞没补全。

**修法（给方向，照磁盘现状落码）**：
1. 把判定从"正则枚举 flow `[`"升级为**白名单形态判定**：frontmatter 中一旦出现 `negative_controls` 键，只接受合法块式序列（该键行末无值/无 `[`/无标量，后续为缩进 `- ` 项）；凡检测到 flow `[`、裸标量、inline map 或其他非块式形态 ⇒ 出 `[nc-form]` block 信号（rule_id 仍归 `EV-FM-YAML-HARDENING`，message 区分 nc-flow/nc-scalar/nc-map）。
2. **作用域严格限定 `negative_controls` 这一个键**，不要把其他合法使用 flow/标量的字段一起拦了（先 grep 全库 frontmatter 确认哪些字段合法用 flow，避免误伤）。
3. 前导零分歧（`00000000`→字符串 vs 整数 0）是更广义的 parser divergence：本批至少在 `test_parser_differential.py` 里把"标量前导零/yes-no-on-off 等 YAML 1.1 陷阱词"列为已知分歧清单（注释或 xfail 登记 + 指向本任务），是否扩到其他键的硬化另开任务，不在本批扩大改动面。

**验收（机器判据）**：
- `test_no_gray_state_between_parsers` 转绿；
- 唯一合法块式 nc 的卡 EV-CONC-001 **仍 0 命中**（零误伤，必须实跑 gate 确认）；
- 新增毒样例：`tests/poison/` 加 P43d（裸标量 nc，期望 block；可再加 P43e inline-map nc），登记 ATTACK_TYPES，`poison_drill` 全过且 RULE-COVERAGE 分子同步；
- 改了 gate_engine/poison_drill 必须 `tool_integrity.py --update` 重钉（viso_diff 不在 CORE_TOOLS，勿动）；
- gate 收工仍为 block=0、warn 不新增（136 不变）；replay confirm=56；`pytest -m "not slow" -n auto` 该文件绿。

## 问题 2（P1，flaky 必须根治）：stateful TestTQ 概率性红

**现象（监工实测）**：
- `pytest -m "not slow" -n auto` 全量时偶发：`FAILED tests/test_task_queue_stateful.py::TestTQ::runTest - hypothesis.errors...`，失败最小步骤显示为 `state = TQMachine(); state.teardown()`（零步/teardown）；
- 与 parser_differential 同会话 `-n0` 也曾复现一次；但**单独 `-n0` 连跑 3 次均通过**，失败后无法稳定复现——典型依赖真实时钟 / 文件句柄 / 会话内共享状态的非确定性，不是确定性逻辑错。
- 现状代码已 `deadline=None` 且 `suppress_health_check=list(HealthCheck)`，但 flaky 仍在；**禁止再靠 suppress/跳过测试掩盖**。

**要求：必须让 `pytest -m "not slow" -n auto` 连续 5 轮全绿**（写进 worklog 附 5 轮输出），不能偶发红进 CI。

**排查方向（逐条证伪，别猜）**：
1. **sqlite 连接/WAL 句柄（Windows 头号嫌疑）**：读 `tools/task_queue.py`，确认每次 `db_path=...` 调用是"新开连接、用完即关"还是复用了模块级/全局连接。teardown 是 `shutil.rmtree(ignore_errors=True)`——若 tq 内部还有连接句柄/WAL 没关，Windows 下文件删不掉、下一实例或同 worker 后续测试可能踩到残留。正确修法是**连接随 db_path 隔离、teardown 前显式关闭本测试库的所有连接**（在测试里持有 connection 并 close，或给 tq 加 close/上下文管理），而不是 ignore_errors 吞掉。
2. **预算 invariant 的时钟/中间态**：`inv_db_consistency` 的 `desc <= budget_calls` 是否在 yield 创建子任务与父预算字段更新之间存在可读中间态（单线程状态机理论上没有，但要核实 tq.yield_task 是否分多次 commit）；心跳 rule 用真实 `time.time()`、invariant 也取 now，确认不存在跨秒边界把合法心跳判成 future。
3. **会话内共享**：确认 stateful 不依赖任何模块级全局（全局连接、全局计数器、真实 `data/tasks`）；每个 TQMachine 实例的 `mkdtemp` 目录唯一（已确认），但若 tq 有模块级单例缓存，需按 db_path 做 key 隔离。
4. **禁止用 `@pytest.mark.serial`/踢出 `-n auto`/降 max_examples 来"消灭"flaky**——stateful 用独立临时库，本就该能并行；若证实根因是 tq 的全局共享连接，正解是修 tq 的连接隔离（这会让真实并发也更稳，呼应 535 冷启动竞态那类问题），不是降级测试。若最终证明某条 flaky 确属不可消除的真实时钟噪声，须在 worklog 给出证据并 freeze 时钟（注入 clock，而非用墙钟），仍保持并行。

**验收**：`-n auto` 连续 5 轮 fast 全绿；确定性的 A3/A5/A7/touch/retry/deps 用例不受影响；若改了 `tools/task_queue.py`，跑其全量 pytest + ruff 0.6.9，并确认真实 `data/tasks`（若存在）默认行为逐字不变、零污染。

---

## 收工总验收（fresh run，逐项报实测）
1. `pytest -m "not slow" -n auto` **连续 3 轮全绿**（问题 2 要求开发期连 5 轮）；
2. `pytest -m slow -n0`：除 `test_golden_lock_json` 这 1 条 **pre-existing** 外全绿——该条是 golden 基线（warn 59，最后 accept 于 67c1962）落后于 548/553 后 gate 新规则（warn 现 136），**开工前 c15614e 就已红，与 554/556 无关，禁止代签 accept**，在 worklog 注明待监工安排一次 warn 分类签署；
3. gate 规则 61/block=0/warn=136/advice=5（问题 1 修复后 warn 不新增、block 仍 0，仅 poison 毒样例被拦）；poison 全过、覆盖分子同步；replay confirm=56/refute=0；
4. 受控目录零污染；问题 1、问题 2 各自独立 commit；worklog 写明两条问题的根因证据与复现/修复命令。

## 交监工裁决（不自动做）
- golden_lock warn 59→136 的分类签署（含 INFERENCE 28 条等四桶）何时安排 `--accept`；
- 是否为前导零/YAML 1.1 陷阱词的跨键 parser divergence 单开一个硬化任务。
