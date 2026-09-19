# MIS-STL-004（misconception）

## 正面

【误解】MIS-STL-004 clear() 会释放 vector 占用的内存
触发说法：clear 之后内存就还了

## 背面

为什么错：clear() 只析构元素，capacity() 不变——内存仍被容器持有；释放在 shrink_to_fit() 或换用空 vector 交换
