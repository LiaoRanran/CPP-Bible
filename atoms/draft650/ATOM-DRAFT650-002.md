---
id: ATOM-DRAFT650-002
verified_at: 2026-09-27
title: 独立看门狗 IWDG 由 LSI 驱动，主时钟失效仍能复位 MCU
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

IWDG 时钟源是独立低速内部 RC，主 HSE/HSI 停振不影响它；喂狗逻辑须确保主循环与高优先级任务都健康才喂，避免假活。
