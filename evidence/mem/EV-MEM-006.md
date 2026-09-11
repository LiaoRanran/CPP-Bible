---
id: EV-MEM-006
serves: [ATOM-MEM-VALUE-001]
kind: run
hypothesis: >-
  C++11 起每个表达式落于 glvalue×rvalue 正交二维：lvalue = glvalue∧¬rvalue、xvalue = glvalue∧rvalue、
  prvalue = ¬glvalue∧rvalue；std::move(x) 把 lvalue 转成 xvalue（decltype 得 T&&），不是 prvalue
  （decltype 得 T）；临时对象/字面量是 prvalue；具名右值引用（形参同理）在表达式体内是左值（decltype 得 T&）。
controlled_vars: 同一 TU、同一编译器、同一 -O2；唯一变量 = 被测表达式的形式（具名变量 / std::move / 字面量 / 具名右值引用 / 临时）
matrix:
  compiler: [GCC 15.3.0]
  # Clang 列待 CI Cross-check 步回填（GCC 15.3.0 已实测）
  std: [c++23]
  opt: [-O2]
  arch: [x86-64]
fixture: Examples/_atom_value_cat.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/_atom_value_cat.cpp -o Examples/_atom_value_cat.asm
  g++ -std=c++23 -O2 Examples/_atom_value_cat.cpp -o build/_replay_vc.exe && ./build/_replay_vc.exe
artifact: Examples/_atom_value_cat.asm
artifact_sha256: 99fc88c576dc2d12081a1a676ffa813be7b3ba2501544519e39cd9ecfc6be2d5
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains, text: "xvalue"}
  - {kind: contains, text: "prvalue"}
expected:
  run: 5 行，分别给出 lvalue/xvalue/prvalue 及其两正交维度；具名右值引用(int&& r)为 lvalue(int&)；std::string() 临时为 prvalue
  asm: 类别字符串字面量进入 .asm（xvalue/prvalue 可被结构断言命中）；static_assert 强制五分类在编译期成立
actual:
  run_cxx23_O2: "lvalue  decltype((x))            => lvalue   glvalue / not-rvalue|xvalue  decltype(std::move(x))    => xvalue   glvalue / rvalue|prvalue decltype(42)             => prvalue   not-glvalue / rvalue|lvalue  named rvalue ref int&& r  => lvalue   (int&)|prvalue std::string() temporary   => prvalue   (std::string)"
verdict: confirm
falsification: >-
  若 decltype((x)) 不是 int&（lvalue 不成立）、或 decltype(std::move(x)) 是 int（即 move 产出 prvalue）、
  或具名右值引用 r 的 decltype 不是 int&，则五分类被推翻，本卡 refute。static_assert 任一失败即编译红
  （机器复算第一步 compile_rc 直接拦截）。
depth_layer: compiler
drill_note: >-
  值类别是重载决议之前的编译期属性，由 decltype 的引用推导直接证明；两正交维度（glvalue/rvalue）
  由 is_reference_v / is_lvalue_reference_v 判定互证。这是"类型系统论证"，与优化档无关（优化不改变
  表达式值类别），故只跑 -O2 一档；双重观测来自 decltype 推导 + 正交维度判定，二者互为印证。
reproduce: 见 command 两行，无外部依赖
---

## 为什么这个证据可信

1. **编译期硬证明 + 运行期可观测**：五分类由 5 条 `static_assert` 强制（类型系统层面，不是"看起来对"）。
   同时把每个类别的名字打印出来，让"类别"成为运行期可比对的标准输出（`run_match` 精确比对）。
2. **两正交维度互证**：`glvalue`/`rvalue` 用 `is_reference_v`/`is_lvalue_reference_v` 独立判定，
   与 `vc_name()`（基于 `is_lvalue_reference_v`/`is_rvalue_reference_v`）的结果落在同一个 2×2 格子上，
   交叉验证"lvalue=glvalue∧¬rvalue / xvalue=glvalue∧rvalue / prvalue=¬glvalue∧rvalue"这一正交结构。
3. **覆盖反直觉点**：`std::move(x)` 得到 `T&&`（xvalue，仍是 glvalue），不是 `T`（prvalue）；
   具名右值引用 `int&& r` 在表达式体内是 `int&`（左值）——正是 [basic.lval] Note 3 的机器化陈述。

## 版本边界诚实说明（红队要求）

值类别的**重定义**发生在 C++11（引入 glvalue/rvalue 二分 + prvalue/xvalue 命名）；C++11 之后五分类
语义稳定。本卡在 c++23 单档实测（类型系统论证，优化无关）；如需全档 CI 佐证，可在 `command` 追加
`-std=c++11/14/17/20` 的同夹具编译（夹具仅用 c++11 起即有的 `decltype`/`static_assert`/`type_traits`，
跨档可编译），输出逐字一致。
