---
id: EV-CONC-002
serves: [ATOM-CONC-001]
kind: asm
hypothesis: >-
  `atomic_signal_fence` 与 `atomic_thread_fence` 在**指令层**完全不同、在**位置层**同样敏感：
  `signal_fence` 是纯编译器屏障（实测自旋侧与写入侧两条路径**都是零机器指令**），
  `thread_fence` 才产生硬件屏障（x86-64 实测 `lock or … [rsp], 0`，riscv64 实测 `fence iorw,iorw`）；
  而且这条硬件屏障**锁在栈地址 `[rsp]` 上，不碰被保护的普通 `int`**——
  被保护的标志仍走普通 `mov` 访存 ⇒ **屏障≠原子类型**（不提供原子性、不建立 happens-before）。
  同一屏障从循环体内挪到循环体外，`spin_fence_outside` 立刻与无屏障版本同形（被整段消除）。
controlled_vars: 同夹具、同编译单元、同优化档（-O2）、同目标架构（x86-64）；被测函数各自独占全局变量；唯一变量 = 屏障的种类（signal vs thread）与位置（体内 vs 体外）
matrix:
  compiler: [GCC 15.3.0 (MinGW-w64), GCC 14.2.0 (WSL), GCC 13.3.0 (WSL)]
  stdlib: [none]
  std: [c++23]
  opt: [-O2]
  arch: [x86-64]
  # 可核对锚 1（主工件生成命令）：
  #   `g++ -std=c++23 -O2 -S -masm=intel Examples/atoms/_atom_fence_vs_atomic.cpp -o Examples/atoms/_atom_fence_vs_atomic.asm`
  # 可核对锚 2（跨编译器，artifact_assert 的真实执行环境 = CI Linux g++）：
  #   `g++-14 -std=c++23 -O2 -S -masm=intel Examples/atoms/_atom_fence_vs_atomic.cpp -o build/_conc_gpp14.s`
  #   `g++-13 -std=c++23 -O2 -S -masm=intel Examples/atoms/_atom_fence_vs_atomic.cpp -o build/_conc_gpp13.s`
  #   两条工具链实测都产出 `lock or<TAB>QWORD PTR [rsp], 0` ⇒ 锚只用单 token（lock / [rsp]），
  #   不锚 "lock or QWORD PTR [rsp], 0" 这种含空白的整句（MinGW 用空格、Linux 用制表符）。
  # 可核对锚 3（跨架构，读数写进本卡、工件不提交）：
  #   `riscv64-unknown-elf-g++ -std=c++23 -O2 -S Examples/atoms/_atom_fence_vs_atomic.cpp -o build/_conc_riscv.s`
  #   ⇒ spin_with_fence 循环内 `fence iorw,iorw`；writer_thread_fence 内 `fence iorw,iorw`；
  #     spin_signal_fence / writer_signal_fence 内**无 `fence`**（零指令结论跨架构成立）。
  # 可核对锚 4（stdout 留痕）：Examples/atoms/_atom_fence_vs_atomic.out
fixture: Examples/atoms/_atom_fence_vs_atomic.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/atoms/_atom_fence_vs_atomic.cpp -o Examples/atoms/_atom_fence_vs_atomic.asm
  g++ -std=c++23 -O2 Examples/atoms/_atom_fence_vs_atomic.cpp -o build/_replay_fence_vs_atomic.exe && ./build/_replay_fence_vs_atomic.exe
artifact: Examples/atoms/_atom_fence_vs_atomic.asm
artifact_sha256: 8dd19bc6bf2facc23d1d09aef6ed4b856d0f33e98c36174b96d2893172319cb3
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains_in, symbol: "_Z17spin_signal_fencev", text: "s_sf_b"}  # 零指令屏障仍保住循环
  - {kind: absent_in, symbol: "_Z17spin_signal_fencev", text: "lock"}      # 自旋侧 signal_fence = 零机器指令
  - {kind: contains_in, symbol: "_Z15spin_with_fencev", text: "lock"}      # thread_fence 才产硬件屏障
  - {kind: contains_in, symbol: "_Z15spin_with_fencev", text: "[rsp]"}     # 被锁的是栈地址，不是标志
  - {kind: contains_in, symbol: "_Z15spin_with_fencev", text: "s_f_b"}     # 标志本身仍是普通访存
  - {kind: absent_in, symbol: "_Z19writer_signal_fencev", text: "lock"}    # 写入侧 signal_fence = 零指令
  - {kind: contains_in, symbol: "_Z19writer_thread_fencev", text: "lock"}  # 写入侧 thread_fence = +1
  - {kind: absent_in, symbol: "_Z18spin_fence_outsidev", text: "s_o_b"}    # 同一屏障挪到体外 ⇒ 无效
  - {kind: contains_in, symbol: "_Z13spin_volatilev", text: "s_v_b"}       # 活性对照（有界 1e6）
actual:
  run_match_file: Examples/atoms/_atom_fence_vs_atomic.out
  run_match_keys: [spin_fence_outside_ret, functions_present]
expected:
  run: >-
    取 `.out` 的第 2、3 行作为本卡的运行期见证：`spin_fence_outside_ret=11|writer_signal_fence_ret=3|writer_thread_fence_ret=3`
    与 `functions_present=7|spin_volatile_engaged=1`。逐字比对通过 ⇒ 当前夹具源码经对应编译器产出的
    stdout 与留痕 `.out` 逐字一致（若编译器对同源码产出相同输出，陈旧 `.out` 也可能通过，故该 key
    主要证明夹具结构与运行期格式未被破坏，不单独作为"已重编译"的强见证）；
    两个 writer 的返回值非 0 说明写入侧函数真的被调用过（其**内部**屏障指令形态由 `artifact_assert` 判定）。
    完整 3 行 stdout 见 `Examples/atoms/_atom_fence_vs_atomic.out`；第 1 行的逐字比对由 EV-CONC-001 承担。
  asm: 9 条 `contains_in` / `absent_in` 为符号区间语义；`lock` 与 `[rsp]` 用**单 token** 锚定，避开 MinGW（空格）与 Linux（制表符）的操作数分隔差异
verdict: confirm
falsification: >-
  **真对照 A（signal_fence 是否真的零指令）**：若 `atomic_signal_fence` 其实生成硬件屏障，
  则 `absent_in _Z17spin_signal_fencev "lock"` 与 `absent_in _Z19writer_signal_fencev "lock"`
  应为假 —— 实测两条均 **0 处**，且 riscv 侧两条也**无 `fence`**（跨架构一致）⇒ "纯编译器屏障"成立。
  **真对照 B（屏障是否给了原子性——本卡的核心否证）**：若硬件屏障把普通 `int` 变成了无竞争访问，
  那么它必须对**该标志的访存**施加原子操作。实测 x86-64 三条工具链一致：
  `spin_with_fence` 区间内的 `lock or … [rsp], 0` **锁的是栈地址 `[rsp]`**，
  而标志仍以普通 `mov` 访问（`mov eax, DWORD PTR s_f_b[rip]`），**没有任何以 `s_f_b` 为目标的
  `lock` 前缀指令** ⇒ 屏障只约束顺序，不改变访问的原子性、不建立 happens-before。
  **真对照 C（位置敏感性）**：`spin_fence_outside` 用的是**同一个** `atomic_thread_fence`，
  只因挪到循环之前，结果与完全不设屏障的 `spin_plain` 同形（`s_o_b` = 0、无 `je`）⇒
  起作用的不是"屏障的存在"，而是"屏障在循环体内"。
  **量化读数（`_symbol_body` 区间内出现次数，实测）**：
  | 断言 | MinGW 15.3 | g++-14.2 | g++-13.3 | riscv64 13.2（不提交工件） |
  |---|---|---|---|---|
  | `_Z17spin_signal_fencev` ∋ `lock` | 0 | 0 | 0 | 0（`fence` 亦为 0） |
  | `_Z15spin_with_fencev` ∋ `lock` | 1 | 1 | 1 | 0（riscv 用 `fence iorw,iorw`） |
  | `_Z15spin_with_fencev` ∋ `[rsp]` | 1 | 1 | 1 | —（riscv 无此寻址形态） |
  | `_Z19writer_signal_fencev` ∋ `lock` | 0 | 0 | 0 | 0（`fence` 亦为 0） |
  | `_Z19writer_thread_fencev` ∋ `lock` | 1 | 1 | 1 | 0（riscv 用 `fence`） |
  x86-64 侧 9/9 全绿；riscv 侧 7/9，差异 2 条是 x86 专有助记符（`lock` / `[rsp]`），
  **已如实标注、不写死进断言**；riscv 的结论等价物是 `fence iorw,iorw`（有）与"无 `fence`"（零指令）。
  **未采集（不编造）**：本卡不含任何运行期自旋行为数据（夹具让循环条件首次即假）；
  也不主张 x86-64 之外的 `lock` 语义。
depth_layer: compile-time
drill_note: >-
  把这两条屏障放在一起看，就能一眼看出"屏障≠原子类型"：
  `atomic_signal_fence` 一条指令都不生成，却足以让编译器**不敢**删掉那个空循环；
  `atomic_thread_fence` 生成 `lock or [rsp], 0`，但这条指令**只碰栈**，与被保护的变量无关——
  它的作用是在流水线上划一条顺序边界，而不是把变量变成原子的。
  所以自旋等待的正确写法是 `std::atomic<bool> ready` + `ready.load(std::memory_order_acquire)`：
  原子类型同时提供**原子性**与**可见性/顺序**，而屏障只提供后者中的顺序那一半，
  且拿普通 `int` 做标志这件事本身就是数据竞争（UB），加多少屏障都救不回来。
---

# EV-CONC-002 · 对照卡：signal_fence 零指令 vs thread_fence 有指令，同一屏障挪出循环即无效

## 实测（-O2，主工件 `Examples/atoms/_atom_fence_vs_atomic.asm`，sha `8dd19bc6…`）

| 对照项 | 自旋侧 | 写入侧 | 读数 |
|---|---|---|---|
| `signal_fence`（纯编译器屏障） | `_Z17spin_signal_fencev` 区间内 `lock` = **0**，但循环**保留** | `_Z19writer_signal_fencev` 区间内 `lock` = **0** | 零机器指令 |
| `thread_fence`（硬件屏障） | `_Z15spin_with_fencev` 区间内 `lock` = **1**，锁在 `[rsp]` | `_Z19writer_thread_fencev` 区间内 `lock` = **1** | 有机器指令 |
| 普通 `int` 的访存 | 仍为 `mov eax, DWORD PTR s_f_b[rip]` | 仍为普通 `mov` 写 | **屏障不改原子性** |
| 同一 `thread_fence` 挪到循环**体外** | `_Z18spin_fence_outsidev` 区间内 `s_o_b` = **0**（被整段消除） | — | **位置决定结果** |

跨架构（riscv64-unknown-elf-g++ 13.2，工件不提交）：`thread_fence` ⇒ 循环内 `fence iorw,iorw`；
`signal_fence` ⇒ **无 `fence`**；`spin_plain` / `spin_fence_outside` 同样被消除。
⇒ 结构结论跨架构一致，差异仅在助记符（`lock` vs `fence`）。

## 与 EV-CONC-001 的分工

- **EV-CONC-001（判据卡）**：证**消除分界**——标志符号在区间内"在不在"，据此判"消除 / 保留"，
  并覆盖 `.out` 全部 3 行（100%）。
- **EV-CONC-002（本卡，对照卡）**：证**屏障本身**——`lock` 有/无（signal vs thread）、
  锁的位置（`[rsp]` 而非标志）、以及同一屏障体内/体外的结果差异。
两条链都锚在**同一个** `artifact`（单 artifact 原则），但取用的指令特征不同：001 看"标志读在哪"，
002 看"屏障指令在哪"；交叉点是 `spin_with_fence`（001 用它证"保留"，002 用它证"锁的不是标志"）。

## 本卡不主张什么

1. 不主张 `signal_fence` 有**任何**运行时效果——实测它在两条路径上都零指令。
2. 不主张 `lock or [rsp], 0` 具备跨架构等价物（riscv 用 `fence`；本卡的 `lock` / `[rsp]` 锚限于 x86-64）。
3. 不主张本夹具演示了"正确的自旋等待"——恰恰相反，用普通 `int` 做标志本身就是数据竞争，
   这正是本原子 claim 的后半句"**但屏障≠原子类型**"要拦住的误用。
