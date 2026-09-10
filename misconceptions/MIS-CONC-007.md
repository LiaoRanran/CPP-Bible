---
id: MIS-CONC-007
name: 原子操作省略内存序参数时默认是 relaxed
level: surface
domain: CONC
trigger_patterns:
  - "不写内存序就是最松的"
  - "默认 relaxed 性能好"
refutations:
  - "默认（以及 ++/--/赋值等运算符重载）是 **memory_order_seq_cst**，即最强顺序一致"
source: ch108_memory_order.md ⑱
related_atoms: []
---

# MIS-CONC-007 · 原子操作省略内存序参数时默认是 relaxed

**层级**：surface —— 表层误解，一次纠正即可

## 触发模式（学习者常这么说 / 这么写）
- 不写内存序就是最松的
- 默认 relaxed 性能好

## 为什么它不成立
1. 默认（以及 ++/--/赋值等运算符重载）是 **memory_order_seq_cst**，即最强顺序一致

## 出处与关联

- 出处：ch108_memory_order.md ⑱
- 关联原子：（暂无，待相关原子锻造后回填）
