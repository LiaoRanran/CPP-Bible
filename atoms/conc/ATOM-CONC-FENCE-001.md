---
id: ATOM-CONC-FENCE-001
title: 内存屏障（fence）只约束顺序，不提供原子性；屏障在循环体内才阻止消除，但屏障≠原子类型
domain: conc
type: mechanism
status: verified
verified_by: human:liaoranran
verified_at: 2026-09-12
dal: A
human_review: required
status_history:
  - {level: draft, at: "2026-09-12", by: machine:writer}
  - {level: machine-verified, at: "2026-09-12", by: machine:gate}
  - {level: verified, at: "2026-09-12", by: human:liaoranran}
audience: intermediate
cognitive_load: medium
prerequisites_readable: true
claim: >-
  任何内存屏障（含零指令的 atomic_signal_fence）只要落在循环体内，就能阻止编译器消除该循环；
  但屏障不提供数据竞争安全——屏障≠原子类型。
claim_boundary:
  standard: [C++11, C++14, C++17, C++20, C++23]
  compilers: [GCC 15.3.0 (MinGW-w64), GCC 14.2.0 (WSL), GCC 13.3.0 (WSL)]
  opt: [-O2]
  platform: [x86-64]
relations: []
evidence:
  - EV-CONC-001
  - EV-CONC-002
sources:
  - {kind: iso, ref: "ISO/IEC 14882:2023 [intro.progress]（允许假定无副作用且不终止的循环不发生，故循环体内无同步操作时整段可被删除）", independent: true}
  - {kind: cppreference, ref: "std::atomic_signal_fence / std::atomic_thread_fence（fence 仅约束内存顺序，不为普通访问提供原子性与 happens-before）", independent: true}
first_hand: true
superiority: >-
  C++ 内存模型教材常把"加个 fence 就能同步"当成默认解法，却讲不清 fence 与原子类型的边界。
  本原子用一组同源对照把三件事拆开讲清：① 消除层——屏障落在循环体内才保住循环（零指令的
  signal_fence 也保得住），挪到体外则与无屏障同形被消除；② 指令层——signal_fence 零机器指令、
  thread_fence 才产 lock，但 lock 锁的是栈地址而非标志；③ 同步层——屏障既不给原子性也不建
  happens-before。三张对照交叉指向同一个 artifact，避免"讲了顺序忘了原子性"的半截理解。
depth:
  layer: compile-time
pedagogy:
  motivation: "读者常以为自旋等待加个 fence 就够了，结果用普通 int 做标志仍是数据竞争（UB）。"
  misconception:
    - {level: surface, text: "误以为屏障（fence）能替代原子类型提供同步：给普通 int 标志加个 atomic_thread_fence 即可当线程间就绪标志用", refutations: [EV-CONC-001, EV-CONC-002]}
    - {level: deep, text: "误以为屏障完全拦不住编译器消除（早期'屏障拦不住消除'说法方向说反）：实测零指令的 signal_fence 只要落在循环体内就能保住循环", refutations: [EV-CONC-001, EV-CONC-002]}
  socratic: "如果屏障真能阻止消除，它保住的是哪个循环？把 thread_fence 的 lock 指令地址打出来，它锁的是哪个变量？"
  predict_first: "先预测：把 atomic_signal_fence 放进空循环体，循环会被消除还是保留？把 thread_fence 生成的 lock 操作数打印出来，它锁的是标志本身吗？"
  misconceptions: [MIS-CONC-001]
misconceptions: [MIS-CONC-001]
---

# ATOM-CONC-001 · 屏障≠原子类型（屏障位置决定消除）

一句话直觉：**屏障是"别乱动"的编译器指令，不是"别人别动"的运行时保护。**

## 1. 三层分解

### 1.1 消除层（编译器能不能删）
`while (!b) {}`（b 为非原子非 volatile 全局 `int`）在 `-O2` 下，若循环体不含同步操作，按 C++ `[intro.progress]`（允许假定"无副作用且不终止的循环"不发生）可被整段删除——`spin_plain` 的最终产物仅是 `mov eax, s_p_a[rip]; ret`，看代码"在读 b"，产物里连 b 的影子都没有。
把 `atomic_signal_fence`（零机器指令）或 `atomic_thread_fence`（产 `lock`）放进**循环体内**，循环体即含同步操作 ⇒ 不再满足"无副作用"前提 ⇒ 不可删（实测 `s_sf_b` / `s_f_b` 出现在区间内且有回边）。

### 1.2 指令层（产生什么 CPU 指令）
`signal_fence` 是**纯编译器屏障**——实测自旋侧与写入侧两条路径**均为零机器指令**；`thread_fence` 才产生硬件屏障：x86-64 `lock or QWORD PTR [rsp], 0`，riscv64 `fence iorw,iorw`。详见 EV-CONC-002。

### 1.3 同步层（能不能保护数据竞争）
两者都**不**为普通 `int` 提供原子性、不建立跨线程 happens-before。关键实测：`lock or … [rsp], 0` **锁的是栈地址 `[rsp]`，不是标志**——标志仍以普通 `mov` 访问。所以屏障 ≠ 原子类型：即便循环保住了，用普通 `int` 做标志仍然是数据竞争（UB）。

## 2. 证据摘要（不复制 full actual，详见两张卡）
- **EV-CONC-001（判据卡，12 条符号区间断言，三平台核验）**：`spin_plain` 与 `spin_fence_outside`（屏障在循环**体外**）区间内 `s_*_b` = 0 ⇒ 被整段消除；`spin_signal_fence` / `spin_with_fence`（屏障在**体内**）区间内可见标志读与循环回边 ⇒ 保留。关键反例 `spin_fence_outside` 用的是**同一个** `thread_fence`，只因挪到循环之前，就与无屏障版本同形 ⇒ "起作用的不是屏障存在，而是它在循环体内"。
- **EV-CONC-002（对照卡，9 条断言）**：`signal_fence` 零指令、却照样保住循环；`thread_fence` 产 `lock` 却锁在 `[rsp]` 而非标志 ⇒ 屏障不改原子性。同一 `thread_fence` 挪到体外即与无屏障同形。

## 3. 教学要点
为什么需要 `std::atomic` 而不是只加屏障：原子类型同时提供**原子性**与**可见性/顺序**；屏障只提供顺序那一半，且拿普通 `int` 做标志本身就是 UB，加多少屏障都救不回来。正确写法 `std::atomic<bool> ready` + `load(acquire)` / `store(release)`。

## 4. 边界与限制
- riscv64 上 3 条 x86 专有助记符断言（`je` / `lock` / `[rsp]`）不适用：riscv 用 `beq` / `fence`，结构性结论一致（消除/保留方向相同），但断言只钉 x86-64。
- 不主张运行时行为：夹具令循环条件首次即假，循环体从未执行，本原子是**结构证据**。
- 不主张重排方向：x86-64 把 load 提到 store 之前、riscv 没有，方向是脆的，故不锚。

## 5. 修订记录
- **v1（312 原始稿）**：claim「屏障拦不住消除」——被三平台实测推翻（零指令的 `signal_fence` 落在体内就能保住循环）。
- **v2（本稿）**：修正为「屏障在循环体内阻止消除，但屏障≠原子类型」。PostgreSQL f8ccab0e（2025-11-07，REL_18_STABLE，backpatch-through 13，C11 fence 只为原子访问定义语义）降为**移植性论据**，不作本地产物断言、不作主 claim。

## 6. 5 分锚定依据

本原子经以下三条独立证据链支撑，达到 `verified` 与 5 分质量锚定：

1. **双平台机器复算**：Windows（MinGW 15.3.0）与 WSL（g++-13.3.0）分别重跑 replay，均 `confirm=2 / refute=0`；主工件 sha `8dd19bc6…` 在两环境逐字一致，`artifact_assert` 的 **12/12 + 9/9** 在跨编译器路径真实执行并全绿（非只看 sha 的真空通过）。
2. **独立红队两段式盲读**：专用子 agent 仅持夹具 / 工件 / 两张卡 actual（不持本草稿），给出 **阻断级 0 / 高级 1（仅文字错配，已修）/ 建议 3**；四项核心论点（体内屏障保循环、体外即失效、signal 零指令、屏障锁栈不锁标志）均被工件反向证伪为成立，证据链可被接收。
3. **三平台读数如实锚定边界**：MinGW 15.3 / g++-14.2 / g++-13.3 各 12/12；riscv64 13.2 为 9/12，差异 3 条全为 x86 专有助记符（`je` / `lock`），已如实标注、不写死进断言；`functions_present=7` 编译期常量已明标不作结论依据（详见 EV-CONC-001 §口径说明）。
