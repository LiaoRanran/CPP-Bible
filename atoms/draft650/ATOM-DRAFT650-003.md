---
id: ATOM-DRAFT650-003
verified_at: 2026-09-27
title: ARM 上 volatile 不足以保证跨核/外设观测顺序，还需 DMB/DSB
domain: conc
type: mechanism
status: draft
dal: B
human_review: required
audience: intermediate
schema_version: 1
status_history:
  - {level: draft, at: "2026-09-27", by: machine:writer}
---

volatile 只禁止编译器重排与缓存，不约束 CPU 访存顺序；与外设或另一核共享数据时需显式内存屏障，见 ARMv7-M DMB 指令。
