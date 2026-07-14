# UB-04 alignment violation（对齐违例）

**分类**：内存对齐 UB ｜ **检测工具**：UBSan (alignment) / 硬件
**源码**：[ub_alignment_violation.cpp](./ub_alignment_violation.cpp)

---

## ① 真实代码

```cpp
#include <cstdint>
#include <cstdio>

int main() {
    char buffer[8] = {0};
    // 故意取 buffer+1：int 需 4 字节对齐，buffer+1 仅 1 字节对齐 → 未定义行为
    void* mis = static_cast<void*>(buffer + 1);
    int* p = static_cast<int*>(mis);
    *p = 0xDEADBEEF;   // ❌ UB：对未对齐地址做 int 写
    std::printf("written via misaligned ptr\n");
    return 0;
}
```

## ② 编译器行为（本机实测，GCC 15.3.0 `-Wall`）

**无警告**。对齐违例属于「落入未定义行为」类，GCC 静态不报——它信任程序员保证对齐。

## ③ 运行时表现（本机实测，无 sanitizer，x86-64）

```
written via misaligned ptr
```
退出码 `0`，**静默通过**。x86-64 硬件**容忍**未对齐访问（性能略降，不报错），
所以本例在 PC 上「看起来没问题」。

> ⚠️ **平台差异（[平台]）**：同样的代码在 **ARM64 / RISC-V** 上会触发
> **总线错误（SIGBUS）** 直接崩溃——这正是「UB 依赖平台」的典型：x86 宽容，
> 嵌入式/移动端致命。跨平台代码绝不可假设硬件容忍未对齐。

## ④ UBSan 报告格式（DOC-REPORT，非本机捕获）

在具备 `libubsan` 的工具链上，`-fsanitize=alignment`（含于 `undefined`）会在存储处报：

```
ub_alignment_violation.cpp:13:9: runtime error: misaligned address 0x... for type 'int',
    which requires 4 byte alignment
0x...: note: pointer points here
 00 00 00 00 00 00 00 00
 ^
SUMMARY: UndefinedBehaviorSanitizer: undefined-behavior ub_alignment_violation.cpp:13:9
```

## ⑤ 根因

C++ 要求对象地址满足其**对齐要求**（`alignof(T)`，如 `int` 为 4）。对未满足对齐的
地址解引用是 UB：x86  silently 执行（可能跨缓存行、变慢），严格对齐架构（ARM/RISC-V）
直接硬件异常，或触发原子性破坏（未对齐的 `std::atomic` 读写）。

## ⑥ 修复

```cpp
#include <cstdint>
#include <cstdio>

int main() {
    alignas(int) char buffer[8] = {0};     // 保证整块按 int 对齐
    int* p = reinterpret_cast<int*>(buffer); // ✅ 地址已对齐
    *p = 0xDEADBEEF;
    std::printf("written via aligned ptr\n");
    return 0;
}
```

或让分配器保证对齐：`std::aligned_alloc(alignof(int), sizeof(int))`、
`std::malloc` 返回之地址对任意基础类型对齐、`std::vector`/`std::array` 按元素类型对齐。
**类型双关**优先用 `std::bit_cast`（不要求重叠对齐地址），避免 `reinterpret_cast` 跨类型踩对齐地雷。
