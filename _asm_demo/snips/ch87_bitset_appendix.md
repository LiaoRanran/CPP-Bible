## 附录：std::bitset 与 <bit> 工具真机汇编实证（ASM-87-bitset / ASM-87-bit · GCC 15.3.0 / C++26 / -O2）

> 证据：`_asm_demo/ch87_bitset_test.cpp`+`ch87_bitset_test.s`、`_asm_demo/ch87_bit_test.cpp`+`ch87_bit_test.s`（另含 `-mpopcnt` 变体 `ch87_bit_test_popcnt.s`）。
> 工具链：`g++.exe (MinGW-W64 x86_64-msvcrt-posix-seh) 15.3.0`；`objdump.exe 2.46.1`。

**结论 1 — `bitset<N>` 是底层字（word）的薄封装，操作为字级位指令**

```asm
; bitset_flip : 整字取反 = 单条 not
mov    rax, rcx
not    rax
ret
; bitset_set(i) : 边界检查 + word |= (1 << (i%32))
cmp    rdx, 0x3f           ; i < 64 边界检查
...
shr    r8, 0x5             ; 字索引 = i / 32
shl    eax, cl             ; 位掩码 = 1 << (i % 32)
or     DWORD PTR [rsp+r8*4+0x30], eax
; bitset_test(i) : 边界检查 + (word & mask) 置标志
cmp    rdx, 0x3f
...
and    eax, DWORD PTR [r8+r9*4]
setne  al
```

→ 无循环、无堆分配；`flip` 是 `not`，`set/test` 是移位+位运算（GCC 选 `shr/shl/and` 而非 `bt` 指令）。**注意 `test/set` 都带 `cmp i,0x3f` + 越界 throw 的 `.cold` 路径——`bitset` 的下标访问是有边界检查的**（与 `std::array::operator[]` 相反）。

**结论 2 — `bitset::count()` 默认是软件 popcount（低/高 32 位各调一次运行库）**

```asm
; bitset_count : 拆成低/高 32 位，各 call 一次 32 位 popcount 运行库（SWAR）
mov    ecx, DWORD PTR [rcx]
call   <popcount 32-bit helper>
mov    ecx, DWORD PTR [rsi+0x4]
call   <popcount 32-bit helper>
add    rax, rbx
```

**结论 3 — `std::popcount` 默认是软件 SWAR，加 `-mpopcnt` 才变硬件单指令（关键）**

```asm
; 默认 -O2（无 -mpopcnt）：std::popcount 走运行库 SWAR 算法
popcnt_u(unsigned):
    mov    ecx, ecx
    call   <popcount helper>     ; 软件循环，非硬件

; 加 -mpopcnt 后：单条硬件指令
popcnt_u(unsigned):
    xor    eax, eax
    popcnt eax, ecx              ; 硬件 popcnt
    ret
```

→ **popcount 并非"免费"**：在基线 x86-64（无 popcnt ISA）或没加 `-mpopcnt`/`-march=native` 时，GCC 生成软件位运算；只有显式开启 popcnt 才是一条指令。`bitset<64>::count()` 同理（按 32 位字调用运行库）。嵌入式/老目标要特别留意。

**结论 4 — `byteswap` / `bit_cast` / `has_single_bit` 零成本**

```asm
; std::byteswap : 单条 bswap
mov    eax, ecx
bswap  eax
ret
; std::bit_cast<float>(uint32_t) : 位不变，仅换类型视图 → 直接进浮点返回寄存器
movd   xmm0, ecx
ret
; std::has_single_bit : (x-1) < (x ^ (x-1)) 等价 (x & (x-1)) == 0
lea    eax, [rcx-0x1]
xor    ecx, eax
cmp    eax, ecx
setb   al
; —— 加 -mpopcnt 后甚至退化为 popcnt(x) == 1 ——
popcnt ecx, ecx
cmp    ecx, 0x1
sete   al
```

| 操作 | 默认 -O2 代码 | 加 -mpopcnt | 边界检查 |
|------|---------------|-------------|:--------:|
| `bitset.flip()` | `not` | `not` | 无 |
| `bitset.set(i)` | 移位+`or` | 同 | 有（`cmp i,0x3f`） |
| `bitset.count()` | 两次 32 位 popcount 运行库调用 | 同（按字） | 无 |
| `std::popcount(x)` | 32 位 popcount 运行库调用（SWAR） | `popcnt eax,ecx` 单指令 | — |
| `std::byteswap(x)` | `bswap` | `bswap` | — |
| `std::bit_cast<To>(x)` | `movd`（位直传） | 同 | — |
