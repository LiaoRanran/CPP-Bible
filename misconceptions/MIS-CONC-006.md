---
id: MIS-CONC-006
name: compare_exchange 失败后 expected 变量保持不变
level: surface
domain: CONC
trigger_patterns:
  - "CAS 失败了我还能用原来的 expected"
  - "失败只是返回 false"
refutations:
  - "compare_exchange_weak/strong 失败时会把**实际值**写入 expected（按引用传参）→ 原值被覆盖"
source: ch107_atomic.md ⑯ 常见误用（示例 38）
related_atoms: []
---

# MIS-CONC-006 · compare_exchange 失败后 expected 变量保持不变

**层级**：surface —— 表层误解，一次纠正即可

## 触发模式（学习者常这么说 / 这么写）
- CAS 失败了我还能用原来的 expected
- 失败只是返回 false

## 为什么它不成立
1. compare_exchange_weak/strong 失败时会把**实际值**写入 expected（按引用传参）→ 原值被覆盖

## 出处与关联

- 出处：ch107_atomic.md ⑯ 常见误用（示例 38）
- 关联原子：（暂无，待相关原子锻造后回填）
