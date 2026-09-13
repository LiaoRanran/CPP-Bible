# MIS-UB-010（misconception）

## 正面

【误解】MIS-UB-010 const_cast 去掉 const 后写入也没关系
触发说法：我只是改一下，反正拿到的是非 const 指针

## 背面

为什么错：若原对象**本身**是 const（可能在 .rodata），写入是 UB，实测 SIGSEGV
反例 1：只有原对象非 const、仅经由 const 引用/指针访问时，去除 const 后写入才合法
