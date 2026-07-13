# DEPENDENCY — 依赖关系图

> 关联: knowledge_graph.json ⟶ GOVERNANCE.md

```
part01(history) ────────────────────────────────────────────┐
    │                                                        │
    ├──→ part02(toolchain) ──→ part13(engineering) ─────────┤
    │                                                        │
    ├──→ part03(language) ─┬──→ part04(memory) ──→ part09(concurrency)
    │                      │       │
    │                      │       ├──→ part14(performance)
    │                      │       │
    │                      ├──→ part05(oop) ──→ part12(patterns)
    │                      │       │
    │                      └──→ part06(templates) ──→ part10(modern)
    │                              │
    │                              └──→ part14(performance)
    │
    └──→ part07(stl) ──→ part08(algorithms)
            │
            ├──→ part10(modern)
            ├──→ part11(source)
            └──→ part15(cases)
                    │
                    └──→ part16(reading)


学习路径依赖:
  beginner:  part01 → part03(ch19-22) → part07(ch76-80) → part10(ch115-117)
  intermediate: +part04 +part05 +part06(ch60-67) +part07(full) +part08 +part12
  advanced:  +part06(ch68-72) +part09 +part10(full) +part11 +part14 +part15
  expert:    +part02 +part13(full) +part16
```
