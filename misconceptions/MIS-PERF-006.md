---
id: MIS-PERF-006
name: 多插 __builtin_prefetch 一定更快
level: surface
domain: PERF
trigger_patterns:
  - "预取多加无害"
  - "prefetch 是纯赚的指令"
refutations:
  - "预取距离错了（太早被淘汰 / 太晚来不及）纯属浪费指令带宽，甚至挤占缓存"
source: ch154_cache_opt.md 反模式
related_atoms: []
---

# MIS-PERF-006 · 多插 __builtin_prefetch 一定更快

**层级**：surface —— 表层误解，一次纠正即可

## 触发模式（学习者常这么说 / 这么写）
- 预取多加无害
- prefetch 是纯赚的指令

## 为什么它不成立
1. 预取距离错了（太早被淘汰 / 太晚来不及）纯属浪费指令带宽，甚至挤占缓存

## 出处与关联

- 出处：ch154_cache_opt.md 反模式
- 关联原子：（暂无，待相关原子锻造后回填）
