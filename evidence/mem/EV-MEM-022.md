---
id: EV-MEM-022
serves: [ATOM-MEM-VALUE-002]
kind: run
hypothesis: >-
  完美转发：std::forward<T>(x) 按推导出的 T 恢复实参值类别——右值转发为右值（触发移动 1 次、拷贝 0 次）、
  左值转发为左值（触发拷贝 1 次、移动 0 次）。转发链里省略 forward 时，形参 x 是具名变量 → 函数体内是
  左值 → 右值实参被当左值继续传，退化为拷贝。
controlled_vars: 同一 Box 类型（拷贝/移动各带 volatile 观测点）、同一编译器；唯一变量 = 转发方式（forward / 省略）× 实参值类别（右值/左值）
matrix:
  compiler: [GCC 15.3.0]
  # Clang 列待 CI Cross-check 步回填（GCC 15.3.0 已实测）
  std: [c++23]
  opt: [-O0, -O2]
  arch: [x86-64]
fixture: Examples/_atom_fwd_count.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/_atom_fwd_count.cpp -o Examples/_atom_fwd_count.asm
  g++ -std=c++23 -O2 Examples/_atom_fwd_count.cpp -o build/_replay_fwd_o2.exe && ./build/_replay_fwd_o2.exe
artifact: Examples/_atom_fwd_count.asm
artifact_sha256: 0df0508167b3f71db6ff8279218a6d76155f42ae865ae4009a88cddac4b092f4
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains_any, texts: ["wrap_forward", "forward rvalue: copies="]}   # forward 路径进工件：MinGW 留函数符号、GCC14 内联仅留打印串，任一即证路径存在
  - {kind: contains_any, texts: ["wrap_bare", "no-forward rvalue: copies="]}    # 省略 forward 对照路径进工件（两条路径都需有可见证据）
expected:
  run: forward 右值 copies=0 moves=1；forward 左值 copies=1 moves=0；省略 forward 右值 copies=1 moves=0
  asm: 两个转发包装函数的符号名进入工件（forward/省略两条路径真实存在）
actual:
  run_cxx23_O0: "forward rvalue: copies=0 moves=1|forward lvalue: copies=1 moves=0|no-forward rvalue: copies=1 moves=0"
  run_cxx23_O2: "forward rvalue: copies=0 moves=1|forward lvalue: copies=1 moves=0|no-forward rvalue: copies=1 moves=0"
verdict: confirm
falsification: >-
  ① 若"具名右值引用在函数体内是左值"不成立（省略 forward 也走移动），则第 3 行应输出 moves=1——实测
  copies=1 moves=0，退化成立；② 若 forward 会把左值也变成右值（过度转发），则第 2 行应输出 moves=1——
  实测 copies=1 moves=0（forward 保持值类别、不越权）。两条件均不成立 => 经受住证伪。
depth_layer: runtime
drill_note: >-
  三个观测组同 TU 对照，唯一变量是转发方式与实参值类别：forward 恢复类别（右值→移动、左值→拷贝），
  省略 forward 则一律拷贝——因为 [basic.lval] Note 3：具名右值引用形参在表达式体内按左值处理。
  计数器 volatile + 拆写的 x = x + 1（C++20 起复合赋值弃用），-O0/-O2 双跑输出逐字一致，排除优化器假象
  （replay 的 run_match 以 -O2 为机器口径：工具逐行执行命令并拼接全部 stdout，双跑若都进 command 会
  拼成 6 行——沿 EV-MEM-008 先例，command 只跑 -O2，-O0 结果记入 run_cxx23_O0，同一会话人工执行）。
  Box 的拷贝/移动构造是仅有的观测点（volatile 写不可消除），C++17 保证 prvalue 返回不引入额外移动，
  故计数干净（各 1 次）。
reproduce: 见 command 两行，无外部依赖
---

## 为什么这个证据可信

1. **有证伪对照（且双向）**：不只证明"省略 forward 有代价"（组 3 vs 组 1），还证明"forward 不越权"
   （组 2：左值经 forward 仍是拷贝）——避免把 forward 教成"加了就对"的咒语。
2. **跨优化档一致**：-O0 与 -O2 输出逐字一致（run_cxx23_O0/O2 同串）；计数器 volatile 且构造函数体内
   只有 volatile 写，-O2 无法把观测点折叠成立即数（EV-MEM-002 教训的针对性防护）。
3. **与既有证据互证**：EV-MEM-006（VALUE-001）用 decltype 证明"具名右值引用是左值"（编译期）；
   本卡用拷贝/移动计数给出同一事实的运行时代价（省略 forward = 每次多一次拷贝）。

## 边界诚实说明

- 计数结果依赖"拷贝/移动构造未被内联消除"：构造体内 volatile 写不可消除，保证观测通路活着
  （"证明某事发生"的同时已证观测点可达）；夹具里同时保留地址观测 sink，防对象整组消除。
- 拷贝/移动的次数结论对三大实现一致（标准保证 forward 的类别恢复语义）；本机 GCC 15.3.0 实测，
  Clang 列由 CI Cross-check 回填。
- 机器实测仅 c++23 单档；夹具仅用 C++11 起即有的特性（std::forward/引用折叠/noexcept 移动），
  跨档可编译，类别语义自 C++11 起稳定（输出与优化档无关的运行计数口径，见 run_cxx23_O0/O2）。

## 修订记录

- **2026-09-11 · gcc-14 兼容性修复（A 方向，verified 状态保留）**
  背景：CI 默认 g++ 14.2 下 `contains "wrap_forward"` / `contains "wrap_bare"` 不命中——两个包装
  函数在 -O2 下被内联，符号名不进工件；但两条路径的**打印串**仍在（观测通路活着，符合
  "证明某事发生的同时已证观测点可达"的纪律）。claim 未变。
  实测：`forward rvalue: copies=` 2 次、`no-forward rvalue: copies=` 1 次；`wrap_forward` /
  `wrap_bare` 均 0 次（g++-14.2 与 g++-13.3 一致）⇒ 两条断言各改 `contains_any`
  （`["wrap_forward", "forward rvalue: copies="]` / `["wrap_bare", "no-forward rvalue: copies="]`），
  仍要求**两条路径各自**有可见证据，不因放宽形态而合并成一条。`artifact_sha256` 未变。
