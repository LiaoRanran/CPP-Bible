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

## 一、已覆盖实证（累计 27 例，STATE 记录）

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

> 方向 1 早期另有 `unique_ptr`(ch41)、`vtable`(ch47) 等以**章内联片段**形式存在的实证，不重复计入本文件清单；总计数以 STATE.json `assembly_empirical_examples` 为准（当前 18）。

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
- [ ] ASM-47-vs-51：虚函数调用（`call [vtable+off]` 间接调用）vs CRTP 静态分发（直接 `call`）的指令数/间接跳转对比
- [ ] ASM-88-variant：`std::variant` 访问（`std::visit`）的类型索引分派 vs `virtual` 虚调用

### 批 E：分配与 PMR
- [ ] ASM-122-pmr：`std::pmr` 多态分配器（资源句柄）vs 默认 `new` 的分配路径差异

### 批 F：类型擦除
- [ ] ASM-std_function：`std::function` 类型擦除的间接调用 + 小对象优化 vs 模板/CRTP 静态内联

---

## 三、使用与维护约定
- 新增实证：先写 `_asm_demo/ASM-<章>-<机制>.cpp`，`g++ -std=c++26 -O2 -c` 编 `.o` 再 `objdump -d -M intel -C` 提取；`.s` 产物一并提交（`.o`/`.exe` 被 `.gitignore` 忽略）。
- 嵌入章：在目标章末尾"附录"小节放**结论 + 关键汇编片段**，正文不扩写。
- 更新：每完成一批，更新本索引"已覆盖"表、STATE.json `assembly_empirical_examples`、并在 `_asm_demo/` 保留 `.cpp`/`.s`。
- 红线校验：`python3 tools/consistency_check.py` 必须 0/0；所有汇编均真机产物，不手绘。
