# UB-L3 vptr corruption（虚表指针损坏）

**分类**：对象模型 UB ｜ **检测工具**：ASan / Valgrind / 崩溃
**源码**：[ub_vptr_corruption.cpp](./ub_vptr_corruption.cpp)

---

## ① 真实代码

```cpp
#include <cstdio>

struct Base {
    virtual int f() { return 1; }
    virtual ~Base() = default;
};

int main() {
    Base b;
    *reinterpret_cast<void**>(&b) = nullptr;   // ❌ 把对象首字（vptr）覆写成 nullptr
    std::printf("calling virtual...\n");
    return b.f();                               // ❌ 经损坏 vptr 的虚调用
}
```

## ② 编译器行为（本机实测）

**无警告**。`reinterpret_cast` 写 vptr 是程序员"主动"的 UB，编译器信任。

## ③ 运行时表现（本机实测）

```
calling virtual...
(exit 1 — access violation / 空 vptr 解引用崩溃)
```

> 虚调用经被覆写为 `nullptr` 的 vptr 解引用 → 访问违规崩溃。本例是**可控的最小复现**：
> 真实场景里 vptr 损坏常来自 `memcpy`/`memset` 越过对象边界、类型双关写错偏移、或
> placement-new 未先调析构就覆盖含虚函数的对象。

## ④ 根因

多态对象的**首字节（通常）存放虚表指针（vptr）**，指向该类型虚函数表。`*reinterpret_cast<void**>(&b)=nullptr`
把 vptr 改成非法地址；`b.f()` 的底层 `call [vptr+offset]` 解引用 0 → 崩溃。

## ⑤ 正确做法

```cpp
// 1) 用基类指针/引用做多态，绝不手工写 vptr
Base* p = new Derived();   // ✅ 构造自动设正确 vptr
p->f();                     // ✅ 虚调用经合法 vptr

// 2) 复用内存必须先析构再构造（placement new 配对）
std::destroy_at(p);                       // 调 ~Derived，恢复/清理
new (p) Derived();                        // 重新设 vptr

// 3) 绝不用 memcpy 覆盖含虚函数的对象整体——会清掉正确 vptr
```

> 经验：vptr 是编译器实现细节（ABI），**任何**手写覆盖对象首字的操作都是 UB。
> 多态对象的生命周期用构造/析构管理，禁止字节级覆写。
