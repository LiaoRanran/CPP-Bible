---
id: MIS-HIST-001
name: auto_ptr 和 unique_ptr 差不多，只是名字旧一点
level: surface
domain: HIST
trigger_patterns:
  - "auto_ptr 就是老版本的 unique_ptr"
  - "换个名字而已"
refutations:
  - "两者对拷贝的处置相反：auto_ptr 允许拷贝（且静默转移+清空源），unique_ptr 拷贝构造 = delete（编译期拒绝）"
source: 三样板 C；ch41_smart_pointers.md
related_atoms: [ATOM-HIST-AUTOPTR-001]
---

# MIS-HIST-001 · auto_ptr 和 unique_ptr 差不多，只是名字旧一点

**层级**：surface —— 表层误解，一次纠正即可

## 触发模式（学习者常这么说 / 这么写）
- auto_ptr 就是老版本的 unique_ptr
- 换个名字而已

## 为什么它不成立
1. 两者对拷贝的处置相反：auto_ptr 允许拷贝（且静默转移+清空源），unique_ptr 拷贝构造 = delete（编译期拒绝）

## 出处与关联

- 出处：三样板 C；ch41_smart_pointers.md
- 关联原子：ATOM-HIST-AUTOPTR-001
