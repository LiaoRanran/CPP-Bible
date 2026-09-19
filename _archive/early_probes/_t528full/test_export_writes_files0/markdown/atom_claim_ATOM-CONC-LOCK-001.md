# ATOM-CONC-LOCK-001（atom_claim）

## 正面

【conc】ATOM-CONC-LOCK-001
以下论断是否成立？依据是什么？
高竞争下 CAS 的原子 RMW 代价可能超过 mutex；但该结论依赖核数与竞争度，≤2 核环境可能反向—— 锁与无锁各有适用域，无绝对最优。

## 背面

论断：高竞争下 CAS 的原子 RMW 代价可能超过 mutex；但该结论依赖核数与竞争度，≤2 核环境可能反向—— 锁与无锁各有适用域，无绝对最优。
边界：{'standard': ['C++11', 'C++14', 'C++17', 'C++20', 'C++23'], 'compilers': ['GCC 15.3.0 (MinGW-w64)', 'GCC 14.2.0 (WSL)', 'GCC 13.3.0 (WSL)'], 'opt': ['-O2'], 'platform': ['x86-64']}
关键证据：
  - EV-CONC-003: confirm
  - EV-CONC-004: confirm
常见误解：
  - 误以为 atomic 是零代价、无锁一定比 mutex 快
  - 误以为 CAS 无锁就一定优于 mutex：高竞争下 CAS 重试风暴使其代价反超 mutex
  - MIS-CONC-002
