---
id: MIS-MEM-028
name: "sizeof(std::string) 到处都是 32 字节（把某一实现的布局当语言事实）"
level: deep
domain: MEM
trigger_patterns:
  - "std::string 就是 32 字节，指针 8 + 大小 8 + SSO 缓冲 16"
  - "跨平台传 std::string 没事，反正大小固定"
  - "sizeof 是编译期常量，所以各平台一样"
refutations:
  - "实测同一份夹具（判据 = 数据指针是否落在对象自身字节范围内）：libstdc++（GCC 15.3.0 MinGW + GCC 14.2.0 WSL）`sizeof_string=32`，libc++（libc++-18，WSL）`sizeof_string=24` —— 差 8 字节，而两者都**完全符合** [string] 的要求"
  - "标准只约束可观察行为，不约束对象布局：[string] 未规定 sizeof、未规定 SSO 是否存在、更未规定其容量；32 这个数字来自 libstdc++ 把 `size + capacity + 16 字节缓冲` 打包成 3 个 8 字节字的**实现选择**，不是 [string] 的条文"
  - "推论随之崩塌：被 32 掩盖的两件事——(a) 布局跨 ABI 不兼容（把 GCC 编出的 string 交给 Clang/libc++ 编的代码析构，是按错误布局解释内存）；(b) SSO 容量跟着变（libstdc++ 15 vs libc++ 22，见 MIS-MEM-029）"
source: G5 第四批指令（PERF-003）；ATOM-MEM-PERF-003 / ATOM-MEM-PERF-002；EV-MEM-038 实测（libstdc++ 32 / libc++ 24）
related_atoms: [ATOM-MEM-PERF-003, ATOM-MEM-PERF-002, ATOM-MEM-ALLOC-001]
---

# MIS-MEM-028 · "sizeof(std::string) 到处都是 32 字节"

**层级**：deep —— 它不是记错一个数字，而是把**实现参数**误当**语言保证**。后果不止"预期落空"：一旦据此跨 ABI 传递 `std::string`（或写死缓冲偏移做内存操作），得到的是**未定义行为**，而代码在任何单一平台上都"看着没问题"。

## 触发模式（学习者常这么说 / 这么写）
- "std::string 就是 32 字节，指针 8 + 大小 8 + SSO 缓冲 16"
- "跨平台传 std::string 没事，反正大小固定"
- "sizeof 是编译期常量，所以各平台一样"

## 为什么它不成立
1. **实测两个实现差 8 字节**：同一份夹具（判据 = 数据指针是否落在对象自身字节范围内）——libstdc++（GCC 15.3.0 MinGW + GCC 14.2.0 WSL）`sizeof_string=32`；libc++（libc++-18，WSL）`sizeof_string=24`；而两者都**完全符合** [string] 的要求
2. **标准不约束布局**：[string] 只约束可观察行为，未规定 `sizeof`、未规定 SSO 是否存在、更未规定其容量。32 这个数字来自 libstdc++ 把"size + capacity + 16 字节缓冲"打包成 3 个 8 字节字的**实现选择**，不是条文
3. **推论随之崩塌**：(a) 布局跨 ABI 不兼容——把 GCC 编出的 `std::string` 交给 libc++ 编的代码析构，是按错误布局解释内存（UB）；(b) SSO 容量跟着变（15 vs 22，见 MIS-MEM-029）

## 正确理解
- **判据**：问"这个数字是标准写的，还是我的标准库选的？"——`sizeof`、SSO 阈值、`capacity()`、`data()` 的地址归属全都属于后者
- 工程做法：跨 ABI 边界的字符串用 `const char*` + 长度（或双方约定的序列化），**永不**跨 ABI 传 `std::string`；需要布局保证时用 `std::array<char, N>` 之类的语言级保证
- 一条可复用自检：**"我的断言在换一个标准库后还成立吗？"**——不成立的数字，写进代码就是把实现细节当契约

## 出处与关联
- 出处：G5 第四批指令（PERF-003）；ATOM-MEM-PERF-003 / ATOM-MEM-PERF-002；EV-MEM-038 实测（libstdc++ 32 / libc++ 24）
- 关联原子：ATOM-MEM-PERF-003、ATOM-MEM-PERF-002、ATOM-MEM-ALLOC-001
