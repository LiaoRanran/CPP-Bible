# ATOM-HIST-AUTOPTR-001（atom_claim）

## 正面

【HIST】ATOM-HIST-AUTOPTR-001
以下论断是否成立？依据是什么？
std::auto_ptr 的"拷贝构造"签名是 auto_ptr(auto_ptr&)（非 const 左值引用）：它**不满足** CopyConstructible，却能从非 const 对象"拷贝"，且拷贝后**源被清空**（转移所有权）。 这是 C++98 缺少移动语义时的工程妥协——用拷贝的语法表达转移的语义，因而与容器 "拷贝后两对象等价"的隐含约定从根上冲突。C++11 用移动语义（unique_ptr）给出正确表达后， auto_ptr 被弃用（C++11 deprecated → C++17 从标准移除）。

## 背面

论断：std::auto_ptr 的"拷贝构造"签名是 auto_ptr(auto_ptr&)（非 const 左值引用）：它**不满足** CopyConstructible，却能从非 const 对象"拷贝"，且拷贝后**源被清空**（转移所有权）。 这是 C++98 缺少移动语义时的工程妥协——用拷贝的语法表达转移的语义，因而与容器 "拷贝后两对象等价"的隐含约定从根上冲突。C++11 用移动语义（unique_ptr）给出正确表达后， auto_ptr 被弃用（C++11 deprecated → C++17 从标准移除）。
边界：{'standard': ['C++98', 'C++11', 'C++14', 'C++17', 'C++23'], 'compilers': ['GCC 15.3.0', 'GCC 13.3.0', 'Clang 18.1.3'], 'opt': ['-O2'], 'platform': ['x86-64 MinGW-w64', 'x86-64 Linux']}
关键证据：
  - EV-HIST-001: confirm
  - EV-MEM-003: confirm
