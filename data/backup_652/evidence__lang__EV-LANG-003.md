---
id: EV-LANG-003
serves: [ATOM-LANG-DECAY-001]
kind: run
hypothesis: >-
  同一数组在调用方与被调用方的 sizeof 不同：调用方是数组字节数，函数内是指针字节数。
controlled_vars: 同一夹具、同一编译器族；唯一变量 = 档位（-std 与 -O）
matrix:
  compiler: [gcc 13.1.0 / clang 22.1.8]
  std: [c11]
  opt: [-O2]
  arch: [x86-64]
fixture: Examples/atoms/_c_decay.c
command: |
  gcc -std=c11 -O2 -S -masm=intel Examples/atoms/_c_decay.c -o Examples/atoms/_c_decay.asm
  gcc -std=c11 -O2 -Wall -Wextra Examples/atoms/_c_decay.c -o build/c648/_c_decay.exe
  build/c648/_c_decay.exe > Examples/atoms/_c_decay.out
artifact: Examples/atoms/_c_decay.asm
artifact_producer: gcc -std=c11 -O2 -S -masm=intel Examples/atoms/_c_decay.c -o Examples/atoms/_c_decay.asm
artifact_sha256: 97509b8f4bf442598807454e49eff591c65e4e8dd0917537e2fac8371d2a6e2f
artifact_compiler: "gcc 13.1.0 / clang 22.1.8"
artifact_assert:
  - {kind: contains, text: "decay_param_sizeof"}
run_match_file: Examples/atoms/_c_decay.out
run_match_keys: [decay_len_true, decay_len_wrong_inside, decay_sizeof_array, decay_sizeof_param]
expected:
  run: decay_len_true=10 decay_len_wrong_inside=2 decay_sizeof_array=40 decay_sizeof_param=8
actual:
  run_gcc_c11_O2: "decay_len_true=10 decay_len_wrong_inside=2 decay_sizeof_array=40 decay_sizeof_param=8"
  run_gcc_c17_O2: "decay_len_true=10 decay_len_wrong_inside=2 decay_sizeof_array=40 decay_sizeof_param=8"
  run_gcc_c2x_O2: "decay_len_true=10 decay_len_wrong_inside=2 decay_sizeof_array=40 decay_sizeof_param=8"
  run_clang_c11_O2: "decay_len_true=10 decay_len_wrong_inside=2 decay_sizeof_array=40 decay_sizeof_param=8"
  run_clang_c17_O2: "decay_len_true=10 decay_len_wrong_inside=2 decay_sizeof_array=40 decay_sizeof_param=8"
  run_clang_c23_O2: "decay_len_true=10 decay_len_wrong_inside=2 decay_sizeof_array=40 decay_sizeof_param=8"
artifact_version: 1
verdict: confirm
falsification: >-
  若把夹具里的「错误写法」改成「正确写法」而输出不变，则本实验无判别力：
  实测主档位输出为 decay_len_true=10 decay_len_wrong_inside=2 decay_sizeof_array=40 decay_sizeof_param=8（两个写法的结果不同 ⇒ 有判别力）；若两者相同则本卡作废。
depth_layer: compiler
---

# EV-LANG-003 · 服务 ATOM-LANG-DECAY-001

## 实测环境

| 编译器 | 版本 |
|---|---|
| gcc | gcc (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0 |
| clang | clang version 22.1.8 (https://github.com/msys2/MINGW-packages 6e4e79c2f86eeb534e324e583f2057dc9fd5ecab) |

档位：`-std=c11 -O2`（`c17`/`c23` 与 `-O0` 的结果见 `data/648_c_probe.json`）。

## 实测输出（主档位）

```
decay_len_true=10 decay_len_wrong_inside=2 decay_sizeof_array=40 decay_sizeof_param=8
```

## 标准依据（N1570 原文，可复核）

> A declaration of a parameter as ''array of type'' shall be adjusted to ''qualified pointer to type'', where the type qualifiers (if any) are those specified within the [ and ] of the array type derivation. If the keyword static also appears within the [ and ] of the array type derivation, then for each call to the function, the value of the corresponding actual argument shall provide access to the

— ISO/IEC 9899:2011 6.7.6.3p7，取自 https://port70.net/~nsz/c/c11/n1570.html#6.7.6.3p7（字节偏移 415081）。
