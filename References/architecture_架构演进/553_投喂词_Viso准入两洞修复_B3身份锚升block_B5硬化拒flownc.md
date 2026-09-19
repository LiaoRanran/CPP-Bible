# 553 · 投喂词：修 V-iso 准入层两洞（B3 身份锚升 block + B5 硬化拒 flow nc）

> 来源：547 异族对抗（`_adv_v95b/`）报 B3/B5 两 ESCAPE；assistant 已独立复跑探针确认复现、已读 `viso_diff.py` / `atom_evidence_replay.py` / `gate_engine.py` 源码核实机制。
> 目标：把"阴阳同构准入层"的两道身份/解析缺口补齐，让 gate 准入层（不编译）就对 `negative_controls` 不再零认知。
> 执行方：好模型/苦力；本词写到照做粒度。一任务一 commit。

## 〇、开工前必读（先建基线，别照抄本词数字）
1. 权威解释器：`.venv\Scripts\python.exe`（有 PyYAML）。禁止用无 pyyaml 的解释器跑门禁。
2. 跑基线并记录（开工快照，收工要逐字对比）：
   ```
   .venv\Scripts\python.exe _adv_v95b/probes/run_all.py        # 当前红：2 ESCAPE（B3/B5）
   .venv\Scripts\python.exe tools/cppbible.py gate --check     # 规则数/block/warn/advice
   .venv\Scripts\python.exe tools/cppbible.py poison_drill
   .venv\Scripts\python.exe tools/cppbible.py replay --check
   .venv\Scripts\python.exe -m pytest -m fast -q
   ```
3. 现状真相（assistant 已读码确认，供你对照，仍以你磁盘实测为准）：
   - B3：`tools/viso_diff.py::validate_nc_schema` 约 L341-347：阴面 fixture 的**命名规约只 `warns.append`**（注释自述"v1 只告警，收集一批后再谈升 block"）。它只拦"fixture==阳夹具自身"（约 L337），**从不验证阴面与阳夹具同源**。且该纯函数只有 replay 路径（`atom_evidence_replay.check_negative_controls` 约 L1217）调用，**`gate --check` 硬化层不知道 nc 存在**。
   - B5：`tools/gate_engine.py::_fm_hardening_uncached`（约 L1316-1354）四信号：indent-smuggle 只认 block 式缩进、dup-key、invalid、parse-diverge（只比对 id/verdict/status/artifact_sha256 四键）。flow 式 `negative_controls: [...]` 被自定义 `parse_frontmatter`（replay 侧）收下成 list，但硬化层四信号无一触发 → gate 给虚假干净。replay `check_negative_controls` 约 L1191/L1207 才要求 block list / block map。

## 任务 1（P0）B3：阴面 fixture 身份锚升 block
**改 `tools/viso_diff.py::validate_nc_schema`**：
- 把约 L345-347 的命名规约从 `warns.append(...)` 改为 `errs.append(...)`（block）。
- 精确规则：阴面 fixture 的文件名 stem **必须等于** `阳夹具主干名 + "." + nc_id后缀`：
  - `yang_stem` = `yang_fixture` 去目录、去后缀（`.cpp/.cc/.cxx`）后的 basename。
  - 若 `nid` 已以 `nc` 开头（如 `nc1`），期望 stem 以 `.{nid}` 结尾（如 `_atom_fence_vs_atomic.nc1`）；否则期望以 `.nc{nid}` 结尾。
  - 不符 → `errs.append(f"{tag}: 阴面 fixture 未锚定本卡阳夹具：{posix!r} 期望 `{yang_stem}.nc{nid}`（身份绑定，防借别卡产物冒充翻转证据）")`。
- 保留现有其它校验一字不动（fixture 相对路径、后缀、不指 build/、不指阳夹具自身、存在性、anchor 单定义、retain/probe 校验）。
- **存量零误伤硬门槛**：开工先跑一次——当前唯一带 nc 的卡是 `ATOM-CONC-001`，其阴面 `Examples/atoms/_atom_fence_vs_atomic.nc1.cpp`（stem=`_atom_fence_vs_atomic.nc1`，阳夹具 `_atom_fence_vs_atomic.cpp` 主干=`_atom_fence_vs_atomic`，nid=`nc1`）应**恰好合规**。若体检发现任何存量卡不合规，**不要硬升 block**：改为先把那张卡的阴面改名为规约名（加法、不动语义），再升 block，并在 worklog 记录。
- 为什么现在做：schema 是 fail-closed 层，第一道身份门不能开着；内容 diff 仍由 replay 的 `judge_min_diff` 兜底，本任务只是把"同源假设"在静态层也钉死。

## 任务 2（P0）B5：硬化层拒 flow 式 negative_controls
**改 `tools/gate_engine.py::_fm_hardening_uncached`**：
- 在现有四信号之前，对 frontmatter 原文 `fm` 增一条信号：扫每一行，若命中 `^\s*negative_controls\s*:\s*\[`（行内直接 flow list 起点）→
  `Finding("EV-FM-YAML-HARDENING", "block", _rel(p), "[nc-flow] negative_controls 必须用 block 式（533 §2.1）：flow 式会让硬化层与 replay 判决不一致", "改为 block 式逐行写法")`。
- **不要**走 parse-diverge 路线（已分析：flow 式 nc 自定义解析器与 PyYAML 都收下成 list，两解析器无分歧，parse-diverge 永远不触发——这条死路明确排除）。
- 实现注意：检测基于 frontmatter 原文正则（在 `yaml_mod is None` 早退之前也要跑，保证无 pyyaml 环境也能拦 flow）；block 式（`negative_controls:` 换行 `- id:`）不得误报。
- **存量零误伤硬门槛**：先确认 `ATOM-CONC-001` 的 nc 是 block 式（多行 `- id: nc1`），不是 flow 单行式；若是 flow 式，先改成 block 式再升 block，worklog 留痕。

## 任务 3（P1）：探针转正式回归 + poison 锁
- 把 `_adv_v95b/probes/probe_viso_negative.py` 的 B3/B5 两个 ESCAPE 断言，改写为 `tests/` 下正式 pytest（一个测"借来的/命名不符阴面 → validate_nc_schema errors 非空"，一个测"flow 式 nc → 硬化出 block Finding"）。探针文件保留（可复跑证据），但回归不得只依赖探针。
- 给 `tools/poison_drill.py` 加对应毒样例载荷（B3 借品阴面、B5 flow 式 nc），确保对应规则进 RULE-COVERAGE、无 uncovered。注意历史坑：覆盖正则只认字面量 `"RULE-ID" in who`，参数化比较会"载荷全过但规则仍算未覆盖"。
- gate_engine.py 与 viso_diff.py 都是被 `.tool_checksums` 钉住的核心工具 → 改完必须 `python tools/tool_integrity.py --update` 重钉。

## 任务 4（验收）
1. `.venv\Scripts\python.exe _adv_v95b/probes/run_all.py` → B 面 **0 ESCAPE**（B3/B5 由 ESCAPE 变"被拦/PASS"）。
2. 全套门禁 fresh 复跑，与开工基线逐字对比：
   - `gate --check`：新规则只作用于不合规写法；**存量 56 卡零新增命中**（block/warn 数字与基线对比，若涨必须解释是哪张卡、为何本就不合规）。
   - `poison_drill`：全过、RULE-COVERAGE 无 uncovered。
   - `replay --check`：confirm=56 / refute=0 / infra_error=0（nc 判定路径不能回归）。
   - `pytest -m fast` + `pytest -m slow` 全绿（**改核心工具后跑全量，不只单文件**——528 教训：ConstructorError 改名只跑单文件漏检）。
   - `tool_integrity`：重钉后 exit 0。
3. `git status`：受控目录 `atoms/ evidence/ tools/ tests/ Examples/` 改动仅限本任务；零污染自证。

## 硬纪律（违反即回滚重做）
- 一任务一 commit：B3 / B5 / 回归锁+毒样例 各一 commit。
- 不 push、不 `--no-verify`、不 golden `--accept`、不动任何 signed_by / 人签字段。
- 存量零误伤是硬约束：升 block 前必跑存量体检；误伤存量就先把存量改合规（加法），不许为了数字好看放宽规则。
- 诚实：若复跑发现 B3/B5 修法与既有 block 路径重复命中、或存量无法零误伤，**停手报告，不硬上**（541 两次回退的教训）。
- 交人项：B1/B6（需真实编译 -O0/-O2/-Os 比对 nc1 诚实性）本轮不做，记入 worklog；C2（549 自测范围）未实现，不在本词范围。

## 收工要汇报的数字
探针 ESCAPE 数（2→0）、gate 规则数与 block/warn 对比、poison 覆盖数、replay confirm 数、pytest 通过数、tool_integrity 状态、各 commit hash。复跑命令照抄本词第〇节。
