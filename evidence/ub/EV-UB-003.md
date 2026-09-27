---
id: EV-UB-003
serves: [ATOM-UB-SIGNEDOVF-001]
kind: run
hypothesis: >-
  有符号溢出是 UB ⇒ 同一表达式在不同编译器上可给出相反答案（gcc=1 / clang=0）；无符号回绕是定义好的。
controlled_vars: 同一夹具、同一编译器族；唯一变量 = 档位（-std 与 -O）
matrix:
  compiler: [gcc 13.1.0 / clang 22.1.8]
  std: [c11]
  opt: [-O2]
  arch: [x86-64]
fixture: Examples/atoms/_c_signedovf.c
command: |
  gcc -std=c11 -O2 -S -masm=intel Examples/atoms/_c_signedovf.c -o Examples/atoms/_c_signedovf.asm
  gcc -std=c11 -O2 -Wall -Wextra Examples/atoms/_c_signedovf.c -o build/c648/_c_signedovf.exe
  build/c648/_c_signedovf.exe > Examples/atoms/_c_signedovf.out
artifact: Examples/atoms/_c_signedovf.asm
artifact_producer: gcc -std=c11 -O2 -S -masm=intel Examples/atoms/_c_signedovf.c -o Examples/atoms/_c_signedovf.asm
artifact_sha256: 685393cbc5fe1961d2c28e312b7479ad26e6472fd916d5c6638332a58e671065
artifact_compiler: "gcc 13.1.0 / clang 22.1.8"
artifact_assert:
  - {kind: contains, text: "signedovf_probe"}
run_match_file: Examples/atoms/_c_signedovf.out
run_match_keys: [signed_plus1_gt, unsigned_plus1_gt, unsigned_wrapped]
expected:
  run: signed_plus1_gt=1 unsigned_plus1_gt=0 unsigned_wrapped=0
actual:
  run_gcc_c11_O2: "signed_plus1_gt=1 unsigned_plus1_gt=0 unsigned_wrapped=0"
  run_gcc_c17_O2: "signed_plus1_gt=1 unsigned_plus1_gt=0 unsigned_wrapped=0"
  run_gcc_c2x_O2: "signed_plus1_gt=1 unsigned_plus1_gt=0 unsigned_wrapped=0"
  run_clang_c11_O2: "signed_plus1_gt=0 unsigned_plus1_gt=0 unsigned_wrapped=0"
  run_clang_c17_O2: "signed_plus1_gt=0 unsigned_plus1_gt=0 unsigned_wrapped=0"
  run_clang_c23_O2: "signed_plus1_gt=0 unsigned_plus1_gt=0 unsigned_wrapped=0"
artifact_version: 1
verdict: confirm
falsification: >-
  若把夹具里的「错误写法」改成「正确写法」而输出不变，则本实验无判别力：
  实测主档位输出为 signed_plus1_gt=1 unsigned_plus1_gt=0 unsigned_wrapped=0（两个写法的结果不同 ⇒ 有判别力）；若两者相同则本卡作废。
depth_layer: compiler
---

# EV-UB-003 · 服务 ATOM-UB-SIGNEDOVF-001

## 实测环境

| 编译器 | 版本 |
|---|---|
| gcc | gcc (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0 |
| clang | clang version 22.1.8 (https://github.com/msys2/MINGW-packages 6e4e79c2f86eeb534e324e583f2057dc9fd5ecab) |

档位：`-std=c11 -O2`（`c17`/`c23` 与 `-O0` 的结果见 `data/648_c_probe.json`）。

## 实测输出（主档位）

```
signed_plus1_gt=1 unsigned_plus1_gt=0 unsigned_wrapped=0
```

## 标准依据（N1570 原文，可复核）

> If an exceptional condition occurs during the evaluation of an expression (that is, if the result is not mathematically defined or not in the range of representable values for its type), the behavior is undefined.

— ISO/IEC 9899:2011 6.5p5，取自 https://port70.net/~nsz/c/c11/n1570.html#6.5p5（字节偏移 257122）。
