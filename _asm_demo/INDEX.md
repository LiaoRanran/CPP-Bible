# 真机汇编实证矩阵（ASM MATRIX）· GCC 15.3.0

> **目标**：把"每个 C++ 抽象在 GCC 15.3.0 下到底生成什么代码"系统化，每个实证揭示一个**非显然的底层事实**（零开销是否成立 / 优化等级影响 / 平台 ABI 差异 / 工程陷阱）。
>
> **工具链（实测）**：`g++.exe (MinGW-W64 x86_64-msvcrt-posix-seh, built by Brecht Sanders, r1) 15.3.0`；`objdump.exe 2.46.1`。
> 默认编译：`g++ -std=c++26 -O2 <src>.cpp -o <src>.exe`；对比等级时显式 `-O0/-Os`。反汇编：`objdump.exe -d -M intel -C <obj>.o`。
>
> **红线**：① 全部真实编译 + 真实 `objdump`，**绝不伪造**；② 不新增章节，实证嵌入现有章的"附录"小节，正文保持最简洁；③ 标准列了 ≠ 编译器真能跑，不可用特性诚实标注（含失败证据）。
>
> **编号规则**：`ASM-<章号>-<机制>`。证据源码与 `.s` 汇编产物均落本目录 `_asm_demo/`。

---

## 一、已覆盖实证（累计 53 例，STATE 记录）

> 下表为本目录可查证证据文件；其中 `ch08_mdspan_test` / `ch08_print_test` 为**失败证据**（头缺失 / 链接失败），不计入成功汇编但保留以诚实记录"标准 vs 实测"差距。

| 编号 | 机制 | 章 | 证据文件 | 关键结论 |
|------|------|:--:|----------|----------|
| ASM-08-expected | `std::expected` tagged union | ch08 | `ch08_expected_test.cpp/.s` | 零开销：union 值/错误指针偏移 0，has_value 1 字节标志偏移 8 |
| ASM-08-generator | `std::generator` 协程帧 | ch08 | `ch08_generator_test.cpp/.s` | 每次 `iota` `operator new(0x68=104B)` 堆分配协程帧 |
| ASM-08-format | `std::format` 类型擦除 | ch08 | `ch08_format_test.cpp/.s` | handler 函数指针分派（非 vtable）；`std::print` 链接失败→用 format 等价 |
| ASM-08-opt | 优化等级对比 | ch08 | `ch08_opt_expected.cpp/.s` | parse_digit: -O0 182B/3 次构造调用，-O2 99B/0 调用，-Os 74B 最小 |
| ASM-08-ranges | `std::ranges` 零成本 | ch08 | `ch08_ranges_test.cpp/.s` | ranges::sort≡std::sort 同 `__introsort_loop`；filter 谓词内联为 `test`+`jne` |
| ASM-08-mdspan | `std::mdspan` | ch08 | `ch08_mdspan_test.cpp` | ❌ 失败证据：`<mdspan>` 头缺失 |
| ASM-08-print | `std::print` | ch08 | `ch08_print_test.cpp` | 🚧 失败证据：宏定义但 libstdc++ 未导出 `__open_terminal`，链接失败 |
| ASM-09-contracts | Contracts `-fcontracts` | ch09 | `ch09_contracts_test.cpp/.o` | clamp post 检查 `cmp/jg`；链接缺 `handle_contract_violation`（GCC 实验限制） |
| ASM-27-cast | 四种 cast | ch27 | `ch27_cast_test.cpp/.s` + `ch27_with_impl.s` | `static_cast`/`reinterpret_cast` 零成本；`dynamic_cast` 走 RTTI 查询 |
| ASM-40-exception | 异常 unwinding | ch40 | `ch40_exception_test.cpp/.o` | 异常路径生成 LSDA + personality 例程，正常路径零开销 |
| ASM-42-aliasing | strict aliasing | ch42 | `ch42_aliasing_test.cpp/.o` | `__restrict`/NSA 消除防别名 reload，循环去冗余加载 |
| ASM-48-rtti | RTTI `dynamic_cast` | ch48 | `ch48_rtti_test.cpp/.o` | vtable 内 `__si_class_type_info` 链遍历 |
| ASM-51-crtp | CRTP 静态多态 | ch51 | `ch51_crtp_test.cpp/.o` | 静态分发，无虚调用，编译期展开 |
| ASM-52-ebo | 空基类优化 | ch52 | `ch52_ebo_test.cpp/.o` | 空基类占 0 字节，子类布局不膨胀 |
| ASM-77-vector | `std::vector` | ch77 | `ch77_vector_test.cpp/.o` | 下标访问编译为 `base + idx*4` 单条 `mov`；扩容走 `realloc` |
| ASM-93-thread | `std::thread` | ch93 | `ch93_thread_test.cpp/.o` | 包装函数 + `pthread_create` 系统调用分发 |
| ASM-115-move | 移动语义 | ch115 | `ch115_move_test.cpp/.o` | 移动 = 指针浅拷，零深拷贝；RVO 消除临时对象 |
| ASM-117-elision | 拷贝省略 NRVO | ch117 | `ch117_elision_test.cpp/.o` | 具名返回值优化消除一次拷贝构造 |
| ASM-108-memory_order | 内存序指令屏障 | ch108 | `ch108_memory_order_test.cpp/.s` | acquire/release 因 TSO 零屏障；seq_cst store 付 `xchg`；原子 RMW 付 `lock xadd` |
| ASM-41-shared_ptr | shared_ptr 引用计数 | ch41 | `ch41_shared_ptr_test.cpp/.s` | 拷贝构造 = 16B memcpy + `lock add [rdx+0x8]` 原子递增 use_count |
| ASM-107-atomic_rmw | 原子 RMW (fetch_add/exchange/CAS) | ch107 | `ch107_atomic_rmw_test.cpp/.s` | fetch_add relaxed/seqcst 逐字节相同 `lock xadd`；exchange 用隐式锁 `xchg`；CAS 环 `lock cmpxchg`+`jne` |
| ASM-109-fence | 显式内存屏障 | ch109 | `ch109_fence_test.cpp/.s` | seq_cst fence=`lock or`(非 mfence)；acquire/release/acq_rel 全空；signal fence 零指令 |
| ASM-69-constexpr | constexpr 编译期求值 | ch69 | `ch69_constexpr_test.cpp/.s` | 常量参数→`mov eax,0x1a6d`(6765) 递归零痕迹；运行时参数→退化为真实 `fib_cx` 递归体 |
| ASM-116-perfect_fwd | 完美转发引用折叠 | ch116 | `ch116_perfect_fwd_test.cpp/.s` | `std::forward` 运行时零指令；模板两实例化与手写转发逐字节相同 `jmp sink_l/sink_r`；按值传递多 16B 栈拷贝 |
| ASM-117-nrvo | 拷贝省略 vs 未省略 | ch117 | `ch117_nrvo_test.cpp/.s` | prvalue/NRVO 零 call；多返回路径 NRVO 失效→两分支各 `call` move 构造 |
| ASM-81-sso | `std::string` 小字符串优化 | ch81 | `ch81_sso_test.cpp/.s` | 短串 `make_short` 无 `operator new`（SSO 栈内缓冲）；长串 `make_long` 含 `call operator new` 堆分配 |
| ASM-77-vector_grow | `vector::push_back` 扩容 | ch77 | `ch77_vector_grow_test.cpp/.s` | 扩容三连 `operator new`+`memcpy`+`operator delete`；`reserve` 后循环无扩容 call |
| ASM-47-vs-51 | 虚调用 vs CRTP 静态分发 | ch47 | `ch47_vs_51_dispatch_test.cpp/.s` | 单点虚调用 `mov vptr;jmp [vtable]`；虚循环每轮 `call [vtable]` 无法内联；CRTP 循环体 `imul` 内联零 call |
| ASM-88-variant | `std::variant`+`std::visit` 分派 | ch88 | `ch88_variant_visit_test.cpp/.s` | visit = 按 index 字节 `cmp`/`je` 分支链，零 `call`，handler 内联；≈ 手写 switch；标签真实偏移 0x4（全 int 变体） |
| ASM-122-pmr | `std::pmr` 分配路径 | ch122 | `ch122_pmr_test.cpp/.s` | 默认 vector `operator new`+`memcpy`+`operator delete` 堆三连；pmr 栈缓冲够用→零 `operator new`，分配内联为指针递增 |
| ASM-std_function | `std::function` 类型擦除 | ch26 | `ch26_std_function_test.cpp/.s` | 调用=经对象内 invoker 指针 `call [rcx+0x18]`+空守卫；裸函数指针 `jmp rax`；无捕获 lambda 内联零 call；与虚调用同代价类 |
| ASM-26-lambda-capture | lambda 捕获代价 | ch26 | `ch26_lambda_capture_test.cpp/.s` | 无捕获=1B 占位；按值捕获值=4B 快照(调用点寄存器搬运 0 访存)；按引用捕获=8B 持指针(调用点经指针解引用多 1 次加载)；目标可证明不变时 GCC 折叠引用捕获为零开销 |
| ASM-50-vi | 虚继承 this 调整 thunk | ch50 | `ch50_vi_test.cpp/.s` | virtual thunk(`_ZTv0_n24_N1D1fEv`)经 vbtable 运行时查虚基类偏移调整 this(`add rcx,[rax-0x18]`)，非固定 `sub`；比非虚 MI thunk(`sub rdi,0x10`)更贵 |
| ASM-40-noexcept | noexcept 对异常处理元数据体积 | ch40 | `ch40_nt_maythrow.cpp/.o/.s` + `ch40_nt_noexcept.cpp/.o/.s` | SEH: may_throw EH 元数据 100B vs no_throw 32B(−68%)；`.xdata.unlikely` LSDA 块整体消失；`.text.unlikely` 抛异常路径代码消除(64→0)；等价于 ELF 上 `.gcc_except_table` 消失 |
| ASM-88-optional | `std::optional` 布局与访问代价 | ch88 | `ch88_optional_test.cpp/.s` | 访问零额外间接（值单条 mov，engaged 标志@offset4）；空间代价真实：optional<int> 8B / optional<long long> 16B / optional<char> 2B（vs int 4B） |
| ASM-82-span | `std::span` 零成本视图 | ch82 | `ch82_span_test.cpp/.s` | 遍历与裸 `ptr+len` 逐字节同码；`operator[]` 无运行时边界检查（越界静默 UB）；sizeof=16（ptr+size_t） |
| ASM-89-tuple | `std::tuple` / 结构化绑定 | ch89 | `ch89_tuple_test.cpp/.s` | `get<N>` 编译期偏移访问（无索引计算）；结构化绑定与裸 struct 成员访问逐字节相同；libstdc++ 递归继承致末参在最底地址（get<2>@0/get<1>@8/get<0>@16），sizeof=24 |
| ASM-80-array | `std::array` 零开销下标 | ch80 | `ch80_array_test.cpp/.s` | 与裸数组逐字节同布局（均 32B）；`operator[]`=`mov eax,[rcx+rdx*4]` 无边界检查；`at()`=`cmp rdx,0x7`+`ja` throw 路径；`data()`=`mov rax,rcx`；按值传递整段 32B 拷贝 |
| ASM-81-string_view | `std::string_view` 零成本视图 | ch81 | `ch81_string_view_test.cpp/.s` | 布局 `{len@0,ptr@8}`、16B；`sv_substr` 零 call O(1)；`str_substr` 含 `_M_create/_M_copy` 调用 O(n)；`sv_at`=`add rdx,[rcx+8]`+`movzx` 无检查 |
| ASM-32-init_list | `std::initializer_list` 寿命陷阱 | ch32 | `ch32_init_list_test.cpp/.s` | 布局 `{ptr@0,len@8}`；range-for 退化为指针自增循环；`dangling_il()` 触发 `-Winit-list-lifetime` 告警；字面量提升为 .rdata 非常量悬垂 |
| ASM-87-bitset | `std::bitset` 边界检查代价 | ch87 | `ch87_bitset_test.cpp/.s` | `bitset_flip`=`not`；`bitset_set/test` 移位+位运算带 `cmp i,0x3f` 边界检查；`bitset_count` 拆低/高 32 位各 call 一次 popcount 运行库 |
| ASM-87-bit | `<bit>` 工具与硬件 popcount | ch87 | `ch87_bit_test.cpp/.s` + `ch87_bit_test_popcnt.s` | `popcnt_u` 默认走运行库 SWAR；`bswap_u`=`bswap`；`to_float`=`movd`；`is_pow2`=`(x-1)<(x^(x-1))`；`-mpopcnt` 后 `popcnt eax,ecx` 单指令 |
| ASM-24-enum | `enum class` 强类型零开销 | ch24 | `ch24_enum_test.cpp/.s` | `use_enum`=`movzx`+`add`+越界`cmovae`；`use_plain`=`lea [rcx+1]` 隐式转换零成本；`enum_underlying`=`mov eax,ecx` |
| ASM-83-map | `std::map` 红黑树指针追逐 | ch83 | `ch83_map_test.cpp/.s` | `build()` 三次 `call _M_emplace_hint_unique`（每元素 `operator new` 节点）；`find_it` 沿 `+0x10`左/`+0x18`右指针追逐比较键`@0x20`，O(log n) |
| ASM-85-unordered | `std::unordered_map` 桶链表 | ch85 | `ch85_unordered_test.cpp/.s` | `build()` 节点堆分配+桶数组（`max_load_factor=0x3f800000`）；`find_it` 先 `div r11` 取桶索引再沿 `+0x00` next 单链表比较键`@0x08` |
| ASM-78-deque | `std::deque` 分块映射双间接 | ch78 | `ch78_deque_test.cpp/.s` | 块大小=512B(128×int)；`operator[]`=`sar rdx,0x7`块索引→`mov rdx,[rbx+rdx*8]`查表→`lea rdx,[rdx+r9*4]`元素偏移；push_back 越块触发`operator new(0x200)` |
| ASM-79-list | `std::list` 节点堆分配+指针追逐 | ch79 | `ch79_list_test.cpp/.s` | 每元素`operator new` 24B 节点(prev+next+value)；遍历=`mov rax,[rax+0x8]` 纯 next 追逐无缓存局部性；与 vector 求和差距 8-15× |
| ASM-79-fwdlist | `std::forward_list` 无 size+单链哨兵 | ch79 | `ch79_fwdlist_test.cpp/.s` | 无 `size` 成员(O(n) distance)；`insert_after` 仅改写 2 个 next 指针；节点 16B(比 list 省 8B prev) |
| ASM-84-set | `std::set` 红黑树节点+指针追逐 | ch84 | `ch84_set_test.cpp/.s` | 每节点`operator new(0x28=40B)`；find 比较键`@0x20`追逐左`@0x10`/右`@0x18`指针；键即值均存 0x20 |
| ASM-85-uset | `std::unordered_set` 哈希桶+单链 | ch85 | `ch85_uset_test.cpp/.s` | find 先`div`取桶→沿`+0x00` next 链比较值`@0x08`；节点 16B(next 指针+value)；rehash 是 O(n) 全局操作 |
| ASM-86-pq | `std::priority_queue` 堆上浮 | ch86 | `ch86_pq_test.cpp/.s` | push=vector::push_back+push_heap 上浮环(`sar`除2+`cmp`+交换)；top=`mov eax,[rbx]`(c.front())；无虚函数零开销 |
| ASM-86-adapters | `stack`/`queue` 委托适配器 | ch86 | `ch86_adapters_test.cpp/.s` | stack::top=deque::back；queue::front 直接读 deque._M_start 首元素(无函数调用)；全部编译期委托零开销 |
| ASM-89-any | `std::any` SBO 边界 | ch89 | `ch89_any_test.cpp/.s` | ≤16B 类型 SBO 内联存(零堆)；>16B 走 `_Manager_external`+operator new 堆；any_cast 内联 typeid 比对 |

> 方向 1 早期另有 `unique_ptr`(ch41)、`vtable`(ch47) 等以**章内联片段**形式存在的实证，不重复计入本文件清单；总计数以 STATE.json `assembly_empirical_examples` 为准（当前 53）。

---

## 二、Phase 5 计划覆盖（批次）

> 按"嵌入式相关性 × 非显然度"排序。每批完成即更新上方"已覆盖"表与 STATE 计数。

### 批 A：并发与原子（嵌入式最关键）
- [x] **ASM-108-memory_order**：`relaxed`/`acquire`/`release`/`seq_cst` 在 x86-64 下的指令屏障差异（acquire/release 因 TSO 零屏障；seq_cst store 付 `xchg`；原子 RMW 付 `lock` 前缀）
- [x] **ASM-41-shared_ptr**：`shared_ptr` 拷贝构造的引用计数原子递增（`lock add [rdx+0x8]` 原子 RMW）
- [x] ASM-107-atomic_rmw：`fetch_add`/`compare_exchange` 的 `lock xadd`/`lock cmpxchg` 与 CAS 循环展开
- [x] ASM-109-fence：显式 `atomic_thread_fence` 生成的 `lock or` 全屏障 / acquire-release 空 / signal 零指令

### 批 B：零开销验证
- [x] ASM-69-constexpr：`constexpr` 编译期求值 → 运行时零痕迹（函数体在运行时完全消失；带运行时参数退化为真实递归）
- [x] ASM-116-perfect_fwd：完美转发的引用折叠（零开销，`std::forward` 运行时零指令，与手写转发逐字节相同，按值传递多 16B 栈拷贝）
- [x] ASM-117-nrvo：拷贝省略 vs 未省略的指令数对比（prvalue/NRVO 零 call；多返回路径 NRVO 失效触发真实 move 构造）

### 批 C：字符串与容器
- [x] ASM-81-sso：`std::string` 小字符串优化（SSO）：短串存栈内联缓冲，免堆分配（链接后 objdump 显示 `make_short` 无 `operator new`、`make_long` 有）
- [x] ASM-77-vector_grow：`push_back` 触发扩容的 `operator new`+`memcpy`+`operator delete` 三连（扩展现有 ASM-77-vector，与附录 H 互补）

### 批 D：多态分发
- [x] ASM-47-vs-51：虚函数调用（`call [vtable+off]` 间接调用）vs CRTP 静态分发（直接 `call`）的指令数/间接跳转对比
- [x] ASM-88-variant：`std::variant` 访问（`std::visit`）的类型索引分派 vs `virtual` 虚调用

### 批 E：分配与 PMR
- [x] ASM-122-pmr：`std::pmr` 多态分配器（资源句柄）vs 默认 `new` 的分配路径差异

### 批 F：类型擦除
- [x] ASM-std_function：`std::function` 类型擦除的间接调用 + 小对象优化 vs 模板/CRTP 静态内联

### 批 G：捕获 / 虚继承 / noexcept 元数据（嵌入式高相关、非显然）
- [x] **ASM-26-lambda-capture**：lambda 捕获形式的指令代价与闭包布局（无捕获 1B / 按值 4B / 按引用 8B；引用捕获在目标可证明不变时被 GCC 折叠为零开销，实时读取才显式二次解引用）
- [x] **ASM-50-vi**：虚继承 this 调整 thunk 经 vbtable 运行时查虚基类偏移（非固定 `sub`，比非虚 MI thunk 更贵）——虚继承除 vbptr 外的第二重运行时代价
- [x] **ASM-40-noexcept**：noexcept 对异常处理元数据体积影响（SEH：100B→32B，LSDA 块消失；等价 ELF `.gcc_except_table`）

---

### 批 H：零成本词汇类型（optional / span / tuple）
- [x] **ASM-88-optional**：`std::optional` 布局与访问代价（空间真实膨胀、访问零额外间接；engaged 标志@offset4；optional<int> 8B vs int 4B）
- [x] **ASM-82-span**：`std::span` 零成本视图（遍历≡裸 `ptr+len`；`operator[]` 不查边界；sizeof=16）
- [x] **ASM-89-tuple**：`std::tuple`/`get<N>`/结构化绑定编译期偏移访问（零运行时索引；libstdc++ 末参在最底地址布局；sizeof=24）

### 批 I：零成本词汇/容器（array / string_view / initializer_list）
- [x] **ASM-80-array**：`std::array` 与裸数组逐字节同布局（均 32B）、`operator[]`=`mov eax,[rcx+rdx*4]` 无边界检查、`at()`=`cmp rdx,0x7`+`ja` throw 路径、`data()`=`mov rax,rcx`、按值传递整段 32B 拷贝（movdqu+mov）
- [x] **ASM-81-string_view**：`string_view`={len@0,ptr@8}、16B、`sv_substr` 零 call O(1)、`str_substr` 含 `_M_create/_M_copy` 调用 O(n)、`sv_at`=`add rdx,[rcx+8]`+`movzx` 无检查
- [x] **ASM-32-init_list**：`initializer_list`={ptr@0,len@8}、range-for 退化为指针自增循环、`dangling_il()` 触发 `-Winit-list-lifetime` 告警、字面量提升为 .rdata 非常量悬垂

### 批 J：零成本工具与强类型（bitset / <bit> / enum class）
- [x] **ASM-87-bitset**：`bitset_flip`=`not`、`bitset_set/test` 移位+位运算带 `cmp i,0x3f` 边界检查、`bitset_count` 拆低/高 32 位各 call 一次 popcount 运行库
- [x] **ASM-87-bit**：`<bit>` 工具 `popcnt_u` 默认走运行库 SWAR、`bswap_u`=`bswap`、`to_float`=`movd`、`is_pow2`=`(x-1)<(x^(x-1))`；`-mpopcnt` 后 `popcnt eax,ecx` 单指令
- [x] **ASM-24-enum**：`use_enum`=`movzx`+`add`+越界`cmovae`、`use_plain`=`lea [rcx+1]` 隐式转换零成本、`enum_underlying`=`mov eax,ecx`

### 批 K：关联容器（map / unordered_map）
- [x] **ASM-83-map**：vtable 内 `__si_class_type_info` 链遍历
- [x] **ASM-85-unordered**：`std::unordered_map` 桶链表+hash div→next 对比

### 批 L：STL 容器真实成本实证（deque/list/forward_list/set/unordered_set/adapter/any）
- [x] **ASM-78-deque**：分块映射双间接（`sar 0x7`块索引+map查表+偏移）、push_back 越块 operator new(0x200=512B)
- [x] **ASM-79-list**：每元素 operator new 24B 节点、遍历纯 next 指针追逐、缓存局部性差
- [x] **ASM-79-fwdlist**：无 size 成员(O(n))、before_begin 哨兵、insert_after 单指针改写
- [x] **ASM-84-set**：operator new(0x28=40B)红黑树节点、find 比较键@0x20追逐左/右指针
- [x] **ASM-85-uset**：div 取桶+next 单链比较值@0x08、rehash O(n)全量迁移
- [x] **ASM-86-pq**：push_heap 上浮环(sar除2+cmp+交换)、top=c.front()单load
- [x] **ASM-86-adapters**：stack::top=deque::back、queue::front=直接读首元素指针
- [x] **ASM-89-any**：≤16B SBO 内联零堆、>16B _Manager_external+operator new、any_cast内联typeid

### 批 K：关联容器（map / unordered_map）
- [x] **ASM-83-map**：`build()` 三次 `call _M_emplace_hint_unique`（每元素 `operator new` 节点）；`find_it` 沿 `+0x10`左/`+0x18`右指针追逐比较键`@0x20`，O(log n)
- [x] **ASM-85-unordered**：`build()` 节点堆分配+桶数组（`max_load_factor=0x3f800000`）；`find_it` 先 `div r11` 取桶索引再沿 `+0x00` next 单链表比较键`@0x08`

---

## 三、使用与维护约定
- 新增实证：先写 `_asm_demo/ASM-<章>-<机制>.cpp`，`g++ -std=c++26 -O2 -c` 编 `.o` 再 `objdump -d -M intel -C` 提取；`.s` 产物一并提交（`.o`/`.exe` 被 `.gitignore` 忽略）。
- 嵌入章：在目标章末尾"附录"小节放**结论 + 关键汇编片段**，正文不扩写。
- 更新：每完成一批，更新本索引"已覆盖"表、STATE.json `assembly_empirical_examples`、并在 `_asm_demo/` 保留 `.cpp`/`.s`。
- 红线校验：`python3 tools/consistency_check.py` 必须 0/0；所有汇编均真机产物，不手绘。
