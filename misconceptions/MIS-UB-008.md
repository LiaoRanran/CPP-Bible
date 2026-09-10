---
id: MIS-UB-008
name: reinterpret_cast 做类型双关读是常规操作
level: deep
domain: UB
trigger_patterns:
  - "强转指针再解引用就能重新解释位模式"
  - "C 里都这么干，C++ 也行"
refutations:
  - "reinterpret_cast 的类型双关读违反严格别名规则 [basic.lval] → UB；优化器可重排读写顺序"
  - "正确做法是 std::bit_cast（C++20）或 memcpy（两者都是定义良好的位重解释）"
source: ch27_cast.md ⑮ 易错点 3；ch42_strict_aliasing.md ㉒.3
related_atoms: [ATOM-UB-GRAY-001]
---

# MIS-UB-008 · reinterpret_cast 做类型双关读是常规操作

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏（认知科学依据：一次纠正不够）

## 触发模式（学习者常这么说 / 这么写）
- 强转指针再解引用就能重新解释位模式
- C 里都这么干，C++ 也行

## 为什么它不成立
1. reinterpret_cast 的类型双关读违反严格别名规则 [basic.lval] → UB；优化器可重排读写顺序
2. 正确做法是 std::bit_cast（C++20）或 memcpy（两者都是定义良好的位重解释）

## 出处与关联

- 出处：ch27_cast.md ⑮ 易错点 3；ch42_strict_aliasing.md ㉒.3
- 关联原子：ATOM-UB-GRAY-001
