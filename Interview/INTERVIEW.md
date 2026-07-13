# 面试题库 · INTERVIEW

> 按难度/公司分类。每条含问 + 要点答案 + 章节。持续扩充。

## 初级
1. **指针与引用区别？** 见 FAQ、ch20。
2. **`const` 有哪几种用法？** 顶层/底层 const、成员函数 const、ch21。
3. **`new`/`delete` 与 `malloc`/`free` 区别？** ch38。
4. **什么是浅拷贝？** 指针成员共享，需深拷贝，ch48。
5. **`#include` 与前置声明？** 降低耦合，ch118、ch19。

## 中级
6. **虚函数实现原理与开销？** vtable/vptr，一次间接跳转，ch54。
7. **虚继承对象布局？** 虚基类偏移表/vbase 指针，ch56。
8. **`vector` 扩容机制与迭代器失效？** 1.5 倍、Amortized O(1)、扩容全失效，ch77。
9. **`std::move` 语义？** 转右值，ch115。
10. **智能指针 `unique_ptr`/`shared_ptr` 区别与线程安全？** 引用计数原子但对象不保，ch48。
11. **`auto` 推导规则？** ch22。
12. **Lambda 实现（闭包类）？** 编译器生成带成员的类，ch27。

## 高级
13. **完美转发与万能引用？** ch116。
14. **`memory_order` 各档语义与硬件映射？** ch108、ch109。
15. **无锁队列如何避免 ABA？** 带标记指针/hazard pointer，ch111、ch112。
16. **CRTP 与静态多态实战？** ch57、ch73。
17. **SFINAE vs Concepts？** ch66、ch67。
18. **`constexpr` 与编译期计算边界？** ch69。
19. **`std::string` SSO 与 COW 历史？** COW 因 C++11 多线程被弃，SSO 主流，ch81。
20. **异常安全三等级？** 基本/强/不抛，ch49。

## 公司专项
### Google
- 强调代码风格、测试、简洁。`std::sort` 复杂度？`unique_ptr` 零开销？见 ch96、ch48。
- 常问：大规模 C++ 构建（头文件/模块）、ch118、ch144。

### Meta
- 性能与并发：无锁、缓存、内存序，ch110–ch112、ch44。

### 腾讯 / 字节
- 偏基础扎实：虚表、对象布局、STL 实现、智能指针、移动语义，ch54、ch77、ch48、ch115。
- 项目深挖：你写的网络库/线程池设计，ch159、ch163。

### 微软
- MSVC/Win32/ABI：`__declspec`、`COM`、异常模型，ch11、ch54（vtable 与 COM 类似）。

### 高频真题
- 「`sizeof` 空类为什么是 1？」ch58
- 「`i++ + ++i` 为什么 UB？」ch34
- 「`reserve` 能否缩小容量？」ch77
- 「`shared_ptr` 循环引用？」ch48（weak_ptr 解）
- 「`std::sort` 用快排还是什么？」Introsort，ch96

---
*按初级/中级/高级/公司持续扩充。每条链章节与误区库。*
