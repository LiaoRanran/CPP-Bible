---
id: EV-MEM-033
serves: [ATOM-MEM-UNIQUE-002]
kind: asm
hypothesis: >-
  shared_ptr 的删除器被**类型擦除**：语言层面不存在 `shared_ptr<T, D>`（对比 `unique_ptr<T, D>`
  有 D 参数），删除器只能经构造函数按值注入并被控制块持有（一次拷贝发生在形参初始化，块内不再拷贝）；
  对象大小恒为两个指针（16 字节）、与删除器类型无关。擦除的运行期代价是**控制块自身的堆分配**：
  实测 `shared_ptr<T>(new T)` 触发 2 次堆分配（对象 + 控制块）、`make_shared<T>` 合并为 1 次，
  而 unique_ptr 对照路径恒为 1 次（只有对象本身）。
controlled_vars: 同一 TU、同一编译器、同一 -O2（另跑 -O0 复核）；唯一变量 = 删除器类型/状态（空/有状态 TagDel）、构造方式（裸指针 vs make_shared）与持有者数量（1 vs 3 共享控制块）
matrix:
  compiler: [GCC 15.3.0]
  stdlib: [libstdc++ (GCC 15.3.0 MinGW-w64)]
  std: [c++23]
  opt: [-O0, -O2]
  arch: [x86-64]
fixture: Examples/atoms/_atom_shared_deleter_erase.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/atoms/_atom_shared_deleter_erase.cpp -o Examples/atoms/_atom_shared_deleter_erase.asm
  g++ -std=c++23 -O2 Examples/atoms/_atom_shared_deleter_erase.cpp -o build/_replay_sderase.exe && ./build/_replay_sderase.exe
artifact: Examples/atoms/_atom_shared_deleter_erase.asm
artifact_sha256: a26740cd570112fd429b27c01d43601d28a2d1f7d17899e871ef69f8bdd1dd25
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains_any, texts: ["Sp_counted_deleterIPi6TagDel", "Sp_counted_deleter"]}  # 删除器被搬进**控制块**类型（MinGW 43 次 / gcc-13、14 各 65 次；按行 grep 口径）
  - {kind: contains_any, texts: ["10_M_disposeEv", "10_M_destroyEv"]}                    # 控制块的虚派发钩子成员（擦除后调用删除器的通路；命中定义/vtable，非调用点）
  - {kind: contains_any, texts: ["_Znwm", "_Znwy"]}                                      # 控制块自身的堆分配（擦除的运行期代价；MinGW 9 次 / gcc-14 8 次）
expected:
  run: shared_ptr 恒 16 字节且 sizes equal=1（与删除器无关）；删除器在构造时拷贝 1 次、共享控制块时拷贝 0 次；三个持有者全 reset 只调用删除器 1 次；堆分配计数 2 / 1 / 1（裸指针构造 / make_shared / unique_ptr 对照）；同一静态类型可先后持有 tag=11 与 tag=22 两份删除器
  asm: 删除器类型出现在控制块类名 `_Sp_counted_deleter` 中，而 shared_ptr 自身的类名里没有删除器
actual:
  run_cxx23_O2: "sizeof shared_ptr default=16|sizeof shared_ptr with stateful deleter=16|shared_ptr sizes equal=1|deleter copies on ctor=1|deleter copies on share=0|deleter calls after all reset=1|deleter tag seen=99|shared_ptr from raw ptr allocs=2|make_shared allocs=1|unique_ptr allocs=1|tag seen after reset #1=11|tag seen after reset #2=22"
  run_cxx23_O0: "sizeof shared_ptr default=16|sizeof shared_ptr with stateful deleter=16|shared_ptr sizes equal=1|deleter copies on ctor=1|deleter copies on share=0|deleter calls after all reset=1|deleter tag seen=99|shared_ptr from raw ptr allocs=2|make_shared allocs=1|unique_ptr allocs=1|tag seen after reset #1=11|tag seen after reset #2=22"
verdict: confirm
falsification: >-
  **真对照（在卡内可复核）**：① 分配计数是**与值类别无关**的硬对照——若 shared_ptr 不需要控制块，
  则 `shared_ptr from raw ptr allocs` 应为 1（只有对象）；实测 2（对象 + 控制块），且 `make_shared`
  为 1、unique_ptr 为 1，三行数字共同把"控制块"这一额外分配钉死。
  ② 若删除器只是按引用挂在共享状态上（而非持有副本），则局部删除器 `TagDel d(99)` 析构后控制块
  会持悬垂引用；实测释放时仍读到 `deleter tag seen=99`，且原始 `d` 的栈槽在共享阶段已被覆盖
  （工件里 `_M_dispose` 体内 `mov edx, DWORD PTR 16[rcx]` 读的是**块内偏移 16**的副本）⇒ 持有副本成立。
  ③ 若共享控制块时每个副本各拷一份删除器，则 `deleter copies on share` 应等于新增副本数（2）——
  实测 0。三条件均不成立 => 经受住证伪。
  **已删除的伪证伪**（红队 Step 2 拦截）：原版拿"unique_ptr 传右值(0 拷贝) vs shared_ptr 传左值
  (1 拷贝)"当对照——差异只来自实参**值类别**，与"类型参数 vs 擦除"无关，属无效对照，已撤除。
depth_layer: asm
drill_note: >-
  `shared_ptr<T>` 的模板参数表里**没有**删除器（语言层面如此，实测 `shared_ptr<int, TagDel>` 报
  `wrong number of template arguments (2, should be 1)`），删除器只能经构造函数 `shared_ptr(Y*, D)`
  注入，被搬进控制块 `_Sp_counted_deleter<Y*, D, A, L>`——这是"类型擦除"的实现形态：控制块是
  模板化的（每对 (T,D) 一个实例），而 shared_ptr 自身的类型与 D 无关，于是同一静态类型可以先后
  持有任意删除器（实测 tag=11 → tag=22）。代价可量化：控制块自身一次堆分配（裸指针构造共 2 次、
  make_shared 合并为 1 次）、调用经控制块虚表槽 `call [QWORD PTR 16[rax]]`（本工件 352/395/441 行）。
  注意 `-O2` 下该间接调用在 gcc-14 工件里会被进一步内联，故断言不锚"必须是间接调用"，只锚控制块
  类型与虚派发钩子的存在性。
reproduce: 见 command 两行，无外部依赖
---

## 为什么这个证据可信

1. **语言层面的事实先立住**：`std::shared_ptr<int, TagDel>` 是**编译错误**（实测 GCC 15.3.0 与
   14.2 均报 `wrong number of template arguments (2, should be 1)`），而 `std::unique_ptr<int, TagDel>`
   合法——"删除器是否进类型参数"不是风格差异，是语言规定。
2. **代价被拆成可数的三笔，且与值类别无关**：堆分配次数（裸指针构造 2 / make_shared 1 / unique_ptr 1）、
   共享时删除器拷贝增量（0）、释放时调用次数（3 个持有者全 reset 只 1 次）——把"擦除在哪付代价"分开，
   而不是笼统说"shared_ptr 更慢"。
3. **"持有副本"有结构性证据**：`_M_dispose` 体内从控制块偏移 16 读出删除器（副本），配合 tag=99 的
   运行期读回，排除"按引用持有"的替代解释；共享阶段删除器拷贝增量为 0 则排除"每副本一份"。
4. **汇编层与运行层互证**：控制块类型 `_Sp_counted_deleterIPi6TagDelSaIvELN9__gnu_cxx12_Lock_policyE2EE`
   三平台各出现（按行 grep：MinGW 43 / gcc-13 65 / gcc-14 65），其虚派发钩子 `_M_dispose` / `_M_destroy`
   同现；而 shared_ptr 自身的类名里没有 TagDel。与 EV-MEM-032 的 `unique_ptrIi12StatelessDelE` 互为镜像。

## 机器口径与边界诚实说明

- **`-O0` 档是人工复跑留痕**：`command` 只跑 `-O2`（replay 机器口径沿 EV-MEM-008 先例），
  `run_cxx23_O0` 由同一会话用 `-O0` 复跑填入，两档输出逐字一致，矩阵因此声明 `opt: [-O0, -O2]`。
- **"拷贝 1 次"的归因**：这 1 次拷贝发生在**按值形参从实参初始化**（`shared_ptr(Y*, D d)`），
  控制块随后持有该形参的副本（块内不再拷贝）——次数属实现细节，标准只要求 D 可拷贝构造。
- **断言只跨 libstdc++ 版本稳定**：`_Sp_counted_deleter` 是 libstdc++ 的实现类型名，libc++ 与 MSVC STL
  并不存在同名类型；本卡不断言"跨标准库稳定"，跨标准库结论只到"shared_ptr 对象恒为两个指针"这一层。
- **本卡不量化跨线程引用计数的原子开销**——那属 ATOM-MEM-SHARED-001 的领域（另有证据卡），
  两块证据不重复。
