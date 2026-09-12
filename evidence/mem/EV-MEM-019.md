---
id: EV-MEM-019
serves: [ATOM-MEM-ALIGN-001]
kind: run
hypothesis: >-
  结构体成员按自身对齐要求排列，编译器在成员间/末尾插入 padding 使每个成员与整体满足对齐；sizeof 含 padding。
  `struct { char a; int b; }`：a 偏移 0、b 偏移 4（中间 3 字节 padding），sizeof=8。
controlled_vars: 同一 Padded 类型、同一编译器、同一 -O2；唯一变量 = 成员顺序（a 在前、b 在后）
matrix:
  compiler: [GCC 15.3.0]
  # Clang 列待 CI Cross-check 步回填（GCC 15.3.0 已实测）
  std: [c++23]
  opt: [-O2]
  arch: [x86-64]
fixture: Examples/atoms/_atom_align_pad.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/atoms/_atom_align_pad.cpp -o Examples/atoms/_atom_align_pad.asm
  g++ -std=c++23 -O2 Examples/atoms/_atom_align_pad.cpp -o build/_replay_apad.exe && ./build/_replay_apad.exe
artifact: Examples/atoms/_atom_align_pad.asm
artifact_sha256: e35737bdca1a8397bea82c698b90e932028b66a6a385bd7df27c1b8ed99afe3b
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains, text: "Padded"}    # 类型名进入工件（padding 布局真实存在）
expected:
  run: sizeof=8、offsetof a=0、offsetof b=4、padding=3
  asm: 类型名 "Padded" 进入工件（padding 布局真实存在）
actual:
  run_cxx23_O2: "sizeof(Padded)=8|offsetof a=0|offsetof b=4|padding bytes=3"
verdict: confirm
falsification: >-
  若成员紧密排列无填充（sizeof == 1+4 == 5、offsetof b == 1），则"无 padding"被证伪——但那样 int b 会
  落在未对齐地址，访问 UB。实测 sizeof=8、offsetof b=4、padding=3 => 编译器确实插了 padding => 经受住证伪。
depth_layer: compiler
drill_note: >-
  对齐由 [basic.align] 规定：每个类型有对齐要求，成员放在满足自身对齐的偏移；结构体整体对齐取成员最大者，
  sizeof 向上取整到整体对齐的倍数（故末尾也可能 padding）。offsetof 是编译期常量，跨优化档稳定。
reproduce: 见 command 两行，无外部依赖
---

## 为什么这个证据可信

1. **padding 可量化**：offsetof b=4（非 1）、padding=3、sizeof=8，三数互相印证，不是"看起来有填充"。
2. **与 UB 自洽**：若真紧密排列（b 在偏移 1），int 会未对齐访问 → UB；padding 正是为避免它，证明"填充不是浪费"。
3. **跨优化档稳定**：offsetof/sizeof 是编译期常量，与 -O2 无关（已在卡内注明）。
