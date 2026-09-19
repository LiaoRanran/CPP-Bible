# MIS-HIST-001（misconception）

## 正面

【误解】MIS-HIST-001 auto_ptr 和 unique_ptr 差不多，只是名字旧一点
触发说法：auto_ptr 就是老版本的 unique_ptr

## 背面

为什么错：两者对拷贝的处置相反：auto_ptr 允许拷贝（且静默转移+清空源），unique_ptr 拷贝构造 = delete（编译期拒绝）
关联原子：ATOM-HIST-AUTOPTR-001
