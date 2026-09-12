---
id: EV-CONC-001
serves: [ATOM-CONC-FENCE-001]
kind: asm
hypothesis: >-
  `while (!b) {}`（b 为非原子非 volatile 全局 `int`）在 `-O2` 下是否被整段消除，
  由**同步操作落在循环体内还是体外**决定，而不是由"函数里有没有屏障"决定：
  无屏障（`spin_plain`）与屏障在**循环体外**（`spin_fence_outside`）都被整段消除，
  函数符号区间内**零** `s_*_b` 符号引用；屏障在**循环体内**（`spin_signal_fence` 零机器指令 /
  `spin_with_fence` 产 `lock`）则循环保留，区间内可见 `s_sf_b` / `s_f_b` 与循环回边。
controlled_vars: 同夹具、同编译单元、同优化档（-O2）、同目标架构（x86-64）、同 `extern "C"` printf 声明；每个被测函数**独占**自己的全局变量（`s_p_*` / `s_sf_*` / `s_f_*` / `s_v_*` / `s_o_*` / `w_*`）⇒ 某符号出现在某函数区间内只可能来自该函数体；唯一变量 = 同步操作的位置与种类
matrix:
  compiler: [GCC 15.3.0 (MinGW-w64), GCC 14.2.0 (WSL), GCC 13.3.0 (WSL)]
  stdlib: [none]
  std: [c++23]
  opt: [-O2]
  arch: [x86-64]
  # 可核对锚 1（主工件生成命令，逐字可复算 sha）：
  #   `g++ -std=c++23 -O2 -S -masm=intel Examples/atoms/_atom_fence_vs_atomic.cpp -o Examples/atoms/_atom_fence_vs_atomic.asm`
  # 可核对锚 2（artifact_assert 的真实执行环境 = CI 的 Linux g++；本卡 12/12 已在此复算）：
  #   `g++-14 -std=c++23 -O2 -S -masm=intel Examples/atoms/_atom_fence_vs_atomic.cpp -o build/_conc_gpp14.s`
  #   `g++-13 -std=c++23 -O2 -S -masm=intel Examples/atoms/_atom_fence_vs_atomic.cpp -o build/_conc_gpp13.s`
  # 可核对锚 3（stdout 留痕，run_match_file 比对对象）：
  #   Examples/atoms/_atom_fence_vs_atomic.out
  # 夹具零 #include（riscv64-unknown-elf-g++ 裸机工具链连 <cstdio> 都没有，实测
  #   `fatal error: cstdio: No such file or directory`），故 stdlib 记为 none：
  #   只用 __atomic_* 内建 + 手写 printf 声明。
fixture: Examples/atoms/_atom_fence_vs_atomic.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/atoms/_atom_fence_vs_atomic.cpp -o Examples/atoms/_atom_fence_vs_atomic.asm
  g++ -std=c++23 -O2 Examples/atoms/_atom_fence_vs_atomic.cpp -o build/_replay_fence_vs_atomic.exe && ./build/_replay_fence_vs_atomic.exe
artifact: Examples/atoms/_atom_fence_vs_atomic.asm
artifact_sha256: 8dd19bc6bf2facc23d1d09aef6ed4b856d0f33e98c36174b96d2893172319cb3
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: absent_in, symbol: "_Z10spin_plainv", text: "s_p_b"}            # 无屏障 ⇒ 标志读被删除
  - {kind: absent_in, symbol: "_Z10spin_plainv", text: "je"}               # 连条件跳转都没了 ⇒ 整段消除
  - {kind: contains_in, symbol: "_Z17spin_signal_fencev", text: "s_sf_b"}  # 体内零指令屏障 ⇒ 循环保留
  - {kind: contains_in, symbol: "_Z17spin_signal_fencev", text: "je"}      # 保留循环回边
  - {kind: absent_in, symbol: "_Z17spin_signal_fencev", text: "lock"}      # signal_fence 零硬件指令（活性对照）
  - {kind: contains_in, symbol: "_Z15spin_with_fencev", text: "s_f_b"}     # 体内 thread_fence ⇒ 保留
  - {kind: contains_in, symbol: "_Z15spin_with_fencev", text: "lock"}      # 产硬件屏障（x86-64）
  - {kind: contains_in, symbol: "_Z13spin_volatilev", text: "s_v_b"}       # volatile 活性对照（有界 1e6）
  - {kind: absent_in, symbol: "_Z18spin_fence_outsidev", text: "s_o_b"}    # 屏障在体外 ⇒ 同样被消除
  - {kind: absent_in, symbol: "_Z18spin_fence_outsidev", text: "je"}       # 同上：无循环回边
  - {kind: absent_in, symbol: "_Z19writer_signal_fencev", text: "lock"}    # 写入侧零指令（活性对照）
  - {kind: contains_in, symbol: "_Z19writer_thread_fencev", text: "lock"}  # 写入侧 +1
actual:
  run_match_file: Examples/atoms/_atom_fence_vs_atomic.out
  run_match_keys: [spin_plain_ret, spin_fence_outside_ret, functions_present]
expected:
  run: >-
    夹具 stdout 共 3 行，`run_match_keys` 的 3 个 key **覆盖全部 3 行（100%）**：
    `spin_plain_ret=7|…`（覆盖 4 个 spin 返回值）、`spin_fence_outside_ret=11|…`（覆盖
    `spin_fence_outside` 与两个 writer）、`functions_present=7|spin_volatile_engaged=1`。
    逐字比对通过 ⇒ 当前夹具源码经对应编译器产出的 stdout 与留痕 `.out` **逐字一致**。
    需说明：若编译器对同源码产出相同输出，陈旧 `.out` 也可能通过，故该 key 主要证明
    **夹具结构与运行期格式未被破坏**，不单独作为"已重编译"的强见证；结构证据由 12 条
    `artifact_assert` 承担。返回值 7/8/9/10/11 互不相同，说明 7 个函数各自被调用且返回了从全局加载的值。
  asm: 12 条 `contains_in` / `absent_in` 均为**符号区间语义**（`<symbol>:` → 下一个列 0 标号或 `.cfi|.seh_endproc`）；符号缺失时区间为 `None` ⇒ 该条直接判失败（fail-closed）
verdict: confirm
falsification: >-
  **真对照 A（位置 vs 存在性，核心）**：若决定因素是"函数里**存在**屏障"而不是"**循环体内**有屏障"，
  则 `spin_fence_outside`（函数里**有** `atomic_thread_fence`，只是挪到循环之前）应当保住循环 ——
  实测它与完全不设屏障的 `spin_plain` **同形**：区间内 `s_o_b` = 0、`s_p_b` = 0，两者都无 `je`。
  ⇒ "存在性"假设被否，"位置"假设存活。该对照即夹具 ⑤，是本卡否决竞争解释的关键。
  **真对照 B（signal_fence 是否真的零指令）**：若 `atomic_signal_fence` 其实产出了硬件屏障，
  则 `absent_in _Z17spin_signal_fencev "lock"` 与 `absent_in _Z19writer_signal_fencev "lock"`
  应为假 —— 实测两条都是 **0 处**（两条路径都零指令）⇒ "纯编译器屏障"成立。
  **量化读数（`_symbol_body` 区间内出现次数，实测；本卡 12 条断言全覆盖）**：
  | 断言 | MinGW 15.3 | g++-14.2 | g++-13.3 | riscv64 13.2（不提交工件） |
  |---|---|---|---|---|
  | `_Z10spin_plainv` ∋ `s_p_b` | 0 | 0 | 0 | 0 |
  | `_Z10spin_plainv` ∋ `je` | 0 | 0 | 0 | 0（riscv 无 `je`，用 `beq`） |
  | `_Z17spin_signal_fencev` ∋ `s_sf_b` | 2 | 1 | 1 | 3 |
  | `_Z17spin_signal_fencev` ∋ `je` | 1 | 1 | 1 | 0（riscv 无 `je`，用 `beq`） |
  | `_Z17spin_signal_fencev` ∋ `lock` | 0 | 0 | 0 | 0 |
  | `_Z15spin_with_fencev` ∋ `s_f_b` | 2 | 1 | 1 | 3 |
  | `_Z15spin_with_fencev` ∋ `lock` | 1 | 1 | 1 | 0（riscv 用 `fence iorw,iorw`） |
  | `_Z13spin_volatilev` ∋ `s_v_b` | 1 | 1 | 1 | 2 |
  | `_Z18spin_fence_outsidev` ∋ `s_o_b` | 0 | 0 | 0 | 0 |
  | `_Z18spin_fence_outsidev` ∋ `je` | 0 | 0 | 0 | 0（riscv 无 `je`，用 `beq`） |
  | `_Z19writer_signal_fencev` ∋ `lock` | 0 | 0 | 0 | 0 |
  | `_Z19writer_thread_fencev` ∋ `lock` | 1 | 1 | 1 | 0（riscv 用 `fence`） |
  x86-64 侧 **12/12 全绿**（两条独立工具链）⇒ 断言锚可用；riscv 侧 **9/12**，
  差异 3 条是 **x86 专有助记符**（1 条 `je` + 2 条 `lock`，riscv 分别用 `beq` / `fence iorw,iorw`），已如实标注，**不写死进断言**
  （riscv 上对应 `beq` / `fence`，结构性结论一致：消除/保留的方向完全相同）。
  **注意**：`[rsp]` 锚（证"屏障锁栈不锁标志"）只属于 **EV-CONC-002** 的 9 条断言，**不在本卡 12 条内**，勿跨卡张冠李戴。
  **未采集（不编造）**：`spin_volatile` 在标志为 0 时实际自旋了多少次——夹具用
  `set_all_flags(1)` 让循环条件首次即假，**循环体从未执行**；本卡是**结构证据**，不含运行时行为断言。
depth_layer: compile-time
drill_note: >-
  C++ 的 `[intro.progress]` 允许编译器假定"无副作用且不终止的循环"不会发生，因此
  `while (!b) {}` 里若没有同步操作，这个循环连同循环体内的 load 都可以被整段删掉——
  `spin_plain` 的最终产物是 `mov eax, s_p_a[rip]; ret`，看代码"在读 b"，产物里连 b 的影子都没有。
  把 `atomic_signal_fence`（一条机器指令都不生成）放进**循环体内**就足以改变结论：循环体有了
  同步操作 ⇒ 不再是"无副作用" ⇒ 不可删（实测 `s_sf_b` 出现在区间内且有回边）。
  但**屏障不是原子类型**：它既不给普通 `int` 原子性，也不建立跨线程 happens-before，
  所以这段自旋即便"没被删掉"，用普通 `int` 做标志仍然是数据竞争（UB）。
  正确修法是改用 `std::atomic<bool>` + `load(acquire)` / `store(release)`，而不是往循环里塞 fence。
---

# EV-CONC-001 · 消除分界：屏障在**循环体内**才拦住消除（三平台实测）

## 实测（-O2，主工件 `Examples/atoms/_atom_fence_vs_atomic.asm`，sha `8dd19bc6…`，5165 B）

| 函数 | 屏障 | x86-64 产物形态（MinGW 15.3；g++-14 / g++-13 同形） | 区间内标志符号引用 | 结论 |
|---|---|---|---|---|
| `spin_plain` | 无 | `mov eax, s_p_a[rip]` → `ret` | `s_p_b` = **0** | **整段消除** |
| `spin_signal_fence` | 体内 `signal_fence` | 循环回边 + `je`，**区间内零 `lock`** | `s_sf_b` = **2** | **保留** |
| `spin_with_fence` | 体内 `thread_fence` | 循环内 `lock or QWORD PTR [rsp], 0` ×1 | `s_f_b` = **2** | **保留** |
| `spin_volatile` | 体内 volatile（有界 1e6） | 有界循环保留 | `s_v_b` = **1** | 活性对照 |
| `spin_fence_outside` | **体外** `thread_fence` | `mov eax, s_o_a[rip]` → `ret` | `s_o_b` = **0** | **与无屏障同：被消除** |
| `writer_signal_fence` | 写入侧 `signal_fence` | 区间内零屏障指令 | `lock` = **0** | signal_fence 零指令 |
| `writer_thread_fence` | 写入侧 `thread_fence` | 区间内 `lock` ×1 | `lock` = **1** | thread_fence 才有硬件屏障 |

riscv64-unknown-elf-g++ 13.2（同夹具、`-O2 -S`，**工件不提交**、只留读数）：
`spin_plain` = `lw a0, %lo(s_p_a); ret`（同样消除）；`spin_signal_fence` 保留回边（`beq`）、
**区间内无 `fence`**；`spin_with_fence` 循环内 `fence iorw,iorw`；
`writer_thread_fence` 内 `fence iorw,iorw`，`writer_signal_fence` 内无 `fence`。
⇒ 跨架构方向一致，差异只在助记符。

## 符号区间断言的语义（为什么它能把"消除"变成可机器判定）

`artifact_assert` 的 `contains_in` / `absent_in` 把文本切到**符号区间**：
从 `<symbol>:` 到下一个列 0 标号或 `.cfi_endproc` / `.seh_endproc`。
2026-09-12 前该停止条件只认列 0 的 `.seh_endproc`，而真实工件里它是**制表符缩进**的
（MinGW/Mingw-W64 产物实测），导致区间一路越过下一个函数的头部——那样
"`_Z10spin_plainv` 区间内不含 `s_p_b`"就会**恒真**（真空通过）。已修正为正则
`^(?:[^\s.][^\s:]*:\s*$|\s*\.(?:cfi|seh)_endproc\s*$)` 并加回归锁
（`tests/test_atom_evidence_replay.py::test_symbol_scope_stops_at_endproc_not_next_function`）。
本卡的 12 条断言全部建立在该区间语义上，且每个函数**独占**全局变量（第二层保险）。

## 关于 `functions_present=7`（口径说明，非结论依据）

`functions_present=7` 是夹具 `printf` **格式串里的编译期常量**（`printf("functions_present=7|…")`），
按本项目 S3 口径它**不构成活性观测**——它只声明"夹具里有 7 个函数"。
本卡把它保留为 `run_match_keys` 之一，作用是让 `.out` 的**第 3 行进入逐字比对**（覆盖同行的
`spin_volatile_engaged`，该项由运行期 `r_v != 0` 派生），**不作为结论依据**。
函数存在性由 12 条区间断言 fail-closed 承担：符号缺失 ⇒ `_symbol_body` 返回 `None` ⇒ 该条判失败。

## 本卡不主张什么

1. **不主张运行时行为**：`spin_loop` 的循环体在本次运行中从未执行（`set_all_flags(1)` 使条件首次即假），
   故本卡只证"编译器产出了什么结构"。
2. **不主张重排方向**：x86-64 把 load 提到 store 之前、riscv 没有，方向是脆的，故不锚。
3. **不主张屏障可以当同步用**——恰恰相反：屏障只影响编译器对循环的处理，不给普通 `int`
   原子性与跨线程可见性（见 EV-CONC-002）。
