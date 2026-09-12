---
id: EV-MEM-035
serves: [ATOM-MEM-SHARED-002]
kind: asm
hypothesis: >-
  unique_ptr 的移动与析构**不含原子操作**：工件全文不出现 `lock` 子串（MinGW 与 gcc-14 均为 0），
  移动只是纯指针搬运；其"零共享开销"由类型系统保障——unique_ptr 不可拷贝（copyable=0），
  要共享就必须显式改用 shared_ptr 并接受其原子代价（EV-MEM-034）。
controlled_vars: 同一 TU、同一编译器、同一 -O2（另跑 -O0 复核）；唯一变量 = 所有权类型（镜像对照 EV-MEM-034 的 shared_ptr 工件，同档同工具链）
matrix:
  compiler: [GCC 15.3.0]
  stdlib: [libstdc++]
  std: [c++23]
  opt: [-O0, -O2]
  arch: [x86-64]
fixture: Examples/atoms/_atom_unique_noatomic.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/atoms/_atom_unique_noatomic.cpp -o Examples/atoms/_atom_unique_noatomic.asm
  g++ -std=c++23 -O2 Examples/atoms/_atom_unique_noatomic.cpp -o build/_replay_unique_noatomic.exe && ./build/_replay_unique_noatomic.exe
artifact: Examples/atoms/_atom_unique_noatomic.asm
artifact_sha256: 94e96313b81f7d8180adf56c6177f0338c49e4804c73cf9face96478a8ce82ed
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains_any, texts: ["moves=", "dtor after scope="]}   # 活性：观测代码在工件里（防"空壳工件"）
  - {kind: absent, text: "lock"}                                   # 工件全文不得出现 lock 子串（一条覆盖全形态；夹具名已改去 nolock 以免被 .file 行误伤）
expected:
  run: unique_ptr sizeof=8（与裸指针同宽）；copyable=0、movable=1；两次移动后值 7 完好；生命周期内析构 0 次、离开作用域恰 1 次；moves 经 volatile 计数器读出（-O2 不可折叠）
  asm: 工件全文零 `lock` 子串
actual:
  run_cxx23_O2: "sizeof unique_ptr=8|copyable=0|movable=1|value=7 dtor during lifetime=0|moves=2 dtor after scope=1"
  run_cxx23_O0: "sizeof unique_ptr=8|copyable=0|movable=1|value=7 dtor during lifetime=0|moves=2 dtor after scope=1"
verdict: confirm
falsification: >-
  ① 若 unique_ptr 的所有权转移需要原子操作（例如实现里也走引用计数），工件里会出现 `lock` 前缀
  ——实测两平台均为 **0**（口径：`grep -c 'lock' <工件>`）；
  ② 若"不可拷贝"只是运行期检查而非类型系统约束，`copyable` 应为 1——实测 0（`is_copy_constructible`
  是编译期常量，等于说"共享"这条路径在编译期就被关闭）；
  ③ 若移动不是纯指针搬运，`dtor during lifetime` 会 >0（中间对象析构会连带释放资源）——实测 0，
  且离开作用域仍恰 1 次析构；`moves=2` 由 **volatile** 计数器读出（-O2 无法折叠；非 volatile 版本
  实测被折叠成立即数 `mov edx, 2`，本条即为此修正的留痕）。
  三条件均不成立 => 经受住证伪。
depth_layer: asm
drill_note: >-
  unique_ptr 的所有权转移是"把指针从旧对象搬到新对象、把旧对象置空"，没有任何跨线程可见的共享状态，
  所以既不产生原子指令、也不需要控制块——`sizeof` 恒为 8（与裸指针同宽，其 EBO 边界见 EV-MEM-032）。
  真正把"要不要付原子代价"变成可判选择的，是类型系统：unique_ptr 的拷贝构造被删除（copyable=0），
  共享只能显式改写成 shared_ptr（copyable=1、每份副本带一次原子增减，见 EV-MEM-034）。
reproduce: 见 command 两行，无外部依赖
---

## 为什么这个证据可信

1. **负向断言的正确用法**：`absent` 只在"被证明的对象确实存在"时才有意义——本卡先用
   `contains_any ["moves=", "dtor after scope="]` 证明工件含活代码，再用一条 `absent: "lock"`
   证明原子指令不出现。空壳工件无法通过第一关，故"零 lock"不是"没编译出东西"的假象。
2. **镜像对照成立**：EV-MEM-034 在同一优化档、同一工具链下给出 8 条 lock（`lock add` ×3 +
   `lock sub` ×5，全部落在控制块符号作用域内）；本卡给 0 条。差异只能来自所有权类型。
3. **类型系统与实现双证**：`copyable=0`（编译期约束）解释"唯一所有权"，`sizeof=8` + 零 lock（实现层）
   解释"零共享开销"——两侧证据指向同一条设计：独占 ⇒ 无需原子。
4. **有界声称**：本卡只说"**所有权管理本身**（移动/析构）不含原子 RMW"，不说"unique_ptr 永远无原子"
   ——持有 `std::atomic` 成员的类型当然会有，那是成员的代价，不是所有权机制的代价。

## 机器口径与边界诚实说明

- **`absent` 用一条 `lock` 覆盖全形态（含改名留痕）**：夹具原名 `_atom_unique_nolock.cpp`，其
  `.file` 指令会把 "lock" 子串带进工件、令 `absent: "lock"` 恒 refute（红队 M4 拦截）。按建议改名为
  `_atom_unique_noatomic.cpp` 后，单条 `absent: "lock"` 即可覆盖 `lock add/sub/xadd/cmpxchg/inc/dec/
  or/and/xor/xchg/bts` 等**全部**形态，并天然免疫"工具链把 lock 单独打一行或大写"的形态漂移。
- **"零 lock 前缀" ≠ "零原子操作"**（普遍化边界）：libatomic 出线调用（如 `call __atomic_load_16`）
  与内存操作数的隐式锁定 `xchg` 都不带 `lock` 前缀。本卡结论限定为"**所有权管理本身**不含原子 RMW"。
- **哪些是编译期常量**：`sizeof=8`、`copyable=0`、`movable=1` 在工件里是立即数（编译期常量）；
  `value`、`dtor during lifetime/after scope`、`moves` 是运行期读（`moves` 经 volatile 计数器）。
- **`-O0` 档是人工复跑留痕**：`command` 只跑 `-O2`（replay 机器口径沿 EV-MEM-008 先例），
  `run_cxx23_O0` 由同一会话 `-O0` 复跑填入，两档输出逐字一致。
- **不是"零成本"的普遍结论**：`sizeof=8` 依赖 libstdc++ 的 EBO（空且非 final 删除器，见 EV-MEM-032
  的 `final` 反例），跨标准库不保证。
