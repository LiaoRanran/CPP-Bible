# UB-03 stack-use-after-scope（栈对象越界使用）

**分类**：内存生命周期 UB ｜ **检测工具**：ASan / GCC `-Wdangling-pointer=`
**源码**：[ub_stack_after_scope.cpp](./ub_stack_after_scope.cpp)

---

## ① 真实代码

```cpp
#include <cstdio>

int* leaked = nullptr;

void f() {
    int x = 5;        // 局部变量，生命周期限于 f()
    leaked = &x;      // ❌ 保存指向局部变量的指针
}                     // x 在此销毁，leaked 变为悬垂

int main() {
    f();
    *leaked = 10;     // ❌ UB：作用域外写栈内存
    std::printf("leaked = %d\n", *leaked);
    return 0;
}
```

## ② 编译器行为（本机实测，GCC 15.3.0 `-Wall`）

```
ub_stack_after_scope.cpp: In function 'void f()':
ub_stack_after_scope.cpp:10:12: warning: storing the address of local variable 'x' in 'leaked' [-Wdangling-pointer=]
   10 |     leaked = &x;
ub_stack_after_scope.cpp:9:9: note: 'x' declared here
    9 |     int x = 5;
ub_stack_after_scope.cpp:6:6: note: 'leaked' declared here
    6 | int* leaked = nullptr;
```

> `-Wdangling-pointer=` 是 GCC 12+ 的指针逃逸分析成果，能静态抓到「局部地址外泄」。

## ③ 运行时表现（本机实测，无 sanitizer）

```
leaked = 10
```
退出码 `0`，**看似正常**。`f()` 返回后 `x` 的栈槽尚未被覆盖，`*leaked = 10` 恰好写进
那个仍「温热」的栈槽——但一旦后续函数调用复用该栈空间，值立即被冲掉，表现为
「偶发性」数据错误。

## ④ ASan 报告格式（DOC-REPORT，非本机捕获）

在具备 `libasan` 的工具链上，`-fsanitize=address` 会在 `f()` 返回后毒化（poison）
`x` 的栈槽，越界访问即报：

```
==12345==ERROR: AddressSanitizer: stack-use-after-scope on address 0x7ffd... at pc 0x...
READ/WRITE of size 4 at 0x7ffd... thread T0
    #0 0x... in main ub_stack_after_scope.cpp:15
Address 0x7ffd... is located in stack of thread T0 at offset ... in frame
    #0 0x... in f() ub_stack_after_scope.cpp:8
  This frame has 1 object(s):
    [32, 36) 'x' (line 9) <== Memory access at offset ... is inside this variable
```

## ⑤ 根因

具有自动存储期的局部变量在作用域结束（本例 `f()` 返回）时销毁，其栈内存归还
给栈帧分配器。持有其地址的指针变成悬垂；越界使用等于读写「已不属于本对象」的栈槽。

## ⑥ 修复

```cpp
#include <cstdio>
#include <memory>

int main() {
    auto x = std::make_unique<int>(5);   // 提升到堆，生命周期独立
    int* leaked = x.get();               // 或按值返回 / std::move
    *leaked = 10;
    std::printf("leaked = %d\n", *leaked);
    return 0;
}
```

原则：**不返回/不保存指向局部非静态对象的指针或引用**。需要跨作用域存活就用
堆对象（`std::unique_ptr`/`std::shared_ptr`）或值语义。
