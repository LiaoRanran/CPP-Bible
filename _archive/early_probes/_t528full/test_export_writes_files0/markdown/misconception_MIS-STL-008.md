# MIS-STL-008（misconception）

## 正面

【误解】MIS-STL-008 std::sort 是稳定排序
触发说法：sort 会保持相等元素的原顺序

## 背面

为什么错：std::sort **不**保证稳定性（实现多为 introsort）；需要保持原序用 std::stable_sort
