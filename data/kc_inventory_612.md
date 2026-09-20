# 612 D1 · KC 知识组件台账（只读）

> 生成时间：2026-09-20T21:42:09 ｜ 命令：`python tools/kc_inventory.py`
>
> 27 张原子卡 = 27 个 KC。难度为**自动估算建议**（套用任务书分档），前置依赖来自卡面 `relations.prerequisite`（自动推导，待人工复核）。

## 1 · 总览

- KC 总数：**27**
- 平均命题数：2.93 ｜ 平均关联 MIS 数：1.56
- 有前置依赖的 KC：**19** 张

**难度分布**（1=易 … 5=难）：

| 等级 | KC 数 |
|---|---|
| 1 | 3 |
| 2 | 21 |
| 3 | 1 |
| 4 | 1 |
| 5 | 1 |

## 2 · KC 台账

| KC | 领域 | 难度 | 命题(观/推) | 关联MIS | 前置依赖 | 后继 |
|---|---|---|---|---|---|---|
| `ATOM-CONC-FENCE-001` | conc | 1 | 2(1/1) | 0 | — | — |
| `ATOM-CONC-LOCK-001` | conc | 1 | 2(1/1) | 0 | — | — |
| `ATOM-CONC-RACE-001` | conc | 2 | 3(1/2) | 1 | — | — |
| `ATOM-HIST-AUTOPTR-001` | HIST | 3 | 4(3/1) | 4 | — | — |
| `ATOM-LANG-INLINE-001` | LANG | 2 | 3(2/1) | 1 | — | — |
| `ATOM-MEM-ALIGN-001` | MEM | 2 | 3(2/1) | 1 | — | — |
| `ATOM-MEM-ALLOC-001` | MEM | 2 | 4(3/1) | 1 | ATOM-MEM-NEW-001, ATOM-MEM-RAII-001 | ATOM-MEM-ALLOC-002 |
| `ATOM-MEM-ALLOC-002` | MEM | 2 | 3(2/1) | 1 | ATOM-MEM-ALLOC-001 | — |
| `ATOM-MEM-LEAK-001` | MEM | 2 | 3(2/1) | 1 | ATOM-MEM-SHARED-001, ATOM-MEM-WEAK-001 | — |
| `ATOM-MEM-LEAK-002` | MEM | 2 | 3(2/1) | 1 | ATOM-MEM-SHARED-001, ATOM-MEM-WEAK-001 | — |
| `ATOM-MEM-MOVE-002` | MEM | 4 | 3(2/1) | 6 | ATOM-MEM-VALUE-001 | ATOM-MEM-PERF-001, ATOM-MEM-RAII-002, ATOM-MEM-RVREF-001, ATOM-MEM-VALUE-002 |
| `ATOM-MEM-NEW-001` | MEM | 2 | 3(2/1) | 0 | ATOM-MEM-RAII-001 | ATOM-MEM-ALLOC-001, ATOM-MEM-PERF-002 |
| `ATOM-MEM-PERF-001` | MEM | 1 | 2(1/1) | 0 | ATOM-MEM-MOVE-002 | ATOM-MEM-PERF-002, ATOM-MEM-PERF-003, ATOM-MEM-PERF-004 |
| `ATOM-MEM-PERF-002` | MEM | 2 | 2(1/1) | 2 | ATOM-MEM-NEW-001, ATOM-MEM-PERF-001 | — |
| `ATOM-MEM-PERF-003` | MEM | 2 | 3(1/2) | 2 | ATOM-MEM-PERF-001 | — |
| `ATOM-MEM-PERF-004` | MEM | 2 | 3(2/1) | 1 | ATOM-MEM-PERF-001 | — |
| `ATOM-MEM-RAII-001` | MEM | 2 | 3(2/1) | 2 | — | ATOM-MEM-ALLOC-001, ATOM-MEM-NEW-001, ATOM-MEM-RAII-002, ATOM-MEM-UNIQUE-001 |
| `ATOM-MEM-RAII-002` | MEM | 2 | 4(3/1) | 2 | ATOM-MEM-MOVE-002, ATOM-MEM-RAII-001 | — |
| `ATOM-MEM-RVREF-001` | MEM | 2 | 3(2/1) | 0 | ATOM-MEM-MOVE-002 | — |
| `ATOM-MEM-SHARED-001` | MEM | 2 | 3(2/1) | 1 | ATOM-MEM-UNIQUE-001 | ATOM-MEM-LEAK-001, ATOM-MEM-LEAK-002, ATOM-MEM-SHARED-002, ATOM-MEM-WEAK-001 |
| `ATOM-MEM-SHARED-002` | MEM | 2 | 3(2/1) | 1 | ATOM-MEM-SHARED-001 | — |
| `ATOM-MEM-UNIQUE-001` | MEM | 2 | 3(2/1) | 0 | ATOM-MEM-RAII-001 | ATOM-MEM-SHARED-001, ATOM-MEM-UNIQUE-002 |
| `ATOM-MEM-UNIQUE-002` | MEM | 2 | 3(2/1) | 2 | ATOM-MEM-UNIQUE-001 | — |
| `ATOM-MEM-VALUE-001` | MEM | 2 | 3(2/1) | 0 | — | ATOM-MEM-MOVE-002, ATOM-MEM-VALUE-002 |
| `ATOM-MEM-VALUE-002` | MEM | 2 | 3(2/1) | 2 | ATOM-MEM-MOVE-002, ATOM-MEM-VALUE-001 | — |
| `ATOM-MEM-WEAK-001` | MEM | 2 | 3(2/1) | 0 | ATOM-MEM-SHARED-001 | ATOM-MEM-LEAK-001, ATOM-MEM-LEAK-002 |
| `ATOM-UB-GRAY-001` | UB | 5 | 2(1/1) | 10 | ATOM-UB-DEF-001 | — |

## 3 · 依赖关系（前置 → 后继，自动推导）

- `ATOM-MEM-NEW-001` → `ATOM-MEM-ALLOC-001`
- `ATOM-MEM-RAII-001` → `ATOM-MEM-ALLOC-001`
- `ATOM-MEM-ALLOC-001` → `ATOM-MEM-ALLOC-002`
- `ATOM-MEM-SHARED-001` → `ATOM-MEM-LEAK-001`
- `ATOM-MEM-WEAK-001` → `ATOM-MEM-LEAK-001`
- `ATOM-MEM-SHARED-001` → `ATOM-MEM-LEAK-002`
- `ATOM-MEM-WEAK-001` → `ATOM-MEM-LEAK-002`
- `ATOM-MEM-VALUE-001` → `ATOM-MEM-MOVE-002`
- `ATOM-MEM-RAII-001` → `ATOM-MEM-NEW-001`
- `ATOM-MEM-MOVE-002` → `ATOM-MEM-PERF-001`
- `ATOM-MEM-NEW-001` → `ATOM-MEM-PERF-002`
- `ATOM-MEM-PERF-001` → `ATOM-MEM-PERF-002`
- `ATOM-MEM-PERF-001` → `ATOM-MEM-PERF-003`
- `ATOM-MEM-PERF-001` → `ATOM-MEM-PERF-004`
- `ATOM-MEM-MOVE-002` → `ATOM-MEM-RAII-002`
- `ATOM-MEM-RAII-001` → `ATOM-MEM-RAII-002`
- `ATOM-MEM-MOVE-002` → `ATOM-MEM-RVREF-001`
- `ATOM-MEM-UNIQUE-001` → `ATOM-MEM-SHARED-001`
- `ATOM-MEM-SHARED-001` → `ATOM-MEM-SHARED-002`
- `ATOM-MEM-RAII-001` → `ATOM-MEM-UNIQUE-001`
- `ATOM-MEM-UNIQUE-001` → `ATOM-MEM-UNIQUE-002`
- `ATOM-MEM-MOVE-002` → `ATOM-MEM-VALUE-002`
- `ATOM-MEM-VALUE-001` → `ATOM-MEM-VALUE-002`
- `ATOM-MEM-SHARED-001` → `ATOM-MEM-WEAK-001`
- `ATOM-UB-DEF-001` → `ATOM-UB-GRAY-001`

## 4 · 口径与边界（诚实）

- **难度是建议**：分档公式直接套用任务书 bands（命题数 / 关联 MIS 数取较高档），不声称客观难度。
- **前置依赖来源**：任务书写「基于 evidence 引用关系推导」，但本仓 evidence 指向 EV 卡而非 ATOM 卡，故以卡面 `relations.prerequisite` 为权威；可能与「真正应先学的卡」有出入，标注待复核。
- **关联 MIS**：`data/flashcards/markdown/misconception_*.md` 反向索引；未关联 MIS 的 KC 记 0。
- **只读**：不修改任何卡面 / 闪卡文件。
