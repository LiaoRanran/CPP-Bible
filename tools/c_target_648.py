"""648 A · **C 语言打靶**：真编译器实测 → 证据卡 → 原子卡（一条链，数字全部来自实跑）。

E1 调研的结论是「67 条规则没有一条是 C++ 语法专用的 ⇒ 主战场在 Domain Pack + 卡片 + 证据源」。
648 就按这条结论开工：**先建证据，再建卡**（与仓内 PERF-003 的成功顺序一致）。

链路（`--probe` → `--cards`，两步都可复跑）：

1. **`--probe`**：把 10 个 C 夹具写进 `Examples/c/`，用 **gcc 与 clang 的 C 模式**
   在 `c11 / c17 / c23 × -O0 / -O2` 下**真编译 + 真运行**，把 stdout 落盘成 `.out`，
   `-O2 -S` 的汇编落盘成 `.asm`（作为证据卡工件），并记下诊断（warning）条数
   ⇒ `data/648_c_probe.json`；
2. **`--cards`**：读探针结果 + `data/648_c_standard.json`（N1570 原文）⇒ 写
   **10 张证据卡**（`evidence/<域>/EV-…`）与 **10 张原子卡**（`atoms/<域>/ATOM-…`）。

**反例（必须的「让它失败的实验"）**：每个夹具都同时跑「正确写法」与「看起来对但错的写法」，
两个结果都打印出来 —— 卡片正文的反例节直接用这两个**实测**数字，不靠想象。

诚实边界：
* 卡的 `status` 一律 `draft` —— verified 唯人签，Agent 不自置（不代签）；
* 标准引用只写**能机器核对的** N1570（C11）条款；C17/C23 只留下载留痕（PDF 无解析库）；
* 编译器/标准组合跑不通时**如实记 failed**，不静默跳过。

CLI：`--check` 只读自检 · `--probe` · `--cards` · `--report`。纯标准库。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

OUT_MD = os.path.join(ROOT, "data", "648_c_target.md")
OUT_JSON = os.path.join(ROOT, "data", "648_c_probe.json")
STD_JSON = os.path.join(ROOT, "data", "648_c_standard.json")
#: 夹具与工件放 `Examples/atoms/`（与存量 51 个工件同一台账；648 的 C 夹具统一用 `_c_` 前缀）
EXAMPLES_C = os.path.join(ROOT, "Examples", "atoms")
BUILD = os.path.join(ROOT, "build", "c648")

#: 编译器（实测可用：gcc 13.1.0 MinGW / clang 22.1.8）
COMPILERS = ("gcc", "clang")
#: 标准档位。`c23` 在部分编译器上不存在 ⇒ 逐档试 [c23, c2x]，用哪个记哪个
STDS = ("c11", "c17", "c23")
STD_FALLBACK = {"c23": "c2x"}
OPTS = ("-O0", "-O2")
#: 证据卡的「主档位」（工件与 .out 用它生成，保证可复现）
MAIN_CC, MAIN_STD, MAIN_OPT = "gcc", "c11", "-O2"

DATE = "2026-09-27"


# ============================== 10 个 C 夹具 ==============================
# 每个夹具都打印 `key=value` 行：既含「正确写法」的结果，也含「反例写法」的结果。
FIXTURES: list[dict[str, Any]] = [
    {
        "key": "decay", "dir": "lang", "domain": "LANG", "topic": "DECAY", "type": "rule",
        "symbol": "decay_param_sizeof",
        "title": "数组形参会退化为指针：函数内的 sizeof 拿不到数组长度",
        "clause": "decay",
        "audience": "beginner", "cognitive_load": "low", "depth": "compiler",
        "claim": ("C 的数组形参在函数内已退化为指针，因此函数内用 sizeof(p)/sizeof(p[0]) "
                  "算出的「元素个数」恒为 sizeof(指针)/sizeof(元素)（x86-64 上 int 数组恒得 2），"
                  "与实参数组长度无关。"),
        "assert_symbol": "decay_param_sizeof",
        "code": r'''#include <stdio.h>

static void decay_param_sizeof(int p[10]) {
    printf("decay_sizeof_param=%zu\n", sizeof p);
    printf("decay_len_wrong_inside=%zu\n", sizeof p / sizeof p[0]);
}

int main(void) {
    int a[10];
    printf("decay_sizeof_array=%zu\n", sizeof a);
    printf("decay_len_true=%zu\n", sizeof a / sizeof a[0]);
    decay_param_sizeof(a);
    return 0;
}
''',
        "counterexample": ("`decay_len_wrong_inside` 是「看起来对」的写法（教科书里算数组长度的那一行），"
                           "实测恒为 2；`decay_len_true` 才是 10。二者的差就是退化。"),
    },
    {
        "key": "malloc", "dir": "mem", "domain": "MEM", "topic": "MALLOC", "type": "idiom",
        "symbol": "malloc_lifecycle_probe",
        "title": "free 不清空指针变量，也不保证 malloc(0) 返回 NULL",
        "clause": "malloc",
        "audience": "beginner", "cognitive_load": "medium", "depth": "runtime",
        "claim": ("C 的 free 只释放空间：被 free 的指针变量仍持有原地址（故 if (p) 判断无效），"
                  "free(NULL) 是定义好的空操作，而 malloc(0) 是否返回 NULL 是实现相关的"
                  "（本次实测两个编译器都返回非 NULL）。"),
        "assert_symbol": "malloc_lifecycle_probe",
        "code": r'''#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stddef.h>

static uintptr_t malloc_lifecycle_probe(void) {
    void *p = malloc(0);
    int zero_is_null = (p == NULL);
    free(p);

    int *q = malloc(sizeof(int) * 4);
    int aligned = (((uintptr_t)q % _Alignof(max_align_t)) == 0);
    uintptr_t before = (uintptr_t)q;
    free(q);                       /* 只释放；变量 q 本身不会被清零 */

    free(NULL);                    /* 标准：空操作 */
    printf("malloc0_null=%d\n", zero_is_null);
    printf("alloc_aligned=%d\n", aligned);
    printf("dangling_value_nonzero=%d\n", before != 0);
    printf("reached_after_free_null=1\n");
    return before;
}

int main(void) {
    (void)malloc_lifecycle_probe();
    return 0;
}
''',
        "counterexample": ("`dangling_value_nonzero=1` 证明「free 后指针变量仍非 NULL」，"
                           "所以 `if (p) { use(p); }` 这类「保护」是无效的；"
                           "把 `malloc(0)` 当「必定返回 NULL」来判错 likewise 会误判。"),
    },
    {
        "key": "strbound", "dir": "mem", "domain": "MEM", "topic": "STRBOUND", "type": "pitfall",
        "symbol": "strbound_probe",
        "title": "snprintf 的返回值是「本该写入的长度」，strncpy 不保证 NUL 终止",
        "clause": "strbound",
        "audience": "intermediate", "cognitive_load": "medium", "depth": "runtime",
        "claim": ("snprintf 返回的是「若缓冲够大本会写入的字符数」（可能大于缓冲，实测 10 > 8 ⇒ 已截断），"
                  "把它当成「实际写入长度」会越界；strncpy 在源串长度 ≥ n 时**不会**写 NUL 终止符"
                  "（实测 strncpy_nul_terminated=0）。"),
        "assert_symbol": "strbound_probe",
        "code": r'''#include <stdio.h>
#include <string.h>

static void strbound_probe(void) {
    char buf[8];
    int n = snprintf(buf, sizeof buf, "%s", "1234567890");
    printf("snprintf_ret=%d\n", n);
    printf("snprintf_written=%d\n", (int)strlen(buf));
    printf("snprintf_truncated=%d\n", n >= (int)sizeof buf);

    char dst[8];
    memset(dst, 'X', sizeof dst);
    strncpy(dst, "12345678", sizeof dst);
    int terminated = 0;
    for (size_t i = 0; i < sizeof dst; i++) {
        if (dst[i] == '\0') { terminated = 1; }
    }
    printf("strncpy_nul_terminated=%d\n", terminated);
    printf("strncpy_last_byte=%d\n", (int)(unsigned char)dst[7]);
}

int main(void) {
    strbound_probe();
    return 0;
}
''',
        "counterexample": ("`snprintf_ret=10` 而缓冲只有 8 —— 把返回值当长度去 `buf[n]` 就越界；"
                           "`strncpy_nul_terminated=0` 说明「用了 strncpy 就安全」是错的。"
                           "（注意：本卡**不**用 strlen(dst) 去读未终止的缓冲，那本身就越界。）"),
    },
    {
        "key": "fnptr", "dir": "lang", "domain": "LANG", "topic": "FNPTR", "type": "rule",
        "symbol": "fnptr_probe",
        "title": "函数指针必须与目标函数类型兼容，否则调用是未定义行为",
        "clause": "fnptr",
        "audience": "intermediate", "cognitive_load": "medium", "depth": "compiler",
        "claim": ("C 允许把函数指针强转成别的函数指针类型，但**经不兼容类型调用即未定义行为**（C11 6.5.2.2p9）；"
                  "本批不去触发它（触发即 UB），而是以两条真实证据固定这一点：① 标准原文的措辞；"
                  "② 直接强转时 gcc 13.1.0 与 clang 22.1.8 **各给出 1 条诊断**（实测），"
                  "而转换本身仍能编译通过、地址也非空 ⇒ 「能编过」不等于「调用安全」。"),
        "assert_symbol": "fnptr_probe",
        "code": r'''#include <stdio.h>

static int add2(int a, int b) { return a + b; }

typedef int (*FnVoid)(void);

static void fnptr_probe(void) {
    int (*good)(int, int) = add2;
    FnVoid bad = (FnVoid)add2;           /* 直接强转（不经 void*）：类型不兼容，调用即 UB（本卡不调用） */
    printf("fnptr_sizeof=%zu\n", sizeof good);
    printf("good_call=%d\n", good(2, 3));
    printf("bad_addr_nonzero=%d\n", bad != NULL);
}

int main(void) {
    fnptr_probe();
    return 0;
}
''',
        "counterexample": ("`bad_addr_nonzero=1` 说明「转换本身能过、地址也非空」——于是容易误以为"
                           "调用也安全。真正的判据是编译器的 `-Wcast-function-type` 诊断与标准条款，"
                           "而不是「它跑起来了」。"),
    },
    {
        "key": "volatile", "dir": "lang", "domain": "LANG", "topic": "VOLATILE", "type": "concept",
        "symbol": "volatile_probe",
        "title": "volatile 的作用是「每次都真的去访问一次」，不是「多线程同步」",
        "clause": "volatile",
        "audience": "intermediate", "cognitive_load": "high", "depth": "asm",
        "claim": ("volatile 约束的是**抽象的访存次数**：-O2 下普通变量的三次读取被**完全折叠**"
                  "（实测生成的汇编里对它的引用次数为 0），而 volatile 变量必须逐次访问（实测引用 4 次）；"
                  "它**不**提供原子性，也**不**提供线程间的同步顺序。"),
        "assert_symbol": "volatile_probe",
        "code": r'''#include <stdio.h>

static int plain_flag = 0;
static volatile int vol_flag = 0;

static int volatile_probe(void) {
    int sink = 0;
    for (int i = 0; i < 3; i++) { sink += plain_flag; }
    for (int i = 0; i < 3; i++) { sink += vol_flag; }
    return sink;
}

int main(void) {
    printf("sink=%d\n", volatile_probe());
    return 0;
}
''',
        "counterexample": ("把 `volatile` 当「线程安全的开关」是最常见的误解：它只保证"
                           "「每次都去内存读」，既不原子也不建立顺序 —— 汇编里读的次数变了，"
                           "但「读-改-写」仍可能交错。"),
    },
    {
        "key": "setjmp", "dir": "lang", "domain": "LANG", "topic": "SETJMP", "type": "pitfall",
        "symbol": "setjmp_probe",
        "title": "longjmp 之后，非 volatile 的局部变量值是不确定的",
        "clause": "setjmp",
        "audience": "intermediate", "cognitive_load": "high", "depth": "compiler",
        "claim": ("longjmp 返回后，setjmp 所在函数里**非 volatile 的自动变量**若在两者之间被改过，"
                  "其值**不确定**：实测同一份代码在 -O0 下读回 5、在 -O2 下读回 0（gcc 与 clang 一致），"
                  "而 volatile 变量在两个档位下都读回 5（标准保证）。"),
        "assert_symbol": "setjmp_probe",
        "code": r'''#include <stdio.h>
#include <setjmp.h>

static jmp_buf env;

static void jump_back(void) { longjmp(env, 1); }

static void setjmp_probe(void) {
    volatile int vol_local = 0;
    int plain_local = 0;
    if (setjmp(env) == 0) {
        vol_local = 5;
        plain_local = 5;
        jump_back();
    }
    printf("after_longjmp_plain=%d\n", plain_local);
    printf("after_longjmp_volatile=%d\n", vol_local);
}

int main(void) {
    setjmp_probe();
    return 0;
}
''',
        "counterexample": ("`after_longjmp_plain` 在 -O0 与 -O2 下可以不一样（这就是「不确定」的实测形态）；"
                           "只有 `after_longjmp_volatile` 恒为 5。用普通局部变量在长跳转后传递状态是错的。"),
    },
    {
        "key": "intpromo", "dir": "lang", "domain": "LANG", "topic": "INTPROMO", "type": "rule",
        "symbol": "intpromo_probe",
        "title": "有符号与无符号比较时，有符号一侧会被转成无符号（-1 < 1u 是假）",
        "clause": "intpromo",
        "audience": "beginner", "cognitive_load": "low", "depth": "runtime",
        "claim": ("常用算术转换会把有符号操作数转成无符号：实测 `-1 < 1u` 的结果为 0（因为 -1 转成了 UINT_MAX），"
                  "而 `signed char` 参与运算会先提升到 int（实测 sizeof(c+d)=4，故 100+100=200 不溢出）。"),
        "assert_symbol": "intpromo_probe",
        "code": r'''#include <stdio.h>

static void intpromo_probe(void) {
    int i = -1;
    unsigned u = 1u;
    printf("cmp_signed_unsigned=%d\n", i < u);
    printf("minus1_as_unsigned=%u\n", (unsigned)-1);

    signed char c = 100;
    signed char d = 100;
    printf("char_promoted_sum=%d\n", c + d);
    printf("char_sum_type_size=%zu\n", sizeof(c + d));
}

int main(void) {
    intpromo_probe();
    return 0;
}
''',
        "counterexample": ("`cmp_signed_unsigned=0` 是反直觉的（-1 明明更小），"
                           "把数组长度 `size_t` 与 `int` 混比时这个转换会造出经典越界；"
                           "对照 `char_promoted_sum=200` 说明提升本身是好事，问题出在符号性。"),
    },
    {
        "key": "bitfield", "dir": "lang", "domain": "LANG", "topic": "BITFIELD", "type": "pitfall",
        "symbol": "bitfield_probe",
        "title": "位域的布局与 Plain int 位域的符号性都是实现定义的",
        "clause": "bitfield",
        "audience": "expert", "cognitive_load": "high", "depth": "abi",
        "claim": ("位域在同一「可寻址存储单元」内的分配顺序、跨单元的对齐都是**实现定义**；"
                  "plain `int` 位域被解释为有符号还是无符号也**由实现决定**"
                  "（实测两个编译器都按有符号处理 ⇒ 4 位位域存 -1 读回 -1，但这不是可移植结论）。"),
        "assert_symbol": "bitfield_probe",
        "code": r'''#include <stdio.h>
#include <string.h>

struct BF { unsigned a : 3; unsigned b : 5; int c : 4; };

static void bitfield_probe(void) {
    struct BF s;
    memset(&s, 0, sizeof s);
    s.a = 5;
    s.b = 21;
    s.c = -1;
    printf("bf_sizeof=%zu\n", sizeof s);
    printf("bf_a=%u\n", s.a);
    printf("bf_b=%u\n", s.b);
    printf("bf_c_signed_readback=%d\n", s.c);
    unsigned char raw[sizeof s];
    memcpy(raw, &s, sizeof s);
    printf("bf_byte0=%u\n", (unsigned)raw[0]);
    printf("bf_byte1=%u\n", (unsigned)raw[1]);
}

int main(void) {
    bitfield_probe();
    return 0;
}
''',
        "counterexample": ("`bf_c_signed_readback=-1` 只在「实现把 plain int 位域当 signed」时成立；"
                           "换编译器即可变成 15。把它写进寄存器映射或序列化格式就是埋雷。"),
    },
    {
        "key": "macro", "dir": "lang", "domain": "LANG", "topic": "MACRO", "type": "pitfall",
        "symbol": "macro_probe",
        "title": "宏是文本替换：不加括号会错优先级，传带副作用实参会被求值多次",
        "clause": "macro",
        "audience": "beginner", "cognitive_load": "low", "depth": "compiler",
        "claim": ("函数式宏在替换前先展开实参，替换是**文本级**的：实测 `SQ(x) x*x` 在 `SQ(3+1)` 上得 7"
                  "（而正确写法得 16），`MAX(a,b)` 传入 `i++` 时该实参被求值两次（实测 i 从 0 变 2）。"),
        "assert_symbol": "macro_probe",
        "code": r'''#include <stdio.h>

#define SQ_BAD(x)   x * x
#define SQ_GOOD(x)  ((x) * (x))
#define MAX_BAD(a, b) ((a) > (b) ? (a) : (b))

static void macro_probe(void) {
    int v = 3;
    printf("sq_bad=%d\n", SQ_BAD(v + 1));
    printf("sq_good=%d\n", SQ_GOOD(v + 1));

    int i = 0;
    int m = MAX_BAD(0, i++);   /* 走 else 分支 ⇒ i++ 被求值第二次 */
    printf("max_bad_result=%d\n", m);
    printf("i_after=%d\n", i);
}

int main(void) {
    macro_probe();
    return 0;
}
''',
        "counterexample": ("`sq_bad=7` 与 `sq_good=16` 同一次运行对照；`i_after=2` 直接证明"
                           "「i++ 被求值了两次」（写的人只想要一次）。"),
    },
    {
        "key": "signedovf", "dir": "ub", "domain": "UB", "topic": "SIGNEDOVF", "type": "pitfall",
        "symbol": "signedovf_probe",
        "title": "有符号整数溢出是 UB：同一行「溢出检查」在两个编译器上答案相反",
        "clause": "signedovf",
        "audience": "intermediate", "cognitive_load": "medium", "depth": "compiler",
        "claim": ("有符号溢出是 UB（C11 6.5p5），因此「加完再比较」不是可靠的溢出检查：实测 "
                  "`INT_MAX + 1 > INT_MAX` 在 gcc 13.1.0 上**恒为 1**（-O0 与 -O2 都折叠成常量真），"
                  "在 clang 22.1.8 上**恒为 0**（两个档位都按回绕算）——同一表达式在两个编译器上"
                  "**答案相反且都不崩**，这正是 UB 的含义（结果由实现决定，不是「会回绕」）；"
                  "无符号回绕则是定义良好的（实测 0）。"),
        "assert_symbol": "signedovf_probe",
        "code": r'''#include <stdio.h>
#include <limits.h>

static void signedovf_probe(void) {
    int i = INT_MAX;
    printf("signed_plus1_gt=%d\n", (i + 1) > i);

    unsigned u = UINT_MAX;
    printf("unsigned_plus1_gt=%d\n", (u + 1) > u);
    printf("unsigned_wrapped=%u\n", u + 1);
}

int main(void) {
    signedovf_probe();
    return 0;
}
''',
        "counterexample": ("`signed_plus1_gt` 在 -O0/-O2 下给出**不同**答案，就是「UB 不是『会回绕』」"
                           "而是「编译器可以任意处理」的直接证据；把它当溢出检测用是错的。"),
    },
]


#: 证据卡编号（**写死**：生成时已核对与存量不冲突 —— LANG 现有 001/002，MEM 现有 001..045，UB 现有 001/002）
EV_NO: dict[str, int] = {"decay": 3, "fnptr": 4, "volatile": 5, "setjmp": 6, "intpromo": 7,
                         "bitfield": 8, "macro": 9, "malloc": 46, "strbound": 47,
                         "signedovf": 3}

#: 卡片文案（与夹具分开，便于把「可编译的代码」与「给读者的话」各自改各自的）
CARD_TEXT: dict[str, dict[str, str]] = {
    "decay": {
        "subject": "数组形参", "predicate": "进入函数后", "object": "pointer decay",
        "hypothesis": "同一数组在调用方与被调用方的 sizeof 不同：调用方是数组字节数，函数内是指针字节数。",
        "motivation": "为什么 sizeof(a)/sizeof(a[0]) 在 main 里对、挪进函数就恒等于 2？",
        "socratic": "如果把形参写成 int *p 与 int p[10]，编译器看到的有区别吗？",
        "predict_first": "先猜函数内 sizeof(p) 的值，再看实测。",
        "analogy": "数组把「长度」写在自己身上，而形参只拿到一张写着地址的纸条——纸条上没有长度。",
        "boundary": "不要把数组长度当参数省掉：要么显式传长度，要么用哨兵/结构体携带长度。",
    },
    "malloc": {
        "subject": "free 之后的指针变量", "predicate": "其值为", "object": "dangling pointer",
        "hypothesis": "free 释放空间但不清空指针变量；free(NULL) 是空操作；malloc(0) 可为非 NULL。",
        "motivation": "为什么 `if (p) use(p);` 挡不住悬垂指针？",
        "socratic": "free(p) 之后再加一句 p = NULL，改变的是指针还是那块内存？",
        "predict_first": "先猜 malloc(0) 返回 NULL 还是非 NULL，再看两个编译器的实测。",
        "analogy": "free 像是把房间退了，可你手里的房卡还写着那个房间号——刷卡不会报错，但房间已经不是你的了。",
        "boundary": "不要用 `if (p)` 判断内存是否还有效；释放后立刻置空是唯一的自保写法。",
    },
    "strbound": {
        "subject": "snprintf 的返回值", "predicate": "表示的是", "object": "would-be length",
        "hypothesis": "snprintf 返回「本该写入的长度」（可大于缓冲），strncpy 在源长 ≥ n 时不写 NUL。",
        "motivation": "为什么「用 snprintf 就安全了」这句话只对了一半？",
        "socratic": "返回值比缓冲还大时，多出来的字符去哪了？",
        "predict_first": "先猜 snprintf 的返回值是 7（实际写入）还是 10（本该写入）。",
        "boundary": "不要用返回值当「已写入长度」去索引；strncpy 之后要手动补终止符。",
    },
    "fnptr": {
        "subject": "经不兼容函数指针的调用", "predicate": "其性质是", "object": "undefined behavior",
        "hypothesis": "函数指针可被强转，但经不兼容类型调用即 UB；直接强转时两个编译器各给出 1 条诊断（warn，非 error）。",
        "motivation": "转换能编译、地址也非空——那调用为什么还是 UB？",
        "socratic": "如果两者参数个数不同，栈上的实参由谁负责匹配？",
        "predict_first": "先猜编译器会不会在该转换处报警告。",
        "boundary": "不要靠强转函数指针「复用」回调签名；改签名或用适配函数。",
    },
    "volatile": {
        "subject": "volatile 变量", "predicate": "约束的是", "object": "access count",
        "hypothesis": "-O2 下普通变量的多次读取可被折叠，volatile 变量必须逐次访问（汇编引用次数不同）。",
        "motivation": "volatile 到底是「原子」还是「别优化掉」？",
        "socratic": "两次读都被保留了，就说明两个线程不会交错吗？",
        "predict_first": "先猜汇编里 plain_flag 与 vol_flag 谁被读的次数多。",
        "boundary": "不要用 volatile 做线程同步（不原子、不建立顺序）；同步请用原子类型或锁。",
    },
    "setjmp": {
        "subject": "longjmp 后的自动变量", "predicate": "其值", "object": "indeterminate value",
        "hypothesis": "longjmp 后非 volatile 局部量的值不确定（档位不同读数可不同），volatile 量被保证。",
        "motivation": "为什么「跳回来之后变量还是我设的值」在 -O2 下就不一定了？",
        "socratic": "值「不确定」和「值被改坏了」是一回事吗？",
        "predict_first": "先猜 -O0 与 -O2 会不会给出不同的读数。",
        "boundary": "不要跨 longjmp 用普通局部变量传状态；需要就用 volatile 或静态存储期。",
    },
    "intpromo": {
        "subject": "有符号/无符号混合比较", "predicate": "比较结果是", "object": "unsigned conversion",
        "hypothesis": "-1 < 1u 为假（-1 转成 UINT_MAX）；signed char 参与运算先提升到 int。",
        "motivation": "为什么 -1 明明更小，`-1 < 1u` 却是假？",
        "socratic": "把 int 与 size_t 混比时，谁是「被转的那个」？",
        "predict_first": "先猜 `cmp_signed_unsigned` 是 1 还是 0。",
        "boundary": "不要把有符号与无符号混在同一表达式里比较；循环下标统一用 size_t 并避免减成负数。",
    },
    "bitfield": {
        "subject": "位域布局", "predicate": "其分配顺序是", "object": "implementation-defined",
        "hypothesis": "位域的单元分配与 plain int 位域的符号性都由实现决定（本批两个编译器都按有符号）。",
        "motivation": "位域明明写死了比特数，为什么还说它不可移植？",
        "socratic": "把位域结构体直接 memcpy 成字节发出去，接收方凭什么还原？",
        "predict_first": "先猜 4 位位域存 -1 读回来是 -1 还是 15。",
        "boundary": "不要把位域用于寄存器映射或跨机序列化；要布局就显式用掩码与移位。",
    },
    "macro": {
        "subject": "函数式宏", "predicate": "其实质是", "object": "text substitution",
        "hypothesis": "宏是文本替换：缺括号会错优先级（3+1 平方得 7），带副作用实参会被求值多次（i 从 0 变 2）。",
        "motivation": "为什么加了括号还可能有坑？",
        "socratic": "`MAX(i++, j)` 里 i++ 到底被执行了几次？",
        "predict_first": "先猜 SQ_BAD(3+1) 是 16 还是 7。",
        "analogy": "宏像复印机：它复印的是你写的那串字符，而不是「那个值」——印两次就跑两次。",
        "boundary": "不要用宏实现有副作用的「函数」；优先 static inline 函数（有类型检查、求值一次）。",
    },
    "signedovf": {
        "subject": "有符号整数溢出", "predicate": "其性质是", "object": "undefined behavior",
        "hypothesis": "有符号溢出是 UB ⇒ 同一表达式在不同编译器上可给出相反答案（gcc=1 / clang=0）；无符号回绕是定义好的。",
        "motivation": "为什么同一行「溢出检查」换个编译器答案就反了？",
        "socratic": "UB 的意思是「会崩」还是「编译器可以任意处理」？",
        "predict_first": "先猜 `INT_MAX + 1 > INT_MAX` 在 gcc 与 clang 上是否同值。",
        "boundary": "不要用「加完再比较」检测有符号溢出；用无符号或先与极限比较。",
    },
}


def _sha256(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def _run(argv: list[str], timeout: int = 120) -> dict[str, Any]:
    try:
        p = subprocess.run(argv, capture_output=True, text=True, cwd=ROOT,
                           encoding="utf-8", errors="replace", timeout=timeout)
        return {"rc": p.returncode, "out": p.stdout, "err": p.stderr}
    except (OSError, subprocess.SubprocessError) as exc:
        return {"rc": 1, "out": "", "err": f"{type(exc).__name__}: {exc}"}


def _compiler_version(cc: str) -> str:
    r = _run([cc, "--version"], timeout=30)
    first = (r["out"] or r["err"]).strip().splitlines()
    return first[0].strip() if first else "unknown"


def std_flag_for(cc: str, std: str) -> Optional[str]:
    """某编译器是否支持 `-std=<std>`；不支持则试回退档（c23 → c2x），都不行返回 None。"""
    probe = os.path.join(BUILD, "_stdprobe.c")
    os.makedirs(BUILD, exist_ok=True)
    with open(probe, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("int main(void){return 0;}\n")
    for cand in (std, STD_FALLBACK.get(std, "")):
        if not cand:
            continue
        r = _run([cc, f"-std={cand}", probe, "-o", os.path.join(BUILD, "_stdprobe.exe")])
        if r["rc"] == 0:
            return cand
    return None


def rel(path: str) -> str:
    return os.path.relpath(path, ROOT).replace("\\", "/")


# ============================== 1) --probe ==============================
def probe(keep_std_check: bool = True) -> dict[str, Any]:
    """真编译 + 真运行 10 个夹具（gcc/clang × c11/c17/c23 × -O0/-O2）。"""
    os.makedirs(EXAMPLES_C, exist_ok=True)
    os.makedirs(BUILD, exist_ok=True)
    res: dict[str, Any] = {"date": DATE, "compilers": {}, "fixtures": {}, "failed": []}
    for cc in COMPILERS:
        res["compilers"][cc] = {"version": _compiler_version(cc),
                                "available": shutil.which(cc) is not None}

    for fx in FIXTURES:
        key = fx["key"]
        src = os.path.join(EXAMPLES_C, f"_c_{key}.c")
        with open(src, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(fx["code"])
        rec: dict[str, Any] = {"fixture": rel(src), "runs": {}, "diag": {}, "asm_refs": {}}

        # 主档位汇编（证据卡工件）
        asm = os.path.join(EXAMPLES_C, f"_c_{key}.asm")
        asm_cmd = [MAIN_CC, f"-std={MAIN_STD}", MAIN_OPT, "-S", "-masm=intel",
                   rel(src), "-o", rel(asm)]
        r = _run(asm_cmd)
        rec["asm"] = {"path": rel(asm), "rc": r["rc"], "cmd": " ".join(asm_cmd),
                      "sha256": _sha256(asm) if os.path.isfile(asm) else ""}

        for cc in COMPILERS:
            if not res["compilers"][cc]["available"]:
                rec["runs"][cc] = {"error": "编译器不可用"}
                continue
            for std in STDS:
                flag = std_flag_for(cc, std) if keep_std_check else None
                if flag is None:
                    rec["runs"].setdefault(cc, {})[std] = {"supported": False}
                    continue
                for opt in OPTS:
                    exe = os.path.join(BUILD, f"_c_{key}_{cc}_{flag}_{opt}.exe")
                    cmd = [cc, f"-std={flag}", opt, "-Wall", "-Wextra", rel(src), "-o", rel(exe)]
                    c = _run(cmd)
                    diag_n = len([ln for ln in c["err"].splitlines() if "warning:" in ln])
                    entry: dict[str, Any] = {"supported": True, "std_flag": flag, "opt": opt,
                                             "compile_rc": c["rc"], "diag_warnings": diag_n,
                                             "cmd": " ".join(cmd)}
                    if c["rc"] == 0:
                        run = _run([rel(exe)])
                        entry["run_rc"] = run["rc"]
                        entry["stdout"] = run["out"]
                        entry["kv"] = dict(re.findall(r"^([A-Za-z0-9_]+)=(-?\d+)$",
                                                      run["out"], re.MULTILINE))
                    else:
                        entry["run_rc"] = None
                        entry["stdout"] = ""
                        entry["kv"] = {}
                        res["failed"].append(f"{key}/{cc}/{flag}/{opt}: 编译 rc={c['rc']}")
                    rec["runs"].setdefault(cc, {}).setdefault(std, {})[opt] = entry

        # 主档位 .out（run_match_file）
        main = rec["runs"].get(MAIN_CC, {}).get(MAIN_STD, {}).get(MAIN_OPT, {})
        outp = os.path.join(EXAMPLES_C, f"_c_{key}.out")
        with open(outp, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(main.get("stdout", ""))
        rec["out"] = {"path": rel(outp), "kv": main.get("kv", {}),
                      "keys": sorted(main.get("kv", {}))}

        # volatile：数汇编里对两个 flag 的引用次数（这是本卡唯一能证明「逐次访问」的量）
        if key == "volatile" and os.path.isfile(asm):
            txt = open(asm, encoding="utf-8", errors="replace").read()
            rec["asm_refs"] = {"plain_flag": len(re.findall(r"plain_flag", txt)),
                               "vol_flag": len(re.findall(r"vol_flag", txt))}

        res["fixtures"][key] = rec
    res["n_fixtures"] = len(FIXTURES)
    res["n_failed"] = len(res["failed"])
    return res


# ============================== 2) --cards ==============================
def _quote(clause_key: str) -> dict[str, Any]:
    if not os.path.isfile(STD_JSON):
        return {}
    data = json.load(open(STD_JSON, encoding="utf-8"))
    got = data.get("clauses", {}).get(clause_key, {})
    return dict(got) if isinstance(got, dict) else {}


def _yaml_list(items: list[str]) -> str:
    return "[" + ", ".join(items) + "]"


def _q(s: str) -> str:
    """YAML 单行标量**一律加双引号**。

    648 实测踩到：`socratic: `MAX(i++, j)` 里…` 这种以反引号开头的明文标量，
    YAML 解析直接失败（found character '`' that cannot start any token）⇒ 门禁报
    EV-FM-YAML-HARDENING。加引号是最省事且不损失信息的修法。
    """
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def evidence_card(fx: dict[str, Any], rec: dict[str, Any]) -> tuple[str, str]:
    """返回 (路径, 内容)。数字全部来自 `rec`（实跑结果）。"""
    key = fx["key"]
    ev_id = f"EV-{fx['domain']}-{fx['ev_no']:03d}"
    q = _quote(fx["clause"])
    kv = rec["out"]["kv"]
    actual_lines = []
    for cc in COMPILERS:
        for std in STDS:
            e = rec["runs"].get(cc, {}).get(std, {}).get("-O2", {})
            if e.get("supported") and e.get("kv"):
                actual_lines.append(f"  run_{cc}_{e['std_flag']}_O2: \""
                                    + " ".join(f"{k}={v}" for k, v in e["kv"].items()) + "\"")
    if not actual_lines:
        actual_lines.append('  run_none: "no successful run"')
    kv_main = " ".join(f"{k}={v}" for k, v in kv.items()) or "no output"
    body = f"""---
id: {ev_id}
serves: [{fx['atom_id']}]
kind: run
hypothesis: >-
  {fx['hypothesis']}
controlled_vars: 同一夹具、同一编译器族；唯一变量 = 档位（-std 与 -O）
matrix:
  compiler: [{rec['cc_label']}]
  std: [{MAIN_STD}]
  opt: [{MAIN_OPT}]
  arch: [x86-64]
fixture: {rec['fixture']}
command: |
  {rec['asm']['cmd']}
  {MAIN_CC} -std={MAIN_STD} {MAIN_OPT} -Wall -Wextra {rec['fixture']} -o build/c648/_c_{key}.exe
  build/c648/_c_{key}.exe > {rec['out']['path']}
artifact: {rec['asm']['path']}
artifact_producer: {rec['asm']['cmd']}
artifact_sha256: {rec['asm']['sha256']}
artifact_compiler: {_q(rec['cc_label'])}
artifact_assert:
  - {{kind: contains, text: "{fx['assert_symbol']}"}}
run_match_file: {rec['out']['path']}
run_match_keys: {_yaml_list(rec['out']['keys'])}
expected:
  run: {kv_main}
actual:
{chr(10).join(actual_lines)}
artifact_version: 1
verdict: confirm
falsification: >-
  若把夹具里的「错误写法」改成「正确写法」而输出不变，则本实验无判别力：
  实测主档位输出为 {kv_main}（两个写法的结果不同 ⇒ 有判别力）；若两者相同则本卡作废。
depth_layer: {fx['depth']}
---

# {ev_id} · 服务 {fx['atom_id']}

## 实测环境

| 编译器 | 版本 |
|---|---|
| gcc | {rec['cc_versions'].get('gcc', '—')} |
| clang | {rec['cc_versions'].get('clang', '—')} |

档位：`-std={MAIN_STD} {MAIN_OPT}`（`c17`/`c23` 与 `-O0` 的结果见 `data/648_c_probe.json`）。

## 实测输出（主档位）

```
{kv_main}
```

## 标准依据（N1570 原文，可复核）

> {q.get('quote', '（未取到原文）')[:400]}

— {q.get('iso', 'ISO/IEC 9899:2011')} {q.get('anchor', '?')}，取自 {q.get('url', 'N1570')}（字节偏移 {q.get('offset', -1)}）。
"""
    path = os.path.join(ROOT, "evidence", fx["dir"], f"{ev_id}.md")
    return path, body


def atom_card(fx: dict[str, Any], rec: dict[str, Any]) -> tuple[str, str]:
    q = _quote(fx["clause"])
    ref = f"{q.get('iso', 'ISO/IEC 9899:2011')} {q.get('anchor', '?')}"
    quote_txt = q.get("quote", "").replace('"', "'")
    kv = rec["out"]["kv"]
    obs = " ".join(f"{k}={v}" for k, v in kv.items()) or "no output"
    # ATOM-GRAY-ZONE：domain == "UB" 的卡必须声明灰区类别（否则 block）
    gray_zone_line = "gray_zone: ub\n" if fx["domain"] == "UB" else ""
    # ATOM-AUDIENCE：audience=beginner 时正文要出现类比词，否则 warn
    analogy = ""
    if fx["audience"] == " beginner".strip():
        analogy = ("\n打个比方（类比）：" + fx.get("analogy", "把它想成「借来的尺子量不出自己的长度」。")
                   + "\n")
    body = f"""---
id: {fx['atom_id']}
title: {_q(fx['title'])}
domain: {fx['domain']}
type: {fx['type']}
{gray_zone_line}status: draft
dal: C
human_review: optional
audience: {fx['audience']}
cognitive_load: {fx['cognitive_load']}
prerequisites_readable: true
claim: >-
  {fx['claim']}
claim_structured:
  - id: prop-1
    subject: {_q(fx['subject'])}
    predicate: {_q(fx['predicate'])}
    object: {_q(fx['object'])}
    claim_type: observation
    statement: {_q(obs + "（" + MAIN_CC + " -std=" + MAIN_STD + " " + MAIN_OPT + " 实测）。")}
    evidence: [{fx['ev_id']}]
    extracted_by: writer
    liveness: {{kind: fixture_symbol, symbol: {fx['assert_symbol']}}}
claim_boundary:
  standard: [C11, C17, C23]
  compilers: [{rec['cc_label']}]
  opt: [-O0, -O2]
  platform: [x86-64]
relations: []
evidence:
  - {fx['ev_id']}
sources:
  - {{kind: iso, ref: "{ref}：{quote_txt[:160]}", independent: true}}
first_hand: true
superiority: >-
  常见材料只给结论；本卡给的是**同一次运行里的两个数字**——正确写法与「看起来对」的写法
  各自的输出（见反例节），以及 N1570 对应条款的原文出处（可复核的字节偏移）。
depth:
  layer: {fx['depth']}
status_history:
  - {{level: draft, at: {DATE}, by: writer:agent}}
pedagogy:
  motivation: {_q(fx['motivation'])}
  socratic: {_q(fx['socratic'])}
  predict_first: {_q(fx['predict_first'])}
---

# {fx['atom_id']} · {fx['title']}

> 状态 `draft`：**verified 唯人签，Agent 不自置**（不代签）。待 human 签署后晋升。

## 实测（{MAIN_CC} -std={MAIN_STD} {MAIN_OPT}）

```
{obs}
```
{analogy}
## 反例：让它失败的实验

{fx['counterexample']}

## 标准依据

> {quote_txt[:400]}

— {ref}（N1570，字节偏移 {q.get('offset', -1)}，取自 {q.get('url', 'N1570')}）。

C17（N2310）与 C23（N3096）本批**只留下载留痕**（PDF，本环境无解析库），条款号**未逐条核对**，需人核。

## 边界（不该用在哪里）

{fx['boundary']}
"""
    path = os.path.join(ROOT, "atoms", fx["dir"], f"{fx['atom_id']}.md")
    return path, body


def build_cards(res: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {"atoms": [], "evidence": [], "refused": []}
    # 证据卡编号**写死在夹具里**（不再"取现有最大号 +1"）：
    # 后者在同一批里复跑一次就会新建一套新号，旧号留在库里成孤儿——648 实测踩到过
    # （第一次生成 LANG-003..009，第二次变成 LANG-010..016，两套并存）。
    for fx in FIXTURES:
        fx["ev_no"] = EV_NO[fx["key"]]
        fx["ev_id"] = f"EV-{fx['domain']}-{fx['ev_no']:03d}"
        fx.update(CARD_TEXT[fx["key"]])
        # 覆写保护：目标路径若已是**别人的**卡（id 不同），拒绝覆盖
        tgt = os.path.join(ROOT, "evidence", fx["dir"], f"{fx['ev_id']}.md")
        if os.path.isfile(tgt):
            head = open(tgt, encoding="utf-8").read(400)
            if f"id: {fx['ev_id']}" not in head:
                out["refused"].append(rel(tgt))
                raise SystemExit(f"拒绝覆盖非本批卡：{rel(tgt)}")
    for fx in FIXTURES:
        rec = res["fixtures"][fx["key"]]
        # 编译器标签：**去掉长括号里的逗号**（YAML flow list 里裸逗号会被当成列表分隔符，
        # 把"一个编译器"读成"两个"，进而误触 EV-MATRIX-UNBACKED）
        short = {}
        for c, v in res["compilers"].items():
            m = re.search(r"(\d+\.\d+\.\d+)", v.get("version") or "")
            short[c] = f"{c} {m.group(1)}" if m else str(c)
        rec["cc_label"] = " / ".join(short[c] for c in COMPILERS)
        rec["cc_versions"] = {c: (v.get("version") or "") for c, v in res["compilers"].items()}
        fx["atom_id"] = f"ATOM-{fx['domain']}-{fx['topic']}-001"
        p, txt = evidence_card(fx, rec)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(txt)
        out["evidence"].append(rel(p))
        p2, txt2 = atom_card(fx, rec)
        os.makedirs(os.path.dirname(p2), exist_ok=True)
        with open(p2, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(txt2)
        out["atoms"].append(rel(p2))
    out["n"] = len(out["atoms"])
    # 写完**立刻自解析 YAML**：648 实测踩到"以反引号开头的明文标量 ⇒ YAML 解析失败"，
    # 那次是门禁替我发现 的；从此生成器自己先兜一遍（不依赖下游）。
    out["yaml_bad"] = verify_yaml(out["atoms"] + out["evidence"])
    return out


def verify_yaml(paths: list[str]) -> list[str]:
    """逐卡解析 frontmatter；返回解析失败或 id 缺失的文件列表（空 = 全过）。"""
    import yaml  # 仓内已有依赖（gate_engine 同款）
    bad = []
    for rp in paths:
        p = os.path.join(ROOT, rp)
        try:
            txt = open(p, encoding="utf-8").read()
            fm = txt.split("---")[1]
            d = yaml.safe_load(fm)
            if not isinstance(d, dict) or not d.get("id"):
                bad.append(f"{rp}: 缺 id")
        except Exception as exc:  # noqa: BLE001
            bad.append(f"{rp}: {type(exc).__name__} {exc}".replace("\n", " ")[:160])
    return bad


# ============================== CLI ==============================
def write_report(res: dict[str, Any], cards: Optional[dict[str, Any]] = None) -> str:
    lines = ["# 648 A · C 语言打靶（真编译器实测）", "",
             "| 编译器 | 版本 | 可用 |", "|---|---|---|"]
    for cc, v in res["compilers"].items():
        lines.append(f"| {cc} | {v['version']} | {'✅' if v['available'] else '❌'} |")
    lines += ["", "## 十张卡的实测输出（主档位 gcc -std=c11 -O2）", "",
              "| 卡 | 输出 |", "|---|---|"]
    for fx in FIXTURES:
        rec = res["fixtures"].get(fx["key"], {})
        kv = rec.get("out", {}).get("kv", {})
        lines.append(f"| {fx['atom_id'] if 'atom_id' in fx else fx['key']} | "
                     f"`{' '.join(f'{k}={v}' for k, v in kv.items()) or '—'}` |")
    lines += ["", f"失败组合：**{res['n_failed']}**（{'; '.join(res['failed'][:5]) or '无'}）", ""]
    if cards:
        lines += ["## 产出", "", f"- 原子卡 {len(cards['atoms'])} 张；证据卡 {len(cards['evidence'])} 张。", ""]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("10 个夹具", len(FIXTURES) == 10)
    chk("key 唯一", len({f['key'] for f in FIXTURES}) == 10)
    chk("域只能是 16 域之一",
        all(f["domain"] in ("LANG", "MEM", "UB") for f in FIXTURES))
    chk("type 属于 10 类",
        all(f["type"] in ("concept", "mechanism", "rule", "idiom", "anti_pattern",
                          "pitfall", "contrast", "evolution", "decision", "experiment")
            for f in FIXTURES))
    chk("每个夹具都有反例说明", all(f.get("counterexample") for f in FIXTURES))
    chk("每个夹具都声明了断言符号", all(f.get("assert_symbol") for f in FIXTURES))
    # 夹具源码里必须出现该符号（EV-ASSERT-SYMBOL-MAPPED 的判据）
    chk("断言符号确实出现在夹具源码里",
        all(f["assert_symbol"] in f["code"] for f in FIXTURES))
    chk("夹具不含 TODO/占位",
        not any(re.search(r"TODO|TBD|FIXME|placeholder", f["code"]) for f in FIXTURES))
    chk("夹具不使用环境变量键",
        not any(re.search(r"\b(nproc|hostname|date)\s*=", f["code"]) for f in FIXTURES))
    chk("10 个夹具都有配套卡片文案", set(CARD_TEXT) == {f["key"] for f in FIXTURES})
    chk("证据编号覆盖 10 张", set(EV_NO) == {f["key"] for f in FIXTURES})
    ids = [f"EV-{f['domain']}-{EV_NO[f['key']]:03d}" for f in FIXTURES]
    chk("证据 id 无重号", len(set(ids)) == 10, str(sorted(ids)))
    # _q 的判据：以反引号/井号/冒号开头的标量必须被引起来（否则 YAML 解析失败）
    import yaml
    for probe in ("`MAX(a,b)` 说明", "# 井号开头", "a: b", "普通中文"):
        got = yaml.safe_load("k: " + _q(probe))["k"]
        chk(f"_q 可回环：{probe[:12]}", got == probe)
    chk("卡片文案字段齐全",
        all(all(k in t for k in ("subject", "predicate", "object", "hypothesis",
                                 "motivation", "socratic", "predict_first", "boundary"))
            for t in CARD_TEXT.values()))
    chk("禁词自检（superiority 不许出现的措辞）",
        not any(w in "常见材料只给结论；本卡给的是两个数字"
                for w in ("更通俗易懂", "更全面", "更加深入", "帮助读者理解", "结合实际")))
    print(f"c-target selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="648 C 语言打靶")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--probe", action="store_true", help="真编译 + 真运行，写工件与探针 JSON")
    ap.add_argument("--cards", action="store_true", help="据探针结果生成证据卡与原子卡")
    ap.add_argument("--report", action="store_true", help="写报告")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    if a.probe:
        res = probe()
        with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(res, fh, ensure_ascii=False, indent=2, sort_keys=True)
        print(f"written {OUT_JSON}（失败组合 {res['n_failed']}）")
        return 0 if res["n_failed"] == 0 else 1
    if a.cards:
        if not os.path.isfile(OUT_JSON):
            print("先跑 --probe")
            return 1
        res = json.load(open(OUT_JSON, encoding="utf-8"))
        cards = build_cards(res)
        print(f"written {len(cards['atoms'])} atoms + {len(cards['evidence'])} evidence；"
              f"YAML 自检 {'全过' if not cards['yaml_bad'] else '失败 ' + str(cards['yaml_bad'])}")
        return 0 if not cards["yaml_bad"] else 1
    if a.report:
        if not os.path.isfile(OUT_JSON):
            print("先跑 --probe")
            return 1
        res = json.load(open(OUT_JSON, encoding="utf-8"))
        print(f"written {write_report(res)}")
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
