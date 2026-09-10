---
id: MIS-UB-002
name: 有符号整数溢出会像无符号一样回绕
level: deep
domain: UB
trigger_patterns:
  - "int 加到最大就变成负数，循环自然退出"
  - "溢出回绕是可预测的"
refutations:
  - "有符号溢出是 UB，无符号才是定义好的模运算——两者规则不同，不能类推"
  - "实测后果：GCC -O2 依此把 for (int i=0; i>=0; ++i) 编译成无条件 jmp 死循环"
source: ch28_lifetime_ub.md ⑪.1
related_atoms: [ATOM-UB-GRAY-001]
---

# MIS-UB-002 · 有符号整数溢出会像无符号一样回绕

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏（认知科学依据：一次纠正不够）

## 触发模式（学习者常这么说 / 这么写）
- int 加到最大就变成负数，循环自然退出
- 溢出回绕是可预测的

## 为什么它不成立
1. 有符号溢出是 UB，无符号才是定义好的模运算——两者规则不同，不能类推
2. 实测后果：GCC -O2 依此把 for (int i=0; i>=0; ++i) 编译成无条件 jmp 死循环

## 出处与关联

- 出处：ch28_lifetime_ub.md ⑪.1
- 关联原子：ATOM-UB-GRAY-001
