---
schema_version: 1
id: ATOM-LANG-MACRO-001
verified_at: 2026-09-27
title: "宏是文本替换：不加括号会错优先级，传带副作用实参会被求值多次"
domain: LANG
type: pitfall
status: draft
dal: C
human_review: optional
audience: beginner
cognitive_load: low
prerequisites_readable: true
claim: >-
  函数式宏在替换前先展开实参，替换是**文本级**的：实测 `SQ(x) x*x` 在 `SQ(3+1)` 上得 7（而正确写法得 16），`MAX(a,b)` 传入 `i++` 时该实参被求值两次（实测 i 从 0 变 2）。
claim_structured:
  - id: prop-1
    subject: "函数式宏"
    predicate: "其实质是"
    object: "text substitution"
    claim_type: observation
    statement: "i_after=2 max_bad_result=1 sq_bad=7 sq_good=16（gcc -std=c11 -O2 实测）。"
    evidence: [EV-LANG-009]
    extracted_by: writer
    # 673q: 锚由「夹具里的 static C 函数名」改为「本命题的载荷读数键」。原锚指向的
    # 函数在 -O2 下被内联、符号名在任何 .asm 里都不出现；673q A 已把证据卡的
    # artifact_assert 换成真实存在的 claim 锚定断言，原锚随之悬空，故同步改指。
    liveness: {kind: fixture_symbol, symbol: "sq_bad=%d"}
claim_boundary:
  standard: [C11, C17, C23]
  compilers: [gcc 13.1.0 / clang 22.1.8]
  opt: [-O0, -O2]
  platform: [x86-64]
relations: []
evidence:
  - EV-LANG-009
sources:
  - {kind: iso, ref: "ISO/IEC 9899:2011 6.10.3.1p1：After the arguments for the invocation of a function-like macro have been identified, argument substitution takes place. A parameter in the replacement list, un", independent: true}
first_hand: true
superiority: >-
  常见材料只给结论；本卡给的是**同一次运行里的两个数字**——正确写法与「看起来对」的写法
  各自的输出（见反例节），以及 N1570 对应条款的原文出处（可复核的字节偏移）。
depth:
  layer: compiler
status_history:
  - {level: draft, at: 2026-09-27, by: writer:agent}
pedagogy:
  motivation: "为什么加了括号还可能有坑？"
  socratic: "`MAX(i++, j)` 里 i++ 到底被执行了几次？"
  predict_first: "先猜 SQ_BAD(3+1) 是 16 还是 7。"
---

# ATOM-LANG-MACRO-001 · 宏是文本替换：不加括号会错优先级，传带副作用实参会被求值多次

> 状态 `draft`：**verified 唯人签，Agent 不自置**（不代签）。待 human 签署后晋升。

## 实测（gcc -std=c11 -O2）

```
i_after=2 max_bad_result=1 sq_bad=7 sq_good=16
```

打个比方（类比）：宏像复印机：它复印的是你写的那串字符，而不是「那个值」——印两次就跑两次。

## 反例：让它失败的实验

`sq_bad=7` 与 `sq_good=16` 同一次运行对照；`i_after=2` 直接证明「i++ 被求值了两次」（写的人只想要一次）。

## 标准依据

> After the arguments for the invocation of a function-like macro have been identified, argument substitution takes place. A parameter in the replacement list, unless preceded by a # or ## preprocessing token or followed by a ## preprocessing token (see below), is replaced by the corresponding argument after all macros contained therein have been expanded. Before being substituted, each argument's p

— ISO/IEC 9899:2011 6.10.3.1p1（N1570，字节偏移 505977，取自 https://port70.net/~nsz/c/c11/n1570.html#6.10.3.1p1）。

C17（N2310）与 C23（N3096）本批**只留下载留痕**（PDF，本环境无解析库），条款号**未逐条核对**，需人核。

## 边界（不该用在哪里）

不要用宏实现有副作用的「函数」；优先 static inline 函数（有类型检查、求值一次）。
