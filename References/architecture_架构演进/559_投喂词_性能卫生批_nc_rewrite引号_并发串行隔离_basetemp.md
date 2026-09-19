# 559 · 投喂词：性能与并发卫生批（-o 引号真 bug + 任意跑法不假红 + basetemp 根治卡顿）

> 你是「阙疑」元系统的建设者。仓库根 `C:\CodeLearnling\note\note\C++\CPP-Bible`，分支 master，Windows。
> 本批是**小而确定的卫生/化债批**：不加 gate 规则、不动 56 卡信任结论、不碰 L2/L3 功能，只修 558 验收暴露的一个真 bug、一处并发脆弱、一个环境卡顿源。
>
> **铁律（违反即返工）**
> - 解释器只用 `.venv\Scripts\python.exe`（PyYAML 6.0.3）；workbuddy python 禁跑门禁。
> - 一 Part 一 commit；每个修复配**回归锁 pytest**（正例+反例）；改核心工具后跑全量 pytest 并 `tool_integrity.py --update` 重钉。
> - 存量零误伤：gate 必须保持 **61 规则 · 命中 141（block=0 warn=136 advice=5）**；replay **confirm=56/refute=0/infra=0**；poison **107/107、覆盖 36/61+27**。
> - 不 push、不 --no-verify、不 golden accept、不改四桶分类。
> - 提示词与磁盘不符以磁盘为准，记偏差表；做不完按 Part 边界停（A>B>C），不留半成品。

---

## Part 0 · 开工对账
实测并记录基线：gate 61/141（block=0 warn=136 advice=5）、poison 107/107、replay confirm=56、`pytest -m "not slow" -n auto` 全绿、`pytest -m slow -n0` 全绿（含 test_golden_lock_json）、golden buckets 未分类=0。任一不符先停下报监工。

## Part A ·（P1 真 bug）阴面 `-o` 目标未加引号，产物可能写到 CWD
- 定位：`tools/atom_evidence_replay.py:1130 def _nc_rewrite(line, yang_rel, yin_rel, new_out)`，调用在 1245-1246（asm_out）、1276-1277（exe_out）。
- 现象（558 交人）：replay 阴面沙箱里，编译行的 `-o` 目标经 `_nc_rewrite` 改写后，若路径含空格/被 shlex 吃掉分隔符，会写成 CWD 相对名（曾在仓库根残留 `UsersASUS…replay_…nc_nc1.s`）。558 三条命令未复现，但定位明确。
- 先读 1130 函数体与调用上下文，确认它是字符串替换还是 shlex 分词；用**参数级**正确做法修复（推荐：shlex split → 定位 `-o` → 替换其后参数为 `new_out` → shlex join 时对含空格路径 quote；或等价的、对含空格/反斜杠/中文路径稳健的写法）。不要用脆弱的正则拼字符串。
- **回归锁**：构造一个路径**含空格的临时输出目录**跑阴面 rewrite/编译，断言产物落在该目录、仓库根与 CWD 不出现 `*.s/*.exe` 残留；再加一条"路径无空格时行为逐字不变"的对照。
- 验收：replay 全量 confirm=56；NC1 阴面仍 `阳=2 阴=0 flip verified`；仓库根 `Get-ChildItem *.s,*.exe`（构建产物外）为空。

## Part B ·（P2 并发健壮性）共享 replay 锁的测试，在任意 `-n` 跑法下都不假红
- **先侦察、别盲改**：确认 `tests/test_json_output.py::test_golden_lock_json`（:67）与 `tests/test_writer_selfcheck.py`（:12 起）是否都已标 `slow`；按设计跑法 fast `-n auto` + slow `-n0` 是否本就全绿（pyproject 注释写明两阶段是刻意设计，~14 模块共享 `build/.replay_lock` 与"删→重生成→比 sha→还原"）。
- 558 的假红只在**错误地对全量/slow 用 `-n auto`** 时出现。目标不是改两阶段，而是**让这两例即使被误并行也安全**：
  - **禁止重走 508 已证无效的 `--dist loadgroup` + `xdist_group("serial")`**（当时实测调度器读不到 marker，测试仍散到各 worker）。
  - 采用真正生效的串行隔离：让这些测试通过**同一把文件锁/复用 replay 既有 `build/.replay_lock` 的获取逻辑**串行化（拿不到锁就 skip-with-reason 或阻塞等待，不得假失败）；或等价的、在 `-n auto` 下也确定成立的机制。先写一个能在 `-n auto` 下**稳定复现假红**的探针，再修到连跑 3 轮全绿。
- 把权威两阶段跑法固化进 CI 配置/本地预检文档（若已有 `ci_local_precheck.py` 则核对它就是 fast 并行 + slow 串行，别让它静默漏抽）。
- 验收：`-m "not slow" -n auto` 连 3 轮全绿；`-m slow -n0` 全绿；**额外** `pytest -n auto`（全量误跑法）这两例不再假红（串行化或带因 skip，不许 F/E）。

## Part C ·（P2 环境卫生）pytest 临时目录移出系统 %TEMP%，根治 safe-delete 卡顿
- 现象：pytest 默认 tmp 在系统 `%TEMP%`（writable root 外），会话收尾批量删 >500 个临时文件触发 `[safe-delete][SAFE_DELETE_BULK_CONFIRM_REQUIRED]`，表现为每次测试后卡很久、偶发首轮假红 rc=1（复跑即绿）。
- 修法：`pyproject.toml [tool.pytest.ini_options]` 的 `addopts` 增加仓内临时目录（按本机 pytest 版本支持的参数名，先 `pytest --help` 确认是 `--basetemp` 及 tmp 保留策略参数的准确名字，**不要凭记忆写错参数**），指向仓内（如 `.pytest_tmp`），并把该目录加入 `.gitignore`（注意：.gitignore 规则**不要写行内注释**，508 已证行内注释会使整条规则失效）。
- 这是改核心测试配置：改完 fast + slow **两阶段都全量回归**；确认临时文件确实落在仓内、收尾不再触发 safe-delete、`.pytest_tmp` 不进 git status。
- 验收：连跑 2 轮无 safe-delete 拦截输出；git status 不出现 `.pytest_tmp`；全量测试结果与改前逐字一致（只改位置不改判定）。

---

## 收工总验收（fresh，写进 _worklog_559.md）
gate 61/141 不变 · poison 107/107（覆盖 36/61）· replay confirm=56/refute=0 · fast `-n auto` 连 3 轮绿 · slow `-n0` 绿 · 全量 `-n auto` 两例不假红 · 仓库根无 stray `.s/.exe` · 无 safe-delete 卡顿 · tool_integrity 已重钉（若动了被钉工具）· 受控目录零污染（仅 pre-existing EV-CONC-001）。偏差表逐条记录。

## 明确本批不做
不加 gate/poison 规则；不改 56 卡与 golden 四桶；不做 replay 并行化（那是 trae 560 调研后的专项，本批只做"任意跑法不假红"的防护）；不做 golden_lock 自身并行；不碰 L2 task_queue 功能、不开 L3、不开 G-supervisor。
