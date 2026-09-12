---
id: EV-CONC-005
domain: conc
type: criterion
kind: asm
status: draft
dal: A
verdict: confirm
hypothesis: >-
  本夹具构造了一个教科书式数据竞争：两个线程并发读写同一非原子全局变量 g_shared，全程零同步原语
  （无 mutex/atomic/barrier）。按 C++ 标准该形态即 data race，属未定义行为（UB）；三场景
  （单线程基线 / 有竞争 / 原子无竞争）均真实编译进工件且运行时都执行。
fixture: Examples/atoms/_atom_data_race.cpp
command: |
  g++ -O2 -std=c++23 -pthread -DBENCH_FULL Examples/atoms/_atom_data_race.cpp -o build/_replay_data_race.exe && ./build/_replay_data_race.exe
  g++ -O2 -std=c++23 -pthread -DBENCH_FULL -S Examples/atoms/_atom_data_race.cpp -o Examples/atoms/_atom_data_race.asm
artifact: Examples/atoms/_atom_data_race.asm
artifact_sha256: 5c5549aebfb148a053498f173aaa09757a92e180f54e956dc853c4761d2405bc
artifact_compiler: GCC 15.3.0 (MinGW-w64)
serves: [ATOM-CONC-RACE-001]
relations: []
evidence: []
controlled_vars:
  - 唯一变量: 是否存在数据竞争（有竞争 vs 无竞争对照）
  - 活性对照: 单线程无同步基线（bench_single）
  - 反例对照: 同语义改用 std::atomic（bench_safe）→ 无竞争
matrix:
  compiler: [GCC 15.3.0 (MinGW-w64), GCC 13.3.0 (WSL)]
  stdlib: [pthread]
  std: [c++23]
  opt: [-O2]
  arch: [x86-64]
actual:
  run_match_file: Examples/atoms/_atom_data_race.out
  run_match_keys:
    - single_total
    - race_ops_total
    - safe_ops_total
    - safe_final
artifact_assert:
  - {kind: contains, text: "_Z12bench_singlev"}
  - {kind: contains, text: "_Z10bench_racev"}
  - {kind: contains, text: "_Z10bench_safev"}
falsification: |
  若以下任一发生，判 refute：
  1. 任一 bench_* 函数符号在 -O2 工件中消失（被内联/消除）→ 实验路径未真实编译进工件；
  2. 任一 run_match_key 与留痕 .out 不符 → 运行时未真正执行对应场景；
  3. 同一份夹具在 -fsanitize=thread 下竟不报 data race（见 EV-CONC-006 的 WSL 实测）——若
     真出现，说明本夹具"竞争"不构成标准 data race，假阳性。
expected: |
  contains_in 三条全中（三种场景均编译进工件）；
  run_match 四个方向量 key 与留痕 .out 逐字一致；
  WSL g++13.3 与 MinGW 15.3 工件符号同名、.out 输出逐字一致（已双端实测）。
sources:
  - {kind: iso, ref: "ISO/IEC 14882:2023 [intro.race]（data race 的定义：不同线程对同对象无同步的并发冲突访问，且至少一个是写；其结果是未定义行为）", independent: true}
  - {kind: cppreference, ref: "Data race（无同步的并发冲突访问 ⇒ 未定义行为）", independent: true}
first_hand: true
superiority: >-
  教材常把"数据竞争"讲成"结果可能不对"，弱化其严重性。本卡用同一份夹具把"无同步并发写"与"同语义
  用 atomic 保护"并置，并以工件符号证明两种路径都真实编译，再以 EV-CONC-006 的 TSan 报告把
  "未定义行为"从信念变成可观测告警——证明这不仅是"答案偶尔错"，而是标准明文规定的 UB。
depth:
  layer: language-law
  drill_note: >-
    数据竞争是 UB，但其"有害性"不靠程序崩溃证明（x86-64 上 int 读写天然对齐，不会 SIGSEGV），
    而靠 TSan 静态/动态插桩对 happens-before 的边追踪证明。TSan 检测证据走手动 WSL 复算
    （replay 工具链只跑 ASan/UBSan，不跑 TSan），详见 EV-CONC-006 的 drill_note。
pedagogy:
  motivation: 两个线程同时改一个普通变量，到底算不算"bug"？
  level: intermediate
---

# EV-CONC-005 · CONC-003 判据卡：数据竞争是未定义行为

## §0 选题

CONC-003 的 claim 方向是「数据竞争是 C++ 未定义行为；TSan 可检测但有边界」。其中**「是 UB」是前提判据**，
本卡只锚这件事：夹具确实构造了一个标准定义的 data race，且它在工件与运行时都真实存在。

## §1 夹具设计

`Examples/atoms/_atom_data_race.cpp` 用唯一变量=是否存在数据竞争，配两组对照：

- **活性对照**：`bench_single`——单线程无同步基线，对局部变量累加，结果确定（`single_total=kIters`）；
- **有竞争**：`bench_race`——两线程并发 `g_shared += 1`，**零同步原语**（无 mutex、无 atomic、无 barrier）；
  `g_shared` 是非原子 `int`，两个线程既无 happens-before 也无同一原子对象的修改顺序 ⇒ 标准定义的 data race；
- **反例对照**：`bench_safe`——同一语义改用 `std::atomic<int>` 的 `fetch_add`，建立 happens-before ⇒ 无竞争。

`__attribute__((noinline))` 故意保留三个 `bench_*` 符号，防止 `-O2` 把负载内联进 `main` 而在工件中"消失"
（符号断言需稳定命中），不改变任何竞争语义。

## §2 工件与断言

3 条 `contains_in`（scope: file）锚三种场景的函数定义符号，MinGW 15.3 与 WSL g++13.3 工件**均验证存在**：

| 断言 | 符号 | MinGW | WSL |
|---|---|---|---|
| 单线程基线 | `_Z12bench_singlev` | √ | √ |
| 有竞争 | `_Z10bench_racev` | √ | √ |
| 无竞争 | `_Z10bench_safev` | √ | √ |

## §3 量化读数（run_match_keys，实测）

| 方向量 | MinGW 15.3 | WSL g++13.3 |
|---|---|---|
| `single_total` | 100000 | 100000 |
| `race_ops_total` | 200000 | 200000 |
| `safe_ops_total` | 200000 | 200000 |
| `safe_final` | 200000 | 200000 |

计数确定：`kIters=100000`，竞争版两线程各跑 `kIters` ⇒ `race_ops_total=2*kIters`；原子版同理且
`safe_final` 确定性等于 `2*kIters`（happens-before 保证）。双平台逐字一致（已实测）。

> **诚实边界**：机器可验部分（run_match 四方向量 + 三符号断言）只证明三场景均真实编译进工件、
> 且运行时都执行到 `join()` 完成；`bench_race`「无同步并发写」这一核心事实，由标准 [intro.race] 的 data race
> 定义 + EV-CONC-006 的 TSan 实测共同确立，**而非**由 stdout 的计数常量证明（那些只是「循环跑完」的见证）。
> `bench_race` 起手 `sleep_for(1ms)` 仅为拉宽 TSan 检测窗口，**不建立 happens-before**；两版本唯一语义差异是
> 「无原子同步」vs「有 `std::atomic` 同步」。

## §4 反例与边界

- **反例对照成立**：`bench_safe` 用 `std::atomic` 后 TSan 零报告（见 EV-CONC-006），证明"同一语义、加同步即无竞争"，
  反衬 `bench_race` 的"无同步"才是竞争根因，而非"多线程"本身。
- **不打印竞争终值**：`g_shared` 终值非确定（UB 的体现），故从不把它写进 `run_match_keys`——只锚确定性操作数，
  避免 replay 双平台因非确定值失配（"证明某事没发生"的观测通路用 TSan 承担，见 EV-CONC-006）。

## §5 修订记录

- v1（本稿）：依 343 线 B-2 设计，三场景对照 + 确定性输出 + noinline 保符号 + 双平台实测。
