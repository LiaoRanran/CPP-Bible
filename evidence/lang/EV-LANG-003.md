---
id: EV-LANG-003
verified_at: 2026-09-27
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
  build/c648/_c_decay.exe
artifact: Examples/atoms/_c_decay.asm
artifact_producer: gcc -std=c11 -O2 -S -masm=intel Examples/atoms/_c_decay.c -o Examples/atoms/_c_decay.asm
artifact_sha256: 97509b8f4bf442598807454e49eff591c65e4e8dd0917537e2fac8371d2a6e2f
artifact_compiler: "gcc 13.1.0 / clang 22.1.8"
artifact_assert:
  # 673q：原断言写的是夹具里的 **static C 函数名**（`- {kind: contains, text: "decay_param_sizeof"}`）。该函数在本卡 -O2
  # 档位下必然被内联进 main ⇒ 符号名在任何编译器/任何优化档的 .asm 里都不出现
  # （实测卡自己归属的 gcc 13.1.0 工件里也没有）⇒ 属**原理上不可满足**的坏断言。
  # 之所以此前不红：toolchain 长期等于卡归属的 13.1.0 ⇒ artifact_sha 命中、
  # 结构断言从不被评估；650 批把工具链切到 mingw1530 GCC 15.3.0 后 sha 走不通、
  # 回落到结构断言，这条断言才第一次被真正执行 ⇒ quality 红。
  # 改为断言工件里真实存在、且承载本卡 claim 的两类证据：
  #   ① 读数键的 printf 格式串（.rdata，跨编译器稳定，绑定期望输出的 key）
  #   ② 承载 claim 的关键立即数：sizeof 数组 40 != sizeof 形参 8（x86-64 SysV
  #      第二整数实参走 edx）—— 这正是本卡 hypothesis 的直接产物
  # 文本里的制表符是**真实 TAB**（YAML 双引号转义，仓内既有约定见
  # EV-UB-NULLDEREF-669）：check_artifact_assert 两侧都归一空白故可匹配，而
  # gate_engine EV-ASSERT-SYMBOL-MAPPED 的 haystack **不归一**、要求与产物逐字
  # 相同 ⇒ 必须写真实 TAB，不能写字面反斜杠 t。
  # 673q 五路实测全部命中：仓库已提交工件(13.1.0) / GCC 15.3.0 MinGW /
  # GCC 13.1.0 MinGW / clang 22.1.8(MSYS2) / Ubuntu gcc 13.3.0（CI 侧等价物）。
  - {kind: contains_any, texts: ["decay_sizeof_array=%zu", "decay_sizeof_param=%zu", "decay_len_true=%zu", "decay_len_wrong_inside=%zu"]}
  - {kind: contains, text: "mov	edx, 40"}
  - {kind: contains, text: "mov	edx, 8"}
  - {kind: contains, text: "mov	edx, 2"}
expected:
  run: decay_len_true=10 decay_len_wrong_inside=2 decay_sizeof_array=40 decay_sizeof_param=8
actual:
  run_match_file: Examples/atoms/_c_decay.out
  run_match_keys: [decay_len_true, decay_len_wrong_inside, decay_sizeof_array, decay_sizeof_param]
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
