# A4 控制流：cmp/test、条件跳转与循环

> 平台约定：x86-64 / Microsoft x64。反汇编 Intel 语法。编译器 GCC 15.3.0。

## ① 我们真正要回答的问题 <span class="badge badge-std">标准</span>

1. C++ 的 `if` / `for` / `while` 落到机器上是什么？分支预测为什么重要？
2. `cmp` 和 `test` 到底在做什么？「条件跳转」读的是什么？
3. 为什么同一个循环，`-O0` 和 `-O2` 的反汇编天差地别？

先给判断：**高级语言的选择与重复，在机器上只是一组「比较标志位 + 跳来跳去」的指令。** 没有「if」，只有「如果上一次比较结果满足某条件，就跳」。理解这一点，你就能看懂编译器为循环做的所有手脚。

## ② 标志寄存器与 `cmp`/`test`

分支的前提是「比较结果」。x86 用 `rflags` 标志位记录上一条算术/比较指令的结果：

- `cmp A, B` 本质执行 `A - B`（**不写回结果**，只改标志位）。随后 `jl`(小于)/`jle`(≤)/`jg`(>)/`jge`(≥)/`je`(==)/`jne`(!=) 读这些标志位决定跳不跳。
- `test A, A` 做 `A & A`（同样只改标志），常用来判断「是否为 0 / 是否为负」：`test eax,eax; jz label` = 「若 eax==0 则跳」。

> 立场：[标准] 有符号比较用 `jl/jg`（看 SF≠OF），无符号用 `jb/ja`（看 CF）。混用是经典安全/正确性问题——一个本该无符号的比较写成有符号，溢出时分支方向就反了。

## ③ 真实示例一：数组累加循环

源 `asm/_demo/a4_flow.cpp`（`sum`，`-O0` 保留清晰结构）：

```cpp
// 编译: g++ -std=c++23 -O0 -c -o a4_flow.o a4_flow.cpp
// 反汇编: objdump -d -M intel a4_flow.o
__attribute__((noinline))
long sum(const long* a, long n) {
    long s = 0;
    for (long i = 0; i < n; ++i)
        s += a[i];
    return s;
}
```

GCC 15.3.0 `-O0`：

```asm
0000000000000000 <_Z3sumPKll>:
   f:   c7 45 fc 00 00 00 00  mov  DWORD PTR [rbp-0x4],0x0    ; s = 0
  16:   c7 45 f8 00 00 00 00  mov  DWORD PTR [rbp-0x8],0x0    ; i = 0
  1d:   eb 1d                jmp  3c <+0x3c>                  ; ① 先跳去判条件
  1f:   mov  eax,[rbp-0x8]                                 ; ② 循环体: i
  22:   cdqe                                                 ; 符号扩展到 64 位
  24:   lea  rdx,[rax*4+0x0]                                ; i*4（元素偏移）
  2c:   mov  rax,QWORD PTR [rbp+0x10]                       ; a 基址
  30:   add  rax,rdx                                        ; a + i*4
  33:   mov  eax,DWORD PTR [rax]                             ; 取 a[i]
  35:   add  DWORD PTR [rbp-0x4],eax                         ; s += a[i]
  38:   add  DWORD PTR [rbp-0x8],0x1                         ; i++
  3c:   mov  eax,[rbp-0x8]                                  ; ③ 条件: i
  3f:   cmp  eax,[rbp+0x18]                                 ; i 与 n 比较
  42:   7c db                jl   1f <+0x1f>                 ; 若 i<n 跳回循环体
  44:   mov  eax,[rbp-0x4]                                  ; ④ 返回 s
  47:   add  rsp,0x10
  4b:   pop  rbp
  4c:   c3  ret
```

读这张图，把「for 循环」拆成机器四件套：

1. **初始化**：`s=0`、`i=0`（两条 `mov`）。
2. **条件前置**：`jmp 3c` 先跳到条件判断——编译器把 `for` 翻译成「先判后做」的 do-while 形态。
3. **循环体**：`a[i]` 的寻址正是 A2 的公式 `[基址 + i*4]`（`lea rdx,[rax*4]` + `add rax,rdx`），`s += a[i]` 是 `add`。
4. **增量 + 条件**：`i++` 后 `cmp` 比较 `i` 与 `n`，`jl` 在 `i<n` 时跳回 `0x1f`。

> 立场：[经验] `jl` 是有符号「小于」。当 `n` 是无符号或极大时，此处该用 `jb`；C++ 里用 `size_t` 做循环变量能消除这类隐患（见 C3）。

## ④ 真实示例二：分支 `max2`

```cpp
__attribute__((noinline))
long max2(long x, long y) { return x > y ? x : y; }
```

GCC 15.3.0 `-O0`：

```asm
000000000000004d <_Z4max2ll>:
  57:   mov  eax,[rbp+0x10]        ; x
  5a:   cmp  eax,[rbp+0x18]        ; 比较 x 与 y
  5d:   7e 05                jle  64 <+0x17>   ; 若 x<=y 跳到 64
  5f:   mov  eax,[rbp+0x10]        ; 不选：返回 x  → eax
  62:   eb 03                jmp  67           ; 跳到收尾
  64:   mov  eax,[rbp+0x18]        ; 选中：返回 y  → eax
  67:   pop  rbp
  68:   c3  ret
```

`cmp` 后 `jle`（≤）决定走 `y` 还是 `x`。注意结果统一经 `eax` 返回——这正是 A3「返回值走 `rax`」的体现。`-O2` 下这个分支通常会被编译成 `cmp`+`cmovg`（条件传送），**没有跳转**，彻底规避分支预测失败的开销——这正是「为什么有时候 `cmov` 比 `if` 快」。

## ⑤ 分支预测：为什么 `if` 有隐藏成本

现代 CPU 是流水线的：取指、译码、执行、写回重叠进行。遇到 `jmp` 条件跳转，CPU **必须**猜一个方向才能不 stall。猜错（分支预测失败）就要丢弃已执行的后续指令、重填流水线——几十个周期的损失。

> 立场：[经验] 这就是为什么「数据有序时的分支」远快于「随机数据时的分支」：`std::sort` 的 comparator 若高度可预测，循环飞快；而 `if (rand() & 1)` 这类随机分支会让流水线反复排空。C++ 标准库算法、分支无关写法（`cmov`、查表、SIMD）都是在消灭这类惩罚。

## ⑥ 小结

- `if` = `cmp` + 条件跳转；`for` = 初始化 + 条件 + 体 + 增量，编译成 do-while 形态。
- 数组访问 `[base + i*scale]` 是控制流与寻址的交汇点。
- 分支有预测失败的真实成本；`-O2` 常用 `cmov` 消除它。

下一章把「数据」摆上台面：数组寻址与**结构体字段偏移、对齐 padding**——C++ 对象内存布局的全部秘密都在这里。
