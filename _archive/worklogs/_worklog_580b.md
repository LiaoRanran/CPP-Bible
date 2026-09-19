# _worklog_580b · 卡间确定性并行（在 579 根隔离之上提速 mutation）

> 任务书：`References/architecture_架构演进/580_苦力_卡间确定性并行_mutation提速_根隔离之上.md`
> 承接 579（`fdb210a`/`296fb6e`/`2cc5a5a`）· 提交：`f574b76`（任务1）、`cc4974d`（任务2+3）
> 铁律：判决逻辑一字未改；新能力默认 OFF（`--jobs 1` = 今天的串行路径）；不 push、不 golden accept。
> （注：`_worklog_580.md` 在本环境被写成 0 字节两次，故落为 `_worklog_580b.md`。两份同内容等价。）

## 第 0 步 · 开工基线（先量后动）

| 项 | 实测 |
|---|---|
| HEAD | `2cc5a5a`（含 579 三笔）✓ |
| `os.cpu_count()` | **32** ⇒ `--jobs auto` = min(4, 31, 卡数) = **4** |
| 串行全量墙钟（改前，`data/mutation/_580_serial.json`） | **`elapsed_s = 667.56`**（83 卡 / 7 算子 / **1183 变体**） |
| 三总数 | `blocked 989（严格 619）· escaped 9 · n_a 185`（malformed 0 / out_of_scope 69） |
| 逐算子 (b/e/n_a) | M1 64/1/27｜M2 168/0/27｜M3 65/0/42｜M4 200/0/33｜M5 29/0/56｜M6 324/8/0｜M7 139/0/0 —— 与任务书逐字一致 |
| STATS（改前口径） | `ge_runs 999 · replay_runs 65 · replay_skipped 139` |
| 行号（符号名定位） | replay：`_REPLAY_LOCK=939`、引用 `959/963/974/981/996/1005`、`CCACHE_DIR=847`（保持真实 ROOT）、`_release_replay_lock=1044`/`_install_lock_cleanup=1094`（只调 `_try_unlink_lock`，无需改）；mutation：`sandbox=64`、`_rel_in_sandbox=92`、`_snapshot=106`、`STATS=112`、`classify=474`、`run_fuzz=589`、`_variant_index=749`、`main=773` |

> 诚实标注：第 0 步那次串行跑与若干测试并发，`667.56s` 可能受影响（579 同口径实测 790s）。
> 任务 4 的加速比因此用**同批、干净时序**的 jobs1 vs jobs4 两个数。

## 任务 1 · replay 并发锁跟随跑批根分片（`f574b76`）

* 模块常量 → 路径函数 `_replay_lock_path() = run_root()/"build"/".replay_lock"`；
  `_acquire_replay_lock`（循环前取一次 `lock`）、`_try_unlink_lock`、`_read_lock_pid` 三处引用改掉。
  **锁语义一字未动**（O_CREAT|O_EXCL、pid 存活接管、mtime 陈旧接管、等待/超时分离）。
* `CCACHE_DIR` 保持真实 ROOT（ccache 自带并发安全，多 worker 共享更快）。
* 连带（不改就红）：`poison_drill.py` P45/P46 载荷 patch 该路径 ⇒ 改函数替身；
  `tests/test_p0g_lock.py`（fixture + 子进程脚本）、`tests/test_replay_lock_serial.py` 三处替身同步改法（**断言未改**）。
* 新增 `tests/test_replay_lock_shard_580.py`（4 例）：默认路径**逐字节**不变 / 跟随 `batch_root` /
  同根仍互斥 / **异根不互斥**（旧代码必超时 —— 并行的成立证据）。
* 验收：`replay --check` `confirm=56 refute=0 infra_error=0` ✓ · poison `118/118`（零覆盖攻击面：无）✓ ·
  `tool_integrity --check` exit 0 ✓（CORE_TOOLS 同 commit 重钉）。

## 任务 2 · mutation 卡间进程并行（`--jobs`，默认 1 = 串行）（`cc4974d`）

* **抽取单一真源**：`_card_variants(card, ops, baseline, tmp)`（`run_fuzz` 逐卡主体**原样**抽出，卡内串行 +
  卡末 `finally` 还原不变）与 `_report(...)`（报告尾部）。串行与 worker **共用同一份** ⇒ 并行不改判决由构造保证。
  `run_fuzz(cards, ops, limit, progress)` **签名/行为不变**（内部 `per.extend(_card_variants(...))` + `return _report(...)`）。
* 并行：`ProcessPoolExecutor(initializer=_worker_init, initargs=(ops,))`；
  `_worker_init` 建 `mutworker_*` 根（atoms/evidence/**Examples** + 空 build + `batch_root` + 各自 baseline，进程内复用）；
  `_worker_card(card_str)` ⇒ `(卡rel, per, STATS 增量, pid)`；主进程按 `selected` 顺序**重排**后 `_report`。
  worker `atexit` → `_worker_cleanup()`（还原 batch_root、ge.ATOMS/EVIDENCE、删自己 tmp）。
* `--jobs`：默认 `"1"`；`auto` = min(4, cpu_count-1, 卡数)；非法值回落 1（绝不静默变并行）。
  报告**只加**字段 `jobs`/`parallel`（串行也给：1/False）；并行另加 `parallel_baseline_scans`。
* 异常 fail-loud：任一卡任务抛错 ⇒ `SystemExit` 并打印**哪张卡**（丢卡会改分母）。

## 任务 3 · 判决一致性硬门 + 真实根输入冻结（同 `cc4974d`）

1. `--selfcheck-determinism` 扩展：`jobs>1` 时除同 jobs 复跑外，**再用 jobs=1 跑同一子集**逐变体比对 ⇒ 分歧列清单 + exit 2。
2. `_real_root_fingerprint()`（Examples+atoms+evidence 全树：排序后 路径+内容 sha256）在进程池启动前/收齐后各算一次；
   不一致 ⇒ `rep["invalid"]` + `root_fingerprint_ok=False` + CLI exit 2。
3. 新增测试不按卡裁剪 diff（全量 `new - baseline`，548 红线未碰）。

## 任务 4 · 加速比实测（同机器、同卡集：83 卡/7 算子/1183 变体）

| 跑次 | 命令 | `elapsed_s` |
|---|---|---|
| 改前串行（第 0 步） | （无 `--jobs`） | **667.56** |
| 改后 jobs=1（`_580_jobs1.json`） | `--jobs 1` | **687.41** |
| 改后 jobs=4（`_580_parallel_j4.json`） | `--jobs 4` | **198.19** |

**加速比 `jobs1/jobs4 = 3.47×`（改前串行/jobs4 = 3.37×）⇒ 达标（喂料门 ≥2.5×）** ✓

* jobs4 已**含** copytree（4×13.4MB）与进程启动开销；4 worker 基本吻合 3.47× ⇒ 瓶颈仍在"每变体一次全库 `ge.run()`"。
* `auto` 在本机解析为 **4** ✓；2/8 对照未跑（预算），建议下一批补。
* 真实根副作用：`root_fingerprint_ok=True`、`parallel_baseline_scans=4`；真实 `build/.replay_lock` 全程未动。

### 4-1 · 判决一致性（比提速更重要）

| 对照 | 结果 |
|---|---|
| 改前串行 vs jobs1 | 10 项计数全等 · `by_operator`/`by_card` 相等 · `results` **1183/1183 逐条完全相等** |
| jobs1 vs jobs4 | 10 项计数全等 · **逐变体索引 1183 键 0 差异** · `results` **逐条完全相等** · `escaped_list` 相等 · `root_fingerprint_ok=True` |
| 改前串行 vs jobs4 | `results` **逐条完全相等** |

## 5 · 收工门禁（fresh，串行；退出码定论）

| # | 项 | 实测 |
|---|---|---|
| 1 | `tools/tool_integrity.py --check`（脚本方式） | `OK：5 个核心工具与基准一致` **exit 0** ✓ |
| 2 | `python -m tools.gate_engine --check` | `规则 63 条 · 命中 191 (block=0 warn=186 advice=5)` —— 与开工基线**逐字一致** ✓ |
| 3 | `python tools/poison_drill.py`（脚本方式） | `118/118 —— 制衡层有效` + `攻击面分类 {A1 19, A2 13, A3 21, …}` + `零覆盖攻击面：无` ✓ |
| 4 | `python -m tools.atom_evidence_replay --check` | `confirm=56 refute=0 infra_error=0 共 56 张卡` ✓ |
| 5 | `python -m pytest -m "not slow" -n auto -q` | **exit 0** ✓（首轮曾因 579 指纹用例在 `-n auto` 下假红一次，已用 `replay_serial` 修好，见 §6-7） |
| 6 | `python -m pytest -m slow -n0 -q` | exit 1，**唯一失败 = `test_json_output.py::test_golden_lock_json`**（golden warn 136→186 的存量债务，**待人审 accept，苦力未动**）✓ |
| 7 | ruff（`python -m ruff check tools/ tests/`；pyproject 已钉 `select`） | `All checks passed!` **exit 0** ✓（本批新增文件先有 5 条 I001/F401，已 `--fix`） |
| 8 | 受控目录 | `git diff --quiet -- atoms/ evidence/ Examples/` **exit 0** ✓（EV-CONC-001 行尾假脏位除外） |
| 9 | 真实 `build/.replay_lock` | **不存在**（jobs4 全程未触碰；锁都落在各 worker tmp）✓ |
| 10 | 串行权威数字 | `989（严格 619）/ 9 / 185` + 逐算子 M1..M7 与第 0 步**逐字一致**；jobs4 与之 `results` **逐条完全相等** ✓ |

## 6 · 偏差表（任务书假设 X / 实测 Y）

| # | 任务书假设 | 实测 | 处置 |
|---|---|---|---|
| 1 | 单进程约 11–16 分钟 | 第 0 步 **667.56s ≈ 11.1 min** ✓ 在区间内 | 无（分母在案；该次有并发负载 ⇒ 任务 4 另用同批 jobs1） |
| 2 | 门禁 5.3 写 `python -m tools.poison_drill` | `-m` 方式输出易被截断；脚本方式稳定 | 门禁脚本用**脚本方式**跑 poison；`-m` 用于 gate/replay |
| 3 | 三计数"总数与串行一致" | worker 各 materialize 一次基线 ⇒ 计入则 `ge_runs` 必多 (workers−1) | **口径收窄**：`ge_runs` 记**逻辑**扫描数（1 基线 + 每变体 1），真实基线次数另记 `parallel_baseline_scans` ⇒ `jobs1==jobs4` **完全相等**（实测） |
| 4 | "--jobs 1 必须走原串行代码" | 逐卡主体/报告尾部被**原样抽出**成共用函数（签名/行为不变） | 以"改前 vs jobs1 的 `results` 1183 条逐条相等"作等价证据 |
| 5 | 锁语义不许动 | 只把常量换成路径函数 | 旧锁测试 12 例断言未改全绿 |
| 6 | （新发现的连带面） | `poison_drill` P45/P46 + 两个锁测试文件共 4 处 patch 该常量 ⇒ 不改即 `AttributeError` 崩 | 一并改为函数替身，纳入任务 1 同 commit |
| 7 | （收工验收暴露） | 首轮 fast `-n auto` 里 `test_579_run_fuzz_leaves_real_repo_untouched` **红过一次**；串行 8/8 不复现 | 定位为本仓 559 已确立的同类假红：该用例比对**真实 Examples 全树指纹**，而别的 xdist worker 的合法 replay 正在删-建真实工件 ⇒ 给 4 例指纹类用例套 `conftest.replay_serial`（共用同一把锁串行；拿不到锁则带因 skip）；修后完整 fast **exit 0**。**不是**并行路径的判决问题（jobs4 与串行逐条相等已证） |

## 7 · 交人清单

1. **`--jobs` 仍默认 1**（任务书硬要求）。若要把并行设为默认，属架构决策 ⇒ 建议先让
   `--selfcheck-determinism` 进 CI 跑若干轮，再由监工裁决。
2. **未做**（任务书 §6）：replay/golden 的 `--jobs`（本批已备锁分片原语，下批可直接复用
   `batch_root()` + `_replay_lock_path()`）、560 B3/B4/B5、M6 剩 8 条逃逸、N4/N5、PoC#3。
3. 2/8 worker 对照未跑（预算）；`parallel_baseline_scans` 是新字段，下游若有 strict schema 需登记。
4. **环境异常记录（非本批引入，不影响仓库内文件）**：`_worklog_580.md` 与个别根级 `_*580*` 探针脚本
   在本环境出现"写入被截成 0 字节"现象（换名重写即正常），原因未定位（疑似写入拦截/杀软）。
   仓库内受控文件与产物**不受影响**（三份 report、所有代码与测试均在）。
