---
id: EV-LANG-009
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
  build/c648/_c_macro.exe > Examples/atoms/_c_macro.out
artifact: Examples/atoms/_c_macro.asm
artifact_producer: gcc -std=c11 -O2 -S -masm=intel Examples/atoms/_c_macro.c -o Examples/atoms/_c_macro.asm
artifact_sha256: eca0a33e9d346dd6bcc18b2aef8418646cfe1b4f8a54705cc6ef97e9c33856a5
artifact_compiler: "gcc 13.1.0 / clang 22.1.8"
artifact_assert:
  - {kind: contains, text: "macro_probe"}
run_match_file: Examples/atoms/_c_macro.out
run_match_keys: [i_after, max_bad_result, sq_bad, sq_good]
expected:
  run: i_after=2 max_bad_result=1 sq_bad=7 sq_good=16
actual:
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
