---
id: MIS-STL-010
name: span / string_view 拥有数据，可以返回函数内新建的数据
level: deep
domain: STL
trigger_patterns:
  - "返回 string_view 比返回 string 轻量，直接这么写"
  - "span 持有它的元素"
refutations:
  - "span/string_view 是**非拥有**视图，只借用；返回指向局部缓冲的视图即悬垂 → UB"
  - "底层容器扩容后，先前取的 span 也会失效（vector 重分配）"
source: ch82_span.md ⑯ 易错点 1/2/4
related_atoms: []
---

# MIS-STL-010 · span / string_view 拥有数据，可以返回函数内新建的数据

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏（认知科学依据：一次纠正不够）

## 触发模式（学习者常这么说 / 这么写）
- 返回 string_view 比返回 string 轻量，直接这么写
- span 持有它的元素

## 为什么它不成立
1. span/string_view 是**非拥有**视图，只借用；返回指向局部缓冲的视图即悬垂 → UB
2. 底层容器扩容后，先前取的 span 也会失效（vector 重分配）

## 出处与关联

- 出处：ch82_span.md ⑯ 易错点 1/2/4
- 关联原子：（暂无，待相关原子锻造后回填）
