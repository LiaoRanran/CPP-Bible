# 术语表（GLOSSARY）

> 本文件由 `tools/gen_indexes.py` 自动生成，请勿手改。
> 术语 → 讲解该主题的章节。仅收录能匹配到真实章节的术语。
> 共 33 条术语。

- **RAII / 资源管理**：[ch39](part04_memory/ch39_raii_rule.md)
- **智能指针**：[ch41](part04_memory/ch41_smart_pointers.md)
- **移动语义**：[ch115](part10_modern/ch115_move.md)
- **完美转发**：[ch79](part07_stl/ch79_list.md)；[ch116](part10_modern/ch116_perfect_forwarding.md)
- **拷贝省略 / RVO**：[ch117](part10_modern/ch117_copy_elision.md)
- **引用与指针**：[ch20](part03_language/ch20_reference_pointer.md)；[ch41](part04_memory/ch41_smart_pointers.md)；[ch112](part09_concurrency/ch112_hazard_rcu.md)；[ch115](part10_modern/ch115_move.md)；[ch116](part10_modern/ch116_perfect_forwarding.md)
- **const / 常量性**：[ch21](part03_language/ch21_const_family.md)；[ch26](part03_language/ch26_lambda.md)；[ch27](part03_language/ch27_cast.md)；[ch69](part06_templates/ch69_constexpr.md)；[ch70](part06_templates/ch70_tag_dispatch.md)
- **类型转换 (cast)**：[ch27](part03_language/ch27_cast.md)；[ch48](part05_oo/ch48_rtti.md)
- **初始化**：[ch21](part03_language/ch21_const_family.md)；[ch32](part03_language/ch32_initialization.md)；[ch69](part06_templates/ch69_constexpr.md)
- **对象生命周期**：[ch20](part03_language/ch20_reference_pointer.md)；[ch28](part03_language/ch28_lifetime_ub.md)
- **模板**：[ch26](part03_language/ch26_lambda.md)；[ch51](part05_oo/ch51_crtp.md)；[ch60](part06_templates/ch60_template_basics.md)；[ch61](part06_templates/ch61_template_overload.md)；[ch62](part06_templates/ch62_specialization.md)；[ch63](part06_templates/ch63_variadic.md)；[ch68](part06_templates/ch68_tmp.md)；[ch72](part06_templates/ch72_expression_templates.md)
- **变参模板**：[ch63](part06_templates/ch63_variadic.md)
- **模板元编程**：[ch66](part06_templates/ch66_sfinae.md)；[ch67](part06_templates/ch67_concepts.md)；[ch68](part06_templates/ch68_tmp.md)
- **虚函数 / 多态**：[ch47](part05_oo/ch47_virtual_functions.md)；[ch49](part05_oo/ch49_virtual_inheritance.md)；[ch51](part05_oo/ch51_crtp.md)；[ch122](part10_modern/ch122_pmr.md)；[ch139](part12_patterns/ch139_crtp_pattern.md)
- **继承**：[ch46](part05_oo/ch46_encapsulation_inheritance.md)；[ch49](part05_oo/ch49_virtual_inheritance.md)；[ch50](part05_oo/ch50_multiple_inheritance.md)；[ch52](part05_oo/ch52_ebo.md)；[ch71](part06_templates/ch71_policy.md)；[ch140](part12_patterns/ch140_policy_pattern.md)
- **异常安全**：[ch40](part04_memory/ch40_exception_safety.md)
- **STL 容器**：[ch77](part07_stl/ch77_vector.md)；[ch78](part07_stl/ch78_deque.md)；[ch79](part07_stl/ch79_list.md)；[ch80](part07_stl/ch80_array.md)；[ch83](part07_stl/ch83_map.md)；[ch84](part07_stl/ch84_set.md)；[ch85](part07_stl/ch85_unordered.md)；[ch86](part07_stl/ch86_adapters.md) 等 10 章
- **迭代器**：[ch76](part07_stl/ch76_stl_arch.md)
- **算法库**：[ch95](part08_algorithms/ch95_algo_overview.md)；[ch96](part08_algorithms/ch96_sorting.md)；[ch98](part08_algorithms/ch98_heap.md)；[ch99](part08_algorithms/ch99_numeric.md)；[ch100](part08_algorithms/ch100_ranges_algo.md)；[ch101](part08_algorithms/ch101_algo_theory.md)
- **ranges / 视图**：[ch82](part07_stl/ch82_span.md)；[ch90](part07_stl/ch90_ranges.md)；[ch95](part08_algorithms/ch95_algo_overview.md)；[ch100](part08_algorithms/ch100_ranges_algo.md)；[ch119](part10_modern/ch119_ranges_deep.md)；[ch147](part13_engineering/ch147_code_review.md)
- **lambda 表达式**：[ch26](part03_language/ch26_lambda.md)
- **并发与线程**：[ch93](part07_stl/ch93_thread_async.md)；[ch159](part15_cases/ch159_threadpool.md)
- **原子操作 / 内存序**：[ch30](part03_language/ch30_volatile.md)；[ch107](part09_concurrency/ch107_atomic.md)；[ch108](part09_concurrency/ch108_memory_order.md)
- **互斥与锁**：[ch110](part09_concurrency/ch110_lockfree.md)
- **协程**：[ch113](part09_concurrency/ch113_coroutine.md)；[ch120](part10_modern/ch120_coroutine_app.md)
- **编译期计算 / constexpr**：[ch21](part03_language/ch21_const_family.md)；[ch26](part03_language/ch26_lambda.md)；[ch65](part06_templates/ch65_type_traits.md)；[ch66](part06_templates/ch66_sfinae.md)；[ch67](part06_templates/ch67_concepts.md)；[ch69](part06_templates/ch69_constexpr.md)；[ch87](part07_stl/ch87_bitset.md)
- **Concepts / 约束**：[ch67](part06_templates/ch67_concepts.md)
- **Modules 模块**：[ch118](part10_modern/ch118_modules.md)
- **设计模式**：[ch51](part05_oo/ch51_crtp.md)；[ch120](part10_modern/ch120_coroutine_app.md)；[ch135](part12_patterns/ch135_patterns_intro.md)；[ch136](part12_patterns/ch136_creational.md)；[ch137](part12_patterns/ch137_structural.md)；[ch138](part12_patterns/ch138_behavioral.md)；[ch139](part12_patterns/ch139_crtp_pattern.md)；[ch140](part12_patterns/ch140_policy_pattern.md) 等 9 章
- **内存模型 / 布局**：[ch35](part04_memory/ch35_memory_layout.md)；[ch44](part04_memory/ch44_memory_pool.md)；[ch78](part07_stl/ch78_deque.md)；[ch108](part09_concurrency/ch108_memory_order.md)
- **性能优化 / 缓存**：[ch15](part02_toolchain/ch15_profiling.md)；[ch42](part04_memory/ch42_strict_aliasing.md)；[ch43](part04_memory/ch43_cache_locality.md)；[ch52](part05_oo/ch52_ebo.md)；[ch81](part07_stl/ch81_string.md)；[ch116](part10_modern/ch116_perfect_forwarding.md)；[ch151](part13_engineering/ch151_benchmark.md)；[ch152](part14_perf/ch152_perf_model.md) 等 11 章
- **未定义行为 (UB)**：[ch28](part03_language/ch28_lifetime_ub.md)；[ch42](part04_memory/ch42_strict_aliasing.md)
- **链接与编译**：[ch11](part02_toolchain/ch11_compilers.md)；[ch15](part02_toolchain/ch15_profiling.md)；[ch17](part02_toolchain/ch17_crosscompile.md)；[ch19](part03_language/ch19_variables.md)；[ch28](part03_language/ch28_lifetime_ub.md)；[ch42](part04_memory/ch42_strict_aliasing.md)；[ch65](part06_templates/ch65_type_traits.md)；[ch66](part06_templates/ch66_sfinae.md) 等 14 章
