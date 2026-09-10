---
id: MIS-UB-006
name: for (int x : make()) 遍历临时容器是安全的
level: deep
domain: UB
trigger_patterns:
  - "范围 for 会帮我把临时容器留住"
  - "make() 的结果在循环里一直活着"
refutations:
  - "C++17 起范围 for 的临时对象不再被延长到循环结束（init-statement 之后的临时在循环外即销毁）"
  - "结果是迭代器悬垂 → UB；应写成 for (auto&& c = make(); int x : c)"
source: ch28_lifetime_ub.md ⑥.3
related_atoms: []
---

# MIS-UB-006 · for (int x : make()) 遍历临时容器是安全的

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏（认知科学依据：一次纠正不够）

## 触发模式（学习者常这么说 / 这么写）
- 范围 for 会帮我把临时容器留住
- make() 的结果在循环里一直活着

## 为什么它不成立
1. C++17 起范围 for 的临时对象不再被延长到循环结束（init-statement 之后的临时在循环外即销毁）
2. 结果是迭代器悬垂 → UB；应写成 for (auto&& c = make(); int x : c)

## 出处与关联

- 出处：ch28_lifetime_ub.md ⑥.3
- 关联原子：（暂无，待相关原子锻造后回填）
