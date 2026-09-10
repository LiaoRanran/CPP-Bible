---
id: MIS-MEM-004
name: 对 const 对象 std::move 也能省掉拷贝
level: surface
domain: MEM
trigger_patterns:
  - "const T 也能 move，反正只是转换"
  - "std::move(const_obj) 会走移动构造"
refutations:
  - "std::move(const T&) 得到 const T&&，无法绑定 T&& 移动构造 → 静默退化为拷贝构造"
source: ch115_move.md ⑯ 易错点 2
related_atoms: [ATOM-MEM-MOVE-002]
---

# MIS-MEM-004 · 对 const 对象 std::move 也能省掉拷贝

**层级**：surface —— 表层误解，一次纠正即可

## 触发模式（学习者常这么说 / 这么写）
- const T 也能 move，反正只是转换
- std::move(const_obj) 会走移动构造

## 为什么它不成立
1. std::move(const T&) 得到 const T&&，无法绑定 T&& 移动构造 → 静默退化为拷贝构造

## 出处与关联

- 出处：ch115_move.md ⑯ 易错点 2
- 关联原子：ATOM-MEM-MOVE-002
