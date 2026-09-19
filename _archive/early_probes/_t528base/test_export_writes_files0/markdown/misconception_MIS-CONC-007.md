# MIS-CONC-007（misconception）

## 正面

【误解】MIS-CONC-007 原子操作省略内存序参数时默认是 relaxed
触发说法：不写内存序就是最松的

## 背面

为什么错：默认（以及 ++/--/赋值等运算符重载）是 **memory_order_seq_cst**，即最强顺序一致
