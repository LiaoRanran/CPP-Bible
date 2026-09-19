# ATOM-MEM-ALIGN-001（atom_claim）

## 正面

【MEM】ATOM-MEM-ALIGN-001
以下论断是否成立？依据是什么？
每个类型有对齐要求；结构体成员按自身对齐排列，编译器在成员间/末尾插入 padding，使每个成员与整体满足对齐， sizeof 包含 padding（故通常 > 各成员大小之和）。alignas 可提升对齐、alignof 查询对齐；搬运结构体用 按字节 memcpy（安全），用 reinterpret_cast 强转指针对齐/类型双关是未定义行为。

## 背面

论断：每个类型有对齐要求；结构体成员按自身对齐排列，编译器在成员间/末尾插入 padding，使每个成员与整体满足对齐， sizeof 包含 padding（故通常 > 各成员大小之和）。alignas 可提升对齐、alignof 查询对齐；搬运结构体用 按字节 memcpy（安全），用 reinterpret_cast 强转指针对齐/类型双关是未定义行为。
边界：{'standard': ['C++11', 'C++14', 'C++17', 'C++20', 'C++23'], 'compilers': ['GCC 15.3.0'], 'opt': ['-O2'], 'platform': ['x86-64 MinGW-w64']}
关键证据：
  - EV-MEM-019: confirm
  - EV-MEM-020: confirm
