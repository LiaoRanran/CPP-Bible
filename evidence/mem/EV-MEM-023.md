---
id: EV-MEM-023
serves: [ATOM-MEM-RAII-002]
kind: run
hypothesis: >-
  Rule of Zero：成员全是 RAII 类型（std::unique_ptr）时，零特殊成员函数声明——编译器隐式生成的特殊
  成员函数把正确语义全部做对：移动构造/移动赋值隐式生成（unique_ptr 可移动）、拷贝构造/拷贝赋值被
  隐式**删除**（unique_ptr 不可拷贝）、析构隐式生成且正确（委托给成员析构）。
  运行期：移动转移所有权、资源恰好构造 1 次析构 1 次释放 1 次（零泄漏、零双重析构）。
controlled_vars: 同一 Holder 类型、同一编译器、同一 -O2；唯一变量 = 被触发的特殊成员函数（移动/析构）
matrix:
  compiler: [GCC 15.3.0]
  # Clang 列待 CI Cross-check 步回填（GCC 15.3.0 已实测）
  std: [c++23]
  opt: [-O2]
  arch: [x86-64]
fixture: Examples/atoms/_atom_rule_zero.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/atoms/_atom_rule_zero.cpp -o Examples/atoms/_atom_rule_zero.asm
  g++ -std=c++23 -O2 Examples/atoms/_atom_rule_zero.cpp -o build/_replay_rz.exe && ./build/_replay_rz.exe
artifact: Examples/atoms/_atom_rule_zero.asm
artifact_sha256: 6016c553283a4ef716e8ffd081b50bdf31254b0e7ded878c31b1f8680f917fe8
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains, text: "rule zero"}     # 夹具输出字面量进入工件（观测点真实存在）
  - {kind: contains, text: "owner_changed"}
expected:
  run: 类型系统 move_constructible=1 copy_constructible=0；移动转移所有权 owner_changed=1；allocs=1 dtors=1 frees=1（恰一次，零泄漏）
  asm: 观测点字符串进入工件；unique_ptr 的移动/析构路径真实存在
actual:
  run_cxx23_O2: "rule zero: move_constructible=1 copy_constructible=0 (type system)|move transfer: owner_changed=1|allocs=1 dtors=1 frees=1 (exactly once, no leak)"
  run_cxx23_O0: "rule zero: move_constructible=1 copy_constructible=0 (type system)|move transfer: owner_changed=1|allocs=1 dtors=1 frees=1 (exactly once, no leak)"
verdict: confirm
falsification: >-
  ① 若"零声明"导致拷贝仍可用（is_copy_constructible 为 true），对应 static_assert 编译红——但那样
  unique_ptr 的独占语义就被破坏，违反库设计；② 若移动不转移所有权（owner_changed=0）或析构不是
  恰好 1 次（dtors≠1 或 frees≠1，泄漏/双重析构），运行计数即 refute。实测全部成立 => 经受住证伪。
depth_layer: runtime
drill_note: >-
  隐式规则链（[class.copy.ctor]/[class.dtor]）：用户零声明 ⇒ 全部隐式生成/删除由成员形状决定——
  unique_ptr 可移动 ⇒ 移动成员隐式生成；不可拷贝 ⇒ 拷贝成员被删除；成员析构在 Holder 析构体内
  逐成员调用 ⇒ Resource 恰好一次构造一次析构。这正是 Rule of Zero 的安全性来源：**正确性由成员
  类型组合保证，而非程序员记忆**。类型系统论证 + 运行计数双重观测。
reproduce: 见 command 两行，无外部依赖
---

## 为什么这个证据可信

1. **类型系统硬证明**：move/copy 的可用性由 5 条 static_assert 强制——"隐式规则做对了什么"不是
   文字描述，而是编译期可判定的命题。
2. **运行期恰一次观测**：allocs=1 / dtors=1 / frees=1 三数互证——不泄漏（dtors==allocs）也不双重
   析构（dtors==1 恰等于资源数）。
3. **与 EV-MEM-024 构成对照对**：本卡（Rule of Zero）与违反 Rule of Three 的卡共用同一套计数纪律
   （operator new/delete 重载 + volatile 计数），唯一变量是"是否手写拷贝/析构"——对照有区分力。

## 边界诚实说明

- "拷贝被删除"是**成员形状**（unique_ptr 不可拷贝）驱动的隐式结果；若成员换成可拷贝 RAII 类型
  （如 std::string），拷贝会隐式生成且语义正确——Rule of Zero 的普适性正源于此，卡内正文展开。
- -O0/-O2 双跑输出逐字一致（run_cxx23_O0/O2 同串）；replay 机器口径为 -O2（沿 EV-MEM-008 先例）。
