# MIS-MEM-005（misconception）

## 正面

【误解】MIS-MEM-005 函数里拿到 T&& 具名参数后直接用它就会自动移动
触发说法：void f(T&& x) { T y = x; } 里发生的是移动

## 背面

为什么错：函数体场景：具名右值引用是左值（[basic.lval] Note 3 原文：named rvalue references are treated as lvalues），`T y = x;` 触发拷贝构造；要移动须再写 std::move(x)
反例 1：构造函数 mem-initializer-list 同样中招：`A(Probe&& x) : m(x) {}` 是拷贝，必须写成 `m(std::move(x))`——这比函数体场景更常被漏
反例 2：lambda 场景：`[x]` 是拷贝捕获，且**非 mutable 的 lambda 体内** `std::move(x)` 得到的是 `const T&&`，仍退化拷贝；要移动须用 init-capture `[x = std::move(x)]`（或 `mutable` lambda——但捕获本身仍是一次拷贝，init-capture 的优势是连捕获那次也省掉）
关联原子：ATOM-MEM-MOVE-002 ATOM-MEM-RVREF-001
