# A5 数据结构在汇编层：数组寻址、结构体偏移与对齐

> 平台约定：x86-64 / Microsoft x64。反汇编 Intel 语法。编译器 GCC 15.3.0。**LLP64 数据模型**（`long` = 4 字节，见 §5）。

## ① 我们真正要回答的问题 <span class="badge badge-std">标准</span>

1. `arr[i]` 在机器上怎么变成地址？`i` 怎么和「元素大小」相乘？
2. 结构体的字段 `p->x`、`p->y` 在内存里隔多远？偏移是谁定的？
3. 为什么 `struct { char a; int b; }` 占 8 字节而不是 5 字节？padding 从哪来？

先给判断：**C++ 的对象内存布局，本质就是「字段偏移 + 对齐填充」。** 你写的每个 `struct`/`class`，编译器都按一套对齐规则把它拍平成一串带偏移的字节。读懂这一章，主书里「虚表指针在哪」「为什么 `sizeof` 比你算的大」「内存对齐如何影响 cache」才接得住。

## ② 数组：`[base + i * sizeof(T)]`

源 `asm/_demo/a5_layout.cpp` 的 `arr_at`：

```cpp
__attribute__((noinline)) long arr_at(const int* a, long i) { return a[i]; }
```

GCC 15.3.0 `-O2`：

```asm
0000000000000010 <_Z6arr_atPKil>:
  10:   48 63 d2             movsxd rdx,edx          ; i 符号扩展到 64 位
  13:   8b 04 91             mov    eax,DWORD PTR [rcx+rdx*4]   ; a[i] = *(a + i*4)
  16:   c3                   ret
```

`[rcx + rdx*4]` 正是 A2 的有效地址公式：`base(a)` + `i * 4`（`int` 占 4 字节，scale=4）。**下标不是魔法，就是一次「基址 + 索引×元素大小」的地址计算。** 多维数组、指针算术全部归约于此。

## ③ 结构体字段偏移

`Point { int x; int y; long id; }` 的真机尺寸（`offsetof` 实测，见下）：`x@0, y@4, id@8`。`manhattan` 的反汇编直接印证：

```asm
0000000000000000 <_Z9manhattanPK5Point>:
   0:   8b 01                mov    eax,DWORD PTR [rcx]      ; p->x  @ 偏移 0
   2:   03 41 04             add    eax,DWORD PTR [rcx+0x4]  ; p->y  @ 偏移 4
   5:   c3                   ret
```

`[rcx]` 取 `x`，`[rcx+0x4]` 取 `y`——偏移硬编码进指令。字段名在编译后**彻底消失**，只剩「结构体基址 + 常数偏移」。

## ④ 对齐与 padding：为什么 `char a; int b` 不是 5 字节

源 `asm/_demo/a5_sizes.cpp`（`offsetof` + `sizeof`，GCC 15.3.0 真机输出）：

```
sizeof(Point)=12   alignof(Point)=4
Point.x@0  y@4  id@8
sizeof(Padded)=12 alignof(Padded)=4
Padded.a@0  b@4  c@8
```

`Padded { char a; int b; short c; }` 的内存布局：

```text
偏移: 0    1    2    3    4    5    6    7    8    9    10   11
字节: [a ] [pad][pad][pad][  b (int,4B)  ][ c (short) ][pad][pad]
```

- `a`(char) 在 @0；
- `b`(int) 要求 **4 字节对齐**，编译器在 `a` 后填 3 字节 padding，把 `b` 顶到 @4；
- `c`(short) 要求 2 字节对齐，落在 @8；
- 结构体整体按最大成员对齐（4）向上取整 → `sizeof = 12`（不是 10，不是 5）。

> 立场：[实现·GCC15.3] padding 是「用空间换对齐访问速度」：未对齐的内存访问在部分架构上会触发总线错误（SIGBUS）或性能惩罚。`#pragma pack` / `alignas` 能改写规则（C6 详述），但跨 ABI 传递结构体时改对齐极易踩坑。

## ⑤ 关键题外话：Windows `long` 只有 4 字节（LLP64）

注意 `Point` 里的 `long id` 在本机只占 **4 字节**——`sizeof(Point)` 是 12 而非 16。原因是：

| 数据模型 | `int` | `long` | 指针 | 平台 |
|----------|-------|--------|------|------|
| **LLP64** | 4 | **4** | 8 | Windows（MinGW / MSVC） |
| LP64 | 4 | 8 | 8 | Linux / macOS x86-64 |

> 立场：[平台·x86-64] 本机 MinGW 是 **LLP64**，所以 `long`=4 字节。同样的 `struct Point` 在 Linux（LP64，`long`=8）下 `sizeof` 会是 **16**、`id@8` 后还有 4 字节尾填充。这是「为什么 Windows 和 Linux 不能混链同一 `.o`」的又一例证（与 A3 调用约定并列）。`int32_t`/`int64_t`（`<cstdint>`）才是跨平台稳定选择。**这条坑会在 C 章（类型）和 C9（互操作）反复出现。**

## ⑥ 小结

- `arr[i]` = `base + i * sizeof(T)`，编译成 `[reg + idx*scale]`。
- 结构体字段 = 基址 + 编译期常数偏移；字段名编译后消失。
- 对齐 padding 让 `sizeof` 常大于「字段字节和」；这是 C++ 对象模型与性能的地基。
- 平台数据模型（LLP64 vs LP64）直接改变 `long` 大小与结构体布局。

下一章收尾汇编篇：把 C++ 源码喂给编译器，看 `-O0` 与 `-O2` 的反汇编差多远，并亲手写一段内联汇编。
