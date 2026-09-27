---
schema_version: 1
id: ATOM-UB-SIGNEDOVF-001
verified_at: 2026-09-27
title: "有符号整数溢出是 UB：同一行「溢出检查」在两个编译器上答案相反"
domain: UB
type: pitfall
gray_zone: ub
status: draft
dal: C
human_review: optional
audience: intermediate
cognitive_load: medium
prerequisites_readable: true
claim: >-
  有符号溢出是 UB（C11 6.5p5），因此「加完再比较」不是可靠的溢出检查：实测 `INT_MAX + 1 > INT_MAX` 在 gcc 13.1.0 上**恒为 1**（-O0 与 -O2 都折叠成常量真），在 clang 22.1.8 上**恒为 0**（两个档位都按回绕算）——同一表达式在两个编译器上**答案相反且都不崩**，这正是 UB 的含义（结果由实现决定，不是「会回绕」）；无符号回绕则是定义良好的（实测 0）。
claim_structured:
  - id: prop-1
    subject: "有符号整数溢出"
    predicate: "其性质是"
    object: "undefined behavior"
    claim_type: observation
    statement: "signed_plus1_gt=1 unsigned_plus1_gt=0 unsigned_wrapped=0（gcc -std=c11 -O2 实测）。"
    evidence: [EV-UB-003]
    extracted_by: writer
    liveness: {kind: fixture_symbol, symbol: signedovf_probe}
claim_boundary:
  standard: [C11, C17, C23]
  compilers: [gcc 13.1.0 / clang 22.1.8]
  opt: [-O0, -O2]
  platform: [x86-64]
relations: []
evidence:
  - EV-UB-003
sources:
  - {kind: iso, ref: "ISO/IEC 9899:2011 6.5p5：If an exceptional condition occurs during the evaluation of an expression (that is, if the result is not mathematically defined or not in the range of represent", independent: true}
first_hand: true
superiority: >-
  常见材料只给结论；本卡给的是**同一次运行里的两个数字**——正确写法与「看起来对」的写法
  各自的输出（见反例节），以及 N1570 对应条款的原文出处（可复核的字节偏移）。
depth:
  layer: compiler
status_history:
  - {level: draft, at: 2026-09-27, by: writer:agent}
pedagogy:
  motivation: "为什么同一行「溢出检查」换个编译器答案就反了？"
  socratic: "UB 的意思是「会崩」还是「编译器可以任意处理」？"
  predict_first: "先猜 `INT_MAX + 1 > INT_MAX` 在 gcc 与 clang 上是否同值。"
---

# ATOM-UB-SIGNEDOVF-001 · 有符号整数溢出是 UB：同一行「溢出检查」在两个编译器上答案相反

> 状态 `draft`：**verified 唯人签，Agent 不自置**（不代签）。待 human 签署后晋升。

## 实测（gcc -std=c11 -O2）

```
signed_plus1_gt=1 unsigned_plus1_gt=0 unsigned_wrapped=0
```

## 反例：让它失败的实验

`signed_plus1_gt` 在 -O0/-O2 下给出**不同**答案，就是「UB 不是『会回绕』」而是「编译器可以任意处理」的直接证据；把它当溢出检测用是错的。

## 标准依据

> If an exceptional condition occurs during the evaluation of an expression (that is, if the result is not mathematically defined or not in the range of representable values for its type), the behavior is undefined.

— ISO/IEC 9899:2011 6.5p5（N1570，字节偏移 257122，取自 https://port70.net/~nsz/c/c11/n1570.html#6.5p5）。

C17（N2310）与 C23（N3096）本批**只留下载留痕**（PDF，本环境无解析库），条款号**未逐条核对**，需人核。

## 边界（不该用在哪里）

不要用「加完再比较」检测有符号溢出；用无符号或先与极限比较。
