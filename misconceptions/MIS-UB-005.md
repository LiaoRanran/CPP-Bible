---
id: MIS-UB-005
name: 把临时对象绑定到引用，生命周期就一定被延长
level: deep
domain: UB
trigger_patterns:
  - "const T& r = f(); 临时对象活到 r 作用域结束"
  - "绑到引用就延长了"
refutations:
  - "生命周期延长只适用于**直接绑定到引用变量**这一条路径；例外见标准 [class.temporary]"
  - "绑定到结构体成员引用、数组元素、函数返回引用、initializer_list 元素均**不**延长"
source: ch28_lifetime_ub.md ⑥ 临时生命周期延长「例外」
related_atoms: []
---

# MIS-UB-005 · 把临时对象绑定到引用，生命周期就一定被延长

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏（认知科学依据：一次纠正不够）

## 触发模式（学习者常这么说 / 这么写）
- const T& r = f(); 临时对象活到 r 作用域结束
- 绑到引用就延长了

## 为什么它不成立
1. 生命周期延长只适用于**直接绑定到引用变量**这一条路径；例外见标准 [class.temporary]
2. 绑定到结构体成员引用、数组元素、函数返回引用、initializer_list 元素均**不**延长

## 出处与关联

- 出处：ch28_lifetime_ub.md ⑥ 临时生命周期延长「例外」
- 关联原子：（暂无，待相关原子锻造后回填）
