---
id: MIS-CONC-003
name: std::atomic<T> 对任何类型都是无锁的
level: deep
domain: CONC
trigger_patterns:
  - "atomic 就是无锁的，比 mutex 快"
  - "atomic<大结构体> 也能用"
refutations:
  - "超过平台支持宽度（通常 8/16 字节）的 atomic 会退化为内部加锁（is_lock_free() 为 false）"
  - "大对象同步应该用 mutex，不要塞进 atomic"
source: ch107_atomic.md ⑯ 常见误用
related_atoms: []
---

# MIS-CONC-003 · std::atomic<T> 对任何类型都是无锁的

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏（认知科学依据：一次纠正不够）

## 触发模式（学习者常这么说 / 这么写）
- atomic 就是无锁的，比 mutex 快
- atomic<大结构体> 也能用

## 为什么它不成立
1. 超过平台支持宽度（通常 8/16 字节）的 atomic 会退化为内部加锁（is_lock_free() 为 false）
2. 大对象同步应该用 mutex，不要塞进 atomic

## 出处与关联

- 出处：ch107_atomic.md ⑯ 常见误用
- 关联原子：（暂无，待相关原子锻造后回填）
