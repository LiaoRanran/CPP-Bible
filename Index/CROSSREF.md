# 交叉引用图 · CROSSREF

> 知识点双向链接。每对 `A ⇄ B` 表示两章互相引用。随章节推进扩充。

## 核心链
- RAII (ch47) ⇄ 智能指针 (ch48/unique_ptr) ⇄ 异常安全 (ch49)
- new/delete (ch38) ⇄ allocator (ch41) ⇄ 内存池 (ch42) ⇄ PMR (ch122)
- 引用 (ch20) ⇄ 生命周期 (ch33) ⇄ 悬垂 (ch34 UB)
- const (ch21) ⇄ constexpr (ch69) ⇄ 编译期 (ch123)
- 虚函数 (ch54) ⇄ 对象布局 (ch51) ⇄ 多继承 (ch55) ⇄ 虚继承 (ch56)
- 模板 (ch60) ⇄ 特化 (ch62) ⇄ SFINAE (ch66) ⇄ Concepts (ch67) ⇄ Type Traits (ch65)
- 移动 (ch115) ⇄ 完美转发 (ch116) ⇄ 拷贝消除 (ch117) ⇄ Rule of Five (ch48)
- atomic (ch107) ⇄ 内存序 (ch108) ⇄ fence (ch109) ⇄ 无锁 (ch110) ⇄ RCU (ch112)
- 协程 (ch113) ⇄ Executor (ch114) ⇄ 线程池 (ch114/项目)
- vector (ch77) ⇄ allocator (ch41) ⇄ 迭代器失效 (ch76) ⇄ 扩容 (ch77)
- 缓存 (ch44) ⇄ 伪共享 (ch44) ⇄ NUMA (ch45) ⇄ 性能 (ch152)
- ranges (ch90/ch119) ⇄ 算法 (ch95) ⇄ 视图 (ch90)
- CRTP (ch57/ch73) ⇄ 静态多态 (ch57) ⇄ Policy (ch71/ch140) ⇄ 设计模式 (ch135)
- string (ch81) ⇄ SSO (ch81) ⇄ 短字符串 (ch81)
- 模块 (ch118) ⇄ 头文件/ODR (ch19) ⇄ 编译模型
- 异常 (ch49) ⇄ 栈展开 ⇄ noexcept ⇄ 移动 (move_if_noexcept)

## 索引入口
- 术语定义见 `GLOSSARY.md`
- 误区见 `Index/MISCONCEPTIONS.md`
- 全文章目见 `INDEX.md`
