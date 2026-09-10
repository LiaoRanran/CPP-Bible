---
id: MIS-UB-009
name: static_cast 做多态向下转型是安全的（编译过了就对）
level: deep
domain: UB
trigger_patterns:
  - "Base* 转 Derived* 编译通过就说明类型对"
  - "我知道实际类型，static_cast 更快"
refutations:
  - "static_cast 向下转型不做运行时检查；对象实际不是该派生类型时，访问派生成员即 UB"
  - "需运行时安全用 dynamic_cast（失败返回 nullptr / 抛 bad_cast）"
source: ch27_cast.md ⑮ 易错点 1
related_atoms: []
---

# MIS-UB-009 · static_cast 做多态向下转型是安全的（编译过了就对）

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏（认知科学依据：一次纠正不够）

## 触发模式（学习者常这么说 / 这么写）
- Base* 转 Derived* 编译通过就说明类型对
- 我知道实际类型，static_cast 更快

## 为什么它不成立
1. static_cast 向下转型不做运行时检查；对象实际不是该派生类型时，访问派生成员即 UB
2. 需运行时安全用 dynamic_cast（失败返回 nullptr / 抛 bad_cast）

## 出处与关联

- 出处：ch27_cast.md ⑮ 易错点 1
- 关联原子：（暂无，待相关原子锻造后回填）
