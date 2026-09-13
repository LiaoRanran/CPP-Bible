# MIS-MEM-003（misconception）

## 正面

【误解】MIS-MEM-003 return std::move(local) 能加速返回
触发说法：返回局部变量时加 move 是帮编译器一把

## 背面

为什么错：返回局部对象时编译器本就允许 NRVO / 隐式移动，加 std::move 反而阻断 NRVO
反例 1：对返回值而言 std::move 把 lvalue 转 xvalue，使 NRVO 不再适用——是减效不是增效
关联原子：ATOM-MEM-MOVE-002
