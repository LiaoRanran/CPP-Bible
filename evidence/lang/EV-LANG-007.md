---
id: EV-LANG-007
verified_at: 2026-09-27
serves: [ATOM-LANG-INTPROMO-001]
kind: run
hypothesis: >-
  -1 < 1u 为假（-1 转成 UINT_MAX）；signed char 参与运算先提升到 int。
controlled_vars: 同一夹具、同一编译器族；唯一变量 = 档位（-std 与 -O）
matrix:
  compiler: [gcc 13.1.0 / clang 22.1.8]
  std: [c11]
  opt: [-O2]
  arch: [x86-64]
fixture: Examples/atoms/_c_intpromo.c
command: |
  gcc -std=c11 -O2 -S -masm=intel Examples/atoms/_c_intpromo.c -o Examples/atoms/_c_intpromo.asm
  gcc -std=c11 -O2 -Wall -Wextra Examples/atoms/_c_intpromo.c -o build/c648/_c_intpromo.exe
  build/c648/_c_intpromo.exe
artifact: Examples/atoms/_c_intpromo.asm
artifact_producer: gcc -std=c11 -O2 -S -masm=intel Examples/atoms/_c_intpromo.c -o Examples/atoms/_c_intpromo.asm
artifact_sha256: 8294058c9ff42b04e033aba984fae1c6b51c017e014d0a5d4a896ca58bcff08c
artifact_compiler: "gcc 13.1.0 / clang 22.1.8"
artifact_assert:
  # 673q：原断言写的是夹具里的 **static C 函数名**（`- {kind: contains, text: "intpromo_probe"}`）。该函数在本卡 -O2
  # 档位下必然被内联进 main ⇒ 符号名在任何编译器/任何优化档的 .asm 里都不出现
  # （实测卡自己归属的 gcc 13.1.0 工件里也没有）⇒ 属**原理上不可满足**的坏断言。
  # 之所以此前不红：toolchain 长期等于卡归属的 13.1.0 ⇒ artifact_sha 命中、
  # 结构断言从不被评估；650 批把工具链切到 mingw1530 GCC 15.3.0 后 sha 走不通、
  # 回落到结构断言，这条断言才第一次被真正执行 ⇒ quality 红。
  # 改为断言工件里真实存在、且承载本卡 claim 的两类证据：
  #   ① 读数键的 printf 格式串（.rdata，跨编译器稳定，绑定期望输出的 key）
  #   ② 承载 claim 的关键立即数：200 = 100+100（整型提升后不溢出 char）、
  #      4 = sizeof(c+d)（提升到 int 的直接证据）、-1 = (unsigned)-1 的传出形态
  # 文本里的制表符是**真实 TAB**（YAML 双引号转义，仓内既有约定见
  # EV-UB-NULLDEREF-669）：check_artifact_assert 两侧都归一空白故可匹配，而
  # gate_engine EV-ASSERT-SYMBOL-MAPPED 的 haystack **不归一**、要求与产物逐字
  # 相同 ⇒ 必须写真实 TAB，不能写字面反斜杠 t。
  # 673q 五路实测全部命中：仓库已提交工件(13.1.0) / GCC 15.3.0 MinGW /
  # GCC 13.1.0 MinGW / clang 22.1.8(MSYS2) / Ubuntu gcc 13.3.0（CI 侧等价物）。
  - {kind: contains_any, texts: ["cmp_signed_unsigned=%d", "minus1_as_unsigned=%u", "char_promoted_sum=%d", "char_sum_type_size=%zu"]}
  - {kind: contains, text: "mov	edx, 200"}
  - {kind: contains, text: "mov	edx, 4"}
  - {kind: contains, text: "mov	edx, -1"}
expected:
  run: char_promoted_sum=200 char_sum_type_size=4 cmp_signed_unsigned=0 minus1_as_unsigned=4294967295
actual:
  run_match_file: Examples/atoms/_c_intpromo.out
  run_match_keys: [char_promoted_sum, char_sum_type_size, cmp_signed_unsigned, minus1_as_unsigned]
  run_gcc_c11_O2: "char_promoted_sum=200 char_sum_type_size=4 cmp_signed_unsigned=0 minus1_as_unsigned=4294967295"
  run_gcc_c17_O2: "char_promoted_sum=200 char_sum_type_size=4 cmp_signed_unsigned=0 minus1_as_unsigned=4294967295"
  run_gcc_c2x_O2: "char_promoted_sum=200 char_sum_type_size=4 cmp_signed_unsigned=0 minus1_as_unsigned=4294967295"
  run_clang_c11_O2: "char_promoted_sum=200 char_sum_type_size=4 cmp_signed_unsigned=0 minus1_as_unsigned=4294967295"
  run_clang_c17_O2: "char_promoted_sum=200 char_sum_type_size=4 cmp_signed_unsigned=0 minus1_as_unsigned=4294967295"
  run_clang_c23_O2: "char_promoted_sum=200 char_sum_type_size=4 cmp_signed_unsigned=0 minus1_as_unsigned=4294967295"
artifact_version: 1
verdict: confirm
falsification: >-
  若把夹具里的「错误写法」改成「正确写法」而输出不变，则本实验无判别力：
  实测主档位输出为 char_promoted_sum=200 char_sum_type_size=4 cmp_signed_unsigned=0 minus1_as_unsigned=4294967295（两个写法的结果不同 ⇒ 有判别力）；若两者相同则本卡作废。
depth_layer: runtime
---

# EV-LANG-007 · 服务 ATOM-LANG-INTPROMO-001

## 实测环境

| 编译器 | 版本 |
|---|---|
| gcc | gcc (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0 |
| clang | clang version 22.1.8 (https://github.com/msys2/MINGW-packages 6e4e79c2f86eeb534e324e583f2057dc9fd5ecab) |

档位：`-std=c11 -O2`（`c17`/`c23` 与 `-O0` 的结果见 `data/648_c_probe.json`）。

## 实测输出（主档位）

```
char_promoted_sum=200 char_sum_type_size=4 cmp_signed_unsigned=0 minus1_as_unsigned=4294967295
```

## 标准依据（N1570 原文，可复核）

> Many operators that expect operands of arithmetic type cause conversions and yield result types in a similar way. The purpose is to determine a common real type for the operands and result. For the specified operands, each operand is converted, without change of type domain, to a type whose corresponding real type is the common real type. Unless explicitly stated otherwise, the common real type is

— ISO/IEC 9899:2011 6.3.1.8p1，取自 https://port70.net/~nsz/c/c11/n1570.html#6.3.1.8p1（字节偏移 196616）。
