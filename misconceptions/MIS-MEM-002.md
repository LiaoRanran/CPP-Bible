---
id: MIS-MEM-002
name: 移动后源对象为空，可以当空容器用
level: deep
domain: MEM
trigger_patterns:
  - "移动完 size() 一定是 0"
  - "移动后的源可以当空字符串 / 空容器继续用"
refutations:
  - "标准只说源对象处于有效但未指定状态，清空是实现细节而非保证 [lib.types.movedfrom]"
  - "std::string 的小字符串优化（SSO）下移动后源可能仍保留内容；实测需 volatile 读回才观测得到"
source: ch115_move.md ⑯ 易错点 4 / 三样板 A
related_atoms: [ATOM-MEM-MOVE-002]
---

# MIS-MEM-002 · 移动后源对象为空，可以当空容器用

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏（认知科学依据：一次纠正不够）

## 触发模式（学习者常这么说 / 这么写）
- 移动完 size() 一定是 0
- 移动后的源可以当空字符串 / 空容器继续用

## 为什么它不成立
1. 标准只说源对象处于有效但未指定状态，清空是实现细节而非保证 [lib.types.movedfrom]
2. std::string 的小字符串优化（SSO）下移动后源可能仍保留内容；实测需 volatile 读回才观测得到

## 出处与关联

- 出处：ch115_move.md ⑯ 易错点 4 / 三样板 A
- 关联原子：ATOM-MEM-MOVE-002
