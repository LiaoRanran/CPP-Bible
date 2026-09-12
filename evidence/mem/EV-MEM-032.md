---
id: EV-MEM-032
serves: [ATOM-MEM-UNIQUE-002]
kind: asm
hypothesis: >-
  unique_ptr 的删除器是**类型的一部分**（`unique_ptr<T, D>` 的 D 进类型系统）：在 libstdc++ 实现下，
  空**且非 final** 的删除器被空基类优化吸收（sizeof == 裸指针 8 字节），有状态删除器必须作为对象
  成员存储（sizeof 16）；数组特化 `unique_ptr<T[]>` 走 delete[] 而不是 delete，且只提供 operator[]、
  不提供 operator* / operator->——这些差异全部在**编译期**就能被类型系统看见。
controlled_vars: 同一 TU、同一编译器、同一 -O2（另跑 -O0 复核，见「机器口径」）；唯一变量 = 删除器类型（空/空但 final/有状态）与指针形态（对象/数组）
matrix:
  compiler: [GCC 15.3.0]
  stdlib: [libstdc++ (GCC 15.3.0 MinGW-w64)]
  std: [c++23]
  opt: [-O0, -O2]
  arch: [x86-64]
fixture: Examples/atoms/_atom_unique_deleter.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/atoms/_atom_unique_deleter.cpp -o Examples/atoms/_atom_unique_deleter.asm
  g++ -std=c++23 -O2 Examples/atoms/_atom_unique_deleter.cpp -o build/_replay_udeleter.exe && ./build/_replay_udeleter.exe
artifact: Examples/atoms/_atom_unique_deleter.asm
artifact_sha256: a96938954e8f1004381f75acf61793996e281bf5167f3d14f98a5198ba84eb14
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains_any, texts: ["unique_ptrIi12StatelessDelE", "unique_ptrIi12StatelessDel"]}  # 删除器类型出现在 unique_ptr 的 mangled 类型名里（=类型参数；MinGW 工件实测 7 次，gcc-13/14 各 12 次）
  - {kind: contains_any, texts: ["Sp_counted_deleter"]}   # 对照：shared_ptr 的删除器不在 shared_ptr 类型名里，而被搬进控制块类型（本工件 86 次）
  - {kind: contains_any, texts: ["_Znwm", "_Znwy"]}       # operator new 的**调用点**真实存在（分配层；MinGW 13 次 / gcc-14 11 次）
expected:
  run: sizeof 六连（default=8 / stateless=8 / stateful=16 / array=8 / ref deleter=16 / final stateless=16）；shared_ptr 三连恒 16 且 sizes equal=1；数组特化 subscript=1 deref=0 arrow=0、对象特化与之相反；三种删除器调用 delta 各 1；数组 len=8 elem=12（运行期派生）；array new/delete calls 各 1；单对象路径 delete[] delta=0
  asm: 删除器类型出现在 unique_ptr 的 mangled 类型名中（类型参数）；shared_ptr 侧同一删除器只出现在控制块类型名里
actual:
  run_cxx23_O2: "sizeof unique_ptr default=8|sizeof unique_ptr stateless=8|sizeof unique_ptr stateful=16|sizeof unique_ptr array=8|sizeof unique_ptr ref deleter=16|sizeof unique_ptr final stateless=16|sizeof shared_ptr default=16|sizeof shared_ptr stateless=16|sizeof shared_ptr stateful=16|shared_ptr sizes equal=1|shared_ptr retargeted=1|array has subscript=1|array has deref=0|array has arrow=0|object has subscript=0|object has deref=1|object has arrow=1|stateless calls delta=1|stateful calls delta=1|final deleter calls delta=1|array len=8 elem=12|array new calls=1|array delete calls=1|single object delete[] delta=0"
  run_cxx23_O0: "sizeof unique_ptr default=8|sizeof unique_ptr stateless=8|sizeof unique_ptr stateful=16|sizeof unique_ptr array=8|sizeof unique_ptr ref deleter=16|sizeof unique_ptr final stateless=16|sizeof shared_ptr default=16|sizeof shared_ptr stateless=16|sizeof shared_ptr stateful=16|shared_ptr sizes equal=1|shared_ptr retargeted=1|array has subscript=1|array has deref=0|array has arrow=0|object has subscript=0|object has deref=1|object has arrow=1|stateless calls delta=1|stateful calls delta=1|final deleter calls delta=1|array len=8 elem=12|array new calls=1|array delete calls=1|single object delete[] delta=0"
verdict: confirm
falsification: >-
  **真对照（在卡内可复核）**：① `StatelessFinalDel`（空**但 final** 的删除器）实测 sizeof=16，而
  普通空删除器 = 8 —— 若"无状态删除器不增大对象"是普遍成立的语言保证，本行应同为 8；实测 16，
  故该表述**被证伪**，只能退守到"libstdc++ 对空且非 final 的类型做 EBO（实现边界）"。
  ② 若数组特化走的是 delete 而非 delete[]，则 `array delete calls` 与 `single object delete[] delta`
  会同时为 0 —— 实测 1 / 0，路径区分成立（该结论由**运行层重载计数**给出，不由汇编断言给出，见下）。
  ③ 若 unique_ptr 的删除器也走类型擦除，则 `unique_ptr<int, StatefulDel>` 的 sizeof 应等于
  `unique_ptr<int>`（8）—— 实测 16，随删除器变化，"擦除"假设被推翻。
depth_layer: asm
drill_note: >-
  删除器进类型系统带来两个可量化后果：① 存储——libstdc++ 的 EBO 门槛是"空**且非 final**"
  （内部 trait `__empty_not_final`）：普通空删除器 sizeof=8（与裸指针同，零开销），但空却 final 的
  删除器 sizeof=16，有状态删除器（带 int tag）同样 16。② 接口——`unique_ptr<T[]>` 是独立特化：
  只提供 `operator[]`，`*p` 与 `p->` 在编译期就不存在（实测 trait：subscript=1/deref=0/arrow=0，
  对象特化相反）。汇编层证据：删除器类型出现在 unique_ptr 的 mangled 类型名
  `unique_ptrIi12StatelessDelE` 中（本工件 7 次），而 shared_ptr 恰恰相反（见 EV-MEM-033）。
  注意 `-O2` 下数组路径的 `delete[]` 被**完全内联**进 main：工件里只有夹具自定义的 `_ZdaPv`
  定义、没有任何 `call _ZdaPv` 调用点，故**汇编层无法判"走了哪条释放路径"**，该结论只由运行层
  `operator new[]/delete[]` 重载计数承担（`array delete calls=1` vs `single object delta=0`）。
reproduce: 见 command 两行，无外部依赖
---

## 为什么这个证据可信

1. **唯一变量对照，且带真反例**：同一 TU 内并列 `unique_ptr<int>` / `<int, StatelessDel>` /
   `<int, StatelessFinalDel>` / `<int, StatefulDel>` / `<int[]>`，唯一变量是删除器类型与指针形态。
   其中 `final` 组是**真证伪对照**（不是"若…则应…"的假设句）：它实测 16，直接推翻"无状态 ⇒ 不增大"
   的普遍表述，把 claim 逼回"libstdc++ 实现边界"这个可辩护的位置。
2. **双向证据**：运行层（sizeof + 编译期 trait + delete[] 重载计数）与汇编层（mangled 类型名里含删除器）
   独立指向同一结论；trait 三条（subscript/deref/arrow）把"数组特化只给 operator[]"变成可编译验证的判据。
3. **跨优化档一致**：`-O0` 与 `-O2` 输出逐字一致（见 `run_cxx23_O0`），说明 24 行数字不是优化器假象；
   删除器调用计数一律用**差分**（`...delta=`）读取，避免累计值混入其他代码块的调用。
4. **与 EV-MEM-033 构成机制对照对**：本卡证明"删除器是类型参数"，033 证明"shared_ptr 的删除器被
   类型擦除"——两卡的 mangled 类型名证据互为镜像（`unique_ptrIi12StatelessDelE` vs
   `_Sp_counted_deleterIPi6TagDel...`），共同支撑 ATOM-MEM-UNIQUE-002 的核心论断。

## 机器口径与边界诚实说明

- **`-O0` 档是人工复跑留痕**：`command` 只跑 `-O2`（replay 的机器口径为 -O2，沿 EV-MEM-008/
  EV-MEM-022 先例），`run_cxx23_O0` 由同一会话用 `g++ -std=c++23 -O0 -Wall -Wextra` 复跑填入；
  两档输出逐字一致。矩阵因此声明 `opt: [-O0, -O2]`。
- **EBO 是实现细节，不是语言保证**：标准只要求 `unique_ptr` 能存下指针与删除器，不要求零开销。
  本卡的 8 字节结论绑定 `matrix.stdlib`（libstdc++ / GCC 15.3.0），`final` 组就是这条边界的反例。
- **汇编断言只锚"符号存在性"**：`unique_ptrIi12StatelessDelE` 在三个编译器下出现次数为 7/12/12
  （MinGW/gcc-13/gcc-14，统计口径：`grep -c 'unique_ptrIi12StatelessDelE' <工件>` 按行计），
  故断言用 `contains_any` 只锚存在性，不写死计数（内联决策随编译器变化）。
- **删除器调用形态**：`-O2` 下 unique_ptr 侧的删除器调用被完全内联（无间接调用）；shared_ptr 侧则
  保留控制块虚派发 `call [QWORD PTR 16[rax]]`（本工件 322/365 行）——两卡对照见 EV-MEM-033。
  该间接调用点是**MinGW 工件**的形态，gcc-14 工件里被进一步内联，故不写进跨编译器断言。
