---
id: ATOM-DRAFT650-005
verified_at: 2026-09-27
title: const 引用会延长所绑定临时对象的生命周期到引用作用域
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

const T& r = T(); 使临时对象存活到 r 的作用域结束，常用于避免拷贝；非 const 引用无法绑定临时。
