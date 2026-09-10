---
id: MIS-UB-013
name: f(i++, i++) 在所有标准版本都是未定义行为
level: deep
domain: UB
trigger_patterns:
  - "同一表达式改两次 i 就是 UB，C++17 也一样"
  - "自增两次必然 UB"
refutations:
  - "C++17（P0145R3）把**函数实参初始化**从 unsequenced 改为 indeterminately sequenced → 该式在 C++17 起是 unspecified"
  - "而运算符操作数仍为 unsequenced，故 i = i++ + ++i 在**所有版本**都是 UB——必须用版本区分"
source: 三样板 B（人审第 1 轮纠正）；ch（求值顺序）
related_atoms: [ATOM-UB-GRAY-001]
---

# MIS-UB-013 · f(i++, i++) 在所有标准版本都是未定义行为

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏（认知科学依据：一次纠正不够）

## 触发模式（学习者常这么说 / 这么写）
- 同一表达式改两次 i 就是 UB，C++17 也一样
- 自增两次必然 UB

## 为什么它不成立
1. C++17（P0145R3）把**函数实参初始化**从 unsequenced 改为 indeterminately sequenced → 该式在 C++17 起是 unspecified
2. 而运算符操作数仍为 unsequenced，故 i = i++ + ++i 在**所有版本**都是 UB——必须用版本区分

## 出处与关联

- 出处：三样板 B（人审第 1 轮纠正）；ch（求值顺序）
- 关联原子：ATOM-UB-GRAY-001
