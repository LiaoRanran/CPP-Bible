# UB-L1 dangling reference（悬垂引用/指针）

**分类**：生命周期 UB ｜ **检测工具**：GCC `-Wreturn-local-addr` / ASan
**源码**：[ub_dangling_reference.cpp](./ub_dangling_reference.cpp)

---

## ① 真实代码

```cpp
#include <cstdio>

int* dangling() {
    int x = 5;
    return &x;            // ❌ 返回局部变量地址 → 悬垂
}

int main() {
    int* p = dangling();
    *p = 10;              // ❌ 写已销毁的栈槽
    std::printf("value = %d\n", *p);
    return 0;
}
```

## ② 编译器行为（本机实测，GCC 15.3.0 `-Wall`）

```
ub_dangling_reference.cpp:7:12: warning: address of local variable 'x' returned [-Wreturn-local-addr]
```

> 注意：**引用版本 `int& f(){ int x; return x; }` 在 GCC 15.3 已是硬错误**（
> `cannot bind non-const lvalue reference ... to an rvalue`），比 warning 更严。
> 指针版本仍仅为 warning——但同样是 UB。

## ③ 运行时表现（本机实测）

```
Segmentation fault (exit 139 = SIGSEGV)
```

解引用悬垂指针写越界栈 → 访问违规崩溃。vs 之前内存批中「use-after-free 静默通过」
的对照：崩溃与否取决于栈槽是否仍映射、是否被复用——**不可预测**。

## ④ ASan 报告格式（DOC-REPORT，非本机捕获）

```
==12345==ERROR: AddressSanitizer: stack-use-after-return on address 0x...
    #0 0x... in main ub_dangling_reference.cpp:12
address ... is located in stack of thread T0 at offset ... in frame
    #0 0x... in dangling() ub_dangling_reference.cpp:5
```

## ⑤ 根因与修复

局部变量在作用域结束时销毁，其地址/引用随之悬垂。修复：返回对象（值/移动）、
提升到堆（`std::unique_ptr`）、或返回引用前确认目标生命周期覆盖使用点。

```cpp
#include <memory>
std::unique_ptr<int> make() { return std::make_unique<int>(5); }  // 堆对象，生命周期独立
```
