---
id: EV-MEM-016
serves: [ATOM-MEM-WEAK-001]
kind: run
hypothesis: >-
  用 weak_ptr 打破 shared_ptr 循环引用：父->子用 shared_ptr（拥有）、子->父用 weak_ptr（旁观、不拥有），
  离开作用域后强引用计数能归零，两个节点都析构（无泄漏）。这正是 EV-MEM-014 泄漏场景的解法。
controlled_vars: 同一 Node 类型、同一编译器、同一 -O2；唯一变量 = 子->父用 shared_ptr（成环）还是 weak_ptr（打破）
matrix:
  compiler: [GCC 15.3.0]
  std: [c++23]
  opt: [-O2]
  arch: [x86-64]
fixture: Examples/_atom_weak_cycle.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/_atom_weak_cycle.cpp -o Examples/_atom_weak_cycle.asm
  g++ -std=c++23 -O2 Examples/_atom_weak_cycle.cpp -o build/_replay_wcyc.exe && ./build/_replay_wcyc.exe
artifact: Examples/_atom_weak_cycle.asm
artifact_sha256: 4a824906da3e5eefd46b813f489bdf846e06ed5889764e43151736a2f9cd8d69
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains, text: "destroyed"}    # "nodes destroyed count=" 进入工件
expected:
  run: 子->父改 weak 后，a use_count=1、b use_count=2；离开作用域两节点都析构（destroyed count=2）
  asm: 析构路径（"destroyed"）在循环场景正确触发
actual:
  run_cxx23_O2: "a use_count=1|b use_count=2|nodes destroyed count=2"
verdict: confirm
falsification: >-
  证伪"weak 不能打破循环"：若改用 weak 后仍然泄漏（destroyed count != 2），则本卡 refute。
  实测 destroyed count=2（两节点都释放），与 EV-MEM-014 的 0 形成直接对照 => weak 确实打破了循环。
  反向：若把 `b->parent = a` 改回 shared_ptr（成环），destroyed count 应变回 0（回到 EV-MEM-014 场景）。
depth_layer: runtime
drill_note: >-
  子->父用 weak_ptr 不增加 a 的强引用计数（a.use_count=1），故 a 离开作用域即归零释放；a 析构时释放
  a->child(b)，b 计数随之归零释放。弱引用只影响"能否提升"，不影响"何时释放"——这正是打破循环的关键。
reproduce: 见 command 两行，无外部依赖
---

## 为什么这个证据可信

1. **与 EV-MEM-014 直接对照**：同一结构，仅把子->父从 shared 改 weak，destroyed count 0→2——weak 打破循环可证。
2. **计数量化解释**：a.use_count=1（weak 不计数）、b.use_count=2（a 拥有 + 局部），离开作用域能归零。
3. **解法闭环**：本卡是 SHARED-001 证伪卡给出的修复路径的实证，证伪自带解法。
