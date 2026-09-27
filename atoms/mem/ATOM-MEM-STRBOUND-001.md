---
schema_version: 1
id: ATOM-MEM-STRBOUND-001
title: "snprintf 的返回值是「本该写入的长度」，strncpy 不保证 NUL 终止"
domain: MEM
type: pitfall
status: draft
dal: C
human_review: optional
audience: intermediate
cognitive_load: medium
prerequisites_readable: true
claim: >-
  snprintf 返回的是「若缓冲够大本会写入的字符数」（可能大于缓冲，实测 10 > 8 ⇒ 已截断），把它当成「实际写入长度」会越界；strncpy 在源串长度 ≥ n 时**不会**写 NUL 终止符（实测 strncpy_nul_terminated=0）。
claim_structured:
  - id: prop-1
    subject: "snprintf 的返回值"
    predicate: "表示的是"
    object: "would-be length"
    claim_type: observation
    statement: "snprintf_ret=10 snprintf_truncated=1 snprintf_written=7 strncpy_last_byte=56 strncpy_nul_terminated=0（gcc -std=c11 -O2 实测）。"
    evidence: [EV-MEM-047]
    extracted_by: writer
    liveness: {kind: fixture_symbol, symbol: strbound_probe}
claim_boundary:
  standard: [C11, C17, C23]
  compilers: [gcc 13.1.0 / clang 22.1.8]
  opt: [-O0, -O2]
  platform: [x86-64]
relations: []
evidence:
  - EV-MEM-047
sources:
  - {kind: iso, ref: "ISO/IEC 9899:2011 7.21.6.5p3：The snprintf function returns the number of characters that would have been written had n been sufficiently large, not counting the terminating null character, ", independent: true}
first_hand: true
superiority: >-
  常见材料只给结论；本卡给的是**同一次运行里的两个数字**——正确写法与「看起来对」的写法
  各自的输出（见反例节），以及 N1570 对应条款的原文出处（可复核的字节偏移）。
depth:
  layer: runtime
status_history:
  - {level: draft, at: 2026-09-27, by: writer:agent}
pedagogy:
  motivation: "为什么「用 snprintf 就安全了」这句话只对了一半？"
  socratic: "返回值比缓冲还大时，多出来的字符去哪了？"
  predict_first: "先猜 snprintf 的返回值是 7（实际写入）还是 10（本该写入）。"
---

# ATOM-MEM-STRBOUND-001 · snprintf 的返回值是「本该写入的长度」，strncpy 不保证 NUL 终止

> 状态 `draft`：**verified 唯人签，Agent 不自置**（不代签）。待 human 签署后晋升。

## 实测（gcc -std=c11 -O2）

```
snprintf_ret=10 snprintf_truncated=1 snprintf_written=7 strncpy_last_byte=56 strncpy_nul_terminated=0
```

## 反例：让它失败的实验

`snprintf_ret=10` 而缓冲只有 8 —— 把返回值当长度去 `buf[n]` 就越界；`strncpy_nul_terminated=0` 说明「用了 strncpy 就安全」是错的。（注意：本卡**不**用 strlen(dst) 去读未终止的缓冲，那本身就越界。）

## 标准依据

> The snprintf function returns the number of characters that would have been written had n been sufficiently large, not counting the terminating null character, or a negative value if an encoding error occurred. Thus, the null-terminated output has been completely written if and only if the returned value is nonnegative and less than n.

— ISO/IEC 9899:2011 7.21.6.5p3（N1570，字节偏移 898708，取自 https://port70.net/~nsz/c/c11/n1570.html#7.21.6.5p3）。

C17（N2310）与 C23（N3096）本批**只留下载留痕**（PDF，本环境无解析库），条款号**未逐条核对**，需人核。

## 边界（不该用在哪里）

不要用返回值当「已写入长度」去索引；strncpy 之后要手动补终止符。
