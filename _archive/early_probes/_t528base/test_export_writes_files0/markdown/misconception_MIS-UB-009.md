# MIS-UB-009（misconception）

## 正面

【误解】MIS-UB-009 static_cast 做多态向下转型是安全的（编译过了就对）
触发说法：Base* 转 Derived* 编译通过就说明类型对

## 背面

为什么错：static_cast 向下转型不做运行时检查；对象实际不是该派生类型时，访问派生成员即 UB
反例 1：需运行时安全用 dynamic_cast（失败返回 nullptr / 抛 bad_cast）
