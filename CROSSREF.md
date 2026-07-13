# CROSSREF.md — 《现代 C++ 终极圣经》全局章节依赖索引

> **自动生成文档 · 2026-07-11 12:20:51 · 禁止手改**

本文件由 `tools/gen_crossref.py` 从各章内嵌交叉引用抽取生成，是独立于正文的**导航/速查件**（非 `chXXX.md`，不计入一致性门禁）。重生成命令：

```bash
python tools/gen_crossref.py
```

## 0. 速读说明

- **章节总数**：147
- **依赖边总数**（出链去重后）：732
- **有出链的章**：147 ｜ **有入链的章**：146
- **含策展 `前置/后续` 字段的章**：40
- **断链**：0（应为 0）

**三类引用来源**：
1. 箭头链接 `⟶ Book/...chYY.md`（145 章）
2. 反引号链接 `` `Book/...chYY.md` ``（44 章）
3. 策展元数据 `> ...｜前置：…｜后续：…｜`（39 章，权威学习路径）

**出链** = 本章主动指向的章；**入链** = 指向本章的章（即「本章是哪些章的前置」）。

## 1. Part 总览

| Part | 章数 | 章节范围 |
|---|---|---|
| `part01_history` | 10 | ch01–ch10 |
| `part02_toolchain` | 8 | ch11–ch18 |
| `part03_language` | 14 | ch19–ch32 |
| `part04_memory` | 10 | ch35–ch44 |
| `part05_oo` | 8 | ch45–ch52 |
| `part06_templates` | 13 | ch60–ch72 |
| `part07_stl` | 19 | ch76–ch94 |
| `part08_algorithms` | 7 | ch95–ch101 |
| `part09_concurrency` | 7 | ch107–ch113 |
| `part10_modern` | 9 | ch115–ch123 |
| `part11_source` | 11 | ch124–ch134 |
| `part12_patterns` | 9 | ch135–ch143 |
| `part13_engineering` | 8 | ch144–ch151 |
| `part14_perf` | 7 | ch152–ch158 |
| `part15_cases` | 6 | ch159–ch164 |
| `part16_reading` | 1 | ch165–ch165 |

## 2. 全局依赖速查主表

> 行序按章号。点击 `chXX 标题` 直达正文；`出链/入链` 为该章依赖边数。

| 章 | 标题 | Part | 出链 | 入链 | 策展前置 | 策展后续 |
|---|---|---|---:|---:|---|---|
| [ch01](Book/part01_history/ch01_c_history.md) | C 语言遗产与 C with Classes | `part01_history` | 3 | 4 | — | ch02、ch19、ch50 |
| [ch02](Book/part01_history/ch02_standardization.md) | 标准化组织、WG21 与提案流程 | `part01_history` | 4 | 2 | — | — |
| [ch03](Book/part01_history/ch03_cpp98_03.md) | C++98 / C++03：奠基时代 | `part01_history` | 5 | 2 | — | — |
| [ch04](Book/part01_history/ch04_cpp11.md) | C++11：现代 C++ 革命 | `part01_history` | 4 | 4 | ch01、ch02、ch03 | ch21、ch22、ch27、ch31、ch48、ch69、ch93、ch107、ch115、ch116 |
| [ch05](Book/part01_history/ch05_cpp14.md) | C++14：小幅完善 | `part01_history` | 4 | 4 | ch04 | ch27、ch48、ch63、ch69 |
| [ch06](Book/part01_history/ch06_cpp17.md) | C++17：生产力跃升 | `part01_history` | 4 | 4 | ch04、ch05 | ch26、ch32、ch33、ch64、ch81、ch82、ch88、ch91、ch99 |
| [ch07](Book/part01_history/ch07_cpp20.md) | C++20：量级升级 | `part01_history` | 4 | 4 | ch04、ch05、ch06、ch60、ch63 | ch21、ch25、ch32、ch67、ch90、ch113、ch118、ch119、ch120 |
| [ch08](Book/part01_history/ch08_cpp23.md) | C++23：标准库大修 | `part01_history` | 4 | 5 | ch04、ch05、ch06、ch07 | ch34、ch82、ch88、ch90、ch131 |
| [ch09](Book/part01_history/ch09_cpp26.md) | C++26：已确定特性与方向 | `part01_history` | 4 | 3 | ch07、ch67、ch113、ch114 | ch74、ch114、ch121 |
| [ch10](Book/part01_history/ch10_version_matrix.md) | 版本特性全景对照表与迁移指南 | `part01_history` | 3 | 1 | ch03、ch04、ch05、ch06、ch07、ch08、ch09 | — |
| [ch11](Book/part02_toolchain/ch11_compilers.md) | 编译器全景：GCC / Clang / MSVC 架构与 ABI（C++） | `part02_toolchain` | 3 | 6 | — | — |
| [ch12](Book/part02_toolchain/ch12_buildsystems.md) | 构建系统：Make / Ninja / CMake（C++） | `part02_toolchain` | 3 | 4 | — | — |
| [ch13](Book/part02_toolchain/ch13_packaging.md) | 包管理：vcpkg / Conan（C++） | `part02_toolchain` | 3 | 2 | — | — |
| [ch14](Book/part02_toolchain/ch14_debugging.md) | 调试与诊断：GDB / LLDB / Sanitizer / Valgrind（C++） | `part02_toolchain` | 5 | 3 | — | — |
| [ch15](Book/part02_toolchain/ch15_profiling.md) | 性能分析：perf / VTune / 火焰图 / Compiler Explorer（C++） | `part02_toolchain` | 4 | 3 | — | — |
| [ch16](Book/part02_toolchain/ch16_ide.md) | IDE 与编辑器：VSCode / CLion / QtCreator / VIM（C++） | `part02_toolchain` | 4 | 3 | — | — |
| [ch17](Book/part02_toolchain/ch17_crosscompile.md) | 交叉编译与嵌入式工具链（C++） | `part02_toolchain` | 4 | 3 | — | — |
| [ch18](Book/part02_toolchain/ch18_buildconfig.md) | 构建配置：Debug / Release / LTO / PGO（C++） | `part02_toolchain` | 3 | 4 | — | — |
| [ch19](Book/part03_language/ch19_variables.md) | 变量、存储期、链接与 ODR（工业级深度版） | `part03_language` | 5 | 19 | ch01、ch10、ch20、ch31 | ch21、ch32、ch33、ch35、ch60、ch102 |
| [ch20](Book/part03_language/ch20_reference_pointer.md) | 引用（reference）vs 指针（pointer）：语义本质、底层实现与生命周期战争 | `part03_language` | 5 | 12 | ch19 | ch21、ch31、ch33、ch52、ch77、ch89、ch94、ch115、ch116、ch154、ch157 |
| [ch21](Book/part03_language/ch21_const_family.md) | const / constexpr / consteval / constinit 深度详解 | `part03_language` | 4 | 5 | ch19、ch20 | — |
| [ch22](Book/part03_language/ch22_auto_decltype.md) | 第 22 章 · `auto` 类型推导、`decltype` 与返回类型推导 | `part03_language` | 4 | 2 | — | — |
| [ch23](Book/part03_language/ch23_namespace_adl.md) | 命名空间（namespace）、using 与参数依赖查找（ADL）：隔离、版本化与隐形查找 | `part03_language` | 4 | 3 | ch19 | ch21、ch31、ch60、ch62、ch119 |
| [ch24](Book/part03_language/ch24_enum.md) | 第 24 章 枚举（枚举类型全解：unscoped / enum class / 位掩码 / ABI / 反射） | `part03_language` | 4 | 2 | — | — |
| [ch25](Book/part03_language/ch25_union_variant.md) | union 与 std::variant 深度详解 | `part03_language` | 4 | 2 | ch19、ch20、ch21、ch34、ch59、ch115 | — |
| [ch26](Book/part03_language/ch26_lambda.md) | lambda 表达式全解：闭包类型、捕获、泛型/模板 lambda、constexpr、ABI 与 std::function 类型擦除 | `part03_language` | 4 | 6 | ch19、ch20、ch21、ch22、ch59、ch80、ch115、ch116 | ch27、ch52、ch115、ch116、ch154 |
| [ch27](Book/part03_language/ch27_cast.md) | 显式转型四兄弟与隐式转换：const_cast / static_cast / dynamic_cast / reinterpret_cast 深度详解 | `part03_language` | 4 | 5 | ch19、ch20、ch21、ch60 | ch31、ch42、ch65 |
| [ch28](Book/part03_language/ch28_lifetime_ub.md) | 对象生命周期与未定义行为（UB）：生存期、悬垂、UB 分类与编译器武器化 | `part03_language` | 5 | 3 | ch19、ch20、ch21、ch25、ch27、ch31、ch33、ch42、ch61 | ch42、ch61 |
| [ch29](Book/part03_language/ch29_friend.md) | 友元 friend 与访问控制 | `part03_language` | 8 | 6 | ch46 | — |
| [ch30](Book/part03_language/ch30_volatile.md) | volatile / atomic 与硬件寄存器 | `part03_language` | 7 | 6 | — | — |
| [ch31](Book/part03_language/ch31_operator_overloading.md) | 运算符重载 | `part03_language` | 6 | 5 | — | — |
| [ch32](Book/part03_language/ch32_initialization.md) | 初始化与列表初始化 | `part03_language` | 6 | 6 | — | — |
| [ch35](Book/part04_memory/ch35_memory_layout.md) | 第 35 章  C++ 程序的内存模型与操作系统视角 | `part04_memory` | 3 | 5 | — | — |
| [ch36](Book/part04_memory/ch36_stack_heap.md) | 第 36 章 栈（stack）与堆（heap）的深度对比 | `part04_memory` | 3 | 4 | — | — |
| [ch37](Book/part04_memory/ch37_new_delete.md) | 第 37 章 动态内存分配原语：`operator new` / `operator delete` | `part04_memory` | 4 | 5 | — | — |
| [ch38](Book/part04_memory/ch38_allocator.md) | 第 38 章 分配器（Allocator）模型与 PMR | `part04_memory` | 4 | 6 | — | — |
| [ch39](Book/part04_memory/ch39_raii_rule.md) | 第 39 章 RAII 与 Rule of Zero/Three/Five | `part04_memory` | 3 | 12 | — | — |
| [ch40](Book/part04_memory/ch40_exception_safety.md) | 第 40 章 异常安全（Exception Safety） | `part04_memory` | 7 | 7 | — | — |
| [ch41](Book/part04_memory/ch41_smart_pointers.md) | 第 41 章 智能指针全解（unique_ptr / shared_ptr / weak_ptr / enable_shared_from_this） | `part04_memory` | 5 | 2 | — | — |
| [ch42](Book/part04_memory/ch42_strict_aliasing.md) | 第 42 章 · 严格别名规则（Strict Aliasing）与编译器优化 | `part04_memory` | 5 | 3 | — | — |
| [ch43](Book/part04_memory/ch43_cache_locality.md) | 第 43 章 CPU 缓存体系与内存局部性 | `part04_memory` | 4 | 5 | — | — |
| [ch44](Book/part04_memory/ch44_memory_pool.md) | 第 44 章 内存池（Memory Pool）从零实现 | `part04_memory` | 3 | 3 | — | — |
| [ch45](Book/part05_oo/ch45_oop_object_model.md) | 第 45 章 C++ 面向对象总览与对象模型基础 | `part05_oo` | 3 | 8 | — | — |
| [ch46](Book/part05_oo/ch46_encapsulation_inheritance.md) | 第 46 章 封装与继承深度：访问控制、三种继承、切片、构造/析构、名字隐藏、override/final、NVI | `part05_oo` | 3 | 4 | — | — |
| [ch47](Book/part05_oo/ch47_virtual_functions.md) | 虚函数与虚表（vtable）：动态多态的发动机 | `part05_oo` | 4 | 8 | — | — |
| [ch48](Book/part05_oo/ch48_rtti.md) | RTTI 与 typeid/dynamic_cast：运行时类型查询 | `part05_oo` | 3 | 3 | — | — |
| [ch49](Book/part05_oo/ch49_virtual_inheritance.md) | 虚继承与菱形继承：共享虚基类 | `part05_oo` | 3 | 3 | — | — |
| [ch50](Book/part05_oo/ch50_multiple_inheritance.md) | 多重继承与对象模型（Multiple Inheritance） | `part05_oo` | 3 | 3 | — | ch14、ch19、ch45、ch46、ch47、ch48、ch49、ch51 |
| [ch51](Book/part05_oo/ch51_crtp.md) | CRTP 与静态多态（Curiously Recurring Template Pattern） | `part05_oo` | 4 | 6 | — | ch47、ch50、ch62、ch67、ch69、ch73 |
| [ch52](Book/part05_oo/ch52_ebo.md) | 空基类优化 EBO（Empty Base Optimization） | `part05_oo` | 4 | 4 | — | ch19、ch41、ch45、ch50、ch71 |
| [ch60](Book/part06_templates/ch60_template_basics.md) | 模板基础与实例化（Template Basics & Instantiation） | `part06_templates` | 3 | 5 | — | — |
| [ch61](Book/part06_templates/ch61_template_overload.md) | 函数模板重载决议（Function Template Overload Resolution） | `part06_templates` | 4 | 3 | — | — |
| [ch62](Book/part06_templates/ch62_specialization.md) | 类模板特化与偏特化（Class Template Specialization） | `part06_templates` | 4 | 2 | — | — |
| [ch63](Book/part06_templates/ch63_variadic.md) | 可变参数模板与包展开（Variadic Templates & Pack Expansion） | `part06_templates` | 3 | 8 | — | — |
| [ch64](Book/part06_templates/ch64_fold.md) | 折叠表达式 Fold Expression（C++17） | `part06_templates` | 3 | 4 | — | — |
| [ch65](Book/part06_templates/ch65_type_traits.md) | 类型特性 Type Traits —— 编译期类型自省与分发 | `part06_templates` | 3 | 16 | — | — |
| [ch66](Book/part06_templates/ch66_sfinae.md) | SFINAE 与 std::enable_if —— 替换失败非错误的编译期分发 | `part06_templates` | 2 | 3 | — | — |
| [ch67](Book/part06_templates/ch67_concepts.md) | Concepts 与 requires —— C++20 的编译期约束 | `part06_templates` | 3 | 8 | — | — |
| [ch68](Book/part06_templates/ch68_tmp.md) | 模板元编程 TMP 基础（递归 / 分支 / 循环） | `part06_templates` | 3 | 8 | — | — |
| [ch69](Book/part06_templates/ch69_constexpr.md) | 编译期计算：constexpr / consteval / constinit | `part06_templates` | 3 | 9 | — | — |
| [ch70](Book/part06_templates/ch70_tag_dispatch.md) | std::integral_constant 与标签分发（Tag Dispatch） | `part06_templates` | 4 | 2 | — | — |
| [ch71](Book/part06_templates/ch71_policy.md) | 策略设计 Policy-Based Design | `part06_templates` | 4 | 4 | — | — |
| [ch72](Book/part06_templates/ch72_expression_templates.md) | 表达式模板 Expression Templates | `part06_templates` | 3 | 1 | — | — |
| [ch76](Book/part07_stl/ch76_stl_arch.md) | STL 架构与迭代器概念 | `part07_stl` | 13 | 10 | ch19、ch60、ch67 | ch77、ch84、ch85 |
| [ch77](Book/part07_stl/ch77_vector.md) | vector：扩容、失效、allocator 协作 | `part07_stl` | 10 | 21 | ch37、ch38、ch76 | ch78、ch84、ch154 |
| [ch78](Book/part07_stl/ch78_deque.md) | deque 与分段连续 [标准] | `part07_stl` | 10 | 3 | ch63、ch76、ch77、ch79、ch86、ch90 | ch79、ch86、ch90 |
| [ch79](Book/part07_stl/ch79_list.md) | list / forward_list [标准] | `part07_stl` | 9 | 5 | ch76、ch77、ch78、ch86、ch90 | ch86、ch90 |
| [ch80](Book/part07_stl/ch80_array.md) | array 与固定数组 | `part07_stl` | 6 | 6 | ch19、ch20、ch77、ch81、ch82、ch90 | ch77、ch81、ch90 |
| [ch81](Book/part07_stl/ch81_string.md) | std::string 与 SSO 短字符串优化 | `part07_stl` | 7 | 4 | — | — |
| [ch82](Book/part07_stl/ch82_span.md) | span 与裸数组视图 | `part07_stl` | 9 | 3 | ch20、ch77、ch80、ch83、ch90 | ch83、ch90 |
| [ch83](Book/part07_stl/ch83_map.md) | map / multimap（红黑树） | `part07_stl` | 10 | 7 | ch20、ch76、ch80、ch84、ch85、ch90 | ch84、ch85、ch90 |
| [ch84](Book/part07_stl/ch84_set.md) | set / multiset：红黑树有序集合 | `part07_stl` | 9 | 5 | ch19、ch65、ch83 | ch85、ch154 |
| [ch85](Book/part07_stl/ch85_unordered.md) | unordered_map / unordered_set：哈希开链集合 | `part07_stl` | 7 | 4 | ch19、ch65、ch84 | ch124、ch154 |
| [ch86](Book/part07_stl/ch86_adapters.md) | 容器适配器：stack / queue / priority_queue | `part07_stl` | 13 | 4 | ch76、ch77、ch78 | ch19、ch88、ch98 |
| [ch87](Book/part07_stl/ch87_bitset.md) | bitset：编译期定长位集 | `part07_stl` | 8 | 3 | ch65、ch77、ch80 | ch88、ch124、ch155 |
| [ch88](Book/part07_stl/ch88_optional_variant.md) | optional / expected / variant：可空与可辨别联合 | `part07_stl` | 7 | 13 | — | — |
| [ch89](Book/part07_stl/ch89_tuple_any.md) | tuple / pair / any / function / bind | `part07_stl` | 9 | 2 | — | — |
| [ch90](Book/part07_stl/ch90_ranges.md) | ranges 与 views：惰性求值与管道组合 | `part07_stl` | 8 | 10 | — | — |
| [ch91](Book/part07_stl/ch91_filesystem.md) | 文件系统 filesystem | `part07_stl` | 12 | 4 | ch19、ch39、ch47 | ch92、ch122 |
| [ch92](Book/part07_stl/ch92_chrono.md) | 时间库 chrono | `part07_stl` | 15 | 2 | ch19、ch39、ch47 | ch91、ch151、ch152 |
| [ch93](Book/part07_stl/ch93_thread_async.md) | 线程与异步：thread / future / async | `part07_stl` | 9 | 6 | ch19、ch63、ch93、ch94、ch107 | ch93、ch94、ch107 |
| [ch94](Book/part07_stl/ch94_stop_token.md) | stop_token 与协作取消 [标准] | `part07_stl` | 5 | 1 | ch93、ch107 | ch93 |
| [ch95](Book/part08_algorithms/ch95_algo_overview.md) | STL 算法分类与复杂度（C++） | `part08_algorithms` | 3 | 9 | — | — |
| [ch96](Book/part08_algorithms/ch96_sorting.md) | 排序：sort / stable_sort / partial_sort（C++） | `part08_algorithms` | 4 | 6 | — | — |
| [ch97](Book/part08_algorithms/ch97_search.md) | 查找与二分（C++） | `part08_algorithms` | 3 | 3 | — | — |
| [ch98](Book/part08_algorithms/ch98_heap.md) | 堆算法 heap（C++） | `part08_algorithms` | 3 | 4 | — | — |
| [ch99](Book/part08_algorithms/ch99_numeric.md) | 数值算法与并行执行策略（C++） | `part08_algorithms` | 4 | 2 | — | — |
| [ch100](Book/part08_algorithms/ch100_ranges_algo.md) | Ranges 算法与投影（C++20） | `part08_algorithms` | 4 | 4 | — | — |
| [ch101](Book/part08_algorithms/ch101_algo_theory.md) | 哈希、图、树、DP、贪心（算法思想） | `part08_algorithms` | 3 | 1 | — | — |
| [ch107](Book/part09_concurrency/ch107_atomic.md) | std::atomic 原子类型（C++11） | `part09_concurrency` | 5 | 12 | — | — |
| [ch108](Book/part09_concurrency/ch108_memory_order.md) | memory_order：六种内存序（C++11） | `part09_concurrency` | 3 | 6 | — | — |
| [ch109](Book/part09_concurrency/ch109_fence.md) | 内存屏障与 fence | `part09_concurrency` | 3 | 4 | — | — |
| [ch110](Book/part09_concurrency/ch110_lockfree.md) | 无锁编程：lock-free / wait-free（C++11） | `part09_concurrency` | 7 | 6 | — | — |
| [ch111](Book/part09_concurrency/ch111_aba.md) | ABA 问题与解决（C++11） | `part09_concurrency` | 6 | 3 | — | — |
| [ch112](Book/part09_concurrency/ch112_hazard_rcu.md) | Hazard Pointer 与 RCU（C++11/实践） | `part09_concurrency` | 3 | 3 | — | — |
| [ch113](Book/part09_concurrency/ch113_coroutine.md) | 协程 coroutine：promise / awaiter（C++20） | `part09_concurrency` | 3 | 5 | — | — |
| [ch115](Book/part10_modern/ch115_move.md) | 移动语义与右值引用 | `part10_modern` | 7 | 17 | ch19、ch20、ch27、ch39、ch77、ch116、ch117 | ch27、ch116、ch117 |
| [ch116](Book/part10_modern/ch116_perfect_forwarding.md) | 完美转发与万能引用 | `part10_modern` | 7 | 9 | ch20、ch63、ch115 | ch107、ch117、ch122 |
| [ch117](Book/part10_modern/ch117_copy_elision.md) | RVO / NRVO 与拷贝消除（C++17） | `part10_modern` | 5 | 4 | — | — |
| [ch118](Book/part10_modern/ch118_modules.md) | Modules 模块（C++20） | `part10_modern` | 5 | 4 | — | — |
| [ch119](Book/part10_modern/ch119_ranges_deep.md) | Ranges 深入（C++20） | `part10_modern` | 7 | 9 | — | — |
| [ch120](Book/part10_modern/ch120_coroutine_app.md) | Coroutine 应用模式 | `part10_modern` | 7 | 6 | ch113、ch120 | ch120 |
| [ch121](Book/part10_modern/ch121_contracts.md) | Contracts 契约（方向，C++26） | `part10_modern` | 7 | 5 | ch120、ch122 | ch122 |
| [ch122](Book/part10_modern/ch122_pmr.md) | PMR 与多态分配器 | `part10_modern` | 14 | 10 | ch37、ch38、ch47 | ch38、ch44、ch121、ch154 |
| [ch123](Book/part10_modern/ch123_ct_programming.md) | Compile-Time 编程范式总览 | `part10_modern` | 12 | 4 | — | — |
| [ch124](Book/part11_source/ch124_libstdcxx.md) | libstdc++ 架构与阅读入口（C++） | `part11_source` | 3 | 7 | — | — |
| [ch125](Book/part11_source/ch125_libcxx.md) | libc++ 架构（C++） | `part11_source` | 6 | 4 | — | — |
| [ch126](Book/part11_source/ch126_msstl.md) | MS STL 架构（C++） | `part11_source` | 3 | 3 | — | — |
| [ch127](Book/part11_source/ch127_llvm.md) | LLVM / Clang 架构（C++） | `part11_source` | 4 | 3 | — | — |
| [ch128](Book/part11_source/ch128_boost.md) | Boost 核心库（C++） | `part11_source` | 4 | 4 | — | — |
| [ch129](Book/part11_source/ch129_qt.md) | Qt 对象模型与信号槽（C++） | `part11_source` | 4 | 3 | — | — |
| [ch130](Book/part11_source/ch130_chromium_abseil.md) | Chromium / Abseil 基础设施（C++） | `part11_source` | 3 | 2 | — | — |
| [ch131](Book/part11_source/ch131_fmt_spdlog.md) | fmt / spdlog 格式化与日志（C++） | `part11_source` | 7 | 5 | — | — |
| [ch132](Book/part11_source/ch132_leveldb_rocksdb.md) | LevelDB / RocksDB 存储引擎（C++） | `part11_source` | 4 | 2 | — | — |
| [ch133](Book/part11_source/ch133_clickhouse_redis.md) | ClickHouse / Redis 实现精读（C++） | `part11_source` | 3 | 3 | — | — |
| [ch134](Book/part11_source/ch134_unreal.md) | Unreal Engine C++ 架构（C++） | `part11_source` | 3 | 1 | — | — |
| [ch135](Book/part12_patterns/ch135_patterns_intro.md) | 设计模式总论（C++） | `part12_patterns` | 3 | 7 | — | — |
| [ch136](Book/part12_patterns/ch136_creational.md) | 创建型模式（C++） | `part12_patterns` | 3 | 2 | — | — |
| [ch137](Book/part12_patterns/ch137_structural.md) | 结构型模式（C++） | `part12_patterns` | 4 | 3 | — | — |
| [ch138](Book/part12_patterns/ch138_behavioral.md) | 行为型模式（C++） | `part12_patterns` | 3 | 3 | — | — |
| [ch139](Book/part12_patterns/ch139_crtp_pattern.md) | CRTP 与静态多态（C++） | `part12_patterns` | 4 | 2 | — | — |
| [ch140](Book/part12_patterns/ch140_policy_pattern.md) | Policy-Based Design（C++） | `part12_patterns` | 4 | 4 | — | — |
| [ch141](Book/part12_patterns/ch141_di.md) | 依赖注入（C++） | `part12_patterns` | 4 | 5 | — | — |
| [ch142](Book/part12_patterns/ch142_ecs.md) | 实体组件系统 ECS（C++） | `part12_patterns` | 3 | 5 | — | — |
| [ch143](Book/part12_patterns/ch143_dod.md) | 面向数据设计 DOD（C++） | `part12_patterns` | 6 | 3 | — | — |
| [ch144](Book/part13_engineering/ch144_style.md) | 代码风格与规范（C++） | `part13_engineering` | 7 | 5 | — | — |
| [ch145](Book/part13_engineering/ch145_naming_api.md) | 命名与 API 设计（C++） | `part13_engineering` | 3 | 3 | — | — |
| [ch146](Book/part13_engineering/ch146_error_handling.md) | 错误处理（C++） | `part13_engineering` | 4 | 5 | — | — |
| [ch147](Book/part13_engineering/ch147_code_review.md) | 代码审查（C++） | `part13_engineering` | 4 | 4 | — | — |
| [ch148](Book/part13_engineering/ch148_gitflow.md) | Git 工作流（C++） | `part13_engineering` | 3 | 3 | — | — |
| [ch149](Book/part13_engineering/ch149_ci_cd.md) | CI/CD 流水线（C++） | `part13_engineering` | 6 | 3 | — | — |
| [ch150](Book/part13_engineering/ch150_testing.md) | 测试策略（C++） | `part13_engineering` | 3 | 4 | — | — |
| [ch151](Book/part13_engineering/ch151_benchmark.md) | 基准测试与性能度量（C++） | `part13_engineering` | 3 | 6 | — | — |
| [ch152](Book/part14_perf/ch152_perf_model.md) | 性能模型与测量学 | `part14_perf` | 7 | 11 | — | — |
| [ch153](Book/part14_perf/ch153_cpu_micro.md) | CPU 微架构：流水线 / 分支预测 / 乱序执行 | `part14_perf` | 10 | 4 | — | — |
| [ch154](Book/part14_perf/ch154_cache_opt.md) | 缓存优化与数据局部性（C++/硬件） | `part14_perf` | 3 | 11 | — | — |
| [ch155](Book/part14_perf/ch155_simd.md) | SIMD / AVX 向量化（C++/硬件） | `part14_perf` | 7 | 7 | — | — |
| [ch156](Book/part14_perf/ch156_compiler_opt.md) | 编译器优化：O2/O3/Ofast/LTO/PGO（GCC） | `part14_perf` | 5 | 6 | — | — |
| [ch157](Book/part14_perf/ch157_compiler_explorer.md) | Compiler Explorer 实战 | `part14_perf` | 7 | 8 | — | — |
| [ch158](Book/part14_perf/ch158_perf_antipatterns.md) | 性能反模式与陷阱 | `part14_perf` | 7 | 4 | — | — |
| [ch159](Book/part15_cases/ch159_threadpool.md) | 从零实现线程池（C++） | `part15_cases` | 3 | 8 | — | — |
| [ch160](Book/part15_cases/ch160_mempool.md) | 从零实现内存池（C++） | `part15_cases` | 3 | 5 | — | — |
| [ch161](Book/part15_cases/ch161_logger.md) | 从零实现日志库（C++） | `part15_cases` | 4 | 3 | — | — |
| [ch162](Book/part15_cases/ch162_json.md) | 从零实现 JSON 库（C++） | `part15_cases` | 4 | 2 | — | — |
| [ch163](Book/part15_cases/ch163_net.md) | 从零实现网络编程（C++） | `part15_cases` | 4 | 2 | — | — |
| [ch164](Book/part15_cases/ch164_framework.md) | 从零实现迷你框架（C++） | `part15_cases` | 3 | 1 | — | — |
| [ch165](Book/part16_reading/ch165_roadmap.md) | C++ 进阶路线图（C++） | `part16_reading` | 5 | 0 | — | — |

## 3. 依赖明细（出链 / 入链 / 策展路径）

> 每章一个小节；`出链` 为本章指向，`入链` 为指向本章（反向依赖）。

### ch01 · C 语言遗产与 C with Classes

- 文件：`Book/part01_history/ch01_c_history.md` ｜ Part：`part01_history`
- **出链**（本章指向）：
  [ch02 标准化组织、WG21 与提案流程](Book/part01_history/ch02_standardization.md)、[ch19 变量、存储期、链接与 ODR（工业级深度版）](Book/part03_language/ch19_variables.md)、[ch32 初始化与列表初始化](Book/part03_language/ch32_initialization.md)
- **入链**（指向本章）：
  [ch02 标准化组织、WG21 与提案流程](Book/part01_history/ch02_standardization.md)、[ch03 C++98 / C++03：奠基时代](Book/part01_history/ch03_cpp98_03.md)、[ch32 初始化与列表初始化](Book/part03_language/ch32_initialization.md)、[ch165 C++ 进阶路线图（C++）](Book/part16_reading/ch165_roadmap.md)
- **策展路径**：前置 无 ｜ 后续 ch02、ch19、ch50

### ch02 · 标准化组织、WG21 与提案流程

- 文件：`Book/part01_history/ch02_standardization.md` ｜ Part：`part01_history`
- **出链**（本章指向）：
  [ch01 C 语言遗产与 C with Classes](Book/part01_history/ch01_c_history.md)、[ch03 C++98 / C++03：奠基时代](Book/part01_history/ch03_cpp98_03.md)、[ch04 C++11：现代 C++ 革命](Book/part01_history/ch04_cpp11.md)、[ch05 C++14：小幅完善](Book/part01_history/ch05_cpp14.md)
- **入链**（指向本章）：
  [ch01 C 语言遗产与 C with Classes](Book/part01_history/ch01_c_history.md)、[ch03 C++98 / C++03：奠基时代](Book/part01_history/ch03_cpp98_03.md)

### ch03 · C++98 / C++03：奠基时代

- 文件：`Book/part01_history/ch03_cpp98_03.md` ｜ Part：`part01_history`
- **出链**（本章指向）：
  [ch01 C 语言遗产与 C with Classes](Book/part01_history/ch01_c_history.md)、[ch02 标准化组织、WG21 与提案流程](Book/part01_history/ch02_standardization.md)、[ch04 C++11：现代 C++ 革命](Book/part01_history/ch04_cpp11.md)、[ch05 C++14：小幅完善](Book/part01_history/ch05_cpp14.md)、[ch06 C++17：生产力跃升](Book/part01_history/ch06_cpp17.md)
- **入链**（指向本章）：
  [ch02 标准化组织、WG21 与提案流程](Book/part01_history/ch02_standardization.md)、[ch04 C++11：现代 C++ 革命](Book/part01_history/ch04_cpp11.md)

### ch04 · C++11：现代 C++ 革命

- 文件：`Book/part01_history/ch04_cpp11.md` ｜ Part：`part01_history`
- **出链**（本章指向）：
  [ch03 C++98 / C++03：奠基时代](Book/part01_history/ch03_cpp98_03.md)、[ch05 C++14：小幅完善](Book/part01_history/ch05_cpp14.md)、[ch63 可变参数模板与包展开（Variadic Templates & Pack Expansion）](Book/part06_templates/ch63_variadic.md)、[ch115 移动语义与右值引用](Book/part10_modern/ch115_move.md)
- **入链**（指向本章）：
  [ch02 标准化组织、WG21 与提案流程](Book/part01_history/ch02_standardization.md)、[ch03 C++98 / C++03：奠基时代](Book/part01_history/ch03_cpp98_03.md)、[ch05 C++14：小幅完善](Book/part01_history/ch05_cpp14.md)、[ch10 版本特性全景对照表与迁移指南](Book/part01_history/ch10_version_matrix.md)
- **策展路径**：前置 ch01、ch02、ch03 ｜ 后续 ch21、ch22、ch27、ch31、ch48、ch69、ch93、ch107、ch115、ch116

### ch05 · C++14：小幅完善

- 文件：`Book/part01_history/ch05_cpp14.md` ｜ Part：`part01_history`
- **出链**（本章指向）：
  [ch04 C++11：现代 C++ 革命](Book/part01_history/ch04_cpp11.md)、[ch06 C++17：生产力跃升](Book/part01_history/ch06_cpp17.md)、[ch69 编译期计算：constexpr / consteval / constinit](Book/part06_templates/ch69_constexpr.md)、[ch115 移动语义与右值引用](Book/part10_modern/ch115_move.md)
- **入链**（指向本章）：
  [ch02 标准化组织、WG21 与提案流程](Book/part01_history/ch02_standardization.md)、[ch03 C++98 / C++03：奠基时代](Book/part01_history/ch03_cpp98_03.md)、[ch04 C++11：现代 C++ 革命](Book/part01_history/ch04_cpp11.md)、[ch06 C++17：生产力跃升](Book/part01_history/ch06_cpp17.md)
- **策展路径**：前置 ch04 ｜ 后续 ch27、ch48、ch63、ch69

### ch06 · C++17：生产力跃升

- 文件：`Book/part01_history/ch06_cpp17.md` ｜ Part：`part01_history`
- **出链**（本章指向）：
  [ch05 C++14：小幅完善](Book/part01_history/ch05_cpp14.md)、[ch07 C++20：量级升级](Book/part01_history/ch07_cpp20.md)、[ch64 折叠表达式 Fold Expression（C++17）](Book/part06_templates/ch64_fold.md)、[ch88 optional / expected / variant：可空与可辨别联合](Book/part07_stl/ch88_optional_variant.md)
- **入链**（指向本章）：
  [ch03 C++98 / C++03：奠基时代](Book/part01_history/ch03_cpp98_03.md)、[ch05 C++14：小幅完善](Book/part01_history/ch05_cpp14.md)、[ch07 C++20：量级升级](Book/part01_history/ch07_cpp20.md)、[ch88 optional / expected / variant：可空与可辨别联合](Book/part07_stl/ch88_optional_variant.md)
- **策展路径**：前置 ch04、ch05 ｜ 后续 ch26、ch32、ch33、ch64、ch81、ch82、ch88、ch91、ch99

### ch07 · C++20：量级升级

- 文件：`Book/part01_history/ch07_cpp20.md` ｜ Part：`part01_history`
- **出链**（本章指向）：
  [ch06 C++17：生产力跃升](Book/part01_history/ch06_cpp17.md)、[ch08 C++23：标准库大修](Book/part01_history/ch08_cpp23.md)、[ch67 Concepts 与 requires —— C++20 的编译期约束](Book/part06_templates/ch67_concepts.md)、[ch119 Ranges 深入（C++20）](Book/part10_modern/ch119_ranges_deep.md)
- **入链**（指向本章）：
  [ch06 C++17：生产力跃升](Book/part01_history/ch06_cpp17.md)、[ch08 C++23：标准库大修](Book/part01_history/ch08_cpp23.md)、[ch10 版本特性全景对照表与迁移指南](Book/part01_history/ch10_version_matrix.md)、[ch119 Ranges 深入（C++20）](Book/part10_modern/ch119_ranges_deep.md)
- **策展路径**：前置 ch04、ch05、ch06、ch60、ch63 ｜ 后续 ch21、ch25、ch32、ch67、ch90、ch113、ch118、ch119、ch120

### ch08 · C++23：标准库大修

- 文件：`Book/part01_history/ch08_cpp23.md` ｜ Part：`part01_history`
- **出链**（本章指向）：
  [ch07 C++20：量级升级](Book/part01_history/ch07_cpp20.md)、[ch09 C++26：已确定特性与方向](Book/part01_history/ch09_cpp26.md)、[ch88 optional / expected / variant：可空与可辨别联合](Book/part07_stl/ch88_optional_variant.md)、[ch120 Coroutine 应用模式](Book/part10_modern/ch120_coroutine_app.md)
- **入链**（指向本章）：
  [ch07 C++20：量级升级](Book/part01_history/ch07_cpp20.md)、[ch09 C++26：已确定特性与方向](Book/part01_history/ch09_cpp26.md)、[ch88 optional / expected / variant：可空与可辨别联合](Book/part07_stl/ch88_optional_variant.md)、[ch92 时间库 chrono](Book/part07_stl/ch92_chrono.md)、[ch120 Coroutine 应用模式](Book/part10_modern/ch120_coroutine_app.md)
- **策展路径**：前置 ch04、ch05、ch06、ch07 ｜ 后续 ch34、ch82、ch88、ch90、ch131

### ch09 · C++26：已确定特性与方向

- 文件：`Book/part01_history/ch09_cpp26.md` ｜ Part：`part01_history`
- **出链**（本章指向）：
  [ch08 C++23：标准库大修](Book/part01_history/ch08_cpp23.md)、[ch10 版本特性全景对照表与迁移指南](Book/part01_history/ch10_version_matrix.md)、[ch121 Contracts 契约（方向，C++26）](Book/part10_modern/ch121_contracts.md)、[ch123 Compile-Time 编程范式总览](Book/part10_modern/ch123_ct_programming.md)
- **入链**（指向本章）：
  [ch08 C++23：标准库大修](Book/part01_history/ch08_cpp23.md)、[ch10 版本特性全景对照表与迁移指南](Book/part01_history/ch10_version_matrix.md)、[ch121 Contracts 契约（方向，C++26）](Book/part10_modern/ch121_contracts.md)
- **策展路径**：前置 ch07、ch67、ch113、ch114 ｜ 后续 ch74、ch114、ch121

### ch10 · 版本特性全景对照表与迁移指南

- 文件：`Book/part01_history/ch10_version_matrix.md` ｜ Part：`part01_history`
- **出链**（本章指向）：
  [ch04 C++11：现代 C++ 革命](Book/part01_history/ch04_cpp11.md)、[ch07 C++20：量级升级](Book/part01_history/ch07_cpp20.md)、[ch09 C++26：已确定特性与方向](Book/part01_history/ch09_cpp26.md)
- **入链**（指向本章）：
  [ch09 C++26：已确定特性与方向](Book/part01_history/ch09_cpp26.md)
- **策展路径**：前置 ch03、ch04、ch05、ch06、ch07、ch08、ch09 ｜ 后续 无

### ch11 · 编译器全景：GCC / Clang / MSVC 架构与 ABI（C++）

- 文件：`Book/part02_toolchain/ch11_compilers.md` ｜ Part：`part02_toolchain`
- **出链**（本章指向）：
  [ch12 构建系统：Make / Ninja / CMake（C++）](Book/part02_toolchain/ch12_buildsystems.md)、[ch69 编译期计算：constexpr / consteval / constinit](Book/part06_templates/ch69_constexpr.md)、[ch157 Compiler Explorer 实战](Book/part14_perf/ch157_compiler_explorer.md)
- **入链**（指向本章）：
  [ch12 构建系统：Make / Ninja / CMake（C++）](Book/part02_toolchain/ch12_buildsystems.md)、[ch14 调试与诊断：GDB / LLDB / Sanitizer / Valgrind（C++）](Book/part02_toolchain/ch14_debugging.md)、[ch16 IDE 与编辑器：VSCode / CLion / QtCreator / VIM（C++）](Book/part02_toolchain/ch16_ide.md)、[ch17 交叉编译与嵌入式工具链（C++）](Book/part02_toolchain/ch17_crosscompile.md)、[ch127 LLVM / Clang 架构（C++）](Book/part11_source/ch127_llvm.md)、[ch157 Compiler Explorer 实战](Book/part14_perf/ch157_compiler_explorer.md)

### ch12 · 构建系统：Make / Ninja / CMake（C++）

- 文件：`Book/part02_toolchain/ch12_buildsystems.md` ｜ Part：`part02_toolchain`
- **出链**（本章指向）：
  [ch11 编译器全景：GCC / Clang / MSVC 架构与 ABI（C++）](Book/part02_toolchain/ch11_compilers.md)、[ch13 包管理：vcpkg / Conan（C++）](Book/part02_toolchain/ch13_packaging.md)、[ch18 构建配置：Debug / Release / LTO / PGO（C++）](Book/part02_toolchain/ch18_buildconfig.md)
- **入链**（指向本章）：
  [ch11 编译器全景：GCC / Clang / MSVC 架构与 ABI（C++）](Book/part02_toolchain/ch11_compilers.md)、[ch13 包管理：vcpkg / Conan（C++）](Book/part02_toolchain/ch13_packaging.md)、[ch14 调试与诊断：GDB / LLDB / Sanitizer / Valgrind（C++）](Book/part02_toolchain/ch14_debugging.md)、[ch18 构建配置：Debug / Release / LTO / PGO（C++）](Book/part02_toolchain/ch18_buildconfig.md)

### ch13 · 包管理：vcpkg / Conan（C++）

- 文件：`Book/part02_toolchain/ch13_packaging.md` ｜ Part：`part02_toolchain`
- **出链**（本章指向）：
  [ch12 构建系统：Make / Ninja / CMake（C++）](Book/part02_toolchain/ch12_buildsystems.md)、[ch14 调试与诊断：GDB / LLDB / Sanitizer / Valgrind（C++）](Book/part02_toolchain/ch14_debugging.md)、[ch128 Boost 核心库（C++）](Book/part11_source/ch128_boost.md)
- **入链**（指向本章）：
  [ch12 构建系统：Make / Ninja / CMake（C++）](Book/part02_toolchain/ch12_buildsystems.md)、[ch14 调试与诊断：GDB / LLDB / Sanitizer / Valgrind（C++）](Book/part02_toolchain/ch14_debugging.md)

### ch14 · 调试与诊断：GDB / LLDB / Sanitizer / Valgrind（C++）

- 文件：`Book/part02_toolchain/ch14_debugging.md` ｜ Part：`part02_toolchain`
- **出链**（本章指向）：
  [ch11 编译器全景：GCC / Clang / MSVC 架构与 ABI（C++）](Book/part02_toolchain/ch11_compilers.md)、[ch12 构建系统：Make / Ninja / CMake（C++）](Book/part02_toolchain/ch12_buildsystems.md)、[ch13 包管理：vcpkg / Conan（C++）](Book/part02_toolchain/ch13_packaging.md)、[ch15 性能分析：perf / VTune / 火焰图 / Compiler Explorer（C++）](Book/part02_toolchain/ch15_profiling.md)、[ch16 IDE 与编辑器：VSCode / CLion / QtCreator / VIM（C++）](Book/part02_toolchain/ch16_ide.md)
- **入链**（指向本章）：
  [ch13 包管理：vcpkg / Conan（C++）](Book/part02_toolchain/ch13_packaging.md)、[ch15 性能分析：perf / VTune / 火焰图 / Compiler Explorer（C++）](Book/part02_toolchain/ch15_profiling.md)、[ch16 IDE 与编辑器：VSCode / CLion / QtCreator / VIM（C++）](Book/part02_toolchain/ch16_ide.md)

### ch15 · 性能分析：perf / VTune / 火焰图 / Compiler Explorer（C++）

- 文件：`Book/part02_toolchain/ch15_profiling.md` ｜ Part：`part02_toolchain`
- **出链**（本章指向）：
  [ch14 调试与诊断：GDB / LLDB / Sanitizer / Valgrind（C++）](Book/part02_toolchain/ch14_debugging.md)、[ch16 IDE 与编辑器：VSCode / CLion / QtCreator / VIM（C++）](Book/part02_toolchain/ch16_ide.md)、[ch151 基准测试与性能度量（C++）](Book/part13_engineering/ch151_benchmark.md)、[ch157 Compiler Explorer 实战](Book/part14_perf/ch157_compiler_explorer.md)
- **入链**（指向本章）：
  [ch14 调试与诊断：GDB / LLDB / Sanitizer / Valgrind（C++）](Book/part02_toolchain/ch14_debugging.md)、[ch16 IDE 与编辑器：VSCode / CLion / QtCreator / VIM（C++）](Book/part02_toolchain/ch16_ide.md)、[ch157 Compiler Explorer 实战](Book/part14_perf/ch157_compiler_explorer.md)

### ch16 · IDE 与编辑器：VSCode / CLion / QtCreator / VIM（C++）

- 文件：`Book/part02_toolchain/ch16_ide.md` ｜ Part：`part02_toolchain`
- **出链**（本章指向）：
  [ch11 编译器全景：GCC / Clang / MSVC 架构与 ABI（C++）](Book/part02_toolchain/ch11_compilers.md)、[ch14 调试与诊断：GDB / LLDB / Sanitizer / Valgrind（C++）](Book/part02_toolchain/ch14_debugging.md)、[ch15 性能分析：perf / VTune / 火焰图 / Compiler Explorer（C++）](Book/part02_toolchain/ch15_profiling.md)、[ch17 交叉编译与嵌入式工具链（C++）](Book/part02_toolchain/ch17_crosscompile.md)
- **入链**（指向本章）：
  [ch14 调试与诊断：GDB / LLDB / Sanitizer / Valgrind（C++）](Book/part02_toolchain/ch14_debugging.md)、[ch15 性能分析：perf / VTune / 火焰图 / Compiler Explorer（C++）](Book/part02_toolchain/ch15_profiling.md)、[ch17 交叉编译与嵌入式工具链（C++）](Book/part02_toolchain/ch17_crosscompile.md)

### ch17 · 交叉编译与嵌入式工具链（C++）

- 文件：`Book/part02_toolchain/ch17_crosscompile.md` ｜ Part：`part02_toolchain`
- **出链**（本章指向）：
  [ch11 编译器全景：GCC / Clang / MSVC 架构与 ABI（C++）](Book/part02_toolchain/ch11_compilers.md)、[ch16 IDE 与编辑器：VSCode / CLion / QtCreator / VIM（C++）](Book/part02_toolchain/ch16_ide.md)、[ch18 构建配置：Debug / Release / LTO / PGO（C++）](Book/part02_toolchain/ch18_buildconfig.md)、[ch30 volatile / atomic 与硬件寄存器](Book/part03_language/ch30_volatile.md)
- **入链**（指向本章）：
  [ch16 IDE 与编辑器：VSCode / CLion / QtCreator / VIM（C++）](Book/part02_toolchain/ch16_ide.md)、[ch18 构建配置：Debug / Release / LTO / PGO（C++）](Book/part02_toolchain/ch18_buildconfig.md)、[ch30 volatile / atomic 与硬件寄存器](Book/part03_language/ch30_volatile.md)

### ch18 · 构建配置：Debug / Release / LTO / PGO（C++）

- 文件：`Book/part02_toolchain/ch18_buildconfig.md` ｜ Part：`part02_toolchain`
- **出链**（本章指向）：
  [ch12 构建系统：Make / Ninja / CMake（C++）](Book/part02_toolchain/ch12_buildsystems.md)、[ch17 交叉编译与嵌入式工具链（C++）](Book/part02_toolchain/ch17_crosscompile.md)、[ch149 CI/CD 流水线（C++）](Book/part13_engineering/ch149_ci_cd.md)
- **入链**（指向本章）：
  [ch12 构建系统：Make / Ninja / CMake（C++）](Book/part02_toolchain/ch12_buildsystems.md)、[ch17 交叉编译与嵌入式工具链（C++）](Book/part02_toolchain/ch17_crosscompile.md)、[ch148 Git 工作流（C++）](Book/part13_engineering/ch148_gitflow.md)、[ch149 CI/CD 流水线（C++）](Book/part13_engineering/ch149_ci_cd.md)

### ch19 · 变量、存储期、链接与 ODR（工业级深度版）

- 文件：`Book/part03_language/ch19_variables.md` ｜ Part：`part03_language`
- **出链**（本章指向）：
  [ch20 引用（reference）vs 指针（pointer）：语义本质、底层实现与生命周期战争](Book/part03_language/ch20_reference_pointer.md)、[ch21 const / constexpr / consteval / constinit 深度详解](Book/part03_language/ch21_const_family.md)、[ch32 初始化与列表初始化](Book/part03_language/ch32_initialization.md)、[ch35 第 35 章  C++ 程序的内存模型与操作系统视角](Book/part04_memory/ch35_memory_layout.md)、[ch36 第 36 章 栈（stack）与堆（heap）的深度对比](Book/part04_memory/ch36_stack_heap.md)
- **入链**（指向本章）：
  [ch01 C 语言遗产与 C with Classes](Book/part01_history/ch01_c_history.md)、[ch20 引用（reference）vs 指针（pointer）：语义本质、底层实现与生命周期战争](Book/part03_language/ch20_reference_pointer.md)、[ch21 const / constexpr / consteval / constinit 深度详解](Book/part03_language/ch21_const_family.md)、[ch22 第 22 章 · `auto` 类型推导、`decltype` 与返回类型推导](Book/part03_language/ch22_auto_decltype.md)、[ch28 对象生命周期与未定义行为（UB）：生存期、悬垂、UB 分类与编译器武器化](Book/part03_language/ch28_lifetime_ub.md)、[ch29 友元 friend 与访问控制](Book/part03_language/ch29_friend.md)、[ch30 volatile / atomic 与硬件寄存器](Book/part03_language/ch30_volatile.md)、[ch31 运算符重载](Book/part03_language/ch31_operator_overloading.md)、[ch32 初始化与列表初始化](Book/part03_language/ch32_initialization.md)、[ch76 STL 架构与迭代器概念](Book/part07_stl/ch76_stl_arch.md)、[ch80 array 与固定数组](Book/part07_stl/ch80_array.md)、[ch84 set / multiset：红黑树有序集合](Book/part07_stl/ch84_set.md)、[ch85 unordered_map / unordered_set：哈希开链集合](Book/part07_stl/ch85_unordered.md)、[ch86 容器适配器：stack / queue / priority_queue](Book/part07_stl/ch86_adapters.md)、[ch91 文件系统 filesystem](Book/part07_stl/ch91_filesystem.md)、[ch92 时间库 chrono](Book/part07_stl/ch92_chrono.md)、[ch93 线程与异步：thread / future / async](Book/part07_stl/ch93_thread_async.md)、[ch115 移动语义与右值引用](Book/part10_modern/ch115_move.md)、[ch165 C++ 进阶路线图（C++）](Book/part16_reading/ch165_roadmap.md)
- **策展路径**：前置 ch01、ch10、ch20、ch31 ｜ 后续 ch21、ch32、ch33、ch35、ch60、ch102

### ch20 · 引用（reference）vs 指针（pointer）：语义本质、底层实现与生命周期战争

- 文件：`Book/part03_language/ch20_reference_pointer.md` ｜ Part：`part03_language`
- **出链**（本章指向）：
  [ch19 变量、存储期、链接与 ODR（工业级深度版）](Book/part03_language/ch19_variables.md)、[ch21 const / constexpr / consteval / constinit 深度详解](Book/part03_language/ch21_const_family.md)、[ch32 初始化与列表初始化](Book/part03_language/ch32_initialization.md)、[ch65 类型特性 Type Traits —— 编译期类型自省与分发](Book/part06_templates/ch65_type_traits.md)、[ch69 编译期计算：constexpr / consteval / constinit](Book/part06_templates/ch69_constexpr.md)
- **入链**（指向本章）：
  [ch19 变量、存储期、链接与 ODR（工业级深度版）](Book/part03_language/ch19_variables.md)、[ch21 const / constexpr / consteval / constinit 深度详解](Book/part03_language/ch21_const_family.md)、[ch24 第 24 章 枚举（枚举类型全解：unscoped / enum class / 位掩码 / ABI / 反射）](Book/part03_language/ch24_enum.md)、[ch32 初始化与列表初始化](Book/part03_language/ch32_initialization.md)、[ch76 STL 架构与迭代器概念](Book/part07_stl/ch76_stl_arch.md)、[ch78 deque 与分段连续 [标准]](Book/part07_stl/ch78_deque.md)、[ch80 array 与固定数组](Book/part07_stl/ch80_array.md)、[ch82 span 与裸数组视图](Book/part07_stl/ch82_span.md)、[ch83 map / multimap（红黑树）](Book/part07_stl/ch83_map.md)、[ch89 tuple / pair / any / function / bind](Book/part07_stl/ch89_tuple_any.md)、[ch115 移动语义与右值引用](Book/part10_modern/ch115_move.md)、[ch116 完美转发与万能引用](Book/part10_modern/ch116_perfect_forwarding.md)
- **策展路径**：前置 ch19 ｜ 后续 ch21、ch31、ch33、ch52、ch77、ch89、ch94、ch115、ch116、ch154、ch157

### ch21 · const / constexpr / consteval / constinit 深度详解

- 文件：`Book/part03_language/ch21_const_family.md` ｜ Part：`part03_language`
- **出链**（本章指向）：
  [ch19 变量、存储期、链接与 ODR（工业级深度版）](Book/part03_language/ch19_variables.md)、[ch20 引用（reference）vs 指针（pointer）：语义本质、底层实现与生命周期战争](Book/part03_language/ch20_reference_pointer.md)、[ch22 第 22 章 · `auto` 类型推导、`decltype` 与返回类型推导](Book/part03_language/ch22_auto_decltype.md)、[ch31 运算符重载](Book/part03_language/ch31_operator_overloading.md)
- **入链**（指向本章）：
  [ch19 变量、存储期、链接与 ODR（工业级深度版）](Book/part03_language/ch19_variables.md)、[ch20 引用（reference）vs 指针（pointer）：语义本质、底层实现与生命周期战争](Book/part03_language/ch20_reference_pointer.md)、[ch22 第 22 章 · `auto` 类型推导、`decltype` 与返回类型推导](Book/part03_language/ch22_auto_decltype.md)、[ch31 运算符重载](Book/part03_language/ch31_operator_overloading.md)、[ch32 初始化与列表初始化](Book/part03_language/ch32_initialization.md)
- **策展路径**：前置 ch19、ch20 ｜ 后续 无

### ch22 · 第 22 章 · `auto` 类型推导、`decltype` 与返回类型推导

- 文件：`Book/part03_language/ch22_auto_decltype.md` ｜ Part：`part03_language`
- **出链**（本章指向）：
  [ch19 变量、存储期、链接与 ODR（工业级深度版）](Book/part03_language/ch19_variables.md)、[ch21 const / constexpr / consteval / constinit 深度详解](Book/part03_language/ch21_const_family.md)、[ch23 命名空间（namespace）、using 与参数依赖查找（ADL）：隔离、版本化与隐形查找](Book/part03_language/ch23_namespace_adl.md)、[ch69 编译期计算：constexpr / consteval / constinit](Book/part06_templates/ch69_constexpr.md)
- **入链**（指向本章）：
  [ch21 const / constexpr / consteval / constinit 深度详解](Book/part03_language/ch21_const_family.md)、[ch23 命名空间（namespace）、using 与参数依赖查找（ADL）：隔离、版本化与隐形查找](Book/part03_language/ch23_namespace_adl.md)

### ch23 · 命名空间（namespace）、using 与参数依赖查找（ADL）：隔离、版本化与隐形查找

- 文件：`Book/part03_language/ch23_namespace_adl.md` ｜ Part：`part03_language`
- **出链**（本章指向）：
  [ch22 第 22 章 · `auto` 类型推导、`decltype` 与返回类型推导](Book/part03_language/ch22_auto_decltype.md)、[ch24 第 24 章 枚举（枚举类型全解：unscoped / enum class / 位掩码 / ABI / 反射）](Book/part03_language/ch24_enum.md)、[ch29 友元 friend 与访问控制](Book/part03_language/ch29_friend.md)、[ch61 函数模板重载决议（Function Template Overload Resolution）](Book/part06_templates/ch61_template_overload.md)
- **入链**（指向本章）：
  [ch22 第 22 章 · `auto` 类型推导、`decltype` 与返回类型推导](Book/part03_language/ch22_auto_decltype.md)、[ch24 第 24 章 枚举（枚举类型全解：unscoped / enum class / 位掩码 / ABI / 反射）](Book/part03_language/ch24_enum.md)、[ch29 友元 friend 与访问控制](Book/part03_language/ch29_friend.md)
- **策展路径**：前置 ch19 ｜ 后续 ch21、ch31、ch60、ch62、ch119

### ch24 · 第 24 章 枚举（枚举类型全解：unscoped / enum class / 位掩码 / ABI / 反射）

- 文件：`Book/part03_language/ch24_enum.md` ｜ Part：`part03_language`
- **出链**（本章指向）：
  [ch20 引用（reference）vs 指针（pointer）：语义本质、底层实现与生命周期战争](Book/part03_language/ch20_reference_pointer.md)、[ch23 命名空间（namespace）、using 与参数依赖查找（ADL）：隔离、版本化与隐形查找](Book/part03_language/ch23_namespace_adl.md)、[ch25 union 与 std::variant 深度详解](Book/part03_language/ch25_union_variant.md)、[ch65 类型特性 Type Traits —— 编译期类型自省与分发](Book/part06_templates/ch65_type_traits.md)
- **入链**（指向本章）：
  [ch23 命名空间（namespace）、using 与参数依赖查找（ADL）：隔离、版本化与隐形查找](Book/part03_language/ch23_namespace_adl.md)、[ch25 union 与 std::variant 深度详解](Book/part03_language/ch25_union_variant.md)

### ch25 · union 与 std::variant 深度详解

- 文件：`Book/part03_language/ch25_union_variant.md` ｜ Part：`part03_language`
- **出链**（本章指向）：
  [ch24 第 24 章 枚举（枚举类型全解：unscoped / enum class / 位掩码 / ABI / 反射）](Book/part03_language/ch24_enum.md)、[ch26 lambda 表达式全解：闭包类型、捕获、泛型/模板 lambda、constexpr、ABI 与 std::function 类型擦除](Book/part03_language/ch26_lambda.md)、[ch32 初始化与列表初始化](Book/part03_language/ch32_initialization.md)、[ch88 optional / expected / variant：可空与可辨别联合](Book/part07_stl/ch88_optional_variant.md)
- **入链**（指向本章）：
  [ch24 第 24 章 枚举（枚举类型全解：unscoped / enum class / 位掩码 / ABI / 反射）](Book/part03_language/ch24_enum.md)、[ch26 lambda 表达式全解：闭包类型、捕获、泛型/模板 lambda、constexpr、ABI 与 std::function 类型擦除](Book/part03_language/ch26_lambda.md)
- **策展路径**：前置 ch19、ch20、ch21、ch34、ch59、ch115 ｜ 后续 无

### ch26 · lambda 表达式全解：闭包类型、捕获、泛型/模板 lambda、constexpr、ABI 与 std::function 类型擦除

- 文件：`Book/part03_language/ch26_lambda.md` ｜ Part：`part03_language`
- **出链**（本章指向）：
  [ch25 union 与 std::variant 深度详解](Book/part03_language/ch25_union_variant.md)、[ch27 显式转型四兄弟与隐式转换：const_cast / static_cast / dynamic_cast / reinterpret_cast 深度详解](Book/part03_language/ch27_cast.md)、[ch77 vector：扩容、失效、allocator 协作](Book/part07_stl/ch77_vector.md)、[ch116 完美转发与万能引用](Book/part10_modern/ch116_perfect_forwarding.md)
- **入链**（指向本章）：
  [ch25 union 与 std::variant 深度详解](Book/part03_language/ch25_union_variant.md)、[ch27 显式转型四兄弟与隐式转换：const_cast / static_cast / dynamic_cast / reinterpret_cast 深度详解](Book/part03_language/ch27_cast.md)、[ch28 对象生命周期与未定义行为（UB）：生存期、悬垂、UB 分类与编译器武器化](Book/part03_language/ch28_lifetime_ub.md)、[ch86 容器适配器：stack / queue / priority_queue](Book/part07_stl/ch86_adapters.md)、[ch89 tuple / pair / any / function / bind](Book/part07_stl/ch89_tuple_any.md)、[ch90 ranges 与 views：惰性求值与管道组合](Book/part07_stl/ch90_ranges.md)
- **策展路径**：前置 ch19、ch20、ch21、ch22、ch59、ch80、ch115、ch116 ｜ 后续 ch27、ch52、ch115、ch116、ch154

### ch27 · 显式转型四兄弟与隐式转换：const_cast / static_cast / dynamic_cast / reinterpret_cast 深度详解

- 文件：`Book/part03_language/ch27_cast.md` ｜ Part：`part03_language`
- **出链**（本章指向）：
  [ch26 lambda 表达式全解：闭包类型、捕获、泛型/模板 lambda、constexpr、ABI 与 std::function 类型擦除](Book/part03_language/ch26_lambda.md)、[ch28 对象生命周期与未定义行为（UB）：生存期、悬垂、UB 分类与编译器武器化](Book/part03_language/ch28_lifetime_ub.md)、[ch31 运算符重载](Book/part03_language/ch31_operator_overloading.md)、[ch48 RTTI 与 typeid/dynamic_cast：运行时类型查询](Book/part05_oo/ch48_rtti.md)
- **入链**（指向本章）：
  [ch26 lambda 表达式全解：闭包类型、捕获、泛型/模板 lambda、constexpr、ABI 与 std::function 类型擦除](Book/part03_language/ch26_lambda.md)、[ch28 对象生命周期与未定义行为（UB）：生存期、悬垂、UB 分类与编译器武器化](Book/part03_language/ch28_lifetime_ub.md)、[ch29 友元 friend 与访问控制](Book/part03_language/ch29_friend.md)、[ch31 运算符重载](Book/part03_language/ch31_operator_overloading.md)、[ch115 移动语义与右值引用](Book/part10_modern/ch115_move.md)
- **策展路径**：前置 ch19、ch20、ch21、ch60 ｜ 后续 ch31、ch42、ch65

### ch28 · 对象生命周期与未定义行为（UB）：生存期、悬垂、UB 分类与编译器武器化

- 文件：`Book/part03_language/ch28_lifetime_ub.md` ｜ Part：`part03_language`
- **出链**（本章指向）：
  [ch19 变量、存储期、链接与 ODR（工业级深度版）](Book/part03_language/ch19_variables.md)、[ch26 lambda 表达式全解：闭包类型、捕获、泛型/模板 lambda、constexpr、ABI 与 std::function 类型擦除](Book/part03_language/ch26_lambda.md)、[ch27 显式转型四兄弟与隐式转换：const_cast / static_cast / dynamic_cast / reinterpret_cast 深度详解](Book/part03_language/ch27_cast.md)、[ch29 友元 friend 与访问控制](Book/part03_language/ch29_friend.md)、[ch30 volatile / atomic 与硬件寄存器](Book/part03_language/ch30_volatile.md)
- **入链**（指向本章）：
  [ch27 显式转型四兄弟与隐式转换：const_cast / static_cast / dynamic_cast / reinterpret_cast 深度详解](Book/part03_language/ch27_cast.md)、[ch29 友元 friend 与访问控制](Book/part03_language/ch29_friend.md)、[ch30 volatile / atomic 与硬件寄存器](Book/part03_language/ch30_volatile.md)
- **策展路径**：前置 ch19、ch20、ch21、ch25、ch27、ch31、ch33、ch42、ch61 ｜ 后续 ch42、ch61

### ch29 · 友元 friend 与访问控制

- 文件：`Book/part03_language/ch29_friend.md` ｜ Part：`part03_language`
- **出链**（本章指向）：
  [ch19 变量、存储期、链接与 ODR（工业级深度版）](Book/part03_language/ch19_variables.md)、[ch23 命名空间（namespace）、using 与参数依赖查找（ADL）：隔离、版本化与隐形查找](Book/part03_language/ch23_namespace_adl.md)、[ch27 显式转型四兄弟与隐式转换：const_cast / static_cast / dynamic_cast / reinterpret_cast 深度详解](Book/part03_language/ch27_cast.md)、[ch28 对象生命周期与未定义行为（UB）：生存期、悬垂、UB 分类与编译器武器化](Book/part03_language/ch28_lifetime_ub.md)、[ch30 volatile / atomic 与硬件寄存器](Book/part03_language/ch30_volatile.md)、[ch31 运算符重载](Book/part03_language/ch31_operator_overloading.md)、[ch46 第 46 章 封装与继承深度：访问控制、三种继承、切片、构造/析构、名字隐藏、override/final、NVI](Book/part05_oo/ch46_encapsulation_inheritance.md)、[ch150 测试策略（C++）](Book/part13_engineering/ch150_testing.md)
- **入链**（指向本章）：
  [ch23 命名空间（namespace）、using 与参数依赖查找（ADL）：隔离、版本化与隐形查找](Book/part03_language/ch23_namespace_adl.md)、[ch28 对象生命周期与未定义行为（UB）：生存期、悬垂、UB 分类与编译器武器化](Book/part03_language/ch28_lifetime_ub.md)、[ch30 volatile / atomic 与硬件寄存器](Book/part03_language/ch30_volatile.md)、[ch31 运算符重载](Book/part03_language/ch31_operator_overloading.md)、[ch46 第 46 章 封装与继承深度：访问控制、三种继承、切片、构造/析构、名字隐藏、override/final、NVI](Book/part05_oo/ch46_encapsulation_inheritance.md)、[ch150 测试策略（C++）](Book/part13_engineering/ch150_testing.md)
- **策展路径**：前置 ch46 ｜ 后续 无

### ch30 · volatile / atomic 与硬件寄存器

- 文件：`Book/part03_language/ch30_volatile.md` ｜ Part：`part03_language`
- **出链**（本章指向）：
  [ch17 交叉编译与嵌入式工具链（C++）](Book/part02_toolchain/ch17_crosscompile.md)、[ch19 变量、存储期、链接与 ODR（工业级深度版）](Book/part03_language/ch19_variables.md)、[ch28 对象生命周期与未定义行为（UB）：生存期、悬垂、UB 分类与编译器武器化](Book/part03_language/ch28_lifetime_ub.md)、[ch29 友元 friend 与访问控制](Book/part03_language/ch29_friend.md)、[ch31 运算符重载](Book/part03_language/ch31_operator_overloading.md)、[ch32 初始化与列表初始化](Book/part03_language/ch32_initialization.md)、[ch107 std::atomic 原子类型（C++11）](Book/part09_concurrency/ch107_atomic.md)
- **入链**（指向本章）：
  [ch17 交叉编译与嵌入式工具链（C++）](Book/part02_toolchain/ch17_crosscompile.md)、[ch28 对象生命周期与未定义行为（UB）：生存期、悬垂、UB 分类与编译器武器化](Book/part03_language/ch28_lifetime_ub.md)、[ch29 友元 friend 与访问控制](Book/part03_language/ch29_friend.md)、[ch31 运算符重载](Book/part03_language/ch31_operator_overloading.md)、[ch32 初始化与列表初始化](Book/part03_language/ch32_initialization.md)、[ch107 std::atomic 原子类型（C++11）](Book/part09_concurrency/ch107_atomic.md)

### ch31 · 运算符重载

- 文件：`Book/part03_language/ch31_operator_overloading.md` ｜ Part：`part03_language`
- **出链**（本章指向）：
  [ch19 变量、存储期、链接与 ODR（工业级深度版）](Book/part03_language/ch19_variables.md)、[ch21 const / constexpr / consteval / constinit 深度详解](Book/part03_language/ch21_const_family.md)、[ch27 显式转型四兄弟与隐式转换：const_cast / static_cast / dynamic_cast / reinterpret_cast 深度详解](Book/part03_language/ch27_cast.md)、[ch29 友元 friend 与访问控制](Book/part03_language/ch29_friend.md)、[ch30 volatile / atomic 与硬件寄存器](Book/part03_language/ch30_volatile.md)、[ch32 初始化与列表初始化](Book/part03_language/ch32_initialization.md)
- **入链**（指向本章）：
  [ch21 const / constexpr / consteval / constinit 深度详解](Book/part03_language/ch21_const_family.md)、[ch27 显式转型四兄弟与隐式转换：const_cast / static_cast / dynamic_cast / reinterpret_cast 深度详解](Book/part03_language/ch27_cast.md)、[ch29 友元 friend 与访问控制](Book/part03_language/ch29_friend.md)、[ch30 volatile / atomic 与硬件寄存器](Book/part03_language/ch30_volatile.md)、[ch32 初始化与列表初始化](Book/part03_language/ch32_initialization.md)

### ch32 · 初始化与列表初始化

- 文件：`Book/part03_language/ch32_initialization.md` ｜ Part：`part03_language`
- **出链**（本章指向）：
  [ch01 C 语言遗产与 C with Classes](Book/part01_history/ch01_c_history.md)、[ch19 变量、存储期、链接与 ODR（工业级深度版）](Book/part03_language/ch19_variables.md)、[ch20 引用（reference）vs 指针（pointer）：语义本质、底层实现与生命周期战争](Book/part03_language/ch20_reference_pointer.md)、[ch21 const / constexpr / consteval / constinit 深度详解](Book/part03_language/ch21_const_family.md)、[ch30 volatile / atomic 与硬件寄存器](Book/part03_language/ch30_volatile.md)、[ch31 运算符重载](Book/part03_language/ch31_operator_overloading.md)
- **入链**（指向本章）：
  [ch01 C 语言遗产与 C with Classes](Book/part01_history/ch01_c_history.md)、[ch19 变量、存储期、链接与 ODR（工业级深度版）](Book/part03_language/ch19_variables.md)、[ch20 引用（reference）vs 指针（pointer）：语义本质、底层实现与生命周期战争](Book/part03_language/ch20_reference_pointer.md)、[ch25 union 与 std::variant 深度详解](Book/part03_language/ch25_union_variant.md)、[ch30 volatile / atomic 与硬件寄存器](Book/part03_language/ch30_volatile.md)、[ch31 运算符重载](Book/part03_language/ch31_operator_overloading.md)

### ch35 · 第 35 章  C++ 程序的内存模型与操作系统视角

- 文件：`Book/part04_memory/ch35_memory_layout.md` ｜ Part：`part04_memory`
- **出链**（本章指向）：
  [ch36 第 36 章 栈（stack）与堆（heap）的深度对比](Book/part04_memory/ch36_stack_heap.md)、[ch37 第 37 章 动态内存分配原语：`operator new` / `operator delete`](Book/part04_memory/ch37_new_delete.md)、[ch39 第 39 章 RAII 与 Rule of Zero/Three/Five](Book/part04_memory/ch39_raii_rule.md)
- **入链**（指向本章）：
  [ch19 变量、存储期、链接与 ODR（工业级深度版）](Book/part03_language/ch19_variables.md)、[ch36 第 36 章 栈（stack）与堆（heap）的深度对比](Book/part04_memory/ch36_stack_heap.md)、[ch40 第 40 章 异常安全（Exception Safety）](Book/part04_memory/ch40_exception_safety.md)、[ch41 第 41 章 智能指针全解（unique_ptr / shared_ptr / weak_ptr / enable_shared_from_this）](Book/part04_memory/ch41_smart_pointers.md)、[ch42 第 42 章 · 严格别名规则（Strict Aliasing）与编译器优化](Book/part04_memory/ch42_strict_aliasing.md)

### ch36 · 第 36 章 栈（stack）与堆（heap）的深度对比

- 文件：`Book/part04_memory/ch36_stack_heap.md` ｜ Part：`part04_memory`
- **出链**（本章指向）：
  [ch35 第 35 章  C++ 程序的内存模型与操作系统视角](Book/part04_memory/ch35_memory_layout.md)、[ch37 第 37 章 动态内存分配原语：`operator new` / `operator delete`](Book/part04_memory/ch37_new_delete.md)、[ch39 第 39 章 RAII 与 Rule of Zero/Three/Five](Book/part04_memory/ch39_raii_rule.md)
- **入链**（指向本章）：
  [ch19 变量、存储期、链接与 ODR（工业级深度版）](Book/part03_language/ch19_variables.md)、[ch35 第 35 章  C++ 程序的内存模型与操作系统视角](Book/part04_memory/ch35_memory_layout.md)、[ch37 第 37 章 动态内存分配原语：`operator new` / `operator delete`](Book/part04_memory/ch37_new_delete.md)、[ch43 第 43 章 CPU 缓存体系与内存局部性](Book/part04_memory/ch43_cache_locality.md)

### ch37 · 第 37 章 动态内存分配原语：`operator new` / `operator delete`

- 文件：`Book/part04_memory/ch37_new_delete.md` ｜ Part：`part04_memory`
- **出链**（本章指向）：
  [ch36 第 36 章 栈（stack）与堆（heap）的深度对比](Book/part04_memory/ch36_stack_heap.md)、[ch38 第 38 章 分配器（Allocator）模型与 PMR](Book/part04_memory/ch38_allocator.md)、[ch39 第 39 章 RAII 与 Rule of Zero/Three/Five](Book/part04_memory/ch39_raii_rule.md)、[ch115 移动语义与右值引用](Book/part10_modern/ch115_move.md)
- **入链**（指向本章）：
  [ch35 第 35 章  C++ 程序的内存模型与操作系统视角](Book/part04_memory/ch35_memory_layout.md)、[ch36 第 36 章 栈（stack）与堆（heap）的深度对比](Book/part04_memory/ch36_stack_heap.md)、[ch38 第 38 章 分配器（Allocator）模型与 PMR](Book/part04_memory/ch38_allocator.md)、[ch77 vector：扩容、失效、allocator 协作](Book/part07_stl/ch77_vector.md)、[ch122 PMR 与多态分配器](Book/part10_modern/ch122_pmr.md)

### ch38 · 第 38 章 分配器（Allocator）模型与 PMR

- 文件：`Book/part04_memory/ch38_allocator.md` ｜ Part：`part04_memory`
- **出链**（本章指向）：
  [ch37 第 37 章 动态内存分配原语：`operator new` / `operator delete`](Book/part04_memory/ch37_new_delete.md)、[ch39 第 39 章 RAII 与 Rule of Zero/Three/Five](Book/part04_memory/ch39_raii_rule.md)、[ch122 PMR 与多态分配器](Book/part10_modern/ch122_pmr.md)、[ch160 从零实现内存池（C++）](Book/part15_cases/ch160_mempool.md)
- **入链**（指向本章）：
  [ch37 第 37 章 动态内存分配原语：`operator new` / `operator delete`](Book/part04_memory/ch37_new_delete.md)、[ch39 第 39 章 RAII 与 Rule of Zero/Three/Five](Book/part04_memory/ch39_raii_rule.md)、[ch40 第 40 章 异常安全（Exception Safety）](Book/part04_memory/ch40_exception_safety.md)、[ch76 STL 架构与迭代器概念](Book/part07_stl/ch76_stl_arch.md)、[ch77 vector：扩容、失效、allocator 协作](Book/part07_stl/ch77_vector.md)、[ch122 PMR 与多态分配器](Book/part10_modern/ch122_pmr.md)

### ch39 · 第 39 章 RAII 与 Rule of Zero/Three/Five

- 文件：`Book/part04_memory/ch39_raii_rule.md` ｜ Part：`part04_memory`
- **出链**（本章指向）：
  [ch38 第 38 章 分配器（Allocator）模型与 PMR](Book/part04_memory/ch38_allocator.md)、[ch40 第 40 章 异常安全（Exception Safety）](Book/part04_memory/ch40_exception_safety.md)、[ch77 vector：扩容、失效、allocator 协作](Book/part07_stl/ch77_vector.md)
- **入链**（指向本章）：
  [ch35 第 35 章  C++ 程序的内存模型与操作系统视角](Book/part04_memory/ch35_memory_layout.md)、[ch36 第 36 章 栈（stack）与堆（heap）的深度对比](Book/part04_memory/ch36_stack_heap.md)、[ch37 第 37 章 动态内存分配原语：`operator new` / `operator delete`](Book/part04_memory/ch37_new_delete.md)、[ch38 第 38 章 分配器（Allocator）模型与 PMR](Book/part04_memory/ch38_allocator.md)、[ch40 第 40 章 异常安全（Exception Safety）](Book/part04_memory/ch40_exception_safety.md)、[ch41 第 41 章 智能指针全解（unique_ptr / shared_ptr / weak_ptr / enable_shared_from_this）](Book/part04_memory/ch41_smart_pointers.md)、[ch91 文件系统 filesystem](Book/part07_stl/ch91_filesystem.md)、[ch92 时间库 chrono](Book/part07_stl/ch92_chrono.md)、[ch94 stop_token 与协作取消 [标准]](Book/part07_stl/ch94_stop_token.md)、[ch115 移动语义与右值引用](Book/part10_modern/ch115_move.md)、[ch124 libstdc++ 架构与阅读入口（C++）](Book/part11_source/ch124_libstdcxx.md)、[ch165 C++ 进阶路线图（C++）](Book/part16_reading/ch165_roadmap.md)

### ch40 · 第 40 章 异常安全（Exception Safety）

- 文件：`Book/part04_memory/ch40_exception_safety.md` ｜ Part：`part04_memory`
- **出链**（本章指向）：
  [ch35 第 35 章  C++ 程序的内存模型与操作系统视角](Book/part04_memory/ch35_memory_layout.md)、[ch38 第 38 章 分配器（Allocator）模型与 PMR](Book/part04_memory/ch38_allocator.md)、[ch39 第 39 章 RAII 与 Rule of Zero/Three/Five](Book/part04_memory/ch39_raii_rule.md)、[ch41 第 41 章 智能指针全解（unique_ptr / shared_ptr / weak_ptr / enable_shared_from_this）](Book/part04_memory/ch41_smart_pointers.md)、[ch42 第 42 章 · 严格别名规则（Strict Aliasing）与编译器优化](Book/part04_memory/ch42_strict_aliasing.md)、[ch84 set / multiset：红黑树有序集合](Book/part07_stl/ch84_set.md)、[ch91 文件系统 filesystem](Book/part07_stl/ch91_filesystem.md)
- **入链**（指向本章）：
  [ch39 第 39 章 RAII 与 Rule of Zero/Three/Five](Book/part04_memory/ch39_raii_rule.md)、[ch41 第 41 章 智能指针全解（unique_ptr / shared_ptr / weak_ptr / enable_shared_from_this）](Book/part04_memory/ch41_smart_pointers.md)、[ch42 第 42 章 · 严格别名规则（Strict Aliasing）与编译器优化](Book/part04_memory/ch42_strict_aliasing.md)、[ch84 set / multiset：红黑树有序集合](Book/part07_stl/ch84_set.md)、[ch91 文件系统 filesystem](Book/part07_stl/ch91_filesystem.md)、[ch92 时间库 chrono](Book/part07_stl/ch92_chrono.md)、[ch93 线程与异步：thread / future / async](Book/part07_stl/ch93_thread_async.md)

### ch41 · 第 41 章 智能指针全解（unique_ptr / shared_ptr / weak_ptr / enable_shared_from_this）

- 文件：`Book/part04_memory/ch41_smart_pointers.md` ｜ Part：`part04_memory`
- **出链**（本章指向）：
  [ch35 第 35 章  C++ 程序的内存模型与操作系统视角](Book/part04_memory/ch35_memory_layout.md)、[ch39 第 39 章 RAII 与 Rule of Zero/Three/Five](Book/part04_memory/ch39_raii_rule.md)、[ch40 第 40 章 异常安全（Exception Safety）](Book/part04_memory/ch40_exception_safety.md)、[ch42 第 42 章 · 严格别名规则（Strict Aliasing）与编译器优化](Book/part04_memory/ch42_strict_aliasing.md)、[ch43 第 43 章 CPU 缓存体系与内存局部性](Book/part04_memory/ch43_cache_locality.md)
- **入链**（指向本章）：
  [ch40 第 40 章 异常安全（Exception Safety）](Book/part04_memory/ch40_exception_safety.md)、[ch42 第 42 章 · 严格别名规则（Strict Aliasing）与编译器优化](Book/part04_memory/ch42_strict_aliasing.md)

### ch42 · 第 42 章 · 严格别名规则（Strict Aliasing）与编译器优化

- 文件：`Book/part04_memory/ch42_strict_aliasing.md` ｜ Part：`part04_memory`
- **出链**（本章指向）：
  [ch35 第 35 章  C++ 程序的内存模型与操作系统视角](Book/part04_memory/ch35_memory_layout.md)、[ch40 第 40 章 异常安全（Exception Safety）](Book/part04_memory/ch40_exception_safety.md)、[ch41 第 41 章 智能指针全解（unique_ptr / shared_ptr / weak_ptr / enable_shared_from_this）](Book/part04_memory/ch41_smart_pointers.md)、[ch43 第 43 章 CPU 缓存体系与内存局部性](Book/part04_memory/ch43_cache_locality.md)、[ch44 第 44 章 内存池（Memory Pool）从零实现](Book/part04_memory/ch44_memory_pool.md)
- **入链**（指向本章）：
  [ch40 第 40 章 异常安全（Exception Safety）](Book/part04_memory/ch40_exception_safety.md)、[ch41 第 41 章 智能指针全解（unique_ptr / shared_ptr / weak_ptr / enable_shared_from_this）](Book/part04_memory/ch41_smart_pointers.md)、[ch43 第 43 章 CPU 缓存体系与内存局部性](Book/part04_memory/ch43_cache_locality.md)

### ch43 · 第 43 章 CPU 缓存体系与内存局部性

- 文件：`Book/part04_memory/ch43_cache_locality.md` ｜ Part：`part04_memory`
- **出链**（本章指向）：
  [ch36 第 36 章 栈（stack）与堆（heap）的深度对比](Book/part04_memory/ch36_stack_heap.md)、[ch42 第 42 章 · 严格别名规则（Strict Aliasing）与编译器优化](Book/part04_memory/ch42_strict_aliasing.md)、[ch44 第 44 章 内存池（Memory Pool）从零实现](Book/part04_memory/ch44_memory_pool.md)、[ch154 缓存优化与数据局部性（C++/硬件）](Book/part14_perf/ch154_cache_opt.md)
- **入链**（指向本章）：
  [ch41 第 41 章 智能指针全解（unique_ptr / shared_ptr / weak_ptr / enable_shared_from_this）](Book/part04_memory/ch41_smart_pointers.md)、[ch42 第 42 章 · 严格别名规则（Strict Aliasing）与编译器优化](Book/part04_memory/ch42_strict_aliasing.md)、[ch44 第 44 章 内存池（Memory Pool）从零实现](Book/part04_memory/ch44_memory_pool.md)、[ch87 bitset：编译期定长位集](Book/part07_stl/ch87_bitset.md)、[ch122 PMR 与多态分配器](Book/part10_modern/ch122_pmr.md)

### ch44 · 第 44 章 内存池（Memory Pool）从零实现

- 文件：`Book/part04_memory/ch44_memory_pool.md` ｜ Part：`part04_memory`
- **出链**（本章指向）：
  [ch43 第 43 章 CPU 缓存体系与内存局部性](Book/part04_memory/ch43_cache_locality.md)、[ch122 PMR 与多态分配器](Book/part10_modern/ch122_pmr.md)、[ch160 从零实现内存池（C++）](Book/part15_cases/ch160_mempool.md)
- **入链**（指向本章）：
  [ch42 第 42 章 · 严格别名规则（Strict Aliasing）与编译器优化](Book/part04_memory/ch42_strict_aliasing.md)、[ch43 第 43 章 CPU 缓存体系与内存局部性](Book/part04_memory/ch43_cache_locality.md)、[ch122 PMR 与多态分配器](Book/part10_modern/ch122_pmr.md)

### ch45 · 第 45 章 C++ 面向对象总览与对象模型基础

- 文件：`Book/part05_oo/ch45_oop_object_model.md` ｜ Part：`part05_oo`
- **出链**（本章指向）：
  [ch46 第 46 章 封装与继承深度：访问控制、三种继承、切片、构造/析构、名字隐藏、override/final、NVI](Book/part05_oo/ch46_encapsulation_inheritance.md)、[ch47 虚函数与虚表（vtable）：动态多态的发动机](Book/part05_oo/ch47_virtual_functions.md)、[ch52 空基类优化 EBO（Empty Base Optimization）](Book/part05_oo/ch52_ebo.md)
- **入链**（指向本章）：
  [ch46 第 46 章 封装与继承深度：访问控制、三种继承、切片、构造/析构、名字隐藏、override/final、NVI](Book/part05_oo/ch46_encapsulation_inheritance.md)、[ch50 多重继承与对象模型（Multiple Inheritance）](Book/part05_oo/ch50_multiple_inheritance.md)、[ch52 空基类优化 EBO（Empty Base Optimization）](Book/part05_oo/ch52_ebo.md)、[ch129 Qt 对象模型与信号槽（C++）](Book/part11_source/ch129_qt.md)、[ch134 Unreal Engine C++ 架构（C++）](Book/part11_source/ch134_unreal.md)、[ch137 结构型模式（C++）](Book/part12_patterns/ch137_structural.md)、[ch141 依赖注入（C++）](Book/part12_patterns/ch141_di.md)、[ch142 实体组件系统 ECS（C++）](Book/part12_patterns/ch142_ecs.md)

### ch46 · 第 46 章 封装与继承深度：访问控制、三种继承、切片、构造/析构、名字隐藏、override/final、NVI

- 文件：`Book/part05_oo/ch46_encapsulation_inheritance.md` ｜ Part：`part05_oo`
- **出链**（本章指向）：
  [ch29 友元 friend 与访问控制](Book/part03_language/ch29_friend.md)、[ch45 第 45 章 C++ 面向对象总览与对象模型基础](Book/part05_oo/ch45_oop_object_model.md)、[ch47 虚函数与虚表（vtable）：动态多态的发动机](Book/part05_oo/ch47_virtual_functions.md)
- **入链**（指向本章）：
  [ch29 友元 friend 与访问控制](Book/part03_language/ch29_friend.md)、[ch45 第 45 章 C++ 面向对象总览与对象模型基础](Book/part05_oo/ch45_oop_object_model.md)、[ch47 虚函数与虚表（vtable）：动态多态的发动机](Book/part05_oo/ch47_virtual_functions.md)、[ch52 空基类优化 EBO（Empty Base Optimization）](Book/part05_oo/ch52_ebo.md)

### ch47 · 虚函数与虚表（vtable）：动态多态的发动机

- 文件：`Book/part05_oo/ch47_virtual_functions.md` ｜ Part：`part05_oo`
- **出链**（本章指向）：
  [ch46 第 46 章 封装与继承深度：访问控制、三种继承、切片、构造/析构、名字隐藏、override/final、NVI](Book/part05_oo/ch46_encapsulation_inheritance.md)、[ch48 RTTI 与 typeid/dynamic_cast：运行时类型查询](Book/part05_oo/ch48_rtti.md)、[ch49 虚继承与菱形继承：共享虚基类](Book/part05_oo/ch49_virtual_inheritance.md)、[ch51 CRTP 与静态多态（Curiously Recurring Template Pattern）](Book/part05_oo/ch51_crtp.md)
- **入链**（指向本章）：
  [ch45 第 45 章 C++ 面向对象总览与对象模型基础](Book/part05_oo/ch45_oop_object_model.md)、[ch46 第 46 章 封装与继承深度：访问控制、三种继承、切片、构造/析构、名字隐藏、override/final、NVI](Book/part05_oo/ch46_encapsulation_inheritance.md)、[ch48 RTTI 与 typeid/dynamic_cast：运行时类型查询](Book/part05_oo/ch48_rtti.md)、[ch49 虚继承与菱形继承：共享虚基类](Book/part05_oo/ch49_virtual_inheritance.md)、[ch51 CRTP 与静态多态（Curiously Recurring Template Pattern）](Book/part05_oo/ch51_crtp.md)、[ch91 文件系统 filesystem](Book/part07_stl/ch91_filesystem.md)、[ch92 时间库 chrono](Book/part07_stl/ch92_chrono.md)、[ch122 PMR 与多态分配器](Book/part10_modern/ch122_pmr.md)

### ch48 · RTTI 与 typeid/dynamic_cast：运行时类型查询

- 文件：`Book/part05_oo/ch48_rtti.md` ｜ Part：`part05_oo`
- **出链**（本章指向）：
  [ch47 虚函数与虚表（vtable）：动态多态的发动机](Book/part05_oo/ch47_virtual_functions.md)、[ch49 虚继承与菱形继承：共享虚基类](Book/part05_oo/ch49_virtual_inheritance.md)、[ch65 类型特性 Type Traits —— 编译期类型自省与分发](Book/part06_templates/ch65_type_traits.md)
- **入链**（指向本章）：
  [ch27 显式转型四兄弟与隐式转换：const_cast / static_cast / dynamic_cast / reinterpret_cast 深度详解](Book/part03_language/ch27_cast.md)、[ch47 虚函数与虚表（vtable）：动态多态的发动机](Book/part05_oo/ch47_virtual_functions.md)、[ch49 虚继承与菱形继承：共享虚基类](Book/part05_oo/ch49_virtual_inheritance.md)

### ch49 · 虚继承与菱形继承：共享虚基类

- 文件：`Book/part05_oo/ch49_virtual_inheritance.md` ｜ Part：`part05_oo`
- **出链**（本章指向）：
  [ch47 虚函数与虚表（vtable）：动态多态的发动机](Book/part05_oo/ch47_virtual_functions.md)、[ch48 RTTI 与 typeid/dynamic_cast：运行时类型查询](Book/part05_oo/ch48_rtti.md)、[ch50 多重继承与对象模型（Multiple Inheritance）](Book/part05_oo/ch50_multiple_inheritance.md)
- **入链**（指向本章）：
  [ch47 虚函数与虚表（vtable）：动态多态的发动机](Book/part05_oo/ch47_virtual_functions.md)、[ch48 RTTI 与 typeid/dynamic_cast：运行时类型查询](Book/part05_oo/ch48_rtti.md)、[ch50 多重继承与对象模型（Multiple Inheritance）](Book/part05_oo/ch50_multiple_inheritance.md)

### ch50 · 多重继承与对象模型（Multiple Inheritance）

- 文件：`Book/part05_oo/ch50_multiple_inheritance.md` ｜ Part：`part05_oo`
- **出链**（本章指向）：
  [ch45 第 45 章 C++ 面向对象总览与对象模型基础](Book/part05_oo/ch45_oop_object_model.md)、[ch49 虚继承与菱形继承：共享虚基类](Book/part05_oo/ch49_virtual_inheritance.md)、[ch51 CRTP 与静态多态（Curiously Recurring Template Pattern）](Book/part05_oo/ch51_crtp.md)
- **入链**（指向本章）：
  [ch49 虚继承与菱形继承：共享虚基类](Book/part05_oo/ch49_virtual_inheritance.md)、[ch51 CRTP 与静态多态（Curiously Recurring Template Pattern）](Book/part05_oo/ch51_crtp.md)、[ch52 空基类优化 EBO（Empty Base Optimization）](Book/part05_oo/ch52_ebo.md)
- **策展路径**：前置 无 ｜ 后续 ch14、ch19、ch45、ch46、ch47、ch48、ch49、ch51

### ch51 · CRTP 与静态多态（Curiously Recurring Template Pattern）

- 文件：`Book/part05_oo/ch51_crtp.md` ｜ Part：`part05_oo`
- **出链**（本章指向）：
  [ch47 虚函数与虚表（vtable）：动态多态的发动机](Book/part05_oo/ch47_virtual_functions.md)、[ch50 多重继承与对象模型（Multiple Inheritance）](Book/part05_oo/ch50_multiple_inheritance.md)、[ch52 空基类优化 EBO（Empty Base Optimization）](Book/part05_oo/ch52_ebo.md)、[ch68 模板元编程 TMP 基础（递归 / 分支 / 循环）](Book/part06_templates/ch68_tmp.md)
- **入链**（指向本章）：
  [ch47 虚函数与虚表（vtable）：动态多态的发动机](Book/part05_oo/ch47_virtual_functions.md)、[ch50 多重继承与对象模型（Multiple Inheritance）](Book/part05_oo/ch50_multiple_inheritance.md)、[ch52 空基类优化 EBO（Empty Base Optimization）](Book/part05_oo/ch52_ebo.md)、[ch72 表达式模板 Expression Templates](Book/part06_templates/ch72_expression_templates.md)、[ch123 Compile-Time 编程范式总览](Book/part10_modern/ch123_ct_programming.md)、[ch139 CRTP 与静态多态（C++）](Book/part12_patterns/ch139_crtp_pattern.md)
- **策展路径**：前置 无 ｜ 后续 ch47、ch50、ch62、ch67、ch69、ch73

### ch52 · 空基类优化 EBO（Empty Base Optimization）

- 文件：`Book/part05_oo/ch52_ebo.md` ｜ Part：`part05_oo`
- **出链**（本章指向）：
  [ch45 第 45 章 C++ 面向对象总览与对象模型基础](Book/part05_oo/ch45_oop_object_model.md)、[ch46 第 46 章 封装与继承深度：访问控制、三种继承、切片、构造/析构、名字隐藏、override/final、NVI](Book/part05_oo/ch46_encapsulation_inheritance.md)、[ch50 多重继承与对象模型（Multiple Inheritance）](Book/part05_oo/ch50_multiple_inheritance.md)、[ch51 CRTP 与静态多态（Curiously Recurring Template Pattern）](Book/part05_oo/ch51_crtp.md)
- **入链**（指向本章）：
  [ch45 第 45 章 C++ 面向对象总览与对象模型基础](Book/part05_oo/ch45_oop_object_model.md)、[ch51 CRTP 与静态多态（Curiously Recurring Template Pattern）](Book/part05_oo/ch51_crtp.md)、[ch86 容器适配器：stack / queue / priority_queue](Book/part07_stl/ch86_adapters.md)、[ch89 tuple / pair / any / function / bind](Book/part07_stl/ch89_tuple_any.md)
- **策展路径**：前置 无 ｜ 后续 ch19、ch41、ch45、ch50、ch71

### ch60 · 模板基础与实例化（Template Basics & Instantiation）

- 文件：`Book/part06_templates/ch60_template_basics.md` ｜ Part：`part06_templates`
- **出链**（本章指向）：
  [ch61 函数模板重载决议（Function Template Overload Resolution）](Book/part06_templates/ch61_template_overload.md)、[ch69 编译期计算：constexpr / consteval / constinit](Book/part06_templates/ch69_constexpr.md)、[ch77 vector：扩容、失效、allocator 协作](Book/part07_stl/ch77_vector.md)
- **入链**（指向本章）：
  [ch61 函数模板重载决议（Function Template Overload Resolution）](Book/part06_templates/ch61_template_overload.md)、[ch62 类模板特化与偏特化（Class Template Specialization）](Book/part06_templates/ch62_specialization.md)、[ch76 STL 架构与迭代器概念](Book/part07_stl/ch76_stl_arch.md)、[ch92 时间库 chrono](Book/part07_stl/ch92_chrono.md)、[ch123 Compile-Time 编程范式总览](Book/part10_modern/ch123_ct_programming.md)

### ch61 · 函数模板重载决议（Function Template Overload Resolution）

- 文件：`Book/part06_templates/ch61_template_overload.md` ｜ Part：`part06_templates`
- **出链**（本章指向）：
  [ch60 模板基础与实例化（Template Basics & Instantiation）](Book/part06_templates/ch60_template_basics.md)、[ch62 类模板特化与偏特化（Class Template Specialization）](Book/part06_templates/ch62_specialization.md)、[ch66 SFINAE 与 std::enable_if —— 替换失败非错误的编译期分发](Book/part06_templates/ch66_sfinae.md)、[ch67 Concepts 与 requires —— C++20 的编译期约束](Book/part06_templates/ch67_concepts.md)
- **入链**（指向本章）：
  [ch23 命名空间（namespace）、using 与参数依赖查找（ADL）：隔离、版本化与隐形查找](Book/part03_language/ch23_namespace_adl.md)、[ch60 模板基础与实例化（Template Basics & Instantiation）](Book/part06_templates/ch60_template_basics.md)、[ch62 类模板特化与偏特化（Class Template Specialization）](Book/part06_templates/ch62_specialization.md)

### ch62 · 类模板特化与偏特化（Class Template Specialization）

- 文件：`Book/part06_templates/ch62_specialization.md` ｜ Part：`part06_templates`
- **出链**（本章指向）：
  [ch60 模板基础与实例化（Template Basics & Instantiation）](Book/part06_templates/ch60_template_basics.md)、[ch61 函数模板重载决议（Function Template Overload Resolution）](Book/part06_templates/ch61_template_overload.md)、[ch63 可变参数模板与包展开（Variadic Templates & Pack Expansion）](Book/part06_templates/ch63_variadic.md)、[ch68 模板元编程 TMP 基础（递归 / 分支 / 循环）](Book/part06_templates/ch68_tmp.md)
- **入链**（指向本章）：
  [ch61 函数模板重载决议（Function Template Overload Resolution）](Book/part06_templates/ch61_template_overload.md)、[ch63 可变参数模板与包展开（Variadic Templates & Pack Expansion）](Book/part06_templates/ch63_variadic.md)

### ch63 · 可变参数模板与包展开（Variadic Templates & Pack Expansion）

- 文件：`Book/part06_templates/ch63_variadic.md` ｜ Part：`part06_templates`
- **出链**（本章指向）：
  [ch62 类模板特化与偏特化（Class Template Specialization）](Book/part06_templates/ch62_specialization.md)、[ch64 折叠表达式 Fold Expression（C++17）](Book/part06_templates/ch64_fold.md)、[ch116 完美转发与万能引用](Book/part10_modern/ch116_perfect_forwarding.md)
- **入链**（指向本章）：
  [ch04 C++11：现代 C++ 革命](Book/part01_history/ch04_cpp11.md)、[ch62 类模板特化与偏特化（Class Template Specialization）](Book/part06_templates/ch62_specialization.md)、[ch64 折叠表达式 Fold Expression（C++17）](Book/part06_templates/ch64_fold.md)、[ch78 deque 与分段连续 [标准]](Book/part07_stl/ch78_deque.md)、[ch89 tuple / pair / any / function / bind](Book/part07_stl/ch89_tuple_any.md)、[ch93 线程与异步：thread / future / async](Book/part07_stl/ch93_thread_async.md)、[ch116 完美转发与万能引用](Book/part10_modern/ch116_perfect_forwarding.md)、[ch162 从零实现 JSON 库（C++）](Book/part15_cases/ch162_json.md)

### ch64 · 折叠表达式 Fold Expression（C++17）

- 文件：`Book/part06_templates/ch64_fold.md` ｜ Part：`part06_templates`
- **出链**（本章指向）：
  [ch63 可变参数模板与包展开（Variadic Templates & Pack Expansion）](Book/part06_templates/ch63_variadic.md)、[ch65 类型特性 Type Traits —— 编译期类型自省与分发](Book/part06_templates/ch65_type_traits.md)、[ch77 vector：扩容、失效、allocator 协作](Book/part07_stl/ch77_vector.md)
- **入链**（指向本章）：
  [ch06 C++17：生产力跃升](Book/part01_history/ch06_cpp17.md)、[ch63 可变参数模板与包展开（Variadic Templates & Pack Expansion）](Book/part06_templates/ch63_variadic.md)、[ch65 类型特性 Type Traits —— 编译期类型自省与分发](Book/part06_templates/ch65_type_traits.md)、[ch89 tuple / pair / any / function / bind](Book/part07_stl/ch89_tuple_any.md)

### ch65 · 类型特性 Type Traits —— 编译期类型自省与分发

- 文件：`Book/part06_templates/ch65_type_traits.md` ｜ Part：`part06_templates`
- **出链**（本章指向）：
  [ch64 折叠表达式 Fold Expression（C++17）](Book/part06_templates/ch64_fold.md)、[ch66 SFINAE 与 std::enable_if —— 替换失败非错误的编译期分发](Book/part06_templates/ch66_sfinae.md)、[ch68 模板元编程 TMP 基础（递归 / 分支 / 循环）](Book/part06_templates/ch68_tmp.md)
- **入链**（指向本章）：
  [ch20 引用（reference）vs 指针（pointer）：语义本质、底层实现与生命周期战争](Book/part03_language/ch20_reference_pointer.md)、[ch24 第 24 章 枚举（枚举类型全解：unscoped / enum class / 位掩码 / ABI / 反射）](Book/part03_language/ch24_enum.md)、[ch48 RTTI 与 typeid/dynamic_cast：运行时类型查询](Book/part05_oo/ch48_rtti.md)、[ch64 折叠表达式 Fold Expression（C++17）](Book/part06_templates/ch64_fold.md)、[ch66 SFINAE 与 std::enable_if —— 替换失败非错误的编译期分发](Book/part06_templates/ch66_sfinae.md)、[ch68 模板元编程 TMP 基础（递归 / 分支 / 循环）](Book/part06_templates/ch68_tmp.md)、[ch70 std::integral_constant 与标签分发（Tag Dispatch）](Book/part06_templates/ch70_tag_dispatch.md)、[ch71 策略设计 Policy-Based Design](Book/part06_templates/ch71_policy.md)、[ch76 STL 架构与迭代器概念](Book/part07_stl/ch76_stl_arch.md)、[ch84 set / multiset：红黑树有序集合](Book/part07_stl/ch84_set.md)、[ch85 unordered_map / unordered_set：哈希开链集合](Book/part07_stl/ch85_unordered.md)、[ch86 容器适配器：stack / queue / priority_queue](Book/part07_stl/ch86_adapters.md)、[ch87 bitset：编译期定长位集](Book/part07_stl/ch87_bitset.md)、[ch116 完美转发与万能引用](Book/part10_modern/ch116_perfect_forwarding.md)、[ch123 Compile-Time 编程范式总览](Book/part10_modern/ch123_ct_programming.md)、[ch128 Boost 核心库（C++）](Book/part11_source/ch128_boost.md)

### ch66 · SFINAE 与 std::enable_if —— 替换失败非错误的编译期分发

- 文件：`Book/part06_templates/ch66_sfinae.md` ｜ Part：`part06_templates`
- **出链**（本章指向）：
  [ch65 类型特性 Type Traits —— 编译期类型自省与分发](Book/part06_templates/ch65_type_traits.md)、[ch67 Concepts 与 requires —— C++20 的编译期约束](Book/part06_templates/ch67_concepts.md)
- **入链**（指向本章）：
  [ch61 函数模板重载决议（Function Template Overload Resolution）](Book/part06_templates/ch61_template_overload.md)、[ch65 类型特性 Type Traits —— 编译期类型自省与分发](Book/part06_templates/ch65_type_traits.md)、[ch67 Concepts 与 requires —— C++20 的编译期约束](Book/part06_templates/ch67_concepts.md)

### ch67 · Concepts 与 requires —— C++20 的编译期约束

- 文件：`Book/part06_templates/ch67_concepts.md` ｜ Part：`part06_templates`
- **出链**（本章指向）：
  [ch66 SFINAE 与 std::enable_if —— 替换失败非错误的编译期分发](Book/part06_templates/ch66_sfinae.md)、[ch68 模板元编程 TMP 基础（递归 / 分支 / 循环）](Book/part06_templates/ch68_tmp.md)、[ch119 Ranges 深入（C++20）](Book/part10_modern/ch119_ranges_deep.md)
- **入链**（指向本章）：
  [ch07 C++20：量级升级](Book/part01_history/ch07_cpp20.md)、[ch61 函数模板重载决议（Function Template Overload Resolution）](Book/part06_templates/ch61_template_overload.md)、[ch66 SFINAE 与 std::enable_if —— 替换失败非错误的编译期分发](Book/part06_templates/ch66_sfinae.md)、[ch68 模板元编程 TMP 基础（递归 / 分支 / 循环）](Book/part06_templates/ch68_tmp.md)、[ch76 STL 架构与迭代器概念](Book/part07_stl/ch76_stl_arch.md)、[ch90 ranges 与 views：惰性求值与管道组合](Book/part07_stl/ch90_ranges.md)、[ch119 Ranges 深入（C++20）](Book/part10_modern/ch119_ranges_deep.md)、[ch123 Compile-Time 编程范式总览](Book/part10_modern/ch123_ct_programming.md)

### ch68 · 模板元编程 TMP 基础（递归 / 分支 / 循环）

- 文件：`Book/part06_templates/ch68_tmp.md` ｜ Part：`part06_templates`
- **出链**（本章指向）：
  [ch65 类型特性 Type Traits —— 编译期类型自省与分发](Book/part06_templates/ch65_type_traits.md)、[ch67 Concepts 与 requires —— C++20 的编译期约束](Book/part06_templates/ch67_concepts.md)、[ch69 编译期计算：constexpr / consteval / constinit](Book/part06_templates/ch69_constexpr.md)
- **入链**（指向本章）：
  [ch51 CRTP 与静态多态（Curiously Recurring Template Pattern）](Book/part05_oo/ch51_crtp.md)、[ch62 类模板特化与偏特化（Class Template Specialization）](Book/part06_templates/ch62_specialization.md)、[ch65 类型特性 Type Traits —— 编译期类型自省与分发](Book/part06_templates/ch65_type_traits.md)、[ch67 Concepts 与 requires —— C++20 的编译期约束](Book/part06_templates/ch67_concepts.md)、[ch69 编译期计算：constexpr / consteval / constinit](Book/part06_templates/ch69_constexpr.md)、[ch72 表达式模板 Expression Templates](Book/part06_templates/ch72_expression_templates.md)、[ch92 时间库 chrono](Book/part07_stl/ch92_chrono.md)、[ch139 CRTP 与静态多态（C++）](Book/part12_patterns/ch139_crtp_pattern.md)

### ch69 · 编译期计算：constexpr / consteval / constinit

- 文件：`Book/part06_templates/ch69_constexpr.md` ｜ Part：`part06_templates`
- **出链**（本章指向）：
  [ch68 模板元编程 TMP 基础（递归 / 分支 / 循环）](Book/part06_templates/ch68_tmp.md)、[ch70 std::integral_constant 与标签分发（Tag Dispatch）](Book/part06_templates/ch70_tag_dispatch.md)、[ch123 Compile-Time 编程范式总览](Book/part10_modern/ch123_ct_programming.md)
- **入链**（指向本章）：
  [ch05 C++14：小幅完善](Book/part01_history/ch05_cpp14.md)、[ch11 编译器全景：GCC / Clang / MSVC 架构与 ABI（C++）](Book/part02_toolchain/ch11_compilers.md)、[ch20 引用（reference）vs 指针（pointer）：语义本质、底层实现与生命周期战争](Book/part03_language/ch20_reference_pointer.md)、[ch22 第 22 章 · `auto` 类型推导、`decltype` 与返回类型推导](Book/part03_language/ch22_auto_decltype.md)、[ch60 模板基础与实例化（Template Basics & Instantiation）](Book/part06_templates/ch60_template_basics.md)、[ch68 模板元编程 TMP 基础（递归 / 分支 / 循环）](Book/part06_templates/ch68_tmp.md)、[ch70 std::integral_constant 与标签分发（Tag Dispatch）](Book/part06_templates/ch70_tag_dispatch.md)、[ch92 时间库 chrono](Book/part07_stl/ch92_chrono.md)、[ch123 Compile-Time 编程范式总览](Book/part10_modern/ch123_ct_programming.md)

### ch70 · std::integral_constant 与标签分发（Tag Dispatch）

- 文件：`Book/part06_templates/ch70_tag_dispatch.md` ｜ Part：`part06_templates`
- **出链**（本章指向）：
  [ch65 类型特性 Type Traits —— 编译期类型自省与分发](Book/part06_templates/ch65_type_traits.md)、[ch69 编译期计算：constexpr / consteval / constinit](Book/part06_templates/ch69_constexpr.md)、[ch71 策略设计 Policy-Based Design](Book/part06_templates/ch71_policy.md)、[ch95 STL 算法分类与复杂度（C++）](Book/part08_algorithms/ch95_algo_overview.md)
- **入链**（指向本章）：
  [ch69 编译期计算：constexpr / consteval / constinit](Book/part06_templates/ch69_constexpr.md)、[ch71 策略设计 Policy-Based Design](Book/part06_templates/ch71_policy.md)

### ch71 · 策略设计 Policy-Based Design

- 文件：`Book/part06_templates/ch71_policy.md` ｜ Part：`part06_templates`
- **出链**（本章指向）：
  [ch65 类型特性 Type Traits —— 编译期类型自省与分发](Book/part06_templates/ch65_type_traits.md)、[ch70 std::integral_constant 与标签分发（Tag Dispatch）](Book/part06_templates/ch70_tag_dispatch.md)、[ch72 表达式模板 Expression Templates](Book/part06_templates/ch72_expression_templates.md)、[ch140 Policy-Based Design（C++）](Book/part12_patterns/ch140_policy_pattern.md)
- **入链**（指向本章）：
  [ch70 std::integral_constant 与标签分发（Tag Dispatch）](Book/part06_templates/ch70_tag_dispatch.md)、[ch72 表达式模板 Expression Templates](Book/part06_templates/ch72_expression_templates.md)、[ch76 STL 架构与迭代器概念](Book/part07_stl/ch76_stl_arch.md)、[ch140 Policy-Based Design（C++）](Book/part12_patterns/ch140_policy_pattern.md)

### ch72 · 表达式模板 Expression Templates

- 文件：`Book/part06_templates/ch72_expression_templates.md` ｜ Part：`part06_templates`
- **出链**（本章指向）：
  [ch51 CRTP 与静态多态（Curiously Recurring Template Pattern）](Book/part05_oo/ch51_crtp.md)、[ch68 模板元编程 TMP 基础（递归 / 分支 / 循环）](Book/part06_templates/ch68_tmp.md)、[ch71 策略设计 Policy-Based Design](Book/part06_templates/ch71_policy.md)
- **入链**（指向本章）：
  [ch71 策略设计 Policy-Based Design](Book/part06_templates/ch71_policy.md)

### ch76 · STL 架构与迭代器概念

- 文件：`Book/part07_stl/ch76_stl_arch.md` ｜ Part：`part07_stl`
- **出链**（本章指向）：
  [ch19 变量、存储期、链接与 ODR（工业级深度版）](Book/part03_language/ch19_variables.md)、[ch20 引用（reference）vs 指针（pointer）：语义本质、底层实现与生命周期战争](Book/part03_language/ch20_reference_pointer.md)、[ch38 第 38 章 分配器（Allocator）模型与 PMR](Book/part04_memory/ch38_allocator.md)、[ch60 模板基础与实例化（Template Basics & Instantiation）](Book/part06_templates/ch60_template_basics.md)、[ch65 类型特性 Type Traits —— 编译期类型自省与分发](Book/part06_templates/ch65_type_traits.md)、[ch67 Concepts 与 requires —— C++20 的编译期约束](Book/part06_templates/ch67_concepts.md)、[ch71 策略设计 Policy-Based Design](Book/part06_templates/ch71_policy.md)、[ch77 vector：扩容、失效、allocator 协作](Book/part07_stl/ch77_vector.md)、[ch84 set / multiset：红黑树有序集合](Book/part07_stl/ch84_set.md)、[ch85 unordered_map / unordered_set：哈希开链集合](Book/part07_stl/ch85_unordered.md)、[ch90 ranges 与 views：惰性求值与管道组合](Book/part07_stl/ch90_ranges.md)、[ch95 STL 算法分类与复杂度（C++）](Book/part08_algorithms/ch95_algo_overview.md)、[ch155 SIMD / AVX 向量化（C++/硬件）](Book/part14_perf/ch155_simd.md)
- **入链**（指向本章）：
  [ch77 vector：扩容、失效、allocator 协作](Book/part07_stl/ch77_vector.md)、[ch78 deque 与分段连续 [标准]](Book/part07_stl/ch78_deque.md)、[ch79 list / forward_list [标准]](Book/part07_stl/ch79_list.md)、[ch81 std::string 与 SSO 短字符串优化](Book/part07_stl/ch81_string.md)、[ch83 map / multimap（红黑树）](Book/part07_stl/ch83_map.md)、[ch84 set / multiset：红黑树有序集合](Book/part07_stl/ch84_set.md)、[ch86 容器适配器：stack / queue / priority_queue](Book/part07_stl/ch86_adapters.md)、[ch88 optional / expected / variant：可空与可辨别联合](Book/part07_stl/ch88_optional_variant.md)、[ch90 ranges 与 views：惰性求值与管道组合](Book/part07_stl/ch90_ranges.md)、[ch155 SIMD / AVX 向量化（C++/硬件）](Book/part14_perf/ch155_simd.md)
- **策展路径**：前置 ch19、ch60、ch67 ｜ 后续 ch77、ch84、ch85

### ch77 · vector：扩容、失效、allocator 协作

- 文件：`Book/part07_stl/ch77_vector.md` ｜ Part：`part07_stl`
- **出链**（本章指向）：
  [ch37 第 37 章 动态内存分配原语：`operator new` / `operator delete`](Book/part04_memory/ch37_new_delete.md)、[ch38 第 38 章 分配器（Allocator）模型与 PMR](Book/part04_memory/ch38_allocator.md)、[ch76 STL 架构与迭代器概念](Book/part07_stl/ch76_stl_arch.md)、[ch78 deque 与分段连续 [标准]](Book/part07_stl/ch78_deque.md)、[ch80 array 与固定数组](Book/part07_stl/ch80_array.md)、[ch84 set / multiset：红黑树有序集合](Book/part07_stl/ch84_set.md)、[ch85 unordered_map / unordered_set：哈希开链集合](Book/part07_stl/ch85_unordered.md)、[ch87 bitset：编译期定长位集](Book/part07_stl/ch87_bitset.md)、[ch115 移动语义与右值引用](Book/part10_modern/ch115_move.md)、[ch154 缓存优化与数据局部性（C++/硬件）](Book/part14_perf/ch154_cache_opt.md)
- **入链**（指向本章）：
  [ch26 lambda 表达式全解：闭包类型、捕获、泛型/模板 lambda、constexpr、ABI 与 std::function 类型擦除](Book/part03_language/ch26_lambda.md)、[ch39 第 39 章 RAII 与 Rule of Zero/Three/Five](Book/part04_memory/ch39_raii_rule.md)、[ch60 模板基础与实例化（Template Basics & Instantiation）](Book/part06_templates/ch60_template_basics.md)、[ch64 折叠表达式 Fold Expression（C++17）](Book/part06_templates/ch64_fold.md)、[ch76 STL 架构与迭代器概念](Book/part07_stl/ch76_stl_arch.md)、[ch78 deque 与分段连续 [标准]](Book/part07_stl/ch78_deque.md)、[ch79 list / forward_list [标准]](Book/part07_stl/ch79_list.md)、[ch80 array 与固定数组](Book/part07_stl/ch80_array.md)、[ch82 span 与裸数组视图](Book/part07_stl/ch82_span.md)、[ch83 map / multimap（红黑树）](Book/part07_stl/ch83_map.md)、[ch86 容器适配器：stack / queue / priority_queue](Book/part07_stl/ch86_adapters.md)、[ch87 bitset：编译期定长位集](Book/part07_stl/ch87_bitset.md)、[ch95 STL 算法分类与复杂度（C++）](Book/part08_algorithms/ch95_algo_overview.md)、[ch96 排序：sort / stable_sort / partial_sort（C++）](Book/part08_algorithms/ch96_sorting.md)、[ch115 移动语义与右值引用](Book/part10_modern/ch115_move.md)、[ch122 PMR 与多态分配器](Book/part10_modern/ch122_pmr.md)、[ch124 libstdc++ 架构与阅读入口（C++）](Book/part11_source/ch124_libstdcxx.md)、[ch130 Chromium / Abseil 基础设施（C++）](Book/part11_source/ch130_chromium_abseil.md)、[ch133 ClickHouse / Redis 实现精读（C++）](Book/part11_source/ch133_clickhouse_redis.md)、[ch153 CPU 微架构：流水线 / 分支预测 / 乱序执行](Book/part14_perf/ch153_cpu_micro.md)、[ch165 C++ 进阶路线图（C++）](Book/part16_reading/ch165_roadmap.md)
- **策展路径**：前置 ch37、ch38、ch76 ｜ 后续 ch78、ch84、ch154

### ch78 · deque 与分段连续 [标准]

- 文件：`Book/part07_stl/ch78_deque.md` ｜ Part：`part07_stl`
- **出链**（本章指向）：
  [ch20 引用（reference）vs 指针（pointer）：语义本质、底层实现与生命周期战争](Book/part03_language/ch20_reference_pointer.md)、[ch63 可变参数模板与包展开（Variadic Templates & Pack Expansion）](Book/part06_templates/ch63_variadic.md)、[ch76 STL 架构与迭代器概念](Book/part07_stl/ch76_stl_arch.md)、[ch77 vector：扩容、失效、allocator 协作](Book/part07_stl/ch77_vector.md)、[ch79 list / forward_list [标准]](Book/part07_stl/ch79_list.md)、[ch80 array 与固定数组](Book/part07_stl/ch80_array.md)、[ch82 span 与裸数组视图](Book/part07_stl/ch82_span.md)、[ch86 容器适配器：stack / queue / priority_queue](Book/part07_stl/ch86_adapters.md)、[ch90 ranges 与 views：惰性求值与管道组合](Book/part07_stl/ch90_ranges.md)、[ch93 线程与异步：thread / future / async](Book/part07_stl/ch93_thread_async.md)
- **入链**（指向本章）：
  [ch77 vector：扩容、失效、allocator 协作](Book/part07_stl/ch77_vector.md)、[ch79 list / forward_list [标准]](Book/part07_stl/ch79_list.md)、[ch86 容器适配器：stack / queue / priority_queue](Book/part07_stl/ch86_adapters.md)
- **策展路径**：前置 ch63、ch76、ch77、ch79、ch86、ch90 ｜ 后续 ch79、ch86、ch90

### ch79 · list / forward_list [标准]

- 文件：`Book/part07_stl/ch79_list.md` ｜ Part：`part07_stl`
- **出链**（本章指向）：
  [ch76 STL 架构与迭代器概念](Book/part07_stl/ch76_stl_arch.md)、[ch77 vector：扩容、失效、allocator 协作](Book/part07_stl/ch77_vector.md)、[ch78 deque 与分段连续 [标准]](Book/part07_stl/ch78_deque.md)、[ch86 容器适配器：stack / queue / priority_queue](Book/part07_stl/ch86_adapters.md)、[ch90 ranges 与 views：惰性求值与管道组合](Book/part07_stl/ch90_ranges.md)、[ch95 STL 算法分类与复杂度（C++）](Book/part08_algorithms/ch95_algo_overview.md)、[ch115 移动语义与右值引用](Book/part10_modern/ch115_move.md)、[ch131 fmt / spdlog 格式化与日志（C++）](Book/part11_source/ch131_fmt_spdlog.md)、[ch142 实体组件系统 ECS（C++）](Book/part12_patterns/ch142_ecs.md)
- **入链**（指向本章）：
  [ch78 deque 与分段连续 [标准]](Book/part07_stl/ch78_deque.md)、[ch81 std::string 与 SSO 短字符串优化](Book/part07_stl/ch81_string.md)、[ch82 span 与裸数组视图](Book/part07_stl/ch82_span.md)、[ch83 map / multimap（红黑树）](Book/part07_stl/ch83_map.md)、[ch131 fmt / spdlog 格式化与日志（C++）](Book/part11_source/ch131_fmt_spdlog.md)
- **策展路径**：前置 ch76、ch77、ch78、ch86、ch90 ｜ 后续 ch86、ch90

### ch80 · array 与固定数组

- 文件：`Book/part07_stl/ch80_array.md` ｜ Part：`part07_stl`
- **出链**（本章指向）：
  [ch19 变量、存储期、链接与 ODR（工业级深度版）](Book/part03_language/ch19_variables.md)、[ch20 引用（reference）vs 指针（pointer）：语义本质、底层实现与生命周期战争](Book/part03_language/ch20_reference_pointer.md)、[ch77 vector：扩容、失效、allocator 协作](Book/part07_stl/ch77_vector.md)、[ch81 std::string 与 SSO 短字符串优化](Book/part07_stl/ch81_string.md)、[ch82 span 与裸数组视图](Book/part07_stl/ch82_span.md)、[ch90 ranges 与 views：惰性求值与管道组合](Book/part07_stl/ch90_ranges.md)
- **入链**（指向本章）：
  [ch77 vector：扩容、失效、allocator 协作](Book/part07_stl/ch77_vector.md)、[ch78 deque 与分段连续 [标准]](Book/part07_stl/ch78_deque.md)、[ch81 std::string 与 SSO 短字符串优化](Book/part07_stl/ch81_string.md)、[ch82 span 与裸数组视图](Book/part07_stl/ch82_span.md)、[ch83 map / multimap（红黑树）](Book/part07_stl/ch83_map.md)、[ch87 bitset：编译期定长位集](Book/part07_stl/ch87_bitset.md)
- **策展路径**：前置 ch19、ch20、ch77、ch81、ch82、ch90 ｜ 后续 ch77、ch81、ch90

### ch81 · std::string 与 SSO 短字符串优化

- 文件：`Book/part07_stl/ch81_string.md` ｜ Part：`part07_stl`
- **出链**（本章指向）：
  [ch76 STL 架构与迭代器概念](Book/part07_stl/ch76_stl_arch.md)、[ch79 list / forward_list [标准]](Book/part07_stl/ch79_list.md)、[ch80 array 与固定数组](Book/part07_stl/ch80_array.md)、[ch82 span 与裸数组视图](Book/part07_stl/ch82_span.md)、[ch83 map / multimap（红黑树）](Book/part07_stl/ch83_map.md)、[ch91 文件系统 filesystem](Book/part07_stl/ch91_filesystem.md)、[ch122 PMR 与多态分配器](Book/part10_modern/ch122_pmr.md)
- **入链**（指向本章）：
  [ch80 array 与固定数组](Book/part07_stl/ch80_array.md)、[ch82 span 与裸数组视图](Book/part07_stl/ch82_span.md)、[ch91 文件系统 filesystem](Book/part07_stl/ch91_filesystem.md)、[ch122 PMR 与多态分配器](Book/part10_modern/ch122_pmr.md)

### ch82 · span 与裸数组视图

- 文件：`Book/part07_stl/ch82_span.md` ｜ Part：`part07_stl`
- **出链**（本章指向）：
  [ch20 引用（reference）vs 指针（pointer）：语义本质、底层实现与生命周期战争](Book/part03_language/ch20_reference_pointer.md)、[ch77 vector：扩容、失效、allocator 协作](Book/part07_stl/ch77_vector.md)、[ch79 list / forward_list [标准]](Book/part07_stl/ch79_list.md)、[ch80 array 与固定数组](Book/part07_stl/ch80_array.md)、[ch81 std::string 与 SSO 短字符串优化](Book/part07_stl/ch81_string.md)、[ch83 map / multimap（红黑树）](Book/part07_stl/ch83_map.md)、[ch88 optional / expected / variant：可空与可辨别联合](Book/part07_stl/ch88_optional_variant.md)、[ch90 ranges 与 views：惰性求值与管道组合](Book/part07_stl/ch90_ranges.md)、[ch95 STL 算法分类与复杂度（C++）](Book/part08_algorithms/ch95_algo_overview.md)
- **入链**（指向本章）：
  [ch78 deque 与分段连续 [标准]](Book/part07_stl/ch78_deque.md)、[ch80 array 与固定数组](Book/part07_stl/ch80_array.md)、[ch81 std::string 与 SSO 短字符串优化](Book/part07_stl/ch81_string.md)
- **策展路径**：前置 ch20、ch77、ch80、ch83、ch90 ｜ 后续 ch83、ch90

### ch83 · map / multimap（红黑树）

- 文件：`Book/part07_stl/ch83_map.md` ｜ Part：`part07_stl`
- **出链**（本章指向）：
  [ch20 引用（reference）vs 指针（pointer）：语义本质、底层实现与生命周期战争](Book/part03_language/ch20_reference_pointer.md)、[ch76 STL 架构与迭代器概念](Book/part07_stl/ch76_stl_arch.md)、[ch77 vector：扩容、失效、allocator 协作](Book/part07_stl/ch77_vector.md)、[ch79 list / forward_list [标准]](Book/part07_stl/ch79_list.md)、[ch80 array 与固定数组](Book/part07_stl/ch80_array.md)、[ch84 set / multiset：红黑树有序集合](Book/part07_stl/ch84_set.md)、[ch85 unordered_map / unordered_set：哈希开链集合](Book/part07_stl/ch85_unordered.md)、[ch88 optional / expected / variant：可空与可辨别联合](Book/part07_stl/ch88_optional_variant.md)、[ch90 ranges 与 views：惰性求值与管道组合](Book/part07_stl/ch90_ranges.md)、[ch143 面向数据设计 DOD（C++）](Book/part12_patterns/ch143_dod.md)
- **入链**（指向本章）：
  [ch81 std::string 与 SSO 短字符串优化](Book/part07_stl/ch81_string.md)、[ch82 span 与裸数组视图](Book/part07_stl/ch82_span.md)、[ch84 set / multiset：红黑树有序集合](Book/part07_stl/ch84_set.md)、[ch85 unordered_map / unordered_set：哈希开链集合](Book/part07_stl/ch85_unordered.md)、[ch97 查找与二分（C++）](Book/part08_algorithms/ch97_search.md)、[ch122 PMR 与多态分配器](Book/part10_modern/ch122_pmr.md)、[ch132 LevelDB / RocksDB 存储引擎（C++）](Book/part11_source/ch132_leveldb_rocksdb.md)
- **策展路径**：前置 ch20、ch76、ch80、ch84、ch85、ch90 ｜ 后续 ch84、ch85、ch90

### ch84 · set / multiset：红黑树有序集合

- 文件：`Book/part07_stl/ch84_set.md` ｜ Part：`part07_stl`
- **出链**（本章指向）：
  [ch19 变量、存储期、链接与 ODR（工业级深度版）](Book/part03_language/ch19_variables.md)、[ch40 第 40 章 异常安全（Exception Safety）](Book/part04_memory/ch40_exception_safety.md)、[ch65 类型特性 Type Traits —— 编译期类型自省与分发](Book/part06_templates/ch65_type_traits.md)、[ch76 STL 架构与迭代器概念](Book/part07_stl/ch76_stl_arch.md)、[ch83 map / multimap（红黑树）](Book/part07_stl/ch83_map.md)、[ch85 unordered_map / unordered_set：哈希开链集合](Book/part07_stl/ch85_unordered.md)、[ch86 容器适配器：stack / queue / priority_queue](Book/part07_stl/ch86_adapters.md)、[ch115 移动语义与右值引用](Book/part10_modern/ch115_move.md)、[ch154 缓存优化与数据局部性（C++/硬件）](Book/part14_perf/ch154_cache_opt.md)
- **入链**（指向本章）：
  [ch40 第 40 章 异常安全（Exception Safety）](Book/part04_memory/ch40_exception_safety.md)、[ch76 STL 架构与迭代器概念](Book/part07_stl/ch76_stl_arch.md)、[ch77 vector：扩容、失效、allocator 协作](Book/part07_stl/ch77_vector.md)、[ch83 map / multimap（红黑树）](Book/part07_stl/ch83_map.md)、[ch85 unordered_map / unordered_set：哈希开链集合](Book/part07_stl/ch85_unordered.md)
- **策展路径**：前置 ch19、ch65、ch83 ｜ 后续 ch85、ch154

### ch85 · unordered_map / unordered_set：哈希开链集合

- 文件：`Book/part07_stl/ch85_unordered.md` ｜ Part：`part07_stl`
- **出链**（本章指向）：
  [ch19 变量、存储期、链接与 ODR（工业级深度版）](Book/part03_language/ch19_variables.md)、[ch65 类型特性 Type Traits —— 编译期类型自省与分发](Book/part06_templates/ch65_type_traits.md)、[ch83 map / multimap（红黑树）](Book/part07_stl/ch83_map.md)、[ch84 set / multiset：红黑树有序集合](Book/part07_stl/ch84_set.md)、[ch115 移动语义与右值引用](Book/part10_modern/ch115_move.md)、[ch124 libstdc++ 架构与阅读入口（C++）](Book/part11_source/ch124_libstdcxx.md)、[ch154 缓存优化与数据局部性（C++/硬件）](Book/part14_perf/ch154_cache_opt.md)
- **入链**（指向本章）：
  [ch76 STL 架构与迭代器概念](Book/part07_stl/ch76_stl_arch.md)、[ch77 vector：扩容、失效、allocator 协作](Book/part07_stl/ch77_vector.md)、[ch83 map / multimap（红黑树）](Book/part07_stl/ch83_map.md)、[ch84 set / multiset：红黑树有序集合](Book/part07_stl/ch84_set.md)
- **策展路径**：前置 ch19、ch65、ch84 ｜ 后续 ch124、ch154

### ch86 · 容器适配器：stack / queue / priority_queue

- 文件：`Book/part07_stl/ch86_adapters.md` ｜ Part：`part07_stl`
- **出链**（本章指向）：
  [ch19 变量、存储期、链接与 ODR（工业级深度版）](Book/part03_language/ch19_variables.md)、[ch26 lambda 表达式全解：闭包类型、捕获、泛型/模板 lambda、constexpr、ABI 与 std::function 类型擦除](Book/part03_language/ch26_lambda.md)、[ch52 空基类优化 EBO（Empty Base Optimization）](Book/part05_oo/ch52_ebo.md)、[ch65 类型特性 Type Traits —— 编译期类型自省与分发](Book/part06_templates/ch65_type_traits.md)、[ch76 STL 架构与迭代器概念](Book/part07_stl/ch76_stl_arch.md)、[ch77 vector：扩容、失效、allocator 协作](Book/part07_stl/ch77_vector.md)、[ch78 deque 与分段连续 [标准]](Book/part07_stl/ch78_deque.md)、[ch88 optional / expected / variant：可空与可辨别联合](Book/part07_stl/ch88_optional_variant.md)、[ch93 线程与异步：thread / future / async](Book/part07_stl/ch93_thread_async.md)、[ch98 堆算法 heap（C++）](Book/part08_algorithms/ch98_heap.md)、[ch124 libstdc++ 架构与阅读入口（C++）](Book/part11_source/ch124_libstdcxx.md)、[ch152 性能模型与测量学](Book/part14_perf/ch152_perf_model.md)、[ch159 从零实现线程池（C++）](Book/part15_cases/ch159_threadpool.md)
- **入链**（指向本章）：
  [ch78 deque 与分段连续 [标准]](Book/part07_stl/ch78_deque.md)、[ch79 list / forward_list [标准]](Book/part07_stl/ch79_list.md)、[ch84 set / multiset：红黑树有序集合](Book/part07_stl/ch84_set.md)、[ch88 optional / expected / variant：可空与可辨别联合](Book/part07_stl/ch88_optional_variant.md)
- **策展路径**：前置 ch76、ch77、ch78 ｜ 后续 ch19、ch88、ch98

### ch87 · bitset：编译期定长位集

- 文件：`Book/part07_stl/ch87_bitset.md` ｜ Part：`part07_stl`
- **出链**（本章指向）：
  [ch43 第 43 章 CPU 缓存体系与内存局部性](Book/part04_memory/ch43_cache_locality.md)、[ch65 类型特性 Type Traits —— 编译期类型自省与分发](Book/part06_templates/ch65_type_traits.md)、[ch77 vector：扩容、失效、allocator 协作](Book/part07_stl/ch77_vector.md)、[ch80 array 与固定数组](Book/part07_stl/ch80_array.md)、[ch88 optional / expected / variant：可空与可辨别联合](Book/part07_stl/ch88_optional_variant.md)、[ch124 libstdc++ 架构与阅读入口（C++）](Book/part11_source/ch124_libstdcxx.md)、[ch152 性能模型与测量学](Book/part14_perf/ch152_perf_model.md)、[ch155 SIMD / AVX 向量化（C++/硬件）](Book/part14_perf/ch155_simd.md)
- **入链**（指向本章）：
  [ch77 vector：扩容、失效、allocator 协作](Book/part07_stl/ch77_vector.md)、[ch88 optional / expected / variant：可空与可辨别联合](Book/part07_stl/ch88_optional_variant.md)、[ch155 SIMD / AVX 向量化（C++/硬件）](Book/part14_perf/ch155_simd.md)
- **策展路径**：前置 ch65、ch77、ch80 ｜ 后续 ch88、ch124、ch155

### ch88 · optional / expected / variant：可空与可辨别联合

- 文件：`Book/part07_stl/ch88_optional_variant.md` ｜ Part：`part07_stl`
- **出链**（本章指向）：
  [ch06 C++17：生产力跃升](Book/part01_history/ch06_cpp17.md)、[ch08 C++23：标准库大修](Book/part01_history/ch08_cpp23.md)、[ch76 STL 架构与迭代器概念](Book/part07_stl/ch76_stl_arch.md)、[ch86 容器适配器：stack / queue / priority_queue](Book/part07_stl/ch86_adapters.md)、[ch87 bitset：编译期定长位集](Book/part07_stl/ch87_bitset.md)、[ch89 tuple / pair / any / function / bind](Book/part07_stl/ch89_tuple_any.md)、[ch90 ranges 与 views：惰性求值与管道组合](Book/part07_stl/ch90_ranges.md)
- **入链**（指向本章）：
  [ch06 C++17：生产力跃升](Book/part01_history/ch06_cpp17.md)、[ch08 C++23：标准库大修](Book/part01_history/ch08_cpp23.md)、[ch25 union 与 std::variant 深度详解](Book/part03_language/ch25_union_variant.md)、[ch82 span 与裸数组视图](Book/part07_stl/ch82_span.md)、[ch83 map / multimap（红黑树）](Book/part07_stl/ch83_map.md)、[ch86 容器适配器：stack / queue / priority_queue](Book/part07_stl/ch86_adapters.md)、[ch87 bitset：编译期定长位集](Book/part07_stl/ch87_bitset.md)、[ch89 tuple / pair / any / function / bind](Book/part07_stl/ch89_tuple_any.md)、[ch90 ranges 与 views：惰性求值与管道组合](Book/part07_stl/ch90_ranges.md)、[ch91 文件系统 filesystem](Book/part07_stl/ch91_filesystem.md)、[ch92 时间库 chrono](Book/part07_stl/ch92_chrono.md)、[ch146 错误处理（C++）](Book/part13_engineering/ch146_error_handling.md)、[ch162 从零实现 JSON 库（C++）](Book/part15_cases/ch162_json.md)

### ch89 · tuple / pair / any / function / bind

- 文件：`Book/part07_stl/ch89_tuple_any.md` ｜ Part：`part07_stl`
- **出链**（本章指向）：
  [ch20 引用（reference）vs 指针（pointer）：语义本质、底层实现与生命周期战争](Book/part03_language/ch20_reference_pointer.md)、[ch26 lambda 表达式全解：闭包类型、捕获、泛型/模板 lambda、constexpr、ABI 与 std::function 类型擦除](Book/part03_language/ch26_lambda.md)、[ch52 空基类优化 EBO（Empty Base Optimization）](Book/part05_oo/ch52_ebo.md)、[ch63 可变参数模板与包展开（Variadic Templates & Pack Expansion）](Book/part06_templates/ch63_variadic.md)、[ch64 折叠表达式 Fold Expression（C++17）](Book/part06_templates/ch64_fold.md)、[ch88 optional / expected / variant：可空与可辨别联合](Book/part07_stl/ch88_optional_variant.md)、[ch90 ranges 与 views：惰性求值与管道组合](Book/part07_stl/ch90_ranges.md)、[ch100 Ranges 算法与投影（C++20）](Book/part08_algorithms/ch100_ranges_algo.md)、[ch116 完美转发与万能引用](Book/part10_modern/ch116_perfect_forwarding.md)
- **入链**（指向本章）：
  [ch88 optional / expected / variant：可空与可辨别联合](Book/part07_stl/ch88_optional_variant.md)、[ch90 ranges 与 views：惰性求值与管道组合](Book/part07_stl/ch90_ranges.md)

### ch90 · ranges 与 views：惰性求值与管道组合

- 文件：`Book/part07_stl/ch90_ranges.md` ｜ Part：`part07_stl`
- **出链**（本章指向）：
  [ch26 lambda 表达式全解：闭包类型、捕获、泛型/模板 lambda、constexpr、ABI 与 std::function 类型擦除](Book/part03_language/ch26_lambda.md)、[ch67 Concepts 与 requires —— C++20 的编译期约束](Book/part06_templates/ch67_concepts.md)、[ch76 STL 架构与迭代器概念](Book/part07_stl/ch76_stl_arch.md)、[ch88 optional / expected / variant：可空与可辨别联合](Book/part07_stl/ch88_optional_variant.md)、[ch89 tuple / pair / any / function / bind](Book/part07_stl/ch89_tuple_any.md)、[ch91 文件系统 filesystem](Book/part07_stl/ch91_filesystem.md)、[ch100 Ranges 算法与投影（C++20）](Book/part08_algorithms/ch100_ranges_algo.md)、[ch119 Ranges 深入（C++20）](Book/part10_modern/ch119_ranges_deep.md)
- **入链**（指向本章）：
  [ch76 STL 架构与迭代器概念](Book/part07_stl/ch76_stl_arch.md)、[ch78 deque 与分段连续 [标准]](Book/part07_stl/ch78_deque.md)、[ch79 list / forward_list [标准]](Book/part07_stl/ch79_list.md)、[ch80 array 与固定数组](Book/part07_stl/ch80_array.md)、[ch82 span 与裸数组视图](Book/part07_stl/ch82_span.md)、[ch83 map / multimap（红黑树）](Book/part07_stl/ch83_map.md)、[ch88 optional / expected / variant：可空与可辨别联合](Book/part07_stl/ch88_optional_variant.md)、[ch89 tuple / pair / any / function / bind](Book/part07_stl/ch89_tuple_any.md)、[ch91 文件系统 filesystem](Book/part07_stl/ch91_filesystem.md)、[ch92 时间库 chrono](Book/part07_stl/ch92_chrono.md)

### ch91 · 文件系统 filesystem

- 文件：`Book/part07_stl/ch91_filesystem.md` ｜ Part：`part07_stl`
- **出链**（本章指向）：
  [ch19 变量、存储期、链接与 ODR（工业级深度版）](Book/part03_language/ch19_variables.md)、[ch39 第 39 章 RAII 与 Rule of Zero/Three/Five](Book/part04_memory/ch39_raii_rule.md)、[ch40 第 40 章 异常安全（Exception Safety）](Book/part04_memory/ch40_exception_safety.md)、[ch47 虚函数与虚表（vtable）：动态多态的发动机](Book/part05_oo/ch47_virtual_functions.md)、[ch81 std::string 与 SSO 短字符串优化](Book/part07_stl/ch81_string.md)、[ch88 optional / expected / variant：可空与可辨别联合](Book/part07_stl/ch88_optional_variant.md)、[ch90 ranges 与 views：惰性求值与管道组合](Book/part07_stl/ch90_ranges.md)、[ch92 时间库 chrono](Book/part07_stl/ch92_chrono.md)、[ch107 std::atomic 原子类型（C++11）](Book/part09_concurrency/ch107_atomic.md)、[ch115 移动语义与右值引用](Book/part10_modern/ch115_move.md)、[ch122 PMR 与多态分配器](Book/part10_modern/ch122_pmr.md)、[ch146 错误处理（C++）](Book/part13_engineering/ch146_error_handling.md)
- **入链**（指向本章）：
  [ch40 第 40 章 异常安全（Exception Safety）](Book/part04_memory/ch40_exception_safety.md)、[ch81 std::string 与 SSO 短字符串优化](Book/part07_stl/ch81_string.md)、[ch90 ranges 与 views：惰性求值与管道组合](Book/part07_stl/ch90_ranges.md)、[ch92 时间库 chrono](Book/part07_stl/ch92_chrono.md)
- **策展路径**：前置 ch19、ch39、ch47 ｜ 后续 ch92、ch122

### ch92 · 时间库 chrono

- 文件：`Book/part07_stl/ch92_chrono.md` ｜ Part：`part07_stl`
- **出链**（本章指向）：
  [ch08 C++23：标准库大修](Book/part01_history/ch08_cpp23.md)、[ch19 变量、存储期、链接与 ODR（工业级深度版）](Book/part03_language/ch19_variables.md)、[ch39 第 39 章 RAII 与 Rule of Zero/Three/Five](Book/part04_memory/ch39_raii_rule.md)、[ch40 第 40 章 异常安全（Exception Safety）](Book/part04_memory/ch40_exception_safety.md)、[ch47 虚函数与虚表（vtable）：动态多态的发动机](Book/part05_oo/ch47_virtual_functions.md)、[ch60 模板基础与实例化（Template Basics & Instantiation）](Book/part06_templates/ch60_template_basics.md)、[ch68 模板元编程 TMP 基础（递归 / 分支 / 循环）](Book/part06_templates/ch68_tmp.md)、[ch69 编译期计算：constexpr / consteval / constinit](Book/part06_templates/ch69_constexpr.md)、[ch88 optional / expected / variant：可空与可辨别联合](Book/part07_stl/ch88_optional_variant.md)、[ch90 ranges 与 views：惰性求值与管道组合](Book/part07_stl/ch90_ranges.md)、[ch91 文件系统 filesystem](Book/part07_stl/ch91_filesystem.md)、[ch93 线程与异步：thread / future / async](Book/part07_stl/ch93_thread_async.md)、[ch131 fmt / spdlog 格式化与日志（C++）](Book/part11_source/ch131_fmt_spdlog.md)、[ch151 基准测试与性能度量（C++）](Book/part13_engineering/ch151_benchmark.md)、[ch152 性能模型与测量学](Book/part14_perf/ch152_perf_model.md)
- **入链**（指向本章）：
  [ch91 文件系统 filesystem](Book/part07_stl/ch91_filesystem.md)、[ch131 fmt / spdlog 格式化与日志（C++）](Book/part11_source/ch131_fmt_spdlog.md)
- **策展路径**：前置 ch19、ch39、ch47 ｜ 后续 ch91、ch151、ch152

### ch93 · 线程与异步：thread / future / async

- 文件：`Book/part07_stl/ch93_thread_async.md` ｜ Part：`part07_stl`
- **出链**（本章指向）：
  [ch19 变量、存储期、链接与 ODR（工业级深度版）](Book/part03_language/ch19_variables.md)、[ch40 第 40 章 异常安全（Exception Safety）](Book/part04_memory/ch40_exception_safety.md)、[ch63 可变参数模板与包展开（Variadic Templates & Pack Expansion）](Book/part06_templates/ch63_variadic.md)、[ch94 stop_token 与协作取消 [标准]](Book/part07_stl/ch94_stop_token.md)、[ch107 std::atomic 原子类型（C++11）](Book/part09_concurrency/ch107_atomic.md)、[ch108 memory_order：六种内存序（C++11）](Book/part09_concurrency/ch108_memory_order.md)、[ch110 无锁编程：lock-free / wait-free（C++11）](Book/part09_concurrency/ch110_lockfree.md)、[ch115 移动语义与右值引用](Book/part10_modern/ch115_move.md)、[ch159 从零实现线程池（C++）](Book/part15_cases/ch159_threadpool.md)
- **入链**（指向本章）：
  [ch78 deque 与分段连续 [标准]](Book/part07_stl/ch78_deque.md)、[ch86 容器适配器：stack / queue / priority_queue](Book/part07_stl/ch86_adapters.md)、[ch92 时间库 chrono](Book/part07_stl/ch92_chrono.md)、[ch94 stop_token 与协作取消 [标准]](Book/part07_stl/ch94_stop_token.md)、[ch110 无锁编程：lock-free / wait-free（C++11）](Book/part09_concurrency/ch110_lockfree.md)、[ch122 PMR 与多态分配器](Book/part10_modern/ch122_pmr.md)
- **策展路径**：前置 ch19、ch63、ch93、ch94、ch107 ｜ 后续 ch93、ch94、ch107

### ch94 · stop_token 与协作取消 [标准]

- 文件：`Book/part07_stl/ch94_stop_token.md` ｜ Part：`part07_stl`
- **出链**（本章指向）：
  [ch39 第 39 章 RAII 与 Rule of Zero/Three/Five](Book/part04_memory/ch39_raii_rule.md)、[ch93 线程与异步：thread / future / async](Book/part07_stl/ch93_thread_async.md)、[ch107 std::atomic 原子类型（C++11）](Book/part09_concurrency/ch107_atomic.md)、[ch108 memory_order：六种内存序（C++11）](Book/part09_concurrency/ch108_memory_order.md)、[ch159 从零实现线程池（C++）](Book/part15_cases/ch159_threadpool.md)
- **入链**（指向本章）：
  [ch93 线程与异步：thread / future / async](Book/part07_stl/ch93_thread_async.md)
- **策展路径**：前置 ch93、ch107 ｜ 后续 ch93

### ch95 · STL 算法分类与复杂度（C++）

- 文件：`Book/part08_algorithms/ch95_algo_overview.md` ｜ Part：`part08_algorithms`
- **出链**（本章指向）：
  [ch77 vector：扩容、失效、allocator 协作](Book/part07_stl/ch77_vector.md)、[ch96 排序：sort / stable_sort / partial_sort（C++）](Book/part08_algorithms/ch96_sorting.md)、[ch97 查找与二分（C++）](Book/part08_algorithms/ch97_search.md)
- **入链**（指向本章）：
  [ch70 std::integral_constant 与标签分发（Tag Dispatch）](Book/part06_templates/ch70_tag_dispatch.md)、[ch76 STL 架构与迭代器概念](Book/part07_stl/ch76_stl_arch.md)、[ch79 list / forward_list [标准]](Book/part07_stl/ch79_list.md)、[ch82 span 与裸数组视图](Book/part07_stl/ch82_span.md)、[ch96 排序：sort / stable_sort / partial_sort（C++）](Book/part08_algorithms/ch96_sorting.md)、[ch99 数值算法与并行执行策略（C++）](Book/part08_algorithms/ch99_numeric.md)、[ch100 Ranges 算法与投影（C++20）](Book/part08_algorithms/ch100_ranges_algo.md)、[ch101 哈希、图、树、DP、贪心（算法思想）](Book/part08_algorithms/ch101_algo_theory.md)、[ch153 CPU 微架构：流水线 / 分支预测 / 乱序执行](Book/part14_perf/ch153_cpu_micro.md)

### ch96 · 排序：sort / stable_sort / partial_sort（C++）

- 文件：`Book/part08_algorithms/ch96_sorting.md` ｜ Part：`part08_algorithms`
- **出链**（本章指向）：
  [ch77 vector：扩容、失效、allocator 协作](Book/part07_stl/ch77_vector.md)、[ch95 STL 算法分类与复杂度（C++）](Book/part08_algorithms/ch95_algo_overview.md)、[ch97 查找与二分（C++）](Book/part08_algorithms/ch97_search.md)、[ch98 堆算法 heap（C++）](Book/part08_algorithms/ch98_heap.md)
- **入链**（指向本章）：
  [ch95 STL 算法分类与复杂度（C++）](Book/part08_algorithms/ch95_algo_overview.md)、[ch97 查找与二分（C++）](Book/part08_algorithms/ch97_search.md)、[ch98 堆算法 heap（C++）](Book/part08_algorithms/ch98_heap.md)、[ch101 哈希、图、树、DP、贪心（算法思想）](Book/part08_algorithms/ch101_algo_theory.md)、[ch132 LevelDB / RocksDB 存储引擎（C++）](Book/part11_source/ch132_leveldb_rocksdb.md)、[ch153 CPU 微架构：流水线 / 分支预测 / 乱序执行](Book/part14_perf/ch153_cpu_micro.md)

### ch97 · 查找与二分（C++）

- 文件：`Book/part08_algorithms/ch97_search.md` ｜ Part：`part08_algorithms`
- **出链**（本章指向）：
  [ch83 map / multimap（红黑树）](Book/part07_stl/ch83_map.md)、[ch96 排序：sort / stable_sort / partial_sort（C++）](Book/part08_algorithms/ch96_sorting.md)、[ch98 堆算法 heap（C++）](Book/part08_algorithms/ch98_heap.md)
- **入链**（指向本章）：
  [ch95 STL 算法分类与复杂度（C++）](Book/part08_algorithms/ch95_algo_overview.md)、[ch96 排序：sort / stable_sort / partial_sort（C++）](Book/part08_algorithms/ch96_sorting.md)、[ch98 堆算法 heap（C++）](Book/part08_algorithms/ch98_heap.md)

### ch98 · 堆算法 heap（C++）

- 文件：`Book/part08_algorithms/ch98_heap.md` ｜ Part：`part08_algorithms`
- **出链**（本章指向）：
  [ch96 排序：sort / stable_sort / partial_sort（C++）](Book/part08_algorithms/ch96_sorting.md)、[ch97 查找与二分（C++）](Book/part08_algorithms/ch97_search.md)、[ch99 数值算法与并行执行策略（C++）](Book/part08_algorithms/ch99_numeric.md)
- **入链**（指向本章）：
  [ch86 容器适配器：stack / queue / priority_queue](Book/part07_stl/ch86_adapters.md)、[ch96 排序：sort / stable_sort / partial_sort（C++）](Book/part08_algorithms/ch96_sorting.md)、[ch97 查找与二分（C++）](Book/part08_algorithms/ch97_search.md)、[ch99 数值算法与并行执行策略（C++）](Book/part08_algorithms/ch99_numeric.md)

### ch99 · 数值算法与并行执行策略（C++）

- 文件：`Book/part08_algorithms/ch99_numeric.md` ｜ Part：`part08_algorithms`
- **出链**（本章指向）：
  [ch95 STL 算法分类与复杂度（C++）](Book/part08_algorithms/ch95_algo_overview.md)、[ch98 堆算法 heap（C++）](Book/part08_algorithms/ch98_heap.md)、[ch100 Ranges 算法与投影（C++20）](Book/part08_algorithms/ch100_ranges_algo.md)、[ch151 基准测试与性能度量（C++）](Book/part13_engineering/ch151_benchmark.md)
- **入链**（指向本章）：
  [ch98 堆算法 heap（C++）](Book/part08_algorithms/ch98_heap.md)、[ch100 Ranges 算法与投影（C++20）](Book/part08_algorithms/ch100_ranges_algo.md)

### ch100 · Ranges 算法与投影（C++20）

- 文件：`Book/part08_algorithms/ch100_ranges_algo.md` ｜ Part：`part08_algorithms`
- **出链**（本章指向）：
  [ch95 STL 算法分类与复杂度（C++）](Book/part08_algorithms/ch95_algo_overview.md)、[ch99 数值算法与并行执行策略（C++）](Book/part08_algorithms/ch99_numeric.md)、[ch101 哈希、图、树、DP、贪心（算法思想）](Book/part08_algorithms/ch101_algo_theory.md)、[ch119 Ranges 深入（C++20）](Book/part10_modern/ch119_ranges_deep.md)
- **入链**（指向本章）：
  [ch89 tuple / pair / any / function / bind](Book/part07_stl/ch89_tuple_any.md)、[ch90 ranges 与 views：惰性求值与管道组合](Book/part07_stl/ch90_ranges.md)、[ch99 数值算法与并行执行策略（C++）](Book/part08_algorithms/ch99_numeric.md)、[ch101 哈希、图、树、DP、贪心（算法思想）](Book/part08_algorithms/ch101_algo_theory.md)

### ch101 · 哈希、图、树、DP、贪心（算法思想）

- 文件：`Book/part08_algorithms/ch101_algo_theory.md` ｜ Part：`part08_algorithms`
- **出链**（本章指向）：
  [ch95 STL 算法分类与复杂度（C++）](Book/part08_algorithms/ch95_algo_overview.md)、[ch96 排序：sort / stable_sort / partial_sort（C++）](Book/part08_algorithms/ch96_sorting.md)、[ch100 Ranges 算法与投影（C++20）](Book/part08_algorithms/ch100_ranges_algo.md)
- **入链**（指向本章）：
  [ch100 Ranges 算法与投影（C++20）](Book/part08_algorithms/ch100_ranges_algo.md)

### ch107 · std::atomic 原子类型（C++11）

- 文件：`Book/part09_concurrency/ch107_atomic.md` ｜ Part：`part09_concurrency`
- **出链**（本章指向）：
  [ch30 volatile / atomic 与硬件寄存器](Book/part03_language/ch30_volatile.md)、[ch108 memory_order：六种内存序（C++11）](Book/part09_concurrency/ch108_memory_order.md)、[ch109 内存屏障与 fence](Book/part09_concurrency/ch109_fence.md)、[ch110 无锁编程：lock-free / wait-free（C++11）](Book/part09_concurrency/ch110_lockfree.md)、[ch111 ABA 问题与解决（C++11）](Book/part09_concurrency/ch111_aba.md)
- **入链**（指向本章）：
  [ch30 volatile / atomic 与硬件寄存器](Book/part03_language/ch30_volatile.md)、[ch91 文件系统 filesystem](Book/part07_stl/ch91_filesystem.md)、[ch93 线程与异步：thread / future / async](Book/part07_stl/ch93_thread_async.md)、[ch94 stop_token 与协作取消 [标准]](Book/part07_stl/ch94_stop_token.md)、[ch108 memory_order：六种内存序（C++11）](Book/part09_concurrency/ch108_memory_order.md)、[ch109 内存屏障与 fence](Book/part09_concurrency/ch109_fence.md)、[ch110 无锁编程：lock-free / wait-free（C++11）](Book/part09_concurrency/ch110_lockfree.md)、[ch111 ABA 问题与解决（C++11）](Book/part09_concurrency/ch111_aba.md)、[ch113 协程 coroutine：promise / awaiter（C++20）](Book/part09_concurrency/ch113_coroutine.md)、[ch116 完美转发与万能引用](Book/part10_modern/ch116_perfect_forwarding.md)、[ch153 CPU 微架构：流水线 / 分支预测 / 乱序执行](Book/part14_perf/ch153_cpu_micro.md)、[ch159 从零实现线程池（C++）](Book/part15_cases/ch159_threadpool.md)

### ch108 · memory_order：六种内存序（C++11）

- 文件：`Book/part09_concurrency/ch108_memory_order.md` ｜ Part：`part09_concurrency`
- **出链**（本章指向）：
  [ch107 std::atomic 原子类型（C++11）](Book/part09_concurrency/ch107_atomic.md)、[ch109 内存屏障与 fence](Book/part09_concurrency/ch109_fence.md)、[ch110 无锁编程：lock-free / wait-free（C++11）](Book/part09_concurrency/ch110_lockfree.md)
- **入链**（指向本章）：
  [ch93 线程与异步：thread / future / async](Book/part07_stl/ch93_thread_async.md)、[ch94 stop_token 与协作取消 [标准]](Book/part07_stl/ch94_stop_token.md)、[ch107 std::atomic 原子类型（C++11）](Book/part09_concurrency/ch107_atomic.md)、[ch109 内存屏障与 fence](Book/part09_concurrency/ch109_fence.md)、[ch110 无锁编程：lock-free / wait-free（C++11）](Book/part09_concurrency/ch110_lockfree.md)、[ch111 ABA 问题与解决（C++11）](Book/part09_concurrency/ch111_aba.md)

### ch109 · 内存屏障与 fence

- 文件：`Book/part09_concurrency/ch109_fence.md` ｜ Part：`part09_concurrency`
- **出链**（本章指向）：
  [ch107 std::atomic 原子类型（C++11）](Book/part09_concurrency/ch107_atomic.md)、[ch108 memory_order：六种内存序（C++11）](Book/part09_concurrency/ch108_memory_order.md)、[ch110 无锁编程：lock-free / wait-free（C++11）](Book/part09_concurrency/ch110_lockfree.md)
- **入链**（指向本章）：
  [ch107 std::atomic 原子类型（C++11）](Book/part09_concurrency/ch107_atomic.md)、[ch108 memory_order：六种内存序（C++11）](Book/part09_concurrency/ch108_memory_order.md)、[ch110 无锁编程：lock-free / wait-free（C++11）](Book/part09_concurrency/ch110_lockfree.md)、[ch111 ABA 问题与解决（C++11）](Book/part09_concurrency/ch111_aba.md)

### ch110 · 无锁编程：lock-free / wait-free（C++11）

- 文件：`Book/part09_concurrency/ch110_lockfree.md` ｜ Part：`part09_concurrency`
- **出链**（本章指向）：
  [ch93 线程与异步：thread / future / async](Book/part07_stl/ch93_thread_async.md)、[ch107 std::atomic 原子类型（C++11）](Book/part09_concurrency/ch107_atomic.md)、[ch108 memory_order：六种内存序（C++11）](Book/part09_concurrency/ch108_memory_order.md)、[ch109 内存屏障与 fence](Book/part09_concurrency/ch109_fence.md)、[ch111 ABA 问题与解决（C++11）](Book/part09_concurrency/ch111_aba.md)、[ch112 Hazard Pointer 与 RCU（C++11/实践）](Book/part09_concurrency/ch112_hazard_rcu.md)、[ch113 协程 coroutine：promise / awaiter（C++20）](Book/part09_concurrency/ch113_coroutine.md)
- **入链**（指向本章）：
  [ch93 线程与异步：thread / future / async](Book/part07_stl/ch93_thread_async.md)、[ch107 std::atomic 原子类型（C++11）](Book/part09_concurrency/ch107_atomic.md)、[ch108 memory_order：六种内存序（C++11）](Book/part09_concurrency/ch108_memory_order.md)、[ch109 内存屏障与 fence](Book/part09_concurrency/ch109_fence.md)、[ch111 ABA 问题与解决（C++11）](Book/part09_concurrency/ch111_aba.md)、[ch112 Hazard Pointer 与 RCU（C++11/实践）](Book/part09_concurrency/ch112_hazard_rcu.md)

### ch111 · ABA 问题与解决（C++11）

- 文件：`Book/part09_concurrency/ch111_aba.md` ｜ Part：`part09_concurrency`
- **出链**（本章指向）：
  [ch107 std::atomic 原子类型（C++11）](Book/part09_concurrency/ch107_atomic.md)、[ch108 memory_order：六种内存序（C++11）](Book/part09_concurrency/ch108_memory_order.md)、[ch109 内存屏障与 fence](Book/part09_concurrency/ch109_fence.md)、[ch110 无锁编程：lock-free / wait-free（C++11）](Book/part09_concurrency/ch110_lockfree.md)、[ch112 Hazard Pointer 与 RCU（C++11/实践）](Book/part09_concurrency/ch112_hazard_rcu.md)、[ch113 协程 coroutine：promise / awaiter（C++20）](Book/part09_concurrency/ch113_coroutine.md)
- **入链**（指向本章）：
  [ch107 std::atomic 原子类型（C++11）](Book/part09_concurrency/ch107_atomic.md)、[ch110 无锁编程：lock-free / wait-free（C++11）](Book/part09_concurrency/ch110_lockfree.md)、[ch112 Hazard Pointer 与 RCU（C++11/实践）](Book/part09_concurrency/ch112_hazard_rcu.md)

### ch112 · Hazard Pointer 与 RCU（C++11/实践）

- 文件：`Book/part09_concurrency/ch112_hazard_rcu.md` ｜ Part：`part09_concurrency`
- **出链**（本章指向）：
  [ch110 无锁编程：lock-free / wait-free（C++11）](Book/part09_concurrency/ch110_lockfree.md)、[ch111 ABA 问题与解决（C++11）](Book/part09_concurrency/ch111_aba.md)、[ch113 协程 coroutine：promise / awaiter（C++20）](Book/part09_concurrency/ch113_coroutine.md)
- **入链**（指向本章）：
  [ch110 无锁编程：lock-free / wait-free（C++11）](Book/part09_concurrency/ch110_lockfree.md)、[ch111 ABA 问题与解决（C++11）](Book/part09_concurrency/ch111_aba.md)、[ch113 协程 coroutine：promise / awaiter（C++20）](Book/part09_concurrency/ch113_coroutine.md)

### ch113 · 协程 coroutine：promise / awaiter（C++20）

- 文件：`Book/part09_concurrency/ch113_coroutine.md` ｜ Part：`part09_concurrency`
- **出链**（本章指向）：
  [ch107 std::atomic 原子类型（C++11）](Book/part09_concurrency/ch107_atomic.md)、[ch112 Hazard Pointer 与 RCU（C++11/实践）](Book/part09_concurrency/ch112_hazard_rcu.md)、[ch120 Coroutine 应用模式](Book/part10_modern/ch120_coroutine_app.md)
- **入链**（指向本章）：
  [ch110 无锁编程：lock-free / wait-free（C++11）](Book/part09_concurrency/ch110_lockfree.md)、[ch111 ABA 问题与解决（C++11）](Book/part09_concurrency/ch111_aba.md)、[ch112 Hazard Pointer 与 RCU（C++11/实践）](Book/part09_concurrency/ch112_hazard_rcu.md)、[ch120 Coroutine 应用模式](Book/part10_modern/ch120_coroutine_app.md)、[ch163 从零实现网络编程（C++）](Book/part15_cases/ch163_net.md)

### ch115 · 移动语义与右值引用

- 文件：`Book/part10_modern/ch115_move.md` ｜ Part：`part10_modern`
- **出链**（本章指向）：
  [ch19 变量、存储期、链接与 ODR（工业级深度版）](Book/part03_language/ch19_variables.md)、[ch20 引用（reference）vs 指针（pointer）：语义本质、底层实现与生命周期战争](Book/part03_language/ch20_reference_pointer.md)、[ch27 显式转型四兄弟与隐式转换：const_cast / static_cast / dynamic_cast / reinterpret_cast 深度详解](Book/part03_language/ch27_cast.md)、[ch39 第 39 章 RAII 与 Rule of Zero/Three/Five](Book/part04_memory/ch39_raii_rule.md)、[ch77 vector：扩容、失效、allocator 协作](Book/part07_stl/ch77_vector.md)、[ch116 完美转发与万能引用](Book/part10_modern/ch116_perfect_forwarding.md)、[ch117 RVO / NRVO 与拷贝消除（C++17）](Book/part10_modern/ch117_copy_elision.md)
- **入链**（指向本章）：
  [ch04 C++11：现代 C++ 革命](Book/part01_history/ch04_cpp11.md)、[ch05 C++14：小幅完善](Book/part01_history/ch05_cpp14.md)、[ch37 第 37 章 动态内存分配原语：`operator new` / `operator delete`](Book/part04_memory/ch37_new_delete.md)、[ch77 vector：扩容、失效、allocator 协作](Book/part07_stl/ch77_vector.md)、[ch79 list / forward_list [标准]](Book/part07_stl/ch79_list.md)、[ch84 set / multiset：红黑树有序集合](Book/part07_stl/ch84_set.md)、[ch85 unordered_map / unordered_set：哈希开链集合](Book/part07_stl/ch85_unordered.md)、[ch91 文件系统 filesystem](Book/part07_stl/ch91_filesystem.md)、[ch93 线程与异步：thread / future / async](Book/part07_stl/ch93_thread_async.md)、[ch116 完美转发与万能引用](Book/part10_modern/ch116_perfect_forwarding.md)、[ch117 RVO / NRVO 与拷贝消除（C++17）](Book/part10_modern/ch117_copy_elision.md)、[ch118 Modules 模块（C++20）](Book/part10_modern/ch118_modules.md)、[ch119 Ranges 深入（C++20）](Book/part10_modern/ch119_ranges_deep.md)、[ch120 Coroutine 应用模式](Book/part10_modern/ch120_coroutine_app.md)、[ch121 Contracts 契约（方向，C++26）](Book/part10_modern/ch121_contracts.md)、[ch123 Compile-Time 编程范式总览](Book/part10_modern/ch123_ct_programming.md)、[ch165 C++ 进阶路线图（C++）](Book/part16_reading/ch165_roadmap.md)
- **策展路径**：前置 ch19、ch20、ch27、ch39、ch77、ch116、ch117 ｜ 后续 ch27、ch116、ch117

### ch116 · 完美转发与万能引用

- 文件：`Book/part10_modern/ch116_perfect_forwarding.md` ｜ Part：`part10_modern`
- **出链**（本章指向）：
  [ch20 引用（reference）vs 指针（pointer）：语义本质、底层实现与生命周期战争](Book/part03_language/ch20_reference_pointer.md)、[ch63 可变参数模板与包展开（Variadic Templates & Pack Expansion）](Book/part06_templates/ch63_variadic.md)、[ch65 类型特性 Type Traits —— 编译期类型自省与分发](Book/part06_templates/ch65_type_traits.md)、[ch107 std::atomic 原子类型（C++11）](Book/part09_concurrency/ch107_atomic.md)、[ch115 移动语义与右值引用](Book/part10_modern/ch115_move.md)、[ch117 RVO / NRVO 与拷贝消除（C++17）](Book/part10_modern/ch117_copy_elision.md)、[ch122 PMR 与多态分配器](Book/part10_modern/ch122_pmr.md)
- **入链**（指向本章）：
  [ch26 lambda 表达式全解：闭包类型、捕获、泛型/模板 lambda、constexpr、ABI 与 std::function 类型擦除](Book/part03_language/ch26_lambda.md)、[ch63 可变参数模板与包展开（Variadic Templates & Pack Expansion）](Book/part06_templates/ch63_variadic.md)、[ch89 tuple / pair / any / function / bind](Book/part07_stl/ch89_tuple_any.md)、[ch115 移动语义与右值引用](Book/part10_modern/ch115_move.md)、[ch117 RVO / NRVO 与拷贝消除（C++17）](Book/part10_modern/ch117_copy_elision.md)、[ch118 Modules 模块（C++20）](Book/part10_modern/ch118_modules.md)、[ch123 Compile-Time 编程范式总览](Book/part10_modern/ch123_ct_programming.md)、[ch136 创建型模式（C++）](Book/part12_patterns/ch136_creational.md)、[ch159 从零实现线程池（C++）](Book/part15_cases/ch159_threadpool.md)
- **策展路径**：前置 ch20、ch63、ch115 ｜ 后续 ch107、ch117、ch122

### ch117 · RVO / NRVO 与拷贝消除（C++17）

- 文件：`Book/part10_modern/ch117_copy_elision.md` ｜ Part：`part10_modern`
- **出链**（本章指向）：
  [ch115 移动语义与右值引用](Book/part10_modern/ch115_move.md)、[ch116 完美转发与万能引用](Book/part10_modern/ch116_perfect_forwarding.md)、[ch118 Modules 模块（C++20）](Book/part10_modern/ch118_modules.md)、[ch119 Ranges 深入（C++20）](Book/part10_modern/ch119_ranges_deep.md)、[ch120 Coroutine 应用模式](Book/part10_modern/ch120_coroutine_app.md)
- **入链**（指向本章）：
  [ch115 移动语义与右值引用](Book/part10_modern/ch115_move.md)、[ch116 完美转发与万能引用](Book/part10_modern/ch116_perfect_forwarding.md)、[ch118 Modules 模块（C++20）](Book/part10_modern/ch118_modules.md)、[ch119 Ranges 深入（C++20）](Book/part10_modern/ch119_ranges_deep.md)

### ch118 · Modules 模块（C++20）

- 文件：`Book/part10_modern/ch118_modules.md` ｜ Part：`part10_modern`
- **出链**（本章指向）：
  [ch115 移动语义与右值引用](Book/part10_modern/ch115_move.md)、[ch116 完美转发与万能引用](Book/part10_modern/ch116_perfect_forwarding.md)、[ch117 RVO / NRVO 与拷贝消除（C++17）](Book/part10_modern/ch117_copy_elision.md)、[ch119 Ranges 深入（C++20）](Book/part10_modern/ch119_ranges_deep.md)、[ch120 Coroutine 应用模式](Book/part10_modern/ch120_coroutine_app.md)
- **入链**（指向本章）：
  [ch117 RVO / NRVO 与拷贝消除（C++17）](Book/part10_modern/ch117_copy_elision.md)、[ch119 Ranges 深入（C++20）](Book/part10_modern/ch119_ranges_deep.md)、[ch120 Coroutine 应用模式](Book/part10_modern/ch120_coroutine_app.md)、[ch123 Compile-Time 编程范式总览](Book/part10_modern/ch123_ct_programming.md)

### ch119 · Ranges 深入（C++20）

- 文件：`Book/part10_modern/ch119_ranges_deep.md` ｜ Part：`part10_modern`
- **出链**（本章指向）：
  [ch07 C++20：量级升级](Book/part01_history/ch07_cpp20.md)、[ch67 Concepts 与 requires —— C++20 的编译期约束](Book/part06_templates/ch67_concepts.md)、[ch115 移动语义与右值引用](Book/part10_modern/ch115_move.md)、[ch117 RVO / NRVO 与拷贝消除（C++17）](Book/part10_modern/ch117_copy_elision.md)、[ch118 Modules 模块（C++20）](Book/part10_modern/ch118_modules.md)、[ch120 Coroutine 应用模式](Book/part10_modern/ch120_coroutine_app.md)、[ch121 Contracts 契约（方向，C++26）](Book/part10_modern/ch121_contracts.md)
- **入链**（指向本章）：
  [ch07 C++20：量级升级](Book/part01_history/ch07_cpp20.md)、[ch67 Concepts 与 requires —— C++20 的编译期约束](Book/part06_templates/ch67_concepts.md)、[ch90 ranges 与 views：惰性求值与管道组合](Book/part07_stl/ch90_ranges.md)、[ch100 Ranges 算法与投影（C++20）](Book/part08_algorithms/ch100_ranges_algo.md)、[ch117 RVO / NRVO 与拷贝消除（C++17）](Book/part10_modern/ch117_copy_elision.md)、[ch118 Modules 模块（C++20）](Book/part10_modern/ch118_modules.md)、[ch120 Coroutine 应用模式](Book/part10_modern/ch120_coroutine_app.md)、[ch121 Contracts 契约（方向，C++26）](Book/part10_modern/ch121_contracts.md)、[ch123 Compile-Time 编程范式总览](Book/part10_modern/ch123_ct_programming.md)

### ch120 · Coroutine 应用模式

- 文件：`Book/part10_modern/ch120_coroutine_app.md` ｜ Part：`part10_modern`
- **出链**（本章指向）：
  [ch08 C++23：标准库大修](Book/part01_history/ch08_cpp23.md)、[ch113 协程 coroutine：promise / awaiter（C++20）](Book/part09_concurrency/ch113_coroutine.md)、[ch115 移动语义与右值引用](Book/part10_modern/ch115_move.md)、[ch118 Modules 模块（C++20）](Book/part10_modern/ch118_modules.md)、[ch119 Ranges 深入（C++20）](Book/part10_modern/ch119_ranges_deep.md)、[ch121 Contracts 契约（方向，C++26）](Book/part10_modern/ch121_contracts.md)、[ch122 PMR 与多态分配器](Book/part10_modern/ch122_pmr.md)
- **入链**（指向本章）：
  [ch08 C++23：标准库大修](Book/part01_history/ch08_cpp23.md)、[ch113 协程 coroutine：promise / awaiter（C++20）](Book/part09_concurrency/ch113_coroutine.md)、[ch117 RVO / NRVO 与拷贝消除（C++17）](Book/part10_modern/ch117_copy_elision.md)、[ch118 Modules 模块（C++20）](Book/part10_modern/ch118_modules.md)、[ch119 Ranges 深入（C++20）](Book/part10_modern/ch119_ranges_deep.md)、[ch121 Contracts 契约（方向，C++26）](Book/part10_modern/ch121_contracts.md)
- **策展路径**：前置 ch113、ch120 ｜ 后续 ch120

### ch121 · Contracts 契约（方向，C++26）

- 文件：`Book/part10_modern/ch121_contracts.md` ｜ Part：`part10_modern`
- **出链**（本章指向）：
  [ch09 C++26：已确定特性与方向](Book/part01_history/ch09_cpp26.md)、[ch115 移动语义与右值引用](Book/part10_modern/ch115_move.md)、[ch119 Ranges 深入（C++20）](Book/part10_modern/ch119_ranges_deep.md)、[ch120 Coroutine 应用模式](Book/part10_modern/ch120_coroutine_app.md)、[ch122 PMR 与多态分配器](Book/part10_modern/ch122_pmr.md)、[ch123 Compile-Time 编程范式总览](Book/part10_modern/ch123_ct_programming.md)、[ch146 错误处理（C++）](Book/part13_engineering/ch146_error_handling.md)
- **入链**（指向本章）：
  [ch09 C++26：已确定特性与方向](Book/part01_history/ch09_cpp26.md)、[ch119 Ranges 深入（C++20）](Book/part10_modern/ch119_ranges_deep.md)、[ch120 Coroutine 应用模式](Book/part10_modern/ch120_coroutine_app.md)、[ch122 PMR 与多态分配器](Book/part10_modern/ch122_pmr.md)、[ch146 错误处理（C++）](Book/part13_engineering/ch146_error_handling.md)
- **策展路径**：前置 ch120、ch122 ｜ 后续 ch122

### ch122 · PMR 与多态分配器

- 文件：`Book/part10_modern/ch122_pmr.md` ｜ Part：`part10_modern`
- **出链**（本章指向）：
  [ch37 第 37 章 动态内存分配原语：`operator new` / `operator delete`](Book/part04_memory/ch37_new_delete.md)、[ch38 第 38 章 分配器（Allocator）模型与 PMR](Book/part04_memory/ch38_allocator.md)、[ch43 第 43 章 CPU 缓存体系与内存局部性](Book/part04_memory/ch43_cache_locality.md)、[ch44 第 44 章 内存池（Memory Pool）从零实现](Book/part04_memory/ch44_memory_pool.md)、[ch47 虚函数与虚表（vtable）：动态多态的发动机](Book/part05_oo/ch47_virtual_functions.md)、[ch77 vector：扩容、失效、allocator 协作](Book/part07_stl/ch77_vector.md)、[ch81 std::string 与 SSO 短字符串优化](Book/part07_stl/ch81_string.md)、[ch83 map / multimap（红黑树）](Book/part07_stl/ch83_map.md)、[ch93 线程与异步：thread / future / async](Book/part07_stl/ch93_thread_async.md)、[ch121 Contracts 契约（方向，C++26）](Book/part10_modern/ch121_contracts.md)、[ch125 libc++ 架构（C++）](Book/part11_source/ch125_libcxx.md)、[ch126 MS STL 架构（C++）](Book/part11_source/ch126_msstl.md)、[ch152 性能模型与测量学](Book/part14_perf/ch152_perf_model.md)、[ch154 缓存优化与数据局部性（C++/硬件）](Book/part14_perf/ch154_cache_opt.md)
- **入链**（指向本章）：
  [ch38 第 38 章 分配器（Allocator）模型与 PMR](Book/part04_memory/ch38_allocator.md)、[ch44 第 44 章 内存池（Memory Pool）从零实现](Book/part04_memory/ch44_memory_pool.md)、[ch81 std::string 与 SSO 短字符串优化](Book/part07_stl/ch81_string.md)、[ch91 文件系统 filesystem](Book/part07_stl/ch91_filesystem.md)、[ch116 完美转发与万能引用](Book/part10_modern/ch116_perfect_forwarding.md)、[ch120 Coroutine 应用模式](Book/part10_modern/ch120_coroutine_app.md)、[ch121 Contracts 契约（方向，C++26）](Book/part10_modern/ch121_contracts.md)、[ch123 Compile-Time 编程范式总览](Book/part10_modern/ch123_ct_programming.md)、[ch125 libc++ 架构（C++）](Book/part11_source/ch125_libcxx.md)、[ch160 从零实现内存池（C++）](Book/part15_cases/ch160_mempool.md)
- **策展路径**：前置 ch37、ch38、ch47 ｜ 后续 ch38、ch44、ch121、ch154

### ch123 · Compile-Time 编程范式总览

- 文件：`Book/part10_modern/ch123_ct_programming.md` ｜ Part：`part10_modern`
- **出链**（本章指向）：
  [ch51 CRTP 与静态多态（Curiously Recurring Template Pattern）](Book/part05_oo/ch51_crtp.md)、[ch60 模板基础与实例化（Template Basics & Instantiation）](Book/part06_templates/ch60_template_basics.md)、[ch65 类型特性 Type Traits —— 编译期类型自省与分发](Book/part06_templates/ch65_type_traits.md)、[ch67 Concepts 与 requires —— C++20 的编译期约束](Book/part06_templates/ch67_concepts.md)、[ch69 编译期计算：constexpr / consteval / constinit](Book/part06_templates/ch69_constexpr.md)、[ch115 移动语义与右值引用](Book/part10_modern/ch115_move.md)、[ch116 完美转发与万能引用](Book/part10_modern/ch116_perfect_forwarding.md)、[ch118 Modules 模块（C++20）](Book/part10_modern/ch118_modules.md)、[ch119 Ranges 深入（C++20）](Book/part10_modern/ch119_ranges_deep.md)、[ch122 PMR 与多态分配器](Book/part10_modern/ch122_pmr.md)、[ch140 Policy-Based Design（C++）](Book/part12_patterns/ch140_policy_pattern.md)、[ch152 性能模型与测量学](Book/part14_perf/ch152_perf_model.md)
- **入链**（指向本章）：
  [ch09 C++26：已确定特性与方向](Book/part01_history/ch09_cpp26.md)、[ch69 编译期计算：constexpr / consteval / constinit](Book/part06_templates/ch69_constexpr.md)、[ch121 Contracts 契约（方向，C++26）](Book/part10_modern/ch121_contracts.md)、[ch125 libc++ 架构（C++）](Book/part11_source/ch125_libcxx.md)

### ch124 · libstdc++ 架构与阅读入口（C++）

- 文件：`Book/part11_source/ch124_libstdcxx.md` ｜ Part：`part11_source`
- **出链**（本章指向）：
  [ch39 第 39 章 RAII 与 Rule of Zero/Three/Five](Book/part04_memory/ch39_raii_rule.md)、[ch77 vector：扩容、失效、allocator 协作](Book/part07_stl/ch77_vector.md)、[ch125 libc++ 架构（C++）](Book/part11_source/ch125_libcxx.md)
- **入链**（指向本章）：
  [ch85 unordered_map / unordered_set：哈希开链集合](Book/part07_stl/ch85_unordered.md)、[ch86 容器适配器：stack / queue / priority_queue](Book/part07_stl/ch86_adapters.md)、[ch87 bitset：编译期定长位集](Book/part07_stl/ch87_bitset.md)、[ch125 libc++ 架构（C++）](Book/part11_source/ch125_libcxx.md)、[ch126 MS STL 架构（C++）](Book/part11_source/ch126_msstl.md)、[ch128 Boost 核心库（C++）](Book/part11_source/ch128_boost.md)、[ch131 fmt / spdlog 格式化与日志（C++）](Book/part11_source/ch131_fmt_spdlog.md)

### ch125 · libc++ 架构（C++）

- 文件：`Book/part11_source/ch125_libcxx.md` ｜ Part：`part11_source`
- **出链**（本章指向）：
  [ch122 PMR 与多态分配器](Book/part10_modern/ch122_pmr.md)、[ch123 Compile-Time 编程范式总览](Book/part10_modern/ch123_ct_programming.md)、[ch124 libstdc++ 架构与阅读入口（C++）](Book/part11_source/ch124_libstdcxx.md)、[ch126 MS STL 架构（C++）](Book/part11_source/ch126_msstl.md)、[ch127 LLVM / Clang 架构（C++）](Book/part11_source/ch127_llvm.md)、[ch128 Boost 核心库（C++）](Book/part11_source/ch128_boost.md)
- **入链**（指向本章）：
  [ch122 PMR 与多态分配器](Book/part10_modern/ch122_pmr.md)、[ch124 libstdc++ 架构与阅读入口（C++）](Book/part11_source/ch124_libstdcxx.md)、[ch126 MS STL 架构（C++）](Book/part11_source/ch126_msstl.md)、[ch127 LLVM / Clang 架构（C++）](Book/part11_source/ch127_llvm.md)

### ch126 · MS STL 架构（C++）

- 文件：`Book/part11_source/ch126_msstl.md` ｜ Part：`part11_source`
- **出链**（本章指向）：
  [ch124 libstdc++ 架构与阅读入口（C++）](Book/part11_source/ch124_libstdcxx.md)、[ch125 libc++ 架构（C++）](Book/part11_source/ch125_libcxx.md)、[ch127 LLVM / Clang 架构（C++）](Book/part11_source/ch127_llvm.md)
- **入链**（指向本章）：
  [ch122 PMR 与多态分配器](Book/part10_modern/ch122_pmr.md)、[ch125 libc++ 架构（C++）](Book/part11_source/ch125_libcxx.md)、[ch127 LLVM / Clang 架构（C++）](Book/part11_source/ch127_llvm.md)

### ch127 · LLVM / Clang 架构（C++）

- 文件：`Book/part11_source/ch127_llvm.md` ｜ Part：`part11_source`
- **出链**（本章指向）：
  [ch11 编译器全景：GCC / Clang / MSVC 架构与 ABI（C++）](Book/part02_toolchain/ch11_compilers.md)、[ch125 libc++ 架构（C++）](Book/part11_source/ch125_libcxx.md)、[ch126 MS STL 架构（C++）](Book/part11_source/ch126_msstl.md)、[ch128 Boost 核心库（C++）](Book/part11_source/ch128_boost.md)
- **入链**（指向本章）：
  [ch125 libc++ 架构（C++）](Book/part11_source/ch125_libcxx.md)、[ch126 MS STL 架构（C++）](Book/part11_source/ch126_msstl.md)、[ch128 Boost 核心库（C++）](Book/part11_source/ch128_boost.md)

### ch128 · Boost 核心库（C++）

- 文件：`Book/part11_source/ch128_boost.md` ｜ Part：`part11_source`
- **出链**（本章指向）：
  [ch65 类型特性 Type Traits —— 编译期类型自省与分发](Book/part06_templates/ch65_type_traits.md)、[ch124 libstdc++ 架构与阅读入口（C++）](Book/part11_source/ch124_libstdcxx.md)、[ch127 LLVM / Clang 架构（C++）](Book/part11_source/ch127_llvm.md)、[ch129 Qt 对象模型与信号槽（C++）](Book/part11_source/ch129_qt.md)
- **入链**（指向本章）：
  [ch13 包管理：vcpkg / Conan（C++）](Book/part02_toolchain/ch13_packaging.md)、[ch125 libc++ 架构（C++）](Book/part11_source/ch125_libcxx.md)、[ch127 LLVM / Clang 架构（C++）](Book/part11_source/ch127_llvm.md)、[ch129 Qt 对象模型与信号槽（C++）](Book/part11_source/ch129_qt.md)

### ch129 · Qt 对象模型与信号槽（C++）

- 文件：`Book/part11_source/ch129_qt.md` ｜ Part：`part11_source`
- **出链**（本章指向）：
  [ch45 第 45 章 C++ 面向对象总览与对象模型基础](Book/part05_oo/ch45_oop_object_model.md)、[ch128 Boost 核心库（C++）](Book/part11_source/ch128_boost.md)、[ch130 Chromium / Abseil 基础设施（C++）](Book/part11_source/ch130_chromium_abseil.md)、[ch135 设计模式总论（C++）](Book/part12_patterns/ch135_patterns_intro.md)
- **入链**（指向本章）：
  [ch128 Boost 核心库（C++）](Book/part11_source/ch128_boost.md)、[ch130 Chromium / Abseil 基础设施（C++）](Book/part11_source/ch130_chromium_abseil.md)、[ch131 fmt / spdlog 格式化与日志（C++）](Book/part11_source/ch131_fmt_spdlog.md)

### ch130 · Chromium / Abseil 基础设施（C++）

- 文件：`Book/part11_source/ch130_chromium_abseil.md` ｜ Part：`part11_source`
- **出链**（本章指向）：
  [ch77 vector：扩容、失效、allocator 协作](Book/part07_stl/ch77_vector.md)、[ch129 Qt 对象模型与信号槽（C++）](Book/part11_source/ch129_qt.md)、[ch131 fmt / spdlog 格式化与日志（C++）](Book/part11_source/ch131_fmt_spdlog.md)
- **入链**（指向本章）：
  [ch129 Qt 对象模型与信号槽（C++）](Book/part11_source/ch129_qt.md)、[ch131 fmt / spdlog 格式化与日志（C++）](Book/part11_source/ch131_fmt_spdlog.md)

### ch131 · fmt / spdlog 格式化与日志（C++）

- 文件：`Book/part11_source/ch131_fmt_spdlog.md` ｜ Part：`part11_source`
- **出链**（本章指向）：
  [ch79 list / forward_list [标准]](Book/part07_stl/ch79_list.md)、[ch92 时间库 chrono](Book/part07_stl/ch92_chrono.md)、[ch124 libstdc++ 架构与阅读入口（C++）](Book/part11_source/ch124_libstdcxx.md)、[ch129 Qt 对象模型与信号槽（C++）](Book/part11_source/ch129_qt.md)、[ch130 Chromium / Abseil 基础设施（C++）](Book/part11_source/ch130_chromium_abseil.md)、[ch132 LevelDB / RocksDB 存储引擎（C++）](Book/part11_source/ch132_leveldb_rocksdb.md)、[ch133 ClickHouse / Redis 实现精读（C++）](Book/part11_source/ch133_clickhouse_redis.md)
- **入链**（指向本章）：
  [ch79 list / forward_list [标准]](Book/part07_stl/ch79_list.md)、[ch92 时间库 chrono](Book/part07_stl/ch92_chrono.md)、[ch130 Chromium / Abseil 基础设施（C++）](Book/part11_source/ch130_chromium_abseil.md)、[ch132 LevelDB / RocksDB 存储引擎（C++）](Book/part11_source/ch132_leveldb_rocksdb.md)、[ch161 从零实现日志库（C++）](Book/part15_cases/ch161_logger.md)

### ch132 · LevelDB / RocksDB 存储引擎（C++）

- 文件：`Book/part11_source/ch132_leveldb_rocksdb.md` ｜ Part：`part11_source`
- **出链**（本章指向）：
  [ch83 map / multimap（红黑树）](Book/part07_stl/ch83_map.md)、[ch96 排序：sort / stable_sort / partial_sort（C++）](Book/part08_algorithms/ch96_sorting.md)、[ch131 fmt / spdlog 格式化与日志（C++）](Book/part11_source/ch131_fmt_spdlog.md)、[ch133 ClickHouse / Redis 实现精读（C++）](Book/part11_source/ch133_clickhouse_redis.md)
- **入链**（指向本章）：
  [ch131 fmt / spdlog 格式化与日志（C++）](Book/part11_source/ch131_fmt_spdlog.md)、[ch133 ClickHouse / Redis 实现精读（C++）](Book/part11_source/ch133_clickhouse_redis.md)

### ch133 · ClickHouse / Redis 实现精读（C++）

- 文件：`Book/part11_source/ch133_clickhouse_redis.md` ｜ Part：`part11_source`
- **出链**（本章指向）：
  [ch77 vector：扩容、失效、allocator 协作](Book/part07_stl/ch77_vector.md)、[ch132 LevelDB / RocksDB 存储引擎（C++）](Book/part11_source/ch132_leveldb_rocksdb.md)、[ch134 Unreal Engine C++ 架构（C++）](Book/part11_source/ch134_unreal.md)
- **入链**（指向本章）：
  [ch131 fmt / spdlog 格式化与日志（C++）](Book/part11_source/ch131_fmt_spdlog.md)、[ch132 LevelDB / RocksDB 存储引擎（C++）](Book/part11_source/ch132_leveldb_rocksdb.md)、[ch134 Unreal Engine C++ 架构（C++）](Book/part11_source/ch134_unreal.md)

### ch134 · Unreal Engine C++ 架构（C++）

- 文件：`Book/part11_source/ch134_unreal.md` ｜ Part：`part11_source`
- **出链**（本章指向）：
  [ch45 第 45 章 C++ 面向对象总览与对象模型基础](Book/part05_oo/ch45_oop_object_model.md)、[ch133 ClickHouse / Redis 实现精读（C++）](Book/part11_source/ch133_clickhouse_redis.md)、[ch142 实体组件系统 ECS（C++）](Book/part12_patterns/ch142_ecs.md)
- **入链**（指向本章）：
  [ch133 ClickHouse / Redis 实现精读（C++）](Book/part11_source/ch133_clickhouse_redis.md)

### ch135 · 设计模式总论（C++）

- 文件：`Book/part12_patterns/ch135_patterns_intro.md` ｜ Part：`part12_patterns`
- **出链**（本章指向）：
  [ch136 创建型模式（C++）](Book/part12_patterns/ch136_creational.md)、[ch137 结构型模式（C++）](Book/part12_patterns/ch137_structural.md)、[ch138 行为型模式（C++）](Book/part12_patterns/ch138_behavioral.md)
- **入链**（指向本章）：
  [ch129 Qt 对象模型与信号槽（C++）](Book/part11_source/ch129_qt.md)、[ch136 创建型模式（C++）](Book/part12_patterns/ch136_creational.md)、[ch137 结构型模式（C++）](Book/part12_patterns/ch137_structural.md)、[ch140 Policy-Based Design（C++）](Book/part12_patterns/ch140_policy_pattern.md)、[ch141 依赖注入（C++）](Book/part12_patterns/ch141_di.md)、[ch143 面向数据设计 DOD（C++）](Book/part12_patterns/ch143_dod.md)、[ch145 命名与 API 设计（C++）](Book/part13_engineering/ch145_naming_api.md)

### ch136 · 创建型模式（C++）

- 文件：`Book/part12_patterns/ch136_creational.md` ｜ Part：`part12_patterns`
- **出链**（本章指向）：
  [ch116 完美转发与万能引用](Book/part10_modern/ch116_perfect_forwarding.md)、[ch135 设计模式总论（C++）](Book/part12_patterns/ch135_patterns_intro.md)、[ch137 结构型模式（C++）](Book/part12_patterns/ch137_structural.md)
- **入链**（指向本章）：
  [ch135 设计模式总论（C++）](Book/part12_patterns/ch135_patterns_intro.md)、[ch137 结构型模式（C++）](Book/part12_patterns/ch137_structural.md)

### ch137 · 结构型模式（C++）

- 文件：`Book/part12_patterns/ch137_structural.md` ｜ Part：`part12_patterns`
- **出链**（本章指向）：
  [ch45 第 45 章 C++ 面向对象总览与对象模型基础](Book/part05_oo/ch45_oop_object_model.md)、[ch135 设计模式总论（C++）](Book/part12_patterns/ch135_patterns_intro.md)、[ch136 创建型模式（C++）](Book/part12_patterns/ch136_creational.md)、[ch138 行为型模式（C++）](Book/part12_patterns/ch138_behavioral.md)
- **入链**（指向本章）：
  [ch135 设计模式总论（C++）](Book/part12_patterns/ch135_patterns_intro.md)、[ch136 创建型模式（C++）](Book/part12_patterns/ch136_creational.md)、[ch138 行为型模式（C++）](Book/part12_patterns/ch138_behavioral.md)

### ch138 · 行为型模式（C++）

- 文件：`Book/part12_patterns/ch138_behavioral.md` ｜ Part：`part12_patterns`
- **出链**（本章指向）：
  [ch137 结构型模式（C++）](Book/part12_patterns/ch137_structural.md)、[ch139 CRTP 与静态多态（C++）](Book/part12_patterns/ch139_crtp_pattern.md)、[ch141 依赖注入（C++）](Book/part12_patterns/ch141_di.md)
- **入链**（指向本章）：
  [ch135 设计模式总论（C++）](Book/part12_patterns/ch135_patterns_intro.md)、[ch137 结构型模式（C++）](Book/part12_patterns/ch137_structural.md)、[ch139 CRTP 与静态多态（C++）](Book/part12_patterns/ch139_crtp_pattern.md)

### ch139 · CRTP 与静态多态（C++）

- 文件：`Book/part12_patterns/ch139_crtp_pattern.md` ｜ Part：`part12_patterns`
- **出链**（本章指向）：
  [ch51 CRTP 与静态多态（Curiously Recurring Template Pattern）](Book/part05_oo/ch51_crtp.md)、[ch68 模板元编程 TMP 基础（递归 / 分支 / 循环）](Book/part06_templates/ch68_tmp.md)、[ch138 行为型模式（C++）](Book/part12_patterns/ch138_behavioral.md)、[ch140 Policy-Based Design（C++）](Book/part12_patterns/ch140_policy_pattern.md)
- **入链**（指向本章）：
  [ch138 行为型模式（C++）](Book/part12_patterns/ch138_behavioral.md)、[ch140 Policy-Based Design（C++）](Book/part12_patterns/ch140_policy_pattern.md)

### ch140 · Policy-Based Design（C++）

- 文件：`Book/part12_patterns/ch140_policy_pattern.md` ｜ Part：`part12_patterns`
- **出链**（本章指向）：
  [ch71 策略设计 Policy-Based Design](Book/part06_templates/ch71_policy.md)、[ch135 设计模式总论（C++）](Book/part12_patterns/ch135_patterns_intro.md)、[ch139 CRTP 与静态多态（C++）](Book/part12_patterns/ch139_crtp_pattern.md)、[ch141 依赖注入（C++）](Book/part12_patterns/ch141_di.md)
- **入链**（指向本章）：
  [ch71 策略设计 Policy-Based Design](Book/part06_templates/ch71_policy.md)、[ch123 Compile-Time 编程范式总览](Book/part10_modern/ch123_ct_programming.md)、[ch139 CRTP 与静态多态（C++）](Book/part12_patterns/ch139_crtp_pattern.md)、[ch141 依赖注入（C++）](Book/part12_patterns/ch141_di.md)

### ch141 · 依赖注入（C++）

- 文件：`Book/part12_patterns/ch141_di.md` ｜ Part：`part12_patterns`
- **出链**（本章指向）：
  [ch45 第 45 章 C++ 面向对象总览与对象模型基础](Book/part05_oo/ch45_oop_object_model.md)、[ch135 设计模式总论（C++）](Book/part12_patterns/ch135_patterns_intro.md)、[ch140 Policy-Based Design（C++）](Book/part12_patterns/ch140_policy_pattern.md)、[ch142 实体组件系统 ECS（C++）](Book/part12_patterns/ch142_ecs.md)
- **入链**（指向本章）：
  [ch138 行为型模式（C++）](Book/part12_patterns/ch138_behavioral.md)、[ch140 Policy-Based Design（C++）](Book/part12_patterns/ch140_policy_pattern.md)、[ch142 实体组件系统 ECS（C++）](Book/part12_patterns/ch142_ecs.md)、[ch143 面向数据设计 DOD（C++）](Book/part12_patterns/ch143_dod.md)、[ch164 从零实现迷你框架（C++）](Book/part15_cases/ch164_framework.md)

### ch142 · 实体组件系统 ECS（C++）

- 文件：`Book/part12_patterns/ch142_ecs.md` ｜ Part：`part12_patterns`
- **出链**（本章指向）：
  [ch45 第 45 章 C++ 面向对象总览与对象模型基础](Book/part05_oo/ch45_oop_object_model.md)、[ch141 依赖注入（C++）](Book/part12_patterns/ch141_di.md)、[ch143 面向数据设计 DOD（C++）](Book/part12_patterns/ch143_dod.md)
- **入链**（指向本章）：
  [ch79 list / forward_list [标准]](Book/part07_stl/ch79_list.md)、[ch134 Unreal Engine C++ 架构（C++）](Book/part11_source/ch134_unreal.md)、[ch141 依赖注入（C++）](Book/part12_patterns/ch141_di.md)、[ch143 面向数据设计 DOD（C++）](Book/part12_patterns/ch143_dod.md)、[ch144 代码风格与规范（C++）](Book/part13_engineering/ch144_style.md)

### ch143 · 面向数据设计 DOD（C++）

- 文件：`Book/part12_patterns/ch143_dod.md` ｜ Part：`part12_patterns`
- **出链**（本章指向）：
  [ch135 设计模式总论（C++）](Book/part12_patterns/ch135_patterns_intro.md)、[ch141 依赖注入（C++）](Book/part12_patterns/ch141_di.md)、[ch142 实体组件系统 ECS（C++）](Book/part12_patterns/ch142_ecs.md)、[ch144 代码风格与规范（C++）](Book/part13_engineering/ch144_style.md)、[ch145 命名与 API 设计（C++）](Book/part13_engineering/ch145_naming_api.md)、[ch154 缓存优化与数据局部性（C++/硬件）](Book/part14_perf/ch154_cache_opt.md)
- **入链**（指向本章）：
  [ch83 map / multimap（红黑树）](Book/part07_stl/ch83_map.md)、[ch142 实体组件系统 ECS（C++）](Book/part12_patterns/ch142_ecs.md)、[ch144 代码风格与规范（C++）](Book/part13_engineering/ch144_style.md)

### ch144 · 代码风格与规范（C++）

- 文件：`Book/part13_engineering/ch144_style.md` ｜ Part：`part13_engineering`
- **出链**（本章指向）：
  [ch142 实体组件系统 ECS（C++）](Book/part12_patterns/ch142_ecs.md)、[ch143 面向数据设计 DOD（C++）](Book/part12_patterns/ch143_dod.md)、[ch145 命名与 API 设计（C++）](Book/part13_engineering/ch145_naming_api.md)、[ch146 错误处理（C++）](Book/part13_engineering/ch146_error_handling.md)、[ch147 代码审查（C++）](Book/part13_engineering/ch147_code_review.md)、[ch148 Git 工作流（C++）](Book/part13_engineering/ch148_gitflow.md)、[ch161 从零实现日志库（C++）](Book/part15_cases/ch161_logger.md)
- **入链**（指向本章）：
  [ch143 面向数据设计 DOD（C++）](Book/part12_patterns/ch143_dod.md)、[ch145 命名与 API 设计（C++）](Book/part13_engineering/ch145_naming_api.md)、[ch147 代码审查（C++）](Book/part13_engineering/ch147_code_review.md)、[ch149 CI/CD 流水线（C++）](Book/part13_engineering/ch149_ci_cd.md)、[ch161 从零实现日志库（C++）](Book/part15_cases/ch161_logger.md)

### ch145 · 命名与 API 设计（C++）

- 文件：`Book/part13_engineering/ch145_naming_api.md` ｜ Part：`part13_engineering`
- **出链**（本章指向）：
  [ch135 设计模式总论（C++）](Book/part12_patterns/ch135_patterns_intro.md)、[ch144 代码风格与规范（C++）](Book/part13_engineering/ch144_style.md)、[ch146 错误处理（C++）](Book/part13_engineering/ch146_error_handling.md)
- **入链**（指向本章）：
  [ch143 面向数据设计 DOD（C++）](Book/part12_patterns/ch143_dod.md)、[ch144 代码风格与规范（C++）](Book/part13_engineering/ch144_style.md)、[ch146 错误处理（C++）](Book/part13_engineering/ch146_error_handling.md)

### ch146 · 错误处理（C++）

- 文件：`Book/part13_engineering/ch146_error_handling.md` ｜ Part：`part13_engineering`
- **出链**（本章指向）：
  [ch88 optional / expected / variant：可空与可辨别联合](Book/part07_stl/ch88_optional_variant.md)、[ch121 Contracts 契约（方向，C++26）](Book/part10_modern/ch121_contracts.md)、[ch145 命名与 API 设计（C++）](Book/part13_engineering/ch145_naming_api.md)、[ch147 代码审查（C++）](Book/part13_engineering/ch147_code_review.md)
- **入链**（指向本章）：
  [ch91 文件系统 filesystem](Book/part07_stl/ch91_filesystem.md)、[ch121 Contracts 契约（方向，C++26）](Book/part10_modern/ch121_contracts.md)、[ch144 代码风格与规范（C++）](Book/part13_engineering/ch144_style.md)、[ch145 命名与 API 设计（C++）](Book/part13_engineering/ch145_naming_api.md)、[ch147 代码审查（C++）](Book/part13_engineering/ch147_code_review.md)

### ch147 · 代码审查（C++）

- 文件：`Book/part13_engineering/ch147_code_review.md` ｜ Part：`part13_engineering`
- **出链**（本章指向）：
  [ch144 代码风格与规范（C++）](Book/part13_engineering/ch144_style.md)、[ch146 错误处理（C++）](Book/part13_engineering/ch146_error_handling.md)、[ch148 Git 工作流（C++）](Book/part13_engineering/ch148_gitflow.md)、[ch150 测试策略（C++）](Book/part13_engineering/ch150_testing.md)
- **入链**（指向本章）：
  [ch144 代码风格与规范（C++）](Book/part13_engineering/ch144_style.md)、[ch146 错误处理（C++）](Book/part13_engineering/ch146_error_handling.md)、[ch148 Git 工作流（C++）](Book/part13_engineering/ch148_gitflow.md)、[ch149 CI/CD 流水线（C++）](Book/part13_engineering/ch149_ci_cd.md)

### ch148 · Git 工作流（C++）

- 文件：`Book/part13_engineering/ch148_gitflow.md` ｜ Part：`part13_engineering`
- **出链**（本章指向）：
  [ch18 构建配置：Debug / Release / LTO / PGO（C++）](Book/part02_toolchain/ch18_buildconfig.md)、[ch147 代码审查（C++）](Book/part13_engineering/ch147_code_review.md)、[ch149 CI/CD 流水线（C++）](Book/part13_engineering/ch149_ci_cd.md)
- **入链**（指向本章）：
  [ch144 代码风格与规范（C++）](Book/part13_engineering/ch144_style.md)、[ch147 代码审查（C++）](Book/part13_engineering/ch147_code_review.md)、[ch149 CI/CD 流水线（C++）](Book/part13_engineering/ch149_ci_cd.md)

### ch149 · CI/CD 流水线（C++）

- 文件：`Book/part13_engineering/ch149_ci_cd.md` ｜ Part：`part13_engineering`
- **出链**（本章指向）：
  [ch18 构建配置：Debug / Release / LTO / PGO（C++）](Book/part02_toolchain/ch18_buildconfig.md)、[ch144 代码风格与规范（C++）](Book/part13_engineering/ch144_style.md)、[ch147 代码审查（C++）](Book/part13_engineering/ch147_code_review.md)、[ch148 Git 工作流（C++）](Book/part13_engineering/ch148_gitflow.md)、[ch150 测试策略（C++）](Book/part13_engineering/ch150_testing.md)、[ch151 基准测试与性能度量（C++）](Book/part13_engineering/ch151_benchmark.md)
- **入链**（指向本章）：
  [ch18 构建配置：Debug / Release / LTO / PGO（C++）](Book/part02_toolchain/ch18_buildconfig.md)、[ch148 Git 工作流（C++）](Book/part13_engineering/ch148_gitflow.md)、[ch150 测试策略（C++）](Book/part13_engineering/ch150_testing.md)

### ch150 · 测试策略（C++）

- 文件：`Book/part13_engineering/ch150_testing.md` ｜ Part：`part13_engineering`
- **出链**（本章指向）：
  [ch29 友元 friend 与访问控制](Book/part03_language/ch29_friend.md)、[ch149 CI/CD 流水线（C++）](Book/part13_engineering/ch149_ci_cd.md)、[ch151 基准测试与性能度量（C++）](Book/part13_engineering/ch151_benchmark.md)
- **入链**（指向本章）：
  [ch29 友元 friend 与访问控制](Book/part03_language/ch29_friend.md)、[ch147 代码审查（C++）](Book/part13_engineering/ch147_code_review.md)、[ch149 CI/CD 流水线（C++）](Book/part13_engineering/ch149_ci_cd.md)、[ch151 基准测试与性能度量（C++）](Book/part13_engineering/ch151_benchmark.md)

### ch151 · 基准测试与性能度量（C++）

- 文件：`Book/part13_engineering/ch151_benchmark.md` ｜ Part：`part13_engineering`
- **出链**（本章指向）：
  [ch150 测试策略（C++）](Book/part13_engineering/ch150_testing.md)、[ch152 性能模型与测量学](Book/part14_perf/ch152_perf_model.md)、[ch157 Compiler Explorer 实战](Book/part14_perf/ch157_compiler_explorer.md)
- **入链**（指向本章）：
  [ch15 性能分析：perf / VTune / 火焰图 / Compiler Explorer（C++）](Book/part02_toolchain/ch15_profiling.md)、[ch92 时间库 chrono](Book/part07_stl/ch92_chrono.md)、[ch99 数值算法与并行执行策略（C++）](Book/part08_algorithms/ch99_numeric.md)、[ch149 CI/CD 流水线（C++）](Book/part13_engineering/ch149_ci_cd.md)、[ch150 测试策略（C++）](Book/part13_engineering/ch150_testing.md)、[ch152 性能模型与测量学](Book/part14_perf/ch152_perf_model.md)

### ch152 · 性能模型与测量学

- 文件：`Book/part14_perf/ch152_perf_model.md` ｜ Part：`part14_perf`
- **出链**（本章指向）：
  [ch151 基准测试与性能度量（C++）](Book/part13_engineering/ch151_benchmark.md)、[ch153 CPU 微架构：流水线 / 分支预测 / 乱序执行](Book/part14_perf/ch153_cpu_micro.md)、[ch154 缓存优化与数据局部性（C++/硬件）](Book/part14_perf/ch154_cache_opt.md)、[ch155 SIMD / AVX 向量化（C++/硬件）](Book/part14_perf/ch155_simd.md)、[ch156 编译器优化：O2/O3/Ofast/LTO/PGO（GCC）](Book/part14_perf/ch156_compiler_opt.md)、[ch157 Compiler Explorer 实战](Book/part14_perf/ch157_compiler_explorer.md)、[ch158 性能反模式与陷阱](Book/part14_perf/ch158_perf_antipatterns.md)
- **入链**（指向本章）：
  [ch86 容器适配器：stack / queue / priority_queue](Book/part07_stl/ch86_adapters.md)、[ch87 bitset：编译期定长位集](Book/part07_stl/ch87_bitset.md)、[ch92 时间库 chrono](Book/part07_stl/ch92_chrono.md)、[ch122 PMR 与多态分配器](Book/part10_modern/ch122_pmr.md)、[ch123 Compile-Time 编程范式总览](Book/part10_modern/ch123_ct_programming.md)、[ch151 基准测试与性能度量（C++）](Book/part13_engineering/ch151_benchmark.md)、[ch153 CPU 微架构：流水线 / 分支预测 / 乱序执行](Book/part14_perf/ch153_cpu_micro.md)、[ch155 SIMD / AVX 向量化（C++/硬件）](Book/part14_perf/ch155_simd.md)、[ch156 编译器优化：O2/O3/Ofast/LTO/PGO（GCC）](Book/part14_perf/ch156_compiler_opt.md)、[ch157 Compiler Explorer 实战](Book/part14_perf/ch157_compiler_explorer.md)、[ch158 性能反模式与陷阱](Book/part14_perf/ch158_perf_antipatterns.md)

### ch153 · CPU 微架构：流水线 / 分支预测 / 乱序执行

- 文件：`Book/part14_perf/ch153_cpu_micro.md` ｜ Part：`part14_perf`
- **出链**（本章指向）：
  [ch77 vector：扩容、失效、allocator 协作](Book/part07_stl/ch77_vector.md)、[ch95 STL 算法分类与复杂度（C++）](Book/part08_algorithms/ch95_algo_overview.md)、[ch96 排序：sort / stable_sort / partial_sort（C++）](Book/part08_algorithms/ch96_sorting.md)、[ch107 std::atomic 原子类型（C++11）](Book/part09_concurrency/ch107_atomic.md)、[ch152 性能模型与测量学](Book/part14_perf/ch152_perf_model.md)、[ch154 缓存优化与数据局部性（C++/硬件）](Book/part14_perf/ch154_cache_opt.md)、[ch155 SIMD / AVX 向量化（C++/硬件）](Book/part14_perf/ch155_simd.md)、[ch156 编译器优化：O2/O3/Ofast/LTO/PGO（GCC）](Book/part14_perf/ch156_compiler_opt.md)、[ch157 Compiler Explorer 实战](Book/part14_perf/ch157_compiler_explorer.md)、[ch158 性能反模式与陷阱](Book/part14_perf/ch158_perf_antipatterns.md)
- **入链**（指向本章）：
  [ch152 性能模型与测量学](Book/part14_perf/ch152_perf_model.md)、[ch154 缓存优化与数据局部性（C++/硬件）](Book/part14_perf/ch154_cache_opt.md)、[ch155 SIMD / AVX 向量化（C++/硬件）](Book/part14_perf/ch155_simd.md)、[ch158 性能反模式与陷阱](Book/part14_perf/ch158_perf_antipatterns.md)

### ch154 · 缓存优化与数据局部性（C++/硬件）

- 文件：`Book/part14_perf/ch154_cache_opt.md` ｜ Part：`part14_perf`
- **出链**（本章指向）：
  [ch153 CPU 微架构：流水线 / 分支预测 / 乱序执行](Book/part14_perf/ch153_cpu_micro.md)、[ch155 SIMD / AVX 向量化（C++/硬件）](Book/part14_perf/ch155_simd.md)、[ch156 编译器优化：O2/O3/Ofast/LTO/PGO（GCC）](Book/part14_perf/ch156_compiler_opt.md)
- **入链**（指向本章）：
  [ch43 第 43 章 CPU 缓存体系与内存局部性](Book/part04_memory/ch43_cache_locality.md)、[ch77 vector：扩容、失效、allocator 协作](Book/part07_stl/ch77_vector.md)、[ch84 set / multiset：红黑树有序集合](Book/part07_stl/ch84_set.md)、[ch85 unordered_map / unordered_set：哈希开链集合](Book/part07_stl/ch85_unordered.md)、[ch122 PMR 与多态分配器](Book/part10_modern/ch122_pmr.md)、[ch143 面向数据设计 DOD（C++）](Book/part12_patterns/ch143_dod.md)、[ch152 性能模型与测量学](Book/part14_perf/ch152_perf_model.md)、[ch153 CPU 微架构：流水线 / 分支预测 / 乱序执行](Book/part14_perf/ch153_cpu_micro.md)、[ch155 SIMD / AVX 向量化（C++/硬件）](Book/part14_perf/ch155_simd.md)、[ch156 编译器优化：O2/O3/Ofast/LTO/PGO（GCC）](Book/part14_perf/ch156_compiler_opt.md)、[ch158 性能反模式与陷阱](Book/part14_perf/ch158_perf_antipatterns.md)

### ch155 · SIMD / AVX 向量化（C++/硬件）

- 文件：`Book/part14_perf/ch155_simd.md` ｜ Part：`part14_perf`
- **出链**（本章指向）：
  [ch76 STL 架构与迭代器概念](Book/part07_stl/ch76_stl_arch.md)、[ch87 bitset：编译期定长位集](Book/part07_stl/ch87_bitset.md)、[ch152 性能模型与测量学](Book/part14_perf/ch152_perf_model.md)、[ch153 CPU 微架构：流水线 / 分支预测 / 乱序执行](Book/part14_perf/ch153_cpu_micro.md)、[ch154 缓存优化与数据局部性（C++/硬件）](Book/part14_perf/ch154_cache_opt.md)、[ch156 编译器优化：O2/O3/Ofast/LTO/PGO（GCC）](Book/part14_perf/ch156_compiler_opt.md)、[ch157 Compiler Explorer 实战](Book/part14_perf/ch157_compiler_explorer.md)
- **入链**（指向本章）：
  [ch76 STL 架构与迭代器概念](Book/part07_stl/ch76_stl_arch.md)、[ch87 bitset：编译期定长位集](Book/part07_stl/ch87_bitset.md)、[ch152 性能模型与测量学](Book/part14_perf/ch152_perf_model.md)、[ch153 CPU 微架构：流水线 / 分支预测 / 乱序执行](Book/part14_perf/ch153_cpu_micro.md)、[ch154 缓存优化与数据局部性（C++/硬件）](Book/part14_perf/ch154_cache_opt.md)、[ch156 编译器优化：O2/O3/Ofast/LTO/PGO（GCC）](Book/part14_perf/ch156_compiler_opt.md)、[ch157 Compiler Explorer 实战](Book/part14_perf/ch157_compiler_explorer.md)

### ch156 · 编译器优化：O2/O3/Ofast/LTO/PGO（GCC）

- 文件：`Book/part14_perf/ch156_compiler_opt.md` ｜ Part：`part14_perf`
- **出链**（本章指向）：
  [ch152 性能模型与测量学](Book/part14_perf/ch152_perf_model.md)、[ch154 缓存优化与数据局部性（C++/硬件）](Book/part14_perf/ch154_cache_opt.md)、[ch155 SIMD / AVX 向量化（C++/硬件）](Book/part14_perf/ch155_simd.md)、[ch157 Compiler Explorer 实战](Book/part14_perf/ch157_compiler_explorer.md)、[ch158 性能反模式与陷阱](Book/part14_perf/ch158_perf_antipatterns.md)
- **入链**（指向本章）：
  [ch152 性能模型与测量学](Book/part14_perf/ch152_perf_model.md)、[ch153 CPU 微架构：流水线 / 分支预测 / 乱序执行](Book/part14_perf/ch153_cpu_micro.md)、[ch154 缓存优化与数据局部性（C++/硬件）](Book/part14_perf/ch154_cache_opt.md)、[ch155 SIMD / AVX 向量化（C++/硬件）](Book/part14_perf/ch155_simd.md)、[ch157 Compiler Explorer 实战](Book/part14_perf/ch157_compiler_explorer.md)、[ch158 性能反模式与陷阱](Book/part14_perf/ch158_perf_antipatterns.md)

### ch157 · Compiler Explorer 实战

- 文件：`Book/part14_perf/ch157_compiler_explorer.md` ｜ Part：`part14_perf`
- **出链**（本章指向）：
  [ch11 编译器全景：GCC / Clang / MSVC 架构与 ABI（C++）](Book/part02_toolchain/ch11_compilers.md)、[ch15 性能分析：perf / VTune / 火焰图 / Compiler Explorer（C++）](Book/part02_toolchain/ch15_profiling.md)、[ch152 性能模型与测量学](Book/part14_perf/ch152_perf_model.md)、[ch155 SIMD / AVX 向量化（C++/硬件）](Book/part14_perf/ch155_simd.md)、[ch156 编译器优化：O2/O3/Ofast/LTO/PGO（GCC）](Book/part14_perf/ch156_compiler_opt.md)、[ch158 性能反模式与陷阱](Book/part14_perf/ch158_perf_antipatterns.md)、[ch159 从零实现线程池（C++）](Book/part15_cases/ch159_threadpool.md)
- **入链**（指向本章）：
  [ch11 编译器全景：GCC / Clang / MSVC 架构与 ABI（C++）](Book/part02_toolchain/ch11_compilers.md)、[ch15 性能分析：perf / VTune / 火焰图 / Compiler Explorer（C++）](Book/part02_toolchain/ch15_profiling.md)、[ch151 基准测试与性能度量（C++）](Book/part13_engineering/ch151_benchmark.md)、[ch152 性能模型与测量学](Book/part14_perf/ch152_perf_model.md)、[ch153 CPU 微架构：流水线 / 分支预测 / 乱序执行](Book/part14_perf/ch153_cpu_micro.md)、[ch155 SIMD / AVX 向量化（C++/硬件）](Book/part14_perf/ch155_simd.md)、[ch156 编译器优化：O2/O3/Ofast/LTO/PGO（GCC）](Book/part14_perf/ch156_compiler_opt.md)、[ch158 性能反模式与陷阱](Book/part14_perf/ch158_perf_antipatterns.md)

### ch158 · 性能反模式与陷阱

- 文件：`Book/part14_perf/ch158_perf_antipatterns.md` ｜ Part：`part14_perf`
- **出链**（本章指向）：
  [ch152 性能模型与测量学](Book/part14_perf/ch152_perf_model.md)、[ch153 CPU 微架构：流水线 / 分支预测 / 乱序执行](Book/part14_perf/ch153_cpu_micro.md)、[ch154 缓存优化与数据局部性（C++/硬件）](Book/part14_perf/ch154_cache_opt.md)、[ch156 编译器优化：O2/O3/Ofast/LTO/PGO（GCC）](Book/part14_perf/ch156_compiler_opt.md)、[ch157 Compiler Explorer 实战](Book/part14_perf/ch157_compiler_explorer.md)、[ch159 从零实现线程池（C++）](Book/part15_cases/ch159_threadpool.md)、[ch160 从零实现内存池（C++）](Book/part15_cases/ch160_mempool.md)
- **入链**（指向本章）：
  [ch152 性能模型与测量学](Book/part14_perf/ch152_perf_model.md)、[ch153 CPU 微架构：流水线 / 分支预测 / 乱序执行](Book/part14_perf/ch153_cpu_micro.md)、[ch156 编译器优化：O2/O3/Ofast/LTO/PGO（GCC）](Book/part14_perf/ch156_compiler_opt.md)、[ch157 Compiler Explorer 实战](Book/part14_perf/ch157_compiler_explorer.md)

### ch159 · 从零实现线程池（C++）

- 文件：`Book/part15_cases/ch159_threadpool.md` ｜ Part：`part15_cases`
- **出链**（本章指向）：
  [ch107 std::atomic 原子类型（C++11）](Book/part09_concurrency/ch107_atomic.md)、[ch116 完美转发与万能引用](Book/part10_modern/ch116_perfect_forwarding.md)、[ch160 从零实现内存池（C++）](Book/part15_cases/ch160_mempool.md)
- **入链**（指向本章）：
  [ch86 容器适配器：stack / queue / priority_queue](Book/part07_stl/ch86_adapters.md)、[ch93 线程与异步：thread / future / async](Book/part07_stl/ch93_thread_async.md)、[ch94 stop_token 与协作取消 [标准]](Book/part07_stl/ch94_stop_token.md)、[ch157 Compiler Explorer 实战](Book/part14_perf/ch157_compiler_explorer.md)、[ch158 性能反模式与陷阱](Book/part14_perf/ch158_perf_antipatterns.md)、[ch160 从零实现内存池（C++）](Book/part15_cases/ch160_mempool.md)、[ch163 从零实现网络编程（C++）](Book/part15_cases/ch163_net.md)、[ch164 从零实现迷你框架（C++）](Book/part15_cases/ch164_framework.md)

### ch160 · 从零实现内存池（C++）

- 文件：`Book/part15_cases/ch160_mempool.md` ｜ Part：`part15_cases`
- **出链**（本章指向）：
  [ch122 PMR 与多态分配器](Book/part10_modern/ch122_pmr.md)、[ch159 从零实现线程池（C++）](Book/part15_cases/ch159_threadpool.md)、[ch161 从零实现日志库（C++）](Book/part15_cases/ch161_logger.md)
- **入链**（指向本章）：
  [ch38 第 38 章 分配器（Allocator）模型与 PMR](Book/part04_memory/ch38_allocator.md)、[ch44 第 44 章 内存池（Memory Pool）从零实现](Book/part04_memory/ch44_memory_pool.md)、[ch158 性能反模式与陷阱](Book/part14_perf/ch158_perf_antipatterns.md)、[ch159 从零实现线程池（C++）](Book/part15_cases/ch159_threadpool.md)、[ch161 从零实现日志库（C++）](Book/part15_cases/ch161_logger.md)

### ch161 · 从零实现日志库（C++）

- 文件：`Book/part15_cases/ch161_logger.md` ｜ Part：`part15_cases`
- **出链**（本章指向）：
  [ch131 fmt / spdlog 格式化与日志（C++）](Book/part11_source/ch131_fmt_spdlog.md)、[ch144 代码风格与规范（C++）](Book/part13_engineering/ch144_style.md)、[ch160 从零实现内存池（C++）](Book/part15_cases/ch160_mempool.md)、[ch162 从零实现 JSON 库（C++）](Book/part15_cases/ch162_json.md)
- **入链**（指向本章）：
  [ch144 代码风格与规范（C++）](Book/part13_engineering/ch144_style.md)、[ch160 从零实现内存池（C++）](Book/part15_cases/ch160_mempool.md)、[ch162 从零实现 JSON 库（C++）](Book/part15_cases/ch162_json.md)

### ch162 · 从零实现 JSON 库（C++）

- 文件：`Book/part15_cases/ch162_json.md` ｜ Part：`part15_cases`
- **出链**（本章指向）：
  [ch63 可变参数模板与包展开（Variadic Templates & Pack Expansion）](Book/part06_templates/ch63_variadic.md)、[ch88 optional / expected / variant：可空与可辨别联合](Book/part07_stl/ch88_optional_variant.md)、[ch161 从零实现日志库（C++）](Book/part15_cases/ch161_logger.md)、[ch163 从零实现网络编程（C++）](Book/part15_cases/ch163_net.md)
- **入链**（指向本章）：
  [ch161 从零实现日志库（C++）](Book/part15_cases/ch161_logger.md)、[ch163 从零实现网络编程（C++）](Book/part15_cases/ch163_net.md)

### ch163 · 从零实现网络编程（C++）

- 文件：`Book/part15_cases/ch163_net.md` ｜ Part：`part15_cases`
- **出链**（本章指向）：
  [ch113 协程 coroutine：promise / awaiter（C++20）](Book/part09_concurrency/ch113_coroutine.md)、[ch159 从零实现线程池（C++）](Book/part15_cases/ch159_threadpool.md)、[ch162 从零实现 JSON 库（C++）](Book/part15_cases/ch162_json.md)、[ch164 从零实现迷你框架（C++）](Book/part15_cases/ch164_framework.md)
- **入链**（指向本章）：
  [ch162 从零实现 JSON 库（C++）](Book/part15_cases/ch162_json.md)、[ch164 从零实现迷你框架（C++）](Book/part15_cases/ch164_framework.md)

### ch164 · 从零实现迷你框架（C++）

- 文件：`Book/part15_cases/ch164_framework.md` ｜ Part：`part15_cases`
- **出链**（本章指向）：
  [ch141 依赖注入（C++）](Book/part12_patterns/ch141_di.md)、[ch159 从零实现线程池（C++）](Book/part15_cases/ch159_threadpool.md)、[ch163 从零实现网络编程（C++）](Book/part15_cases/ch163_net.md)
- **入链**（指向本章）：
  [ch163 从零实现网络编程（C++）](Book/part15_cases/ch163_net.md)

### ch165 · C++ 进阶路线图（C++）

- 文件：`Book/part16_reading/ch165_roadmap.md` ｜ Part：`part16_reading`
- **出链**（本章指向）：
  [ch01 C 语言遗产与 C with Classes](Book/part01_history/ch01_c_history.md)、[ch19 变量、存储期、链接与 ODR（工业级深度版）](Book/part03_language/ch19_variables.md)、[ch39 第 39 章 RAII 与 Rule of Zero/Three/Five](Book/part04_memory/ch39_raii_rule.md)、[ch77 vector：扩容、失效、allocator 协作](Book/part07_stl/ch77_vector.md)、[ch115 移动语义与右值引用](Book/part10_modern/ch115_move.md)
- **入链**：无

## 4. 枢纽章节 Top10（按入链数）

> 入链越高，越多章节以它为前置——优先掌握这些「地基章」。

| 章节 | 入链数 | 出链数 |
|---|---:|---:|
| [ch77](Book/part07_stl/ch77_vector.md) vector：扩容、失效、allocator 协作 | 21 | 10 |
| [ch19](Book/part03_language/ch19_variables.md) 变量、存储期、链接与 ODR（工业级深度版） | 19 | 5 |
| [ch115](Book/part10_modern/ch115_move.md) 移动语义与右值引用 | 17 | 7 |
| [ch65](Book/part06_templates/ch65_type_traits.md) 类型特性 Type Traits —— 编译期类型自省与分发 | 16 | 3 |
| [ch88](Book/part07_stl/ch88_optional_variant.md) optional / expected / variant：可空与可辨别联合 | 13 | 7 |
| [ch20](Book/part03_language/ch20_reference_pointer.md) 引用（reference）vs 指针（pointer）：语义本质、底层实现与生命周期战争 | 12 | 5 |
| [ch39](Book/part04_memory/ch39_raii_rule.md) 第 39 章 RAII 与 Rule of Zero/Three/Five | 12 | 3 |
| [ch107](Book/part09_concurrency/ch107_atomic.md) std::atomic 原子类型（C++11） | 12 | 5 |
| [ch152](Book/part14_perf/ch152_perf_model.md) 性能模型与测量学 | 11 | 7 |
| [ch154](Book/part14_perf/ch154_cache_opt.md) 缓存优化与数据局部性（C++/硬件） | 11 | 3 |

## 5. 孤立章节与断链

- **孤立章节**：无（每章至少在一侧有连接）

- **断链**：0（全部交叉引用目标均存在）
