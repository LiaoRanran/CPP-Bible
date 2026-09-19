# MIS-MEM-007（misconception）

## 正面

【误解】MIS-MEM-007 在构造函数里调用 shared_from_this() 没问题
触发说法：构造函数里就能拿到自己的 shared_ptr

## 背面

为什么错：构造期间对象尚未被任何 shared_ptr 持有 → 抛 bad_weak_ptr（或未定义，取决于实现）
反例 1：标准用法：构造函数私有化 + 工厂函数返回 shared_ptr，构造完成后才用 shared_from_this
