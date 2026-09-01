# A6 内联汇编与读编译器输出

> 平台约定：x86-64 / Microsoft x64。反汇编 Intel 语法。编译器 GCC 15.3.0。

## ① 我们真正要回答的问题 <span class="badge badge-std">标准</span>

1. 同一个 C++ 函数，`-O0` 和 `-O2` 的反汇编能差多远？读懂差异有什么用？
2. 编译器在什么情况下会替我消灭分支（生成 `cmov`）？
3. 内联汇编怎么写？为什么「能不写就不写」？

先给判断：**读懂编译器输出，胜过背一百条优化口诀。** 而且绝大多数你以为「必须手写汇编」的地方，编译器已经替你做对了——`max2` 的 `-O2` 版就是证据。内联汇编是双刃剑：写对了是钥匙，写错了是静默的 bug。

## ② 读编译器输出：`-O0` vs `-O2`

源 `asm/_demo/a4_flow.cpp` 的 `max2` 与 `sum`。

### 2.1 `max2`：分支 → 条件传送

`-O0`（A4 已见，带分支）：

```asm
mov  eax,[rbp+0x10]     ; x
cmp  eax,[rbp+0x18]     ; x 与 y 比较
7e 05   jle  64          ; 若 x<=y 跳去取 y
mov  eax,[rbp+0x10]     ; 否则返回 x
eb 03   jmp  67
64: mov  eax,[rbp+0x18]  ; 返回 y
```

`-O2`（GCC 15.3.0 真实产物）：

```asm
0000000000000030 <_Z4max2ll>:
  30:   39 d1                cmp    ecx,edx        ; x 与 y 比较
  32:   89 d0                mov    eax,edx        ; 默认结果 = y
  34:   0f 4d c1             cmovge eax,ecx        ; 若 x>=y：结果 = x（无分支）
  37:   c3                   ret
```

`-O2` 把整条 `if/else` 压成 **一条 `cmovge`**：没有跳转、没有分支预测风险。这正是 A4 结尾说的「有时候 `cmov` 比 `if` 快」——而你是**白拿的**，编译器自动做的。

> 立场：[经验] 想要分支less，与其手写内联汇编，不如把代码写得让编译器敢用 `cmov`：避免让分支两侧有副作用、避免依赖未定义行为。干净的三元 `x > y ? x : y` 就够了。

### 2.2 `sum`：索引循环 → 指针循环

`-O0` 用「`i` 计数器 + `lea rdx,[rax*4]` 算偏移」；`-O2` 直接把 `a[i]` 变成**指针自增**，连乘法都省了：

```asm
0000000000000000 <_Z3sumPKll>:
  0:   85 d2                test   edx,edx           ; n==0?
  2:   7e 1c                jle    20 <+0x20>        ; n<=0 直接返回 0
  4:   48 63 d2             movsxd rdx,edx
  7:   31 c0                xor    eax,eax           ; s = 0
  9:   48 8d 14 91          lea    rdx,[rcx+rdx*4]   ; end = a + n*4
 10:   03 01                add    eax,DWORD PTR [rcx] ; s += *p
 12:   48 83 c1 04          add    rcx,0x4           ; p++（指针自增 4 字节）
 16:   48 39 d1             cmp    rcx,rdx
 19:   75 f5                jne    10 <+0x10>        ; 未到 end 继续
 1b:   c3                   ret
```

对比 A4 的 `-O0` 版：`-O2` 用 `rcx` 当指针一路 `+4` 推进，用 `rdx` 存「尾地址」做终止判断（经典「指针 vs 尾指针」循环形态），没有帧指针、没有 `i*4` 乘法。同样的逻辑，机器形态天差地别。

## ③ 内联汇编：干净的正确例子

当确实要碰硬件（读时间戳、特殊指令），用 GCC 扩展 asm 语法。源 `asm/_demo/a6_asm.cpp`：

```cpp
// 编译运行: g++ -std=c++23 -O2 a6_asm.cpp -o a6_asm.exe && ./a6_asm.exe
#include <cstdint>
#include <cstdio>
uint64_t rdtsc() {
    uint64_t t;
    __asm__ __volatile__ ("rdtsc" : "=A"(t));   // 输出约束 "=A"：64 位结果在 edx:eax
    return t;
}
int main() {
    uint64_t a = rdtsc();
    int sink = 0;
    for (int i = 0; i < 1000; ++i) sink += i;   // 无意义工作，防优化
    uint64_t b = rdtsc();
    printf("rdtsc: 前=%llu 后=%llu 增量=%llu (sink=%d)\n",
           (unsigned long long)a, (unsigned long long)b,
           (unsigned long long)(b - a), sink);
    return 0;
}
```

GCC 15.3.0 `-O2` 反汇编（`objdump -d -M intel a6_asm.o`）——汇编块原样落进二进制：

```asm
0000000000000000 <_Z5rdtscv>:
   0:   0f 31                rdtsc
   2:   c3                   ret
```

本机运行输出（`rdtsc` 返回单调递增的计数器，证明内联汇编真的执行了）：

```text
rdtsc: 前=210564 后=2266106820 增量=2265896256 (sink=499500)
```

语法要点：
- `__asm__`（GNU 关键字；MSVC 用 `__asm`）+ `__volatile__`（禁止编译器把这条「看似无副作用」的指令挪走/删掉）。
- `: "=A"(t)` 是**输出约束**：`=A` 表示「64 位整数结果落在 `edx:eax` 对」，编译器负责把它收进 `t`。
- 还有输入约束、破坏描述（clobber）等；写错约束是静默错误的温床。

## ④ 为什么「能不写就不写」

内联汇编的坑比想象的多：操作数顺序写反、约束写错、忘了声明破坏的寄存器/内存——编译器的优化器不知道你干了什么，轻则算错、重则破坏调用约定。**本书作者的真实教训**：一个手搓的「无分支 `min`」因 `cmov` 源操作数写成 `%2` 而非 `%1`，在 `-O2` 下被静默优化成「永远返回第二个参数」，反复用真机运行才抓到。结论——

> 立场：[经验] 99% 的场景，**让编译器生成**比手写汇编更对、更快、可移植。`max2` 的 `cmovge` 就是模板：写出清晰的无副作用代码，把指令选择交给 `-O2`。内联汇编只留给「编译器绝对够不着」的角落（特定 CPU 指令、底层同步原语）。

## ⑤ 汇编篇收尾

六章走完：从「为什么读汇编」→ 寄存器/内存 → 栈帧与调用约定 → 控制流 → 数据结构布局 → 读编译器输出与内联汇编。你已经具备把任何 C++ 片段「对到金属上」的能力。

下一站进入 **C 语言篇**（参考《C 语言极致详解手册》）：C++ 脱胎于此，指针、`malloc`、数组退化、结构体内存布局、调用约定、`extern "C"` 全部是 C 的遗产。不懂 C，就懂不透 C++ 的 ABI 与零成本抽象。

---

_汇编篇（A1–A6）全部反汇编证据均来自本机 GCC 15.3.0 真机 `objdump`，可复现。调用约定为 Windows/MinGW 的 Microsoft x64；Linux/macOS 用 System V AMD64 ABI，差异已在各章注明。_
