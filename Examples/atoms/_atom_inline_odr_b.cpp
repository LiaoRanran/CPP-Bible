// ATOM-LANG-INLINE-001 夹具 · TU B（实验组：看到 odr_fn 的定义 B —— 与 TU A 不同，违反 ODR）
#define ODR_VALUE 2
#include "_atom_inline_odr_shared.h"

int tu_b_value() { return odr_fn(); }
int tu_b_stable() { return stable_fn(); }
