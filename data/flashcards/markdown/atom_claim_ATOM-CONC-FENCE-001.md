# ATOM-CONC-FENCE-001（atom_claim）

## 正面

【conc】ATOM-CONC-FENCE-001
以下论断是否成立？依据是什么？
任何内存屏障（含零指令的 atomic_signal_fence）只要落在循环体内，就能阻止编译器消除该循环； 但屏障不提供数据竞争安全——屏障≠原子类型。

## 背面

论断：任何内存屏障（含零指令的 atomic_signal_fence）只要落在循环体内，就能阻止编译器消除该循环； 但屏障不提供数据竞争安全——屏障≠原子类型。
边界：{'standard': ['C++11', 'C++14', 'C++17', 'C++20', 'C++23'], 'compilers': ['GCC 15.3.0 (MinGW-w64)', 'GCC 14.2.0 (WSL)', 'GCC 13.3.0 (WSL)'], 'opt': ['-O2'], 'platform': ['x86-64']}
关键证据：
  - EV-CONC-001: confirm
  - EV-CONC-002: confirm
常见误解：
  - 误以为屏障（fence）能替代原子类型提供同步：给普通 int 标志加个 atomic_thread_fence 即可当线程间就绪标志用
  - 误以为屏障完全拦不住编译器消除（早期'屏障拦不住消除'说法方向说反）：实测零指令的 signal_fence 只要落在循环体内就能保住循环
  - MIS-CONC-001
