# A2 x86-64 寄存器、内存视角与数据移动

> 平台约定：x86-64 / System V AMD64 ABI；反汇编 Intel 语法。编译器 GCC 15.3.0。

## ① 我们真正要回答的问题 <span class="badge badge-std">标准</span>

1. C++ 里的「变量」落到机器上到底存在哪——寄存器还是内存？
2. x86-64 有哪些寄存器可用？传参、返回值、栈指针各是谁？
3. `mov` 和 `lea` 有什么本质区别？为什么编译器爱用 `lea` 做加法？

先给判断：**寄存器是「最快的变量」，内存是「掉地上的变量」。** 编译器的最优策略永远是「能塞寄存器就别进内存」；你写的每一个局部变量，最终要么消失（被优化），要么待在寄存器，要么——最坏情况——落到栈。

## ② 通用寄存器全家福（System V AMD64 ABI）

64 位下有 16 个通用寄存器 `rax rbx rcx rdx rsi rdi rbp rsp r8–r15`。每个都可按宽度访问不同「窗口」：

| 64 位 | 低 32 | 低 16 | 低 8 | 角色（调用约定） |
|-------|-------|-------|------|------------------|
| `rax` | `eax` | `ax` | `al` | 整数返回值 |
| `rcx` | `ecx` | `cx` | `cl` | 第 1 整数参数（**Microsoft x64**） |
| `rdx` | `edx` | `dx` | `dl` | 第 2 整数参数 |
| `r8`  | `r8d`  | `r8w` | `r8b` | 第 3 整数参数 |
| `r9`  | `r9d`  | `r9w` | `r9b` | 第 4 整数参数 |
| `rsi`/`rdi`/`r10`/`r11` | `esi`… | — | — | 易失暂存（**不参与**整数传参） |
| `rbx` | `ebx` | `bx` | `bl` | 被调用者保存（callee-saved） |
| `rbp` | `ebp` | `bp` | `bpl` | 被调用者保存（通常作帧基址） |
| `rsp` | `esp` | `sp` | `spl` | 栈指针（永远指向栈顶） |
| `r12–r15` | `r12d…` | `r12w…` | `r12b…` | 被调用者保存 |

> 调用约定要点（**Microsoft x64，本机 MinGW 实测**）：[实现·GCC15.3] 前 4 个整数参数依次走 `rcx, rdx, r8, r9`；**第 5 个起全部压栈**（调用者还需预留 32 字节 shadow space 供被调用者溢出前 4 参数）；返回值走 `rax`。Linux/macOS 用 System V AMD64 ABI：前 6 个参数 `rdi, rsi, rdx, rcx, r8, r9`。**被调用者保存**寄存器（`rbx, rbp, r12–r15`）在被调用函数改动前必须先压栈保全；易失寄存器（`rax, rcx, rdx, r8–r11, rsi, rdi`）不用保全——这正是「为什么有些变量在函数调用后会丢」的底层原因。

## ③ 浮点与向量：`xmm0–xmm15`

标量浮点（`float`/`double`）与 SIMD 向量走 `xmm0–xmm15`（128 位）。前 8 个浮点参数走 `xmm0–xmm7`，浮点返回值走 `xmm0`。本书主书讲 `std::vector` 的自动向量化时，你会在反汇编里看到 `movdqu`、`addps` 这类操作 `xmm` 的指令。

## ④ 标志寄存器 `rflags`

`cmp` / `test` / 算术指令会改写 `rflags` 的位（零标志 ZF、符号 SF、进位 CF、溢出 OF）。条件跳转（`je`/`jg`/`jl`…）正是读这些标志位做决定的——见 A4。

## ⑤ 内存视角：有效地址公式

反汇编里所有内存操作都长这样：

```asm
mov  DWORD PTR [base + index*scale + displacement], eax
```

- `base`：基址寄存器（如 `rsp`、`rdi`）
- `index*scale`：变址 × 比例因子（scale ∈ {1,2,4,8}，对应 1/2/4/8 字节元素）
- `displacement`：编译期常数偏移（如结构体字段偏移、数组下标常数）

数组 `arr[i]`（每个 4 字节）在机器上就是 `[基址 + i*4]`；结构体字段 `s.field` 就是 `[结构体基址 + 字段偏移]`。这一公式贯穿 A5（数据结构）。

## ⑥ 真实示例：`mov` 与 `lea` 的分工

源 `asm/_demo/a2_move.cpp`：

```cpp
// 编译: g++ -std=c++23 -O2 -c -o a2_move.o a2_move.cpp
// 反汇编: objdump -d -M intel a2_move.o
long f(long a, long b, long* p) {
    long t = a + b;   // lea
    *p = t;           // mov store
    long q = *p + 1;  // mov load + add
    return q;
}
```

GCC 15.3.0 `-O2` 真实反汇编：

```asm
0000000000000000 <_Z1fllPl>:
   0:   8d 04 11                lea    eax,[rcx+rdx*1]   ; t = a + b
   3:   41 89 00                mov    DWORD PTR [r8],eax ; *p = t
   6:   83 c0 01                add    eax,0x1           ; q = (刚才的 t) + 1
   9:   c3                      ret
```

逐条读：

1. `lea eax,[rcx+rdx*1]`：`a`(`rcx`)+`b`(`rdx`) 用 `lea` 算进 `eax`（同 A1，加法不走 `add`）。
2. `mov DWORD PTR [r8],eax`：把 `t` 写进 `*p`（第 3 参数 `p` 在 `r8`）。这是一次**内存存储**。
3. `add eax,0x1`：`q = *p + 1`。注意——编译器**没有重新从内存读 `*p`**，而是直接对寄存器里的 `t` 加 1。这是基于别名分析（它证明 `p` 不会指向 `t`）的优化：省掉了一次内存加载。

> 立场：[实现·GCC15.3] 若把 `p` 改成可能指向 `t` 的指针（如传 `&t`），编译器就**必须**重新加载 `[r8]`——反汇编里会多出一条 `mov eax, DWORD PTR [r8]`。同一段源码，差一个别名假设，机器码就不同。这正是 C++ 别名规则（`restrict`、严格别名）影响性能的根。

再看 `lea` 算地址本职——源 `asm/_demo/a2_lea.cpp`：

```cpp
char* g(char* base, long i) {
    return base + i * 4 + 8;   // 期望 lea 算出有效地址
}
```

真实反汇编：

```asm
0000000000000000 <_Z1gPcl>:
   0:   c1 e2 02                shl    edx,0x2            ; i << 2  ⇒ i*4
   3:   48 63 d2                movsxd rdx,edx           ; 符号扩展回 64 位
   6:   48 8d 44 11 08          lea    rax,[rcx+rdx*1+0x8] ; base + (i*4) + 8
   b:   c3                      ret
```

`lea rax,[rcx+rdx*1+0x8]` 一次性算出 `base + i*4 + 8` 这个地址（不读内存、不写内存，只算指针），装进返回值 `rax`。这就是 `lea` 的本职：**算有效地址**。它被广泛借去当「不碰标志位的加法器」，但本质永远是「地址计算」。

## ⑦ 小结

- 变量默认进寄存器；寄存器不够或地址被取（`&x`）才落地内存。
- 传参走 `rdi…r9`，返回值走 `rax`，栈指针是 `rsp`。
- `mov` 搬数据（寄存器↔内存↔寄存器）；`lea` 算地址（常被借来当加法）。
- 所有内存访问都是 `基址 + 变址*比例 + 偏移`。

下一章把这些零件拼成「函数调用」：`main` 怎么跳进 `f`、参数怎么送进去、返回怎么出来、栈帧怎么开合。
