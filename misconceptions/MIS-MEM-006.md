---
id: MIS-MEM-006
name: 用同一个裸指针构造两个 shared_ptr 也能正常共享引用计数
level: deep
domain: MEM
trigger_patterns:
  - "shared_ptr<int> a(p); shared_ptr<int> b(p); 两个一起管"
  - "同一个指针交给多个智能指针更安全"
refutations:
  - "两个独立控制块各自计数 → 双重释放（double free），不是共享"
  - "正确做法是 shared_ptr<int> b = a;（共享控制块）或用 enable_shared_from_this"
source: ch41_smart_pointers.md 常见陷阱清单 2
related_atoms: []
---

# MIS-MEM-006 · 用同一个裸指针构造两个 shared_ptr 也能正常共享引用计数

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏（认知科学依据：一次纠正不够）

## 触发模式（学习者常这么说 / 这么写）
- shared_ptr<int> a(p); shared_ptr<int> b(p); 两个一起管
- 同一个指针交给多个智能指针更安全

## 为什么它不成立
1. 两个独立控制块各自计数 → 双重释放（double free），不是共享
2. 正确做法是 shared_ptr<int> b = a;（共享控制块）或用 enable_shared_from_this

## 出处与关联

- 出处：ch41_smart_pointers.md 常见陷阱清单 2
- 关联原子：（暂无，待相关原子锻造后回填）
