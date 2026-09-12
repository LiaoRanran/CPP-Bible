---
id: EV-HIST-001
serves: [ATOM-HIST-AUTOPTR-001]   # G4 样板 C 配套证据；人审通过原子化时启用
status: example                    # example：样板配套证据，随样板一并人审
kind: run                          # run（拷贝即转移 + 容器冲突）+ 实现可用性实测
hypothesis: >-
  `std::auto_ptr` 的"拷贝构造"实际语义是**转移所有权**：拷贝后源被清空；因此把元素从容器里
  读/拷出来这一步就会偷空源元素——这与容器"拷贝后两个对象等价"的隐含约定直接冲突。
controlled_vars: >-
  同一 TU、同一编译器、同一优化档；变量 = 标准版本（c++14 / c++17 / c++23，用于测"实现是否仍提供"）
matrix:
  compiler: [GCC 15.3.0]
  std: [c++14, c++17, c++23]
  opt: [-O2]
  arch: [x86-64]
fixture: Examples/atoms/_atom_auto_ptr.cpp
command: |          # POSIX 语义；产物必须写 build/（仓库源只读）
  # 标准自 C++17 起已移除 std::auto_ptr，故钉 -std=c++14（与 C++98 语义语境一致）；
  # deprecation 警告用 -Wno- 静音，但**不掩盖**"它已被弃用"这一事实。
  g++ -std=c++14 -Wno-deprecated-declarations -O2 Examples/atoms/_atom_auto_ptr.cpp -o build/_replay_autoptr.exe && ./build/_replay_autoptr.exe
  g++ -std=c++14 -Wno-deprecated-declarations -O2 -S -masm=intel Examples/atoms/_atom_auto_ptr.cpp -o Examples/atoms/_atom_auto_ptr.asm
artifact: Examples/atoms/_atom_auto_ptr.asm
artifact_sha256: b4f993189459e84031d2a6b37f5bf04da88c140c637cb2c37fb7357f6dfdd691
# 2026-09-10 重生成：旧值 76440eef… 是"尚未加 unique_ptr 移动对照"的版本（见 actual 第三行）。
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:            # 跨编译器可移植的结构断言（身份不匹配时的替代校验）
  # auto_ptr **实例化出的成员函数符号**（析构 `_ZNSt8auto_ptrIiED1Ev.isra.0`，D1=destructor）。
  # 注意：**拷贝构造没有独立符号**——-O2 把它内联进了 main（人审指出，2026-09-10 核正）；
  # 该断言只锚定"符号存在"，与调用次数/内联决策无关，故跨编译器稳定（MinGW / Linux 均实测通过）。
  - {kind: contains, text: "_ZNSt8auto_ptr"}
expected:
  run: >-
    `auto_ptr 拷贝后源为空=是`（拷贝即转移）；`从容器读元素后源为空=是`（容器语义冲突）；
    `unique_ptr 移动后源为空=是`（对照：同一效果，但必须显式 `std::move`）。
    三项都是确定性观测，不依赖 UB。
  asm: >-
    工件含 auto_ptr 实例化出的成员函数符号（`_ZNSt8auto_ptr` 前缀）——**具体是析构**
    `_ZNSt8auto_ptrIiED1Ev.isra.0`（`D1` = destructor；`.isra.0` 是 GCC 常量传播生成的克隆），
    并在汇编中被 `call` 多次（每个 auto_ptr 生命周期结束都要析构）。
    **拷贝构造没有独立符号**：`-O2` 把它内联进 `main` 了——所以"转移"在汇编层的可见形态
    是"源指针被写成 0"，而不是一次 `call`（与样板 A/B 同型的教训：**别预设汇编里应该有什么**）。
actual:                      # 逐项实测（2026-09-10）
  run_GCC15.3_cxx14_O2: "auto_ptr 拷贝后源为空=是 目标值=42 | 从容器读元素后源为空=是 偷到值=7 | unique_ptr 移动后源为空=是 目标值=9"
  # ↓ 实现事实（非 run_*，不参与 run_match）：标准移除 ≠ 实现删除
  impl_GCC15.3_cxx14: "同夹具可编译、运行输出如上"
  impl_GCC15.3_cxx17: "-std=c++17 下**仍可编译**（rc=0）——libstdc++ 保留了已从标准移除的 auto_ptr"
  impl_GCC15.3_cxx23: "-std=c++23 下**仍可编译**（rc=0）"
  impl_Clang18.1.3_CI: "CI（Ubuntu, clang 18.1.3, 默认 libstdc++）：编译通过、四条 static_assert 全过、三行运行输出与 GCC 逐字一致（notice 注解留痕）"
verdict: confirm
falsification: >-
  若拷贝后源**未**被清空（`a.get() != nullptr`），则"拷贝即转移"被推翻；若从容器读出元素后
  源元素仍存活，则"与容器语义冲突"被推翻。两项实测均按预期发生，故 confirm。
depth_layer: runtime
drill_note: >-
  "拷贝即转移"的后果是**运行期数据丢失**（源指针被置空），且没有任何编译期拦阻——
  这正是它与 `unique_ptr` 的本质差别（见 EV-MEM-003：后者把错误用法变成编译错误）。
reproduce: 见 command 两行；三档标准版本可用性用同一最小夹具换 `-std=` 复测
---

## 为什么这个证据可信

1. **确定性观测，不依赖 UB**：`a.get() == nullptr` 与 `v[0].get() == nullptr` 都是"转移是否发生"
   的直接读出，不需要触发排序内部的未指定拷贝次数（那会引入 UB，反而无法作为 expected）。
2. **两项观测互为补充**：① 单个对象上"拷贝 = 偷"；② 容器场景下同一个语义导致**源元素丢失**——
   后者才是当年真实事故的形态（算法内部拷贝元素 → 元素在排序/遍历过程中互相偷空）。
3. **实现可用性另测三档**（`impl_*`）：确认 GCC 15.3 即使在 `-std=c++23` 下仍提供 `auto_ptr`。

## 一个必须记下的实现事实：**标准移除 ≠ 实现删除**

实测（同一最小夹具换 `-std=`）：GCC 15.3 的 **libstdc++ 在 c++14 / c++17 / c++23 三档下都能编译
`std::auto_ptr`**（rc 均为 0），尽管标准自 C++17 起已把它移除。

- 原因：libstdc++ 通过 `<backward/auto_ptr.h>` 保留了向后兼容；而 **libc++ / MSVC 已移除**。
- 教学价值：这构成一个**可移植性陷阱**——在 GCC 上"看起来还能用"的老代码，换工具链就断。
- 引用纪律：本卡因此**不写"C++17 下会编译失败"**（实测不成立），只写"标准自 C++17 移除；
  GCC 15.3 实现仍保留（实测），libc++/MSVC 已移除"。

## 边界与待补

- **Clang 列已实测**（CI `Cross-check Matrix` 步，notice 注解公开可读）：clang 18.1.3 + libstdc++
  下编译通过、四条 `static_assert` 全过、运行输出与 GCC **逐字一致** → 满足 M2 §2 双编译器边界，
  **无需豁免票**。
- **MSVC 列**：MSVC 已移除 `auto_ptr` 且本项目无任何可用路径 → 按 M2 §2 永久边界以标准条文代替。
  准确表述是 **"GCC + Clang 双编译器实测 + MSVC 标准条文"**，不得写成"三编译器全部实测"。
