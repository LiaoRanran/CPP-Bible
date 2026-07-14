# UB-L5 const_cast mutation（去除 const 后修改真 const 对象）

**分类**：类型/常量性 UB ｜ **检测工具**：`-Wcast-qual` / 崩溃 / 静默
**源码**：[ub_const_cast_mutation.cpp](./ub_const_cast_mutation.cpp)

---

## ① 真实代码

```cpp
#include <cstdio>

const int G = 5;                 // 真正 const 对象

int main() {
    const_cast<int&>(G) = 10;   // ❌ 修改真正 const 对象 → UB
    std::printf("G = %d\n", G);
    return 0;
}
```

## ② 编译器行为（本机实测，GCC 15.3.0 `-Wcast-qual`）

**未报 `-Wcast-qual`**（GCC 的 `-Wcast-qual` 主要针对 C 风格强转移除 const；
C++ `const_cast` 此处不触发该警告，属已知缺口）。代码照常编译。

## ③ 运行时表现（本机实测）

```
G = 5
(exit 0)
```

> 程序"正常"结束，打印 `5` 而非 `10`。原因：编译器将 `const int G` 视为编译期常量，
> `printf` 处直接内联了 `5`——`const_cast` 的写入要么落在只读页被忽略，要么改变了
> 内存但该读已被常量折叠。这正说明 **UB 的表现依赖编译器优化**：同一份代码在把 `G`
> 放进只读段的平台/配置下会 **SIGSEGV**，在本机却"看似正确"。

## ④ 根因

`const_cast` 仅移除类型系统的 `const` 限定，**不授予写入真正 const 对象的权限**。
若原对象本身是 `const`（如 `const int G`、或 `const` 成员），写它属于 UB。
仅当原对象底层**非 const**（如 `int x; const int& r = x; const_cast<int&>(r)=1;` 合法）
时修改才定义良好。

## ⑤ 修复

```cpp
// 需要可变：从一开始就不要 const
int G = 5;
G = 10;                       // ✅ 底层本就非常量

// 或运行时确定的常量用 mutable / 去掉 const 限定声明
// 绝不 const_cast 去改 constexpr / 全局 const 对象
```

> 经验法则：`const_cast` 只用于"去掉本就非常量对象的 const 引用/指针"；
> 对真正 `const` 对象动用它是 UB，且在不同平台表现截然不同（静默 / 崩溃）。
