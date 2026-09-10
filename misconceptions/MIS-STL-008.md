---
id: MIS-STL-008
name: std::sort 是稳定排序
level: surface
domain: STL
trigger_patterns:
  - "sort 会保持相等元素的原顺序"
  - "sort 和 stable_sort 差不多"
refutations:
  - "std::sort **不**保证稳定性（实现多为 introsort）；需要保持原序用 std::stable_sort"
source: ch96_sorting.md ⑩ 稳定性陷阱
related_atoms: []
---

# MIS-STL-008 · std::sort 是稳定排序

**层级**：surface —— 表层误解，一次纠正即可

## 触发模式（学习者常这么说 / 这么写）
- sort 会保持相等元素的原顺序
- sort 和 stable_sort 差不多

## 为什么它不成立
1. std::sort **不**保证稳定性（实现多为 introsort）；需要保持原序用 std::stable_sort

## 出处与关联

- 出处：ch96_sorting.md ⑩ 稳定性陷阱
- 关联原子：（暂无，待相关原子锻造后回填）
