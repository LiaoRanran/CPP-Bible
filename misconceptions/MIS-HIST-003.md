---
id: MIS-HIST-003
name: auto_ptr 被移除是因为它有 bug / 实现得不好
level: deep
domain: HIST
trigger_patterns:
  - "auto_ptr 有缺陷所以被弃用"
  - "它是个失败的设计"
refutations:
  - "拷贝构造签名 auto_ptr(auto_ptr&) 不满足 CopyConstructible 却仍能从非 const 对象拷贝——这是 C++98 **没有移动语义**时表达所有权的合理工程妥协，不是实现失误"
  - "C++11 引入移动语义后，同一需求有了正确语法（std::move + = delete），auto_ptr 才被 unique_ptr 取代"
source: 三样板 C（EV-HIST-001 / EV-MEM-003）
related_atoms: [ATOM-HIST-AUTOPTR-001]
---

# MIS-HIST-003 · auto_ptr 被移除是因为它有 bug / 实现得不好

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏（认知科学依据：一次纠正不够）

## 触发模式（学习者常这么说 / 这么写）
- auto_ptr 有缺陷所以被弃用
- 它是个失败的设计

## 为什么它不成立
1. 拷贝构造签名 auto_ptr(auto_ptr&) 不满足 CopyConstructible 却仍能从非 const 对象拷贝——这是 C++98 **没有移动语义**时表达所有权的合理工程妥协，不是实现失误
2. C++11 引入移动语义后，同一需求有了正确语法（std::move + = delete），auto_ptr 才被 unique_ptr 取代

## 出处与关联

- 出处：三样板 C（EV-HIST-001 / EV-MEM-003）
- 关联原子：ATOM-HIST-AUTOPTR-001
