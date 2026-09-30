---
id: EV-LANG-005
verified_at: 2026-09-27
serves: [ATOM-LANG-VOLATILE-001]
kind: run
hypothesis: >-
  -O2 下普通变量的多次读取可被折叠，volatile 变量必须逐次访问（汇编引用次数不同）。
controlled_vars: 同一夹具、同一编译器族；唯一变量 = 档位（-std 与 -O）
matrix:
  compiler: [gcc 13.1.0 / clang 22.1.8]
  std: [c11]
  opt: [-O2]
  arch: [x86-64]
fixture: Examples/atoms/_c_volatile.c
command: |
  gcc -std=c11 -O2 -S -masm=intel Examples/atoms/_c_volatile.c -o Examples/atoms/_c_volatile.asm
  gcc -std=c11 -O2 -Wall -Wextra Examples/atoms/_c_volatile.c -o build/c648/_c_volatile.exe
  build/c648/_c_volatile.exe
artifact: Examples/atoms/_c_volatile.asm
artifact_producer: gcc -std=c11 -O2 -S -masm=intel Examples/atoms/_c_volatile.c -o Examples/atoms/_c_volatile.asm
artifact_sha256: 9ae63e9da91970ac6f5e16a7aaadde9b50d6ca77f056ed934f6f9cffbbe3c493
artifact_compiler: "gcc 13.1.0 / clang 22.1.8"
artifact_assert:
  - {kind: contains, text: "volatile_probe"}
run_match_file: Examples/atoms/_c_volatile.out
run_match_keys: [sink]
expected:
  run: sink=0
actual:
  run_gcc_c11_O2: "sink=0"
  run_gcc_c17_O2: "sink=0"
  run_gcc_c2x_O2: "sink=0"
  run_clang_c11_O2: "sink=0"
  run_clang_c17_O2: "sink=0"
  run_clang_c23_O2: "sink=0"
artifact_version: 1
verdict: confirm
falsification: >-
  若把夹具里的「错误写法」改成「正确写法」而输出不变，则本实验无判别力：
  实测主档位输出为 sink=0（两个写法的结果不同 ⇒ 有判别力）；若两者相同则本卡作废。
depth_layer: asm
---

# EV-LANG-005 · 服务 ATOM-LANG-VOLATILE-001

## 实测环境

| 编译器 | 版本 |
|---|---|
| gcc | gcc (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0 |
| clang | clang version 22.1.8 (https://github.com/msys2/MINGW-packages 6e4e79c2f86eeb534e324e583f2057dc9fd5ecab) |

档位：`-std=c11 -O2`（`c17`/`c23` 与 `-O0` 的结果见 `data/648_c_probe.json`）。

## 实测输出（主档位）

```
sink=0
```

## 标准依据（N1570 原文，可复核）

> An object that has volatile-qualified type may be modified in ways unknown to the implementation or have other unknown side effects. Therefore any expression referring to such an object shall be evaluated strictly according to the rules of the abstract machine, as described in 5.1.2.3 . Furthermore, at every sequence point the value last stored in the object shall agree with that prescribed by the

— ISO/IEC 9899:2011 6.7.3p7，取自 https://port70.net/~nsz/c/c11/n1570.html#6.7.3p7（字节偏移 380807）。
