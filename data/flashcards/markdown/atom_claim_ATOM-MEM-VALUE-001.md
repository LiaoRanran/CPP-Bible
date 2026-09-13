# ATOM-MEM-VALUE-001（atom_claim）

## 正面

【MEM】ATOM-MEM-VALUE-001
以下论断是否成立？依据是什么？
C++11 起每个表达式属于两个正交维度（glvalue 有身份 / rvalue 可移动）的交叉：lvalue = glvalue∧¬rvalue， xvalue = glvalue∧rvalue，prvalue = ¬glvalue∧rvalue。std::move(x) 把 lvalue 转为 xvalue（decltype 得 T&&， 不是 prvalue 的 T）；临时对象/字面量是 prvalue；具名右值引用在表达式体内是左值（decltype 得 T&）。

## 背面

论断：C++11 起每个表达式属于两个正交维度（glvalue 有身份 / rvalue 可移动）的交叉：lvalue = glvalue∧¬rvalue， xvalue = glvalue∧rvalue，prvalue = ¬glvalue∧rvalue。std::move(x) 把 lvalue 转为 xvalue（decltype 得 T&&， 不是 prvalue 的 T）；临时对象/字面量是 prvalue；具名右值引用在表达式体内是左值（decltype 得 T&）。
边界：{'standard': ['C++11', 'C++14', 'C++17', 'C++20', 'C++23'], 'compilers': ['GCC 15.3.0'], 'opt': ['-O2'], 'platform': ['x86-64 MinGW-w64']}
关键证据：
  - EV-MEM-006: confirm
  - EV-MEM-007: confirm
