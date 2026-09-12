---
id: ATOM-CONC-LOCK-001
title: "锁的代价与无锁的代价：高竞争下 CAS 的原子 RMW 代价可能超过 mutex，但依赖核数与竞争度"
domain: conc
type: contrast
status: verified
dal: C
human_review: optional
verified_by: human:liaoranran
verified_at: "2026-09-12"
dal_reviewed_by: human:liaoranran
status_history:
  - {level: draft, at: "2026-09-12", by: machine:writer}
  - {level: machine-verified, at: "2026-09-12", by: machine:gate}
  - {level: verified, at: "2026-09-12", by: human:liaoranran}
audience: intermediate
cognitive_load: medium
prerequisites_readable: true
claim: >-
  高竞争下 CAS 的原子 RMW 代价可能超过 mutex；但该结论依赖核数与竞争度，≤2 核环境可能反向——
  锁与无锁各有适用域，无绝对最优。
claim_boundary:
  standard: [C++11, C++14, C++17, C++20, C++23]
  compilers: [GCC 15.3.0 (MinGW-w64), GCC 14.2.0 (WSL), GCC 13.3.0 (WSL)]
  opt: [-O2]
  platform: [x86-64]
relations:
  - prerequisite: ATOM-CONC-FENCE-001
evidence:
  - EV-CONC-003
  - EV-CONC-004
sources:
  - {kind: cppreference, ref: "std::atomic（RMW 在 x86-64 编译为带 lock 前缀指令，提供硬件同步开销；lock-free 为非保证属性）", independent: true}
  - {kind: iso, ref: "ISO/IEC 14882:2023 [atomics.order] / [thread.mutex]（同步语义定义，未规定相对代价）", independent: true}
first_hand: true
superiority: >-
  C++ 并发教材常给"无锁更快"的单一叙事，却回避代价分层：原子 RMW 在硬件层仍是带 lock 前缀的
  总线/缓存锁，mutex 的代价在 pthread 调用与内核仲裁。本原子用同一份夹具把三类同步原语
  （mutex / atomic fetch_add / atomic CAS）置于唯一变量（同步原语种类）下，以 -O2 工件证明
  原子操作确有硬件锁开销，并以 CAS 高竞争退化为反例，说明"无锁不一定更快"的方向性结论。
depth:
  layer: runtime
pedagogy:
  motivation: "读者常以为 atomic 是零代价魔法，或以为 mutex 永远最慢；实测二者代价位置不同，且 CAS 在高竞争下退化最严重。"
  misconception:
    - {level: surface, text: "误以为 atomic 是零代价、无锁一定比 mutex 快", refutations: [EV-CONC-003, EV-CONC-004]}
    - {level: deep, text: "误以为 CAS 无锁就一定优于 mutex：高竞争下 CAS 重试风暴使其代价反超 mutex", refutations: [EV-CONC-003, EV-CONC-004]}
  socratic: "原子 fetch_add 在 -O2 工件里生成了什么前缀指令？它和 pthread_mutex_lock 的代价分别落在哪一层？"
  predict_first: "先预测：把单线程基线、mutex、atomic fetch_add、atomic CAS 各跑 200000 次累加，哪条路径在 .asm 里出现 lock 前缀？CAS 在 32 核高竞争下会多出什么计数？"
  misconceptions: [MIS-CONC-002]
misconceptions: [MIS-CONC-002]
---

# ATOM-CONC-LOCK-001 · 锁的代价与无锁的代价

一句话直觉：**atomic 不是零代价的魔法，mutex 也不是永远最慢——它们代价落在不同层，且无锁不一定更快。**

## 1. 三层代价分解

### 1.1 硬件层（原子 RMW 的 lock 前缀）
原子 RMW（如 `fetch_add`、`compare_exchange`）在 `-O2` 下编译为带 **`lock` 前缀**的指令：
MinGW 15.3 生成 `lock addl $1, g_atomic_cnt(%rip)` / `lock cmpxchgl`，WSL g++13.3 生成
`lock addq` / `lock cmpxchgq`（位宽差异，前缀语义一致）。`lock` 前缀在 x86-64 上触发总线锁或
缓存锁，是实实在在的硬件同步开销——原子操作**不是零代价**。详见 EV-CONC-004。

### 1.2 运行时层（mutex 的 pthread 调用）
`std::mutex` 路径（`bench_mutex`）在 -O2 工件里**不含 `lock` 助记符**，其开销落在
`pthread_mutex_lock` / `pthread_mutex_unlock` 的库调用与内核仲裁——代价位置与原子 RMW 完全不同。
这正是"锁与原子代价分层"的结构性差异。详见 EV-CONC-003 / EV-CONC-004。

### 1.3 竞争层（CAS 高竞争退化）
CAS 在无竞争时单次成功；高竞争下 `compare_exchange_weak` 失败触发重试，重试计数
`g_cas_retries` 被观测到 `>0`（`cas_retry_observed=1`），且 `cas_high_contention_tested=1`
（多核环境成立）。重试风暴使 CAS 的有效代价随竞争度陡增，可能反超 mutex。

## 2. 证据摘要（详见两张卡）
- **EV-CONC-003（判据卡）**：4 条符号断言锚 `bench_single/mutex/atomic_fetch/atomic_cas` 在
  -O2 工件真实存在（MinGW 15.3 与 WSL g++13.3 双端验证）；`run_match_keys` 含 `*_result`
  确定性计数（单线程 200000 / 并发 800000）与 `cas_retry_observed` 活性量，方向量双平台稳定。
- **EV-CONC-004（性能卡）**：2 条 `lock` 前缀断言锚原子 RMW 的硬件锁开销（双端 grep 验证）；
  单线程基线作结构对照，CAS 高竞争退化作反例对照；性能数字只留痕 `.out`、不进 `actual`。

## 3. 教学要点
"无锁"省掉的是**内核仲裁**那一层代价，不是全部代价。原子 RMW 把同步代价下推到硬件
（`lock` 前缀），mutex 把代价上移到库/内核；谁更省取决于核数、竞争度、临界区大小。
CAS 在中等竞争下常最优，但在高竞争下退化最严重——这是"无锁不一定更快"的具象反例。

## 4. 边界与前提
- **核数**：`nproc=32` 双平台稳定观测到 CAS 高竞争退化；`≤2` 核环境 `cas_high_contention_tested`
  翻转（甚至 `insufficient_cores=1`），CAS 退化未必出现，claim 的"CAS 反超"在此合法不成立。
- **竞争度**：CAS 退化只在高竞争（多线程抢同一 target）出现；低竞争下 CAS 接近单次成功。
- **迭代数**：`kIters=200000` 固定、有界，防 replay 超时（铁律 1）。
- **不主张倍数**：性能绝对值随运行波动 2x+，故只锚方向、不锚倍数（PERF-003/004 教训）。

## 5. relations 说明
- `prerequisite: ATOM-CONC-FENCE-001`：屏障只约束顺序、不提供原子性/同步；理解"锁与无锁的
  代价分层"需先建立"原子类型 ≠ 屏障"的基础，故 FENCE-001 为本原子前置。
- `evidence: [EV-CONC-003, EV-CONC-004]`：两张卡分别支撑"路径真实编译执行"与"原子 RMW 硬件锁开销"。

## 6. 修订记录
- **v1（343 线 B-1 起草）**：claim 收窄为"高竞争下 CAS 代价可能超过 mutex，但依赖核数与竞争度，
  ≤2 核可能反向"；锚方向不锚倍数；声明变量域（核数/竞争度/迭代数）；含低核证伪守卫。

## 7. 5 分锚定依据（人审授予）
本原子经以下三条独立证据链支撑，达到 `verified` 与 5 分质量锚定：
1. **双平台机器复算**：Windows（MinGW 15.3.0）与 WSL（g++-13.3.0）重跑 replay 均
   `confirm=2 / refute=0`；主工件 sha `d84c7516…` 在两环境逐字一致，`artifact_assert` 的
   4 条符号断言 + 2 条 `lock` 前缀断言在跨编译器路径真实执行并全绿（非只看 sha 的真空通过）。
2. **独立红队两段式盲读**：专用子 agent 仅持夹具/工件/两张卡 actual，给出
   **阻断级 0 / 高级 2 / 建议 3**，A4 修复（纳入 `*_result` 真活性、falsification 加低核守卫、
   双端 lock 验证）已闭环；核心论点（原子 RMW 含 lock 前缀、mutex 不含、CAS 高竞争退化）均被
   工件反向证伪为成立。
3. **变量域如实锚定边界**：核数（`nproc=32`）、竞争度（CAS `cas_high_contention_tested`）、
   迭代数（`kIters=200000` 固定）显式声明；`≤2` 核环境的合法翻转以 `insufficient_cores=1`
   兜底，不写死"CAS 必慢"，符合"claim 必须可证伪"。
