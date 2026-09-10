---
id: MIS-PERF-007
name: SoA 永远比 AoS 快
level: deep
domain: PERF
trigger_patterns:
  - "结构体拆成数组一定更快"
  - "SoA 是缓存优化的标准答案"
refutations:
  - "若每次访问都要用到对象的**全部**字段，AoS 的局部性反而更好（一次 cache line 拿全一个对象）"
  - "SoA 的收益只在'热循环只访问少数字段'时成立；须以 profile 数据为准"
source: ch154_cache_opt.md 设计取舍 AoS vs SoA
related_atoms: []
---

# MIS-PERF-007 · SoA 永远比 AoS 快

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏（认知科学依据：一次纠正不够）

## 触发模式（学习者常这么说 / 这么写）
- 结构体拆成数组一定更快
- SoA 是缓存优化的标准答案

## 为什么它不成立
1. 若每次访问都要用到对象的**全部**字段，AoS 的局部性反而更好（一次 cache line 拿全一个对象）
2. SoA 的收益只在'热循环只访问少数字段'时成立；须以 profile 数据为准

## 出处与关联

- 出处：ch154_cache_opt.md 设计取舍 AoS vs SoA
- 关联原子：（暂无，待相关原子锻造后回填）
