# MIS-UB-006（misconception）

## 正面

【误解】MIS-UB-006 for (int x : make()) 遍历临时容器是安全的
触发说法：范围 for 会帮我把临时容器留住

## 背面

为什么错：C++17 起范围 for 的临时对象不再被延长到循环结束（init-statement 之后的临时在循环外即销毁）
反例 1：结果是迭代器悬垂 → UB；应写成 for (auto&& c = make(); int x : c)
