# ATOM-MEM-PERF-004（atom_claim）

## 正面

【MEM】ATOM-MEM-PERF-004
以下论断是否成立？依据是什么？
多线程各自读写**逻辑独立**的变量时仍可能因共享缓存行（false sharing）付出约一个数量级的性能代价 ——本机实测 4 线程各累加 1e7 次：相邻布局中位数 562500600 ns vs `alignas` 隔离后 29824800 ns （**18.86×**，Linux 同夹具 18.54×，方向一致）；该结构前提可用地址**确定性判定** （`tight_same_line=1` / `padded_same_line=0`，不依赖计时），而 padding 的代价是空间 （`padded_sizeof=128`）⇒ 存在最优对齐粒度，"padding 一定值得"同样是过度概括。

## 背面

论断：多线程各自读写**逻辑独立**的变量时仍可能因共享缓存行（false sharing）付出约一个数量级的性能代价 ——本机实测 4 线程各累加 1e7 次：相邻布局中位数 562500600 ns vs `alignas` 隔离后 29824800 ns （**18.86×**，Linux 同夹具 18.54×，方向一致）；该结构前提可用地址**确定性判定** （`tight_same_line=1` / `padded_same_line=0`，不依赖计时），而 padding 的代价是空间 （`padded_sizeof=128`）⇒ 存在最优对齐粒度，"padding 一定值得"同样是过度概括。
边界：{'standard': ['C++11', 'C++17', 'C++20', 'C++23'], 'compilers': ['GCC 15.3.0 (MinGW-w64)', 'GCC 14.2.0 (WSL)'], 'opt': ['-O2'], 'platform': ['x86-64，缓存行 64 字节']}
关键证据：
  - EV-MEM-044: confirm
  - EV-MEM-045: confirm
常见误解：
  - MIS-MEM-032
