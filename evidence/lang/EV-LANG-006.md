---
id: EV-LANG-006
serves: [ATOM-LANG-SETJMP-001]
kind: run
hypothesis: >-
  longjmp 后非 volatile 局部量的值不确定（档位不同读数可不同），volatile 量被保证。
controlled_vars: 同一夹具、同一编译器族；唯一变量 = 档位（-std 与 -O）
matrix:
  compiler: [gcc 13.1.0 / clang 22.1.8]
  std: [c11]
  opt: [-O2]
  arch: [x86-64]
fixture: Examples/atoms/_c_setjmp.c
command: |
  gcc -std=c11 -O2 -S -masm=intel Examples/atoms/_c_setjmp.c -o Examples/atoms/_c_setjmp.asm
  gcc -std=c11 -O2 -Wall -Wextra Examples/atoms/_c_setjmp.c -o build/c648/_c_setjmp.exe
  build/c648/_c_setjmp.exe > Examples/atoms/_c_setjmp.out
artifact: Examples/atoms/_c_setjmp.asm
artifact_producer: gcc -std=c11 -O2 -S -masm=intel Examples/atoms/_c_setjmp.c -o Examples/atoms/_c_setjmp.asm
artifact_sha256: e6a7ed718fa902689d16f4d98906a8b982cc523588984680451718bada51487e
artifact_compiler: "gcc 13.1.0 / clang 22.1.8"
artifact_assert:
  - {kind: contains, text: "setjmp_probe"}
run_match_file: Examples/atoms/_c_setjmp.out
run_match_keys: [after_longjmp_plain, after_longjmp_volatile]
expected:
  run: after_longjmp_plain=0 after_longjmp_volatile=5
actual:
  run_gcc_c11_O2: "after_longjmp_plain=0 after_longjmp_volatile=5"
  run_gcc_c17_O2: "after_longjmp_plain=0 after_longjmp_volatile=5"
  run_gcc_c2x_O2: "after_longjmp_plain=0 after_longjmp_volatile=5"
  run_clang_c11_O2: "after_longjmp_plain=0 after_longjmp_volatile=5"
  run_clang_c17_O2: "after_longjmp_plain=0 after_longjmp_volatile=5"
  run_clang_c23_O2: "after_longjmp_plain=0 after_longjmp_volatile=5"
artifact_version: 1
verdict: confirm
falsification: >-
  若把夹具里的「错误写法」改成「正确写法」而输出不变，则本实验无判别力：
  实测主档位输出为 after_longjmp_plain=0 after_longjmp_volatile=5（两个写法的结果不同 ⇒ 有判别力）；若两者相同则本卡作废。
depth_layer: compiler
---

# EV-LANG-006 · 服务 ATOM-LANG-SETJMP-001

## 实测环境

| 编译器 | 版本 |
|---|---|
| gcc | gcc (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0 |
| clang | clang version 22.1.8 (https://github.com/msys2/MINGW-packages 6e4e79c2f86eeb534e324e583f2057dc9fd5ecab) |

档位：`-std=c11 -O2`（`c17`/`c23` 与 `-O0` 的结果见 `data/648_c_probe.json`）。

## 实测输出（主档位）

```
after_longjmp_plain=0 after_longjmp_volatile=5
```

## 标准依据（N1570 原文，可复核）

> All accessible objects have values, and all other components of the abstract machine 249) have state, as of the time the longjmp function was called, except that the values of objects of automatic storage duration that are local to the function containing the invocation of the corresponding setjmp macro that do not have volatile-qualified type and have been changed between the setjmp invocation an

— ISO/IEC 9899:2011 7.13.2.1p3，取自 https://port70.net/~nsz/c/c11/n1570.html#7.13.2.1p3（字节偏移 733616）。
