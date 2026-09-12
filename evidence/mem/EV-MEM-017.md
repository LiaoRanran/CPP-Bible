---
id: EV-MEM-017
serves: [ATOM-MEM-NEW-001]
kind: run
hypothesis: >-
  new/delete 是两层：new = operator new(分配) + 构造；delete = 析构 + operator delete(释放)。
  二者各自独立、各发生一次（用全局重载的 volatile 计数 + 构造/析构标志观测）。
controlled_vars: 同一 Box 类型、同一编译器、同一 -O2；唯一变量 = 走 new/delete 还是手动
matrix:
  compiler: [GCC 15.3.0]
  # Clang 列待 CI Cross-check 步回填（GCC 15.3.0 已实测）
  std: [c++23]
  opt: [-O2]
  arch: [x86-64]
fixture: Examples/atoms/_atom_new_layer.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/atoms/_atom_new_layer.cpp -o Examples/atoms/_atom_new_layer.asm
  g++ -std=c++23 -O2 Examples/atoms/_atom_new_layer.cpp -o build/_replay_nlay.exe && ./build/_replay_nlay.exe
artifact: Examples/atoms/_atom_new_layer.asm
artifact_sha256: 094311a8f172880928aa1bab97fc4c988cc7fa1254a35a74cbc2c0215d258b45
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains, text: "_Znwm"}    # operator new 进入工件（分配层真实存在）
expected:
  run: new 后 alloc=1 ctor=1；delete 后 dealloc=1 dtor=1（两层各一次）
  asm: operator new(_Znwm) / operator delete 调用点真实存在
actual:
  run_cxx23_O2: "after new: alloc=1 ctor=1|after delete: dealloc=1 dtor=1"
verdict: confirm
falsification: >-
  若 new 只分配不构造（ctor=0）或 delete 只析构不释放（dealloc=0），则"两层分离"被推翻 => refute。
  实测 alloc/ctor 各 1、dealloc/dtor 各 1 => 经受住证伪（注意 -O2 优先调"带尺寸的 delete"，
  operator delete(void*, size_t) 也须重载才能观测到释放，已补）。
depth_layer: runtime
drill_note: >-
  operator new/delete 是替换点（[basic.stc.dynamic]），new 表达式 = 分配 + 构造、delete 表达式 = 析构 + 释放。
  volatile 计数把"两层各发生一次"变成可比对输出；修复了 -O2 下 sized-delete 不被重载导致 dealloc 不增的坑。
reproduce: 见 command 两行，无外部依赖
---

## 为什么这个证据可信

1. **两层各自可数**：alloc/ctor 与 dealloc/dtor 是四个独立 volatile 计数，new 触发前两个、delete 触发后两个，
   不存在"一步到位"的假象。
2. **修复了优化坑**：初版只重载无尺寸 delete，-O2 调 sized delete 导致 dealloc 不增；补尺寸重载后观测正确。
3. **与 RAII-001 自洽**：RAII 的智能指针正是把"分配+构造/析构+释放"这对动作封装进构造/析构，本卡证明
   这对动作确实是两个独立步骤（所以才会"忘了 delete 就泄漏"）。
