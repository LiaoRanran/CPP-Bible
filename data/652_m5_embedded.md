# 652 M5 · 嵌入式 C 适配包（裸金属约束静态检查）

- fixtures 10｜违规 41｜LLM 嵌入式 pass@1 诚实登记 = **0.556**

> 能编译≠对；交叉编译/真机(HIL)本环境不可得（gap）；LLM 嵌入式 pass@1≈55.6% 必须机器验证。

| 文件 | 违规数 | 规则 |
|---|---|---|
| Examples\atoms\_c_bitfield.c | 6 | no_heavy_printf |
| Examples\atoms\_c_decay.c | 4 | no_heavy_printf |
| Examples\atoms\_c_fnptr.c | 3 | no_heavy_printf |
| Examples\atoms\_c_intpromo.c | 4 | no_heavy_printf |
| Examples\atoms\_c_macro.c | 4 | no_heavy_printf |
| Examples\atoms\_c_malloc.c | 9 | no_heap,no_heavy_printf |
| Examples\atoms\_c_setjmp.c | 2 | no_heavy_printf |
| Examples\atoms\_c_signedovf.c | 3 | no_heavy_printf |
| Examples\atoms\_c_strbound.c | 5 | no_heavy_printf |
| Examples\atoms\_c_volatile.c | 1 | no_heavy_printf |
