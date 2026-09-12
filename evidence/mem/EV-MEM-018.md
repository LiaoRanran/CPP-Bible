---
id: EV-MEM-018
serves: [ATOM-MEM-NEW-001]
kind: run
hypothesis: >-
  new[] 与 delete[] 必须配对（new[] 调 operator new[] 一次、delete[] 调 operator delete[] 一次）；
  nothrow 版本在分配失败时返回 nullptr 而非抛 std::bad_alloc。内置类型数组不初始化（读取是 UB，故不读）。
controlled_vars: 同一 int 数组、同一编译器、同一 -O2；唯一变量 = 用 new[]/delete[] 还是 new(std::nothrow)
matrix:
  compiler: [GCC 15.3.0]
  # Clang 列待 CI Cross-check 步回填（GCC 15.3.0 已实测）
  std: [c++23]
  opt: [-O2]
  arch: [x86-64]
fixture: Examples/atoms/_atom_new_array.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/atoms/_atom_new_array.cpp -o Examples/atoms/_atom_new_array.asm
  g++ -std=c++23 -O2 Examples/atoms/_atom_new_array.cpp -o build/_replay_narr.exe && ./build/_replay_narr.exe
artifact: Examples/atoms/_atom_new_array.asm
artifact_sha256: 360a35729ac710c564df754bfa1fbda73089efaaf5848547be9b15f81f1241d5
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains_any, texts: ["_Znay", "_Znam"]}  # operator new[] 进入工件：MinGW 标 _Znay、GCC14 标 _Znam，任一即证数组分配层真实存在
expected:
  run: new[] 调一次、delete[] 调一次（配对）；nothrow 大分配失败返回 null=1
  asm: operator new[] 调用点真实存在（MinGW 归 _Znay / Linux GCC 归 _Znam，断言语义相同）
actual:
  run_cxx23_O2: "array new[] calls=1|array delete[] calls=1|nothrow huge returned null=1"
verdict: confirm
falsification: >-
  证伪"new[] 与 delete 混用安全"：若 new[] 配 delete（非 delete[]）能正常释放，则"必须配对"被推翻——
  实测若混用会 UB（未在本卡运行，留作证伪条件文本；本卡证明正确配对时 new[]/delete[] 各一次）。
  证伪"nothrow 抛异常"：若 nothrow 大分配抛异常而非返回 null，则 refute；实测返回 null=1 => nothrow 不抛。
depth_layer: runtime
drill_note: >-
  new[] 调 operator new[]（数组尺寸含 Cookie），delete[] 调 operator delete[]；两者必须配对，混用是 UB。
  nothrow 在分配失败返回 nullptr（不抛），是"失败不想异常"场景的写法。内置类型数组不初始化是语言规定
  （需手动赋值或用值初始化 `new int[10]()`）。
reproduce: 见 command 两行，无外部依赖
---

## 为什么这个证据可信

1. **配对可数**：new[]/delete[] 各触发一次 operator new[]/delete[]（volatile 计数），证明"数组分配是独立一层"。
2. **nothrow 行为实测**：约 400GB 分配必然失败，nothrow 返回 null=1（不抛异常）——直接区分 new 与 new(nothrow)。
3. **与 RAII-001 衔接**：裸 new[]/delete[] 一旦漏写 delete[] 即泄漏（EV-MEM-009 的裸路径同构），故优先容器/智能指针。

## 修订记录

- **2026-09-11 · gcc-14 兼容性修复（A 方向，verified 状态保留）**
  同 EV-MEM-008：`contains "_Znay"` 在 Linux GCC 上不命中（`size_t` 宽度差异 ⇒ `_Znam`）。
  实测：`_Znam` 在 g++-14.2 / g++-13.3 工件中均出现 5 次，`_Znay` 0 次 ⇒
  断言改 `contains_any ["_Znay", "_Znam"]`。claim 与 run_match 未变，`artifact_sha256` 未变。
