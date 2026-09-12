---
id: MIS-MEM-014
name: delete 放在函数尾就够：没意识到异常/提前 return 会跳过 delete
level: deep
domain: MEM
trigger_patterns:
  - "在函数最后 delete 就安全了"
  - "资源在函数末尾释放，没问题"
refutations:
  - "函数在 new 与尾部 delete 之间抛异常或提前 return，尾部 delete 不可达 → 泄漏；只有析构（RAII）在栈展开时必然调用 [except.ctor]"
  - "实测：safe_path 抛异常后 RAII 析构仍调用（g_live 归 0），裸路径 g_live 留 1（见 ATOM-MEM-RAII-001 / EV-MEM-009）"
source: ch37_new_delete.md 常见陷阱；ATOM-MEM-RAII-001 / EV-MEM-009
related_atoms: [ATOM-MEM-RAII-001]
---

# MIS-MEM-014 · delete 放在函数尾就够：没意识到异常/提前 return 会跳过 delete

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏

## 触发模式（学习者常这么说 / 这么写）
- 在函数最后 delete 就安全了
- 资源在函数末尾释放，没问题

## 为什么它不成立
1. 函数在 new 与尾部 delete 之间抛异常或提前 return，尾部 delete 不可达 → 泄漏；只有析构（RAII）在栈展开时必然调用 [except.ctor]
2. 实测：safe_path 抛异常后 RAII 析构仍调用（g_live 归 0），裸路径 g_live 留 1（见 ATOM-MEM-RAII-001 / EV-MEM-009）

## 出处与关联
- 出处：ch37_new_delete.md 常见陷阱；ATOM-MEM-RAII-001 / EV-MEM-009
- 关联原子：ATOM-MEM-RAII-001
