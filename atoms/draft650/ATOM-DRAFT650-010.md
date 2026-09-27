---
id: ATOM-DRAFT650-010
verified_at: 2026-09-27
title: RCU 读侧临界区禁止抢占与休眠，否则宽限期无法结束
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

读侧持 rcu_read_lock 期间若被抢占并休眠，优雅期（grace period）无法推进，写侧回收挂起；参见 RCU 设计约束。
