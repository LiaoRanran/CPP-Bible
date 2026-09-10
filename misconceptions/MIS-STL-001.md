---
id: MIS-STL-001
name: 只有 erase（删除）才会让迭代器失效，插入不会
level: deep
domain: STL
trigger_patterns:
  - "我只是 push_back，原来的迭代器还能用"
  - "insert 不影响已有迭代器"
refutations:
  - "vector 插入可能触发重分配 → **全部**迭代器/引用/指针失效；不重分配时插入点之后的也失效"
  - "各容器失效规则不同（list 插入不失效，deque 插入使全部失效），须逐容器查"
source: ch76_stl_arch.md ⑯ 易错点；ch77_vector.md ⑯
related_atoms: []
---

# MIS-STL-001 · 只有 erase（删除）才会让迭代器失效，插入不会

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏（认知科学依据：一次纠正不够）

## 触发模式（学习者常这么说 / 这么写）
- 我只是 push_back，原来的迭代器还能用
- insert 不影响已有迭代器

## 为什么它不成立
1. vector 插入可能触发重分配 → **全部**迭代器/引用/指针失效；不重分配时插入点之后的也失效
2. 各容器失效规则不同（list 插入不失效，deque 插入使全部失效），须逐容器查

## 出处与关联

- 出处：ch76_stl_arch.md ⑯ 易错点；ch77_vector.md ⑯
- 关联原子：（暂无，待相关原子锻造后回填）
