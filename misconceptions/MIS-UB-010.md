---
id: MIS-UB-010
name: const_cast 去掉 const 后写入也没关系
level: deep
domain: UB
trigger_patterns:
  - "我只是改一下，反正拿到的是非 const 指针"
  - "const_cast 就是用来改的"
refutations:
  - "若原对象**本身**是 const（可能在 .rodata），写入是 UB，实测 SIGSEGV"
  - "只有原对象非 const、仅经由 const 引用/指针访问时，去除 const 后写入才合法"
source: ch27_cast.md ⑮ 易错点 2；ch19_variables.md ⑯
related_atoms: []
---

# MIS-UB-010 · const_cast 去掉 const 后写入也没关系

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏（认知科学依据：一次纠正不够）

## 触发模式（学习者常这么说 / 这么写）
- 我只是改一下，反正拿到的是非 const 指针
- const_cast 就是用来改的

## 为什么它不成立
1. 若原对象**本身**是 const（可能在 .rodata），写入是 UB，实测 SIGSEGV
2. 只有原对象非 const、仅经由 const 引用/指针访问时，去除 const 后写入才合法

## 出处与关联

- 出处：ch27_cast.md ⑮ 易错点 2；ch19_variables.md ⑯
- 关联原子：（暂无，待相关原子锻造后回填）
