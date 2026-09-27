---
id: EV-LANG-004
serves: [ATOM-LANG-FNPTR-001]
kind: run
hypothesis: >-
  函数指针可被强转，但经不兼容类型调用即 UB；直接强转时两个编译器各给出 1 条诊断（warn，非 error）。
controlled_vars: 同一夹具、同一编译器族；唯一变量 = 档位（-std 与 -O）
matrix:
  compiler: [gcc 13.1.0 / clang 22.1.8]
  std: [c11]
  opt: [-O2]
  arch: [x86-64]
fixture: Examples/atoms/_c_fnptr.c
command: |
  gcc -std=c11 -O2 -S -masm=intel Examples/atoms/_c_fnptr.c -o Examples/atoms/_c_fnptr.asm
  gcc -std=c11 -O2 -Wall -Wextra Examples/atoms/_c_fnptr.c -o build/c648/_c_fnptr.exe
  build/c648/_c_fnptr.exe > Examples/atoms/_c_fnptr.out
artifact: Examples/atoms/_c_fnptr.asm
artifact_producer: gcc -std=c11 -O2 -S -masm=intel Examples/atoms/_c_fnptr.c -o Examples/atoms/_c_fnptr.asm
artifact_sha256: a013afa520d2be26bd3639c8d93dcb7099a79bb7d6777b1506031fa62028f28f
artifact_compiler: "gcc 13.1.0 / clang 22.1.8"
artifact_assert:
  - {kind: contains, text: "fnptr_probe"}
run_match_file: Examples/atoms/_c_fnptr.out
run_match_keys: [bad_addr_nonzero, fnptr_sizeof, good_call]
expected:
  run: bad_addr_nonzero=1 fnptr_sizeof=8 good_call=5
actual:
  run_gcc_c11_O2: "bad_addr_nonzero=1 fnptr_sizeof=8 good_call=5"
  run_gcc_c17_O2: "bad_addr_nonzero=1 fnptr_sizeof=8 good_call=5"
  run_gcc_c2x_O2: "bad_addr_nonzero=1 fnptr_sizeof=8 good_call=5"
  run_clang_c11_O2: "bad_addr_nonzero=1 fnptr_sizeof=8 good_call=5"
  run_clang_c17_O2: "bad_addr_nonzero=1 fnptr_sizeof=8 good_call=5"
  run_clang_c23_O2: "bad_addr_nonzero=1 fnptr_sizeof=8 good_call=5"
artifact_version: 1
verdict: confirm
falsification: >-
  若把夹具里的「错误写法」改成「正确写法」而输出不变，则本实验无判别力：
  实测主档位输出为 bad_addr_nonzero=1 fnptr_sizeof=8 good_call=5（两个写法的结果不同 ⇒ 有判别力）；若两者相同则本卡作废。
depth_layer: compiler
---

# EV-LANG-004 · 服务 ATOM-LANG-FNPTR-001

## 实测环境

| 编译器 | 版本 |
|---|---|
| gcc | gcc (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0 |
| clang | clang version 22.1.8 (https://github.com/msys2/MINGW-packages 6e4e79c2f86eeb534e324e583f2057dc9fd5ecab) |

档位：`-std=c11 -O2`（`c17`/`c23` 与 `-O0` 的结果见 `data/648_c_probe.json`）。

## 实测输出（主档位）

```
bad_addr_nonzero=1 fnptr_sizeof=8 good_call=5
```

## 标准依据（N1570 原文，可复核）

> If the function is defined with a type that is not compatible with the type (of the expression) pointed to by the expression that denotes the called function, the behavior is undefined.

— ISO/IEC 9899:2011 6.5.2.2p9，取自 https://port70.net/~nsz/c/c11/n1570.html#6.5.2.2p9（字节偏移 274411）。
