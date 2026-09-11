---
id: MIS-MEM-016
name: 智能指针都自动安全：以为 shared_ptr 管了就绝不泄漏（忽略循环引用）
level: deep
domain: MEM
trigger_patterns:
  - "用了 shared_ptr 就再也不会内存泄漏"
  - "智能指针自动管理，不用操心"
refutations:
  - "shared_ptr 只在**非循环**的所有权图里自动释放；成环时引用计数永不为 0 → 泄漏（实测 EV-MEM-014 循环引用 destroyed count=0）"
  - "打破循环须用 weak_ptr 旁观（不增计数）；把'自动管理'等同于'绝不泄漏'是误解 [smartptr.weakptr]（见 ATOM-MEM-SHARED-001 / ATOM-MEM-WEAK-001）"
source: ch41_smart_pointers.md 常见陷阱；ATOM-MEM-SHARED-001 / EV-MEM-014
related_atoms: [ATOM-MEM-SHARED-001, ATOM-MEM-WEAK-001]
---

# MIS-MEM-016 · 智能指针都自动安全：以为 shared_ptr 管了就绝不泄漏（忽略循环引用）

**层级**：deep —— 结构性误解，源于"智能指针=免泄漏"的心智模型；须 ≥2 条独立反例才可能纠偏

## 触发模式（学习者常这么说 / 这么写）
- 用了 shared_ptr 就再也不会内存泄漏
- 智能指针自动管理，不用操心

## 为什么它不成立
1. shared_ptr 只在**非循环**的所有权图里自动释放；成环时引用计数永不为 0 → 泄漏（实测 EV-MEM-014 循环引用 destroyed count=0）
2. 打破循环须用 weak_ptr 旁观（不增计数）；把"自动管理"等同于"绝不泄漏"是误解 [smartptr.weakptr]（见 ATOM-MEM-SHARED-001 / ATOM-MEM-WEAK-001）

## 出处与关联
- 出处：ch41_smart_pointers.md 常见陷阱；ATOM-MEM-SHARED-001 / EV-MEM-014
- 关联原子：ATOM-MEM-SHARED-001、ATOM-MEM-WEAK-001
