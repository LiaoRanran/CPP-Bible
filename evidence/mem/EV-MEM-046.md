---
id: EV-MEM-046
verified_at: 2026-09-27
serves: [ATOM-MEM-MALLOC-001]
kind: run
hypothesis: >-
  free 释放空间但不清空指针变量；free(NULL) 是空操作；malloc(0) 可为非 NULL。
controlled_vars: 同一夹具、同一编译器族；唯一变量 = 档位（-std 与 -O）
matrix:
  compiler: [gcc 13.1.0 / clang 22.1.8]
  std: [c11]
  opt: [-O2]
  arch: [x86-64]
fixture: Examples/atoms/_c_malloc.c
command: |
  gcc -std=c11 -O2 -S -masm=intel Examples/atoms/_c_malloc.c -o Examples/atoms/_c_malloc.asm
  gcc -std=c11 -O2 -Wall -Wextra Examples/atoms/_c_malloc.c -o build/c648/_c_malloc.exe
  build/c648/_c_malloc.exe > Examples/atoms/_c_malloc.out
artifact: Examples/atoms/_c_malloc.asm
artifact_producer: gcc -std=c11 -O2 -S -masm=intel Examples/atoms/_c_malloc.c -o Examples/atoms/_c_malloc.asm
artifact_sha256: b375bd2a05cd1a6737e185ea2f9767883b9ecbf3efad20b99e18d7c4696d72f5
artifact_compiler: "gcc 13.1.0 / clang 22.1.8"
artifact_assert:
  - {kind: contains, text: "malloc_lifecycle_probe"}
run_match_file: Examples/atoms/_c_malloc.out
run_match_keys: [alloc_aligned, dangling_value_nonzero, malloc0_null, reached_after_free_null]
expected:
  run: alloc_aligned=1 dangling_value_nonzero=1 malloc0_null=0 reached_after_free_null=1
actual:
  run_gcc_c11_O2: "alloc_aligned=1 dangling_value_nonzero=1 malloc0_null=0 reached_after_free_null=1"
  run_gcc_c17_O2: "alloc_aligned=1 dangling_value_nonzero=1 malloc0_null=0 reached_after_free_null=1"
  run_gcc_c2x_O2: "alloc_aligned=1 dangling_value_nonzero=1 malloc0_null=0 reached_after_free_null=1"
  run_clang_c11_O2: "alloc_aligned=1 dangling_value_nonzero=1 malloc0_null=0 reached_after_free_null=1"
  run_clang_c17_O2: "alloc_aligned=1 dangling_value_nonzero=1 malloc0_null=0 reached_after_free_null=1"
  run_clang_c23_O2: "alloc_aligned=1 dangling_value_nonzero=1 malloc0_null=0 reached_after_free_null=1"
artifact_version: 1
verdict: confirm
falsification: >-
  若把夹具里的「错误写法」改成「正确写法」而输出不变，则本实验无判别力：
  实测主档位输出为 alloc_aligned=1 dangling_value_nonzero=1 malloc0_null=0 reached_after_free_null=1（两个写法的结果不同 ⇒ 有判别力）；若两者相同则本卡作废。
depth_layer: runtime
---

# EV-MEM-046 · 服务 ATOM-MEM-MALLOC-001

## 实测环境

| 编译器 | 版本 |
|---|---|
| gcc | gcc (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0 |
| clang | clang version 22.1.8 (https://github.com/msys2/MINGW-packages 6e4e79c2f86eeb534e324e583f2057dc9fd5ecab) |

档位：`-std=c11 -O2`（`c17`/`c23` 与 `-O0` 的结果见 `data/648_c_probe.json`）。

## 实测输出（主档位）

```
alloc_aligned=1 dangling_value_nonzero=1 malloc0_null=0 reached_after_free_null=1
```

## 标准依据（N1570 原文，可复核）

> The free function causes the space pointed to by ptr to be deallocated, that is, made available for further allocation. If ptr is a null pointer, no action occurs. Otherwise, if the argument does not match a pointer earlier returned by a memory management function, or if the space has been deallocated by a call to free or realloc, the behavior is undefined.

— ISO/IEC 9899:2011 7.22.3.3p2，取自 https://port70.net/~nsz/c/c11/n1570.html#7.22.3.3p2（字节偏移 958873）。
