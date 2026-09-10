---
id: MIS-CONC-002
name: memory_order_relaxed 可以当数据已就绪的标志位用
level: deep
domain: CONC
trigger_patterns:
  - "用 relaxed 的 flag 表示数据写完了"
  - "relaxed 只是不保证顺序，但值能看到"
refutations:
  - "relaxed 只保证原子性，不建立同步关系 → 读线程可能看到 flag 为真却读到未初始化的数据"
  - "发布-订阅要用 release/acquire 配对（或 seq_cst）"
source: ch108_memory_order.md ⑯ 误用案例
related_atoms: []
---

# MIS-CONC-002 · memory_order_relaxed 可以当数据已就绪的标志位用

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏（认知科学依据：一次纠正不够）

## 触发模式（学习者常这么说 / 这么写）
- 用 relaxed 的 flag 表示数据写完了
- relaxed 只是不保证顺序，但值能看到

## 为什么它不成立
1. relaxed 只保证原子性，不建立同步关系 → 读线程可能看到 flag 为真却读到未初始化的数据
2. 发布-订阅要用 release/acquire 配对（或 seq_cst）

## 出处与关联

- 出处：ch108_memory_order.md ⑯ 误用案例
- 关联原子：（暂无，待相关原子锻造后回填）
