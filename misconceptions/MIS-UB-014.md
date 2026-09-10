---
id: MIS-UB-014
name: 函数参数的求值顺序是未定义行为
level: deep
domain: UB
trigger_patterns:
  - "f(g(), h()) 里顺序不确定，所以是 UB"
  - "求值顺序不确定就等于未定义行为"
refutations:
  - "C++17（P0145R3）把实参初始化从 unsequenced 改为 **indeterminately sequenced**（[expr.call]）：不保证先后，但**绝不允许重叠** → 是 unspecified，不是 UB"
  - "判据是副作用的**测序关系**：unsequenced（可重叠）→ UB；indeterminately sequenced（不重叠）→ unspecified。把两者混为一谈会让读者对合法代码产生不必要的恐慌"
source: 三样板 B（人审第 1 轮纠正：执行方曾拿 C++11/14 规则套 C++17）
related_atoms: [ATOM-UB-GRAY-001]
---

# MIS-UB-014 · 函数参数的求值顺序是未定义行为

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏（认知科学依据：一次纠正不够）

## 触发模式（学习者常这么说 / 这么写）
- f(g(), h()) 里顺序不确定，所以是 UB
- 求值顺序不确定就等于未定义行为

## 为什么它不成立
1. C++17（P0145R3）把实参初始化从 unsequenced 改为 **indeterminately sequenced**（[expr.call]）：不保证先后，但**绝不允许重叠** → 是 unspecified，不是 UB
2. 判据是副作用的**测序关系**：unsequenced（可重叠）→ UB；indeterminately sequenced（不重叠）→ unspecified。把两者混为一谈会让读者对合法代码产生不必要的恐慌

## 出处与关联

- 出处：三样板 B（人审第 1 轮纠正：执行方曾拿 C++11/14 规则套 C++17）
- 关联原子：ATOM-UB-GRAY-001
