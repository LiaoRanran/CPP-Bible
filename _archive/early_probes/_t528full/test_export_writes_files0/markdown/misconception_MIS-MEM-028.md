# MIS-MEM-028（misconception）

## 正面

【误解】MIS-MEM-028 sizeof(std::string) 到处都是 32 字节（把某一实现的布局当语言事实）
触发说法：std::string 就是 32 字节，指针 8 + 大小 8 + SSO 缓冲 16

## 背面

为什么错：实测同一份夹具（判据 = 数据指针是否落在对象自身字节范围内）：libstdc++（GCC 15.3.0 MinGW + GCC 14.2.0 WSL）`sizeof_string=32`，libc++（libc++-18，WSL）`sizeof_string=24` —— 差 8 字节，而两者都**完全符合** [string] 的要求
反例 1：标准只约束可观察行为，不约束对象布局：[string] 未规定 sizeof、未规定 SSO 是否存在、更未规定其容量；32 这个数字来自 libstdc++ 把 `size + capacity + 16 字节缓冲` 打包成 3 个 8 字节字的**实现选择**，不是 [string] 的条文
反例 2：推论随之崩塌：被 32 掩盖的两件事——(a) 布局跨 ABI 不兼容（把 GCC 编出的 string 交给 Clang/libc++ 编的代码析构，是按错误布局解释内存）；(b) SSO 容量跟着变（libstdc++ 15 vs libc++ 22，见 MIS-MEM-029）
关联原子：ATOM-MEM-PERF-003 ATOM-MEM-PERF-002 ATOM-MEM-ALLOC-001
