---
id: MIS-UB-003
name: 前面加 if (p != nullptr) 就能防住后面的空指针解引用
level: deep
domain: UB
trigger_patterns:
  - "先判空再解引用就安全了"
  - "判空是最好的防御"
refutations:
  - "解引用空指针已是 UB；优化器据此反推 p 非空，可能把后续判空检查整段删掉"
  - "实测汇编可见删掉检查后只剩 movl %eax,0 + ud2——保护被优化器移除"
source: ch28_lifetime_ub.md ⑪.2
related_atoms: [ATOM-UB-GRAY-001]
---

# MIS-UB-003 · 前面加 if (p != nullptr) 就能防住后面的空指针解引用

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏（认知科学依据：一次纠正不够）

## 触发模式（学习者常这么说 / 这么写）
- 先判空再解引用就安全了
- 判空是最好的防御

## 为什么它不成立
1. 解引用空指针已是 UB；优化器据此反推 p 非空，可能把后续判空检查整段删掉
2. 实测汇编可见删掉检查后只剩 movl %eax,0 + ud2——保护被优化器移除

## 出处与关联

- 出处：ch28_lifetime_ub.md ⑪.2
- 关联原子：ATOM-UB-GRAY-001
