# MIS-CONC-004（misconception）

## 正面

【误解】MIS-CONC-004 std::async 默认就会起新线程并行执行
触发说法：async 就是异步，肯定开线程

## 背面

为什么错：默认策略是 async|deferred，实现可二选一 → 可能完全在调用线程串行执行
反例 1：需要真并行必须显式传 std::launch::async
