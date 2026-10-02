---
id: EV-LANG-008
verified_at: 2026-09-27
serves: [ATOM-LANG-BITFIELD-001]
kind: run
hypothesis: >-
  位域的单元分配与 plain int 位域的符号性都由实现决定（本批两个编译器都按有符号）。
controlled_vars: 同一夹具、同一编译器族；唯一变量 = 档位（-std 与 -O）
matrix:
  compiler: [gcc 13.1.0 / clang 22.1.8]
  std: [c11]
  opt: [-O2]
  arch: [x86-64]
fixture: Examples/atoms/_c_bitfield.c
command: |
  gcc -std=c11 -O2 -S -masm=intel Examples/atoms/_c_bitfield.c -o Examples/atoms/_c_bitfield.asm
  gcc -std=c11 -O2 -Wall -Wextra Examples/atoms/_c_bitfield.c -o build/c648/_c_bitfield.exe
  build/c648/_c_bitfield.exe
artifact: Examples/atoms/_c_bitfield.asm
artifact_producer: gcc -std=c11 -O2 -S -masm=intel Examples/atoms/_c_bitfield.c -o Examples/atoms/_c_bitfield.asm
artifact_sha256: 9610238ae891e83c4f7b917dbe72e0d679a9b02a2b7e975d7541d630dbe8112b
artifact_compiler: "gcc 13.1.0 / clang 22.1.8"
artifact_assert:
  # 673q：原断言 `{kind: contains, text: "bitfield_probe"}` 写的是夹具里的 **static C
  # 函数名**——-O2 下被内联进 main，符号名在任何编译器产物里都不出现（连卡归属的 13.1.0
  # 工件里也没有）⇒ 原理上不可满足的坏断言。此前不红是因为 toolchain 长期等于卡归属的
  # 13.1.0 ⇒ artifact_sha 命中、断言从不被评估；650 批切到 mingw1530 GCC 15.3.0 后
  # sha 走不通、回落到结构断言，才第一次被执行 ⇒ 红。
  # 改为断言真实存在且承载 claim 的证据：① 读数键格式串（跨编译器稳定）② 关键立即数。
  # 其中 `mov\tedx, 173` 一条就锚住了整张卡的位布局 claim：173 = 0xAD = 101|10101|1
  #   （a:3=5、b:5=21、c:4 的有符号位读回 -1），`mov\tedx, -1` 另锚符号扩展。
  # "mov\tedx, N" 用真实制表符（YAML 双引号 \t，参照 EV-UB-NULLDEREF-669）：断言匹配侧
  # 两侧都归一空白，而 gate_engine EV-ASSERT-SYMBOL-MAPPED 的 haystack 不归一、须逐字相同。
  # 673q 五路实测全部命中：仓库工件(13.1.0) / GCC 15.3.0 / GCC 13.1.0 / clang 22.1.8 /
  # Ubuntu gcc 13.3.0（CI 侧等价物）。
  - {kind: contains_any, texts: ["bf_sizeof=%zu", "bf_a=%u", "bf_b=%u", "bf_c_signed_readback=%d", "bf_byte0=%u", "bf_byte1=%u"]}
  - {kind: contains, text: "mov	edx, 173"}
  - {kind: contains, text: "mov	edx, -1"}
  - {kind: contains, text: "mov	edx, 4"}
expected:
  run: bf_a=5 bf_b=21 bf_byte0=173 bf_byte1=15 bf_c_signed_readback=-1 bf_sizeof=4
actual:
  run_match_file: Examples/atoms/_c_bitfield.out
  run_match_keys: [bf_a, bf_b, bf_byte0, bf_byte1, bf_c_signed_readback, bf_sizeof]
  run_gcc_c11_O2: "bf_a=5 bf_b=21 bf_byte0=173 bf_byte1=15 bf_c_signed_readback=-1 bf_sizeof=4"
  run_gcc_c17_O2: "bf_a=5 bf_b=21 bf_byte0=173 bf_byte1=15 bf_c_signed_readback=-1 bf_sizeof=4"
  run_gcc_c2x_O2: "bf_a=5 bf_b=21 bf_byte0=173 bf_byte1=15 bf_c_signed_readback=-1 bf_sizeof=4"
  run_clang_c11_O2: "bf_a=5 bf_b=21 bf_byte0=173 bf_byte1=15 bf_c_signed_readback=-1 bf_sizeof=4"
  run_clang_c17_O2: "bf_a=5 bf_b=21 bf_byte0=173 bf_byte1=15 bf_c_signed_readback=-1 bf_sizeof=4"
  run_clang_c23_O2: "bf_a=5 bf_b=21 bf_byte0=173 bf_byte1=15 bf_c_signed_readback=-1 bf_sizeof=4"
artifact_version: 1
verdict: confirm
falsification: >-
  若把夹具里的「错误写法」改成「正确写法」而输出不变，则本实验无判别力：
  实测主档位输出为 bf_a=5 bf_b=21 bf_byte0=173 bf_byte1=15 bf_c_signed_readback=-1 bf_sizeof=4（两个写法的结果不同 ⇒ 有判别力）；若两者相同则本卡作废。
depth_layer: abi
---

# EV-LANG-008 · 服务 ATOM-LANG-BITFIELD-001

## 实测环境

| 编译器 | 版本 |
|---|---|
| gcc | gcc (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0 |
| clang | clang version 22.1.8 (https://github.com/msys2/MINGW-packages 6e4e79c2f86eeb534e324e583f2057dc9fd5ecab) |

档位：`-std=c11 -O2`（`c17`/`c23` 与 `-O0` 的结果见 `data/648_c_probe.json`）。

## 实测输出（主档位）

```
bf_a=5 bf_b=21 bf_byte0=173 bf_byte1=15 bf_c_signed_readback=-1 bf_sizeof=4
```

## 标准依据（N1570 原文，可复核）

> An implementation may allocate any addressable storage unit large enough to hold a bit- field. If enough space remains, a bit-field that immediately follows another bit-field in a structure shall be packed into adjacent bits of the same unit. If insufficient space remains, whether a bit-field that does not fit is put into the next unit or overlaps adjacent units is implementation-defined. The orde

— ISO/IEC 9899:2011 6.7.2.1p11，取自 https://port70.net/~nsz/c/c11/n1570.html#6.7.2.1p11（字节偏移 359259）。
