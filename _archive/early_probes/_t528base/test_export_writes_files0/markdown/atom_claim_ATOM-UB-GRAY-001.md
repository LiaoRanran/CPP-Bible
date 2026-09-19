# ATOM-UB-GRAY-001（atom_claim）

## 正面

【UB】ATOM-UB-GRAY-001
以下论断是否成立？依据是什么？
`f(g(), h())` 的实参求值顺序是**未指定**（unspecified）：两种顺序都合法、程序不会崩，但不可依赖； **未测序（unsequenced）的同一标量修改**（如 `i = i++ + ++i`）与**通过不兼容类型指针访问对象** （严格别名）属于**未定义行为**，标准不再要求任何行为，优化器可据此删除你的访问。 （版本边界：函数实参 `f(i++, i++)` 自 **C++17 起是 _indeterminately sequenced_** → **unspecified**； C++11/14 下才是 UB。）

## 背面

论断：`f(g(), h())` 的实参求值顺序是**未指定**（unspecified）：两种顺序都合法、程序不会崩，但不可依赖； **未测序（unsequenced）的同一标量修改**（如 `i = i++ + ++i`）与**通过不兼容类型指针访问对象** （严格别名）属于**未定义行为**，标准不再要求任何行为，优化器可据此删除你的访问。 （版本边界：函数实参 `f(i++, i++)` 自 **C++17 起是 _indeterminately sequenced_** → **unspecified**； C++11/14 下才是 UB。）
边界：{'standard': ['C++11', 'C++14', 'C++17', 'C++23'], 'compilers': ['GCC 15.3.0', 'GCC 13.1.0', 'GCC 8.1.0', 'Clang (CI ubuntu-latest runner 默认)'], 'opt': ['-O0', '-O2'], 'platform': ['x86-64 MinGW-w64', 'x86-64 Linux']}
关键证据：
  - EV-UB-001: confirm
  - EV-UB-002: confirm
