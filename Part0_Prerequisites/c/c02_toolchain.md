# C2 C 工具链：从 `.c` 到 `.exe` 的四个阶段

> 参考：《C 语言极致详解手册》。编译器 GCC 15.3.0（`gcc -std=c11`）。本章所有产物均为本机真机生成，命令与输出可完整复现。
> 示例源：`c/_demo/c2_toolchain.c`

## ① 我们真正要回答的问题 <span class="badge badge-std">标准</span>

1. `gcc hello.c -o hello` 这一行背后到底发生了什么？
2. 为什么要拆成「预处理 / 编译 / 汇编 / 链接」四步？拆开有什么用？
3. `.o` 目标文件里到底有什么？为什么它**不能直接运行**？
4. 怎么读 `.o`（`objdump`），从而把 C 源码和机器码一一对应上？

先给判断：**编译不是一个动作，而是一条流水线。** 拆开它，你才能第一时间判断「这个报错是预处理期、编译期还是链接期」，也才看得懂后面各章（尤其汇编部分）的证据从哪来。

## ② 四阶段总览

```text
   hello.c  （源文本）
      │
      │ ① 预处理 cpp：展开 #include / #define / #if，剥掉注释
      ▼
   hello.i  （纯 C 文本：无宏、无 #include）
      │
      │ ② 编译 cc1：词法/语法/语义分析 + 优化 → 生成汇编
      ▼
   hello.s  （汇编文本，人可读）
      │
      │ ③ 汇编 as：汇编 → 机器码，并按节区整理 + 生成符号表/重定位表
      ▼
   hello.o  （目标文件：可重定位，但还不能跑）
      │
      │ ④ 链接 ld：合并多个 .o + 解析库符号 + 修补重定位 + 接 CRT 启动代码
      ▼
   hello.exe（PE-x86-64 / ELF 可执行文件，可加载运行）
```

平时一条 `gcc hello.c -o hello` 会把四步**一次做完并删除中间文件**；想留下中间产物用 `-save-temps`。下面逐个阶段把它拆开看。

> 立场：[标准] 四阶段中的前三个（预处理、编译、翻译）在 C 标准里被规定为 **8 个翻译阶段**（N1570 5.1.1.2），其中第 4 阶段是预处理、第 7 阶段是编译；「汇编 + 链接」属于实现（工具链）而非标准语义，标准只要求「分别编译后可链接成可执行程序」。

## ③ 阶段 1：预处理（`-E` → `.i`）

预处理器**只做文本替换**：它不认识 C 语法，只认识 `#` 开头的行和宏。

```bash
gcc -std=c11 -E c2_toolchain.c -o c2.i
```

`c2.i` 的尾部（真实产物，`.i` 全文几百行，绝大部分是展开进来的 `stdio.h`）：

```c
# 16 "c2_toolchain.c"
static int counter = 0;
int g_value = 42;

int add(int a, int b) {
    return a + b;
}

int main(void) {
    int x = 5;
    int y = ((x) * (x));
    counter = counter + 1;
    printf("x=%d sq=%d add=%d counter=%d g=%d\n",
           x, y, add(x, y), counter, g_value);
    return 0;
}
```

三个必看细节：

- **`#include <stdio.h>` 消失了**——整份头文件的内容被原样插了进来（所以 `.i` 有几百行）。
- **`SQUARE(x)` 消失了**——源码里的 `SQUARE(x)` 被替换成 `((x) * (x))`。注意这是**纯文本替换**：宏不做类型检查、也不保证求值顺序，这正是 C7 要展开的宏陷阱根源（例如 `SQUARE(i++)` 会求值两次）。
- **行标记 `# 16 "c2_toolchain.c"`**——告诉编译器「下面这行来自源文件的第 16 行」，这样报错行号才对得上。

> 立场：[经验] 判断一个错误是不是预处理期错误，最简单的方法是加 `-E` 看 `.i`：如果期望的宏没展开，或者展开后语法就崩了，问题一定在预处理。

## ④ 阶段 2：编译（`-S` → `.s`）

这是「编译器」真正的本体：词法分析 → 语法分析 → 语义分析 → 优化 → 代码生成，产物是**汇编文本**。

```bash
gcc -std=c11 -O0 -S c2_toolchain.c -o c2.s
```

`.s` 里的 `add:` 就是后面第 ⑦ 节看到的机器码来源。这一阶段的产物仍是文本，人可读，是「C 代码 ↔ 机器码」对照的最佳中间态（汇编部分 A6 专门讲怎么读它）。

## ⑤ 阶段 3：汇编（`-c` → `.o`）

汇编器把 `.s` 变成机器码，并按**节区（section）**重新整理。

```bash
gcc -std=c11 -O0 -c c2_toolchain.c -o c2.o
objdump -h c2.o        # 查看节区表
```

真实输出：

```text
c2.o:     file format pe-x86-64

Sections:
Idx Name          Size      VMA               LMA               File off  Algn
  0 .text         00000090  0000000000000000  0000000000000000  0000012c  2**4
                  CONTENTS, ALLOC, LOAD, RELOC, READONLY, CODE
  1 .data         00000010  0000000000000000  0000000000000000  000001bc  2**4
                  CONTENTS, ALLOC, LOAD, DATA
  2 .bss          00000010  0000000000000000  0000000000000000  00000000  2**4
                  ALLOC
  3 .xdata        00000018  0000000000000000  0000000000000000  000001cc  2**2
                  CONTENTS, ALLOC, LOAD, READONLY, DATA
  4 .pdata        00000018  0000000000000000  0000000000000000  000001e4  2**2
                  CONTENTS, ALLOC, LOAD, RELOC, READONLY, DATA
  5 .rdata        00000030  0000000000000000  0000000000000000  000001fc  2**4
                  CONTENTS, ALLOC, LOAD, READONLY, DATA
  6 .rdata$zzz    00000050  0000000000000000  0000000000000000  0000022c  2**4
                  CONTENTS, ALLOC, LOAD, READONLY, DATA
```

| 节区 | 放什么 | 关键性质 |
|------|--------|----------|
| `.text` | 函数机器码（`add`、`main`） | `READONLY` + `CODE`，可执行 |
| `.data` | 已初始化的全局/静态（本例 `g_value = 42`） | **占文件空间**（File off 有值） |
| `.bss` | 未初始化或初值为 0 的全局/静态（本例 `static int counter = 0;`） | **`File off = 00000000`，不占磁盘空间**，加载时才分配并清零 |
| `.rdata` | 只读数据：`printf` 的格式字符串字面量 | `READONLY` |
| `.xdata` / `.pdata` | Windows 结构化异常处理（SEH）元数据 | **PE 格式特有**，Linux ELF 没有 |

> 立场：[标准] `.bss` 不占磁盘空间这件事有直接工程价值：**把大数组初始化为 0，不会让可执行文件变大**。`char buf[1024*1024];`（初值 0）进 `.bss`，文件尺寸不变；而 `char buf[1024*1024] = {1};` 进 `.data`，exe 立刻大 1 MB。标准不规定节区名字，但所有主流工具链都遵循这套约定。

> 立场：[经验] 注意首行 `file format pe-x86-64`——本机 MinGW 产出的是 **Windows PE 格式**，不是 Linux 的 `elf64-x86-64`。跨平台读 `objdump` 时，节区名大同小异，但 `.xdata`/`.pdata` 是 PE/SEH 独有；这也是 Part0 反复强调「本机调用约定是 Microsoft x64、数据模型是 LLP64」的又一个佐证。

## ⑥ 阶段 4：链接（`.o` + 库 → `.exe`）

`.o` 还**不能运行**——因为它引用的外部函数地址还是空的。看重定位表：

```bash
objdump -r c2.o
```

真实输出（节选）：

```text
RELOCATION RECORDS FOR [.text]:
000000000000007b IMAGE_REL_AMD64_REL32  __mingw_printf

RELOCATION RECORDS FOR [.pdata]:
0000000000000000 IMAGE_REL_AMD64_ADDR32NB  .text
0000000000000004 IMAGE_REL_AMD64_ADDR32NB  .text
0000000000000008 IMAGE_REL_AMD64_ADDR32NB  .xdata
```

`.text` 偏移 `0x7b` 处有一条 `IMAGE_REL_AMD64_REL32 __mingw_printf`——意思是：**这个位置的地址留空，等链接时填 `__mingw_printf` 的真实地址**。

链接器做的四件事：

1. 把多个 `.o` 的同名节区合并（`.text` 合并进 `.text`，`.data` 合并进 `.data`）；
2. **解析未定义符号**：`__mingw_printf` 在 C 运行库（msvcrt / MinGW 导入库）里找到；
3. **修补重定位**：把 `0x7b` 处留的空填成真实地址；
4. 接上 **CRT 启动代码**——`main` **不是程序真正的入口**，入口是 CRT 的 `mainCRTStartup`：它准备好 `argc`/`argv`、堆、`stdin`/`stdout`，然后才调用你的 `main`，`main` 返回后由它调用 `exit`。

```bash
gcc c2.o -o c2.exe
```

真实运行输出：

```text
x=5 sq=25 add=30 counter=1 g=42
```

> 立场：[经验] 注意 `printf` 在 `.o` 里变成了 **`__mingw_printf`**——这是 MinGW 为兼容性/格式检查做的重命名（实现细节，**不是标准**）。你在链接错误里看到带 `__mingw_` 前缀的符号，就知道这是工具链包装，不是你写错了。

## ⑦ 用 `objdump` 读 `.o`：把 C 和机器码对上

```bash
objdump -d -M intel c2.o
```

`add` 函数的真实反汇编（`-O0`）：

```text
0000000000000000 <add>:
   0:	55                   	push   rbp
   1:	48 89 e5             	mov    rbp,rsp
   4:	89 4d 10             	mov    DWORD PTR [rbp+0x10],ecx
   7:	89 55 18             	mov    DWORD PTR [rbp+0x18],edx
   a:	8b 55 10             	mov    edx,DWORD PTR [rbp+0x10]
   d:	8b 45 18             	mov    eax,DWORD PTR [rbp+0x18]
  10:	01 d0                	add    eax,edx
  12:	5d                   	pop    rbp
  13:	c3                   	ret
```

逐条对应到 `int add(int a, int b) { return a + b; }`：

| 汇编 | 含义 |
|------|------|
| `push rbp` / `mov rbp,rsp` | 建立栈帧（`-O0` 未优化，规规矩矩建帧；`-O2` 下很可能消失） |
| `mov [rbp+0x10],ecx` | 第 1 个参数 `a` 从 **`ecx`** 取 |
| `mov [rbp+0x18],edx` | 第 2 个参数 `b` 从 **`edx`** 取 |
| `add eax,edx` | 相加，结果放 **`eax`**（返回值寄存器） |
| `pop rbp` / `ret` | 撤栈帧并返回 |

**这是 Microsoft x64 调用约定的活标本**（与 `asm/asm03_stack_abi.md` 完全一致）：

- 前 4 个整数参数走寄存器 `rcx, rdx, r8, r9`；返回值走 `rax`。
- `-O0` 下编译器把寄存器参数「spill」回栈上，落点 `[rbp+0x10]`、`[rbp+0x18]` 不是随便选的：`rbp+0x8` 是返回地址，`rbp+0x10` 起就是调用者预留的 **32 字节影子空间（shadow space）** 的头两个 home slot。换句话说，**你在汇编里看到的这两个槽位，就是影子空间本身**。
- 对照 Linux/macOS 的 **System V AMD64 ABI**：前 6 个参数走 `rdi, rsi, rdx, rcx, r8, r9`，且**没有影子空间**。同一份 C 代码在两边的汇编不一样——这就是「跨平台读汇编」最常踩的坑。

## ⑧ 命令速查

| 目的 | 命令 |
|------|------|
| 只预处理 | `gcc -std=c11 -E a.c -o a.i` |
| 只编译到汇编 | `gcc -std=c11 -O0 -S a.c -o a.s` |
| 只汇编到目标文件 | `gcc -std=c11 -O0 -c a.c -o a.o` |
| 链接 | `gcc a.o -o a.exe` |
| 保留全部中间产物 | `gcc -save-temps a.c -o a.exe` |
| 看节区表（含 `.bss` 是否占空间） | `objdump -h a.o` |
| 反汇编（Intel 语法） | `objdump -d -M intel a.o` |
| 看重定位项（未解析符号） | `objdump -r a.o` |
| 看符号表 | `objdump -t a.o`（或 `nm a.o`） |

## ⑨ 报错属于哪个阶段（查错路线图）

| 现象 | 阶段 | 第一反应 |
|------|------|----------|
| `fatal error: xxx.h: No such file or directory` | **预处理** | 头文件路径/`-I` 没给对 |
| `error: expected ';' before ...` | **编译** | 语法/类型错误，看 `.i` 确认宏是否如预期展开 |
| `warning: implicit declaration of function 'foo'` | **编译** | C99 起必须声明，补 `#include` 或原型 |
| `undefined reference to 'foo'` | **链接**（最常被误判成编译错！） | 声明有了但**定义没给**：漏了源文件/库，或忘了 `-lm` 之类 |
| 能编译能链接，但运行崩溃或结果不对 | **运行期** | 多半是未定义行为（越界、野指针、未初始化），见 C3/C5 |

## ⑩ 小结与路线图

工具链的四阶段不是考点，而是**定位问题的坐标**：预处理管文本、编译管语义、汇编管节区与机器码、链接管符号解析与地址修补。`.o` 是「半成品」——代码已变成机器码，但外部符号仍然悬空（重定位表就是这些悬空点的清单）。

下一章（C3）进入类型系统：整数提升、隐式转换、数组退化——这些「编译期就决定、但运行期才咬人」的规则，正好站在本章「编译 vs 运行」的分界线上。

## 参考引用

- `[std-c11]`（N1570，本地 `docs/references/external/standards/N1570_C11.pdf`）：5.1.1.2 翻译阶段、6.10 预处理指令、6.2.2 标识符的链接。
- `[gcc:options]`：GCC 编译驱动选项 `-E` / `-S` / `-c` / `-save-temps`（`https://gcc.gnu.org/onlinedocs/`）。
- `[gcc:mingw-w64]`：MinGW-w64 目标格式为 PE-x86-64、使用 SEH（`.xdata`/`.pdata`）、`printf` 被包装为 `__mingw_printf`。
- 交叉引用：Part0 `asm/asm03_stack_abi.md`（Microsoft x64 调用约定与 32 字节影子空间）、`asm/asm06_inline_and_opt.md`（`-O0` vs `-O2` 读编译器输出）。
