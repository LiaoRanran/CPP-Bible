# ATOM-MEM-RAII-001（atom_claim）

## 正面

【MEM】ATOM-MEM-RAII-001
以下论断是否成立？依据是什么？
RAII 的核心是"资源生命周期绑定到对象生命周期"：构造时获取资源、析构时释放。栈展开时（即使函数 因异常提前返回）作用域内对象的析构按构造逆序自动调用，因此 RAII 管理的资源在异常路径也不泄漏； 裸 new/delete 在异常路径跳过 delete 则泄漏。lock_guard、unique_ptr、vector 都是 RAII。

## 背面

论断：RAII 的核心是"资源生命周期绑定到对象生命周期"：构造时获取资源、析构时释放。栈展开时（即使函数 因异常提前返回）作用域内对象的析构按构造逆序自动调用，因此 RAII 管理的资源在异常路径也不泄漏； 裸 new/delete 在异常路径跳过 delete 则泄漏。lock_guard、unique_ptr、vector 都是 RAII。
边界：{'standard': ['C++11', 'C++14', 'C++17', 'C++20', 'C++23'], 'compilers': ['GCC 15.3.0'], 'opt': ['-O2'], 'platform': ['x86-64 MinGW-w64']}
关键证据：
  - EV-MEM-009: confirm
  - EV-MEM-010: confirm
