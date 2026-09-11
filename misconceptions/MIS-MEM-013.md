---
id: MIS-MEM-013
name: 裸资源管理靠"记得释放"：认为 new 后自己 delete 就能管好资源
level: deep
domain: MEM
trigger_patterns:
  - "new 完记得 delete 就行"
  - "资源管理就是别忘记释放"
refutations:
  - "RAII 把释放绑到析构，由语言在作用域结束（含异常栈展开）保证调用；靠人'记得'在异常/提前 return 路径会漏删 → 泄漏 [except.ctor]"
  - "实测：裸路径在 leak_path 后 g_live 留 1（未释放），同场景 RAII 对象析构后 g_live 归 0（见 ATOM-MEM-RAII-001 / EV-MEM-009）"
source: ch37_new_delete.md 常见陷阱；ATOM-MEM-RAII-001 / EV-MEM-009
related_atoms: [ATOM-MEM-RAII-001]
---

# MIS-MEM-013 · 裸资源管理靠"记得释放"：认为 new 后自己 delete 就能管好资源

**层级**：deep —— 结构性误解，源于"资源靠我记着收"的心智模型；须 ≥2 条独立反例才可能纠偏

## 触发模式（学习者常这么说 / 这么写）
- new 完记得 delete 就行
- 资源管理就是别忘记释放

## 为什么它不成立
1. RAII 把释放绑到析构，由语言在作用域结束（含异常栈展开）保证调用；靠人"记得"在异常/提前 return 路径会漏删 → 泄漏 [except.ctor]
2. 实测：裸路径在 leak_path 后 g_live 留 1（未释放），同场景 RAII 对象析构后 g_live 归 0（见 ATOM-MEM-RAII-001 / EV-MEM-009）

## 出处与关联
- 出处：ch37_new_delete.md 常见陷阱；ATOM-MEM-RAII-001 / EV-MEM-009
- 关联原子：ATOM-MEM-RAII-001
