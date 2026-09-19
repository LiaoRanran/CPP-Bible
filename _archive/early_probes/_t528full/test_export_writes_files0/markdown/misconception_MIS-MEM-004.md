# MIS-MEM-004（misconception）

## 正面

【误解】MIS-MEM-004 对 const 对象 std::move 也能省掉拷贝
触发说法：const T 也能 move，反正只是转换

## 背面

为什么错：std::move(const T&) 得到 const T&&，无法绑定 T&& 移动构造 → 静默退化为拷贝构造
关联原子：ATOM-MEM-MOVE-002
