---
id: MIS-UB-012
name: 函数实参的求值顺序是确定的，可以依赖它
level: deep
domain: UB
trigger_patterns:
  - "f(g(), h()) 一定先算 g 再算 h"
  - "实参从左到右求值"
refutations:
  - "实参初始化是**不确定顺序**（indeterminately sequenced），只保证不重叠、不保证先后"
  - "实测 GCC 输出 h/g（右→左）、Clang 输出 g/h（左→右）——连编译器之间都相反"
source: 三样板 B；ch（求值顺序）CI Gray-zone 实测
related_atoms: [ATOM-UB-GRAY-001]
---

# MIS-UB-012 · 函数实参的求值顺序是确定的，可以依赖它

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏（认知科学依据：一次纠正不够）

## 触发模式（学习者常这么说 / 这么写）
- f(g(), h()) 一定先算 g 再算 h
- 实参从左到右求值

## 为什么它不成立
1. 实参初始化是**不确定顺序**（indeterminately sequenced），只保证不重叠、不保证先后
2. 实测 GCC 输出 h/g（右→左）、Clang 输出 g/h（左→右）——连编译器之间都相反

## 出处与关联

- 出处：三样板 B；ch（求值顺序）CI Gray-zone 实测
- 关联原子：ATOM-UB-GRAY-001
