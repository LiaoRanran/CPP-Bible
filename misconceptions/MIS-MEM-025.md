---
id: MIS-MEM-025
name: "unique_ptr<T[]> 只是 unique_ptr<T> 的语法糖"
level: surface
domain: MEM
trigger_patterns:
  - "数组版本就是把类型写成 T[]，没别的区别"
  - "unique_ptr<int> p(new int[8]) 一样能用，析构会自动处理"
refutations:
  - "接口不同：实测 EV-MEM-032 编译期 trait——`unique_ptr<int[]>` 有 operator[]（subscript=1）但**没有** operator* 与 operator->（deref=0 arrow=0）；对象特化恰好相反。这不是风格差异，是两套不同的接口约束"
  - "释放路径不同：`unique_ptr<int[]>` 走 delete[]（operator delete[] 计数=1），而 `unique_ptr<int>` 路径的 delete[] 增量为 0——两者调用的释放函数根本不是同一个"
  - "配对律：`new int[8]` 必须配 delete[]；用 `unique_ptr<int>` 接 `new int[]` 会让析构走 delete，属 UB（数组 Cookie 与元素析构都不会被正确处理）"
source: G5 第三批指令（UNIQUE-002）；ATOM-MEM-UNIQUE-002 / EV-MEM-032
related_atoms: [ATOM-MEM-UNIQUE-002, ATOM-MEM-NEW-001]
---

# MIS-MEM-025 · "unique_ptr<T[]> 只是 unique_ptr<T> 的语法糖"

**层级**：surface —— 表述层误解：把 T[] 当成"写法的微调"，纠正成本低，但若按此写代码会直接踩 UB。

## 触发模式（学习者常这么说 / 这么写）
- "数组版本就是把类型写成 T[]，没别的区别"
- "unique_ptr<int> p(new int[8]) 一样能用，析构会自动处理"

## 为什么它不成立
1. 接口不同：实测 EV-MEM-032 编译期 trait——`unique_ptr<int[]>` 有 operator[]（subscript=1）但**没有** operator* 与 operator->（deref=0 arrow=0）；对象特化恰好相反。这不是风格差异，是两套不同的接口约束
2. 释放路径不同：`unique_ptr<int[]>` 走 delete[]（operator delete[] 计数=1），而 `unique_ptr<int>` 路径的 delete[] 增量为 0——两者调用的释放函数根本不是同一个
3. 配对律：`new int[8]` 必须配 delete[]；用 `unique_ptr<int>` 接 `new int[]` 会让析构走 delete，属 UB（数组 Cookie 与元素析构都不会被正确处理）

## 正确理解
- `T[]` 触发的是**特化**（独立类模板），不是"同一个类换个拼写"：它同时改掉接口（只给 `operator[]`）与删除器默认类型（`default_delete<T[]>` ⇒ `delete[]`）。
- 判据：**用 new[] 分配就必须用能调 delete[] 的所有权载体**——`unique_ptr<T[]>`、容器，或自己在删除器里写 delete[]。

## 出处与关联
- 出处：G5 第三批指令（UNIQUE-002）；ATOM-MEM-UNIQUE-002 / EV-MEM-032
- 关联原子：ATOM-MEM-UNIQUE-002、ATOM-MEM-NEW-001
