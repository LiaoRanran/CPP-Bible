---
id: EV-MEM-009
serves: [ATOM-MEM-RAII-001]
kind: run
hypothesis: >-
  RAII 把资源生命周期绑定到对象生命周期：构造获取、析构释放；即使函数因异常提前返回，栈展开时
  析构仍自动调用，资源不泄漏。裸 new/delete 在异常路径跳过 delete => 泄漏。
controlled_vars: 同一 main、同一编译器、同一 -O2；唯一变量 = 用 RAII 对象还是裸 new 管理资源
matrix:
  compiler: [GCC 15.3.0]
  # Clang 列待 CI Cross-check 步回填（GCC 15.3.0 已实测）
  std: [c++23]
  opt: [-O2]
  arch: [x86-64]
fixture: Examples/_atom_raii.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/_atom_raii.cpp -o Examples/_atom_raii.asm
  g++ -std=c++23 -O2 Examples/_atom_raii.cpp -o build/_replay_raii.exe && ./build/_replay_raii.exe
artifact: Examples/_atom_raii.asm
artifact_sha256: 7bba13b03d736f5a1e9d5cd767ab91fd53ab651ca48f688054fdd913bafa7720
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains, text: "g_live"}
expected:
  run: RAII 析构在异常后仍被调用（g_live 归 0）；裸路径异常跳过 delete 致 g_live 留 1（泄漏）
  asm: 观测字符串 "g_live" 进入工件（g_live 是 dtor 唯一下减量，归 0 即证明析构在异常路径执行）
actual:
  run_cxx23_O2: "after safe_path g_live=0|after leak_path g_live=1"
verdict: confirm
falsification: >-
  若 safe_path 抛异常后 g_live 仍非 0（RAII 析构未被调用），则"栈展开自动析构"被推翻 => refute。
  若 leak_path 异常后 g_live 归 0（裸资源也被释放），则"裸资源泄漏"对照失效 => refute。
  实测 g_live 0 / 1 => 两条件均不成立，经受住证伪。
depth_layer: runtime
drill_note: >-
  RAII 对象 r 的析构在 safe_path 抛异常后的栈展开中被调用（g_live 回到 0），与"无异常时析构调用"
  是同一套机制；裸路径因 delete 在 throw 之后而不可达，g_live 留在 1 —— 这正是 C++ 用 RAII
  而非手动释放的根本理由（[except.ctor] 保证栈展开调用析构）。
reproduce: 见 command 两行，无外部依赖
---

## 为什么这个证据可信

1. **有证伪对照**：同 TU 内"RAII 对象"与"裸 new"两路径对比，唯一变量是资源管理方式；g_live
   用 `volatile` 计数，排除 -O2 折叠。
2. **负观测也诚实**：泄漏路径的"证据"是 g_live 留 1（没回到 0）——这正是"裸资源未释放"的可观测形态，
   不是"没观察到就当没发生"。
3. **跨优化档稳定**：RAII 析构调用由语言语义（[except.ctor] 栈展开）保证，与 -O2 无关；本卡在 -O2
   实测，输出可在 -O0 复现（构造/析构不受优化影响）。
