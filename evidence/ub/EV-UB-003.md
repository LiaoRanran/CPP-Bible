---
id: EV-UB-003
verified_at: 2026-09-27
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
  build/c648/_c_signedovf.exe
artifact: Examples/atoms/_c_signedovf.asm
artifact_producer: gcc -std=c11 -O2 -S -masm=intel Examples/atoms/_c_signedovf.c -o Examples/atoms/_c_signedovf.asm
artifact_sha256: 685393cbc5fe1961d2c28e312b7479ad26e6472fd916d5c6638332a58e671065
artifact_compiler: "gcc 13.1.0 / clang 22.1.8"
artifact_assert:
  # 673q：原断言写的是夹具里的 **static C 函数名**（`- {kind: contains, text: "signedovf_probe"}`）。该函数在本卡 -O2
  # 档位下必然被内联进 main ⇒ 符号名在任何编译器/任何优化档的 .asm 里都不出现
  # （实测卡自己归属的 gcc 13.1.0 工件里也没有）⇒ 属**原理上不可满足**的坏断言。
  # 之所以此前不红：toolchain 长期等于卡归属的 13.1.0 ⇒ artifact_sha 命中、
  # 结构断言从不被评估；650 批把工具链切到 mingw1530 GCC 15.3.0 后 sha 走不通、
  # 回落到结构断言，这条断言才第一次被真正执行 ⇒ quality 红。
  # 改为断言工件里真实存在、且承载本卡 claim 的两类证据：
  #   ① 读数键的 printf 格式串（.rdata，跨编译器稳定，绑定期望输出的 key）
  #   (2) 承载 claim 的关键立即数：xor edx, edx —— unsigned 两路读数都编成 0，即
  #       (unsigned)-1 + 1 回绕为 0（defined）；而 signed 侧被编译器按「不溢出」
  #       折叠成常量 1——这正是本卡核心：UB 让编译器有权编出与运行时不同的形态。
  # 文本里的制表符是**真实 TAB**（YAML 双引号转义，仓内既有约定见
  # EV-UB-NULLDEREF-669）：check_artifact_assert 两侧都归一空白故可匹配，而
  # gate_engine EV-ASSERT-SYMBOL-MAPPED 的 haystack **不归一**、要求与产物逐字
  # 相同 ⇒ 必须写真实 TAB，不能写字面反斜杠 t。
  # 673q 五路实测全部命中：仓库已提交工件(13.1.0) / GCC 15.3.0 MinGW /
  # GCC 13.1.0 MinGW / clang 22.1.8(MSYS2) / Ubuntu gcc 13.3.0（CI 侧等价物）。
  - {kind: contains_any, texts: ["signed_plus1_gt=%d", "unsigned_plus1_gt=%d", "unsigned_wrapped=%u"]}
  - {kind: contains, text: "xor	edx, edx"}
expected:
  run: signed_plus1_gt=1 unsigned_plus1_gt=0 unsigned_wrapped=0
actual:
  run_match_file: Examples/atoms/_c_signedovf.out
  run_match_keys: [signed_plus1_gt, unsigned_plus1_gt, unsigned_wrapped]
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
