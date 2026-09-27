---
id: ATOM-DRAFT650-006
verified_at: 2026-09-27
title: DMA 缓冲区须 cache 一致或置 non-cacheable，否则读到陈旧数据
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

CPU 经 DCache 改写后 DMA 看到的仍是旧内存；发送前 clean、接收后 invalidate，或把缓冲区设为 non-cacheable。
