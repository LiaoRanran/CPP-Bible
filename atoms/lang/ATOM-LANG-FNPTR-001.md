---
schema_version: 1
id: ATOM-LANG-FNPTR-001
verified_at: 2026-09-27
title: "函数指针必须与目标函数类型兼容，否则调用是未定义行为"
domain: LANG
type: rule
status: draft
dal: C
human_review: optional
audience: intermediate
cognitive_load: medium
prerequisites_readable: true
claim: >-
  C 允许把函数指针强转成别的函数指针类型，但**经不兼容类型调用即未定义行为**（C11 6.5.2.2p9）；本批不去触发它（触发即 UB），而是以两条真实证据固定这一点：① 标准原文的措辞；② 直接强转时 gcc 13.1.0 与 clang 22.1.8 **各给出 1 条诊断**（实测），而转换本身仍能编译通过、地址也非空 ⇒ 「能编过」不等于「调用安全」。
claim_structured:
  - id: prop-1
    subject: "经不兼容函数指针的调用"
    predicate: "其性质是"
    object: "undefined behavior"
    claim_type: observation
    statement: "bad_addr_nonzero=1 fnptr_sizeof=8 good_call=5（gcc -std=c11 -O2 实测）。"
    evidence: [EV-LANG-004]
    extracted_by: writer
    # 673q: 锚由「夹具里的 static C 函数名」改为「本命题的载荷读数键」。原锚指向的
    # 函数在 -O2 下被内联、符号名在任何 .asm 里都不出现；673q A 已把证据卡的
    # artifact_assert 换成真实存在的 claim 锚定断言，原锚随之悬空，故同步改指。
    liveness: {kind: fixture_symbol, symbol: "fnptr_sizeof=%zu"}
claim_boundary:
  standard: [C11, C17, C23]
  compilers: [gcc 13.1.0 / clang 22.1.8]
  opt: [-O0, -O2]
  platform: [x86-64]
relations: []
evidence:
  - EV-LANG-004
sources:
  - {kind: iso, ref: "ISO/IEC 9899:2011 6.5.2.2p9：If the function is defined with a type that is not compatible with the type (of the expression) pointed to by the expression that denotes the called function, t", independent: true}
first_hand: true
superiority: >-
  常见材料只给结论；本卡给的是**同一次运行里的两个数字**——正确写法与「看起来对」的写法
  各自的输出（见反例节），以及 N1570 对应条款的原文出处（可复核的字节偏移）。
depth:
  layer: compiler
status_history:
  - {level: draft, at: 2026-09-27, by: writer:agent}
pedagogy:
  motivation: "转换能编译、地址也非空——那调用为什么还是 UB？"
  socratic: "如果两者参数个数不同，栈上的实参由谁负责匹配？"
  predict_first: "先猜编译器会不会在该转换处报警告。"
---

# ATOM-LANG-FNPTR-001 · 函数指针必须与目标函数类型兼容，否则调用是未定义行为

> 状态 `draft`：**verified 唯人签，Agent 不自置**（不代签）。待 human 签署后晋升。

## 实测（gcc -std=c11 -O2）

```
bad_addr_nonzero=1 fnptr_sizeof=8 good_call=5
```

## 反例：让它失败的实验

`bad_addr_nonzero=1` 说明「转换本身能过、地址也非空」——于是容易误以为调用也安全。真正的判据是编译器的 `-Wcast-function-type` 诊断与标准条款，而不是「它跑起来了」。

## 标准依据

> If the function is defined with a type that is not compatible with the type (of the expression) pointed to by the expression that denotes the called function, the behavior is undefined.

— ISO/IEC 9899:2011 6.5.2.2p9（N1570，字节偏移 274411，取自 https://port70.net/~nsz/c/c11/n1570.html#6.5.2.2p9）。

C17（N2310）与 C23（N3096）本批**只留下载留痕**（PDF，本环境无解析库），条款号**未逐条核对**，需人核。

## 边界（不该用在哪里）

不要靠强转函数指针「复用」回调签名；改签名或用适配函数。
