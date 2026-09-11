---
id: EV-MEM-004
serves: [ATOM-MEM-RVREF-001]     # G5 MEM 域第一批；原子锻造后 EV-SERVES-EXIST 债自动清零
status: example                  # 随原子一同送审；人审通过前不作为已验收原子的正式证据
kind: run
hypothesis: >-
  函数形参声明为 `T&&` 时，形参名在函数体内**是左值**：用 `T y = x;` 初始化触发拷贝构造，
  必须写成 `T y = std::move(x);` 才触发移动构造。且该论断对**无移动构造的类型**同样成立——
  `std::move` 会**静默退化**选中拷贝构造（第三组对照）。
controlled_vars: >-
  唯一变量 = 直接初始化 vs std::move(x)（vs 无移动构造类型的 std::move）；Probe/CopyOnly
  类型、编译器、标准档、优化档在同一档内固定。
matrix:                          # ⚠️ 笛卡尔声明 ≠ 实测组数：GCC 13.1 只跑了 {c++17 × -O2} 一组
  compiler: [GCC 15.3.0, GCC 13.1.0]
  # Clang 列待 CI Cross-check 步回填（GCC 15.3.0 已实测）
  std: [c++11, c++14, c++17, c++20, c++23]
  opt: [-O0, -O2]
  arch: [x86-64]
fixture: Examples/_atom_named_rvalue.cpp
command: |          # 产物 exe 必须写 build/（防根级 exe 泄漏被 pre-push 拦）；asm 入库以便比 sha
  g++ -std=c++17 -O2 Examples/_atom_named_rvalue.cpp -o build/_atom_named_rvalue.exe && ./build/_atom_named_rvalue.exe
  g++ -std=c++17 -O2 -S -masm=intel Examples/_atom_named_rvalue.cpp -o Examples/_atom_named_rvalue.asm
artifact: Examples/_atom_named_rvalue.asm
artifact_sha256: f9804693137251177c83dea01bab17886ca0ef5f9e88889b07c4c85267f38ab4
# 2026-09-11 四改：加第三组对照（CopyOnly，无移动构造类型）→ 工件重生成、哈希同步换。
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:            # 跨编译器可移植结构断言（身份不匹配时启用；缺失/不满足即 refute）
  # ⚠️ 实测：拷贝/移动构造的符号都被 -O2 内联——asm 里没有 `C1` 系列符号，只有被内联后
  # 残留的 volatile 计数器读改写（**三组 = 三次 `add eax, 1`**，@L22/@L29/@L37）。
  # 铁律：不要预设汇编里有什么，先看工件再写断言。
  # ⚠️ 口径：这些 mangling 是 **Itanium ABI（GCC/Clang）** 通用，**不是"跨平台"**——
  # MSVC mangling 完全不同；按 M2 §2 永久边界，MSVC 以标准条文代替，此处不会真跑。
  - {kind: contains, text: "_ZN5Probe6copiesE"}     # static volatile 拷贝计数器（Itanium ABI）
  - {kind: contains, text: "_ZN5Probe5movesE"}      # static volatile 移动计数器
  - {kind: contains, text: "_ZN8CopyOnly6copiesE"}  # 第三组：无移动构造类型的拷贝计数器
expected:
  # 加引号：`|` 是卡内的字段/行分隔符，裸写会被切成两行（B 样板踩过、G5 又踩一次）。
  run: "as_is copy=1 move=0 / moved copy=0 move=1 / copyonly copy=1"
actual:                      # 11 组实测（2026-09-11）：C++11–C++23 全五档 × {-O0,-O2} + GCC 13.1
  run_GCC15.3_O2_cxx11: "as_is copy=1 move=0 / moved copy=0 move=1 / copyonly copy=1"
  run_GCC15.3_O0_cxx11: "as_is copy=1 move=0 / moved copy=0 move=1 / copyonly copy=1"
  run_GCC15.3_O2_cxx14: "as_is copy=1 move=0 / moved copy=0 move=1 / copyonly copy=1"
  run_GCC15.3_O0_cxx14: "as_is copy=1 move=0 / moved copy=0 move=1 / copyonly copy=1"
  run_GCC15.3_O2_cxx17: "as_is copy=1 move=0 / moved copy=0 move=1 / copyonly copy=1"
  run_GCC15.3_O0_cxx17: "as_is copy=1 move=0 / moved copy=0 move=1 / copyonly copy=1"
  run_GCC15.3_O2_cxx20: "as_is copy=1 move=0 / moved copy=0 move=1 / copyonly copy=1"
  run_GCC15.3_O0_cxx20: "as_is copy=1 move=0 / moved copy=0 move=1 / copyonly copy=1"
  run_GCC15.3_O2_cxx23: "as_is copy=1 move=0 / moved copy=0 move=1 / copyonly copy=1"
  run_GCC15.3_O0_cxx23: "as_is copy=1 move=0 / moved copy=0 move=1 / copyonly copy=1"
  run_GCC13.1_O2_cxx17: "as_is copy=1 move=0 / moved copy=0 move=1 / copyonly copy=1"
  # Clang 列：经 ci.yml「Cross-check Matrix」步的 ::notice:: 注解回填（本机无 Clang，
  # M2 §2 双编译器边界）；回填后此处补 run_Clang_* 行，值预期与 GCC 逐字一致。
verdict: confirm
falsification: >-
  三组**三角验证**，且观测通路经汇编确认存活（@L22/@L29/@L37 三次 `add eax, 1`）：
  ① 若"形参是 T&& 就自动移动"成立，as_is 组应为 copy=0 move=1 —— 实测 copy=1 move=0，被推翻；
  ② 若 std::move 也没生效（移动构造未定义/被整体消除），moved 组应为 copy=1 move=0，实验
     无区分力 —— 实测 move=1，证明移动构造通路真实可观测；
  ③ 若"写了 std::move 就一定移动"成立，copyonly 组应为 copy=0 —— 实测 copy=1（**静默退化**
     选中拷贝构造），该误解被推翻。
  三条同时成立，本证据既不是恒真测试，也不漏"反向误解"。
depth_layer: compiler         # 判定发生在**重载决议 / 值类别**层，非运行时
drill_note: >-
  差异不是"优化与否"，而是**值类别**：具名的右值引用是左值（[basic.lval] Note 3：
  "named rvalue references are treated as lvalues"），故 `T y = x;` 选中 `Probe(const Probe&)`；
  `std::move(x)` 把 x 变成 xvalue（cast to rvalue reference），才选中 `Probe(Probe&&)`。
  第三组则显示重载决议的另一面：xvalue 只是一个"候选资格"，**没有 T&& 重载可选中时照样退化**。
reproduce: 见 command 两行，无外部依赖（自包含夹具，volatile 静态计数器）
---

## 为什么这个证据可信

1. **三组三角验证**：as_is（左值→拷贝）/ moved（xvalue→移动）/ copyonly（xvalue 但无移动
   重载→退化拷贝），既证伪"自动移动"，也证伪"move 必移动"，双向都有区分力。
2. **观测通路经汇编确认**：`-O2` 工件里 `@L22`/`@L29`/`@L37` 三次 `add eax, 1` 是真实自增。
3. **十一档一致**：C++11–C++23 **全五档** × {-O0,-O2}（GCC 15.3）+ GCC 13.1 × -O2 输出
   **逐字相同**（红队 G1 指出"九档缺 c++20"的超报后补测）
   → 结论不依赖优化档、标准档、编译器小版本（C++11 起 14 年间规则未变）。
4. **机器可复算**：`artifact_sha256` + `artifact_assert[]` 双轨，工件与断言同代。

## 踩过的坑（留痕，供后续夹具参考）

1. 🔴 **计数器忘了 `volatile` → 零观测伪证据**（红队 S1 抓到，详见 git 历史）。初版用普通
   `static int`，`-O2` 把结果常量折叠成立即数，运行时一次构造都没发生。改 `volatile` 后
   工件出现真实读-改-写。自增要写 `x = x + 1` 而非 `++x`（C++20 起 volatile 复合赋值已弃用）。
2. 🔴 **输出里不能用 `|` 做分隔符**：它是证据卡的字段/行分隔符 → `refute:run_mismatch`。
   夹具输出用 ` / `，`expected` 加引号双保险。
3. **输出合并成一行**（一次 `printf`）：复算契约「一条 command 的 stdout ↔ 一组 `run_*`」。
4. **"内联"与"整个消除"是两回事**：描述必须如实，否则人审按错误预期去工件里找东西。
5. **`= delete` 移动构造 ≠ 没有移动构造**：前者仍参与重载决议且被选中 → 编译错误（显式
   报错，不是静默退化）；后者才静默退化成拷贝。第三组对照必须用"没有"，不能用"删除"。

## 待补

- Clang 列（CI notice 回填，见 `actual` 尾注）。
- MSVC：永久边界，以标准条文代替（M2 §2）。
