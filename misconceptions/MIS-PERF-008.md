---
id: MIS-PERF-008
name: 编译器能自动向量化任何循环
level: surface
domain: PERF
trigger_patterns:
  - "开 -O3 就会自动 SIMD"
  - "循环自然会被向量化"
refutations:
  - "自动向量化要求无循环携带依赖、连续访存、可判定的别名；任一不满足即退化为标量"
  - "验证手段是 -fopt-info-vec，而不是假设"
source: ch155_simd.md ㉒.3
related_atoms: []
---

# MIS-PERF-008 · 编译器能自动向量化任何循环

**层级**：surface —— 表层误解，一次纠正即可

## 触发模式（学习者常这么说 / 这么写）
- 开 -O3 就会自动 SIMD
- 循环自然会被向量化

## 为什么它不成立
1. 自动向量化要求无循环携带依赖、连续访存、可判定的别名；任一不满足即退化为标量
2. 验证手段是 -fopt-info-vec，而不是假设

## 出处与关联

- 出处：ch155_simd.md ㉒.3
- 关联原子：（暂无，待相关原子锻造后回填）
