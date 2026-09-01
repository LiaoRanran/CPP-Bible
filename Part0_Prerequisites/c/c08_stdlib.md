# C8 标准库：函数不替你管边界

> 参考：《C 语言极致详解手册》。编译器 GCC 15.3.0（`gcc -std=c11`），所有输出为本机真实运行产物（MinGW x64，LLP64）。
> 示例源：`c/_demo/c08_stdlib.c`、`c/_demo/c08_assert.c`

## ① 我们真正要回答的问题 <span class="badge badge-std">标准</span>

1. 为什么 `strcpy(buf, src)` 是教科书里的「反面教材」？安全替代品到底是什么？
2. `strncpy` 不是「安全版 strcpy」——它哪里还会咬人？
3. 固定宽度整型 `int32_t` / `uint64_t` 为什么比 `int` / `long` 靠谱（接 C6）？
4. `assert` 到底是什么，为什么生产环境里它「神秘消失」？

> 判决先行：**C 标准库函数「按调用者负责边界」设计——它不替你检查目标够不够大、不保证一定写终止符、不替你处理重叠。** 所谓安全，是你把对的参数传进去；否则它静默越界、静默截断、或制造未定义行为。这和第 ⑥ 章「宏不检查类型」是同一种哲学：**信任程序员，代价自负。**

> 历史注脚：C 标准库（libc，glibc / msvcrt / musl）是 C 程序与操作系统之间的薄层（手册 522 的分层图：`用户代码 → 标准库 → 系统调用`）。K&R 把 I/O、字符串、内存管理收敛进 `<stdio.h>/<string.h>/<stdlib.h>`，C89 把它标准化。`malloc`（C5）、`qsort`（本章）、`assert`（本章）都出自这一层。

## ② 证据一：固定宽度整型（接 C6 的 LLP64）

```text
sizeof int32_t=4 uint64_t=8 intptr_t=8
```

`int32_t`/`uint64_t`（`<stdint.h>`）的宽度由标准**钉死**，跨平台不变；`intptr_t` = 能装下指针的整数（本机 x64 = 8 字节）。对比 C6：本机 `long` 只有 4 字节（LLP64），所以用 `long` 当「64 位容器」在 Linux 上能装、在 Windows 上溢出。**跨平台数据一律用 `<stdint.h>` 的固定宽度类型 + `intptr_t` 装指针。**

## ③ 证据二：`strncpy` 不补 `\0` 的坑

真机：把 5 字符 `"hello"` 拷进 `char b2[5]`（恰好 5 字节，无空间放终止符）：

```text
c08_stdlib.c:24:5: warning: 'strncpy' output truncated before terminating nul
                       copying 5 bytes from a string of the same length [-Wstringop-truncation]
strncpy("hello",5)->b2[5] 逐字节: hello  (无 \0 -> %s 会越界读到内存里下一个 \0)
```

`strncpy` 只保证「最多拷 n 字节」，**不会补终止符**。结果 `b2` 不是合法 C 字符串，随后 `printf("%s", b2)` 会一直读到内存里下一个 `\0` 才停——经典越界读（未定义行为）。**安全写法**：`snprintf(b2, sizeof b2, "%s", src)` 或手写补 `\0`。

## ④ 证据三：`snprintf` 返回「本应写入的长度」

```text
c08_stdlib.c:19:13: warning: 'snprintf' output 12 bytes into a destination of size 8 [-Wformat-truncation=]
snprintf("hello world"->buf[8]) 返回=11 实际写入="hello w"
```

`snprintf` 把 `"hello world"`（11 字符 + `\0` = 12 字节）截进 `buf[8]`：**实际只写 `"hello w\0"`（8 字节），返回 11**（= 若不限长度本应写出的字符数，含 `\0` 前的 11 个可见字符）。**返回值是你判断「是否被截断」的依据**——`if (n >= sizeof buf) /* 截断了，需扩容 */`。它比 `strncpy` 安全，但「返回 11 ≠ 实际写入 8」这个反直觉点常被人误用。

## ⑤ 证据四：`qsort` 用 `void*` + 函数指针做「泛型」

```text
qsort -> 1 2 5 5 6 9
```

`qsort(arr, 6, sizeof(int), cmp_int)`：比较函数通过 `void*` 接收元素、内部转回 `int*`。这是 C 没有模板/泛型时的标准手法（手册 1.3.3、1716）——代价是类型安全完全靠你自己，传错元素大小就未定义行为。

## ⑥ 证据五：`memmove` 能处理重叠，`memcpy` 不能

```text
memmove 重叠后 m = 0 0 1 2 4 5
```

把 `m[0..2]` 重叠拷到 `m[1..3]`，`memmove` 先缓冲再写，结果正确。**`memcpy` 要求源目的不重叠**，重叠是未定义行为（它可能用快路径指令直接覆写源）。字符串/内存函数的「重叠」禁忌是 C 标准库的隐形雷区。

## ⑦ 事故现场：`assert` 在生产「消失」

`assert` 本身就是个宏（接 C7）。两份编译，一份默认、一份 `-DNDEBUG`：

```text
=== 无 NDEBUG（默认）===
Assertion failed: 1 == 2, file c08_assert.c, line 6
（进程中止，exit=3）

=== -DNDEBUG（发布编译）===
never reached
（断言整行被删除，程序照常跑，exit=0）
```

> 立场：[标准] `assert` 在 `NDEBUG` 宏被定义时**整个表达式从源码中消失**（6.5.3.4 / 7.2）。它查的是「内部不变式」——「到这儿 x 必不为 NULL」这种程序员自证；**不要拿它做运行时错误恢复**（用户输入非法、文件打不开）——那些情况断言被关掉后错误就被吞了。错误恢复用返回码/错误码，不变式检查才用 `assert`。
> 立场：[经验] 字符串/内存函数红线：`strcpy`→`snprintf`/`memcpy_s`（Annex K，可选）；`strncpy` 记得手动补 `\0`；`memcpy` 前先确认源目的不重叠否则换 `memmove`；所有目标缓冲区大小必须由调用者算清（CERT `STR35-C`、`STR31-C`）。

## ⑧ 小结与路线图

`<stdint.h>` 固定宽度跨平台靠谱；`strncpy` 不补 `\0`、`snprintf` 返回「应写长度」；`qsort` 靠 `void*`+函数指针泛型；`memmove` 处理重叠、`memcpy` 不；`assert` 在 `NDEBUG` 下整体消失，只查不变式不恢复错误。

下一章（C9）把 C 拉进 C++ 世界：为什么 C 写的函数 C++ 直接链接会「undefined reference」，以及 `extern "C"` 如何桥接两套名字。

## 参考引用

- `[std-c11]`（N1570，本地 `docs/references/external/standards/N1570_C11.pdf`）：7.19 通用工具（`<stdlib.h>`、`qsort`/`bsearch`）、7.21 字符串（`<string.h>`、`strcpy`/`strncpy`/`memcpy`/`memmove`/`snprintf`）、7.20 整数类型（`<stdint.h>`）、7.2 诊断（`assert`/`NDEBUG`）。
- `[cppref:c/string]`、`[cppref:c/error/assert]`（离线 cppreference）：各函数语义与注意事项。
- `[cert:STR35-C]` 不得把无界源数据拷进定长数组；`[cert:STR31-C]` 保证字符串以 `\0` 终止（在线源）。
- 交叉引用：C5（`malloc/free` 同属 `<stdlib.h>`）；C6（`<stdint.h>` 接 LLP64）；C9（互操作里标准库 ABI）；主书 ch40（C 字符串与 `<string>`）、ch44（分配器）。
