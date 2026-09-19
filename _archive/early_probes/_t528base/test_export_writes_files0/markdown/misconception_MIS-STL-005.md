# MIS-STL-005（misconception）

## 正面

【误解】MIS-STL-005 reserve(n) 之后 capacity() 恰好等于 n
触发说法：reserve(100) 后 capacity 就是 100

## 背面

为什么错：标准只保证 capacity() **至少** n，实现可给更大（如按 2 的幂向上取整）
