# MIS-PERF-006（misconception）

## 正面

【误解】MIS-PERF-006 多插 __builtin_prefetch 一定更快
触发说法：预取多加无害

## 背面

为什么错：预取距离错了（太早被淘汰 / 太晚来不及）纯属浪费指令带宽，甚至挤占缓存
