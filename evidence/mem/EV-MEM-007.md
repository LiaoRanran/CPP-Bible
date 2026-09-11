---
id: EV-MEM-007
serves: [ATOM-MEM-VALUE-001]
kind: run
hypothesis: >-
  xvalue 有身份（指代特定对象 x），prvalue 没有身份（不指代任何命名对象）。若 std::move(x) 真是 prvalue
  （即"x 的一份临时副本"），则从它移动不应改动 x；实测移动后 x 被改动 => std::move(x) 指代真实对象 x
  => 它是 xvalue，不是 prvalue。
controlled_vars: 同一 Box 类型、同一编译器、同一 -O2；唯一变量 = 移动来源是 xvalue(std::move(a)) 还是 prvalue(临时)
matrix:
  compiler: [GCC 15.3.0]
  std: [c++23]
  opt: [-O2]
  arch: [x86-64]
fixture: Examples/_atom_value_xvalue.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/_atom_value_xvalue.cpp -o Examples/_atom_value_xvalue.asm
  g++ -std=c++23 -O2 Examples/_atom_value_xvalue.cpp -o build/_replay_xv.exe && ./build/_replay_xv.exe
artifact: Examples/_atom_value_xvalue.asm
artifact_sha256: 988f921283b0be3977df0ca79baed518ca5d55c9e0b1db5e7b40856b74fa7006
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains, text: "xvalue"}
expected:
  run: 2 行——从 xvalue(std::move(a)) 移动后源 a.v = -1（证明 xvalue 指代真实对象 a）；b.v/c.v 均为 7
  asm: 移动构造把源置 -1 的副作用进入工件（xvalue 身份可观测）
actual:
  run_cxx23_O2: "after move from xvalue(std::move(a)): source a.v = -1|b.v = 7  c.v = 7"
verdict: confirm
falsification: >-
  证伪"std::move 产生 prvalue"：若 move 结果是 prvalue（临时副本），则 Box b = std::move(a) 的移动构造
  应作用于临时、不动 a，输出 a.v 仍为 7。实测 a.v = -1 => 移动作用于真实对象 a => 表达式是 xvalue。
  反例边界：若把夹具里 `Box b = std::move(a);` 改成 `Box b = a;`（拷贝），则 a.v 保持 7 —— 恰说明
  "改动 a"是移动构造（xvalue 触发）的专属后果，不是任何构造都会发生。
depth_layer: runtime
drill_note: >-
  xvalue 与 prvalue 的机器可观测差异不在"可否取地址"（二者都不能对 `&` 取地址——`&` 要求左值，
  xvalue 虽是 glvalue 但非左值），而在"是否指代一个有身份的既有对象"：移动 xvalue 会改动该对象，
  移动 prvalue 不会。本卡用移动构造置源为 -1 的副作用把"身份"变成运行期可比对输出。
reproduce: 见 command 两行，无外部依赖
---

## 为什么这个证据可信

1. **有证伪对照（且对照本身解释边界）**：把 `std::move(a)` 换成 `a`（拷贝）时 a.v 保持 7，说明
   "a 被改动"是 xvalue 触发移动构造的专属后果；若 move 真是 prvalue，`std::move(a)` 也会像拷贝一样
   不动 a —— 实测相反，故"move 产生 prvalue"被推翻。
2. **术语精确**：明确区分"xvalue 是 glvalue（有身份）"与"`&` 取地址需要左值"——二者不冲突，
   xvalue 有身份但不可直接 `&`。这堵住了"xvalue 能取地址所以和 lvalue 一样"的常见误读。

## 红队已抓的初版错误（留痕）

第一版夹具写成 `int* p = &std::move(x);` 想"证明 xvalue 可取地址"，结果 GCC 直接报
`error: taking address of rvalue [-fpermissive]`——`&` 的 operand 必须是左值，xvalue 不是左值。
这恰恰说明"可否取地址"不是 xvalue/prvalue 的区分点，改用"移动是否改动既有对象"来观测身份，
结论才站得住。
