# MIS-UB-012（misconception）

## 正面

【误解】MIS-UB-012 函数实参的求值顺序是确定的，可以依赖它
触发说法：f(g(), h()) 一定先算 g 再算 h

## 背面

为什么错：实参初始化是**不确定顺序**（indeterminately sequenced），只保证不重叠、不保证先后
反例 1：实测 GCC 输出 h/g（右→左）、Clang 输出 g/h（左→右）——连编译器之间都相反
关联原子：ATOM-UB-GRAY-001
