---
id: ATOM-DRAFT650-008
verified_at: 2026-09-27
title: 有符号整数溢出是未定义行为，编译器可假设不发生
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

int x = INT_MAX; x+1; 是 UB，编译器据此做范围推断与死代码删除；应使用无符号或饱和/checked 运算。
