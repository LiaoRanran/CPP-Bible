---
id: MIS-PERF-005
name: 到处贴 [[likely]] 总能提速
level: deep
domain: PERF
trigger_patterns:
  - "把热分支标上 likely 就快了"
  - "likely 是免费优化"
refutations:
  - "[[likely]] 只调整布局与预测提示，不消除分支；数据分布均匀时会误导预测器甚至变慢"
  - "真正去分支要改写为无分支算法，而后者也可能更慢（见 MIS-PERF-004）"
source: ch153_cpu_micro.md ⑯
related_atoms: []
---

# MIS-PERF-005 · 到处贴 [[likely]] 总能提速

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏（认知科学依据：一次纠正不够）

## 触发模式（学习者常这么说 / 这么写）
- 把热分支标上 likely 就快了
- likely 是免费优化

## 为什么它不成立
1. [[likely]] 只调整布局与预测提示，不消除分支；数据分布均匀时会误导预测器甚至变慢
2. 真正去分支要改写为无分支算法，而后者也可能更慢（见 MIS-PERF-004）

## 出处与关联

- 出处：ch153_cpu_micro.md ⑯
- 关联原子：（暂无，待相关原子锻造后回填）
