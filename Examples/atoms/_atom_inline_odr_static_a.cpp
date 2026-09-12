// ATOM-LANG-INLINE-001 机制判别对照夹具 · TU A（**内部链接孪生**）
//
// 与实验组（`_atom_inline_odr_a.cpp`）的唯一差异：`sfn` 带 `static`（内部链接）。
// 预期（推断，由本对照实测检验）：内部链接 ⇒ 两个 TU **各持一份、不发生符号合并**
//   ⇒ 无论链接顺序，程序恒为 sa=1 / sb=2（"各用自己看到的定义"）。
// 若实测随顺序变化，则"顺序依赖来自弱符号合并"这一机制解释被否。
static inline int sfn() { return 1; }

int sa_value() { return sfn(); }
