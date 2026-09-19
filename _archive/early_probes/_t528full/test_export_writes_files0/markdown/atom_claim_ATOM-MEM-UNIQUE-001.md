# ATOM-MEM-UNIQUE-001（atom_claim）

## 正面

【MEM】ATOM-MEM-UNIQUE-001
以下论断是否成立？依据是什么？
std::unique_ptr<T> 是唯一所有权智能指针：移动转移所有权（源被置空、目标获得对象），拷贝构造被删除 （不可共享），析构恰好 delete 一次（无双释放）。它是零开销抽象——sizeof 等于裸指针（x86-64 下 8 字节）， 所有权语义只体现在编译期（拷贝删除 + 移动转移），不在运行时加字段。禁用裸 new；需要共享才升级到 shared_ptr。

## 背面

论断：std::unique_ptr<T> 是唯一所有权智能指针：移动转移所有权（源被置空、目标获得对象），拷贝构造被删除 （不可共享），析构恰好 delete 一次（无双释放）。它是零开销抽象——sizeof 等于裸指针（x86-64 下 8 字节）， 所有权语义只体现在编译期（拷贝删除 + 移动转移），不在运行时加字段。禁用裸 new；需要共享才升级到 shared_ptr。
边界：{'standard': ['C++11', 'C++14', 'C++17', 'C++20', 'C++23'], 'compilers': ['GCC 15.3.0'], 'opt': ['-O2'], 'platform': ['x86-64 MinGW-w64']}
关键证据：
  - EV-MEM-011: confirm
  - EV-MEM-012: confirm
