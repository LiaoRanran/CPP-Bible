# MIS-STL-010（misconception）

## 正面

【误解】MIS-STL-010 span / string_view 拥有数据，可以返回函数内新建的数据
触发说法：返回 string_view 比返回 string 轻量，直接这么写

## 背面

为什么错：span/string_view 是**非拥有**视图，只借用；返回指向局部缓冲的视图即悬垂 → UB
反例 1：底层容器扩容后，先前取的 span 也会失效（vector 重分配）
