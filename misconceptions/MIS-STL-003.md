---
id: MIS-STL-003
name: 用 map::operator[] 做只读存在性判断不会改动容器
level: deep
domain: STL
trigger_patterns:
  - "if (m[k]) 只是看看有没有"
  - "operator[] 只是读"
refutations:
  - "operator[] 对不存在的键会**插入**该键并值初始化 → 容器被改动、size 变化"
  - "只读查询用 find() / contains()（C++20）"
source: ch83_map.md ⑰ 易错点 1；ch101_algo_theory.md ⑯ 坑 1
related_atoms: []
---

# MIS-STL-003 · 用 map::operator[] 做只读存在性判断不会改动容器

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏（认知科学依据：一次纠正不够）

## 触发模式（学习者常这么说 / 这么写）
- if (m[k]) 只是看看有没有
- operator[] 只是读

## 为什么它不成立
1. operator[] 对不存在的键会**插入**该键并值初始化 → 容器被改动、size 变化
2. 只读查询用 find() / contains()（C++20）

## 出处与关联

- 出处：ch83_map.md ⑰ 易错点 1；ch101_algo_theory.md ⑯ 坑 1
- 关联原子：（暂无，待相关原子锻造后回填）
