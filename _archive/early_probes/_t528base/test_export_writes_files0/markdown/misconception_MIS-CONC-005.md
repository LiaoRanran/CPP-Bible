# MIS-CONC-005（misconception）

## 正面

【误解】MIS-CONC-005 无锁一定比 mutex 快
触发说法：lock-free 更高级，肯定更快

## 背面

为什么错：低中竞争 + 短临界区下 mutex（用户态自旋 + futex）常更快；无锁的收益在高竞争且临界区极短时才显现
反例 1：必须基准测试；无锁还带来 ABA、内存回收等额外复杂度
