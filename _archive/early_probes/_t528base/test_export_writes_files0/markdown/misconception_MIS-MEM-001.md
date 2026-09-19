# MIS-MEM-001（misconception）

## 正面

【误解】MIS-MEM-001 std::move 会移动对象
触发说法：std::move(x) 之后 x 就被搬空了

## 背面

为什么错：std::move 只是 static_cast<T&&>(x)，本身不生成任何指令 [expr.static.cast]
反例 1：移动是否发生取决于重载决议是否选中移动构造；源对象仅保证有效但未指定 [lib.types.movedfrom]
关联原子：ATOM-MEM-MOVE-002
