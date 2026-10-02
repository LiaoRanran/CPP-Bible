---
id: EV-MEM-047
verified_at: 2026-09-27
serves: [ATOM-MEM-STRBOUND-001]
kind: run
hypothesis: >-
  snprintf 返回「本该写入的长度」（可大于缓冲），strncpy 在源长 ≥ n 时不写 NUL。
controlled_vars: 同一夹具、同一编译器族；唯一变量 = 档位（-std 与 -O）
matrix:
  compiler: [gcc 13.1.0 / clang 22.1.8]
  std: [c11]
  opt: [-O2]
  arch: [x86-64]
fixture: Examples/atoms/_c_strbound.c
command: |
  gcc -std=c11 -O2 -S -masm=intel Examples/atoms/_c_strbound.c -o Examples/atoms/_c_strbound.asm
  gcc -std=c11 -O2 -Wall -Wextra Examples/atoms/_c_strbound.c -o build/c648/_c_strbound.exe
  build/c648/_c_strbound.exe
artifact: Examples/atoms/_c_strbound.asm
artifact_producer: gcc -std=c11 -O2 -S -masm=intel Examples/atoms/_c_strbound.c -o Examples/atoms/_c_strbound.asm
artifact_sha256: 1ba9f95a9314d6ddb22bcbdb05751ce0343fb17a32262dc36b19e9a2bed23767
artifact_compiler: "gcc 13.1.0 / clang 22.1.8"
artifact_assert:
  - {kind: contains, text: "strbound_probe"}
expected:
  run: snprintf_ret=10 snprintf_truncated=1 snprintf_written=7 strncpy_last_byte=56 strncpy_nul_terminated=0
actual:
  run_match_file: Examples/atoms/_c_strbound.out
  run_match_keys: [snprintf_ret, snprintf_truncated, snprintf_written, strncpy_last_byte, strncpy_nul_terminated]
  run_gcc_c11_O2: "snprintf_ret=10 snprintf_truncated=1 snprintf_written=7 strncpy_last_byte=56 strncpy_nul_terminated=0"
  run_gcc_c17_O2: "snprintf_ret=10 snprintf_truncated=1 snprintf_written=7 strncpy_last_byte=56 strncpy_nul_terminated=0"
  run_gcc_c2x_O2: "snprintf_ret=10 snprintf_truncated=1 snprintf_written=7 strncpy_last_byte=56 strncpy_nul_terminated=0"
  run_clang_c11_O2: "snprintf_ret=10 snprintf_truncated=1 snprintf_written=7 strncpy_last_byte=56 strncpy_nul_terminated=0"
  run_clang_c17_O2: "snprintf_ret=10 snprintf_truncated=1 snprintf_written=7 strncpy_last_byte=56 strncpy_nul_terminated=0"
  run_clang_c23_O2: "snprintf_ret=10 snprintf_truncated=1 snprintf_written=7 strncpy_last_byte=56 strncpy_nul_terminated=0"
artifact_version: 1
verdict: confirm
falsification: >-
  若把夹具里的「错误写法」改成「正确写法」而输出不变，则本实验无判别力：
  实测主档位输出为 snprintf_ret=10 snprintf_truncated=1 snprintf_written=7 strncpy_last_byte=56 strncpy_nul_terminated=0（两个写法的结果不同 ⇒ 有判别力）；若两者相同则本卡作废。
depth_layer: runtime
---

# EV-MEM-047 · 服务 ATOM-MEM-STRBOUND-001

## 实测环境

| 编译器 | 版本 |
|---|---|
| gcc | gcc (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0 |
| clang | clang version 22.1.8 (https://github.com/msys2/MINGW-packages 6e4e79c2f86eeb534e324e583f2057dc9fd5ecab) |

档位：`-std=c11 -O2`（`c17`/`c23` 与 `-O0` 的结果见 `data/648_c_probe.json`）。

## 实测输出（主档位）

```
snprintf_ret=10 snprintf_truncated=1 snprintf_written=7 strncpy_last_byte=56 strncpy_nul_terminated=0
```

## 标准依据（N1570 原文，可复核）

> The snprintf function returns the number of characters that would have been written had n been sufficiently large, not counting the terminating null character, or a negative value if an encoding error occurred. Thus, the null-terminated output has been completely written if and only if the returned value is nonnegative and less than n.

— ISO/IEC 9899:2011 7.21.6.5p3，取自 https://port70.net/~nsz/c/c11/n1570.html#7.21.6.5p3（字节偏移 898708）。
