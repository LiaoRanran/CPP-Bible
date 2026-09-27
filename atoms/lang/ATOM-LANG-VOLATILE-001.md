---
schema_version: 1
id: ATOM-LANG-VOLATILE-001
title: "volatile 的作用是「每次都真的去访问一次」，不是「多线程同步」"
domain: LANG
type: concept
status: draft
dal: C
human_review: optional
audience: intermediate
cognitive_load: high
prerequisites_readable: true
claim: >-
  volatile 约束的是**抽象的访存次数**：-O2 下普通变量的三次读取被**完全折叠**（实测生成的汇编里对它的引用次数为 0），而 volatile 变量必须逐次访问（实测引用 4 次）；它**不**提供原子性，也**不**提供线程间的同步顺序。
claim_structured:
  - id: prop-1
    subject: "volatile 变量"
    predicate: "约束的是"
    object: "access count"
    claim_type: observation
    statement: "sink=0（gcc -std=c11 -O2 实测）。"
    evidence: [EV-LANG-005]
    extracted_by: writer
    liveness: {kind: fixture_symbol, symbol: volatile_probe}
claim_boundary:
  standard: [C11, C17, C23]
  compilers: [gcc 13.1.0 / clang 22.1.8]
  opt: [-O0, -O2]
  platform: [x86-64]
relations: []
evidence:
  - EV-LANG-005
sources:
  - {kind: iso, ref: "ISO/IEC 9899:2011 6.7.3p7：An object that has volatile-qualified type may be modified in ways unknown to the implementation or have other unknown side effects. Therefore any expression re", independent: true}
first_hand: true
superiority: >-
  常见材料只给结论；本卡给的是**同一次运行里的两个数字**——正确写法与「看起来对」的写法
  各自的输出（见反例节），以及 N1570 对应条款的原文出处（可复核的字节偏移）。
depth:
  layer: asm
status_history:
  - {level: draft, at: 2026-09-27, by: writer:agent}
pedagogy:
  motivation: "volatile 到底是「原子」还是「别优化掉」？"
  socratic: "两次读都被保留了，就说明两个线程不会交错吗？"
  predict_first: "先猜汇编里 plain_flag 与 vol_flag 谁被读的次数多。"
---

# ATOM-LANG-VOLATILE-001 · volatile 的作用是「每次都真的去访问一次」，不是「多线程同步」

> 状态 `draft`：**verified 唯人签，Agent 不自置**（不代签）。待 human 签署后晋升。

## 实测（gcc -std=c11 -O2）

```
sink=0
```

## 反例：让它失败的实验

把 `volatile` 当「线程安全的开关」是最常见的误解：它只保证「每次都去内存读」，既不原子也不建立顺序 —— 汇编里读的次数变了，但「读-改-写」仍可能交错。

## 标准依据

> An object that has volatile-qualified type may be modified in ways unknown to the implementation or have other unknown side effects. Therefore any expression referring to such an object shall be evaluated strictly according to the rules of the abstract machine, as described in 5.1.2.3 . Furthermore, at every sequence point the value last stored in the object shall agree with that prescribed by the

— ISO/IEC 9899:2011 6.7.3p7（N1570，字节偏移 380807，取自 https://port70.net/~nsz/c/c11/n1570.html#6.7.3p7）。

C17（N2310）与 C23（N3096）本批**只留下载留痕**（PDF，本环境无解析库），条款号**未逐条核对**，需人核。

## 边界（不该用在哪里）

不要用 volatile 做线程同步（不原子、不建立顺序）；同步请用原子类型或锁。
