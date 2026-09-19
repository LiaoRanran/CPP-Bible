# ATOM-MEM-LEAK-001（atom_claim）

## 正面

【MEM】ATOM-MEM-LEAK-001
以下论断是否成立？依据是什么？
内存泄漏的机器检测信号分三层且强度不同——进程退出码与 stderr **不携带**泄漏信号（泄漏进程照常 `return 0`、无任何错误输出），夹具内 volatile 析构计数与控制块 `use_count()` 是**不依赖 sanitizer 环境**的确定信号，而 ASan/LSan 的判定**对优化档与对象存活位置高度敏感**（同一泄漏：`-O0` 极简环报 80 B/2 次分配、同档树形不报、`noinline` 隔离后 `-O2` 树形报 224 B/4 次分配、而 `-O2` 极简环不报） ——因此"ASan 没报"不能推出"没泄漏"。

## 背面

论断：内存泄漏的机器检测信号分三层且强度不同——进程退出码与 stderr **不携带**泄漏信号（泄漏进程照常 `return 0`、无任何错误输出），夹具内 volatile 析构计数与控制块 `use_count()` 是**不依赖 sanitizer 环境**的确定信号，而 ASan/LSan 的判定**对优化档与对象存活位置高度敏感**（同一泄漏：`-O0` 极简环报 80 B/2 次分配、同档树形不报、`noinline` 隔离后 `-O2` 树形报 224 B/4 次分配、而 `-O2` 极简环不报） ——因此"ASan 没报"不能推出"没泄漏"。
边界：{'standard': ['C++11', 'C++14', 'C++17', 'C++20', 'C++23'], 'compilers': ['GCC 15.3.0'], 'sanitizer_env': ['WSL Ubuntu g++-14.2', '-std=c++23', '-fsanitize=address', 'undefined', 'ASAN_OPTIONS 默认'], 'opt': ['-O0', '-O1', '-O2'], 'platform': ['x86-64 MinGW-w64（运行层）; x86-64 Linux（sanitizer 层）']}
关键证据：
  - EV-MEM-036: confirm
  - EV-MEM-037: confirm
