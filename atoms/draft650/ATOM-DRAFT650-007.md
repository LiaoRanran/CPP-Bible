---
id: ATOM-DRAFT650-007
title: -O2 可能移除无副作用循环/变量，调试(-O0)与发布行为可不同
domain: hist
type: myth
status: draft
dal: B
human_review: required
audience: intermediate
schema_version: 1
status_history:
  - {level: draft, at: "2026-09-27", by: machine:writer}
---

发布优化会删死代码、复算内联；依赖未定义读写顺序的调试期现象在 -O2 下可能消失，不能据此判断正确性。
