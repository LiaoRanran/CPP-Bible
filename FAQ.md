# FAQ — 全书常见问题索引

> 从 48 章的 ⑰ FAQ/常见问题 节自动提取。关联: ⟶ PROGRESS.md ⟶ ISSUES.md

## 版本史 (part01)
- **ch01**: 为何不设计全新语言？ C with Classes 为何有 class 又有 struct？
- **ch02**: 需要读标准原文吗？提案和最终标准差很多吗？
- **ch03**: C++98 代码为何现在还能编译？C++03 值得专门学吗？
- **ch04**: C++11 还能算"C++"吗？为什么叫 C++11 而不是 C++10？
- **ch05**: C++14 值得单独学吗？
- **ch06**: if constexpr 与运行时 if 区别？为什么 optional 不用 union 实现？
- **ch07**: 必须学 Modules 吗？Coroutines 难吗？
- **ch08**: 为什么 expected 不直接用异常？print 和 format 区别？
- **ch09**: C++26 何时发布？需要现在学吗？
- **ch10**: 能否随意升到 -std=c++23？如何写跨版本代码？

## 面向对象 (part05)
- **ch47**: (空) ⟶ 待补
- **ch48**: (空) ⟶ 待补
- **ch49**: (空) ⟶ 待补
- **ch50**: 为什么第二基类偏移不是 0？thunk 有运行时开销吗？
- **ch51**: CRTP 的 static_cast 不会越界吗？为什么叫"奇异递归"？

## 模板 (part06)
- **ch60**: 模板定义为什么要放在头文件？分离编译为何失败？
- **ch61**: 为什么显式特化比偏特化优先？ADL 和重载决议谁先？
- **ch62**: 偏特化能特化成员函数吗？全特化影响主模板吗？
- **ch63**: 递归展开和折叠表达式哪个更优？
- **ch64**: 为什么 `(void)(x...)` 不合法？
- **ch65**: type traits 是编译期还是运行期？
- **ch66**: SFINAE 和 Concepts 选哪个？
- **ch67**: Concept 的 requires 和 requires 子句区别？
- **ch68**: TMP 递归有深度限制吗？
- **ch69**: constexpr 函数在运行时能调用吗？
- **ch70**: tag dispatch 和 if constexpr 怎么选？
- **ch71**: Policy 类必须无状态吗？
- **ch72**: 表达式模板和 Ranges 是什么关系？

## STL (part07)
- 15 章含 FAQ: ch76–ch94 各章 ⑰ 节
- 覆盖: vector 扩容/失效、map lower_bound、unordered rehash、span 越界、ranges dangling、filesystem 跨平台 等

## 现代特性 (part10)
- **ch115**: const 对象能 move 吗？return std::move 为何是反模式？
- **ch116**: forward 和 move 的本质区别？
- 待补: ch120–123 ⟶ ch120 协程状态转移、ch121 契约 vs 异常

## 性能 (part14)
- **ch115 性能**: noexcept 移动为何影响 vector 性能？
- **ch120**: (待补)
- **ch152**: 为什么 microbenchmark 抓不到 p99？-O3 比 -O2 慢的可能原因？

> 详细答案见各自章节的 ⑰ 节。本文档为索引，定期自动更新。
