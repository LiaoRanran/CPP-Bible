# MIS-MEM-008（misconception）

## 正面

【误解】MIS-MEM-008 new/delete 与 new[]/delete[] 可以混用
触发说法：delete 一个 new[] 出来的数组只是少调几个析构

## 背面

为什么错：混用是未定义行为：new[] 会在块头存元素个数，delete 按单对象布局释放 → 堆损坏
