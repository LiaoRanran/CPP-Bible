# MIS-CONC-002（misconception）

## 正面

【误解】MIS-CONC-002 memory_order_relaxed 可以当数据已就绪的标志位用
触发说法：用 relaxed 的 flag 表示数据写完了

## 背面

为什么错：relaxed 只保证原子性，不建立同步关系 → 读线程可能看到 flag 为真却读到未初始化的数据
反例 1：发布-订阅要用 release/acquire 配对（或 seq_cst）
