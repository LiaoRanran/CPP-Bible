# MIS-MEM-017（misconception）

## 正面

【误解】MIS-MEM-017 std::forward 只是个 cast，写不写都行（忽略省略 forward 的运行时代价）
触发说法：std::forward 和 std::move 差不多，就是个类型转换

## 背面

为什么错：实测 EV-MEM-022：转发链省略 forward 后，右值实参 copies=1 moves=0——形参是具名变量、函数体内按左值处理（[basic.lval] Note 3），每次转发多付一次拷贝
反例 1：std::forward<T>(x) 按**推导出的 T** 恢复实参值类别（[temp.deduct.call] 特判 + 引用折叠）：右值转回右值、左值保持左值；它是'按 T 恢复类别'的 cast，不是无差别 cast，省略后类别信息丢失不可恢复（见 ATOM-MEM-VALUE-002 / EV-MEM-021）
关联原子：ATOM-MEM-VALUE-002 ATOM-MEM-MOVE-002
