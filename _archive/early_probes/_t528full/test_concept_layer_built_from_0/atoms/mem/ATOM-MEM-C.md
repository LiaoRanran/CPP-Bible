---
id: ATOM-MEM-C
title: t
status: draft
claim_structured:
  - id: prop-1
    subject: 内存屏障(fence)
    predicate: 落在循环体内时
    object: 阻止编译器消除该循环
    claim_type: observation
    statement: st1
    extracted_by: writer
  - id: prop-2
    subject: 内存屏障(fence)
    predicate: 不提供
    object: 原子性
    claim_type: inference
    statement: st2
    extracted_by: writer
---
