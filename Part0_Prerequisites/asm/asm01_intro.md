# A1 汇编导论：为何 C++ 程序员要懂汇编 + 工具链

> 平台约定：x86-64 / System V AMD64 ABI；反汇编统一 Intel 语法。编译器 GCC 15.3.0。

## ① 我们真正要回答的问题 <span class="badge badge-std">标准</span>

1. 为什么 C++ 程序员——尤其是追求「零成本抽象」「性能可预测」的工业级开发者——必须能读一点汇编？
2. 编译器到底把我的 C++ 变成了什么？`inline` 真内联了吗？栈对象真的零成本吗？`constexpr` 在编译期算到了哪？
3. 有哪些免费、可复现的工具，能让我在任何一台机器上把「源码」和「机器码」对上号？

先给判断：**汇编不是用来手写业务的，是用来当「编译器行为的显微镜」的。** 你不需要会写一整份汇编程序，但必须看得懂编译器吐出来的那段——尤其是它和你「以为」的生成物不一致的时候。

## ② 为什么是汇编，而不是别的

现代 C++ 的很多命题，其唯一判据就在生成的机器码：

- **「`inline` 真的内联了吗？」** —— 只有看反汇编才知道；`inline` 只是给编译器的建议，编译器可忽略。
- **「虚函数调用为什么比普通调用慢？」** —— 反汇编里会多出一次通过 `vtable` 的间接跳转（`call qword ptr [rax+8]`）。
- **「栈对象为什么零成本？」** —— 因为构造函数若被优化掉，反汇编里可能连一条指令都没有。
- **「UB 为什么危险？」** —— 有符号溢出是 UB，编译器在 `-O2` 下可能直接把整段依赖该值的代码删掉（因为它「假设 UB 不发生」）。

> 立场：[经验] 读汇编的目标不是「复现编译器」，而是「验证你的性能假设」。每次你声称某段代码快/慢，理想情况下都能用一条反汇编证据支撑或推翻。

## ③ 工具链：四件你一定用得上的东西

### 3.1 编译器 + 反汇编器（本机环境）

```bash
# 编译器（GCC 15.3.0，MinGW-w64）
C:/Qt/Tools/mingw1530_64/bin/g++.exe -std=c++23

# 反汇编器（同一工具链）
C:/Qt/Tools/mingw1530_64/bin/objdump.exe
```

编译到目标文件、再反汇编是固定套路：

```bash
g++ -std=c++23 -O2 -c -o demo.o demo.cpp      # 只编译不链接
objdump -d -M intel demo.o                     # Intel 语法反汇编
```

`-M intel` 指定 Intel 语法（AT&T 语法默认，但 Intel 语法对 C++ 读者更直观：`mov eax, ecx` 而非 `mov %ecx, %eax`）。

### 3.2 编译的四阶段（与 C 完全一致）<span class="badge badge-std">标准</span>

```text
demo.cpp ──①预处理──▶ demo.i ──②编译──▶ demo.s(汇编文本) ──③汇编──▶ demo.o ──④链接──▶ demo.exe
             (宏展开/        (C++ → 汇编)      (汇编 → 机器码)      (合并库/重定位)
              头文件包含)
```

`objdump -d` 看的是第 ③ 步产物 `demo.o` 里的 `.text` 段（机器码 + 对应助记符）。

### 3.3 Compiler Explorer（godbolt.org）

在线工具，左边写 C++、右边实时显示 GCC/Clang/MSVC 的反汇编，还能并排对比优化级别。适合快速验证「这个写法会不会内联」「这个循环有没有向量化」。本篇所有结论你都可以在 Compiler Explorer 用同样代码复现。

## ④ 第一个真实例子：你写的 `+` 不一定生成 `add`

源文件 `asm/_demo/a1_add.cpp`：

```cpp
// a1_add.cpp — A1 导论示例
// 编译: g++ -std=c++23 -O2 -c -o a1_add.o a1_add.cpp
// 反汇编: objdump -d -M intel a1_add.o
int add(int a, int b) {
    return a + b;
}

int main() {
    volatile int x = add(2, 3);
    return x;
}
```

GCC 15.3.0 `-O2` 下的真实反汇编（`objdump -d -M intel a1_add.o`）：

```asm
0000000000000000 <_Z3addii>:
   0:   8d 04 11                lea    eax,[rcx+rdx*1]
   3:   c3                      ret
   ...
Disassembly of section .text.startup:
0000000000000000 <main>:
   0:   48 83 ec 38             sub    rsp,0x38
   4:   e8 00 00 00 00          call   9 <main+0x9>
   9:   c7 44 24 2c 05 00 00 00 mov    DWORD PTR [rsp+0x2c],0x5
  11:   8b 44 24 2c             mov    eax,DWORD PTR [rsp+0x2c]
  15:   48 83 c4 38             add    rsp,0x38
  19:   c3                      ret
```

读这段真实产物，得出三个会颠覆「直觉」的结论：

1. **`add` 函数没有生成 `add` 指令**。`a + b` 被编译成 `lea eax, [rcx+rdx*1]`——一条「取有效地址」指令顺手把两数相加装进 `eax`。`lea` 本意是算地址，但这里被当作「不碰标志位的加法」用（因为 `a+b` 不依赖进位标志）。[经验] 编译器的指令选择比「字面翻译」聪明。
2. **`add(2, 3)` 在 `main` 里被常量折叠成 `0x5`**（十进制 5）。函数甚至没被真正调用——`call` 那条是链接占位、`mov DWORD PTR [rsp+0x2c], 0x5` 直接写死结果。这正是「零成本抽象」的真相之一：能算清楚的，编译期就消灭了。
3. **参数不在栈上**。按本机 **Microsoft x64 调用约定**，`add` 的整数参数 `a`、`b` 分别在寄存器 `rcx`、`rdx`（前 4 整数参数走 `rcx, rdx, r8, r9`），返回值走 `eax`。栈帧只在 `main` 里因 `volatile` 落地才出现。

> 立场：[实现·GCC15.3] 以上为 GCC 15.3.0 `-O2` 实测。换 Clang 或 `-O0`，产物会不同（例如 `-O0` 下 `add` 会老老实实 `mov`+`add`+`ret`，且不内联）。本机为 Windows/MinGW，调用约定是 **Microsoft x64**（非 Linux 的 System V）；在 Linux 上同一函数参数会走 `rdi, rsi` 而非 `rcx, rdx`，反汇编据此不同。**任何汇编结论都绑定「编译器+版本+优化级别+平台」四元组，脱离这四元组谈汇编就是空谈。**

## ⑤ 本篇的方法论约定

- 所有汇编证据块一律标注「生成命令 + 编译器版本 + 优化级别」，可复现、可证伪。
- 不手写「示意」汇编；书里每一段 `asm` 都来自真机 `objdump`。
- 平台以 x86-64 / System V AMD64 ABI 为准；Windows（Microsoft x64）调用约定不同处单独注明。

## ⑥ 小结

读懂汇编，等于给「C++ 为什么这样设计」装了一台显微镜。下一章从最底层开始：x86-64 有哪些寄存器、内存怎么看、`mov`/`lea` 到底在搬什么。
