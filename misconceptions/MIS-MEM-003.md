---
id: MIS-MEM-003
name: return std::move(local) 能加速返回
level: deep
domain: MEM
trigger_patterns:
  - "返回局部变量时加 move 是帮编译器一把"
  - "不加 move 就会多一次拷贝"
refutations:
  - "返回局部对象时编译器本就允许 NRVO / 隐式移动，加 std::move 反而阻断 NRVO"
  - "对返回值而言 std::move 把 lvalue 转 xvalue，使 NRVO 不再适用——是减效不是增效"
source: ch115_move.md ⑯ 易错点 3；ch117_copy_elision.md ⓪.3
related_atoms: [ATOM-MEM-MOVE-002]
---

# MIS-MEM-003 · return std::move(local) 能加速返回

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏（认知科学依据：一次纠正不够）

## 触发模式（学习者常这么说 / 这么写）
- 返回局部变量时加 move 是帮编译器一把
- 不加 move 就会多一次拷贝

## 为什么它不成立
1. 返回局部对象时编译器本就允许 NRVO / 隐式移动，加 std::move 反而阻断 NRVO
2. 对返回值而言 std::move 把 lvalue 转 xvalue，使 NRVO 不再适用——是减效不是增效

## 出处与关联

- 出处：ch115_move.md ⑯ 易错点 3；ch117_copy_elision.md ⓪.3
- 关联原子：ATOM-MEM-MOVE-002
