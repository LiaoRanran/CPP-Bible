---
id: MIS-CONC-005
name: 无锁一定比 mutex 快
level: deep
domain: CONC
trigger_patterns:
  - "lock-free 更高级，肯定更快"
  - "CAS 比加锁便宜"
refutations:
  - "低中竞争 + 短临界区下 mutex（用户态自旋 + futex）常更快；无锁的收益在高竞争且临界区极短时才显现"
  - "必须基准测试；无锁还带来 ABA、内存回收等额外复杂度"
source: ch110_lockfree.md ⑮ 何时用无锁
related_atoms: []
---

# MIS-CONC-005 · 无锁一定比 mutex 快

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏（认知科学依据：一次纠正不够）

## 触发模式（学习者常这么说 / 这么写）
- lock-free 更高级，肯定更快
- CAS 比加锁便宜

## 为什么它不成立
1. 低中竞争 + 短临界区下 mutex（用户态自旋 + futex）常更快；无锁的收益在高竞争且临界区极短时才显现
2. 必须基准测试；无锁还带来 ABA、内存回收等额外复杂度

## 出处与关联

- 出处：ch110_lockfree.md ⑮ 何时用无锁
- 关联原子：（暂无，待相关原子锻造后回填）
