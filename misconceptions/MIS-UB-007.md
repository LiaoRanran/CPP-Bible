---
id: MIS-UB-007
name: 读未初始化的变量只是拿到一个垃圾值，不算 UB
level: deep
domain: UB
trigger_patterns:
  - "未初始化的 int 读出来是个随机数而已"
  - "反正后面会赋值"
refutations:
  - "读取不确定值是 UB（陷阱表示亦在此列），优化器可假设它取任意值并据此删分支"
  - "结构体 padding 读取同理：即使用 memset 比较也会因 padding 不确定而失败"
source: ch28_lifetime_ub.md ⑫
related_atoms: []
---

# MIS-UB-007 · 读未初始化的变量只是拿到一个垃圾值，不算 UB

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏（认知科学依据：一次纠正不够）

## 触发模式（学习者常这么说 / 这么写）
- 未初始化的 int 读出来是个随机数而已
- 反正后面会赋值

## 为什么它不成立
1. 读取不确定值是 UB（陷阱表示亦在此列），优化器可假设它取任意值并据此删分支
2. 结构体 padding 读取同理：即使用 memset 比较也会因 padding 不确定而失败

## 出处与关联

- 出处：ch28_lifetime_ub.md ⑫
- 关联原子：（暂无，待相关原子锻造后回填）
