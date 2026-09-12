// ATOM-LANG-INLINE-001 夹具 · TU A（实验组：看到 odr_fn 的定义 A）
#define ODR_VALUE 1
#include "_atom_inline_odr_shared.h"

int tu_a_value() { return odr_fn(); }
int tu_a_stable() { return stable_fn(); }
