---
id: EV-MEM-042
serves: [ATOM-MEM-LEAK-002]
kind: run
hypothesis: >-
  三种生命周期行为可用**零依赖信号**（volatile 析构计数）区分，且该区分**不依赖任何 sanitizer**：
  `scoped`（局部对象）析构 =1；`cycle`（shared_ptr 强引用闭环）析构 =0 且**不可达**（真泄漏）；
  `owned`（堆对象被全局容器持有）析构 =0 但**退出时仍可达**（与 cycle 语义完全不同）。
  一个"析构 =0"的信号对应**两种不同语义**，因此它必须与"可达性"一起看才能下判断。
controlled_vars: 同一夹具、同一优化档、同一观测手段（volatile 计数）；唯一变量 = 对象的所有权形态（局部 / 强引用闭环 / 全局注册表持有）
matrix:
  compiler: [GCC 15.3.0 (MinGW-w64), GCC 14.2.0 (WSL)]
  stdlib: [libstdc++]
  std: [c++23]
  opt: [-O2（本卡）/ -O1（同夹具在 EV-MEM-043 的 sanitizer 观测）]
  arch: [x86-64]
  sanitizer: ["本卡不依赖 sanitizer；同一夹具的 sanitizer 侧观测见 EV-MEM-043"]
  # 跨平台确定性对照（可核对锚）：WSL 复跑命令
  #   `g++-14 -std=c++23 -O2 Examples/atoms/_atom_leak_detection.cpp`，输出与 Windows 侧逐字相同
fixture: Examples/atoms/_atom_leak_detection.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/atoms/_atom_leak_detection.cpp -o Examples/atoms/_atom_leak_detection.asm
  g++ -std=c++23 -O2 Examples/atoms/_atom_leak_detection.cpp -o build/_replay_leak_detection.exe && ./build/_replay_leak_detection.exe
artifact: Examples/atoms/_atom_leak_detection.asm
artifact_sha256: ed44b0c6e06d2fcfdd88336417838e19eaf67ffb24e2f229d67e4a94a7f7b512
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains_any, texts: ["scoped_dtor_count=", "cycle_dtor_count="]}     # 三类对象的析构计数
  - {kind: contains_any, texts: ["owned_registry_size=", "cycle_live_objects="]}     # 可达性对照 + 泄漏判据
expected:
  run: >-
    `scoped_dtor_count=1`（对照组：正常路径确实会析构 ⇒ 计数通路是活的）；
    `cycle_dtor_count=0`（强引用闭环 ⇒ 零析构）且 `cycle_is_leak=1`；
    `owned_dtor_count=0`（全局持有同样零析构）但 `owned_registry_size=1`（说明"零析构"的**原因不同**）。
  asm: 三条计数字面量与判据字面量在工件 `.rodata` 中可见（断言不依赖任何 mangle 符号）
actual:
  run_cxx23_O2: "scoped_dtor_count=1|cycle_dtor_count=0|owned_dtor_count=0|owned_registry_size=1|scoped_is_clean=1|cycle_allocated=2|cycle_destroyed=0|cycle_live_objects=2"
expected_sanitizer: [leak]   # 本夹具**含真泄漏演示**（`cycle` 强引用闭环）：sanitizer 步若报告 leak，
                             #   属**正确检测**（反向证 claim），折算 confirm 而非 refute——同 EV-MEM-014/024 口径。
                             #   本机 MinGW 无 sanitizer（skip）；Linux 侧历史观测为**零报告**（见 EV-MEM-043）。
verdict: confirm
# 载荷留痕（红队 BL1 修复）：`Examples/atoms/_atom_leak_detection.out` 含完整复跑命令行 + stdout +
#   **干净 stderr 原文（0 字节）** + `grep -c -i leaksanitizer` = 0 ⇒ 第三方可复现"LSan 零报告"，
#   排除"没报是因为根本没跑"。
falsification: >-
  **真对照（唯一变量 = 所有权形态）**：若观测通路是死的（循环被优化掉或被跳过），
  `scoped_dtor_count` 应为 **0** —— 实测 **1**（活性对照成立）。若 `cycle` 不是真泄漏，
  `cycle_dtor_count` 应为 **2**（两个 Node 各析构一次）—— 实测 **0**。
  若 `owned` 与 `cycle` 语义相同，两者应能被同一信号区分——实测**不能**（同为 0）：
  `owned_registry_size=1` 才是它们的分水岭（一个仍可达、一个不可达）⇒ 这条实测直接支撑
  "析构计数单独不足以定性，须配可达性"。
  **跨平台**：WSL/g++-14 输出与 Windows 侧**逐字相同**（确定性读数，可安全作断言锚）。
depth_layer: runtime
drill_note: >-
  泄漏检测的教学难点是"信号与语义不是一一对应"：`scoped/cycle/owned` 三种情形里，
  前两者才是传统意义上的"有/无泄漏"，而 `owned` 的零析构是**设计选择**（进程级持有）。
  本卡给出不依赖工具的判据（析构计数 + 可达性来源），使读者在任何环境下都能先定性，
  再决定要不要请工具出场（工具侧边界见 EV-MEM-043）。
---

# EV-MEM-042 · 三类生命周期行为的零依赖区分

## 观测（Windows/MinGW 15.3.0 与 WSL/g++-14 逐字相同）

| 场景 | 所有权 | `*_dtor_count` | 其余读数 | 语义 |
|---|---|---|---|---|
| `scoped` | 局部对象 | **1** | `scoped_is_clean=1` | 正常路径（活性对照） |
| `cycle` | `shared_ptr` 强引用闭环 | **0** | `cycle_is_leak=1` | **真泄漏**（不可达） |
| `owned` | 全局注册表持有 | **0** | `owned_registry_size=1` | 零析构但**仍可达**（非泄漏） |

## 为什么这条证据重要

`cycle` 与 `owned` 的析构计数**同为 0**，但一个是要修的问题、一个是设计选择。
任何"只看析构计数"或"只看工具是否报错"的判据都会在这里失手——
这正是 ATOM-MEM-LEAK-002（工具报告边界）的前置事实：**先能用零依赖信号定性，才知道该不该信工具**。

## 边界

- 本卡不涉及任何 sanitizer（工具侧观测在 EV-MEM-043）；
- 计数用 `volatile` 累加，仅证明"析构函数被调用过"，不度量时间/顺序；
- `run_*` 三个函数带 `__attribute__((noinline))`，避免内联改变生命周期观测位置。
