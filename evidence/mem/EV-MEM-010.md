---
id: EV-MEM-010
serves: [ATOM-MEM-RAII-001]
kind: run
hypothesis: >-
  RAII 清理是"基于作用域"的：同一作用域内多个对象，栈展开时按构造的逆序析构（C 先、B、A 后）。
  这证明"资源生命周期绑定对象生命周期"是逐对象、逆序、跨栈帧的通用机制，而非特例。
controlled_vars: 同一函数、同一编译器、同一 -O2；唯一变量 = 是否触发异常展开（触发后观察析构顺序）
matrix:
  compiler: [GCC 15.3.0]
  # Clang 列待 CI Cross-check 步回填（GCC 15.3.0 已实测）
  std: [c++23]
  opt: [-O2]
  arch: [x86-64]
fixture: Examples/_atom_raii_order.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/_atom_raii_order.cpp -o Examples/_atom_raii_order.asm
  g++ -std=c++23 -O2 Examples/_atom_raii_order.cpp -o build/_replay_raii_order.exe && ./build/_replay_raii_order.exe
artifact: Examples/_atom_raii_order.asm
artifact_sha256: fcd2b8d90bfa27074fb944c0faf8a56a347f09561d531fbeeb0ab8c6b4a862fa
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains, text: "dtor C"}
expected:
  run: 构造序 A B C，异常展开后析构序 C B A（逆序）
  asm: 析构调用（字符串 "dtor C" 等）进入工件，证明展开路径真实存在
actual:
  run_cxx23_O2: "ctor A|ctor B|ctor C|dtor C|dtor B|dtor A"
verdict: confirm
falsification: >-
  若展开后析构顺序不是逆序（如 A B C 或乱序），或某对象析构未被调用，则"基于作用域的逆序清理"被推翻
  => refute。实测 ctor A B C / dtor C B A 严格逆序 => 经受住证伪。
depth_layer: runtime
drill_note: >-
  三个 Tag 对象 a/b/c 在 f() 同一作用域构造，throw 触发栈展开，析构按 c->b->a 逆序进行——与
  "对象离开作用域即析构"完全一致，且跨越 main->f 栈帧，证明该机制是作用域级的通用保证。
reproduce: 见 command 两行，无外部依赖
---

## 为什么这个证据可信

1. **多层对象、跨栈帧**：对象分布在 f() 的栈帧，异常在 f() 内抛出、在 main 捕获，析构仍按逆序完成——
   证明 RAII 清理不依赖"谁捕获异常"，只依赖"对象离开作用域"。
2. **与 EV-MEM-009 互证**：EV-MEM-009 证"异常路径析构被调用（不泄漏）"，本卡证"多个对象按逆序析构
   （清理顺序确定）"——二者合起来覆盖 RAII 机制的两个关键性质（会被调用 + 顺序确定）。
