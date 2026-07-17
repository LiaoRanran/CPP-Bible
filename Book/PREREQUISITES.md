# 前置依赖建议（PREREQUISITES）

> 共 16 章声明了显式前置依赖。
> 本文件由 `tools/gen_indexes.py` 自动生成，请勿手改。

## 一、Part 级阅读链（启发式建议）

> 按全书 part 编号的自然递进顺序，前序 part 是后续 part 的软前置；可按需跳读，非强制。

- 第一部分　历史与演进 —— 入口，无前置。
- 第二部分　工具链与构建 —— 建议先读：第一部分　历史与演进 及之前各部分。
- 第三部分　语言核心 —— 建议先读：第二部分　工具链与构建 及之前各部分。
- 第四部分　内存管理 —— 建议先读：第三部分　语言核心 及之前各部分。
- 第五部分　面向对象 —— 建议先读：第四部分　内存管理 及之前各部分。
- 第六部分　模板与泛型 —— 建议先读：第五部分　面向对象 及之前各部分。
- 第七部分　标准模板库（STL） —— 建议先读：第六部分　模板与泛型 及之前各部分。
- 第八部分　算法 —— 建议先读：第七部分　标准模板库（STL） 及之前各部分。
- 第九部分　并发与多线程 —— 建议先读：第八部分　算法 及之前各部分。
- 第十部分　现代 C++ 特性 —— 建议先读：第九部分　并发与多线程 及之前各部分。
- 第十一部分　源码剖析 —— 建议先读：第十部分　现代 C++ 特性 及之前各部分。
- 第十二部分　设计模式 —— 建议先读：第十一部分　源码剖析 及之前各部分。
- 第十三部分　工程实践 —— 建议先读：第十二部分　设计模式 及之前各部分。
- 第十四部分　性能优化 —— 建议先读：第十三部分　工程实践 及之前各部分。
- 第十五部分　实战案例 —— 建议先读：第十四部分　性能优化 及之前各部分。
- 第十六部分　进阶阅读 —— 建议先读：第十五部分　实战案例 及之前各部分。

## 二、逐章显式前置（来自各章真实元数据 `前置：`）

> 下列条目直接摘自章内元数据，只列出确实声明了前置的章节。

- [ch4](part01_history/ch04_cpp11.md) 第04章　C++11：现代 C++ 革命　←　前置：[ch1](part01_history/ch01_c_history.md)、[ch3](part01_history/ch03_cpp98_03.md)
- [ch5](part01_history/ch05_cpp14.md) 第05章　C++14：小幅完善　←　前置：[ch4](part01_history/ch04_cpp11.md)
- [ch6](part01_history/ch06_cpp17.md) 第06章　C++17：生产力跃升　←　前置：[ch4](part01_history/ch04_cpp11.md)、[ch5](part01_history/ch05_cpp14.md)
- [ch7](part01_history/ch07_cpp20.md) 第07章　C++20：量级升级　←　前置：[ch4](part01_history/ch04_cpp11.md)、[ch6](part01_history/ch06_cpp17.md)、[ch60](part06_templates/ch60_template_basics.md)、[ch63](part06_templates/ch63_variadic.md)
- [ch8](part01_history/ch08_cpp23.md) 第08章　C++23：标准库大修　←　前置：[ch4](part01_history/ch04_cpp11.md)、[ch7](part01_history/ch07_cpp20.md)
- [ch9](part01_history/ch09_cpp26.md) 第09章　C++26：已确定特性与方向　←　前置：[ch7](part01_history/ch07_cpp20.md)、[ch67](part06_templates/ch67_concepts.md)、[ch113](part09_concurrency/ch113_coroutine.md)
- [ch10](part01_history/ch10_version_matrix.md) 第10章　版本特性全景对照表与迁移指南　←　前置：[ch3](part01_history/ch03_cpp98_03.md)、[ch9](part01_history/ch09_cpp26.md)
- [ch19](part03_language/ch19_variables.md) 第19章　变量、存储期、链接与 ODR（工业级深度版）　←　前置：[ch1](part01_history/ch01_c_history.md)、[ch10](part01_history/ch10_version_matrix.md)、[ch20](part03_language/ch20_reference_pointer.md)、[ch31](part03_language/ch31_operator_overloading.md)
- [ch20](part03_language/ch20_reference_pointer.md) 第20章　引用（reference）vs 指针（pointer）：语义本质、底层实现与生命周期战争　←　前置：[ch19](part03_language/ch19_variables.md)
- [ch21](part03_language/ch21_const_family.md) 第21章　const / constexpr / consteval / constinit 深度详解　←　前置：[ch19](part03_language/ch19_variables.md)
- [ch23](part03_language/ch23_namespace_adl.md) 第23章　命名空间（namespace）、using 与参数依赖查找（ADL）：隔离、版本化与隐形查找　←　前置：[ch19](part03_language/ch19_variables.md)
- [ch25](part03_language/ch25_union_variant.md) 第25章　union 与 std::variant 深度详解　←　前置：[ch19](part03_language/ch19_variables.md)
- [ch26](part03_language/ch26_lambda.md) 第26章　lambda 表达式全解：闭包类型、捕获、泛型/模板 lambda、constexpr、ABI 与 std::function 类型擦除　←　前置：[ch19](part03_language/ch19_variables.md)
- [ch27](part03_language/ch27_cast.md) 第27章　显式转型四兄弟与隐式转换：const_cast / static_cast / dynamic_cast / reinterpret_cast 深度详解　←　前置：[ch19](part03_language/ch19_variables.md)
- [ch28](part03_language/ch28_lifetime_ub.md) 第28章　对象生命周期与未定义行为（UB）：生存期、悬垂、UB 分类与编译器武器化　←　前置：[ch19](part03_language/ch19_variables.md)
- [ch65](part06_templates/ch65_type_traits.md) 第65章　类型特性 Type Traits —— 编译期类型自省与分发　←　前置：[ch60](part06_templates/ch60_template_basics.md)、[ch62](part06_templates/ch62_specialization.md)、[ch63](part06_templates/ch63_variadic.md)
