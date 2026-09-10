---
id: MIS-STL-002
name: vector<bool> 的 operator[] 返回 bool&
level: deep
domain: STL
trigger_patterns:
  - "auto& b = vb[0]; 拿到的是 bool 的引用"
  - "vector<bool> 就是省内存的 vector"
refutations:
  - "vector<bool> 是位压缩特化，operator[] 返回代理对象（proxy reference），不是 bool&"
  - "后果：不能取址、不能绑 bool&、不能喂给 span<bool>；需要真 bool 用 vector<char> 或 deque<bool>"
source: ch77_vector.md ⑯ 易错点；ch158_perf_antipatterns.md 附录 I
related_atoms: []
---

# MIS-STL-002 · vector<bool> 的 operator[] 返回 bool&

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏（认知科学依据：一次纠正不够）

## 触发模式（学习者常这么说 / 这么写）
- auto& b = vb[0]; 拿到的是 bool 的引用
- vector<bool> 就是省内存的 vector

## 为什么它不成立
1. vector<bool> 是位压缩特化，operator[] 返回代理对象（proxy reference），不是 bool&
2. 后果：不能取址、不能绑 bool&、不能喂给 span<bool>；需要真 bool 用 vector<char> 或 deque<bool>

## 出处与关联

- 出处：ch77_vector.md ⑯ 易错点；ch158_perf_antipatterns.md 附录 I
- 关联原子：（暂无，待相关原子锻造后回填）
