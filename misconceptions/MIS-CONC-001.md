---
id: MIS-CONC-001
name: volatile 可以用于线程间同步 / 当数据就绪标志
level: deep
domain: CONC
trigger_patterns:
  - "volatile bool ready 就能当标志位"
  - "volatile 保证可见性，够了"
refutations:
  - "volatile 只保证不被优化掉、不重排到同一线程内的 volatile 访问之外；**不**提供原子性、不提供跨线程 happens-before"
  - "线程同步要用 std::atomic 配内存序（默认 seq_cst）"
source: ch30_volatile.md ⑯ 五大误用 1；三样板 B
related_atoms: [ATOM-UB-GRAY-001]
---

# MIS-CONC-001 · volatile 可以用于线程间同步 / 当数据就绪标志

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏（认知科学依据：一次纠正不够）

## 触发模式（学习者常这么说 / 这么写）
- volatile bool ready 就能当标志位
- volatile 保证可见性，够了

## 为什么它不成立
1. volatile 只保证不被优化掉、不重排到同一线程内的 volatile 访问之外；**不**提供原子性、不提供跨线程 happens-before
2. 线程同步要用 std::atomic 配内存序（默认 seq_cst）

## 出处与关联

- 出处：ch30_volatile.md ⑯ 五大误用 1；三样板 B
- 关联原子：ATOM-UB-GRAY-001
