---
id: MIS-MEM-007
name: 在构造函数里调用 shared_from_this() 没问题
level: deep
domain: MEM
trigger_patterns:
  - "构造函数里就能拿到自己的 shared_ptr"
  - "shared_from_this 随时可调用"
refutations:
  - "构造期间对象尚未被任何 shared_ptr 持有 → 抛 bad_weak_ptr（或未定义，取决于实现）"
  - "标准用法：构造函数私有化 + 工厂函数返回 shared_ptr，构造完成后才用 shared_from_this"
source: ch41_smart_pointers.md 常见陷阱清单 3 / ⑮
related_atoms: []
---

# MIS-MEM-007 · 在构造函数里调用 shared_from_this() 没问题

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏（认知科学依据：一次纠正不够）

## 触发模式（学习者常这么说 / 这么写）
- 构造函数里就能拿到自己的 shared_ptr
- shared_from_this 随时可调用

## 为什么它不成立
1. 构造期间对象尚未被任何 shared_ptr 持有 → 抛 bad_weak_ptr（或未定义，取决于实现）
2. 标准用法：构造函数私有化 + 工厂函数返回 shared_ptr，构造完成后才用 shared_from_this

## 出处与关联

- 出处：ch41_smart_pointers.md 常见陷阱清单 3 / ⑮
- 关联原子：（暂无，待相关原子锻造后回填）
