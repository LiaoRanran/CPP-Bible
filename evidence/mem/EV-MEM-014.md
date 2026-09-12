---
id: EV-MEM-014
serves: [ATOM-MEM-SHARED-001]
kind: run
hypothesis: >-
  shared_ptr 不能自动处理循环引用：两个对象互相 shared_ptr 持有，彼此计数为 2，离开作用域后各自
  只减到 1（仍互相持有），计数永不归零 => 两对象都不析构（泄漏）。这证伪"shared_ptr 总能管好生命周期"。
controlled_vars: 同一 Node 类型、同一编译器、同一 -O2；唯一变量 = 是否形成互相持有（循环引用）
matrix:
  compiler: [GCC 15.3.0]
  # Clang 列待 CI Cross-check 步回填（GCC 15.3.0 已实测）
  std: [c++23]
  opt: [-O2]
  arch: [x86-64]
fixture: Examples/atoms/_atom_shared_cycle.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/atoms/_atom_shared_cycle.cpp -o Examples/atoms/_atom_shared_cycle.asm
  g++ -std=c++23 -O2 Examples/atoms/_atom_shared_cycle.cpp -o build/_replay_scyc.exe && ./build/_replay_scyc.exe
artifact: Examples/atoms/_atom_shared_cycle.asm
artifact_sha256: 343c5003d45ea7635712c27ef9bb0b685ac3889f9feb0212026b3e52b77a7656
artifact_compiler: GCC 15.3.0 (MinGW-w64)
expected_sanitizer: [leak]   # 本卡演示循环引用泄漏：sanitizer 命中类型为 leak 时计入 confirm（反向证 claim），不计 refute；其余类型仍 refute
artifact_assert:
  - {kind: contains, text: "destroyed"}    # "nodes destroyed count=" 进入工件（泄漏可观测）
expected:
  run: 循环引用下 a/b use_count 均为 2；离开作用域计数为 1，Node 析构 0 次（nodes destroyed count=0）
  asm: 析构路径（"destroyed"）真实存在但未在循环场景触发
actual:
  run_cxx23_O2: "a use_count=2|b use_count=2|nodes destroyed count=0"
verdict: confirm
falsification: >-
  证伪"shared_ptr 总能自动管理生命周期"：若循环引用也能正确释放，则 nodes destroyed count 应为 2；
  实测为 0 => 循环引用泄漏 => 该论断被推翻（须用 weak_ptr 打破，见 ATOM-MEM-WEAK-001）。
  同时反向证伪本原子自身：若把 `b->next = a` 去掉（不成环），destroyed count 应变 2 => 非循环场景 shared 正常释放。
depth_layer: runtime
drill_note: >-
  循环引用下，a 与 b 各被 2 个 shared_ptr 引用（自身 + 对方），离开作用域各减 1 到 1，互指不退零，
  控制块不释放 -> 泄漏。g_destroy=0 是可观测的"未释放"形态（零观测通路活着）。这是 unique_ptr 不会
  遇到的坑（unique 不可共享，自然不成环），也是引入 weak_ptr 的根本理由。
reproduce: 见 command 两行，无外部依赖
---

## 为什么这个证据可信

1. **证伪对照自带**：卡内即"shared_ptr 在循环引用下泄漏"的反例，直接推翻"shared 总是安全"的错觉。
2. **负观测诚实**：泄漏的证据是 `destroyed count=0`（析构 0 次），不是"没看到就当没事"。
3. **指向修复路径**：明确给出"用 weak_ptr 打破循环"（ATOM-MEM-WEAK-001），使证伪同时给出解法。

## 修订记录

- **2026-09-11 · gcc-14 兼容性修复（A 方向，verified 状态保留）**
  背景：本卡演示"循环引用泄漏"。asm 断言 `contains "destroyed"` 在 gcc-14 下仍命中（实测 1 次），
  真正红因在 sanitizer 步——ASan 运行命中 LeakSanitizer，被工具按"未声明豁免"判成
  `refute:sanitizer_reported`。本卡是**有意泄漏**的演示卡，泄漏报错正是 claim 的反向证据。
  修复：新增 `expected_sanitizer: [leak]` 声明（工具 `check_sanitizer` 新增支持：命中类型**全部**
  落在声明内才折算为 confirm，声明外类型仍判 refute）。`artifact_sha256` 未变。
