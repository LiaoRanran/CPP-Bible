---
id: MIS-MEM-001
name: std::move 会移动对象
level: deep
domain: MEM
trigger_patterns:
  - "std::move(x) 之后 x 就被搬空了"
  - "move 就是 memcpy"
refutations:
  - "std::move 只是 static_cast<T&&>(x)，本身不生成任何指令 [expr.static.cast]"
  - "移动是否发生取决于重载决议是否选中移动构造；源对象仅保证有效但未指定 [lib.types.movedfrom]"
source: ch115_move.md ⑯ 易错点 / 三样板 A
related_atoms: [ATOM-MEM-MOVE-002]
---

# MIS-MEM-001 · std::move 会移动对象

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏（认知科学依据：一次纠正不够）

## 触发模式（学习者常这么说 / 这么写）
- std::move(x) 之后 x 就被搬空了
- move 就是 memcpy

## 为什么它不成立
1. std::move 只是 static_cast<T&&>(x)，本身不生成任何指令 [expr.static.cast]
2. 移动是否发生取决于重载决议是否选中移动构造；源对象仅保证有效但未指定 [lib.types.movedfrom]

## 出处与关联

- 出处：ch115_move.md ⑯ 易错点 / 三样板 A
- 关联原子：ATOM-MEM-MOVE-002
