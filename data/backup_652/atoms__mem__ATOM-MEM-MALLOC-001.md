---
schema_version: 1
id: ATOM-MEM-MALLOC-001
title: "free 不清空指针变量，也不保证 malloc(0) 返回 NULL"
domain: MEM
type: idiom
status: draft
dal: C
human_review: optional
audience: beginner
cognitive_load: medium
prerequisites_readable: true
claim: >-
  C 的 free 只释放空间：被 free 的指针变量仍持有原地址（故 if (p) 判断无效），free(NULL) 是定义好的空操作，而 malloc(0) 是否返回 NULL 是实现相关的（本次实测两个编译器都返回非 NULL）。
claim_structured:
  - id: prop-1
    subject: "free 之后的指针变量"
    predicate: "其值为"
    object: "dangling pointer"
    claim_type: observation
    statement: "alloc_aligned=1 dangling_value_nonzero=1 malloc0_null=0 reached_after_free_null=1（gcc -std=c11 -O2 实测）。"
    evidence: [EV-MEM-046]
    extracted_by: writer
    liveness: {kind: fixture_symbol, symbol: malloc_lifecycle_probe}
claim_boundary:
  standard: [C11, C17, C23]
  compilers: [gcc 13.1.0 / clang 22.1.8]
  opt: [-O0, -O2]
  platform: [x86-64]
relations: []
evidence:
  - EV-MEM-046
sources:
  - {kind: iso, ref: "ISO/IEC 9899:2011 7.22.3.3p2：The free function causes the space pointed to by ptr to be deallocated, that is, made available for further allocation. If ptr is a null pointer, no action occu", independent: true}
first_hand: true
superiority: >-
  常见材料只给结论；本卡给的是**同一次运行里的两个数字**——正确写法与「看起来对」的写法
  各自的输出（见反例节），以及 N1570 对应条款的原文出处（可复核的字节偏移）。
depth:
  layer: runtime
status_history:
  - {level: draft, at: 2026-09-27, by: writer:agent}
pedagogy:
  motivation: "为什么 `if (p) use(p);` 挡不住悬垂指针？"
  socratic: "free(p) 之后再加一句 p = NULL，改变的是指针还是那块内存？"
  predict_first: "先猜 malloc(0) 返回 NULL 还是非 NULL，再看两个编译器的实测。"
---

# ATOM-MEM-MALLOC-001 · free 不清空指针变量，也不保证 malloc(0) 返回 NULL

> 状态 `draft`：**verified 唯人签，Agent 不自置**（不代签）。待 human 签署后晋升。

## 实测（gcc -std=c11 -O2）

```
alloc_aligned=1 dangling_value_nonzero=1 malloc0_null=0 reached_after_free_null=1
```

打个比方（类比）：free 像是把房间退了，可你手里的房卡还写着那个房间号——刷卡不会报错，但房间已经不是你的了。

## 反例：让它失败的实验

`dangling_value_nonzero=1` 证明「free 后指针变量仍非 NULL」，所以 `if (p) { use(p); }` 这类「保护」是无效的；把 `malloc(0)` 当「必定返回 NULL」来判错 likewise 会误判。

## 标准依据

> The free function causes the space pointed to by ptr to be deallocated, that is, made available for further allocation. If ptr is a null pointer, no action occurs. Otherwise, if the argument does not match a pointer earlier returned by a memory management function, or if the space has been deallocated by a call to free or realloc, the behavior is undefined.

— ISO/IEC 9899:2011 7.22.3.3p2（N1570，字节偏移 958873，取自 https://port70.net/~nsz/c/c11/n1570.html#7.22.3.3p2）。

C17（N2310）与 C23（N3096）本批**只留下载留痕**（PDF，本环境无解析库），条款号**未逐条核对**，需人核。

## 边界（不该用在哪里）

不要用 `if (p)` 判断内存是否还有效；释放后立刻置空是唯一的自保写法。
