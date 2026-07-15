## 附录：std::initializer_list 真机汇编实证（ASM-32-init_list · GCC 15.3.0 / C++26 / -O2）

> 证据：`_asm_demo/ch32_init_list_test.cpp` + `ch32_init_list_test.s`（真实编译 + `objdump -d -M intel -C`）。
> 工具链：`g++.exe (MinGW-W64 x86_64-msvcrt-posix-seh) 15.3.0`；`objdump.exe 2.46.1`。

**结论 1 — `initializer_list` 仅是一对 `{const T* _M_array, size_t _M_len}`，零分配**
布局为 ptr@offset0、len@offset8，按值传入时只传这 16 字节（Microsoft x64 ABI 下以指针传递该 16B 结构体），**无堆分配、无元素拷贝**：

```asm
; sum_il : range-for 退化为指针自增循环
mov    rdx, QWORD PTR [rcx+0x8]   ; _M_len
mov    rax, QWORD PTR [rcx]       ; _M_array
lea    rcx, [rax+rdx*4]           ; end = array + len*4
xor    edx, edx
cmp    rcx, rax
je     ...                        ; 空则跳过
add    edx, DWORD PTR [rax]       ; s += *p
add    rax, 0x4                   ; p++
cmp    rax, rcx
jne    ...
mov    eax, edx
ret
; il_begin : begin() 即返回底层数组首地址
mov    rax, QWORD PTR [rcx]
ret
```

**结论 2 — 致命陷阱：底层临时数组生命周期仅限完整表达式**

`initializer_list` 不拥有数据，它指向一个**临时数组**。一旦该数组失效，il 即悬垂：

```cpp
std::initializer_list<int> dangling_il() {
    return {1, 2, 3};   // 底层数组为临时，; 处销毁 → 悬垂
}
```

GCC 直接告警：

```
warning: returning temporary 'initializer_list' does not extend the lifetime of the underlying array [-Winit-list-lifetime]
```

真机细节：对**字面量** `{1,2,3}`，GCC 把后备数组提升为 `.rdata` 静态常量（本例 `lea rdx,[rip+0x0]` 取静态地址，运行时不悬垂）；但对**非常量元素** `{f(), g(), h()}`，后备数组是栈上临时，函数返回后必然悬垂。无论哪种，语言层的生命周期规则都终结于完整表达式——**绝不要把 `initializer_list` 存到比当前完整表达式更久的地方**（不要返回、不要存为成员/静态、不要在 range-for 之外延后使用）。

| 操作 | 代码生成 | 分配 | 注意 |
|------|----------|:----:|------|
| 传参 `f({a,b,c})` | 构造栈/静态临时数组 + 传 (ptr,len) | 无（仅临时数组） | 数组随完整表达式销毁 |
| range-for | 指针自增循环 | 无 | 仅在该表达式内安全 |
| `il.begin()` | `mov rax,[il]` | 无 | 返回的是**临时数组**地址 |
