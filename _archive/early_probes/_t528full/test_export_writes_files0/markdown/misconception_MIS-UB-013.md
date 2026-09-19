# MIS-UB-013（misconception）

## 正面

【误解】MIS-UB-013 f(i++, i++) 在所有标准版本都是未定义行为
触发说法：同一表达式改两次 i 就是 UB，C++17 也一样

## 背面

为什么错：C++17（P0145R3）把**函数实参初始化**从 unsequenced 改为 indeterminately sequenced → 该式在 C++17 起是 unspecified
反例 1：而运算符操作数仍为 unsequenced，故 i = i++ + ++i 在**所有版本**都是 UB——必须用版本区分
关联原子：ATOM-UB-GRAY-001
