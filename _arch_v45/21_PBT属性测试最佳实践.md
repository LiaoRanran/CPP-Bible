# 方向 21：PBT 属性测试最佳实践

## 核心结论
1. 属性测试（PBT）是 QueYi 验证哲学的同族方法：不写"期望输出"，而写"输入-输出必须满足的不变量"，由工具随机生成海量输入找反例。QueYi 的四态判决本质是"对 C++ 代码片段的性质判定"。
2. 最佳实践中最关键的三条：**(a) 性质要"必要且充分"（太弱无意义、太强永不通过）、(b) 必须可缩小（shrinking）到最小反例、(c) 种子可复现**——这三点直接对应 QueYi 的"可复现性"卖点。
3. C++ 侧可用 **rapidcheck**，Python 侧用 **hypothesis**；QueYi 内核（813 行 C++）可用 rapidcheck 对自身做 PBT，作为"验证器自验证"的证据。

## 精确数字与案例
- **工具**：Haskell QuickCheck（鼻祖）、Python hypothesis、C++ rapidcheck、Rust proptest、Java jqwik。
- **性质类型（可直接用于 QueYi）**：
  - *逆运算*：`encode(decode(x))==x`（用于 QueYi 哈希链/Merkle 校验）；
  - *幂等*：`verify(verify(x))==verify(x)`；
  - *交换/结合*：对独立卡顺序无关；
  - *oracle*：QueYi 判决 ⊨ 参考编译器（GCC/Clang）实际行为一致；
  - *蜕变关系(metamorphic)*：给代码加无害注释，判决不变。
- **案例**：hypothesis 能在几千次生成中发现手工测试遗漏的边界（如空串/负数/Unicode）；rapidcheck 对 C++ 容器算法同理。
- **反模式**：性质写成 `f(x)==expected(x)`（那就是普通单测了，非 PBT）；性质太强（如要求所有 UB 都被检出）永远失败。

## 对阙疑的 3 条具体行动
1. **用 rapidcheck 测内核**：对 QueYi 的"四态判决函数"写 PBT：随机生成合法 C++ 片段，验证"幂等 + 哈希链一致 + 与参考编译器 oracle 一致"，作为自验证证据。
2. **性质写进 corpus**：把上面 5 类性质变成 QueYi 的"性质卡"，与 48 知识卡并列，展示验证方法的系统性。
3. **可复现种子**：PBT 跑固定 seed + 记录最小反例（shrunk），存进 452 账本，保证审稿人一键复现 0.59ms/卡 + 反例可追溯。

## 盲区（诚实标注）
- rapidcheck 的 API 细节/成熟度我未逐一核实，写稿前需确认其 2027 可用版本。
- "验证器自验证"若性质依赖参考编译器，而参考编译器本身有 bug（方向 18），则 oracle 不绝对；需声明。
- PBT 对"语义正确性"覆盖有限（只能证伪不能证真），QueYi 应配合人工金标准夹具。

## 来源
- [1] Hypothesis — https://hypothesis.works/
- [2] rapidcheck (C++) — https://github.com/emil-e/rapidcheck
- [3] QuickCheck — https://hackage.haskell.org/package/QuickCheck
- [4] PBT 最佳实践 — https://hypothesis.works/articles/what-is-property-based-testing/
