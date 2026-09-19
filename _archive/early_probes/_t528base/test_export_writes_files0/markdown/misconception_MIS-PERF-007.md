# MIS-PERF-007（misconception）

## 正面

【误解】MIS-PERF-007 SoA 永远比 AoS 快
触发说法：结构体拆成数组一定更快

## 背面

为什么错：若每次访问都要用到对象的**全部**字段，AoS 的局部性反而更好（一次 cache line 拿全一个对象）
反例 1：SoA 的收益只在'热循环只访问少数字段'时成立；须以 profile 数据为准
