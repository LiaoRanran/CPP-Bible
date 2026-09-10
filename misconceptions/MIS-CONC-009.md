---
id: MIS-CONC-009
name: stop_token 能主动把线程停下来
level: deep
domain: CONC
trigger_patterns:
  - "request_stop() 之后线程就会停"
  - "stop_token 是强制中断"
refutations:
  - "停止是**协作**的：request_stop 只置位，线程须主动检查 stop_requested() 并返回"
  - "线程从不检查 → jthread 析构时 join 永久阻塞；阻塞系统调用须用 stop_callback 唤醒"
source: ch94_stop_token.md ⑯ 易错点
related_atoms: []
---

# MIS-CONC-009 · stop_token 能主动把线程停下来

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏（认知科学依据：一次纠正不够）

## 触发模式（学习者常这么说 / 这么写）
- request_stop() 之后线程就会停
- stop_token 是强制中断

## 为什么它不成立
1. 停止是**协作**的：request_stop 只置位，线程须主动检查 stop_requested() 并返回
2. 线程从不检查 → jthread 析构时 join 永久阻塞；阻塞系统调用须用 stop_callback 唤醒

## 出处与关联

- 出处：ch94_stop_token.md ⑯ 易错点
- 关联原子：（暂无，待相关原子锻造后回填）
