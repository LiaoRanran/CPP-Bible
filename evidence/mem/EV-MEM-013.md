---
id: EV-MEM-013
serves: [ATOM-MEM-SHARED-001]
kind: run
hypothesis: >-
  std::shared_ptr 用引用计数实现共享所有权：拷贝 +1、析构 -1；计数归零时资源才释放（析构恰好一次）。
  控制块（RAII）管理计数与资源，使"共享"与"自动释放"可兼得。
controlled_vars: 同一 Box 类型、同一编译器、同一 -O2；唯一变量 = 持有 shared_ptr 的个数（make / copy / 作用域进出）
matrix:
  compiler: [GCC 15.3.0]
  # Clang 列待 CI Cross-check 步回填（GCC 15.3.0 已实测）
  std: [c++23]
  opt: [-O2]
  arch: [x86-64]
fixture: Examples/atoms/_atom_shared_count.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/atoms/_atom_shared_count.cpp -o Examples/atoms/_atom_shared_count.asm
  g++ -std=c++23 -O2 Examples/atoms/_atom_shared_count.cpp -o build/_replay_scnt.exe && ./build/_replay_scnt.exe
artifact: Examples/atoms/_atom_shared_count.asm
artifact_sha256: 323623959ff3114bda64896bd95f6ccb94326123adca0189e0127282473c594e
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains, text: "destroyed"}    # "box destroyed count=" 进入工件（归零才释放可观测）
expected:
  run: use_count 随拷贝 +1、作用域退出 -1；最终归零，Box 析构恰好一次（destroyed count=1）
  asm: 析构路径真实存在（"destroyed" 字符串进入工件）
actual:
  run_cxx23_O2: "use_count after make=1|use_count after copy=2|use_count in scope=3|use_count after scope=2|box destroyed count=1"
verdict: confirm
falsification: >-
  若拷贝后 use_count 不 +1、或析构后不 -1、或计数归零却未释放（destroyed count != 1），则"引用计数共享所有权"
  被推翻 => refute。实测 use_count 1->2->3->2 且最终 destroyed count=1 => 经受住证伪。
depth_layer: runtime
drill_note: >-
  引用计数在控制块中（[util.smartptr.shared]），拷贝/析构改计数；volatile g_destroy 把"归零才释放"
  变成可比对输出。这与 UNIQUE-001 的"移动转移、析构一次"对照：unique 是转移、shared 是计数。
reproduce: 见 command 两行，无外部依赖
---

## 为什么这个证据可信

1. **计数全程可观测**：make/copy/作用域进出四处 `use_count` 输出，单调对应 +1/-1，无跳变。
2. **释放由"归零"定义**：`destroyed count=1` 证明释放只发生在最后一个所有者离开时，不是"每个析构都释放"
   （那是 unique_ptr 的语义，会双释放）。
3. **与 UNIQUE-001 自洽**：shared 把"所有权"从单点变成计数，代价是控制块开销（见本原子 claim 的权衡）。
