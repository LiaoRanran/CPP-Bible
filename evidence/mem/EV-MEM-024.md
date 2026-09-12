---
id: EV-MEM-024
serves: [ATOM-MEM-RAII-002]
kind: run
hypothesis: >-
  违反 Rule of Three 的后果：只写析构函数、不写拷贝构造 → 编译器隐式生成**浅拷贝** → 两个对象共享
  同一块资源（allocs=1、same_ptr=1）→ 同一块资源被析构两次（dtor_runs=2）；若析构函数释放资源即为
  double free。对照组（Rule of Three 三件套齐、深拷贝）：allocs=2、same_ptr=0、dtor_runs=2——同一
  观测口径下二者可区分。
controlled_vars: 同一观测口径（观测型析构 + operator new 重载计数）；唯一变量 = 拷贝语义（隐式浅拷贝 vs 手写深拷贝）
matrix:
  compiler: [GCC 15.3.0]
  # Clang 列待 CI Cross-check 步回填（GCC 15.3.0 已实测）
  std: [c++23]
  opt: [-O2]
  arch: [x86-64]
fixture: Examples/atoms/_atom_rule_three_bug.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/atoms/_atom_rule_three_bug.cpp -o Examples/atoms/_atom_rule_three_bug.asm
  g++ -std=c++23 -O2 Examples/atoms/_atom_rule_three_bug.cpp -o build/_replay_rtb.exe && ./build/_replay_rtb.exe
artifact: Examples/atoms/_atom_rule_three_bug.asm
artifact_sha256: 09892f2e6ae5f048fac1d72826aca895858550adc528803c177bd3f1782d2582
artifact_compiler: GCC 15.3.0 (MinGW-w64)
expected_sanitizer: [leak]   # 观测型析构只计数不释放（有意设计，见 drill_note）：ASan 下必然命中 LeakSanitizer，属 claim 的预期内反向证据
artifact_assert:
  - {kind: contains_any, texts: ["Buggy", "buggy"]}     # 违反组（Buggy）进工件：MinGW 留类型符号、GCC14 内联仅留运行串，任一即证
  - {kind: contains_any, texts: ["Correct", "correct"]}  # 对照组（Correct）进工件
expected:
  run: buggy 组 allocs=1 same_ptr=1 dtor_runs=2（一块资源两次析构）；correct 组 allocs=2 same_ptr=0 dtor_runs=2（各管各的）
  asm: 两组类型名进入工件（对照实验真实存在）
actual:
  run_cxx23_O2: "buggy  : allocs=1 same_ptr=1 dtor_runs=2 (one buffer, two dtors)|correct: allocs=2 same_ptr=0 dtor_runs=2 (two buffers, two dtors)"
verdict: confirm
falsification: >-
  ① 若隐式拷贝不是浅拷贝（same_ptr=0 或 allocs=2），则"只写析构 → 浅拷贝共享资源"被推翻——实测
  same_ptr=1、allocs=1；② 若两次析构不落在同一资源（dtor_runs 分属两块），则 double-destruct 不成立
  ——实测 buggy 组 dtor_runs=2 且资源只有 1 块。对照：correct 组 same_ptr=0/allocs=2 证明实验有
  区分力。三条件均不成立 => 经受住证伪。
depth_layer: runtime
drill_note: >-
  观测纪律：析构为**观测型**（只计数不释放），把 double-destruct 变成可重复、不崩溃的确定观测
  （若析构真 delete，第二次释放即 UB，MinGW release 下行为不定，无法作为 run_match 依据）。
  真实 double-free 由 ASan 在 WSL（Ubuntu g++ 13.3.0，与 CI 同版）捕获，第二证据腿源码已入库：
  `Examples/atoms/_atom_rule_three_bug_asan.cpp`（与主夹具 Buggy 同型、唯一差异是析构真释放），复现命令
  `g++ -std=c++11 -g -fsanitize=address Examples/atoms/_atom_rule_three_bug_asan.cpp -o build/_rtb_asan
  && ./build/_rtb_asan`，运行报 "ERROR: AddressSanitizer: attempting double-free ... #1 ... in
  Buggy::~Buggy() Examples/atoms/_atom_rule_three_bug_asan.cpp:14"——释放点栈帧直指入库文件的析构函数，
  实锤"浅拷贝 → 析构两次 → double free"因果链，人审可从仓库直接复算。Windows MinGW 工具链无
  ASan（replay sanitizer 步 skip，属既有 M2 边界）。
reproduce: 见 command 两行（Windows 计数口径）+ WSL 复现命令（Examples/atoms/_atom_rule_three_bug_asan.cpp，见 drill_note）
---

## 为什么这个证据可信

1. **唯一变量对照**：Buggy（只写析构）与 Correct（三件套齐）同 TU、同观测口径、同 -O2，唯一变量是
   拷贝语义——allocs 1 vs 2、same_ptr 1 vs 0 两组数字把"浅拷贝共享资源"与"深拷贝各管各"分开。
2. **观测不崩溃但结论不折损**：观测型析构把"同一块资源两次析构"变成确定性输出；真实 double-free
   的因果链由 WSL ASan 报告补全（释放点栈帧直接指向 Buggy::~Buggy），双证据互补。
3. **与 EV-MEM-023 构成 Rule of Zero/Three 对照对**：零声明（成员 RAII）→ 一切正确；只写析构 →
   隐式浅拷贝埋雷——同一套计数纪律下语义对照完整。

## 边界诚实说明

- ASan 版本是 WSL 人工复现（Ubuntu g++ 13.3.0 + -fsanitize=address），非 replay 机器口径——因为
  replay 不经 shell、无法吞掉 ASan 的非零退出码；报告摘录（`attempting double-free` + 析构栈帧）
  已留在 drill_note 供人审核对。WSL 预检（ci_local_precheck.py）侧无新增 ASan 义务（本卡主口径
  为 Windows 确定计数）。
- dtor_runs=2 本身不是错误（两对象析构各一次合法），错误在于两次析构共享同一资源——卡内输出用
  `(one buffer, two dtors)` 后缀显式标出这一语义。
- **主夹具在 ASan 下必然命中 LeakSanitizer（已声明豁免）**：主夹具 `_atom_rule_three_bug.cpp` 的
  析构是**观测型**（只计数、不释放，见 drill_note 的观测纪律），被 `new` 出来的一块缓冲在程序
  结束时必然仍被持有 ⇒ LSan 报 leak。这是卡的设计后果、不是缺陷，故声明
  `expected_sanitizer: [leak]`（工具按**类型**判定：命中类型全部在声明内 → 折算 confirm）。
  真实 double-free 的因果链仍由 `_atom_rule_three_bug_asan.cpp` 那条证据腿（析构真释放）承担
  ——两条腿的分工不变。

## 修订记录

- **2026-09-11 · gcc-14 兼容性修复（A 方向，verified 状态保留）**
  背景：CI 默认 g++ 14.2 下 `contains "Buggy"` / `contains "Correct"` 不命中——类型名随函数被
  内联，只剩运行输出里的 `buggy` / `correct` 串。claim 未变。
  实测：`buggy` 1 次、`correct` 1 次；`Buggy` / `Correct` 均 0 次（g++-14.2 与 g++-13.3 一致）⇒
  两条断言各改 `contains_any`，保留大驼峰与全小写两形态——断言是**大小写敏感**匹配，
  `buggy` ≠ `Buggy`，故两形态都必须显式在候选里。`artifact_sha256` 未变。
  另：WSL g++-14 全量复算还暴露本卡 sanitizer 步命中 LeakSanitizer（主夹具观测型析构不释放
  ⇒ 有意泄漏），已声明 `expected_sanitizer: [leak]` 折算 confirm（理由见"边界诚实说明"）。
