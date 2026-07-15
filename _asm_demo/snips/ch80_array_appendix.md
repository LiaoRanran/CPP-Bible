## 附录：std::array 真机汇编实证（ASM-80-array · GCC 15.3.0 / C++26 / -O2）

> 证据：`_asm_demo/ch80_array_test.cpp` + `ch80_array_test.s`（真实编译 + `objdump -d -M intel -C`）。
> 工具链：`g++.exe (MinGW-W64 x86_64-msvcrt-posix-seh) 15.3.0`；`objdump.exe 2.46.1`。

**结论 1 — `std::array` 与裸数组逐字节同布局、同代码**
`sizeof(std::array<int,8>) == sizeof(int[8]) == 32`，且 `operator[]` 与裸指针下标生成**逐字节相同**的指令：

```asm
; access_by_index(const std::array<int,8>&, int)  —— operator[]
movsxd rdx, edx
mov    eax, DWORD PTR [rcx+rdx*4]   ; base + idx*4，单条 mov
ret
; access_raw(const int*, int)  —— 裸数组对照
movsxd rdx, edx
mov    eax, DWORD PTR [rcx+rdx*4]   ; 与上面完全相同
ret
```

→ `std::array` 没有隐藏指针或 size 成员，下标是零开销的编译期偏移计算，**不做运行时边界检查**。

**结论 2 — `at()` 有运行时边界检查，`operator[]` 没有**

```asm
; access_at(const std::array<int,8>&, int)  —— at()
sub    rsp,0x28
movsxd rdx, edx
cmp    rdx,0x7        ; idx 与 size-1(=7) 比较
ja     31 <...>       ; 越界 → 跳 .cold 调 __throw_out_of_range
mov    eax, DWORD PTR [rcx+rdx*4]
add    rsp,0x28
ret
```

→ 需要越界抛 `std::out_of_range` 时用 `at()`（付一次比较 + 可能的 throw 路径）；性能热路径用 `operator[]`。

**结论 3 — `data()` 退化为裸指针，按值传递整段拷贝**

```asm
; get_data : 直接返回首地址，零指令开销
mov    rax, rcx
ret
; by_value_copy(std::array<int,8>) : 按值传递拷贝全部 32 字节
movdqu xmm0, XMMWORD PTR [rdx]    ; 16B
mov    r8,    QWORD PTR [rdx+0x10]
mov    r9,    QWORD PTR [rdx+0x18] ; 16B
mov    rax, rcx
mov    QWORD PTR [rcx+0x10], r8
mov    QWORD PTR [rcx+0x18], r9
movups XMMWORD PTR [rcx], xmm0
ret
```

→ `data()` 与取地址等价；但 `std::array` **按值传递会逐元素整段复制**（N×sizeof(T)），不像裸数组会退化为指针——大数组传参优先用 `const&` 或 `std::span`。

| 操作 | 代码生成 | 边界检查 | 开销 |
|------|----------|:--------:|------|
| `a[i]`（operator[]） | `mov eax,[base+idx*4]` | 无 | 零 |
| `a.at(i)` | `cmp` + `ja` 至 throw 路径 | 有 | 1 次比较 + throw 风险 |
| `a.data()` | `mov rax,rcx` | 无 | 零 |
| 按值传参 | 整段 N×sizeof(T) 拷贝 | — | O(N) 内存搬运 |
