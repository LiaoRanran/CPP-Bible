# ATOM-MEM-NEW-001（atom_claim）

## 正面

【MEM】ATOM-MEM-NEW-001
以下论断是否成立？依据是什么？
new 表达式分两层：先 operator new 分配、再调用构造；delete 表达式也分两层：先调用析构、再 operator delete 释放。 两层各自独立发生一次。new[]/delete[] 针对数组，必须配对（混用是 UB）；new(std::nothrow) 在分配失败时返回 nullptr 而非抛异常；内置类型用 new 不初始化。裸 new 易漏 delete 而泄漏——优先容器/智能指针。

## 背面

论断：new 表达式分两层：先 operator new 分配、再调用构造；delete 表达式也分两层：先调用析构、再 operator delete 释放。 两层各自独立发生一次。new[]/delete[] 针对数组，必须配对（混用是 UB）；new(std::nothrow) 在分配失败时返回 nullptr 而非抛异常；内置类型用 new 不初始化。裸 new 易漏 delete 而泄漏——优先容器/智能指针。
边界：{'standard': ['C++11', 'C++14', 'C++17', 'C++20', 'C++23'], 'compilers': ['GCC 15.3.0'], 'opt': ['-O2'], 'platform': ['x86-64 MinGW-w64']}
关键证据：
  - EV-MEM-017: confirm
  - EV-MEM-018: confirm
