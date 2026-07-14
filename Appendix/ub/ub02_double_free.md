# UB-02 double-free（双重释放）

**分类**：内存生命周期 UB ｜ **检测工具**：ASan / GCC `-Wuse-after-free`
**源码**：[ub_double_free.cpp](./ub_double_free.cpp)

---

## ① 真实代码

```cpp
#include <cstdlib>

int main() {
    int* p = static_cast<int*>(std::malloc(sizeof(int)));
    std::free(p);          // 第一次释放，合法
    std::free(p);          // ❌ UB：第二次释放同一指针
    return 0;
}
```

## ② 编译器行为（本机实测，GCC 15.3.0 `-Wall`）

```
ub_double_free.cpp: In function 'int main()':
ub_double_free.cpp:9:14: warning: pointer 'p' used after 'void free(void*)' [-Wuse-after-free]
    9 |     std::free(p);
ub_double_free.cpp:8:14: note: call to 'void free(void*)' here
    8 |     std::free(p);
```

> GCC 13+ 将第二次 `free` 识别为「在 `free` 之后使用指针」并报警。

## ③ 运行时表现（本机实测，无 sanitizer）

退出码 `0`，**静默通过**。MinGW 的 CRT 在未开启调试堆时不校验重复释放，后果是
分配器内部元数据（freelist 链表）被破坏——后续 `malloc` 可能返回重叠地址，
引发更难追查的二次损坏。

## ④ ASan 报告格式（DOC-REPORT，非本机捕获）

```
==12345==ERROR: AddressSanitizer: attempting double-free on address 0x602000000010 in thread T0
    #0 0x... in free intercept
    #1 0x... in main ub_double_free.cpp:9
0x602000000010 is located 0 bytes inside of 4-byte region [0x602000000010,0x602000000010)
freed by thread T0 here:
    #0 0x... in free intercept
    #1 0x... in main ub_double_free.cpp:8
```

## ⑤ 根因

释放后的指针成为**悬垂指针**（dangling）。对同一地址再次 `free` 会让分配器
把已处于 freelist 中的块再次摘链，造成链表环或跨块覆盖。这是堆腐败（heap corruption）
的经典入口。

## ⑥ 修复

```cpp
#include <cstdlib>

int main() {
    int* p = static_cast<int*>(std::malloc(sizeof(int)));
    std::free(p);
    p = nullptr;          // 释放后立即置空，二次 free(nullptr) 是良定义（no-op）
    std::free(p);         // ✅ 安全：free(nullptr) 定义良好
    return 0;
}
```

更优解：用 `std::unique_ptr`，其析构对空指针安全且不可重复调用。若必须用裸指针，
遵循「释放即置 `nullptr`」纪律——`free(nullptr)`/`delete nullptr` 均为良定义。
