---
id: EV-MEM-025
serves: [ATOM-MEM-RAII-002]
kind: run
hypothesis: >-
  Rule of Five 的 noexcept 细节：vector 扩容搬迁既有元素用 move_if_noexcept——移动构造标了
  noexcept 才用移动（搬迁 copies=0 moves=4）；写了移动构造但漏标 noexcept，搬迁退化为逐个拷贝
  （copies=4 moves=0）。两类型唯一差异是 noexcept 标注，性能损失静默发生、编译器不告警。
controlled_vars: 同一 vector 扩容方式（resize(4) + reserve(64) 搬迁 4 元素）、同一编译器；唯一变量 = 移动构造是否 noexcept
matrix:
  compiler: [GCC 15.3.0]
  # Clang 列待 CI Cross-check 步回填（GCC 15.3.0 已实测）
  std: [c++23]
  opt: [-O0, -O2]
  arch: [x86-64]
fixture: Examples/_atom_rule_five_noexcept.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/_atom_rule_five_noexcept.cpp -o Examples/_atom_rule_five_noexcept.asm
  g++ -std=c++23 -O2 Examples/_atom_rule_five_noexcept.cpp -o build/_replay_rfn.exe && ./build/_replay_rfn.exe
artifact: Examples/_atom_rule_five_noexcept.asm
artifact_sha256: 4e6266ec32b5874fbc4d788a97ed787c646d96645a91c6845183e72c34a07232
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains, text: "relocation"}    # 搬迁观测字符串进入工件
expected:
  run: noexcept move 组搬迁 copies=0 moves=4；throwing move 组搬迁 copies=4 moves=0
  asm: 两组观测点字符串进入工件（双组对照真实存在）
actual:
  run_cxx23_O2: "noexcept move: relocation copies=0 moves=4|throwing move: relocation copies=4 moves=0"
  run_cxx23_O0: "noexcept move: relocation copies=0 moves=4|throwing move: relocation copies=4 moves=0"
verdict: confirm
falsification: >-
  ① 若 noexcept 与否不影响搬迁方式（-O2 下两组都是 moves=4 或都是 copies=4），则 move_if_noexcept
  语义被推翻——实测 -O2 下 noexcept 组 moves=4、throwing 组 copies=4，二者不同；② 若 throwing 组
  仍被移动（move_if_noexcept 失效），第 2 行 moves 应为 4——实测 moves=0。均不成立 => 经受住证伪。
depth_layer: runtime
drill_note: >-
  move_if_noexcept（[class.copy.elision]/库强异常保证）：扩容搬迁若用移动且移动中途抛异常，已搬走
  的元素无法回滚 → 强保证破坏；故标准库只在 is_nothrow_move_constructible（或不可拷贝）时用移动。
  -O0/-O2 双跑输出逐字一致（run_cxx23_O0/O2 同串）：noexcept 组搬迁 copies=0 moves=4、throwing 组
  copies=4 moves=0 与优化档无关——判定发生在库的类型分派（is_nothrow_move_constructible），不是
  优化器行为；replay 机器口径为 -O2（沿 EV-MEM-008 先例）。
reproduce: 见 command 两行，无外部依赖
---

## 为什么这个证据可信

1. **唯一变量对照**：Noex 与 Throwing 五件套相同、仅移动构造差一个 `noexcept` 关键字，同 TU 同
   扩容方式——copies/moves 两组数字（0/4 vs 4/0）把"noexcept 决定搬迁方式"钉死。
2. **-O0/-O2 双跑一致**：两档输出逐字相同（判定发生在库的类型分派层，与优化档无关）；volatile
   计数 + 拆写复合赋值，排除 -O2 常量折叠（EV-MEM-002 教训的针对性防护）。
3. **与 vector 真实路径一致**：扩容搬迁走 std::move_if_noexcept（库实现），计数差异是标准强异常
   保证的可观测结果，不是本卡自造的构造函数选择。

## 边界诚实说明

- moves/copies 的具体次数依赖"搬迁 4 元素 + reserve(64)"这一固定扩容场景；其他容量策略下次数不同
  但**方向**（noexcept→移动、throwing→拷贝）由标准保证。Clang 列由 CI Cross-check 回填。
