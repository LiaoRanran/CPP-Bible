---
id: EV-CONC-004
domain: conc
type: performance
status: draft
dal: A
verdict: confirm
kind: asm
hypothesis: >-
  原子 RMW（fetch_add / CAS）在 -O2 下编译为带 lock 前缀硬件指令，证明确有硬件同步开销，
  与 mutex（pthread 调用）形成代价对照；CAS 高竞争退化方向在 .out 性能数据可观测。
fixture: Examples/atoms/_atom_lock_cost.cpp
command: |
  g++ -O2 -std=c++23 -pthread -DBENCH_FULL Examples/atoms/_atom_lock_cost.cpp -o build/_replay_lock_cost.exe && ./build/_replay_lock_cost.exe
  g++ -O2 -std=c++23 -pthread -DBENCH_FULL -S Examples/atoms/_atom_lock_cost.cpp -o Examples/atoms/_atom_lock_cost.asm
artifact: Examples/atoms/_atom_lock_cost.asm
artifact_sha256: d84c75168df0fda9b032de38efae31f7f51c8cda7eeb187154c53eeba95698f8
artifact_compiler: GCC 15.3.0 (MinGW-w64)
serves: [ATOM-CONC-LOCK-001]
relations: []
evidence: []
controlled_vars:
  - 唯一变量: 同步原语种类（mutex / atomic fetch_add / atomic CAS）
  - 活性对照: 单线程无同步基线
  - 反例对照: CAS 在高竞争下退化
matrix:
  compiler: [GCC 15.3.0 (MinGW-w64), GCC 13.3.0 (WSL)]
  stdlib: [pthread]
  std: [c++23]
  opt: [-O2]
  arch: [x86-64]
actual:
  run_match_file: Examples/atoms/_atom_lock_cost.out
  run_match_keys:
    - mutex_fastpath_exists
    - atomic_rmw_exists
    - cas_retry_observed
    - single_result
    - mutex_result
    - atomic_result
    - cas_result
artifact_assert:
  - {kind: contains_in, symbol: "_Z18bench_atomic_fetchv", scope: file}
  - {kind: contains_in, symbol: "_Z16bench_atomic_casv", scope: file}
falsification: |
  若原子 RMW 函数体不含 lock 前缀指令（编译器将同步语义优化掉）→ 判 refute：
  1. bench_atomic_fetch 体内无 `lock addl`；
  2. bench_atomic_cas 体内无 `lock cmpxchgl`。
expected: |
  bench_atomic_fetch 含 `lock addl`（fetch_add 编译为带 lock 前缀的 RMW）；
  bench_atomic_cas 含 `lock cmpxchgl`（CAS 编译为带 lock 前缀的 cmpxchg）；
  证明原子操作存在硬件锁开销，与 mutex（pthread 调用）形成代价对照。
---

# EV-CONC-004 · CONC-002 性能卡：原子 RMW 的硬件锁开销结构

## §0 选题：为什么这个实验能支撑 claim

CONC-002 的 claim 核心是「锁/原子操作的代价分层，且无锁不一定更快」。代价本身是性能量，**不进
`actual`**（锚方向不锚倍数）。但「原子操作确有硬件同步开销」是代价结论的结构性前提——本卡锚这个
前提：原子 RMW 在 -O2 下编译为带 `lock` 前缀的指令（硬件级总线锁/缓存锁），而非零成本。

## §1 夹具设计

同 EV-CONC-003：唯一变量=同步原语种类。`-DBENCH_FULL` 仅用于 `.out` 性能样本生成。

## §2 工件与断言

2 条 `contains_in`（scope: function）锚原子 RMW 的 `lock` 前缀，MinGW 15.3 工件已验证：

| 实测项 | 函数体 | MinGW 15.3 工件 | WSL g++13.3 工件 |
|---|---|---|---|
| 原子 fetch_add 函数体含 `lock` 前缀 | `_Z18bench_atomic_fetchv` | `lock addl $1, g_atomic_cnt(%rip)` | `lock addl $1, g_atomic_cnt(%rip)` |
| 原子 CAS 函数体含 `lock` 前缀 | `_Z16bench_atomic_casv` | `lock cmpxchgl %ecx, g_cas_target(%rip)` | `lock cmpxchgl %ecx, g_cas_target(%rip)` |

对照：mutex 路径（`_Z11bench_mutexv`）函数体**不含 `lock` 助记符**（其锁开销在 pthread 内部
`pthread_mutex_lock/unlock` 调用处），工件层面看不到 `lock` 前缀指令——这正是「锁与原子 RMW
代价位置不同」的结构性差异。

> **证据形态说明**：`replay` 的 `contains_in` 仅支持**符号名**锚定（匹配 `.globl` 函数符号），
> 不直接匹配助记符子串，故本卡 `artifact_assert` 锚上述两个原子 RMW 函数符号（证明路径真实编译、
> 与 EV-CONC-003 同源验证）；而「`lock` 前缀硬件锁开销」以**双端工件 grep 实证**留痕——
> `lock addl/cmpxchgl` 在 MinGW 15.3 与 WSL g++13.3 的 `bench_atomic_fetch`/`bench_atomic_cas`
> 函数体内均实测存在（已 grep 验证），满足 327「断言候选必须在 Linux 工件验证」要求，但不进机器断言。

## §3 性能方向（锚方向不锚倍数）

`.out` 含 `-DBENCH_FULL` 性能样本（如 `atomic_fetch_ns≈649500`，同机双平台各一轮）。
**性能数字只留痕、不进 `actual`、不进 `run_match_keys`**——跨运行波动 2x+ 属正常（PERF-003 教训）。
另：`nproc` 属同类环境量（CI runner 与开发机核数不同），同样不进 keys。

- 方向结论（正文陈述，非自动断言）：共享/同步路径比单线程基线慢，且 CAS 在高竞争下退化最严重。
- **诚实披露**：当前 `.out` 为单轮样本；327 要求的「完整 7 轮逐样本 + min/max + 比值」扩样待增强
  夹具（增 7 轮循环输出）后补，`run_match_keys` 仍只锚方向量，性能倍数不锚。

## §4 反例与边界

- **CAS 高竞争退化**：`cas_retry_observed=1`（多线程竞争重试被观测）；退化方向在 `.out` 性能数据，
  低核环境 `nproc<4` 时合法翻转为 `insufficient_cores=1`（见 EV-CONC-003 §4）。
- **代价位置差异**：mutex 代价在 pthread 调用（函数体无 `lock`），原子 RMW 代价在 `lock` 前缀
  指令（函数体内）——两者都「有代价」，但代价层级不同，支撑「无锁不一定更快」。

## §5 修订记录

- v1（本稿）：依 327 线 B 设计，锚原子 RMW 的 `lock` 前缀硬件开销；性能样本单轮，7 轮扩样待补。
