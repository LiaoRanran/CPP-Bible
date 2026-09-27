---
id: ATOM-DRAFT650-009
verified_at: 2026-09-27
title: Cortex-M 中断/异常优先级数值越小优先级越高
domain: emb
type: fact
status: draft
dal: B
human_review: required
audience: intermediate
schema_version: 1
status_history:
  - {level: draft, at: "2026-09-27", by: machine:writer}
---

与日常直觉相反：优先级 0 为最高；NVIC 仅高几位有效，配置时须注意对齐与分组（PRIGROUP）。
