---
id: EV-MEM-021
serves: [ATOM-MEM-VALUE-002]
kind: run
hypothesis: >-
  引用折叠只有 4 条规则：T& &→T&、T& &&→T&、T&& &→T&、T&& &&→T&&（唯一保持右值引用的是
  "右值引用的右值引用"）。折叠只对"经模板形参/typedef 引入的引用"生效——直接写 T& & 反而非法。
  T&& 仅在推导语境下是万能引用：传左值推 T=int&（折叠回左值引用）、传右值推 T=int；
  auto&& 同理；const T&& 无推导特判，只绑定右值。
controlled_vars: 同一 TU、同一编译器、同一 -O2；唯一变量 = 复合引用的组合形式（4 组折叠）与实参值类别（左值/右值）
matrix:
  compiler: [GCC 15.3.0]
  # Clang 列待 CI Cross-check 步回填（GCC 15.3.0 已实测）
  std: [c++23]
  opt: [-O2]
  arch: [x86-64]
fixture: Examples/atoms/_atom_fwd_fold.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/atoms/_atom_fwd_fold.cpp -o Examples/atoms/_atom_fwd_fold.asm
  g++ -std=c++23 -O2 Examples/atoms/_atom_fwd_fold.cpp -o build/_replay_fold.exe && ./build/_replay_fold.exe
artifact: Examples/atoms/_atom_fwd_fold.asm
artifact_sha256: 59fc71f41e0389963bc6ea0577cdb75035f8e84a16f77a7e98a23d55fe773d45
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains, text: "sink_lvalue"}   # 对照重载符号进入工件（推导观测路径真实存在）
  - {kind: contains, text: "auto&& from"}   # auto&& 推导观测点进入工件
  # 注：折叠正确性的门禁是 4 条 static_assert（折叠错即编译红，compile_rc 拦截）；
  # 工件断言只锚定"观测路径存在"，不锚定出现在输出字面量里的期望类型串（"期望值进字面量"
  # 属作弊级断言，红队 S3 教训）。
expected:
  run: 4 组折叠分别得 int&/int&/int&/int&&；auto&& 左值得 int&、右值得 int&&；万能引用传左值 T=int&、传右值 T=int；const T&& 只推 T=int（无左值特判）
  asm: 折叠别名与推导观测点的字符串字面量进入工件（类型系统论证真实存在）
actual:
  run_cxx23_O2: "fold T& &   => int&|fold T& &&  => int&|fold T&& &  => int&|fold T&& && => int&&|auto&& from lvalue => int&|auto&& from rvalue => int&&|univ   T&& : T=int&   param_is_lvalue_ref=1|univ   T&& : T=int    param_is_lvalue_ref=0|const T&& : T=int   (rvalue only)|sink_lvalue called x=0"
verdict: confirm
falsification: >-
  ① 若折叠规则不是"仅 T&& && 保持右值引用"（如 T& && 也折叠成 T&&），则对应 static_assert 编译红，
  机器复算第一步 compile_rc 直接拦截；② 若 const T&& 也是万能引用（传左值能推 T=int&），则第 9 行
  输出应为 "T=int&  (ERROR...)" 且参数为左值引用——实测 T=int（只接右值）=> 两条件均不成立 => 经受住证伪。
depth_layer: compiler
drill_note: >-
  折叠发生在"引用被 typedef/模板形参间接引入"的类型构造点（[dcl.ref]）：别名层叠 Lref<Lref<T>> 把第二个
  引用经模板形参引入，折叠规则才得以应用——直写 T& & 是语法非法（GCC 15.3.0 报 "cannot declare reference
  to 'T&', which is not a typedef or a template type parameter"，实测留痕）。万能引用的推导特判在
  [temp.deduct.call]：P 是 T&& 且 A 是左值时推 T=int&，再经折叠得 int&。本卡为类型系统论证
  （decltype/static_assert），优化不改变推导结果，故只跑 -O2 一档。
reproduce: 见 command 两行，无外部依赖
---

## 为什么这个证据可信

1. **编译期硬证明**：4 条折叠规则由 4 条 `static_assert` 强制——任一条折叠成右值引用（或 T&& && 折叠成
   左值引用）都会编译红，不依赖"看起来对"。
2. **推导结果双向可观测**：万能引用传左值/右值的 T 推导结果（int& vs int）由 `is_lvalue_reference_v<T>`
   运行期打印，与 static_assert 的类型系统论证互为印证；`auto&&` 用 `decltype(变量)`（声明类型）独立验证。
3. **带反例对照**：`const T&&` 同 TU 实测只接右值（T=int，无左值特判），把"带 && 就是万能引用"的误读
   堵死在同一夹具内——实验有区分力。

## 边界诚实说明

- **折叠的语法前提是本卡踩坑所得**：初版直接写 `using L = T& &;` 被 GCC 15.3.0 拒（"cannot declare
  reference to 'T&', which is not a typedef or a template type parameter"）——折叠只作用于经 typedef/
  模板形参引入的引用，这个前提本身写进了夹具注释与正文。
- MSVC/Clang 的推导行为依同款标准条款；本机无 Clang/MSVC（M2 边界），Clang 列由 CI Cross-check 回填。
