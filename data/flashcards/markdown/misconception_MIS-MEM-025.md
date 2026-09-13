# MIS-MEM-025（misconception）

## 正面

【误解】MIS-MEM-025 unique_ptr<T[]> 只是 unique_ptr<T> 的语法糖
触发说法：数组版本就是把类型写成 T[]，没别的区别

## 背面

为什么错：接口不同：实测 EV-MEM-032 编译期 trait——`unique_ptr<int[]>` 有 operator[]（subscript=1）但**没有** operator* 与 operator->（deref=0 arrow=0）；对象特化恰好相反。这不是风格差异，是两套不同的接口约束
反例 1：释放路径不同：`unique_ptr<int[]>` 走 delete[]（operator delete[] 计数=1），而 `unique_ptr<int>` 路径的 delete[] 增量为 0——两者调用的释放函数根本不是同一个
反例 2：配对律：`new int[8]` 必须配 delete[]；用 `unique_ptr<int>` 接 `new int[]` 会让析构走 delete，属 UB（数组 Cookie 与元素析构都不会被正确处理）
关联原子：ATOM-MEM-UNIQUE-002 ATOM-MEM-NEW-001
