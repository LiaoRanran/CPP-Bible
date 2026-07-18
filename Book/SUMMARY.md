# 目录（SUMMARY）

> 本文件由 `tools/gen_indexes.py` 自动生成，请勿手改。
> 全书 16 部分 / 147 章。链接路径相对本目录（Book/）。
>
> **编号连续性说明**：本章号并非从 1 连续递增，全书沿用“删章留空、不重排”的设计——历史演进中淘汰或合并的章节，其编号被刻意保留为空缺，后续章节不回填，以保证既有交叉引用（如 `⟶ Book/...chNN_...md`）与读者笔记的稳定性。当前有效编号范围为 1–165，共 147 章；**18 个编号空缺**：33-34、53-59、73-75、102-106、114。这些空缺是设计保留，并非笔误。

## 第一部分　历史与演进

- [第01章　C 语言遗产与 C with Classes](part01_history/ch01_c_history.md)
- [第02章　标准化组织、WG21 与提案流程](part01_history/ch02_standardization.md)
- [第03章　C++98 / C++03：奠基时代](part01_history/ch03_cpp98_03.md)
- [第04章　C++11：现代 C++ 革命](part01_history/ch04_cpp11.md)
- [第05章　C++14：小幅完善](part01_history/ch05_cpp14.md)
- [第06章　C++17：生产力跃升](part01_history/ch06_cpp17.md)
- [第07章　C++20：量级升级](part01_history/ch07_cpp20.md)
- [第08章　C++23：标准库大修](part01_history/ch08_cpp23.md)
- [第09章　C++26：已确定特性与方向](part01_history/ch09_cpp26.md)
- [第10章　版本特性全景对照表与迁移指南](part01_history/ch10_version_matrix.md)

## 第二部分　工具链与构建

- [第11章　编译器全景：GCC / Clang / MSVC 架构与 ABI（C++）](part02_toolchain/ch11_compilers.md)
- [第12章　构建系统：Make / Ninja / CMake（C++）](part02_toolchain/ch12_buildsystems.md)
- [第13章　包管理：vcpkg / Conan（C++）](part02_toolchain/ch13_packaging.md)
- [第14章　调试与诊断：GDB / LLDB / Sanitizer / Valgrind（C++）](part02_toolchain/ch14_debugging.md)
- [第15章　性能分析：perf / VTune / 火焰图 / Compiler Explorer（C++）](part02_toolchain/ch15_profiling.md)
- [第16章　IDE 与编辑器：VSCode / CLion / QtCreator / VIM（C++）](part02_toolchain/ch16_ide.md)
- [第17章　交叉编译与嵌入式工具链（C++）](part02_toolchain/ch17_crosscompile.md)
- [第18章　构建配置：Debug / Release / LTO / PGO（C++）](part02_toolchain/ch18_buildconfig.md)

## 第三部分　语言核心

- [第19章　变量、存储期、链接与 ODR（工业级深度版）](part03_language/ch19_variables.md)
- [第20章　引用（reference）vs 指针（pointer）：语义本质、底层实现与生命周期战争](part03_language/ch20_reference_pointer.md)
- [第21章　const / constexpr / consteval / constinit 深度详解](part03_language/ch21_const_family.md)
- [第 22 章 · `auto` 类型推导、`decltype` 与返回类型推导](part03_language/ch22_auto_decltype.md)
- [第23章　命名空间（namespace）、using 与参数依赖查找（ADL）：隔离、版本化与隐形查找](part03_language/ch23_namespace_adl.md)
- [第 24 章　枚举（枚举类型全解：unscoped / enum class / 位掩码 / ABI / 反射）](part03_language/ch24_enum.md)
- [第25章　union 与 std::variant 深度详解](part03_language/ch25_union_variant.md)
- [第26章　lambda 表达式全解：闭包类型、捕获、泛型/模板 lambda、constexpr、ABI 与 std::function 类型擦除](part03_language/ch26_lambda.md)
- [第27章　显式转型四兄弟与隐式转换：const_cast / static_cast / dynamic_cast / reinterpret_cast 深度详解](part03_language/ch27_cast.md)
- [第28章　对象生命周期与未定义行为（UB）：生存期、悬垂、UB 分类与编译器武器化](part03_language/ch28_lifetime_ub.md)
- [第29章 友元 friend 与访问控制](part03_language/ch29_friend.md)
- [第30章 volatile / atomic 与硬件寄存器](part03_language/ch30_volatile.md)
- [第31章 运算符重载](part03_language/ch31_operator_overloading.md)
- [第32章 初始化与列表初始化](part03_language/ch32_initialization.md)

## 第四部分　内存管理

- [第 35 章  C++ 程序的内存模型与操作系统视角](part04_memory/ch35_memory_layout.md)
- [第 36 章　栈（stack）与堆（heap）的深度对比](part04_memory/ch36_stack_heap.md)
- [第 37 章 动态内存分配原语：`operator new` / `operator delete`](part04_memory/ch37_new_delete.md)
- [第 38 章　分配器（Allocator）模型与 PMR](part04_memory/ch38_allocator.md)
- [第 39 章　RAII 与 Rule of Zero/Three/Five](part04_memory/ch39_raii_rule.md)
- [第 40 章　异常安全（Exception Safety）](part04_memory/ch40_exception_safety.md)
- [第 41 章 智能指针全解（unique_ptr / shared_ptr / weak_ptr / enable_shared_from_this）](part04_memory/ch41_smart_pointers.md)
- [第 42 章 · 严格别名规则（Strict Aliasing）与编译器优化](part04_memory/ch42_strict_aliasing.md)
- [第 43 章　CPU 缓存体系与内存局部性](part04_memory/ch43_cache_locality.md)
- [第 44 章 内存池（Memory Pool）从零实现](part04_memory/ch44_memory_pool.md)

## 第五部分　面向对象

- [第 45 章　C++ 面向对象总览与对象模型基础](part05_oo/ch45_oop_object_model.md)
- [第 46 章　封装与继承深度：访问控制、三种继承、切片、构造/析构、名字隐藏、override/final、NVI](part05_oo/ch46_encapsulation_inheritance.md)
- [第47章 虚函数与虚表（vtable）：动态多态的发动机](part05_oo/ch47_virtual_functions.md)
- [第48章 RTTI 与 typeid/dynamic_cast：运行时类型查询](part05_oo/ch48_rtti.md)
- [第49章 虚继承与菱形继承：共享虚基类](part05_oo/ch49_virtual_inheritance.md)
- [第50章　多重继承与对象模型（Multiple Inheritance）](part05_oo/ch50_multiple_inheritance.md)
- [第51章　CRTP 与静态多态（Curiously Recurring Template Pattern）](part05_oo/ch51_crtp.md)
- [第52章　空基类优化 EBO（Empty Base Optimization）](part05_oo/ch52_ebo.md)

## 第六部分　模板与泛型

- [第60章　模板基础与实例化（Template Basics & Instantiation）](part06_templates/ch60_template_basics.md)
- [第61章　函数模板重载决议（Function Template Overload Resolution）](part06_templates/ch61_template_overload.md)
- [第62章　类模板特化与偏特化（Class Template Specialization）](part06_templates/ch62_specialization.md)
- [第63章　可变参数模板与包展开（Variadic Templates & Pack Expansion）](part06_templates/ch63_variadic.md)
- [第64章　折叠表达式 Fold Expression（C++17）](part06_templates/ch64_fold.md)
- [第65章　类型特性 Type Traits —— 编译期类型自省与分发](part06_templates/ch65_type_traits.md)
- [第66章　SFINAE 与 std::enable_if —— 替换失败非错误的编译期分发](part06_templates/ch66_sfinae.md)
- [第67章　Concepts 与 requires —— C++20 的编译期约束](part06_templates/ch67_concepts.md)
- [第68章　模板元编程 TMP 基础（递归 / 分支 / 循环）](part06_templates/ch68_tmp.md)
- [第69章　编译期计算：constexpr / consteval / constinit](part06_templates/ch69_constexpr.md)
- [第70章　std::integral_constant 与标签分发（Tag Dispatch）](part06_templates/ch70_tag_dispatch.md)
- [第71章　策略设计 Policy-Based Design](part06_templates/ch71_policy.md)
- [第72章　表达式模板 Expression Templates](part06_templates/ch72_expression_templates.md)

## 第七部分　标准模板库（STL）

- [第76章　STL 架构与迭代器概念](part07_stl/ch76_stl_arch.md)
- [第77章　vector：扩容、失效、allocator 协作](part07_stl/ch77_vector.md)
- [第78章　deque 与分段连续 [标准]](part07_stl/ch78_deque.md)
- [第79章　list / forward_list [标准]](part07_stl/ch79_list.md)
- [第80章　array 与固定数组](part07_stl/ch80_array.md)
- [第81章　std::string 与 SSO 短字符串优化](part07_stl/ch81_string.md)
- [第82章　span 与裸数组视图](part07_stl/ch82_span.md)
- [第83章　map / multimap（红黑树）](part07_stl/ch83_map.md)
- [第84章　set / multiset：红黑树有序集合](part07_stl/ch84_set.md)
- [第85章　unordered_map / unordered_set：哈希开链集合](part07_stl/ch85_unordered.md)
- [第86章　容器适配器：stack / queue / priority_queue](part07_stl/ch86_adapters.md)
- [第87章　bitset：编译期定长位集](part07_stl/ch87_bitset.md)
- [第88章　optional / expected / variant：可空与可辨别联合](part07_stl/ch88_optional_variant.md)
- [第89章　tuple / pair / any / function / bind](part07_stl/ch89_tuple_any.md)
- [第90章　ranges 与 views：惰性求值与管道组合](part07_stl/ch90_ranges.md)
- [第91章 文件系统 filesystem](part07_stl/ch91_filesystem.md)
- [第92章 时间库 chrono](part07_stl/ch92_chrono.md)
- [第93章　线程与异步：thread / future / async](part07_stl/ch93_thread_async.md)
- [第94章　stop_token 与协作取消 [标准]](part07_stl/ch94_stop_token.md)

## 第八部分　算法

- [第95章　STL 算法分类与复杂度（C++）](part08_algorithms/ch95_algo_overview.md)
- [第96章　排序：sort / stable_sort / partial_sort（C++）](part08_algorithms/ch96_sorting.md)
- [第97章　查找与二分（C++）](part08_algorithms/ch97_search.md)
- [第98章　堆算法 heap（C++）](part08_algorithms/ch98_heap.md)
- [第99章　数值算法与并行执行策略（C++）](part08_algorithms/ch99_numeric.md)
- [第100章　Ranges 算法与投影（C++20）](part08_algorithms/ch100_ranges_algo.md)
- [第101章　哈希、图、树、DP、贪心（算法思想）](part08_algorithms/ch101_algo_theory.md)

## 第九部分　并发与多线程

- [第107章　std::atomic 原子类型（C++11）](part09_concurrency/ch107_atomic.md)
- [第108章　memory_order：六种内存序（C++11）](part09_concurrency/ch108_memory_order.md)
- [第109章 内存屏障与 fence](part09_concurrency/ch109_fence.md)
- [第110章　无锁编程：lock-free / wait-free（C++11）](part09_concurrency/ch110_lockfree.md)
- [第111章　ABA 问题与解决（C++11）](part09_concurrency/ch111_aba.md)
- [第112章　Hazard Pointer 与 RCU（C++11/实践）](part09_concurrency/ch112_hazard_rcu.md)
- [第113章　协程 coroutine：promise / awaiter（C++20）](part09_concurrency/ch113_coroutine.md)

## 第十部分　现代 C++ 特性

- [第115章　移动语义与右值引用](part10_modern/ch115_move.md)
- [第116章　完美转发与万能引用](part10_modern/ch116_perfect_forwarding.md)
- [第117章　RVO / NRVO 与拷贝消除（C++17）](part10_modern/ch117_copy_elision.md)
- [第118章　Modules 模块（C++20）](part10_modern/ch118_modules.md)
- [第119章　Ranges 深入（C++20）](part10_modern/ch119_ranges_deep.md)
- [第120章 Coroutine 应用模式](part10_modern/ch120_coroutine_app.md)
- [第121章 Contracts 契约（方向，C++26）](part10_modern/ch121_contracts.md)
- [第122章　PMR 与多态分配器](part10_modern/ch122_pmr.md)
- [第123章　Compile-Time 编程范式总览](part10_modern/ch123_ct_programming.md)

## 第十一部分　源码剖析

- [第124章　libstdc++ 架构与阅读入口（C++）](part11_source/ch124_libstdcxx.md)
- [第125章　libc++ 架构（C++）](part11_source/ch125_libcxx.md)
- [第126章　MS STL 架构（C++）](part11_source/ch126_msstl.md)
- [第127章　LLVM / Clang 架构（C++）](part11_source/ch127_llvm.md)
- [第128章　Boost 核心库（C++）](part11_source/ch128_boost.md)
- [第129章　Qt 对象模型与信号槽（C++）](part11_source/ch129_qt.md)
- [第130章　Chromium / Abseil 基础设施（C++）](part11_source/ch130_chromium_abseil.md)
- [第131章　fmt / spdlog 格式化与日志（C++）](part11_source/ch131_fmt_spdlog.md)
- [第132章　LevelDB / RocksDB 存储引擎（C++）](part11_source/ch132_leveldb_rocksdb.md)
- [第133章　ClickHouse / Redis 实现精读（C++）](part11_source/ch133_clickhouse_redis.md)
- [第134章　Unreal Engine C++ 架构（C++）](part11_source/ch134_unreal.md)

## 第十二部分　设计模式

- [第135章 设计模式总论（C++）](part12_patterns/ch135_patterns_intro.md)
- [第136章 创建型模式（C++）](part12_patterns/ch136_creational.md)
- [第137章 结构型模式（C++）](part12_patterns/ch137_structural.md)
- [第138章 行为型模式（C++）](part12_patterns/ch138_behavioral.md)
- [第139章 CRTP 与静态多态（C++）](part12_patterns/ch139_crtp_pattern.md)
- [第140章 Policy-Based Design（C++）](part12_patterns/ch140_policy_pattern.md)
- [第141章 依赖注入（C++）](part12_patterns/ch141_di.md)
- [第142章 实体组件系统 ECS（C++）](part12_patterns/ch142_ecs.md)
- [第143章 面向数据设计 DOD（C++）](part12_patterns/ch143_dod.md)

## 第十三部分　工程实践

- [第144章 代码风格与规范（C++）](part13_engineering/ch144_style.md)
- [第145章 命名与 API 设计（C++）](part13_engineering/ch145_naming_api.md)
- [第146章 错误处理（C++）](part13_engineering/ch146_error_handling.md)
- [第147章 代码审查（C++）](part13_engineering/ch147_code_review.md)
- [第148章 Git 工作流（C++）](part13_engineering/ch148_gitflow.md)
- [第149章 CI/CD 流水线（C++）](part13_engineering/ch149_ci_cd.md)
- [第150章 测试策略（C++）](part13_engineering/ch150_testing.md)
- [第151章 基准测试与性能度量（C++）](part13_engineering/ch151_benchmark.md)

## 第十四部分　性能优化

- [第152章　性能模型与测量学](part14_perf/ch152_perf_model.md)
- [第153章　CPU 微架构：流水线 / 分支预测 / 乱序执行](part14_perf/ch153_cpu_micro.md)
- [第154章　缓存优化与数据局部性（C++/硬件）](part14_perf/ch154_cache_opt.md)
- [第155章　SIMD / AVX 向量化（C++/硬件）](part14_perf/ch155_simd.md)
- [第156章　编译器优化：O2/O3/Ofast/LTO/PGO（GCC）](part14_perf/ch156_compiler_opt.md)
- [第157章 Compiler Explorer 实战](part14_perf/ch157_compiler_explorer.md)
- [第158章 性能反模式与陷阱](part14_perf/ch158_perf_antipatterns.md)

## 第十五部分　实战案例

- [第159章 从零实现线程池（C++）](part15_cases/ch159_threadpool.md)
- [第160章 从零实现内存池（C++）](part15_cases/ch160_mempool.md)
- [第161章 从零实现日志库（C++）](part15_cases/ch161_logger.md)
- [第162章 从零实现 JSON 库（C++）](part15_cases/ch162_json.md)
- [第163章 从零实现网络编程（C++）](part15_cases/ch163_net.md)
- [第164章 从零实现迷你框架（C++）](part15_cases/ch164_framework.md)

## 第十六部分　进阶阅读

- [第165章 C++ 进阶路线图（C++）](part16_reading/ch165_roadmap.md)
