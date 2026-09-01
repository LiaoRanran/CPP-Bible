# A3 栈帧与函数调用约定（Microsoft x64）

> 平台约定：x86-64 / **Microsoft x64 调用约定**（本机 MinGW GCC 15.3 实测）。反汇编 Intel 语法。

## ① 我们真正要回答的问题 <span class="badge badge-std">标准</span>

1. `main` 调用一个函数时，机器层面到底发生了什么？参数怎么送过去、返回怎么回来？
2. 「栈帧」是什么？`push rbp; mov rbp, rsp` 这套 prologue 在保护什么？
3. 参数超过寄存器容量时，多余的那几个去哪了？（这就是 C++ 调用约定 / ABI 的本质）

先给判断：**函数调用 = 一组被调用约定严格约定的寄存器与栈操作。** 编译器、链接器、操作系统都遵守同一套规则，否则 C++ 调 C、调系统 API 全都会崩。读懂这一章，你就读懂了「C++ 函数」在金属上的真身。

## ② Microsoft x64 调用约定规则（本机实测）

| 项目 | 规定 |
|------|------|
| 整数/指针参数 1–4 | `rcx, rdx, r8, r9` |
| 整数/指针参数 5+ | **压栈**（调用者分配，右到左） |
| 浮点参数 1–4 | `xmm0–xmm3` |
| 返回值 | 整数 `rax`；浮点 `xmm0` |
| shadow space | 调用者必须为被调用者预留 **32 字节**（供其溢出前 4 参数） |
| 被调用者保存 | `rbx, rbp, rsi, rdi, r12–r15`（改动前须压栈保全） |
| 易失（不用保全） | `rax, rcx, rdx, r8–r11, rsp` |

> 立场：[实现·GCC15.3] 上表为本机 Windows/MinGW 实测。Linux/macOS 用 **System V AMD64 ABI**：整数前 6 参数 `rdi, rsi, rdx, rcx, r8, r9`，无 shadow space。两者**二进制不兼容**——这正是 `extern "C"` 也不能跨平台混链同一 `.o` 的根因（详见 C9）。

## ③ 真实示例：8 参数函数调用（强制不内联）

源 `asm/_demo/a3_call.cpp`（用 `__attribute__((noinline))` 保留真实调用框，否则 `-O2` 会把它整个内联掉）：

```cpp
// 编译(保留调用框): g++ -std=c++23 -O0 -c -o a3_call.o a3_call.cpp
// 反汇编: objdump -d -M intel a3_call.o
__attribute__((noinline))
long compute(long a, long b, long c, long d, long e, long f, long g, long h) {
    long local = a + b + c + d + e + f + g + h;
    return local * 2;
}

int caller() {
    return (int)compute(1, 2, 3, 4, 5, 6, 7, 8);
}
```

GCC 15.3.0 `-O0` 真实反汇编：

```asm
0000000000000000 <_Z7computellllllll>:
   0:   55                      push   rbp              ; ① prologue
   1:   48 89 e5                mov    rbp,rsp
   4:   48 83 ec 10             sub    rsp,0x10
   8:   89 4d 10                mov    DWORD PTR [rbp+0x10],ecx   ; 溢出 a(rcx)
   b:   89 55 18                mov    DWORD PTR [rbp+0x18],edx   ; 溢出 b(rdx)
   e:   44 89 45 20             mov    DWORD PTR [rbp+0x20],r8d   ; 溢出 c(r8)
  12:   44 89 4d 28             mov    DWORD PTR [rbp+0x28],r9d   ; 溢出 d(r9)
  16:   8b 55 10                mov    edx,[rbp+0x10]    ; 读 a
  19:   8b 45 18                mov    eax,[rbp+0x18]    ; 读 b
  1c:   01 c2                   add    edx,eax
  1e:   8b 45 20                mov    eax,[rbp+0x20]    ; 读 c
  21:   01 c2                   add    edx,eax
  23:   8b 45 28                mov    eax,[rbp+0x28]    ; 读 d
  26:   01 c2                   add    edx,eax
  28:   8b 45 30                mov    eax,[rbp+0x30]    ; 读 e（栈上传入）
  2b:   01 c2                   add    edx,eax
  2d:   8b 45 38                mov    eax,[rbp+0x38]    ; 读 f
  30:   01 c2                   add    edx,eax
  32:   8b 45 40                mov    eax,[rbp+0x40]    ; 读 g
  35:   01 c2                   add    edx,eax
  37:   8b 45 48                mov    eax,[rbp+0x48]    ; 读 h
  3a:   01 d0                   add    eax,edx          ; 八数求和 -> eax
  3c:   89 45 fc                mov    DWORD PTR [rbp-0x4],eax  ; local
  3f:   8b 45 fc                mov    eax,[rbp-0x4]
  42:   01 c0                   add    eax,eax          ; local*2
  44:   48 83 c4 10             add    rsp,0x10         ; ② epilogue
  48:   5d                      pop    rbp
  49:   c3                      ret

000000000000004a <_Z6callerv>:
  4a:   55                      push   rbp
  4b:   48 89 e5                mov    rbp,rsp
  4e:   48 83 ec 40             sub    rsp,0x40         ; 0x20 shadow + 0x20(4栈参)
  52:   c7 44 24 38 08 00 00 00 mov    DWORD PTR [rsp+0x38],0x8  ; h(第8参)
  5a:   c7 44 24 30 07 00 00 00 mov    DWORD PTR [rsp+0x30],0x7  ; g(第7参)
  62:   c7 44 24 28 06 00 00 00 mov    DWORD PTR [rsp+0x28],0x6  ; f(第6参)
  6a:   c7 44 24 20 05 00 00 00 mov    DWORD PTR [rsp+0x20],0x5  ; e(第5参)
  72:   41 b9 04 00 00 00       mov    r9d,0x4          ; d=4
  78:   41 b8 03 00 00 00       mov    r8d,0x3          ; c=3
  7e:   ba 02 00 00 00          mov    edx,0x2          ; b=2
  83:   b9 01 00 00 00          mov    ecx,0x1          ; a=1
  88:   e8 73 ff ff ff          call   0 <_Z7computellllllll>
  8d:   48 83 c4 40             add    rsp,0x40         ; 清栈（含 shadow）
  91:   5d                      pop    rbp
  92:   c3                      ret
```

## ④ 逐条读这张图

### 4.1 调用者 `caller` 怎么送参

- 前 4 个参数 `1,2,3,4` 分别装进 `rcx, rdx, r8, r9`（对应 `a,b,c,d`）——**走寄存器，不碰栈**。
- 后 4 个参数 `5,6,7,8` 由调用者写到栈上：`[rsp+0x20]=5(e)`、`[rsp+0x28]=6(f)`、`[rsp+0x30]=7(g)`、`[rsp+0x38]=8(h)`。注意地址从低到高 = 参数 5→8，但**写入顺序是先写 8 再写 5**（右到左），这正是 cdecl/Microsoft 系列「参数从右向左入栈」的痕迹。
- `sub rsp,0x40`（64 字节）= 32 字节 shadow space + 32 字节容纳 4 个栈参数。调用者为被调用者预留空间，这是 Microsoft x64 的硬性规定。

### 4.2 被调用者 `compute` 的 prologue

```asm
push rbp          ; 保存调用者的帧基址
mov  rbp, rsp     ; 新帧基址 = 当前栈顶
sub  rsp, 0x10    ; 给局部变量 local 留 16 字节
```

`rbp` 在此作为「帧指针」：函数体内所有局部变量和参数都以 `[rbp+偏移]` 寻址，不受后续 `rsp` 变化影响。**代价**：每次调用多两条指令 + 占一个被调用者保存寄存器。所以 `-O2` 默认省略帧指针（`-fomit-frame-pointer`），用 `rsp` 直接寻址——调试时「栈回溯」会变难，这正是为什么 Release 版崩了难看栈。

### 4.3 参数去哪了

`compute` 先把 4 个寄存器参数**溢出**到自己的 shadow space（`[rbp+0x10..0x28]`），因为后面要用这些寄存器；`e,f,g,h` 则直接从调用者栈上传入的位置 `[rbp+0x30..0x48]` 读取。读完八个数、`add` 累加、`*2`，结果在 `eax`（将成返回值）。

### 4.4 epilogue 与返回

```asm
add  rsp, 0x10    ; 收回局部变量空间
pop  rbp          ; 恢复调用者帧基址
ret               ; 弹出返回地址，跳回 caller
```

`caller` 在 `call` 返回后 `add rsp,0x40` 把栈清理干净（包括 shadow space 和 4 个栈参数）——**调用者负责清理栈**，这是 Microsoft x64 与 cdecl 共有的「调用者清栈」模型（区别于 `stdcall` 的被调用者清栈）。

> 立场：[经验] 这一整套「谁放参数、谁清栈、谁保寄存器」就是 **ABI（应用二进制接口）**。C++ 的函数重载、`std::function`、虚函数——它们的机器形态都建立在这套约定之上。不懂 ABI，就不知道「为什么同一个 `compute` 在 Linux 和 Windows 上链接不兼容」。

## ⑤ 小结

- 调用 = 寄存器传参（≤4）+ 栈传参（>4）+ 固定 prologue/epilogue。
- 栈帧由 `rbp/rsp` 框定，局部变量在 `[rbp-偏移]`，参数在 `[rbp+偏移]`。
- shadow space 是 Microsoft x64 的特产；System V 没有。
- 清栈责任在调用者。

下一章看控制流：`if`/`for`/`while` 在机器上是什么——`cmp`/`test` 改写标志位，条件跳转读标志位决定走向。
