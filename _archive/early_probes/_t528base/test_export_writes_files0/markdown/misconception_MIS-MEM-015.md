# MIS-MEM-015（misconception）

## 正面

【误解】MIS-MEM-015 结构体成员紧密排列、sizeof 等于各成员之和；指针强转可读字段
触发说法：struct 成员一个接一个排，sizeof 就是各成员相加

## 背面

为什么错：成员按自身对齐排列，编译器插 padding，sizeof 含 padding：实测 Padded{char a; int b} 的 sizeof=8 而非 5，int 偏移 4 而非 1 [basic.align]/[class.mem]（见 ATOM-MEM-ALIGN-001 / EV-MEM-019）
反例 1：reinterpret_cast 强转指针对齐/类型双关是 UB（未对齐访问 + [strict.aliasing]），轻则读错值重则崩溃；按字节搬运用 memcpy/std::bit_cast（安全，见 ATOM-MEM-ALIGN-001 / EV-MEM-020 roundtrip=7）
关联原子：ATOM-MEM-ALIGN-001
