---
id: MIS-CONC-008
name: 线程对象既不 join 也不 detach，只是警告一下
level: surface
domain: CONC
trigger_patterns:
  - "忘了 join 顶多资源泄漏"
  - "thread 析构会帮我处理"
refutations:
  - "可汇合（joinable）的 thread 析构时调用 std::terminate → 程序直接终止"
source: ch93_thread_async.md ⑯ 易错点
related_atoms: []
---

# MIS-CONC-008 · 线程对象既不 join 也不 detach，只是警告一下

**层级**：surface —— 表层误解，一次纠正即可

## 触发模式（学习者常这么说 / 这么写）
- 忘了 join 顶多资源泄漏
- thread 析构会帮我处理

## 为什么它不成立
1. 可汇合（joinable）的 thread 析构时调用 std::terminate → 程序直接终止

## 出处与关联

- 出处：ch93_thread_async.md ⑯ 易错点
- 关联原子：（暂无，待相关原子锻造后回填）
