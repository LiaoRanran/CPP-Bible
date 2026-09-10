---
id: EV-MEM-004
serves: [ATOM-MEM-RVREF-001]     # G5 MEM 域第一批；原子锻造后 EV-SERVES-EXIST 债自动清零
status: example                  # 随原子一同送审；人审通过前不作为已验收原子的正式证据
kind: run
hypothesis: >-
  函数形参声明为 `T&&` 时，形参名在函数体内**是左值**：用 `T y = x;` 初始化触发拷贝构造，
  必须写成 `T y = std::move(x);` 才触发移动构造。
controlled_vars: >-
  唯一变量 = 直接初始化 vs std::move(x)；Probe 类型、编译器、标准档、优化档在同一档内固定。
  （多档之间互为稳健性对照，不是受控变量。）
# ⚠️ matrix 是**笛卡尔声明**，故不等于实测组数：下面声明的 2×2×2 里，
# GCC 13.1 只跑了 {c++17 × -O2} 一组。**实测 5 组见 `actual` 五行**（红队 M4：
# 不能让矩阵口径大于实测口径还含糊带过）。
matrix:
  compiler: [GCC 15.3.0, GCC 13.1.0]
  std: [c++17, c++23]
  opt: [-O0, -O2]
  arch: [x86-64]
fixture: Examples/_atom_named_rvalue.cpp
command: |          # 产物 exe 必须写 build/（防根级 exe 泄漏被 pre-push 拦）；asm 入库以便比 sha
  g++ -std=c++17 -O2 Examples/_atom_named_rvalue.cpp -o build/_atom_named_rvalue.exe && ./build/_atom_named_rvalue.exe
  g++ -std=c++17 -O2 -S -masm=intel Examples/_atom_named_rvalue.cpp -o Examples/_atom_named_rvalue.asm
artifact: Examples/_atom_named_rvalue.asm
artifact_sha256: 9d77d5543dd6a432e6bcc9dee9e85cb9f441674a2f11c123a76542074980b664
# 2026-09-10 三改：夹具计数器改 `volatile`（修零观测伪证据，见"踩过的坑"第 1 条）
# → 工件重生成、哈希同步换。**改夹具必换哈希**是硬规则。
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:            # 跨编译器可移植结构断言（身份不匹配时启用；缺失/不满足即 refute）
  # ⚠️ 实测：**拷贝/移动构造的符号都被 -O2 内联了**——asm 里既没有 `_ZN5ProbeC1ERKS_`
  # （拷贝构造）也没有 `_ZN5ProbeC1EOS_`（移动构造），只有被内联后残留的 volatile 计数器读改写。
  # 这是本项目第四次遇到同一形态（B 的 g/h、C 的 auto_ptr 拷贝构造、本卡），铁律：
  # **不要预设汇编里有什么，先看工件再写断言。**
  # 故此处只锚定由源码结构决定、跨 Itanium ABI 稳定的静态计数器符号。
  # ⚠️ 注释口径更正（红队指出）：这两个 mangling 是 **Itanium ABI（GCC / Clang）** 通用，
  # **不是"跨平台"**——MSVC 的 mangling 完全不同（形如 `?copies@Probe@@2HA`）。
  # 按 M2 §2 永久边界，MSVC 本项目以标准条文代替，故此处不会真跑。
  - {kind: contains, text: "_ZN5Probe6copiesE"}     # static volatile 拷贝计数器（Itanium ABI）
  - {kind: contains, text: "_ZN5Probe5movesE"}      # static volatile 移动计数器
expected:
  # 加引号：`|` 是卡内的字段/行分隔符，裸写会被切成两行（见"踩过的坑"第 2 条）。
  run: "as_is copy=1 move=0 / moved copy=0 move=1"
actual:                      # 5 组实测（2026-09-10）：两编译器 × 两标准档 × 两优化档
  run_GCC15.3_O2_cxx17: "as_is copy=1 move=0 / moved copy=0 move=1"
  run_GCC15.3_O0_cxx17: "as_is copy=1 move=0 / moved copy=0 move=1"
  run_GCC15.3_O2_cxx23: "as_is copy=1 move=0 / moved copy=0 move=1"
  run_GCC15.3_O0_cxx23: "as_is copy=1 move=0 / moved copy=0 move=1"
  run_GCC13.1_O2_cxx17: "as_is copy=1 move=0 / moved copy=0 move=1"
verdict: confirm
falsification: >-
  两组**互为对照**，且**观测通路经汇编确认为活**（EV-MEM-002 零观测伪证据教训）：
  ① 若"形参是 T&& 就自动移动"成立，as_is 组应输出 copy=0 move=1 —— 实测 copy=1 move=0，被推翻；
  ② 若移动构造没生效（例如未定义、或被整体优化掉），moved 组也应是 copy=1 move=0，实验就
     **没有区分力**——实测 moved 组 move=1，且 `-O2` 工件里两次自增真实存在
     （`Examples/_atom_named_rvalue.asm` **@L23 与 @L30 的 `add eax, 1`**，分别是拷贝构造与
     移动构造内联后残留的 `copies = copies + 1` / `moves = moves + 1`），证明计数通路真实可观测。
  两条同时成立，本证据才不是恒真测试。
depth_layer: compiler         # 判定发生在**重载决议 / 值类别**层，非运行时
drill_note: >-
  差异不是"优化与否"，而是**值类别**：具名的右值引用是左值（[basic.lval] Note 3：
  "named rvalue references are treated as lvalues"），故 `T y = x;` 选中 `Probe(const Probe&)`；
  `std::move(x)` 把 x 变成 xvalue（cast to rvalue reference），才选中 `Probe(Probe&&)`。
  这解释了为什么"形参写 T&&"本身**不**保证移动。
reproduce: 见 command 两行，无外部依赖（自包含夹具，volatile 静态计数器）
---

## 为什么这个证据可信

1. **两组互为证伪对照**：不是"只演示成立"。as_is 组推翻"自动移动"，moved 组证明通路活着。
2. **观测通路经汇编确认**：`-O2` 工件里 `@L23`/`@L30` 的 `add eax, 1` 是两次真实自增，
   不是被常量折叠的立即数。
3. **五档一致**：GCC 15.3 × {-O0, -O2} × {c++17, c++23} 与 GCC 13.1 × -O2 输出**逐字相同**
   → 结论不依赖优化档、标准档、编译器小版本。
4. **机器可复算**：`artifact_sha256` + `artifact_assert[]` 双轨，工件与断言同代。

## 踩过的坑（留痕，供后续夹具参考）

1. 🔴 **计数器忘了 `volatile` → 零观测伪证据**（红队 S1 抓到）。
   初版用普通 `static int copies/moves`，`-O2` 直接把两组结果静态推导出来并**常量折叠**：
   `printf` 的四个实参全是立即数（`mov edx,1` / `xor r8d,r8d` / …），
   **运行时一次构造都没发生**，输出却"完美符合预期"。
   改 `static volatile int` 后，工件里出现真实的读-改-写（`@L23`/`@L30`），观测通路才活。
   ——**这是本项目第二次踩**（EV-MEM-002 初版），规则见 M2 §5：计数类实验计数器必须 volatile、
   -O0 与 -O2 双跑。另：自增要写 `x = x + 1` 而非 `++x`（C++20 起 volatile 复合赋值已弃用）。
2. 🔴 **输出里不能用 `|` 做分隔符**：它是证据卡的字段/行分隔符，`expected` 里裸写会被切成
   两行、与实际的单行输出不符 → `refute:run_mismatch`（B 样板踩过一次，本卡 G5 又踩一次）。
   改夹具输出用 ` / `，并给 `expected` 加引号双保险。
3. **输出合并成一行**（一次 `printf`）：复算契约是「一条 command 的 stdout ↔ 一组 `run_*`」，
   分两次 printf 会让 stdout 累积两行而 mismatch（G4-A 踩过）。
4. **"内联"与"整个消除"是两回事**：初版描述写"-O2 全部内联"，实际更彻底——`-O2` 把对象
   整个消除。描述必须如实，否则人审按错误预期去工件里找东西。

## 待补

- Clang / MSVC 两列：本机无，需 CI `Cross-check Matrix` 步补（`::notice::` 注解回填）。
- C++11 / C++14 两档：本机 GCC 8.1.0 可补（不支持 c++23，需换 c++17），暂未跑。
