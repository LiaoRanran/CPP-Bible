---
id: MIS-STL-007
name: std::string 的拷贝是写时复制（COW），很便宜
level: deep
domain: STL
trigger_patterns:
  - "string 拷贝不复制字符，反正 COW"
  - "传 string 值很便宜"
refutations:
  - "C++11 起禁止 COW（要求迭代器和引用在拷贝后仍有效且 operator[] 返回可写引用）→ 拷贝必深拷贝"
  - "SSO 让**短字符串**拷贝便宜，长字符串拷贝是真实开销；该用 move/引用时别依赖 COW"
source: ch81_string.md ⑦ 拷贝/移动语义与 COW 陷阱
related_atoms: []
---

# MIS-STL-007 · std::string 的拷贝是写时复制（COW），很便宜

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏（认知科学依据：一次纠正不够）

## 触发模式（学习者常这么说 / 这么写）
- string 拷贝不复制字符，反正 COW
- 传 string 值很便宜

## 为什么它不成立
1. C++11 起禁止 COW（要求迭代器和引用在拷贝后仍有效且 operator[] 返回可写引用）→ 拷贝必深拷贝
2. SSO 让**短字符串**拷贝便宜，长字符串拷贝是真实开销；该用 move/引用时别依赖 COW

## 出处与关联

- 出处：ch81_string.md ⑦ 拷贝/移动语义与 COW 陷阱
- 关联原子：（暂无，待相关原子锻造后回填）
