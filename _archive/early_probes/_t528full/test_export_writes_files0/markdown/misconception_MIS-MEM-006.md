# MIS-MEM-006（misconception）

## 正面

【误解】MIS-MEM-006 用同一个裸指针构造两个 shared_ptr 也能正常共享引用计数
触发说法：shared_ptr<int> a(p); shared_ptr<int> b(p); 两个一起管

## 背面

为什么错：两个独立控制块各自计数 → 双重释放（double free），不是共享
反例 1：正确做法是 shared_ptr<int> b = a;（共享控制块）或用 enable_shared_from_this
