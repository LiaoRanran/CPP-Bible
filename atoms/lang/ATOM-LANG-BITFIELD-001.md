---
schema_version: 1
id: ATOM-LANG-BITFIELD-001
verified_at: 2026-09-27
title: "位域的布局与 Plain int 位域的符号性都是实现定义的"
domain: LANG
type: pitfall
status: draft
dal: C
human_review: optional
audience: expert
cognitive_load: high
prerequisites_readable: true
claim: >-
  位域在同一「可寻址存储单元」内的分配顺序、跨单元的对齐都是**实现定义**；plain `int` 位域被解释为有符号还是无符号也**由实现决定**（实测两个编译器都按有符号处理 ⇒ 4 位位域存 -1 读回 -1，但这不是可移植结论）。
claim_structured:
  - id: prop-1
    subject: "位域布局"
    predicate: "其分配顺序是"
    object: "implementation-defined"
    claim_type: observation
    statement: "bf_a=5 bf_b=21 bf_byte0=173 bf_byte1=15 bf_c_signed_readback=-1 bf_sizeof=4（gcc -std=c11 -O2 实测）。"
    evidence: [EV-LANG-008]
    extracted_by: writer
    liveness: {kind: fixture_symbol, symbol: bitfield_probe}
claim_boundary:
  standard: [C11, C17, C23]
  compilers: [gcc 13.1.0 / clang 22.1.8]
  opt: [-O0, -O2]
  platform: [x86-64]
relations: []
evidence:
  - EV-LANG-008
sources:
  - {kind: iso, ref: "ISO/IEC 9899:2011 6.7.2.1p11：An implementation may allocate any addressable storage unit large enough to hold a bit- field. If enough space remains, a bit-field that immediately follows ano", independent: true}
first_hand: true
superiority: >-
  常见材料只给结论；本卡给的是**同一次运行里的两个数字**——正确写法与「看起来对」的写法
  各自的输出（见反例节），以及 N1570 对应条款的原文出处（可复核的字节偏移）。
depth:
  layer: abi
status_history:
  - {level: draft, at: 2026-09-27, by: writer:agent}
pedagogy:
  motivation: "位域明明写死了比特数，为什么还说它不可移植？"
  socratic: "把位域结构体直接 memcpy 成字节发出去，接收方凭什么还原？"
  predict_first: "先猜 4 位位域存 -1 读回来是 -1 还是 15。"
---

# ATOM-LANG-BITFIELD-001 · 位域的布局与 Plain int 位域的符号性都是实现定义的

> 状态 `draft`：**verified 唯人签，Agent 不自置**（不代签）。待 human 签署后晋升。

## 实测（gcc -std=c11 -O2）

```
bf_a=5 bf_b=21 bf_byte0=173 bf_byte1=15 bf_c_signed_readback=-1 bf_sizeof=4
```

## 反例：让它失败的实验

`bf_c_signed_readback=-1` 只在「实现把 plain int 位域当 signed」时成立；换编译器即可变成 15。把它写进寄存器映射或序列化格式就是埋雷。

## 标准依据

> An implementation may allocate any addressable storage unit large enough to hold a bit- field. If enough space remains, a bit-field that immediately follows another bit-field in a structure shall be packed into adjacent bits of the same unit. If insufficient space remains, whether a bit-field that does not fit is put into the next unit or overlaps adjacent units is implementation-defined. The orde

— ISO/IEC 9899:2011 6.7.2.1p11（N1570，字节偏移 359259，取自 https://port70.net/~nsz/c/c11/n1570.html#6.7.2.1p11）。

C17（N2310）与 C23（N3096）本批**只留下载留痕**（PDF，本环境无解析库），条款号**未逐条核对**，需人核。

## 边界（不该用在哪里）

不要把位域用于寄存器映射或跨机序列化；要布局就显式用掩码与移位。
