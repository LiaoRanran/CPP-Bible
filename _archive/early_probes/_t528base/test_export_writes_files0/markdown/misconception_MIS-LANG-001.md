# MIS-LANG-001（misconception）

## 正面

【误解】MIS-LANG-001 以为 inline 函数各 TU 写成不同实现也没关系（编译器/链接器会发现并报错）
触发说法：inline 就是「每个 TU 私有一份」，各写各的实现没关系

## 背面

为什么错：ODR 要求同一实体的多个定义「consist of the same sequence of tokens」（[basic.def.odr]/16.4）；违反属 IFNDR——**无须诊断**：实测 -Wall -Wextra 编译两个不同定义的 TU，零警告零错误（EV-LANG-001 D1 行）
反例 1：行为不是「确定的」：-O0 下链接器取先遇到的 weak 定义，仅交换两个 .o 的链接顺序，同一程序的输出就从 tu_a=1,tu_b=1 变成 tu_a=2,tu_b=2（EV-LANG-001 E1/E2）
反例 2：「固定链接顺序」也兜不住：换到 -O2，两个 TU 各自内联自己看到的定义，形态变成「各用各的」（1/2）且与顺序无关——同一 UB 的第二种合法表现（EV-LANG-002 §1）
关联原子：ATOM-LANG-INLINE-001
