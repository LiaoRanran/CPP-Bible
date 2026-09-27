---
id: ATOM-LANG-SETJMP-001
title: "longjmp 之后，非 volatile 的局部变量值是不确定的"
domain: LANG
type: pitfall
status: draft
dal: C
human_review: optional
audience: intermediate
cognitive_load: high
prerequisites_readable: true
claim: >-
  longjmp 返回后，setjmp 所在函数里**非 volatile 的自动变量**若在两者之间被改过，其值**不确定**：实测同一份代码在 -O0 下读回 5、在 -O2 下读回 0（gcc 与 clang 一致），而 volatile 变量在两个档位下都读回 5（标准保证）。
claim_structured:
  - id: prop-1
    subject: "longjmp 后的自动变量"
    predicate: "其值"
    object: "indeterminate value"
    claim_type: observation
    statement: "after_longjmp_plain=0 after_longjmp_volatile=5（gcc -std=c11 -O2 实测）。"
    evidence: [EV-LANG-006]
    extracted_by: writer
    liveness: {kind: fixture_symbol, symbol: setjmp_probe}
claim_boundary:
  standard: [C11, C17, C23]
  compilers: [gcc 13.1.0 / clang 22.1.8]
  opt: [-O0, -O2]
  platform: [x86-64]
relations: []
evidence:
  - EV-LANG-006
sources:
  - {kind: iso, ref: "ISO/IEC 9899:2011 7.13.2.1p3：All accessible objects have values, and all other components of the abstract machine 249) have state, as of the time the longjmp function was called, except tha", independent: true}
first_hand: true
superiority: >-
  常见材料只给结论；本卡给的是**同一次运行里的两个数字**——正确写法与「看起来对」的写法
  各自的输出（见反例节），以及 N1570 对应条款的原文出处（可复核的字节偏移）。
depth:
  layer: compiler
status_history:
  - {level: draft, at: 2026-09-27, by: writer:agent}
pedagogy:
  motivation: "为什么「跳回来之后变量还是我设的值」在 -O2 下就不一定了？"
  socratic: "值「不确定」和「值被改坏了」是一回事吗？"
  predict_first: "先猜 -O0 与 -O2 会不会给出不同的读数。"
---

# ATOM-LANG-SETJMP-001 · longjmp 之后，非 volatile 的局部变量值是不确定的

> 状态 `draft`：**verified 唯人签，Agent 不自置**（不代签）。待 human 签署后晋升。

## 实测（gcc -std=c11 -O2）

```
after_longjmp_plain=0 after_longjmp_volatile=5
```

## 反例：让它失败的实验

`after_longjmp_plain` 在 -O0 与 -O2 下可以不一样（这就是「不确定」的实测形态）；只有 `after_longjmp_volatile` 恒为 5。用普通局部变量在长跳转后传递状态是错的。

## 标准依据

> All accessible objects have values, and all other components of the abstract machine 249) have state, as of the time the longjmp function was called, except that the values of objects of automatic storage duration that are local to the function containing the invocation of the corresponding setjmp macro that do not have volatile-qualified type and have been changed between the setjmp invocation an

— ISO/IEC 9899:2011 7.13.2.1p3（N1570，字节偏移 733616，取自 https://port70.net/~nsz/c/c11/n1570.html#7.13.2.1p3）。

C17（N2310）与 C23（N3096）本批**只留下载留痕**（PDF，本环境无解析库），条款号**未逐条核对**，需人核。

## 边界（不该用在哪里）

不要跨 longjmp 用普通局部变量传状态；需要就用 volatile 或静态存储期。
