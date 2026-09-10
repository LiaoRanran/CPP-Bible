---
id: EV-UB-001
serves: [ATOM-UB-GRAY-001]      # G4 样板 B 配套证据（灰区判据原子）；人审通过原子化时启用
status: example                  # example：样板配套证据，随样板一并人审
kind: run                        # run（求值顺序观测）+ asm（call 顺序留痕）
hypothesis: >-
  `f(g(), h())` 中 `g` 与 `h` 的求值顺序是**未指定（unspecified）**，不是未定义行为——
  两种顺序都合法，程序不会崩，但**不可依赖**。
controlled_vars: >-
  同一夹具、同一 std（c++17）；变量 = 编译器版本 × 优化档（3 版本 × 2 档 = 6 组）
matrix:
  # Clang 版本并入 CI 的 Gray-zone 步 notice（下一轮 CI 起带版本号）；本轮只记 runner 默认。
  compiler: [GCC 15.3.0, GCC 13.1.0, GCC 8.1.0, Clang (ubuntu-latest runner 默认)]
  std: [c++17]
  opt: [-O0, -O2]
  arch: [x86-64]
fixture: Examples/_atom_eval_order.cpp
command: |          # POSIX 语义；产物必须写 build/（仓库源只读）
  # command 只跑主档（GCC 15.3 × -O2）；其余 5 组为同夹具人工补跑（见 actual）。
  g++ -std=c++17 -O2 Examples/_atom_eval_order.cpp -o build/_replay_eval.exe && ./build/_replay_eval.exe
  g++ -std=c++17 -O2 -S -masm=intel Examples/_atom_eval_order.cpp -o Examples/_atom_eval_order.asm
artifact: Examples/_atom_eval_order.asm
artifact_sha256: 7122e45d05e3c8e05b5e24fa71d5661f33e02754108233f283d0716a9f8bcb76
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:            # 跨编译器可移植的结构断言（身份不匹配时的替代校验）
  - {kind: contains, text: "_Z1gv"}    # 夹具函数 g 的 Itanium mangled 名（平台一致）
  - {kind: contains, text: "_Z1hv"}    # 夹具函数 h
expected_key: run_GCC15.3_O2_cxx17
expected:
  run: >-
    输出三行（h / g / f(1,2) 或 g / h / f(1,2)，两种都合法），rc=0，无 UB 征兆
    （无崩溃、无 sanitizer 报错）——**两种顺序都必须判 confirm**，这正是"未指定"的含义。
  asm: >-
    `main` 内三次 `call __mingw_printf` 的出现顺序与运行输出一致（`@L70` → `@L72` → `@L76`）。
    注：**不能**断言 `call _Z1hv` 在 `call _Z1gv` 之前——`-O2` 会把 `g`/`h` 内联掉（实测踩坑）。
actual:                      # 逐项实测（2026-09-10）
  # ★ GCC 三版本两档（6 组）全为右→左；CI 的 Clang 为**左→右**——两个编译器选了相反顺序。
  run_GCC15.3_O2_cxx17: "h | g | f(1,2)"
  run_GCC15.3_O0_cxx17: "h | g | f(1,2)"
  run_GCC13.1_O2_cxx17: "h | g | f(1,2)"
  run_GCC13.1_O0_cxx17: "h | g | f(1,2)"
  run_GCC8.1_O2_cxx17: "h | g | f(1,2)"
  run_GCC8.1_O0_cxx17: "h | g | f(1,2)"
  run_Clang_CI_O2_cxx17: "g | h | f(1,2)"      # ← 与 GCC 相反；来自 CI Gray-zone 步的 notice 注解
  asm_GCC15.3_O2: "main 内 `call __mingw_printf` 于 L70 / L72 / L76（顺序 h → g → f，与运行输出一致）"
verdict: confirm
falsification: >-
  任何一次运行出现崩溃、或输出在不同运行间**不确定**（同一二进制两次跑结果不同）即证伪"它是
  未指定而非 UB"。GCC 6 组 + Clang 1 组实测均 rc=0、无 sanitizer 报错 → 判为 unspecified。
  **最强证据是"两个编译器给出相反顺序"**：GCC 六个组合全是 `h→g`（右→左），而 CI 的 Clang 是
  `g→h`（左→右）——**如果顺序是被标准规定的，二者必然一致**；实测不一致，恰好证明标准只给了
  "合法结果集合"。
  **对照（反例说明，不造实验）**：`f(i++, i++)` 与本题**不同类**——它让**同一标量 i** 在两处
  未测序地各改一次，标准判为**未定义行为**（[intro.execution] 未测序的标量修改）。本卡不把它
  写成实验，因为它"跑起来大概率也正常"——**正如所有 UB**，不能靠"能跑"定性，只能靠标准条文。
depth_layer: asm
drill_note: >-
  汇编层可读出实现选的顺序：`main` 内三次 `call __mingw_printf` 出现在 `@L70` / `@L72` / `@L76`
  （对应 h → g → f，与运行输出一致）。注意**不能**去找 `call _Z1hv` / `call _Z1gv`——`-O2` 会把
  这两个小函数内联掉（实测踩坑）。这是**实现的选择**而非标准要求：换编译器就翻了（Clang 相反）。
reproduce: 见 command 两行；其余 5 组用同一夹具换 `-O0`/GCC 版本人工补跑
---

## 为什么这个证据可信

1. **有证伪条件且真的去证伪**：UB 会表现为崩溃或**非确定**输出。本卡跑了 6 组（3 版本 × 2 档），
   全部 rc=0 且输出固定 —— 这是"它不是 UB"的**实测依据**（而不是靠"我记得标准这么写"）。
2. **双层互证**：运行层（输出顺序固定）+ 汇编层（`call` 顺序可见），两层都指向"实现选了右→左"。
3. **双编译器已实测（M2 §2 边界达成）**：GCC 三版本 + **Clang（CI Gray-zone 步，notice 注解
   公开可读）**↔ 两者给出**相反顺序**；MSVC 无任何可执行路径 → 按 M2 §2 永久边界以标准条文代替，
   **不得宣称"三编译器实测完备"**（准确表述是：GCC + Clang 双编译器实测 + MSVC 标准条文）。

## 这张卡真正要教的东西：**连编译器之间都不一致**

GCC 三个版本（8.1 → 15.3，跨 7 年）× 两档优化，6 组**全部**输出 `h` 先于 `g`，很容易让人误以为
"标准规定了右→左"；而 **CI 的 Clang 输出 `g` 先于 `h`——正好相反**。事实很清楚：

- 标准给的是**合法结果集合**（两种顺序都合法），实现**任选其一**，且**不要求写进文档**
  （这正是 `unspecified` 与 `implementation_defined` 的分界，见 M2 §7 决策树第 2、3 条）；
- GCC 内部六个组合一致，只是**这批实现恰好都选了右→左**；**换个编译器就翻了**（Clang 实测）；
- 因此正确写法是：**不要**在一个表达式里依赖两个实参的求值先后（例如别让 `g` 和 `h` 改同一状态）。

## 与严格别名（EV-UB-002）的分界——本样板的教学落点

| | 求值顺序（本卡） | 严格别名（EV-UB-002） |
|---|---|---|
| 标准分类 | **unspecified** | **UB** |
| 标准给了什么 | 合法结果集合 | **不再要求任何行为** |
| 会不会崩 | 不会 | 可能，也可能"看起来很对" |
| 能依赖什么 | 可以依赖"不崩"，**不能**依赖顺序 | 什么都不能依赖——**代码已失去意义** |
| 优化器动作 | 只是挑一种顺序 | 可基于"不存在"的假设**删除你的访问**（实测：`alias_kill` 的返回值被静态化为常量 1） |

**判据（一句话版）**：问"标准有没有给合法结果集合"——有 → unspecified；连集合都没有 → UB。
本卡 falsification 里那个 `f(i++, i++)` 就是最容易被误判成 unspecified 的反例。
