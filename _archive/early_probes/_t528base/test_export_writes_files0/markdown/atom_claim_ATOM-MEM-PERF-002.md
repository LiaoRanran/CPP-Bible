# ATOM-MEM-PERF-002（atom_claim）

## 正面

【MEM】ATOM-MEM-PERF-002
以下论断是否成立？依据是什么？
SSO（Small String Optimization）：短于阈值的字符串存在 string 对象内部缓冲，零堆分配；达到阈值 才落堆——本机 libstdc++（GCC 15.3.0）阈值 15 字符、sizeof=32，len≤15 构造/拷贝 allocs=0（赋值 走同一实现路径），len=16 首次落堆。SSO 是实现内建（标准不要求），三实现参数不保证一致 （libstdc++ 32/15、libc++ 24/22、MSVC 32/15——libc++ 与另两家不同），阈值不可移植。历史： C++11 禁 COW 后 libstdc++ 才全面转向 SSO。

## 背面

论断：SSO（Small String Optimization）：短于阈值的字符串存在 string 对象内部缓冲，零堆分配；达到阈值 才落堆——本机 libstdc++（GCC 15.3.0）阈值 15 字符、sizeof=32，len≤15 构造/拷贝 allocs=0（赋值 走同一实现路径），len=16 首次落堆。SSO 是实现内建（标准不要求），三实现参数不保证一致 （libstdc++ 32/15、libc++ 24/22、MSVC 32/15——libc++ 与另两家不同），阈值不可移植。历史： C++11 禁 COW 后 libstdc++ 才全面转向 SSO。
边界：{'standard': ['C++11', 'C++14', 'C++17', 'C++20', 'C++23'], 'compilers': ['GCC 15.3.0'], 'opt': ['-O0', '-O2'], 'platform': ['x86-64 MinGW-w64']}
关键证据：
  - EV-MEM-029: confirm
  - EV-MEM-030: confirm
  - EV-MEM-031: confirm
