# MIS-STL-003（misconception）

## 正面

【误解】MIS-STL-003 用 map::operator[] 做只读存在性判断不会改动容器
触发说法：if (m[k]) 只是看看有没有

## 背面

为什么错：operator[] 对不存在的键会**插入**该键并值初始化 → 容器被改动、size 变化
反例 1：只读查询用 find() / contains()（C++20）
