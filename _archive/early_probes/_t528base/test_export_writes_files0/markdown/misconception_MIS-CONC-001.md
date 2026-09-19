# MIS-CONC-001（misconception）

## 正面

【误解】MIS-CONC-001 volatile 可以用于线程间同步 / 当数据就绪标志
触发说法：volatile bool ready 就能当标志位

## 背面

为什么错：volatile 只保证不被优化掉、不重排到同一线程内的 volatile 访问之外；**不**提供原子性、不提供跨线程 happens-before
反例 1：线程同步要用 std::atomic 配内存序（默认 seq_cst）
关联原子：ATOM-UB-GRAY-001
