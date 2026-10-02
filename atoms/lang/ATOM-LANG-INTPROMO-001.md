---
schema_version: 1
id: ATOM-LANG-INTPROMO-001
verified_at: 2026-09-27
title: "有符号与无符号比较时，有符号一侧会被转成无符号（-1 < 1u 是假）"
domain: LANG
type: rule
status: draft
dal: C
human_review: optional
audience: beginner
cognitive_load: low
prerequisites_readable: true
claim: >-
  常用算术转换会把有符号操作数转成无符号：实测 `-1 < 1u` 的结果为 0（因为 -1 转成了 UINT_MAX），而 `signed char` 参与运算会先提升到 int（实测 sizeof(c+d)=4，故 100+100=200 不溢出）。
claim_structured:
  - id: prop-1
    subject: "有符号/无符号混合比较"
    predicate: "比较结果是"
    object: "unsigned conversion"
    claim_type: observation
    statement: "char_promoted_sum=200 char_sum_type_size=4 cmp_signed_unsigned=0 minus1_as_unsigned=4294967295（gcc -std=c11 -O2 实测）。"
    evidence: [EV-LANG-007]
    extracted_by: writer
    # 673q: 锚由「夹具里的 static C 函数名」改为「本命题的载荷读数键」。原锚指向的
    # 函数在 -O2 下被内联、符号名在任何 .asm 里都不出现；673q A 已把证据卡的
    # artifact_assert 换成真实存在的 claim 锚定断言，原锚随之悬空，故同步改指。
    liveness: {kind: fixture_symbol, symbol: "char_sum_type_size=%zu"}
claim_boundary:
  standard: [C11, C17, C23]
  compilers: [gcc 13.1.0 / clang 22.1.8]
  opt: [-O0, -O2]
  platform: [x86-64]
relations: []
evidence:
  - EV-LANG-007
sources:
  - {kind: iso, ref: "ISO/IEC 9899:2011 6.3.1.8p1：Many operators that expect operands of arithmetic type cause conversions and yield result types in a similar way. The purpose is to determine a common real type", independent: true}
first_hand: true
superiority: >-
  常见材料只给结论；本卡给的是**同一次运行里的两个数字**——正确写法与「看起来对」的写法
  各自的输出（见反例节），以及 N1570 对应条款的原文出处（可复核的字节偏移）。
depth:
  layer: runtime
status_history:
  - {level: draft, at: 2026-09-27, by: writer:agent}
pedagogy:
  motivation: "为什么 -1 明明更小，`-1 < 1u` 却是假？"
  socratic: "把 int 与 size_t 混比时，谁是「被转的那个」？"
  predict_first: "先猜 `cmp_signed_unsigned` 是 1 还是 0。"
---

# ATOM-LANG-INTPROMO-001 · 有符号与无符号比较时，有符号一侧会被转成无符号（-1 < 1u 是假）

> 状态 `draft`：**verified 唯人签，Agent 不自置**（不代签）。待 human 签署后晋升。

## 实测（gcc -std=c11 -O2）

```
char_promoted_sum=200 char_sum_type_size=4 cmp_signed_unsigned=0 minus1_as_unsigned=4294967295
```

打个比方（类比）：把它想成「借来的尺子量不出自己的长度」。

## 反例：让它失败的实验

`cmp_signed_unsigned=0` 是反直觉的（-1 明明更小），把数组长度 `size_t` 与 `int` 混比时这个转换会造出经典越界；对照 `char_promoted_sum=200` 说明提升本身是好事，问题出在符号性。

## 标准依据

> Many operators that expect operands of arithmetic type cause conversions and yield result types in a similar way. The purpose is to determine a common real type for the operands and result. For the specified operands, each operand is converted, without change of type domain, to a type whose corresponding real type is the common real type. Unless explicitly stated otherwise, the common real type is

— ISO/IEC 9899:2011 6.3.1.8p1（N1570，字节偏移 196616，取自 https://port70.net/~nsz/c/c11/n1570.html#6.3.1.8p1）。

C17（N2310）与 C23（N3096）本批**只留下载留痕**（PDF，本环境无解析库），条款号**未逐条核对**，需人核。

## 边界（不该用在哪里）

不要把有符号与无符号混在同一表达式里比较；循环下标统一用 size_t 并避免减成负数。
