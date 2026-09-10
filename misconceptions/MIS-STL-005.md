---
id: MIS-STL-005
name: reserve(n) 之后 capacity() 恰好等于 n
level: surface
domain: STL
trigger_patterns:
  - "reserve(100) 后 capacity 就是 100"
  - "容量精确等于我申请的"
refutations:
  - "标准只保证 capacity() **至少** n，实现可给更大（如按 2 的幂向上取整）"
source: ch77_vector.md ⑰ FAQ
related_atoms: []
---

# MIS-STL-005 · reserve(n) 之后 capacity() 恰好等于 n

**层级**：surface —— 表层误解，一次纠正即可

## 触发模式（学习者常这么说 / 这么写）
- reserve(100) 后 capacity 就是 100
- 容量精确等于我申请的

## 为什么它不成立
1. 标准只保证 capacity() **至少** n，实现可给更大（如按 2 的幂向上取整）

## 出处与关联

- 出处：ch77_vector.md ⑰ FAQ
- 关联原子：（暂无，待相关原子锻造后回填）
