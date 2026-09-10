---
id: MIS-STL-006
name: set/multiset 的比较器写成 <= 也没问题
level: surface
domain: STL
trigger_patterns:
  - "用 <= 当比较器，反正能排"
  - "比较器随便写，能比出大小就行"
refutations:
  - "比较器必须满足**严格弱序**（irreflexive：comp(a,a) 必须为 false）；<= 违反该条 → UB"
source: ch84_set.md ⑯ 易错点（示例 8）
related_atoms: []
---

# MIS-STL-006 · set/multiset 的比较器写成 <= 也没问题

**层级**：surface —— 表层误解，一次纠正即可

## 触发模式（学习者常这么说 / 这么写）
- 用 <= 当比较器，反正能排
- 比较器随便写，能比出大小就行

## 为什么它不成立
1. 比较器必须满足**严格弱序**（irreflexive：comp(a,a) 必须为 false）；<= 违反该条 → UB

## 出处与关联

- 出处：ch84_set.md ⑯ 易错点（示例 8）
- 关联原子：（暂无，待相关原子锻造后回填）
