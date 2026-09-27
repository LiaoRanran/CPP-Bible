---
id: ATOM-DRAFT650-001
verified_at: 2026-09-27
title: STM32 中断里改全局变量须 volatile 或关中断保护，否则编译器优化会丢弃更新
domain: emb
type: mechanism
status: draft
dal: B
human_review: required
audience: intermediate
schema_version: 1
status_history:
  - {level: draft, at: "2026-09-27", by: machine:writer}
---

在 ISR 中写、主循环读的共享标志，若不加 volatile 或临界区，编译器可能把它缓存到寄存器，导致主循环永远看不到更新。参见 C++ volatile 语义与 C++11 顺序章节。
