# ATOM-MEM-LEAK-002（atom_claim）

## 正面

【MEM】ATOM-MEM-LEAK-002
以下论断是否成立？依据是什么？
泄漏检测工具的**报告与否高度依赖被测代码的具体形态**，因此不能直接等价于泄漏有无： 同一份循环引用夹具、同一编译器与档位（WSL/Linux `-O1 -g -fsanitize=address,undefined`）， **改前**（无构造计数）LeakSanitizer **零报告**（stderr 0 字节），**改后**（仅给 `Node` 加一个 与泄漏无关的 `volatile` 构造计数）LSan **报告** `64 byte(s) leaked in 2 allocation(s)` （stderr 1258 字节）——唯一变量是一个与泄漏无关的计数器，且报告数值自洽（64 B = 2 × 32 B） ⇒ 判定泄漏应先用零依赖观测（构造/析构计数、存活对象数）定性，工具报告只作补充证据。

## 背面

论断：泄漏检测工具的**报告与否高度依赖被测代码的具体形态**，因此不能直接等价于泄漏有无： 同一份循环引用夹具、同一编译器与档位（WSL/Linux `-O1 -g -fsanitize=address,undefined`）， **改前**（无构造计数）LeakSanitizer **零报告**（stderr 0 字节），**改后**（仅给 `Node` 加一个 与泄漏无关的 `volatile` 构造计数）LSan **报告** `64 byte(s) leaked in 2 allocation(s)` （stderr 1258 字节）——唯一变量是一个与泄漏无关的计数器，且报告数值自洽（64 B = 2 × 32 B） ⇒ 判定泄漏应先用零依赖观测（构造/析构计数、存活对象数）定性，工具报告只作补充证据。
边界：{'standard': ['C++11', 'C++17', 'C++20', 'C++23'], 'compilers': ['GCC 15.3.0 (MinGW-w64)', 'GCC 14.2.0 (WSL)'], 'opt': ['-O1（sanitizer 观测档）', '-O2（零依赖判据档）'], 'platform': ['x86-64']}
关键证据：
  - EV-MEM-042: confirm
  - EV-MEM-043: confirm
常见误解：
  - MIS-MEM-031
