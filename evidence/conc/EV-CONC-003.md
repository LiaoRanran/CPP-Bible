---
id: EV-CONC-003
domain: conc
type: criterion
status: draft
dal: A
verdict: confirm
kind: asm
hypothesis: >-
  四种同步路径（单线程基线 / mutex / atomic fetch_add / atomic CAS）在 -O2 下均被真实编译并执行；
  CAS 在高竞争下可观测到重试（反例对照），且核不足时实验合法翻转。
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
  - 活性对照: 单线程无同步基线（bench_single）
  - 反例对照: CAS 在高竞争下退化（cas_retry_observed + cas_high_contention_tested）
matrix:
  compiler: [GCC 15.3.0 (MinGW-w64), GCC 13.3.0 (WSL)]
  stdlib: [pthread]
  std: [c++23]
  opt: [-O2]
  arch: [x86-64]
actual:
  run_match_file: Examples/atoms/_atom_lock_cost.out
  run_match_keys:
    - single_thread_baseline
    - mutex_fastpath_exists
    - atomic_rmw_exists
    - cas_retry_observed
    - single_result
    - mutex_result
    - atomic_result
    - cas_result
artifact_assert:
  - {kind: contains, text: "_Z12bench_singlev"}
  - {kind: contains, text: "_Z11bench_mutexv"}
  - {kind: contains, text: "_Z18bench_atomic_fetchv"}
  - {kind: contains, text: "_Z16bench_atomic_casv"}
falsification: |
  若以下任一发生，判 refute：
  1. 任一 bench_* 函数符号在 -O2 工件中消失（被内联/消除）→ 实验路径未真实编译进工件；
  2. 仅当 `cas_high_contention_tested=1`（多核，高竞争实验成立）时，`cas_retry_observed=0` 才 refute
     （说明 CAS 无竞争重试，反例对照失效）；低核环境下 `insufficient_cores=1` 合法翻转，不 refute；
  3. 核数兜底翻转时 insufficient_cores=1 但未在卡内声明（低核环境实验不可成立）；
  4. 任一 `*_result` 计数与 `kIters×kThreads`（或单线程 `kIters`）不符 → 运行时未真正执行累加。
expected: |
  contains_in 四条全中（四种同步路径均编译进工件）；
  run_match 五个方向量 key 与留痕 .out 逐字一致（**nproc 为环境量、跨机必异，不进 keys**；其余恒为 1）；
  cas_retry_observed=1（多线程竞争下 CAS 重试被观测）。
---

# EV-CONC-003 · CONC-002 判据卡：四种同步路径的结构存在性与执行活性

## §0 选题：为什么这个实验能支撑 claim

CONC-002 的 claim 方向是「锁与原子操作的代价分层，且**无锁不一定更快**」。代价本身是性能量（不进
`actual`，见 EV-CONC-004），但「实验确实覆盖了四种同步路径且每条都被真实编译与执行」是代价结论的
**前提活性**。本卡只锚这个前提：四种路径都在工件中存在、运行时都真的跑了。

## §1 夹具设计

`_atom_lock_cost.cpp` 用唯一变量=同步原语种类，配两组对照：
- **活性对照**：`bench_single`（单线程无同步基线）；
- **反例对照**：`bench_atomic_cas` 在高竞争下用 `compare_exchange_weak` 失败分支 `fetch_add` 计数重试。

`-DBENCH_FULL` 仅用于 `.out` 性能样本生成（见 EV-CONC-004），`actual` 只锚方向量与常量。

## §2 工件与断言

4 条 `contains_in`（scope: file）锚四种 bench 函数定义符号，MinGW 15.3 与 WSL g++13.3 工件**均验证存在**：

| 断言 | 符号 | MinGW | WSL |
|---|---|---|---|
| 单线程基线 | `_Z12bench_singlev` | √ | √ |
| mutex 路径 | `_Z11bench_mutexv` | √ | √ |
| 原子 RMW 路径 | `_Z18bench_atomic_fetchv` | √ | √ |
| CAS 路径 | `_Z16bench_atomic_casv` | √ | √ |

## §3 量化读数（run_match_keys，实测）

| 方向量 | MinGW 15.3 | WSL g++13.3 |
|---|---|---|
| `nproc`（环境量，**不参与逐字比对**） | 32 | 32 |
| `single_thread_baseline` | 1 | 1 |
| `mutex_fastpath_exists` | 1 | 1 |
| `atomic_rmw_exists` | 1 | 1 |
| `cas_retry_observed` | 1 | 1 |

计数确定：`single_result=200000`（单线程 `kIters`）；`*_result=800000`（`kThreads×kIters`）。

## §4 反例与边界

- **CAS 高竞争退化**：`cas_retry_observed=1` 证明多线程竞争下 CAS 重试被观测（反例对照成立）。
- **核数兜底**：`nproc < kThreads(4)` 时输出 `insufficient_cores=1`（CAS 退化实验无法成立，合法翻转）；
  32 核机器输出 `cas_high_contention_tested=1`。该翻转**不进 `run_match_keys`**（避免跨机 refute）；
  **`nproc` 亦然**——它是环境量（CI runner 与开发机核数不同），同样不进 keys，仅在 `.out` 留痕，
  仅在正文诚实描述方向，符合「性能数据锚方向不锚倍数」。

## §5 修订记录

- v1（本稿）：依 327 线 B 设计，双构建宏门控 + 稳定方向量输出，4 符号断言双端验证。
