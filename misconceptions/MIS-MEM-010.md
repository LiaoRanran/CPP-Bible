---
id: MIS-MEM-010
name: Rule of Five 只是理论，含裸指针成员的类写个析构就够了
level: deep
domain: MEM
trigger_patterns:
  - "有裸指针就写析构，别的用编译器生成的"
  - "拷贝构造编译器会帮我写好"
refutations:
  - "只写析构而拷贝仍为编译器生成的逐成员拷贝 → 浅拷贝，两个对象析构同一指针 → double free"
  - " Rule of Five：析构/拷贝构造/拷贝赋值/移动构造/移动赋值要么全自定义要么全 default，五缺一即埋雷"
source: ch39_raii_rule.md ㉒.3 生产踩坑；ch115_move.md ⑰ 最佳实践 5
related_atoms: []
---

# MIS-MEM-010 · Rule of Five 只是理论，含裸指针成员的类写个析构就够了

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏（认知科学依据：一次纠正不够）

## 触发模式（学习者常这么说 / 这么写）
- 有裸指针就写析构，别的用编译器生成的
- 拷贝构造编译器会帮我写好

## 为什么它不成立
1. 只写析构而拷贝仍为编译器生成的逐成员拷贝 → 浅拷贝，两个对象析构同一指针 → double free
2.  Rule of Five：析构/拷贝构造/拷贝赋值/移动构造/移动赋值要么全自定义要么全 default，五缺一即埋雷

## 出处与关联

- 出处：ch39_raii_rule.md ㉒.3 生产踩坑；ch115_move.md ⑰ 最佳实践 5
- 关联原子：（暂无，待相关原子锻造后回填）
