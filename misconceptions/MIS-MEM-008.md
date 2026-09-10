---
id: MIS-MEM-008
name: new/delete 与 new[]/delete[] 可以混用
level: surface
domain: MEM
trigger_patterns:
  - "delete 一个 new[] 出来的数组只是少调几个析构"
  - "反正都会把内存还回去"
refutations:
  - "混用是未定义行为：new[] 会在块头存元素个数，delete 按单对象布局释放 → 堆损坏"
source: ch37_new_delete.md 常见陷阱 1
related_atoms: []
---

# MIS-MEM-008 · new/delete 与 new[]/delete[] 可以混用

**层级**：surface —— 表层误解，一次纠正即可

## 触发模式（学习者常这么说 / 这么写）
- delete 一个 new[] 出来的数组只是少调几个析构
- 反正都会把内存还回去

## 为什么它不成立
1. 混用是未定义行为：new[] 会在块头存元素个数，delete 按单对象布局释放 → 堆损坏

## 出处与关联

- 出处：ch37_new_delete.md 常见陷阱 1
- 关联原子：（暂无，待相关原子锻造后回填）
