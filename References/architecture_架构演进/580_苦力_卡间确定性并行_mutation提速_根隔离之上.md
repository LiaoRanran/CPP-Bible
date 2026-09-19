# 580 · 苦力建设投喂词 —— 卡间确定性并行（在 579 根隔离之上，先兑现 mutation 提速）

> 角色：你是机械建设者。**只做本任务书写明的，不扩范围、不抢架构决策。**
> 全程以磁盘现状为准（行号会漂移，用符号名定位）；数字一律实测，跑多少报多少，不编、不抄旧数。
> 铁律重申：判决逻辑一个字不许为速度改动；新能力默认 OFF；存量零误伤；一任务一 commit；
> 改 CORE_TOOLS（gate_engine / atom_evidence_replay / poison_drill / toolchain / cppbible）必须
> 同 commit `python tools/tool_integrity.py --update` 重钉并带上 tools/.tool_checksums。
> 解释器只用 `.venv\Scripts\python.exe`；ruff 用 `uv tool run --from ruff==0.16.5 ruff check`
> （pyproject 已钉 select=["E4","E7","E9","F","I001","FURB167"]）。PowerShell 内联 `python -c`
> 嵌套引号必坏，探针一律写独立 .py。

---

## 0. 背景与本批边界（先读懂，别重造）

- 579 已落地**工件层根隔离**：`atom_evidence_replay.run_root()`（ContextVar，默认=真实 ROOT）、
  `batch_root(p)`（@contextmanager，try/finally 还原）、`manifest_path()`（=run_root()/build/manifest）；
  mutation 的 `sandbox()` 现在每轮复制 atoms/evidence/**Examples** 进一个 tmp，并用 `batch_root(tmp)`
  让 replay 与 gate 的工件读取全部落 tmp，对真实 ROOT 零副作用（监工已在脏态独立验收 989/9/185）。
- **当前长尾是 mutation 全量**：83 卡 × 7 算子 ≈ 1183 变体，单进程约 11–16 分钟（每变体一次全库
  `ge.run()`，M1/M7 还真编译）。replay 全量仅 ~127s、golden 已在 568 复用 manifest（249s→11s），
  **本批不做 replay/golden 的并行 CLI**，只做 mutation 并行；但本批改的"锁分片"原语会为下批 replay
  并行铺路。
- 权威串行数字（本批结束必须**逐变体不变**）：全量 blocked 989（严格 619）/ escaped 9 / n_a 185；
  逐算子 M1 64/1/27｜M2 168/0/27｜M3 65/0/42｜M4 200/0/33｜M5 29/0/56｜M6 324/8/0｜M7 139/0/0
  （b/e/n_a）。命令：
  `python -m tools.mutation_fuzz --cards all --operators M1,M2,M3,M4,M5,M6,M7 --limit 999 --report <path>`

### 第 0 步：开工基线核对（先量后动，结果写进 worklog，不允许跳过）
1. `git log --oneline -3` 确认 HEAD 含 579 三笔（fdb210a / 296fb6e / 2cc5a5a）。
2. 串行全量实测一次 `--jobs` 改造前的墙钟（现状即串行），记 `elapsed_s`（从 report JSON 顶层读），
   作为加速比分母；同时落一份串行 report（如 data/mutation/_580_serial.json）。
3. 读码定位并记录现状行号：`atom_evidence_replay._REPLAY_LOCK` 及其全部引用点；
   `mutation_fuzz.sandbox()`、`run_fuzz()`（卡维外层 + 单一 sandbox + 单一 baseline）、
   `classify()`、模块全局 `STATS`、`_snapshot()`、`_variant_index()`。
4. 记录物理核数（`os.cpu_count()`），作为 jobs 上限依据。

---

## 任务 1（前置）：replay 并发锁跟随跑批根分片 —— 独立 commit

**现状**：`_REPLAY_LOCK = ROOT / "build" / ".replay_lock"` 是模块级常量（约 :939），
被 `_acquire_replay_lock` / `_try_unlink_lock` / `_read_lock_pid` 引用。它硬编码真实 ROOT，
导致哪怕每个 worker 已在各自 `batch_root(tmp)` 里跑，所有进程仍抢同一把全局锁 → 并行被串行化
（加速比≈1，且 120s 等待易超时假红）。

**改法（机械、最小）**：
1. 把模块常量替换为一个路径函数：
   `def _replay_lock_path() -> Path: return run_root() / "build" / ".replay_lock"`
   （run_root() 已在本文件定义；**默认无 batch 时返回真实 ROOT，路径与今天逐字节相同**）。
2. 上述三个函数体内所有 `_REPLAY_LOCK` 引用改为调用 `_replay_lock_path()`（局部取一次值再用，
   避免 acquire 循环里重复求值）。`_release_replay_lock` / `_install_lock_cleanup` 同理核对。
3. **CCACHE_DIR（约 :847）保持指向真实 ROOT 不动**：ccache 自身设计为并发安全（自带锁），
   多 worker 共享一份编译缓存反而更快；P0-A 独立重编仍 `CCACHE_DISABLE=1`，安全性不变。
4. 不要动锁的语义（O_CREAT|O_EXCL 互斥、pid 存活接管、stale 接管、等待/超时参数分离）。

**机器验收（正反例都要有）**：
- 同根并发仍互斥：同一 run_root 下两进程/线程同时 `_acquire_replay_lock`，只一个成功、另一个等待
  （复用现有 E09 锁测试的口径，原有锁测试必须全绿、行为不变）。
- **异根不互斥（新正例）**：两个不同 `batch_root(tmpA/tmpB)` 上下文里同时 acquire，**都立即成功、
  互不阻塞**（这是并行能成立的证据；旧代码此例必串行）。
- 真实根回归：不进 batch_root 的普通 CLI 路径，锁文件仍落在真实 `build/.replay_lock`
  （断言路径字符串与改造前相等）。
- 这是 CORE_TOOLS 改动：跑 `python -m tools.atom_evidence_replay --check`（confirm=56/refute=0）、
  `python -m tools.poison_drill`（118/118、零覆盖攻击面无）、`python tools/tool_integrity.py --update`
  重钉并同 commit 带 .tool_checksums；新增/改动测试进 tests/。

---

## 任务 2：mutation 卡间进程并行（--jobs，默认 OFF=今天的串行路径）—— 独立 commit

**为什么是进程池不是线程池、为什么每 worker 一个根**（想清楚再写，否则必出跨卡污染）：
- 现状所有卡共享**一个** sandbox 根与一次 baseline 快照，卡末才还原。若多线程共享一个根，
  worker A 改卡 X 时其全库 `ge.run()` 会读到 worker B 正在变异的卡 Y（跨卡污染，重现 548 之前的 bug）；
  且 ge.run 持 GIL、模块全局 `STATS`/缓存竞态。
- 正解：**进程池，每 worker 进程一个独立 sandbox 根**（各自 copytree atoms/evidence/Examples +
  空 build + 各自 `with replay.batch_root(自己的tmp)` + 各自算一次全库 baseline）。worker 内部
  对分到的卡仍**卡内串行、卡末 finally 还原**（沿用 run_fuzz 卡循环与 finally 的全部纪律）。

**实现要求**：
1. CLI 加 `--jobs N`，**默认 1 = 今天的 run_fuzz 串行路径，逐字节等价（旧函数不删、不改签名行为）**。
   `--jobs 1` 必须走原串行代码；`--jobs N>=2`（或 `--jobs auto` = `min(4, os.cpu_count()-1, 卡数)`）
   才走新进程池路径。默认 OFF 是硬要求（小批 copytree 开销不划算，也保证零行为漂移）。
2. 用 `concurrent.futures.ProcessPoolExecutor`（Windows 默认 spawn）。**initializer 在 worker
   进程内一次性建好该进程独占的 sandbox 根 + batch_root + baseline**，worker 生命周期内处理多张卡；
   进程退出用 try/finally（+必要时 atexit）清理自己的 tmp 根（`tempfile.mkdtemp(prefix="mutworker_")`），
   不得在真实 build/ 留 worker 残片。
3. 调度单位 = **卡**：把 selected 卡切成 N 份（或任务队列领卡，均可），每个卡任务返回
   `(卡rel, 该卡全部变体 per 记录列表, 该卡的 STATS 增量)`。
4. **STATS 不能用全局自增跨进程聚合**（ge_runs/replay_runs/replay_skipped 在各进程独立会丢）：
   worker 必须把本卡的三个计数随返回值带回，主进程求和，总数与串行一致。
5. **结果顺序必须确定化**（进程完成顺序是非确定来源）：主进程拿到全部卡结果后，
   **按串行顺序重排**——卡顺序 = 输入 selected 顺序，卡内按 ops 顺序、再按变异点顺序，
   使最终 `results` / `by_operator` / `by_card` / counts 与 `--jobs 1` **逐条相等**。
   报告里加 `"jobs": N` 与 `"parallel": bool` 字段（只加不改既有字段）。
6. spawn 约束：worker 入口函数、卡处理函数必须是**模块顶层可 pickle** 对象；不要把 baseline
   （大 set）跨进程传入，让每个 worker 自己算；只传卡路径字符串、ops、limit 等可 pickle 标量。
7. `--progress`：主进程在每个卡任务**完成**时打印 `(已完成卡数/总卡数) 卡rel`（完成顺序无所谓，
   只是活性指示）；禁止多 worker 直接写同一 stdout 造成交错。
8. worker 内异常必须冒泡成 fail-loud：任一卡任务抛错，整批 exit 非 0 并打印是哪张卡/哪个算子，
   不许静默丢卡（丢一张卡就会改变分母）。

**机器验收**：
- `--jobs 1` 全量结果与第 0 步串行 report 的 by_operator / 三个总数 / variants 数**逐字相等**。
- 新增单元测试（可用 2–3 张小卡 + 1–2 个算子，跑得快）：
  (a) `--jobs 1` 与 `--jobs 2/4` 的 `_variant_index()`（卡,算子,变异点 → 5 字段）**完全相等、空 diff**；
  (b) 异根确实并行（可断言两个 worker 的 run_root() 不同、锁路径不同）；
  (c) 结果顺序与串行一致（断言 results 顺序，不只断言计数）；
  (d) STATS 三计数 jobs1==jobs4；
  (e) 任一 worker 注入异常时整批非 0 退出（可 monkeypatch 某卡 classify 抛错）。

---

## 任务 3：判决一致性硬门 + 真实根输入冻结 —— 独立 commit（可与任务2同批，验收独立）

1. **一致性对账（最高优先级，高于提速）**：提供一个可复跑对账（测试或 `--selfcheck-determinism`
   扩展），对同一卡/算子集合分别跑 jobs=1 与 jobs=4，用现有 `_variant_index` 逐变体比对
   `_SELFCHECK_FIELDS`（verdict/kind/why/new_block/new_warn），**出现任何差异即 exit 2 并打印
   分歧变体清单**；全空才算过。`--selfcheck-determinism` 在 `--jobs 4` 下也必须通过。
2. **真实根输入冻结双保险**：进程池启动前主进程算一次真实根指纹（Examples + atoms + evidence
   全树，排序文件 路径+内容 sha256，监工 579 验收用过同口径），所有 worker 收尾后再算一次；
   不一致 ⇒ 整批结果标记 invalid、exit 非 0（579 根隔离本应保证零副作用，这道是抓回归）。
   跑批结束后用 `git status --short Examples/ evidence/ atoms/` 断言无新增改动
   （EV-CONC-001.md 的历史行尾假脏位是已知例外，核对它 diff 为 0 行即可）。
3. 新增的并行/自检测试不许按卡裁剪 diff（548 红线：跨卡规则会漏判）。

---

## 任务 4：加速比实测（喂料门 ≥2.5×，达不到就如实报、绝不向判决让步）—— 记录进 worklog

1. 同一台机器、同一卡集（全量 83 卡/7 算子），分别实测 `--jobs 1` 与 `--jobs 4` 的墙钟
   （report 顶层 elapsed_s；copytree 与进程启动开销必须计入 jobs4 数字，不许只算纯计算段）。
2. 喂料门：**加速比 ≥ 2.5× 且判决逐变体一致**，才算并行达标；jobs 可再试 2/4/8 给一条
   小对照（32 核但编译内存/IO 重，预期甜点在 4 左右，以实测为准）。
3. **若达不到 2.5×**：不许改判决/不许删跨卡全库扫描来凑速度；如实报告实测加速比与瓶颈
   （是 copytree 13.4MB×N 拖垮、还是真编译段、还是 Python 扫描段），保留 `--jobs` 能力但
   在 worklog 写明"未达喂料门、暂不建议作为默认"，交监工裁决。回退路径永远是 `--jobs 1`。
4. 跑批期间真实 build/.ccache 可被共享使用；确认真实 build/.replay_lock 不被 jobs4 触碰
   （应落在各 worker tmp）。

---

## 5. 收工门禁（fresh，串行跑；poison/replay 不可与 mutation 全量并发，会抢真实锁）

按顺序、用退出码定论（`-m slow` 汇总行常被管道吞，看不到 failed 不等于绿）：
1. `python tools/tool_integrity.py --check`（**脚本方式**，`-m` 方式会 ModuleNotFoundError utf8_console）exit 0。
2. `python -m tools.gate_engine --check`：规则/命中数与开工基线一致（block=0；warn 数记录在案）。
3. `python -m tools.poison_drill`：118/118、攻击面分类与开工一致、零覆盖攻击面无。
4. `python -m tools.atom_evidence_replay --check`：confirm=56 / refute=0 / infra_error=0。
5. `python -m pytest -m "not slow" -n auto -q` exit 0；`python -m pytest -m slow -n0 -q` 除已知
   预期红 test_golden_lock_json（golden warn 136→186 待人审 accept，**苦力不得自行 accept**）外全绿。
6. ruff 改动文件 All checks passed。
7. 受控目录 `git diff --quiet -- atoms/ evidence/ Examples/`（EV-CONC-001 行尾假脏位除外）；
   data/mutation/ 大 JSON 不入 git（沿用 .gitignore 现状）。
8. 串行权威数字不变：989（严格 619）/ 9 / 185，逐算子 M1..M7 与第 0 步一致。
9. 一任务一 commit（建议：任务1锁分片 / 任务2进程池 / 任务3一致性+冻结 / 任务4仅记录无 commit）；
   每个 CORE_TOOLS commit 同笔带重钉。**不 push、不 golden accept、不自动给命题填锚。**

## 6. 明确不做（交监工/下一批，别顺手做）
- replay / golden 的 `--jobs` 并行 CLI（本批只铺锁分片原语，下批复用）。
- 560 B3 受影响测试选择、B4 gate 索引化、B5 task_queue 并行调度（各自独立批）。
- M6 剩余 8 条逃逸收口、N4 poison covered 行为级覆盖、N5 豁免签名、PoC#3 校验和自签认证
  —— 均为既有挂账，**不在本批**，不许夹带。
- 任何 LLM 语义闸 / Supervisor / 自动 KG / 在线改权重：永久冻结，等模型。

## 7. 交付物
- 代码与测试（上述 commit）；data/mutation/_580_serial.json、_580_parallel_j4.json（证据）。
- `_worklog_580.md`：第 0 步基线（含行号/核数/串行 elapsed）、逐任务改了什么、
  **偏差表（提示词假设 X / 实测 Y，逐条）**、加速比实测表、收工门禁逐项结果、复跑命令、
  交人清单。汇报里给：jobs1 vs jobs4 逐变体是否一致、实测加速比、真实根零副作用证据、
  各门禁退出码、commit 链。
