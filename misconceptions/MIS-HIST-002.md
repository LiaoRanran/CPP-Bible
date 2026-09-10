---
id: MIS-HIST-002
name: auto_ptr 反正被移除了，C++17 里编译不过
level: surface
domain: HIST
trigger_patterns:
  - "C++17 起 auto_ptr 就没了，肯定编译失败"
  - "标准移除等于实现删除"
refutations:
  - "实测 GCC 15.3 的 libstdc++ 在 -std=c++14/17/23 三档**均仍提供** auto_ptr（<backward/auto_ptr.h>）"
  - "libc++ / MSVC 才是真移除 → 构成可移植性陷阱（在 GCC 上看着还能用，换工具链即断）"
source: 三样板 C（三档实测）
related_atoms: [ATOM-HIST-AUTOPTR-001]
---

# MIS-HIST-002 · auto_ptr 反正被移除了，C++17 里编译不过

**层级**：surface —— 表层误解，一次纠正即可

## 触发模式（学习者常这么说 / 这么写）
- C++17 起 auto_ptr 就没了，肯定编译失败
- 标准移除等于实现删除

## 为什么它不成立
1. 实测 GCC 15.3 的 libstdc++ 在 -std=c++14/17/23 三档**均仍提供** auto_ptr（<backward/auto_ptr.h>）
2. libc++ / MSVC 才是真移除 → 构成可移植性陷阱（在 GCC 上看着还能用，换工具链即断）

## 出处与关联

- 出处：三样板 C（三档实测）
- 关联原子：ATOM-HIST-AUTOPTR-001
