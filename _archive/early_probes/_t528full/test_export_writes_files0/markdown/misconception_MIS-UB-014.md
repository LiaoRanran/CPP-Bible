# MIS-UB-014（misconception）

## 正面

【误解】MIS-UB-014 函数参数的求值顺序是未定义行为
触发说法：f(g(), h()) 里顺序不确定，所以是 UB

## 背面

为什么错：C++17（P0145R3）把实参初始化从 unsequenced 改为 **indeterminately sequenced**（[expr.call]）：不保证先后，但**绝不允许重叠** → 是 unspecified，不是 UB
反例 1：判据是副作用的**测序关系**：unsequenced（可重叠）→ UB；indeterminately sequenced（不重叠）→ unspecified。把两者混为一谈会让读者对合法代码产生不必要的恐慌
关联原子：ATOM-UB-GRAY-001
