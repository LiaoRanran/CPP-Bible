---
id: ATOM-DRAFT650-004
verified_at: 2026-09-27
title: C++11 起静态局部变量初始化是线程安全的（magic statics）
domain: cpp
type: fact
status: draft
dal: B
human_review: required
audience: intermediate
schema_version: 1
status_history:
  - {level: draft, at: "2026-09-27", by: machine:writer}
---

但保证的只是初始化一次且可见，不保证后续并发访问安全；后续读写仍需自行同步。参见 C++11 章节。
