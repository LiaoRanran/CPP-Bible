# MIS-PERF-002（misconception）

## 正面

【误解】MIS-PERF-002 for (auto x : vec) 不会拷贝元素
触发说法：auto 自动推导，不会拷贝

## 背面

为什么错：按值 auto x 会拷贝每个元素；只读应写 const auto&（-Wrange-loop-construct 可告警）
