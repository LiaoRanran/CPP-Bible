---
id: MIS-MEM-011
name: unique_ptr 可以像普通对象一样按值传参
level: surface
domain: MEM
trigger_patterns:
  - "函数签名直接写 unique_ptr<T> 收值"
  - "传 unique_ptr 进去函数就能接管"
refutations:
  - "unique_ptr 不可拷贝，按值传参必须 std::move；调用点忘了 move 就是编译错误（这是优点）"
  - "只读场景应传 T& 或 T*，不涉及所有权就别传智能指针"
source: ch41_smart_pointers.md 常见陷阱清单 6
related_atoms: [ATOM-HIST-AUTOPTR-001]
---

# MIS-MEM-011 · unique_ptr 可以像普通对象一样按值传参

**层级**：surface —— 表层误解，一次纠正即可

## 触发模式（学习者常这么说 / 这么写）
- 函数签名直接写 unique_ptr<T> 收值
- 传 unique_ptr 进去函数就能接管

## 为什么它不成立
1. unique_ptr 不可拷贝，按值传参必须 std::move；调用点忘了 move 就是编译错误（这是优点）
2. 只读场景应传 T& 或 T*，不涉及所有权就别传智能指针

## 出处与关联

- 出处：ch41_smart_pointers.md 常见陷阱清单 6
- 关联原子：ATOM-HIST-AUTOPTR-001
