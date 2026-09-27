---
id: ATOM-LANG-DECAY-001
title: "数组形参会退化为指针：函数内的 sizeof 拿不到数组长度"
domain: LANG
type: rule
status: draft
dal: C
human_review: optional
audience: beginner
cognitive_load: low
prerequisites_readable: true
claim: >-
  C 的数组形参在函数内已退化为指针，因此函数内用 sizeof(p)/sizeof(p[0]) 算出的「元素个数」恒为 sizeof(指针)/sizeof(元素)（x86-64 上 int 数组恒得 2），与实参数组长度无关。
claim_structured:
  - id: prop-1
    subject: "数组形参"
    predicate: "进入函数后"
    object: "pointer decay"
    claim_type: observation
    statement: "decay_len_true=10 decay_len_wrong_inside=2 decay_sizeof_array=40 decay_sizeof_param=8（gcc -std=c11 -O2 实测）。"
    evidence: [EV-LANG-003]
    extracted_by: writer
    liveness: {kind: fixture_symbol, symbol: decay_param_sizeof}
claim_boundary:
  standard: [C11, C17, C23]
  compilers: [gcc 13.1.0 / clang 22.1.8]
  opt: [-O0, -O2]
  platform: [x86-64]
relations: []
evidence:
  - EV-LANG-003
sources:
  - {kind: iso, ref: "ISO/IEC 9899:2011 6.7.6.3p7：A declaration of a parameter as ''array of type'' shall be adjusted to ''qualified pointer to type'', where the type qualifiers (if any) are those specified wit", independent: true}
first_hand: true
superiority: >-
  常见材料只给结论；本卡给的是**同一次运行里的两个数字**——正确写法与「看起来对」的写法
  各自的输出（见反例节），以及 N1570 对应条款的原文出处（可复核的字节偏移）。
depth:
  layer: compiler
status_history:
  - {level: draft, at: 2026-09-27, by: writer:agent}
pedagogy:
  motivation: "为什么 sizeof(a)/sizeof(a[0]) 在 main 里对、挪进函数就恒等于 2？"
  socratic: "如果把形参写成 int *p 与 int p[10]，编译器看到的有区别吗？"
  predict_first: "先猜函数内 sizeof(p) 的值，再看实测。"
---

# ATOM-LANG-DECAY-001 · 数组形参会退化为指针：函数内的 sizeof 拿不到数组长度

> 状态 `draft`：**verified 唯人签，Agent 不自置**（不代签）。待 human 签署后晋升。

## 实测（gcc -std=c11 -O2）

```
decay_len_true=10 decay_len_wrong_inside=2 decay_sizeof_array=40 decay_sizeof_param=8
```

打个比方（类比）：数组把「长度」写在自己身上，而形参只拿到一张写着地址的纸条——纸条上没有长度。

## 反例：让它失败的实验

`decay_len_wrong_inside` 是「看起来对」的写法（教科书里算数组长度的那一行），实测恒为 2；`decay_len_true` 才是 10。二者的差就是退化。

## 标准依据

> A declaration of a parameter as ''array of type'' shall be adjusted to ''qualified pointer to type'', where the type qualifiers (if any) are those specified within the [ and ] of the array type derivation. If the keyword static also appears within the [ and ] of the array type derivation, then for each call to the function, the value of the corresponding actual argument shall provide access to the

— ISO/IEC 9899:2011 6.7.6.3p7（N1570，字节偏移 415081，取自 https://port70.net/~nsz/c/c11/n1570.html#6.7.6.3p7）。

C17（N2310）与 C23（N3096）本批**只留下载留痕**（PDF，本环境无解析库），条款号**未逐条核对**，需人核。

## 边界（不该用在哪里）

不要把数组长度当参数省掉：要么显式传长度，要么用哨兵/结构体携带长度。
