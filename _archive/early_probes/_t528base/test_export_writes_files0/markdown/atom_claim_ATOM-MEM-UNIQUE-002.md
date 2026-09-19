# ATOM-MEM-UNIQUE-002（atom_claim）

## 正面

【MEM】ATOM-MEM-UNIQUE-002
以下论断是否成立？依据是什么？
unique_ptr 的删除器是**类型的一部分**（`unique_ptr<T, D>` 的 D 进类型系统），因此删除器会影响 对象大小与类型：libstdc++ 下，空**且非 final** 的删除器被空基类优化吸收（sizeof == 裸指针 8 字节）， 而空但 final 的删除器与有状态删除器都必须存储（16 字节）——这是**实现边界**而非语言保证 （final 反例实测 16，见 EV-MEM-032）。数组特化 `unique_ptr<T[]>` 是独立特化：只提供 operator[]、 不提供 operator* 与 operator->，且在默认删除器下走 delete[]。与之对照，shared_ptr 的删除器被 **类型擦除**——语言层面不存在 `shared_ptr<T, D>`，删除器只能经构造函数按值注入并被控制块持有， 对象大小恒为两个指针、与删除器类型无关；代价是控制块自身的堆分配（裸指针构造 2 次分配、 make_shared 合并为 1 次，见 EV-MEM-033）。

## 背面

论断：unique_ptr 的删除器是**类型的一部分**（`unique_ptr<T, D>` 的 D 进类型系统），因此删除器会影响 对象大小与类型：libstdc++ 下，空**且非 final** 的删除器被空基类优化吸收（sizeof == 裸指针 8 字节）， 而空但 final 的删除器与有状态删除器都必须存储（16 字节）——这是**实现边界**而非语言保证 （final 反例实测 16，见 EV-MEM-032）。数组特化 `unique_ptr<T[]>` 是独立特化：只提供 operator[]、 不提供 operator* 与 operator->，且在默认删除器下走 delete[]。与之对照，shared_ptr 的删除器被 **类型擦除**——语言层面不存在 `shared_ptr<T, D>`，删除器只能经构造函数按值注入并被控制块持有， 对象大小恒为两个指针、与删除器类型无关；代价是控制块自身的堆分配（裸指针构造 2 次分配、 make_shared 合并为 1 次，见 EV-MEM-033）。
边界：{'standard': ['C++11', 'C++14', 'C++17', 'C++20', 'C++23'], 'compilers': ['GCC 15.3.0'], 'stdlib': ['libstdc++'], 'opt': ['-O0', '-O2'], 'platform': ['x86-64 MinGW-w64']}
关键证据：
  - EV-MEM-032: confirm
  - EV-MEM-033: confirm
