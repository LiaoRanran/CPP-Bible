---
id: MIS-PERF-002
name: for (auto x : vec) 不会拷贝元素
level: surface
domain: PERF
trigger_patterns:
  - "auto 自动推导，不会拷贝"
  - "范围 for 很省"
refutations:
  - "按值 auto x 会拷贝每个元素；只读应写 const auto&（-Wrange-loop-construct 可告警）"
source: ch158_perf_antipatterns.md ㉒.3
related_atoms: []
---

# MIS-PERF-002 · for (auto x : vec) 不会拷贝元素

**层级**：surface —— 表层误解，一次纠正即可

## 触发模式（学习者常这么说 / 这么写）
- auto 自动推导，不会拷贝
- 范围 for 很省

## 为什么它不成立
1. 按值 auto x 会拷贝每个元素；只读应写 const auto&（-Wrange-loop-construct 可告警）

## 出处与关联

- 出处：ch158_perf_antipatterns.md ㉒.3
- 关联原子：（暂无，待相关原子锻造后回填）
