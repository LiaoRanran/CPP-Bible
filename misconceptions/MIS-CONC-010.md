---
id: MIS-CONC-010
name: 函数内 static 变量初始化线程安全，所以读写也线程安全
level: deep
domain: CONC
trigger_patterns:
  - "局部 static 初始化有守卫，多线程访问也安全"
  - "magic static 保证了一切"
refutations:
  - "标准只保证**初始化**不发生数据竞争（magic static）；初始化之后的并发读写仍需自行同步"
  - "同理 thread_local 在线程池复用线程时不会自动重置，须在任务入口手动重置"
source: ch19_variables.md ⑯ 易错点（static 语义簇 / 线程模型簇）
related_atoms: []
---

# MIS-CONC-010 · 函数内 static 变量初始化线程安全，所以读写也线程安全

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏（认知科学依据：一次纠正不够）

## 触发模式（学习者常这么说 / 这么写）
- 局部 static 初始化有守卫，多线程访问也安全
- magic static 保证了一切

## 为什么它不成立
1. 标准只保证**初始化**不发生数据竞争（magic static）；初始化之后的并发读写仍需自行同步
2. 同理 thread_local 在线程池复用线程时不会自动重置，须在任务入口手动重置

## 出处与关联

- 出处：ch19_variables.md ⑯ 易错点（static 语义簇 / 线程模型簇）
- 关联原子：（暂无，待相关原子锻造后回填）
