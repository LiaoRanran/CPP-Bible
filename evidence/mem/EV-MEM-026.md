---
id: EV-MEM-026
serves: [ATOM-MEM-ALLOC-001]
kind: run
hypothesis: >-
  std::allocator 的基本接口是两层分离的：allocator::allocate 只分配不构造（C++17 后 std::allocator
  连 construct/destroy 成员都移除，构造/析构统一走 std::allocator_traits）——分配层（allocate/
  deallocate）与对象生命周期（construct/destroy）是两个独立动作，各计各的数。
controlled_vars: 同一 Widget 类型、同一编译器、同一 -O2；唯一变量 = 被触发的 allocator 动作（allocate/construct/destroy/deallocate）
matrix:
  compiler: [GCC 15.3.0]
  # Clang 列待 CI Cross-check 步回填（GCC 15.3.0 已实测）
  std: [c++23]
  opt: [-O0, -O2]
  arch: [x86-64]
fixture: Examples/_atom_alloc_basic.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/_atom_alloc_basic.cpp -o Examples/_atom_alloc_basic.asm
  g++ -std=c++23 -O2 Examples/_atom_alloc_basic.cpp -o build/_replay_alloc_basic.exe && ./build/_replay_alloc_basic.exe
artifact: Examples/_atom_alloc_basic.asm
artifact_sha256: 595e63f3fde699a83ad6f1a4a4bbde8f0dcafaa34c9c14cb68c1457284b44559
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains, text: "allocation only"}   # 观测点字符串进入工件（allocate 零构造的断言真实存在）
expected:
  run: allocate 后 allocs=1 ctors=0；construct 两次 ctors=2；destroy 两次 dtors=2；deallocate frees=1
  asm: 观测点字符串进入工件（两层分离的断言真实存在）
actual:
  run_cxx23_O2: "allocate: allocs=1 ctors=0 (allocation only)|construct: ctors=2|destroy: dtors=2|deallocate: frees=1"
  run_cxx23_O0: "allocate: allocs=1 ctors=0 (allocation only)|construct: ctors=2|destroy: dtors=2|deallocate: frees=1"
verdict: confirm
falsification: >-
  ① 若 allocate 顺带构造（ctors=1），"分配/构造两层分离"被推翻——实测 ctors=0；② 若 destroy 不析构或
  deallocate 不释放（dtors/frees 为 0），两层语义不完整——实测 dtors=2、frees=1。均不成立 => 经受住
  证伪。与 EV-MEM-017（new = operator new + 构造）互证：new 表达式只是把这两层缝在一起。
depth_layer: runtime
drill_note: >-
  C++17 起接口收口：std::allocator 只保留 allocate/deallocate（[allocator.members]），construct/
  destroy 由 std::allocator_traits 默认实现承担（本质是 placement new / 显式析构调用）——容器正是
  这样把"内存策略"（allocator）与"对象生命周期"（traits）解耦的。四组 volatile 计数（分配/释放/
  构造/析构）把两层分离变成可比对输出；-O0/-O2 输出逐字一致。
reproduce: 见 command 两行，无外部依赖
---

## 为什么这个证据可信

1. **四组独立计数**：allocs/ctors/dtors/frees 是四个独立 volatile 观测点，"allocate 零构造"
   （allocs=1 ∧ ctors=0）无法被"一层完成"的假象掩盖。
2. **-O0/-O2 双跑一致**：输出逐字相同（run_cxx23_O0/O2 同串），排除优化器折叠（volatile + 拆写
   复合赋值，EV-MEM-002 纪律）。
3. **与既有证据互证**：EV-MEM-017 证明 new 表达式 = operator new + 构造两层；本卡用 allocator
   手工把两层拆开重演——同一事实的两个观察角度，互为印证。

## 边界诚实说明

- allocate(2) 的字节数由实现决定（本机恰好一次 operator new）；卡只锚定"分配次数=1、构造次数=0"
  这一层语义，不写死分配字节数。Clang 列由 CI Cross-check 回填。
