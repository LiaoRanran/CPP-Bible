---
id: EV-MEM-003
serves: [ATOM-HIST-AUTOPTR-001]   # G4 样板 C 配套证据；人审通过原子化时启用
status: example                    # example：样板配套证据，随样板一并人审
kind: run                          # run（类型系统差异，编译期可判定）
hypothesis: >-
  同一个"所有权转移"的需求，C++98 只能用**拷贝构造**的语法表达（`auto_ptr`），C++11 用
  **移动语义**表达（`unique_ptr`）：前者**语法上是拷贝**（不需 `std::move`，源被静默偷空，
  且连 `CopyConstructible` 都不满足）；后者**语法上必须 `move`**（意图显式，错误用法在编译期被拒）。
controlled_vars: 同一 TU、同一编译器、同一优化档；变量 = 被比较的智能指针类型（auto_ptr vs unique_ptr）
matrix:
  compiler: [GCC 15.3.0]
  # Clang 列待 CI Cross-check 步回填（GCC 15.3.0 已实测）
  std: [c++14]
  opt: [-O2]
  arch: [x86-64]
fixture: Examples/atoms/_atom_auto_ptr.cpp
command: |          # POSIX 语义；产物必须写 build/（仓库源只读）
  # 同一夹具（内含 auto_ptr/unique_ptr 双向 static_assert），故与 EV-HIST-001 共用工件。
  g++ -std=c++14 -Wno-deprecated-declarations -O2 Examples/atoms/_atom_auto_ptr.cpp -o build/_replay_autoptr.exe && ./build/_replay_autoptr.exe
  g++ -std=c++14 -Wno-deprecated-declarations -O2 -S -masm=intel Examples/atoms/_atom_auto_ptr.cpp -o Examples/atoms/_atom_auto_ptr.asm
artifact: Examples/atoms/_atom_auto_ptr.asm
artifact_sha256: b4f993189459e84031d2a6b37f5bf04da88c140c637cb2c37fb7357f6dfdd691
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  # 同 EV-HIST-001：`_ZNSt8auto_ptr` 前缀命中的是**析构**符号（D1）；拷贝构造被 -O2 内联、
  # 无独立符号。断言只锚定符号存在性（与内联决策无关），故跨编译器稳定。
  - {kind: contains, text: "_ZNSt8auto_ptr"}
expected:
  run: 三行观测与 EV-HIST-001 一致；关键对照是第 ②/④ 行的**语法差异**：auto_ptr 直接拷贝即可
       （无需 move），unique_ptr 必须显式 `std::move`。
  compile_time: >-
    `static_assert` 双向锁定——auto_ptr：`is_copy_constructible == false`（拷贝构造收**非 const
    左值引用**，故不满足 `CopyConstructible`）但 `is_constructible<T, T&> == true`（能从非 const
    对象"拷贝"）；unique_ptr：`is_copy_constructible == false` 且 `is_move_constructible == true`。
actual:                      # 逐项实测（2026-09-10）
  run_GCC15.3_cxx14_O2: "auto_ptr 拷贝后源为空=是 目标值=42 | 从容器读元素后源为空=是 偷到值=7 | unique_ptr 移动后源为空=是 目标值=9"
  typediff_GCC15.3_cxx14: "auto_ptr: is_copy_constructible=false / is_constructible<T,T&>=true；unique_ptr: is_copy_constructible=false / is_move_constructible=true（四条 static_assert 全部通过，编译期即判定）"
verdict: confirm
falsification: >-
  若 `static_assert` 任一不成立（例如 auto_ptr 竟满足 `is_copy_constructible`），则"两者设计差异"
  的描述被推翻——**首版正是这样被打回的**：初版断言写成 `is_copy_constructible<auto_ptr> == true`，
  编译直接失败，说明"auto_ptr 是一个可拷贝类型"这个流行说法并不准确（它压根不满足
  `CopyConstructible`，只是**能被非 const 对象拷贝**）。这条修正由编译器当场给出，非人工推演。
depth_layer: compiler
drill_note: >-
  差异落在**类型系统**而非运行时：`unique_ptr` 用 `= delete` 把"拷贝"变成编译错误，从而让
  "我在这里转移所有权"必须写成 `std::move`；`auto_ptr` 没有任何这样的语法提示，
  同一件事伪装成一次普通拷贝——这正是"C++98 缺移动语义"留下的设计扭曲。
reproduce: 见 command 两行（与 EV-HIST-001 共用夹具）
---

## 为什么这个证据可信

1. **编译期判定，零 flake**：四条 `static_assert` 由编译器求值，不依赖运行时状态、不受优化影响；
   任何一条不成立就编译失败（**首版就是这么被当场打回的**）。
2. **两个方向都锁**：不只断言"unique_ptr 不能拷贝"，还断言"auto_ptr 能从不带 const 的对象拷贝"
   ——只写后者会漏掉"它其实不满足 `CopyConstructible`"这一层，而那一层才是容器冲突的根因。
3. **与运行层互证**：编译期差异（能否拷贝）与运行层观测（拷贝后源是否变空）指向同一件事
   ——"转移所有权"这个需求在两代语言里的表达方式不同。

## 这张卡真正要纠正的说法：**auto_ptr 不是"有 bug 的 unique_ptr"**

流行说法是"auto_ptr 有 bug，所以被 unique_ptr 替代"。实测更准确：

- `auto_ptr` **连 `CopyConstructible` 都不满足**（拷贝构造收 `auto_ptr&` 而非 `const auto_ptr&`），
  而容器/算法要求 `CopyConstructible` —— 所以**把 `auto_ptr` 放进容器从标准角度本就不成立**；
- 但在 C++98 语境下它**能工作**（能编译、能转移），只是语义与容器隐含约定冲突；
- C++11 引入移动语义后，同一个需求有了**正确的语法表达**（`unique_ptr` + `= delete` + `std::move`），
  `auto_ptr` 才被弃用（C++11 deprecated → C++17 移除）。

**结论**：这是"**语言特性缺失导致库设计扭曲，语言演化再驱动库重构**"的典型案例，
不是一次库实现失误。

## 待补（人审通过后）

- Clang 列：Linux `clang++` 默认配 **libstdc++**，预期同样可编译并通过断言；由 CI 夹具步骤留痕。
- MSVC 列：按 M2 §2 永久边界以标准条文代替（MSVC 已移除 `auto_ptr`）。
