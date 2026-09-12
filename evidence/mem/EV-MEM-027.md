---
id: EV-MEM-027
serves: [ATOM-MEM-ALLOC-001]
kind: run
hypothesis: >-
  allocator 是 STL 容器的内存**策略**抽象：容器只经 allocator_traits 要内存，不关心策略内容。
  自定义有状态 arena 分配器（预分配一块、线性推进、deallocate 为空操作、相等比较共享同一 arena）
  可无缝接入 std::vector——16 次 push_back 全部由 arena 伺候（calls=5、bytes=124），堆分配为 0；
  对照组（默认 std::allocator 策略）同长度扩容全部走堆（heap_new=5）。
controlled_vars: 同一 vector<int> + 同一 push_back 序列（16 次）、同一编译器；唯一变量 = 分配策略（arena vs 默认堆）
matrix:
  compiler: [GCC 15.3.0]
  # Clang 列待 CI Cross-check 步回填（GCC 15.3.0 已实测）
  std: [c++23]
  opt: [-O0, -O2]
  arch: [x86-64]
fixture: Examples/atoms/_atom_alloc_arena.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/atoms/_atom_alloc_arena.cpp -o Examples/atoms/_atom_alloc_arena.asm
  g++ -std=c++23 -O2 Examples/atoms/_atom_alloc_arena.cpp -o build/_replay_alloc_arena.exe && ./build/_replay_alloc_arena.exe
artifact: Examples/atoms/_atom_alloc_arena.asm
artifact_sha256: e7e7d630dfb8afba4e19e6699bcb87e0c8a86747552bdf42c0c8b5fb6d08cdf3
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains, text: "arena"}     # arena 观测点字符串进入工件（策略路径真实存在）
expected:
  run: arena 组 calls=5 bytes=124 heap_new=0；std 组 heap_new=5（扩容全走堆）
  asm: arena/std 两组观测点字符串进入工件（对照真实存在）
actual:
  run_cxx23_O2: "arena: calls=5 bytes=124 heap_new=0|std  : heap_new=5 (growth reallocations)"
  run_cxx23_O0: "arena: calls=5 bytes=124 heap_new=0|std  : heap_new=5 (growth reallocations)"
verdict: confirm
falsification: >-
  ① 若容器不经 allocator（策略抽象不成立，arena 接不进来），编译红或 calls=0；② 若 arena 组仍走堆
  （heap_new>0），"策略可替换"被推翻——实测 heap_new=0；③ 若对照无区分力（std 组也是 0），实验失效
  ——实测 std 组 heap_new=5。均不成立 => 经受住证伪。
depth_layer: runtime
drill_note: >-
  calls=5/bytes=124 是 libstdc++ vector 倍增扩容的可观测指纹（容量 1→2→4→8→16，字节数
  4×(1+2+4+8+16)=124）：同一 push_back 序列下 std 组 heap_new=5 完全同构——证明容器行为一致，
  唯一变量是内存从哪来。arena 的关键实现点：rebind 出的副本必须共享同一游标（off 用指针）且
  operator== 判等（[allocator.requirements] 的有状态分配器契约），否则 vector 内部副本各用各的
  游标会重复分配/越界。
reproduce: 见 command 两行，无外部依赖
---

## 为什么这个证据可信

1. **同构对照**：两组是同一容器、同一 16 次 push_back 序列，唯一变量是策略——arena 组 calls=5 与
   std 组 heap_new=5 数字同构（同一扩容模式），把"容器行为不变、内存来源变了"分开呈现。
2. **策略语义被真实执行**：arena 的 deallocate 空操作 + 栈上 buf 整体回收，程序无泄漏（buf 不是堆
   内存）；arena_bytes=124 给出策略级字节数，可与 std 组的 5 次堆分配互算自洽。
3. **-O0/-O2 双跑一致**：输出逐字相同，volatile 计数排除折叠。

## 边界诚实说明

- calls=5/bytes=124 依赖 libstdc++ 的倍增扩容模式（1→2→4→8→16）；其他实现扩容策略不同则数字不同，
  但"arena 全承接、堆 0 分配"的结论由标准保证（容器只经 traits 要内存）。
- arena 适合"批量构造、整体回收"场景；单元素释放无意义（deallocate 空操作）是策略取舍而非缺陷，
  正文展开。Clang 列由 CI Cross-check 回填。
