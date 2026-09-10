---
id: MIS-CONC-004
name: std::async 默认就会起新线程并行执行
level: deep
domain: CONC
trigger_patterns:
  - "async 就是异步，肯定开线程"
  - "async(f) 和 thread(f) 差不多"
refutations:
  - "默认策略是 async|deferred，实现可二选一 → 可能完全在调用线程串行执行"
  - "需要真并行必须显式传 std::launch::async"
source: ch93_thread_async.md ⑯ 易错点
related_atoms: []
---

# MIS-CONC-004 · std::async 默认就会起新线程并行执行

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏（认知科学依据：一次纠正不够）

## 触发模式（学习者常这么说 / 这么写）
- async 就是异步，肯定开线程
- async(f) 和 thread(f) 差不多

## 为什么它不成立
1. 默认策略是 async|deferred，实现可二选一 → 可能完全在调用线程串行执行
2. 需要真并行必须显式传 std::launch::async

## 出处与关联

- 出处：ch93_thread_async.md ⑯ 易错点
- 关联原子：（暂无，待相关原子锻造后回填）
