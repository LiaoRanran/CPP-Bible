---
id: EV-LANG-009
verified_at: 2026-09-27
serves: [ATOM-LANG-MACRO-001]
kind: run
hypothesis: >-
  宏是文本替换：缺括号会错优先级（3+1 平方得 7），带副作用实参会被求值多次（i 从 0 变 2）。
controlled_vars: 同一夹具、同一编译器族；唯一变量 = 档位（-std 与 -O）
matrix:
  compiler: [gcc 13.1.0 / clang 22.1.8]
  std: [c11]
  opt: [-O2]
  arch: [x86-64]
fixture: Examples/atoms/_c_macro.c
command: |
  gcc -std=c11 -O2 -S -masm=intel Examples/atoms/_c_macro.c -o Examples/atoms/_c_macro.asm
  gcc -std=c11 -O2 -Wall -Wextra Examples/atoms/_c_macro.c -o build/c648/_c_macro.exe
  build/c648/_c_macro.exe
artifact: Examples/atoms/_c_macro.asm
artifact_producer: gcc -std=c11 -O2 -S -masm=intel Examples/atoms/_c_macro.c -o Examples/atoms/_c_macro.asm
artifact_sha256: eca0a33e9d346dd6bcc18b2aef8418646cfe1b4f8a54705cc6ef97e9c33856a5
artifact_compiler: "gcc 13.1.0 / clang 22.1.8"
artifact_assert:
  # 673q：原断言 `{kind: contains, text: "macro_probe"}` 写的是夹具里的 **static C
  # 函数名**——-O2 下被内联进 main，符号名在任何编译器产物里都不出现（连卡归属的 13.1.0
  # 工件里也没有）⇒ 原理上不可满足的坏断言。此前不红是因为 toolchain 长期等于卡归属的
  # 13.1.0 ⇒ artifact_sha 命中、断言从不被评估；650 批切到 mingw1530 GCC 15.3.0 后
  # sha 走不通、回落到结构断言，才第一次被执行 ⇒ 红。
  # 改为断言真实存在且承载 claim 的证据：① 读数键格式串（跨编译器稳定）② 关键立即数——
  # 7 = 缺括号的 SQ_BAD(3+1)（优先级错）、16 = 带括号的 SQ_GOOD、2 = MAX_BAD 的 i++
  # 被求值两次后的 i_after。这三个立即数正是本卡 hypothesis 的三条断言。
  # "mov\tedx, N" 用真实制表符（YAML 双引号 \t，参照 EV-UB-NULLDEREF-669）：断言匹配侧
  # 两侧都归一空白，而 gate_engine EV-ASSERT-SYMBOL-MAPPED 的 haystack 不归一、须逐字相同。
  # 673q 五路实测全部命中：仓库工件(13.1.0) / GCC 15.3.0 / GCC 13.1.0 / clang 22.1.8 /
  # Ubuntu gcc 13.3.0（CI 侧等价物）。
  - {kind: contains_any, texts: ["sq_bad=%d", "sq_good=%d", "max_bad_result=%d", "i_after=%d"]}
  - {kind: contains, text: "mov	edx, 7"}
  - {kind: contains, text: "mov	edx, 16"}
  - {kind: contains, text: "mov	edx, 2"}
expected:
  run: i_after=2 max_bad_result=1 sq_bad=7 sq_good=16
actual:
  run_match_file: Examples/atoms/_c_macro.out
  run_match_keys: [i_after, max_bad_result, sq_bad, sq_good]
  run_gcc_c11_O2: "i_after=2 max_bad_result=1 sq_bad=7 sq_good=16"
  run_gcc_c17_O2: "i_after=2 max_bad_result=1 sq_bad=7 sq_good=16"
  run_gcc_c2x_O2: "i_after=2 max_bad_result=1 sq_bad=7 sq_good=16"
  run_clang_c11_O2: "i_after=2 max_bad_result=1 sq_bad=7 sq_good=16"
  run_clang_c17_O2: "i_after=2 max_bad_result=1 sq_bad=7 sq_good=16"
  run_clang_c23_O2: "i_after=2 max_bad_result=1 sq_bad=7 sq_good=16"
artifact_version: 1
verdict: confirm
falsification: >-
  若把夹具里的「错误写法」改成「正确写法」而输出不变，则本实验无判别力：
  实测主档位输出为 i_after=2 max_bad_result=1 sq_bad=7 sq_good=16（两个写法的结果不同 ⇒ 有判别力）；若两者相同则本卡作废。
depth_layer: compiler
---

# EV-LANG-009 · 服务 ATOM-LANG-MACRO-001

## 实测环境

| 编译器 | 版本 |
|---|---|
| gcc | gcc (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0 |
| clang | clang version 22.1.8 (https://github.com/msys2/MINGW-packages 6e4e79c2f86eeb534e324e583f2057dc9fd5ecab) |

档位：`-std=c11 -O2`（`c17`/`c23` 与 `-O0` 的结果见 `data/648_c_probe.json`）。

## 实测输出（主档位）

```
i_after=2 max_bad_result=1 sq_bad=7 sq_good=16
```

## 标准依据（N1570 原文，可复核）

> After the arguments for the invocation of a function-like macro have been identified, argument substitution takes place. A parameter in the replacement list, unless preceded by a # or ## preprocessing token or followed by a ## preprocessing token (see below), is replaced by the corresponding argument after all macros contained therein have been expanded. Before being substituted, each argument's p

— ISO/IEC 9899:2011 6.10.3.1p1，取自 https://port70.net/~nsz/c/c11/n1570.html#6.10.3.1p1（字节偏移 505977）。
