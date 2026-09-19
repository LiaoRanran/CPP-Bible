# ATOM-MEM-SHARED-001（atom_claim）

## 正面

【MEM】ATOM-MEM-SHARED-001
以下论断是否成立？依据是什么？
std::shared_ptr<T> 用引用计数实现共享所有权：拷贝 +1、析构 -1，计数归零才释放资源（析构恰好一次）。 控制块（RAII）管理计数与资源。但它不能自动处理循环引用——两个对象互相 shared_ptr 持有，彼此计数 为 2，离开作用域后各减到 1 仍互指，计数永不归零 => 泄漏；循环必须用 weak_ptr 打破。

## 背面

论断：std::shared_ptr<T> 用引用计数实现共享所有权：拷贝 +1、析构 -1，计数归零才释放资源（析构恰好一次）。 控制块（RAII）管理计数与资源。但它不能自动处理循环引用——两个对象互相 shared_ptr 持有，彼此计数 为 2，离开作用域后各减到 1 仍互指，计数永不归零 => 泄漏；循环必须用 weak_ptr 打破。
边界：{'standard': ['C++11', 'C++14', 'C++17', 'C++20', 'C++23'], 'compilers': ['GCC 15.3.0'], 'opt': ['-O2'], 'platform': ['x86-64 MinGW-w64']}
关键证据：
  - EV-MEM-013: confirm
  - EV-MEM-014: confirm
