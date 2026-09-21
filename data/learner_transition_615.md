# 615 D3 · 跃迁触发条件机器判定（门是否在开启）

> 触发条件：掌握度≥0.8 **且** OOD≥0.8。**只判定，不自动触发任何跃迁**。

## 一、门状态

- **门状态 = `closed`**（triggered 0 / ready 5 / not_ready 22）
- 开门数字：真实学习事件 **0/50**（未达标，模拟数据不计入）

## 二、27 KC 跃迁状态

| KC | 掌握度 | OOD | 状态 |
|---|---|---|---|
| `ATOM-CONC-FENCE-001` | 0.7206 | 0.0 | not_ready |
| `ATOM-CONC-LOCK-001` | 0.9762 | 0.0 | ready |
| `ATOM-CONC-RACE-001` | 0.8957 | 0.0 | ready |
| `ATOM-HIST-AUTOPTR-001` | 0.6507 | 0.0 | not_ready |
| `ATOM-LANG-INLINE-001` | 0.7206 | 0.0 | not_ready |
| `ATOM-MEM-ALIGN-001` | 0.9068 | 0.0 | ready |
| `ATOM-MEM-ALLOC-001` | 0.9762 | 0.0 | ready |
| `ATOM-MEM-ALLOC-002` | 0.9382 | 0.0 | ready |
| `ATOM-MEM-LEAK-001` | 0.2675 | 0.0 | not_ready |
| `ATOM-MEM-LEAK-002` | 0.2536 | 0.0 | not_ready |
| `ATOM-MEM-MOVE-002` | 0.1 | 0.0 | not_ready |
| `ATOM-MEM-NEW-001` | 0.1 | 0.0 | not_ready |
| `ATOM-MEM-PERF-001` | 0.1 | 0.0 | not_ready |
| `ATOM-MEM-PERF-002` | 0.1 | 0.0 | not_ready |
| `ATOM-MEM-PERF-003` | 0.1 | 0.0 | not_ready |
| `ATOM-MEM-PERF-004` | 0.1 | 0.0 | not_ready |
| `ATOM-MEM-RAII-001` | 0.1 | 0.0 | not_ready |
| `ATOM-MEM-RAII-002` | 0.1 | 0.0 | not_ready |
| `ATOM-MEM-RVREF-001` | 0.1 | 0.0 | not_ready |
| `ATOM-MEM-SHARED-001` | 0.1 | 0.0 | not_ready |
| `ATOM-MEM-SHARED-002` | 0.1 | 0.0 | not_ready |
| `ATOM-MEM-UNIQUE-001` | 0.1 | 0.0 | not_ready |
| `ATOM-MEM-UNIQUE-002` | 0.1 | 0.0 | not_ready |
| `ATOM-MEM-VALUE-001` | 0.1 | 0.0 | not_ready |
| `ATOM-MEM-VALUE-002` | 0.1 | 0.0 | not_ready |
| `ATOM-MEM-WEAK-001` | 0.1 | 0.0 | not_ready |
| `ATOM-UB-GRAY-001` | 0.1 | 0.0 | not_ready |

## 三、诚实声明

- 当前真实学习事件 = **0**，门状态 = **`closed`**，学习者闭环**尚未开启**。
- 跃迁检测器**只做判定，不自动触发任何跃迁**；开门需真实学习事件 + 人审。


