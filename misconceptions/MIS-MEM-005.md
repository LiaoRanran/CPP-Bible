---
id: MIS-MEM-005
name: 函数里拿到 T&& 具名参数后直接用它就会自动移动
level: deep
domain: MEM
trigger_patterns:
  - "void f(T&& x) { T y = x; } 里发生的是移动"
  - "形参是右值引用，所以传下去也是右值"
refutations:
  - "函数体场景：具名右值引用是左值（[basic.lval] Note 3 原文：named rvalue references are treated as lvalues），`T y = x;` 触发拷贝构造；要移动须再写 std::move(x)"
  - "构造函数 mem-initializer-list 同样中招：`A(Probe&& x) : m(x) {}` 是拷贝，必须写成 `m(std::move(x))`——这比函数体场景更常被漏"
  - "lambda 场景：`[x]` 是拷贝捕获，且**非 mutable 的 lambda 体内** `std::move(x)` 得到的是 `const T&&`，仍退化拷贝；要移动须用 init-capture `[x = std::move(x)]`（或 `mutable` lambda——但捕获本身仍是一次拷贝，init-capture 的优势是连捕获那次也省掉）"
  - "反向误解同样错：'写了 std::move 就一定移动'——对**无移动构造**的类型，std::move 静默退化选中拷贝构造（实测 copyonly 组 copy=1）；而 `= delete` 移动构造则是编译错误（deleted 函数仍参与重载决议且被选中）"
source: ch115_move.md ⑯ 易错点 1
related_atoms: [ATOM-MEM-MOVE-002, ATOM-MEM-RVREF-001]
---

# MIS-MEM-005 · 函数里拿到 T&& 具名参数后直接用它就会自动移动

**层级**：deep —— 结构性误解，须 ≥2 条独立反例才可能纠偏（认知科学依据：一次纠正不够）

## 触发模式（学习者常这么说 / 这么写）
- void f(T&& x) { T y = x; } 里发生的是移动
- 形参是右值引用，所以传下去也是右值

## 为什么它不成立
1. 函数体场景：具名右值引用是左值（[basic.lval] Note 3 原文：named rvalue references are treated as lvalues；准确判据是 [expr.prim.id.unqual]/12，"有名字→左值"只是启发式），`T y = x;` 触发拷贝构造；要移动须再写 std::move(x)
2. 构造函数 mem-initializer-list 同样中招：`A(Probe&& x) : m(x) {}` 是拷贝，必须写成 `m(std::move(x))`——这比函数体场景更常被漏
3. lambda 场景：`[x]` 是拷贝捕获，且**非 mutable 的 lambda 体内** `std::move(x)` 得到的是 `const T&&`，仍退化拷贝；要移动须用 init-capture `[x = std::move(x)]`（或 `mutable` lambda——但捕获本身仍是一次拷贝，init-capture 的优势是连捕获那次也省掉）
4. 反向误解同样错："写了 std::move 就一定移动"——对**无移动构造**的类型，std::move 静默退化选中拷贝构造（实测 copyonly 组 copy=1）；而 `= delete` 移动构造则是编译错误（deleted 函数仍参与重载决议且被选中）

## 出处与关联

- 出处：ch115_move.md ⑯ 易错点 1；G5 原子 ATOM-MEM-RVREF-001（EV-MEM-004 三角验证）
- 关联原子：ATOM-MEM-MOVE-002, ATOM-MEM-RVREF-001
