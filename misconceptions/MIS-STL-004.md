---
id: MIS-STL-004
name: clear() 会释放 vector 占用的内存
level: surface
domain: STL
trigger_patterns:
  - "clear 之后内存就还了"
  - "clear 等于把 vector 清空并缩容"
refutations:
  - "clear() 只析构元素，capacity() 不变——内存仍被容器持有；释放在 shrink_to_fit() 或换用空 vector 交换"
source: ch77_vector.md ⑰ FAQ
related_atoms: []
---

# MIS-STL-004 · clear() 会释放 vector 占用的内存

**层级**：surface —— 表层误解，一次纠正即可

## 触发模式（学习者常这么说 / 这么写）
- clear 之后内存就还了
- clear 等于把 vector 清空并缩容

## 为什么它不成立
1. clear() 只析构元素，capacity() 不变——内存仍被容器持有；释放在 shrink_to_fit() 或换用空 vector 交换

## 出处与关联

- 出处：ch77_vector.md ⑰ FAQ
- 关联原子：（暂无，待相关原子锻造后回填）
