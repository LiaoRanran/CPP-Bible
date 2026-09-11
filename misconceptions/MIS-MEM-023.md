---
id: MIS-MEM-023
name: "SSO 阈值所有编译器都一样（实现差异不可移植）"
level: deep
domain: MEM
trigger_patterns:
  - "短字符串的优化阈值是 C++ 标准规定的"
  - "15 字符以内不分配，哪个编译器都一样"
refutations:
  - "本机实测 EV-MEM-029/031：libstdc++（GCC 15.3.0）SSO 容量 15（sizeof=32）；而 libc++（Clang）为 22 字符（sizeof=24）、MSVC 为 15 字符（sizeof=32）——三实现布局不同（union 设计各异），阈值是实现细节，标准只保证 string 语义、根本不要求 SSO 存在"
  - "写死阈值的代码不可移植且脆弱：阈值随实现/版本可变（标准不承诺），依赖'15 字符内零分配'的性能假设必须实测目标平台（EV-MEM-029 的扫描方法可直接搬用；见 ATOM-MEM-PERF-002 / EV-MEM-031 三实现布局对比）"
source: References/32 G5 第二批指令 §一.4；ATOM-MEM-PERF-002 / EV-MEM-029 / EV-MEM-031
related_atoms: [ATOM-MEM-PERF-002, ATOM-MEM-ALLOC-001]
---

# MIS-MEM-023 · "SSO 阈值所有编译器都一样"（实现差异）

**层级**：deep —— 结构性误解，源于把实现优化当标准承诺、不了解三实现的 union 布局差异；须 ≥2 条独立反例才可能纠偏

## 触发模式（学习者常这么说 / 这么写）
- 短字符串的优化阈值是 C++ 标准规定的
- 15 字符以内不分配，哪个编译器都一样

## 为什么它不成立
1. 本机实测 EV-MEM-029/031：libstdc++（GCC 15.3.0）SSO 容量 15（sizeof=32）；而 libc++（Clang）为 22 字符（sizeof=24）、MSVC 为 15 字符（sizeof=32）——三实现布局不同（union 设计各异），阈值是实现细节，标准只保证 string 语义、根本不要求 SSO 存在
2. 写死阈值的代码不可移植且脆弱：阈值随实现/版本可变（标准不承诺），依赖"15 字符内零分配"的性能假设必须实测目标平台（EV-MEM-029 的扫描方法可直接搬用；见 ATOM-MEM-PERF-002 / EV-MEM-031 三实现布局对比）

## 出处与关联
- 出处：References/32 G5 第二批指令 §一.4；ATOM-MEM-PERF-002 / EV-MEM-029 / EV-MEM-031
- 关联原子：ATOM-MEM-PERF-002、ATOM-MEM-ALLOC-001
