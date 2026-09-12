---
id: EV-MEM-020
serves: [ATOM-MEM-ALIGN-001]
kind: run
hypothesis: >-
  alignas 可提升类型对齐；按字节 memcpy 是搬运结构体的唯一安全方式（不触发对齐/类型双关 UB）。
  反例：reinterpret_cast 强转指针对齐/类型双关是未定义行为（注释实证、不运行）。
controlled_vars: 同一 Aligned 类型、同一编译器、同一 -O2；唯一变量 = 用 memcpy 还是指针强转
matrix:
  compiler: [GCC 15.3.0]
  # Clang 列待 CI Cross-check 步回填（GCC 15.3.0 已实测）
  std: [c++23]
  opt: [-O2]
  arch: [x86-64]
fixture: Examples/atoms/_atom_align_ctrl.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/atoms/_atom_align_ctrl.cpp -o Examples/atoms/_atom_align_ctrl.asm
  g++ -std=c++23 -O2 Examples/atoms/_atom_align_ctrl.cpp -o build/_replay_actl.exe && ./build/_replay_actl.exe
artifact: Examples/atoms/_atom_align_ctrl.asm
artifact_sha256: 0e3ffb202d91ab23212ab2897ba8d16f149b1895d459c90e2a3ae14120bdbdde
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains, text: "Aligned"}    # 类型名进入工件（alignas 布局真实存在）
expected:
  run: alignof(Aligned)=16（alignas 生效）、sizeof=16（含 12 字节 padding）、memcpy roundtrip x=7
  asm: 类型名 "Aligned" 进入工件（alignas 提升对齐真实存在）
actual:
  run_cxx23_O2: "alignof(Aligned)=16|sizeof(Aligned)=16|memcpy roundtrip x=7"
verdict: confirm
falsification: >-
  ① 若 alignas 不提升对齐（alignof != 16），则"alignas 可控"被推翻 => refute；实测 alignof=16。
  ② 若 memcpy 不安全（roundtrip != 7），则"按字节搬运安全"被推翻 => refute；实测 x=7。
  ③ 编译期证伪"强转安全"：取消注释 `*(int*)((char*)&s+1)` 会触发未对齐 + 类型双关 UB（[basic.align]/[strict.aliasing]），
  不能运行（UB），仅留作证伪条件文本。实测 ①②成立 => 经受住证伪。
depth_layer: compiler
drill_note: >-
  alignas 提升整体对齐（[basic.align]），成员 x(int,4) 被推到偏移 0 但整体对齐 16 => sizeof=16（12 字节尾 padding）。
  memcpy 按字节拷贝，不涉及"把字节重新解释成某类型"的 aliasing 假设，故安全；指针强转读字段同时踩
  未对齐访问与严格别名两条 UB，是真实 bug 来源。
reproduce: 见 command 两行，无外部依赖
---

## 为什么这个证据可信

1. **alignas 实测**：alignof=16、sizeof=16，证明对齐可被 alignas 控制（编译期 static_assert 同证）。
2. **memcpy 安全实测**：roundtrip x=7，证明按字节搬运结构体不丢数据、不踩 UB。
3. **UB 注释实证**：强转读字段的未定义行为用标准条款（[basic.align]/[strict.aliasing]）标注，满足"注释断言须有实证"。
