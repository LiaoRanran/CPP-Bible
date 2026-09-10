---
id: MIS-MEM-009
name: 析构函数里抛异常只是传播出去而已
level: deep
domain: MEM
trigger_patterns:
  - "析构里抛异常和别处一样往外传"
  - "抛了也能被外层 catch 到"
refutations:
  - "析构函数默认 noexcept；栈展开期间析构抛异常 → std::terminate，程序直接终止"
  - "这决定了 RAII 类必须把可能失败的操作（关闭连接/刷盘）做成显式方法而非只放析构"
source: ch39_raii_rule.md ㉒.3；ch40_exception_safety.md ⑲ 清单 1
related_atoms: []
---

# MIS-MEM-009 · 析构函数里抛异常只是传播出去而已

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏（认知科学依据：一次纠正不够）

## 触发模式（学习者常这么说 / 这么写）
- 析构里抛异常和别处一样往外传
- 抛了也能被外层 catch 到

## 为什么它不成立
1. 析构函数默认 noexcept；栈展开期间析构抛异常 → std::terminate，程序直接终止
2. 这决定了 RAII 类必须把可能失败的操作（关闭连接/刷盘）做成显式方法而非只放析构

## 出处与关联

- 出处：ch39_raii_rule.md ㉒.3；ch40_exception_safety.md ⑲ 清单 1
- 关联原子：（暂无，待相关原子锻造后回填）
