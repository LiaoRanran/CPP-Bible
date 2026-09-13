# ATOM-MEM-PERF-001（atom_claim）

## 正面

【MEM】ATOM-MEM-PERF-001
以下论断是否成立？依据是什么？
移动构造的收益来自"掏空源对象"：对持堆指针的类型只偷指针（sizeof(void*)=8 字节）并置空源、0 分配； 对无动态资源的纯值类型，移动 = 拷贝（同样搬全部字节、源不被掏空），std::move 无性能收益。

## 背面

论断：移动构造的收益来自"掏空源对象"：对持堆指针的类型只偷指针（sizeof(void*)=8 字节）并置空源、0 分配； 对无动态资源的纯值类型，移动 = 拷贝（同样搬全部字节、源不被掏空），std::move 无性能收益。
边界：{'standard': ['C++11', 'C++14', 'C++17', 'C++20', 'C++23'], 'compilers': ['GCC 15.3.0'], 'opt': ['-O0', '-O2'], 'platform': ['x86-64 MinGW-w64']}
关键证据：
  - EV-MEM-008: confirm
  - EV-MEM-001: confirm
  - EV-MEM-002: confirm
