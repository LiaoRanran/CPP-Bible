---
id: MIS-MEM-018
name: "T&& 就是右值引用（混淆推导语境下的万能引用）"
level: deep
domain: MEM
trigger_patterns:
  - "T&& 就是右值引用，模板参数和普通声明没区别"
  - "看到 && 就是右值引用"
refutations:
  - "实测 EV-MEM-021：推导语境的模板 T&& 传**左值**时推 T=int&，T&& 经引用折叠成 int&（左值引用）；只有传右值才推 T=int、T&& 才是右值引用——T&& 是否为右值引用取决于实参，不是写死的"
  - "T&& 只有在**推导语境**（[temp.deduct.call] 特判）下才是万能引用：auto&& 同理、const T&& 不是（无左值特判，实测只接右值 T=int）；非推导语境下的 T&&（如 std::move 的返回类型）就是普通右值引用（见 ATOM-MEM-VALUE-002 / EV-MEM-021）"
source: References/32 G5 第二批指令 §一.1；ATOM-MEM-VALUE-002 / EV-MEM-021
related_atoms: [ATOM-MEM-VALUE-002, ATOM-MEM-VALUE-001]
---

# MIS-MEM-018 · "T&& 就是右值引用"（混淆万能引用）

**层级**：deep —— 结构性误解，源于把"T&&"当单一语法概念、未区分"声明语境"与"推导语境"；须 ≥2 条独立反例才可能纠偏

## 触发模式（学习者常这么说 / 这么写）
- T&& 就是右值引用，模板参数和普通声明没区别
- 看到 && 就是右值引用

## 为什么它不成立
1. 实测 EV-MEM-021：推导语境的模板 T&& 传**左值**时推 T=int&，T&& 经引用折叠成 int&（左值引用）；只有传右值才推 T=int、T&& 才是右值引用——T&& 是否为右值引用取决于实参，不是写死的
2. T&& 只有在**推导语境**（[temp.deduct.call] 特判）下才是万能引用：auto&& 同理、const T&& 不是（无左值特判，实测只接右值 T=int）；非推导语境下的 T&&（如 std::move 的返回类型）就是普通右值引用（见 ATOM-MEM-VALUE-002 / EV-MEM-021）

## 出处与关联
- 出处：References/32 G5 第二批指令 §一.1；ATOM-MEM-VALUE-002 / EV-MEM-021
- 关联原子：ATOM-MEM-VALUE-002、ATOM-MEM-VALUE-001
