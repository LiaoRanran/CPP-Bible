---
id: EV-MEM-005
serves: [ATOM-MEM-RVREF-001]     # 版本边界专用卡：与 EV-MEM-004 分工（004 讲论断，005 讲边界）
status: example
kind: run
hypothesis: >-
  `return x;`（x 是 `T&&` 形参）触发拷贝还是移动**随标准版本变化**：C++17 及更早是拷贝，
  **C++20 起（P0527R1 / P1825R0 把右值引用形参纳入 return 的隐式移动）是移动**。
  故"返回形参必须写 std::move"是**前 C++20** 的处方。
controlled_vars: 唯一变量 = `return x;` vs `return std::move(x);`；标准档是**分层变量**（非受控）
# 五档实测（2026-09-11，红队第 2 轮 S2-1 处置：原"三档"口径过期）：本卡的"档位"就是
# **分层变量**，c++11/14/17 与 c++20/23 结果不同，详见 `actual` 与正文表格。
matrix:
  compiler: [GCC 15.3.0]
  std: [c++11, c++14, c++17, c++20, c++23]
  opt: [-O2]
  arch: [x86-64]
fixture: Examples/_atom_rvref_return.cpp
command: |          # 主档取 **c++23**：复算契约是「一条 command 的 stdout ↔ expected」
  g++ -std=c++23 -O2 Examples/_atom_rvref_return.cpp -o build/_rvref_return.exe && ./build/_rvref_return.exe
  g++ -std=c++23 -O2 -S -masm=intel Examples/_atom_rvref_return.cpp -o Examples/_atom_rvref_return.asm
artifact: Examples/_atom_rvref_return.asm
artifact_sha256: 2a834e60d6a2a738512f8e08d8a9d1f898fb19d591a2dc8ee0baf80a7c8f57ed
# ⚠️ 工件必须与 **command 里的标准档**同代：初版用 c++17 生成了 asm，而 command 是 c++23
# → replay 重生成后字节不同 → refute:sha256_mismatch（实测教训：**生成工件时的档位要和
# command 一致**，别顺手用别的档）。
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains, text: "_ZN5Probe6copiesE"}     # 计数器符号（Itanium ABI；MSVC 见 M2 §2 永久边界）
# 本卡三档结果**故意不一致**（这正是要记录的版本边界事实）→ 必须显式指明 command 对应哪档，
# 否则 replay 判 `refute:ambiguous_expected`（实测：2026-09-10 首次提交即被拦，工具行为正确）。
expected_key: run_GCC15.3_O2_cxx23
expected:
  run: "ret_plain copy=0 move=1 / ret_moved copy=0 move=1"
actual:
  # ⚠️ 本卡的 actual **故意不一致**：五档分两组结果，这正是本卡要记录的**版本边界**事实。
  # 主档（c++23，command 用的那档）与 expected 一致；另四档为人工实测留痕。
  run_GCC15.3_O2_cxx11: "ret_plain copy=1 move=0 / ret_moved copy=0 move=1"   # ← 拷贝（隐式移动尚未引入）
  run_GCC15.3_O2_cxx14: "ret_plain copy=1 move=0 / ret_moved copy=0 move=1"   # ← 拷贝（同上）
  run_GCC15.3_O2_cxx17: "ret_plain copy=1 move=0 / ret_moved copy=0 move=1"   # ← 拷贝！旧规则
  run_GCC15.3_O2_cxx20: "ret_plain copy=0 move=1 / ret_moved copy=0 move=1"   # ← 隐式移动已生效
  run_GCC15.3_O0_cxx20: "ret_plain copy=0 move=1 / ret_moved copy=0 move=1"   # ← 与优化档无关（红队 B4）
  run_GCC15.3_O2_cxx23: "ret_plain copy=0 move=1 / ret_moved copy=0 move=1"
verdict: confirm
falsification: >-
  若五档都输出 `ret_plain copy=1 move=0`（或都为 `copy=0 move=1`），则"版本边界"不成立，
  本卡作废。实测 c++17 与 c++20/23 **不同** → 边界真实存在。
  另：若 `ret_moved` 在任何一档出现 `copy=1`，说明 std::move 没生效 → 实验无区分力。
depth_layer: compiler
drill_note: >-
  标准依据（[expr.prim.id.unqual]）：*implicitly movable entity* 是"自动存储期的非 volatile
  对象，**或右值引用**"；其 id-expression 若作为 `return` 的操作数则 **move-eligible** → 按
  xvalue 处理。C++20 起右值引用形参被纳入该集合，故 `return x;` 隐式移动。
reproduce: 见 command 两行；换 `-std=` 即可复现三档差异
---

## 这条边界为什么重要

红队审查时指出：原子草稿里"返回形参要写 `std::move`"是**前 C++20** 的规则。
与其凭印象改，不如三档实测——**能实测的不口头声称**。结果：

| 标准档 | `return x;`（x 是 T&& 形参） | `return std::move(x);` |
|---|---|---|
| c++11 / c++14 | `copy=1 move=0` → **拷贝** | `copy=0 move=1` |
| c++17 | `copy=1 move=0` → **拷贝** | `copy=0 move=1` |
| **c++20** | `copy=0 move=1` → **已隐式移动** | `copy=0 move=1`（冗余但无害） |
| c++23 | `copy=0 move=1` | `copy=0 move=1` |

（另实测 c++20 × -O0 同为移动——隐式移动与优化档无关，2026-09-11 补测。）

**结论**：写 `std::move` 在 C++20 起**不是必需的**（也不算错，只是冗余）；但在 C++17 及更早
**必需**——不写就是一次静默拷贝。跨版本代码库里这条差异最容易埋雷。

## 与 EV-MEM-004 的分工

- `EV-MEM-004`：主体论断（形参在函数体内是左值）——**与版本无关**，五档一致。
- 本卡：**返回语句**这个特定场景——**与版本有关**，c++17 vs c++20 分界。

主体论断不受本卡影响：`void f(Probe&& x){ Probe y = x; }` 在**所有档**都是拷贝
（EV-MEM-004 已在 c++17 与 c++23 两档实测，一致）。

## 待补

- Clang / MSVC 两列（尤其 MSVC 对 P0527R1 的实现时机可能不同）。
  （c++11 / c++14 两档已于 2026-09-11 实测完毕并录入 `actual`，红队 S2-1 指出的
  "卡内自相矛盾"即此处未同步——已清除。）
