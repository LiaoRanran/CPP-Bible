---
id: MIS-CONC-003
name: 没被 TSan 报就是没有数据竞争 / 数据竞争只是偶尔算错
level: deep
domain: CONC
trigger_patterns:
  - "没被 TSan 报就是安全的"
  - "数据竞争只是结果偶尔算错，不算 bug"
  - "用 volatile 就能防止多线程竞争"
  - "加个 mutex 随便包一下就行"
refutations:
  - "TSan 只分析被 -fsanitize=thread 插桩的 TU；第三方库/内联汇编/未插桩 TU 内的竞争它看不到（漏报），故「没被报 ≠ 没有」"
  - "数据竞争是 C++ 标准明文的未定义行为，不是「答案偶尔错」：编译器可据此做激进优化（寄存器缓存、删除看似冗余的读），行为完全不可预测"
  - "C++ 的 volatile 不建立线程间 happens-before，不能防数据竞争——TSan 对 volatile 竞争照样报；防竞争靠 atomic/mutex/barrier"
source: 343 线 B-2 · EV-CONC-005 / EV-CONC-006
related_atoms: [ATOM-CONC-RACE-001]
---

# MIS-CONC-003 · 数据竞争与 TSan 的三类典型误解

**层级**：deep —— 数据竞争的真面目（UB 而非「算错」）常被教材弱化，须多反例纠偏。

## 触发模式（学习者常这么说 / 这么写）

- 「没被 TSan 报，说明我的并发没问题」
- 「数据竞争嘛，顶多结果偶尔算错，又不会崩」
- 「给共享变量加个 `volatile` 就不竞争了」
- 「加个 mutex 随便包一下就行」

## 为什么不成立（三条反例）

1. **TSan 沉默 ≠ 安全**：TSan 只插桩用它编译的翻译单元。若任一 TU 未用 `-fsanitize=thread` 混链，或竞争发生在第三方库/内联汇编/系统调用内部，TSan 完全看不到。一次「没报」不是「没有」的证明（与 LSan 同族：没报 ≠ 没泄漏）。
2. **数据竞争是 UB，不是「算错」**：标准要求 data race 属未定义行为。编译器可假定「无数据竞争」做激进优化——把变量缓存进寄存器、删掉看似冗余的读、重排无关写。后果不是「答案偶尔差一点」，而是逻辑整体不可预测，可能在某些优化档/平台上彻底翻车。
3. **`volatile` 防不了竞争**：C++ 的 `volatile` 只抑制单线程内的编译器重排与缓存，**不建立线程间 happens-before**（与 Java/C# 的 volatile 语义不同）。两个线程无同步并发读写一个 `volatile int`，TSan 照样报 data race。正确手段是 `std::atomic` / mutex / 显式 barrier。

## 出处与关联

- 出处：343 线 B-2，证据见 `EV-CONC-005`（数据竞争是 UB）、`EV-CONC-006`（TSan 检测与漏报边界）。
- 关联原子：`ATOM-CONC-RACE-001`。
