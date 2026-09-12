---
id: EV-CONC-006
domain: conc
type: detection
kind: asm
status: draft
dal: A
verdict: confirm
expected_sanitizer: [thread]   # replay 工具链只跑 ASan/UBSan，不跑 TSan；此处声明 TSaN 演示性报错类型（惰性，仅供人审/未来扩展），真实验证见 drill_note 手动 WSL 复算
hypothesis: >-
  TSan 能检测本夹具的 data race（bench_race 两线程无同步并发写 g_shared），且对无竞争版本
  （bench_safe，std::atomic）零误报；但 TSan 有漏报边界，"没被报"≠"没有数据竞争"。
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
  1. 同一份夹具在 -fsanitize=thread（setarch -R）下 race 版本不报 data race —— 说明"竞争"不构成可检 data race；
  2. 同条件下 safe 版本（std::atomic）竟被 TSan 误报 data race —— 检测逻辑自相矛盾；
  3. 任一 run_match_key 与留痕 .out 不符 → 运行时场景未真实执行。
expected: |
  contains_in 三条全中（三种场景均编译进工件）；
  run_match 四个方向量 key 与留痕 .out 逐字一致；
  WSL setarch -R -fsanitize=thread 跑 bench_race 报 "WARNING: ThreadSanitizer: data race"、bench_safe 零报告（已实测，见 drill_note）。
sources:
  - {kind: cppreference, ref: "ThreadSanitizer (TSan)：编译期插桩 + 运行期 happens-before 边追踪，检测数据竞争", independent: true}
  - {kind: iso, ref: "ISO/IEC 14882:2023 [intro.race]（data race ⇒ UB；TSan 检测的是该 UB 的运行时表现）", independent: true}
first_hand: true
superiority: >-
  多数"TSan 教程"只演示"它能报"，不谈它"报不了"什么。本卡用同一份夹具同时给出"报"（race 版）
  与"不报"（safe 版）两种结果，并明确列出漏报边界，把"没被 TSan 报 ≠ 没有数据竞争"这个与
  LEAK-001/002 同族的关键结论落到可复算证据上，而非口号。
depth:
  layer: runtime
  drill_note: >-
    ## 手动 WSL 复算（replay 工具链不跑 TSan，故留痕于此供人审）

    命令（WSL g++-13.3.0，必须 setarch -R 前缀——否则裸跑报
    "FATAL: ThreadSanitizer: unexpected memory mapping"）：

        setarch -R g++ -std=c++23 -O1 -g -pthread -fsanitize=thread Examples/atoms/_atom_data_race.cpp -o /tmp/dr_tsan
        setarch -R /tmp/dr_tsan

    ### 有竞争版本（bench_race）实测输出（节选）：

        ==================
        WARNING: ThreadSanitizer: data race (pid=34)
          Read of size 4 at 0x555555559020 by thread T2:
            #0 operator() Examples/atoms/_atom_data_race.cpp:42
          Previous write of size 4 at 0x555555559020 by thread T1:
            #0 operator() Examples/atoms/_atom_data_race.cpp:38
          As if synchronized via sleep:
            #2 operator() Examples/atoms/_atom_data_race.cpp:41
          Location is global 'g_shared' of size 4 at 0x555555559020
        SUMMARY: ThreadSanitizer: data race Examples/atoms/_atom_data_race.cpp:42 in operator()
        ==================
        ...（程序 stdout 四行确定性计数）...
        ThreadSanitizer: reported 1 warnings

    精确指向 `g_shared`（全局非原子）的并发读写，行 38（写）/ 42（读）—即 bench_race 的竞争点；
    `As if synchronized via sleep` 印证了 bench_race 中线程 b 起手 1ms 延迟拉宽的并发窗口。

    ### 无竞争版本（bench_safe，std::atomic）同命令跑：零 race 告警（仅 "reported 1 warnings" 来自 race 版，
    safe 版本身无报告），证明 TSan 对"已同步"路径不误报。

    ### 边界（漏报场景，"没被报 ≠ 没有"）：
    1. **插桩盲区**：TSan 只能分析它被插桩的翻译单元与运行时；第三方库/内联汇编/系统调用内部的竞争不可见。
    2. **必须全量插桩**：只要有一个 TU 未用 -fsanitize=thread 编译混链，该 TU 内的竞争即漏报。
    3. **时序偶发**：某次运行两线程恰好错开也可能不触发；一次"没报"不是"没有"的证明（与 LEAK 同族）。
    4. **开销**：TSan 运行期约慢 10–20×、内存涨 5–10×，不适合常驻生产。
pedagogy:
  motivation: 程序没崩、TSan 也没叫，是不是就没问题了？
  level: intermediate
---

# EV-CONC-006 · CONC-003 检测卡：TSan 可检测数据竞争，但有边界

## §0 选题

CONC-003 的第二句是「TSan 可检测数据竞争，但有边界」。本卡承上：用同一份夹具给出 TSan 的
**报（race 版）/ 不报（safe 版）** 两种结果，并诚实列出漏报边界——这是与 LEAK-001/002 同族的
「工具沉默 ≠ 安全」结论。

## §1 检测设计

- `bench_race`：两线程无同步并发写 `g_shared` → TSan 应报 `WARNING: ThreadSanitizer: data race`。
- `bench_safe`：同语义 `std::atomic` → happens-before 成立 → TSan 不报（零误报）。
- 线程 b 起手 `sleep_for(1ms)` 拉宽并发窗口，确保竞争被稳定观测（避免"偶发错开"导致假阴性）。
  该 sleep **不建立 happens-before**，只是检测窗口杂质；两版本唯一语义差异是「无原子同步」vs「有 `std::atomic` 同步」。

## §2 机器可验部分（replay 口径）

与 EV-CONC-005 同源：`command` 只做可移植的 `-O2` 编译+运行+`.asm` 生成（**不含 TSan**，否则 Windows/MinGW
无法链接 `-ltsan` 而 refute）。`artifact_assert` 锚三场景符号，`run_match` 锚四个确定性方向量——这部分在
MinGW 与 WSL 双平台均 confirm。

TSan 检测本身走 **drill_note 手动 WSL 复算**（replay 的 sanitizer 步硬编码 `-fsanitize=address,undefined`，
从不在 replay 中运行 TSan），真实输出已引号留痕，人审可直接对照。

## §3 关键边界（漏报场景）

1. **插桩盲区**：TSan 仅分析被插桩的 TU 与运行时；第三方库/内联汇编/系统调用内的竞争不可见。
2. **必须全量插桩**：任一 TU 未用 `-fsanitize=thread` 编译而混链，其内竞争即漏报。
3. **时序偶发**：单次运行两线程恰好错开也可能不触发——一次"没报"不是"没有"的证明。
4. **开销**：运行期约慢 10–20×、内存涨 5–10×，不适合常驻生产。

> 核心教训：**没被 TSan 报 ≠ 没有数据竞争**（同族：没被 LSan 报 ≠ 没有泄漏）。

## §4 修订记录

- v1（本稿）：依 343 线 B-2 设计，三场景对照 + TSan 手动复算留痕 + 漏报边界。
