# MIS-MEM-023（misconception）

## 正面

【误解】MIS-MEM-023 SSO 阈值所有编译器都一样（实现差异不可移植）
触发说法：短字符串的优化阈值是 C++ 标准规定的

## 背面

为什么错：本机实测 EV-MEM-029/031：libstdc++（GCC 15.3.0）SSO 容量 15（sizeof=32）；而 libc++（Clang）为 22 字符（sizeof=24）、MSVC 为 15 字符（sizeof=32）——三实现布局不同（union 设计各异），阈值是实现细节，标准只保证 string 语义、根本不要求 SSO 存在
反例 1：写死阈值的代码不可移植且脆弱：阈值随实现/版本可变（标准不承诺），依赖'15 字符内零分配'的性能假设必须实测目标平台（EV-MEM-029 的扫描方法可直接搬用；见 ATOM-MEM-PERF-002 / EV-MEM-031 三实现布局对比）
关联原子：ATOM-MEM-PERF-002 ATOM-MEM-ALLOC-001
