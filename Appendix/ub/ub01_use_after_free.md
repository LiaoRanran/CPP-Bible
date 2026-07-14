# UB-01 use-after-free（释放后使用）

**分类**：内存生命周期 UB ｜ **检测工具**：ASan / GCC `-Wuse-after-free`
**源码**：[ub_use_after_free.cpp](./ub_use_after_free.cpp)

---

## ① 真实代码

```cpp
#include <cstdio>
#include <cstdlib>

int main() {
    int* p = static_cast<int*>(std::malloc(sizeof(int)));
    *p = 42;
    std::printf("before free: *p = %d\n", *p);
    std::free(p);          // p 指向的内存归还堆
    *p = 7;                // ❌ UB：释放后写
    std::printf("after free: *p = %d\n", *p);  // ❌ UB：释放后读
    return 0;
}
```

## ② 编译器行为（本机实测，GCC 15.3.0 `-Wall`）

```
ub_use_after_free.cpp: In function 'int main()':
ub_use_after_free.cpp:13:16: warning: pointer 'p' used after 'void free(void*)' [-Wuse-after-free]
   13 |     std::printf("after free: *p = %d\n", *p);
ub_use_after_free.cpp:11:14: note: call to 'void free(void*)' here
   11 |     std::free(p);
ub_use_after_free.cpp:12:8: warning: pointer 'p' used after 'void free(void*)' [-Wuse-after-free]
   12 |     *p = 7;
   11 |     std::free(p);
```

> GCC 13+ 的 `-Wuse-after-free` 已能**静态**定位释放后使用。这是本机真实捕获，无需 sanitizer 运行时。

## ③ 运行时表现（本机实测，无 sanitizer）

```
before free: *p = 42
after free: *p = 7
```
退出码 `0`，**看似正常**。这正是 use-after-free 最危险之处：多数情况下它不崩溃，而是
悄悄读到已被分配器复用或填充防护值的内存，埋下随机性数据损坏。

## ④ ASan 报告格式（DOC-REPORT，非本机捕获）

> 以下为在具备 `libasan` 的工具链（Linux GCC / Clang / MSVC）上的**预期**栈回溯格式，
> 取自 GCC/ASan 官方文档，供读者在其环境对照：

```
==12345==ERROR: AddressSanitizer: heap-use-after-free on address 0x602000000010 at pc 0x...
READ of size 4 at 0x602000000010 thread T0
    #0 0x... in main ub_use_after_free.cpp:13
    #1 0x... in __libc_start_main
0x602000000010 is located 0 bytes inside of 4-byte region [0x602000000010,0x602000000010)
freed by thread T0 here:
    #0 0x... in free intercept
    #1 0x... in main ub_use_after_free.cpp:11
previously allocated by thread T0 here:
    #0 0x... in malloc intercept
    #1 0x... in main ub_use_after_free.cpp:8
```

## ⑤ 根因

`std::free(p)` 将 `p` 指向的堆块归还分配器后，该地址的**对象生命周期已结束**。
随后对 `*p` 的读写访问的是「不再属于本对象」的内存——分配器可能已将其分配给
其他代码、填入 `0xDEADBEEF` 防护字节，或保持原值。行为完全未定义。

## ⑥ 修复

```cpp
#include <cstdio>
#include <memory>

int main() {
    auto p = std::make_unique<int>(42);   // RAII：离开作用域自动释放
    std::printf("before reset: *p = %d\n", *p);
    // 不再手动 free；需要提前释放用 p.reset()
    std::printf("after scope: 对象已安全销毁，无悬垂\n");
    return 0;
}
```

用 `std::unique_ptr`/`std::vector` 等 RAII 类型，把生命周期交给作用域，从根源消除
use-after-free。
