# C4 函数：调用约定、栈帧与变参 `stdarg`

> 参考：《C 语言极致详解手册》。编译器 GCC 15.3.0（`gcc -std=c11`），所有汇编为本机 `objdump -d -M intel` 真机产物。
> 示例源：`c/_demo/c4_funcs.c`

## ① 我们真正要回答的问题 <span class="badge badge-std">标准</span>

1. 调用 `f(a, b, c, d, e)` 时，5 个实参到底怎么送达？
2. 栈帧长什么样？为什么 `-O2` 下有些函数连帧都不建？
3. `printf("...", a, b, c)` 这种变参函数的魔法是怎么实现的？`va_arg` 到底做了什么？
4. 为什么变参函数是 C 里**最不安全**的角落？

真实运行输出：

```text
add5 = 15
sum  = 100
avg  = 2.33
fact = 3628800
```

## ② 调用约定回顾（Microsoft x64）

与 `asm/asm03_stack_abi.md` 一致，本章所有反汇编遵循的约定：

| 项 | Microsoft x64（本机） | System V AMD64（Linux/macOS） |
|----|----------------------|------------------------------|
| 整数/指针实参 | 前 4 个：`rcx, rdx, r8, r9` | 前 6 个：`rdi, rsi, rdx, rcx, r8, r9` |
| 浮点实参 | `xmm0-3`（**同时**复制进对应整型寄存器，变参函数尤其如此，见 ⑤⑥） | `xmm0-7`（整型/浮点**分道**，不复制） |
| 第 5+/7+ 个实参 | 从右往左压栈，紧邻 32B 影子空间之后 | 压栈 |
| 返回值 | `rax`（>8 字节结构体经隐藏指针） | `rax`/`xmm0`（大结构按 MEMORY 类处理） |
| 栈清理 | **调用者**清理（callee 不动栈参数） | 调用者清理 |
| 影子空间 | 有，32 字节，callee 可任意使用 | 无 |
| 栈对齐 | `call` 前 `rsp` 16 字节对齐 | 同（另要求 `call` 后 8 对齐进 callee） |

> 立场：[标准] C 标准只规定**语义**（实参求值顺序不定、按值传递、`return` 语义），**不规定寄存器分配**。以上全是 ABI 层事实；换平台换约定，同一份 C 代码的汇编完全不同。

## ③ 实参传递：前 4 个走寄存器，第 5 个开始走栈

源码：`int add5(int a, int b, int c, int d, int e)`。`-O0` 反汇编（真实产物）：

```text
0000000000000000 <add5>:
   0:	55                   	push   rbp
   1:	48 89 e5             	mov    rbp,rsp
   4:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx     ; a ← rcx
   7:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx     ; b ← rdx
   a:	44 89 45 20          	mov    DWORD PTR [rbp+0x20],r8d     ; c ← r8d
   e:	44 89 4d 28          	mov    DWORD PTR [rbp+0x28],r9d     ; d ← r9d
  12:	8b 55 10             	mov    edx,DWORD PTR [rbp+0x10]
  ...
  24:	8b 45 30             	mov    eax,DWORD PTR [rbp+0x30]     ; ★ e 在这里！
  27:	01 d0                	add    eax,edx
  29:	5d                   	pop    rbp
  2a:	c3                   	ret
```

关键在 `★`：`e` 不在寄存器里——它从 `[rbp+0x30]` 取。对照 C2 的影子空间图：

```text
rbp+0x08  返回地址
rbp+0x10  ┐
rbp+0x18  │ 32 字节影子空间
rbp+0x20  │ （调用者预留，恰好是 rcx/rdx/r8/r9 四个 home slot）
rbp+0x28  ┘
rbp+0x30  ★ 第 5 个栈传实参 e —— 紧贴影子空间之后
```

**调用点对称证据**（`-O0` 的 `main`，调用 `sum_all(4, 10, 20, 30, 40)`）：

```text
16f:	c7 44 24 20 28 00 00 00 	mov    DWORD PTR [rsp+0x20],0x28   ; 第5参 40 压栈
177:	41 b9 1e 00 00 00       	mov    r9d,0x1e                    ; 30
17d:	41 b8 14 00 00 00       	mov    r8d,0x14                    ; 20
183:	ba 0a 00 00 00          	mov    edx,0xa                     ; 10
188:	b9 04 00 00 00          	mov    ecx,0x4                     ; count
18d:	e8 99 fe ff ff          	call   2b <sum_all>
```

调用者把第 5 个实参 `40` 写到 `[rsp+0x20]`——正是影子空间结束后的第一个栈槽。

`-O2` 下 `add5` 被压成 5 条指令，**连帧都不建**（叶函数、参数全程驻留寄存器）：

```text
0000000000000000 <add5>:
   0:	01 d1                	add    ecx,edx
   2:	44 01 c1             	add    ecx,r8d
   5:	42 8d 04 09          	lea    eax,[rcx+r9*1]
   9:	03 44 24 28          	add    eax,DWORD PTR [rsp+0x28]   ; 第5参仍从栈上取
   d:	c3                   	ret
```

> 立场：[经验] 无论优化级别，**超出寄存器数量的实参永远走栈**——这是 ABI 契约，不是优化选择。这也解释了为什么「参数越少越好」不只是美学：第 5 个参数起，每次访问都是一次内存读。

## ④ 栈帧解剖：完整帧、递归链与「帧消失」

递归函数 `factorial` 的 `-O0` 全貌（真实产物）：

```text
00000000000000ff <factorial>:
  ff:	55                   	push   rbp              ; 保存上一层 rbp —— 栈帧链的「链环」
 100:	48 89 e5             	mov    rbp,rsp          ; 建立本层帧指针
 103:	48 83 ec 20          	sub    rsp,0x20         ; 本层局部空间（= 影子空间，给递归调用用）
 107:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx  ; n home
 10a:	83 7d 10 01          	cmp    DWORD PTR [rbp+0x10],0x1
 10e:	7e 13                	jle    123 <factorial+0x24>      ; n <= 1 → 基例
 110:	8b 45 10             	mov    eax,DWORD PTR [rbp+0x10]
 113:	83 e8 01             	sub    eax,0x1
 116:	89 c1                	mov    ecx,eax
 118:	e8 e2 ff ff ff       	call   ff <factorial>            ; ★ 自递归：每层一个新帧
 11d:	0f af 45 10          	imul   eax,DWORD PTR [rbp+0x10]  ; 回乘 n
 121:	eb 05                	jmp    128
 123:	b8 01 00 00 00       	mov    eax,0x1                   ; 基例返回 1
 128:	48 83 c4 20          	add    rsp,0x20
 12c:	5d                   	pop    rbp                       ; 弹回上一层 rbp —— 链条回缩
 12d:	c3                   	ret
```

`push rbp` / `pop rbp` 就是「栈帧链」的成环与解环：递归 10 层，就有 10 组这样的帧排在栈上——这也是**栈溢出（stack overflow）的物理形态**（C5 详述）。

而 `-O2` 下，`static` 的 `factorial` 被**整体内联进 `main` 并改写成循环**——独立符号直接消失：

```text
; main（-O2，.text.startup 段）尾部：
  97:	ba 01 00 00 00       	mov    edx,0x1          ; 累积器 = 1
  9c:	b8 0a 00 00 00       	mov    eax,0xa          ; i = 10
  b0:	0f af d0             	imul   edx,eax          ; acc *= i
  b3:	83 e8 01             	sub    eax,0x1          ; --i
  b6:	83 f8 01             	cmp    eax,0x1
  b9:	75 f5                	jne    b0               ; 循环到 i==2
```

没有 `call`、没有帧、没有递归——「递归」只是源码语义，机器看到的是循环。这也是「编译器能把尾递归/简单递归改写成迭代」的实锤（C++ 主书 ch117 的 RVO/拷贝消除是同一族优化）。

## ⑤ 变参 `stdarg`：寄存器保存区与 8 字节步长

`sum_all(int count, ...)` 的 `-O0` 全貌：

```text
000000000000002b <sum_all>:
  2b:	55                   	push   rbp
  2c:	48 89 e5             	mov    rbp,rsp
  2f:	48 83 ec 10          	sub    rsp,0x10
  33:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx   ; count home
  36:	48 89 55 18          	mov    QWORD PTR [rbp+0x18],rdx   ; ┐
  3a:	4c 89 45 20          	mov    QWORD PTR [rbp+0x20],r8    ; │ 变参寄存器保存区：
  3e:	4c 89 4d 28          	mov    QWORD PTR [rbp+0x28],r9    ; ┘ 把 3 个变参 home 进影子空间
  42:	48 8d 45 18          	lea    rax,[rbp+0x18]             ; va_start：ap = 首个变参的地址
  46:	48 89 45 f0          	mov    QWORD PTR [rbp-0x10],rax   ;   （局部变量 ap）
  5a:	48 8b 45 f0          	mov    rax,QWORD PTR [rbp-0x10]   ; ┐ va_arg：
  5e:	48 8d 50 08          	lea    rdx,[rax+0x8]              ; │   ap += 8（槽位大小）
  62:	48 89 55 f0          	mov    QWORD PTR [rbp-0x10],rdx   ; │
  66:	8b 00                	mov    eax,DWORD PTR [rax]        ; ┘   取 4 字节 int
```

三个结论：

1. **`va_start` 只是一条 `lea`**——把指针指到「第一个变参的 home 槽」。没有魔法，变参区在内存里是**连续**的。
2. **`va_arg(int)` 读 4 字节、推进 8 字节**——无论实参实际多宽，槽位大小恒为 8（对齐与布局由 ABI 定死）。
3. `-O2` 下同样成立（保存区被显式搬到栈上）：

```text
; sum_all（-O2）序幕：
  10:	48 83 ec 18          	sub    rsp,0x18
  14:	48 8d 44 24 28       	lea    rax,[rsp+0x28]             ; 保存区起点
  19:	48 89 54 24 28       	mov    QWORD PTR [rsp+0x28],rdx   ; rdx home
  1e:	4c 89 44 24 30       	mov    QWORD PTR [rsp+0x30],r8    ; r8  home
  23:	4c 89 4c 24 38       	mov    QWORD PTR [rsp+0x38],r9    ; r9  home
  28:	48 89 44 24 08       	mov    QWORD PTR [rsp+0x8],rax    ; va_list
; 循环体：add edx,DWORD PTR [rax] ; add rax,0x8
```

> 立场：[标准] `va_list` 是实现定义类型（N1570 7.16）：Windows x64 上它就是一个 `char *`，`va_arg` 按类型宽度读、按 8 对齐推进；System V 上它是个结构体（含 GP/XMM 两个游标），`va_arg` 还要看 `al` 决定要不要翻寄存器保存区——**同一段变参代码，两边的 `va_list` 完全不是一回事**。这也是「不要对 `va_list` 做指针运算」的原因。

## ⑥ 默认实参提升：`float` 进变参会变 `double`

`avg_f(3, 1.5f, 2.5f, 3.0f)` 的调用点（`-O0`）：

```text
1c7:	48 b8 00 00 00 00 00 00 f8 3f 	movabs rax,0x3ff8000000000000  ; 1.5 的 double 位模式！
1d1:	66 0f 6e c0          	movq   xmm0,rax                  ; 同时送入 xmm0
1e8:	48 89 c2             	mov    rdx,rax                   ; ★ 又复制进 rdx（整型寄存器）
1eb:	b9 03 00 00 00       	mov    ecx,0x3
1f0:	e8 8b fe ff ff       	call   80 <avg_f>
```

两个关键事实：

1. **`1.5f` 在压栈前被提升为 `double`**（`0x3ff8000000000000`）——这是「默认实参提升」（N1570 6.5.2.2）：变参位置的 `float→double`、`char/short→int`。所以变参里**必须**用 `va_arg(ap, double)` 读 `float` 实参，用 `int` 读 `short` 实参，类型写错就是 UB。
2. **浮点实参被同时送进 XMM 与对应整型寄存器**（`★`）。原因：被调方无法预知「第几个变参是浮点」，于是 Windows x64 干脆把值**双通道投递**，callee 一律从整型保存区取。对照 System V：callee 靠 `al` 寄存器得知「来了几个 XMM 实参」，把 `xmm0-7` 存进保存区再取——**同一问题，两套相反的解法**。

## ⑦ 变参为什么是 C 最危险的角落

| 坑 | 后果 | 防线 |
|----|------|------|
| `va_arg` 类型与实参实际类型不符 | **UB**（读错位宽/解释） | 提升规则背熟：`float→double`、`char/short→int` |
| 实参个数与 `count` 不符 | 读到垃圾/越界 UB | 约定显式传个数（如本章 `count`），或用格式串（`printf`） |
| 裸 `printf(用户输入)` | 格式串注入 | `-Wformat`（GCC 对 `printf` 族有编译期格式检查） |
| `va_list` 指针运算 | 实现定义（SysV 是结构体） | 只用 `va_start/va_arg/va_end/va_copy` |

> 立场：[经验] `stdarg` 的本质是「**把类型系统的担子从编译器转嫁给约定**」：编译器只保证提升与传递，其余全靠格式串或计数约定。C++ 用**可变参模板**（主书 ch63）与 `fold expression`（ch64）把这件事重新类型安全化——代价是编译期而不是运行期。这也是「现代 C++ 不再手写 `...` 函数」的根本原因。

## ⑧ 小结与路线图

函数调用的全部秘密在 ABI：前 4 参寄存器、其余压栈、影子空间 32 字节、调用者清理。栈帧是「保存的 rbp 链」，`-O2` 能把帧拆掉、把递归摊平成循环。`stdarg` 没有魔法——`va_start` 是 `lea`，`va_arg` 是「读 4 字节、走 8 字节」；危险全在类型约定上。

下一章（C5）进入指针与内存：`malloc/free` 与进程内存布局——本章的「栈帧」正是 C5「栈区」的主角。

## 参考引用

- `[std-c11]`（N1570，本地 `docs/references/external/standards/N1570_C11.pdf`）：6.5.2.2 函数调用与默认实参提升、7.16 `<stdarg.h>`、6.2.5 类型。
- `[abi:msvc-x64]`：Microsoft x64 调用约定（寄存器传参、影子空间、调用者清栈、变参双通道投递）—— `learn.microsoft.com/cpp/build/x64-software-conventions`。
- 对照 `[abi:itanium]`：System V AMD64 ABI（6 个整型寄存器、XMM 计数 `al`、16 字节对齐）。
- 交叉引用：Part0 `asm/asm03_stack_abi.md`（调用约定与影子空间）、`c/c02_toolchain.md`（四阶段与反汇编方法）；主书 ch63（可变参模板）、ch64（fold expression）、ch117（RVO/拷贝消除）。
