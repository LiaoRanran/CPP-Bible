# C5 指针与内存：`malloc/free` 与进程内存布局

> 参考：《C 语言极致详解手册》。编译器 GCC 15.3.0（`gcc -std=c11`），所有输出为本机真实运行产物。
> 示例源：`c/_demo/c5_layout.c`、`c/_demo/c5_uaf.c`

## ① 我们真正要回答的问题 <span class="badge badge-std">标准</span>

1. 程序的内存到底长什么样？代码、全局变量、局部变量、`malloc` 的内存各在哪个区？
2. `malloc(64)` 拿到的真是 64 字节吗？`free` 之后那块内存去了哪？
3. 为什么悬垂指针是 C/C++ 三千年（误）历史里最难缠的 bug？

> 立场：[标准] C11 把存储期定为四种（N1570 6.2.4）：**automatic**（栈，作用域进出即生灭）、**static**（随程序一生）、**allocated**（`malloc/free` 自主管理）、**thread**（C11 起随线程）。指针的一切危险，都来自 allocated 这一种——它把「什么时候死」的决定权完全交给你。

## ② 进程内存布局：把五个区钉在地址上

真实输出（连跑两次，看什么变、什么不变）：

```text
=== RUN#1 ===                                === RUN#2 ===
code  main    = 00007ff712101760              code  main    = 00007ff712101760
code  printf  = 00007ff7121031a0              code  printf  = 00007ff7121031a0
data  g_init  = 00007ff71210a010              data  g_init  = 00007ff71210a010
data  s_init  = 00007ff71210a014              data  s_init  = 00007ff71210a014
bss   g_zero  = 00007ff71210f080              bss   g_zero  = 00007ff71210f080
bss   s_zero  = 00007ff71210f084              bss   s_zero  = 00007ff71210f084
heap  #1      = 00000270c9368a60              heap  #1      = 000001523c5c8a60
heap  #2      = 00000270c9368ab0              heap  #2      = 000001523c5c8ab0
heap  gap     = 80 bytes                      heap  gap     = 80 bytes
stack &local  = 000000fac15ffa9c              stack &local  = 00000023de9ff8ac
```

| 区 | 内容 | 地址关系（本机 x86-64） |
|----|------|------------------------|
| code（`.text`） | 函数机器码 | 最低；两次运行**相同** |
| data（`.data`） | 已初始化全局/静态（`g_init`、`s_init`） | 紧随其后；相同 |
| bss（`.bss`） | 零初始化全局/静态（`g_zero`、`s_zero`） | 相同（不占 exe 空间，见 C2） |
| heap | `malloc` 的领地 | **每次运行不同** |
| stack | 局部变量/栈帧（C4 的主角） | 最高位；**每次运行不同** |

两个值得记住的观测：

- **堆与栈相向生长**：heap 在 `0x000002xx…` 一带，stack 在 `0x000000fa…` 一带，中间隔着巨大的空隙——这正是「栈向下长、堆向上长、撞上了就是内存耗尽」的物理图景。
- **为什么镜像地址两次相同？** 用 `objdump -p` 查 PE 头，本机可执行文件带 `DYNAMIC_BASE`（ASLR）、`HIGH_ENTROPY_VA`、`NX_COMPAT` 三个标志。Windows 对**镜像基址**的随机化是每次开机进行一次（同一次开机里重跑不变），而**堆/栈**是每个进程各随机一次——所以堆栈地址每次都换，镜像地址不变。

> 立场：[经验] ASLR 是安全机制，不是调试便利。它让「crash 地址」在两次运行间不可比——排崩溃时真正的锚点是**相对偏移**（模块内偏移、栈帧序号），不是绝对地址。

## ③ `malloc` 的账本：你要 64，它给 80

看 `heap gap = 80`：相邻两次 `malloc(64)` 与 `malloc(16)` 的指针差是 **80 字节**，不是 64——每个用户块前面藏着**分配器元数据**（块大小、空闲链表指针、对齐填充）。这块账本对你是不可见的，但它占着真实的内存，而且**就住在块的隔壁**。

> 立场：[标准] `malloc` 返回 `void *`，C 里可以隐式转成任意对象指针（N1570 6.3.2.3）；**C++ 里必须显式 cast**——这是 C/C++ 互操作最日常的一条差异（C9 详述）。`malloc(0)` 的返回值标准允许为 `NULL` 或「可安全 free 的唯一指针」；`free(NULL)` 永远安全无事发生；`free` 一个不是 `malloc` 给的指针（栈地址、块中间地址、已 free 的地址）是 UB。
> 对应的 CERT 铁律：`[cert:MEM34-C]`（只 free 动态分配的内存）、`[cert:MEM31-C]`（不再用就 free）。

> 立场：[经验] C++ 世界后来给这个问题造了一整套替代品：构造/析构与 `new/delete`（主书 ch37）、RAII（ch39）、智能指针（ch41）、分配器与内存池（ch38/ch44）。C 的 `malloc/free` 是这一切的**地基**——所以 stdlib4 那句"allocator is the most underestimated interface"在这层就能看懂雏形。

## ④ 事故现场：一次 use-after-free 的完整尸检

> 本节故意制造 UB 并运行之。**生产代码禁止模仿**——`[cert:MEM30-C]`：不得访问已释放的内存。

先看编译器说了什么（GCC 15.3，`-Wall -Wextra`，未开任何 sanitizer）：

```text
c5_uaf.c:29:5: warning: pointer 'p' used after 'free' [-Wuse-after-free]
c5_uaf.c:25:5: warning: pointer 'p' used after 'free' [-Wuse-after-free]
c5_uaf.c:21:5: warning: pointer 'p' used after 'free' [-Wuse-after-free]
```

三处全部被抓——**但请注意它抓的是"字面可见"的悬垂**：如果 `p` 经过函数传参、存进结构体再回来用，静态分析就哑了。警告是岗哨，不是城墙。

然后是真实运行（`fflush` 强刷后）：

```text
before free : p[0..3] = 0 10 20 30
after  free : p[0] = 1216750192（UB：可能原值/被改/崩）
new alloc   : q = 0000020848868a60, p = 0000020848868a60（同址即悬垂炸弹）
```

逐条尸检：

1. `*p` 读回 `1216750192`（`0x4886_2270`）——不是你的 `0`，而是一个**堆地址样式的值**：`free` 后分配器立刻改写了释放块的头几字节，放进去的是它自己的内部记账（空闲链指针/哨兵，实现而定）。所谓"读悬垂指针"不是读旧值，是**把分配器的账本当自己的数据读**。它与新分配地址 `q`（`0x4886_8A60`）同处一段堆区——记账指针具体指向哪由分配器内部结构决定，不必深究；要点只有一个：**旧值没了，这块内存已归账本所有**。
2. `q == p`，逐字节相同：刚 free 的块立刻被 `malloc` 重新发牌。此刻 `p` 和 `q` 指向**同一块活内存**——往 `q` 写的数据会"神秘地"变成 `p` 读到的数据，反之亦然。生产里这类 bug 的表现是「两个八竿子打不着的变量互相污染」，这才是它恶名远扬的原因。
3. 接着 `free(q); free(p);`——double free。进程当场被处决：退出码 `-1073740940` = `0xC0000374`（STATUS_HEAP_CORRUPTION），最后一行 `survived…` **没有机会打印**。
4. 顺带一个工程教训：第一次运行没加 `fflush` 时，**连 "before free" 都没打出来**——stdout 在管道下是全缓冲的，进程异常终止时缓冲区直接蒸发。诊断崩溃时，日志没出现 ≠ 代码没执行；先怀疑缓冲，再怀疑逻辑。

> 历史注脚：C. A. R. Hoare 在 QCon 2009 自称 1965 年为 ALGOL W 引入空引用是「**十亿美元的错误**」（`qcon:2009-hoare-null`）——悬垂/空指针这一族问题的代价，四十年后由发明者亲口盖章。C++ 的答案一路从引用（ch20）、智能指针（ch41）排到 `optional`/`expected`（ch88）；C 的答案是纪律。

## ⑤ 栈：自动存储期与它的天花板

栈区在布局最高处、向下生长（C4 已见过栈帧链）。它的特点是**快而有限**：Windows 主线程默认栈保留大小约 1 MB（链接器可调），MinGW/MSVC 下递归过深直接触顶。C4 的 `factorial` 十层不痛不痒；把 `factorial(100000)` 递归上去就会见到经典的 stack overflow。

> 立场：[经验] 栈上的大数组（`char buf[1<<20]`）能编过也能跑，但每次调用都在栈上刻一块——**大缓冲去堆上要**（`malloc`/容器），栈留给「小而短命」的自动变量。这条直觉 C 和 C++ 通用（C++ 侧见主书 ch36）。

## ⑥ 防御清单

1. `free(p)` 后**立刻** `p = NULL`——把悬垂变成可安全重复 `free` 的空操作（`free(NULL)` 合法）。
2. 谁分配谁释放：封装成 `create/destroy` 对，禁止隔着模块偷 free。
3. 打开 `-Wall -Wextra`；能上 sanitizer 就上（Linux 上 `-fsanitize=address` 即刻现形；Windows/MinGW 的 ASan 支持看工具链版本，退路是 Application Verifier / Dr. Memory，工具链全景见 ch14）。
4. 走查口诀：**每一条 `malloc` 都要有唯一的 `free`，且都在同一层抽象里**。数不清配对就画所有权图——这正是 C++ RAII 要自动化的事（ch39）。
5. 大缓冲、生命周期跨函数的数据 → 堆；小而短命 → 栈。

## ⑦ 小结与路线图

进程内存五区：code/data/bss/heap/stack；`malloc` 的账本藏在块隔壁；悬垂指针的本质是「把分配器账本当数据读」；UB 不一定崩，但崩起来连日志都不给你留。

下一章（C6）讲结构体：字段怎么排、padding 从哪来、`#pragma pack` 动了谁的奶酪——A5 的汇编视角将在 C 语言层再走一遍。

## 参考引用

- `[std-c11]`（N1570，本地 `docs/references/external/standards/N1570_C11.pdf`）：6.2.4 存储期、6.3.2.3 `void *` 与指针转换、7.22.3 内存管理函数。
- `[cppref:c/memory/malloc]`（离线 cppreference）：`malloc/free` 语义与注意事项。
- `[cert:MEM30-C]` 不得访问已释放内存；`[cert:MEM31-C]` 不再用即 free；`[cert:MEM34-C]` 只 free 动态分配的内存（在线源）。
- `[qcon:2009-hoare-null]`：Hoare「Null References: The Billion Dollar Mistake」（人文源，见 `humanities_index.md`）。
- `[ritchie:chist]`：Ritchie《The Development of the C Language》——指针算术直接继承自 BCPL/B 的无类型字地址观（人文源）。
- 交叉引用：Part0 C2（`.bss` 不占 exe）、C4（栈帧）；主书 ch35（内存模型）、ch36（栈堆对比）、ch41（智能指针）、ch44（内存池）。
