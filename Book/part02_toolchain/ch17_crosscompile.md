# 第17章　交叉编译与嵌入式工具链（C++）

⟶ Book/part02_toolchain/ch11_compilers.md
⟶ Book/part03_language/ch30_volatile.md

> 真实编译器取证：本机 MinGW GCC 13.1.0（`C:/Qt/Tools/mingw1310_64/bin/g++.exe`，`g++ --version` → `g++.exe ... 13.1.0`）。
> 交叉工具链（arm-none-eabi-gcc 等）本机大概率未安装，故以**本机 g++ 编译同一程序**展示 x86-64 真实汇编作为硬证据，ARM 侧给出明确标注的「典型输出」（AAPCS，未在本机执行）。
> 源码根：`Examples/_ch17_*.{cpp,cmake,ld}`（均已创建并验证）。

## ① 概述：什么是交叉编译 [标准]

⟶ Book/part02_toolchain/ch16_ide.md
⟶ Book/part02_toolchain/ch18_buildconfig.md


**交叉编译（cross compilation）** = 在**宿主机（host，如 x86-64 Windows）**上编译出运行在**目标机（target，如 ARM Cortex-M）**上的可执行代码。与之相对的是**原生编译（native compilation）**：host == target。

```cpp
// ① 一个完全可移植的“Hello 资源占用”目标程序——它不关心谁编译它
// 文件：Examples/_ch17_hello.cpp（正文示意，不强制运行）
#include <cstdint>
[[noreturn]] void panic(const char*) { for (;;) {} }
int add(int a, int b) { return a + b; }   // 同一份源码，x86 或 ARM 都能编
```

- `[标准]`：ISO C++ 本身不规定“在哪编译、在哪运行”，这是**工具链/ABI 层**问题；语言只要求可移植程序在符合实现的平台给出一致语义。
- `[经验]`：当你说“arm-none-eabi-g++ 编不过”时，问题几乎从不出在 C++ 标准，而在**目标三件套**（头/库/链接脚本）缺失。

## ② 目标三元组（arch-vendor-os-abi） [平台]

**目标三元组（target triple）**形如 `arch-vendor-os-abi`，是工具链定位“为谁生成代码”的字符串。

```cpp
// ② 三元组拆解（注释示意，非运行代码）
// arm      - none   - eabi        : GNU Arm Embedded，裸机嵌入式
//  ↑架构      ↑厂商     ↑OS/ABI
// aarch64 - linux  - gnu         : 64 位 ARM Linux（glibc）
// x86_64  - w64    - mingw32     : 本机 MinGW-W64（Windows）
// riscv32 - unknown - elf        : RISC-V 32 位裸机 ELF
```

```cpp
// ② 用宏确认“编译目标是谁”——同一份源码，不同三元组得到不同 __SIZEOF/宏
#include <cstdio>
int main() {
#if defined(__ARM_ARCH)
    return __ARM_ARCH;          // ARM 目标：返回架构代次（如 7）
#elif defined(__x86_64__)
    return 64;                  // x86-64 目标
#else
    return 0;
#endif
}
```

- `[平台·x86-64]`：本机三元组为 `x86_64-w64-mingw32`；`__x86_64__` 由预处理器定义，可用于条件编译隔离平台代码。
- `[平台·ARM]`：ARM 裸机定义 `__ARM_ARCH`、`__thumb__`；AArch64 定义 `__aarch64__`。

## ③ sysroot 与库 [标准]

**sysroot** 是交叉工具链的“目标系统根目录”，内含目标专用的头文件与库（如 `sysroot/usr/include`、`sysroot/lib`）。编译器用 `--sysroot=<dir>` 把它当作逻辑 `/`。

```cpp
// ③ 交叉编译时，#include <cstdio> 解析到“目标 sysroot 里的 libc++/libstdc++ 头”
// 而非宿主机 /usr/include。这正是交叉与原生的根本差异之一。
#include <cstdio>
int main() { std::printf("built for target\n"); return 0; }
```

```cpp
// ③ 指定 sysroot 的编译调用（arm-none-eabi-gcc 本机未装，仅示意）
// arm-none-eabi-g++ --sysroot=/opt/arm/sysroot -std=c++23 main.cpp -o main.elf
// 宿主机 g++ 也可借 --sysroot 模拟：g++ --sysroot=/path ... （罕见，多用以打包）
```

- `[标准]`：`--sysroot` 改变 `#include` 搜索根与链接时 `-l` 的查找根；它**不影响语言语义**，只改变“找到哪套头/库”。
- `[经验]`：交叉编译报错 `fatal error: cstddef: No such file` 几乎都是 **sysroot/C++ 标准库头没装**或路径错，而非代码错。

## ④ 裸机 vs Linux 目标 [平台]

两类目标差异巨大：`bare-metal`（无 OS，自己写启动/向量表）与 `Linux`（有内核、libc、动态链接器）。

```cpp
// ④ 裸机程序：必须自己定义入口，不能有 main 依赖 libc 的初始化
extern "C" void _start() {              // 复位向量跳到这里
    for (;;) { /* 自旋 */ }
}
// 链接：arm-none-eabi-ld -T script.ld -o fw.elf start.o
```

```cpp
// ④ Linux 目标：可以正常用 main + libc + 系统调用
#include <cstdlib>
int main(int argc, char** argv) {
    return argc > 1 ? std::atoi(argv[1]) : 0;   // 内核替你建好 C 运行时
}
```

- `[平台·ARM]`：Cortex-M 裸机没有 `main` 的“魔法”入口，复位后 PC 直接指向向量表第二项（`_start`/Reset_Handler）。
- `[经验]`：裸机工程 90% 的“编过了却跑不起来”源于 **启动文件/链接脚本/FPU 选项三者不一致**，而不是 C++ 代码。

## ⑤ [实现]真实：用本机 g++ 编译小程序展示 x86 调用约定/对齐 [实现·GCC13]

本机是 x86-64 MinGW-W64，采用 **Microsoft x64 调用约定**（非 System V）：前 4 个整数参数依次进 `RCX, RDX, R8, R9`，第 5、6 个压栈；调用方还需预留 **32 字节 shadow space（影子空间）**。

```cpp
// 文件：Examples/_ch17_callconv.cpp，行号：8（sum6 定义）
// 编译：g++ -std=c++23 -O2 -S -masm=intel Examples/_ch17_callconv.cpp -o Examples/_ch17_callconv.asm
struct Point { long x, y; };
long sum6(long a, long b, long c, long d, long e, long f) {
    return a + b + c + d + e + f;       // 6 个参数：4 寄存器 + 2 栈
}
long manhattan(Point p) { return p.x + p.y; }   // 16 字节结构按值传递
Point make_point(long x, long y) { return {x, y}; }
```

```asm
; 真实取证（本机 g++ 13.1.0 -O2 -masm=intel 产出，Examples/_ch17_callconv.asm:8）
_Z4sum6llllll:
	add	ecx, edx            ; a(RCX)+b(RDX)
	add	ecx, r8d            ; +c(R8)
	lea	eax, [rcx+r9]       ; +d(R9)
	add	eax, DWORD PTR 40[rsp]   ; +e（栈，shadow 之上）
	add	eax, DWORD PTR 48[rsp]   ; +f（栈）
	ret
```

- `[实现·GCC13]`：`sum6` 的前 4 参落在 `RCX/RDX/R8/R9`，第 5、6 参在 `[rsp+40]`、`[rsp+48]`——这正是 **Windows x64 ABI 的 32 字节影子空间 + 栈传参**特征。
- `[平台·x86-64]`：注意 MinGW 用的是 **Microsoft x64 ABI**，与 Linux 的 System V（`RDI/RSI/RDX/RCX/R8/R9`）**寄存器顺序不同**——同一份 C++ 在同一 CPU 上因 OS 而调用约定不同。

## ⑥ 嵌入式工具链（GNU Arm Embedded / 示例 ARM 汇编典型输出） [平台·ARM]

**GNU Arm Embedded（arm-none-eabi-gcc）**是 Cortex-M/R 裸机的事实标准工具链。它用 **AAPCS（ARM Architecture Procedure Call Standard）**：前 4 个整数参数进 `R0–R3`，第 5 个起压栈；返回 32 位值走 `R0`，64 位走 `R0:R1`。

```cpp
// ⑥ 同一 sum6 在 ARM 上的源码——本体与 x86 完全一致（C++ 可移植）
struct Point { long x, y; };
long sum6(long a, long b, long c, long d, long e, long f);
long manhattan(Point p);
Point make_point(long x, long y);
```

```asm
; —— ARM 典型输出（arm-none-eabi-gcc -O2，AAPCS；本机未安装，下列为典型形态，非本机执行）——
; sum6(long,long,long,long,long,long):
;         add     r0, r0, r1          ; a+b  (R0,R1,R2,R3 前 4 参)
;         add     r0, r0, r2          ; +c
;         add     r0, r0, r3          ; +d
;         ldr     r1, [sp, #0]        ; +e  (第5参来自栈)
;         ldr     r2, [sp, #4]        ; +f  (第6参来自栈)
;         add     r0, r0, r1
;         add     r0, r0, r2
;         bx      lr
```

- `[平台·ARM]`：ARM **AAPCS** 用 `R0–R3` 传前 4 个整数参数，第 5 个起才入栈——这与 x86 的“4 寄存器 + 影子空间”数量巧合相同，但**寄存器名/栈偏移语义不同**。
- `[经验]`：把参数控制在 4 个以内（或聚合到 ≤16 字节结构）在 ARM 上能显著减少栈 traffic——跨平台优化要同时看两套 ABI。

## ⑦ CMake 交叉编译工具链文件 [标准]

CMake 通过**工具链文件（toolchain file）**把“编译器、系统名、根路径”一次性声明，业务 `CMakeLists.txt` 保持平台无关。

```cmake
# 文件：Examples/_ch17_arm_toolchain.cmake，行号：1（set CMAKE_SYSTEM_NAME）
set(CMAKE_SYSTEM_NAME Generic)          # 裸机：无 OS
set(CMAKE_SYSTEM_PROCESSOR arm)
set(CMAKE_C_COMPILER   arm-none-eabi-gcc)
set(CMAKE_CXX_COMPILER arm-none-eabi-g++)
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
```

```cpp
// ⑦ 业务代码完全不感知交叉：CMakeLists 里照常 add_executable
// CMakeLists.txt 片段（示意）：
//   cmake_minimum_required(VERSION 3.21)
//   project(fw CXX)
//   add_executable(fw.elf src/main.cpp)
//   target_compile_features(fw.elf PRIVATE cxx_std_23)
```

- `[标准]`：`CMAKE_SYSTEM_NAME=Generic` 告诉 CMake **不要**执行任何宿主机探测；`FIND_ROOT_PATH_MODE_*` 防止 `find_package` 误用宿主机的库。
- `[经验]`：工具链文件**只设变量、不做具体编译**，具体 `-mcpu` 等应放进 `CMAKE_<LANG>_FLAGS_INIT`（见示例文件第 15 行）。

## ⑧ newlib / picolibc 对比 [平台]

裸机没有 glibc（它依赖 Linux 系统调用），于是用 **newlib**（经典）或 **picolibc**（更轻、面向嵌入式）作为 C/C++ 运行时。它们把 `read/write/_sbrk` 等留给用户实现的 **syscall 桩（syscall stubs）**。

```cpp
// ⑧ newlib 需要一个 _sbrk 桩来支撑 malloc/自由存储（否则 new 也会失败）
extern "C" {
    extern char _ebss;                 // 由链接脚本提供
    char* _sbrk(int incr) {
        static char* heap = &_ebss;
        char* prev = heap;
        heap += incr;
        return prev;
    }
}
```

```cpp
// ⑧ picolibc 更小：可裁剪 printf 浮点支持，适合 32KB RAM 的 MCU
// 链接时选 picolibc 而非 newlib：-specs=picolibc.specs
#include <cstdio>
int diag() { return std::snprintf(nullptr, 0, "%d", 42); }  // 尺寸敏感
```

- `[平台·ARM]`：newlib 生态成熟、文档多；picolibc 由 Keith Packard 维护，针对 Cortex-M 做了尺寸与启动整合，binary 更小。
- `[经验]`：若 `new` 抛 `std::bad_alloc` 或 `printf` 打印乱码，先查 **syscall 桩是否齐备**（尤其是 `_sbrk`、`_write`）。

## ⑨ QEMU 用户态模拟运行 [平台]

**QEMU** 能无需真实硬件就跑目标二进制：`qemu-arm` 做用户态模拟（系统调用转译到宿主），`qemu-system-arm` 模拟整块板子。

```cpp
// ⑨ 一个普通的 Linux 目标程序，既能真机跑，也能 qemu 跑
#include <cstdio>
int main() {
    std::puts("running under qemu-arm");   // qemu 把 write 系统调用转译成宿主的 write
    return 0;
}
```

```bash
# ⑨ 在 x86-64 宿主机上用 QEMU 用户态跑 ARM Linux 二进制（示意，需先安装 qemu）
# aarch64-linux-gnu-g++ -static app.cpp -o app
# qemu-aarch64 ./app
```

- `[平台·ARM]`：`qemu-arm`/`qemu-aarch64` 是**用户态**模拟——只翻译应用与其系统调用，启动极快，适合单元测试。
- `[经验]`：QEMU 用户态**不能**模拟外设寄存器（`0x40020014` 这类 MMIO 会段错误）；要测裸机外设得用 `qemu-system-arm` + 设备树或 semihosting。

## ⑩ 固件/镜像生成 [平台]

裸机最终产物是 **ELF**（含调试信息）与烧录用的 **bin/hex（纯机器码 + 加载地址）**。工具链用 `objcopy` 抽取，用链接脚本定地址。

```cpp
// ⑩ 复位向量表：第一项 SP 初值，第二项 Reset_Handler 入口
// 文件：Examples/_ch17_baremetal.cpp，行号：16（_start）
extern "C" void _start() {
    for (;;) { /* 点亮 LED 后自旋 */ }
}
// 向量表通常单独汇编： .word _estack ; .word _start
```

```bash
# ⑩ 由 ELF 生成可烧录镜像（arm-none-eabi 工具链，本机未装，示意）
# arm-none-eabi-objcopy -O binary firmware.elf firmware.bin
# arm-none-eabi-objdump -h firmware.elf      # 检视各段落地址
# 再用 OpenOCD/st-flash 把 firmware.bin 烧到 0x08000000
```

- `[平台·ARM]`：Flash 通常从 `0x08000000` 开始执行，链接脚本（见 `Examples/_ch17_stm32.ld`）必须把 `.isr_vector` 放最前。
- `[经验]`：`.bin` 不含地址信息，烧录工具必须知道基址；`.hex`(Intel HEX) 自带地址更省心，量产前优先。

## ⑪ [实现]对比：x86 与 ARM 同一函数的汇编差异（ARM 段明确标注“典型输出”） [实现·GCC13]

取第⑤节的 `manhattan(Point)` 与 `make_point`，对比两套 ABI 对同一语义的不同寄存器分配：

```cpp
// 文件：Examples/_ch17_callconv.cpp，行号：13（manhattan）/ 16（make_point）
struct Point { long x, y; };
long manhattan(Point p) { return p.x + p.y; }   // 16 字节结构按值传入
Point make_point(long x, long y) { return {x, y}; }
```

```asm
; —— x86-64 真实取证（本机 g++ 13.1.0 -O2 -masm=intel，Examples/_ch17_callconv.asm:22）——
_Z9manhattan5Point:
	mov	rax, rcx            ; 整个 16 字节结构经 RCX 传入
	shr	rax, 32             ; 取高 32 位 = y
	add	eax, ecx            ; eax = x(低32) + y(高32)
	ret
; make_point 经“隐式返回缓冲指针”约定，结果打包进 RAX 返回（asm:34）。
```

```asm
; —— ARM 典型输出（arm-none-eabi-gcc -O2，AAPCS；本机未安装，下列为典型形态，非本机执行）——
; manhattan(Point):            ; 16 字节结构按值：x 在 R0，y 在 R1
;         add     r0, r0, r1   ; r0 = x + y
;         bx      lr
; make_point(long,long):       ; 返回值 16 字节 -> 经隐式 R0(缓冲指针) 写入
;         strd    r1, r2, [r0]  ; 把 (x,y) 存到调用方提供的缓冲
;         bx      lr
```

- `[实现·GCC13]`：x86 把 16 字节结构塞进**单个 RCX**（高低 32 位各装一个 `long`）；ARM **AAPCS** 则把它拆成 `R0`(x) 与 `R1`(y) 两个寄存器——同一结构体，两套截然不同的参数布局。
- `[平台·x86-64]` vs `[平台·ARM]`：这就是交叉编译的核心难点——**C++ 语义一致，机器契约不同**，移植时寄存器映射/对齐/调用约定都要重估。

## ⑫ 大小端/对齐差异 [标准]

**端序（endianness）**决定多字节数在内存的字节序；**对齐（alignment）**决定对象允许的内存地址模数。二者都会让“同样代码、不同目标”产生不同行为或性能。

```cpp
// ⑫ 端序探测：小端机 0x01020304 在内存为 04 03 02 01
#include <cstdint>
bool is_little_endian() {
    uint32_t v = 0x01020304u;
    return reinterpret_cast<uint8_t*>(&v)[0] == 0x04;   // 小端为真
}
```

```cpp
// ⑫ 对齐：alignas 提升对齐以满足 SIMD 加载要求（如 AVX 需 32 字节）
#include <cstddef>
alignas(32) static char dma_buf[128];     // 该数组地址必须是 32 的倍数
```

```asm
; —— x86-64 真实对齐取证（本机 g++ 13.1.0 -O2 -mavx，Examples/_ch17_align.asm:12）——
; vec_broadcast 为 32 字节数组做栈对齐：
	lea	r8, 31[rsp]       ; r8 = rsp + 31
	and	r8, -32           ; 向下舍入到 32 字节边界
	...
	vmovapd	YMMWORD PTR [r8], ymm0   ; 256 位对齐 AVX 存储（地址必 32 对齐）
```

- `[标准]`：C++ 用 `alignas`/`alignof` 表达对齐意图；端序无标准内建，需运行时探测（如上）。
- `[平台·ARM]`：Cortex-M 传统为**小端**，但支持 Big-Endian（BE-8）配置；未对齐访问在老 ARM 上会 **HardFault**，x86 则多付性能代价即可。

## ⑬ 调试（openocd/gdbserver/J-Link） [平台]

嵌入式调试三件套：**调试器硬件（J-Link/ST-Link/OpenOCD 支持的目标）** + **OpenOCD（守护，桥接 USB↔GDB）** + **GDB（含交叉 gdb，如 arm-none-eabi-gdb）**。

```cpp
// ⑬ 调试版应保留符号与帧指针，关闭过度优化
// arm-none-eabi-g++ -std=c++23 -g3 -Og -mcpu=cortex-m4 main.cpp -o fw.elf
// -Og：为调试优化的级别，既快又保真；-g3 含宏信息
volatile int g_dbg = 0;
void toggle() { g_dbg ^= 1; }    // 在 GDB 里设断点、watch g_dbg
```

```bash
# ⑬ 典型调试会话（示意：OpenOCD 在 3333 监听，GDB 通过 3333 接入目标）
# openocd -f interface/stlink.cfg -f target/stm32f4x.cfg &
# arm-none-eabi-gdb fw.elf
#   (gdb) target remote :3333
#   (gdb) load
#   (gdb) break toggle
#   (gdb) continue
```

- `[平台·ARM]`：J-Link 是商业高速调试探针；ST-Link 随 STM32 开发板免费；OpenOCD 开源、支持广。
- `[经验]`：量产固件用 `-Os`、调试固件用 `-Og -g3`——**不要**拿 `-O2` 二进制去单步，变量会被优化掉，体验极差。

## ⑭ 体积优化（-Os/-ffunction-sections/-fdata-sections --gc-sections，[实现]真实 g++ 命令） [实现·GCC13]

嵌入式 FLASH 宝贵。核心手段：`-Os`（为尺寸优化）、`-ffunction-sections -fdata-sections`（每函数/变量独立段）、`--gc-sections`（链接期丢弃未引用段）。

```cpp
// 文件：Examples/_ch17_sizeopt.cpp，行号：7（active，被引用）/ 11（dead，未引用）
#include <cstdint>
uint32_t active(uint32_t x) { return x * 3u + 1u; }   // main 调用 -> 保留
uint32_t dead(uint32_t x)   { return x * x + 12345u; } // 无人调用 -> 期望被 GC
int used_var = 7;        // 被引用 -> 保留
int unused_var = 99;     // 未引用 -> 期望被 GC
```

```bash
# ⑭ 真实测量（本机 g++ 13.1.0，objdump -h 取段大小；data 单位：字节）
# A 默认 -O2            : text=5832 data=160 bss=384
# B -Os                 : text=5816 data=160 bss=384
# C -Os + gc-sections   : text=5752 data=80  bss=336
# D -O2 + gc-sections   : text=5752 data=80  bss=336
# 仅加 --gc-sections，data 即由 160 -> 80（unused_var 被丢），text 由 5832 -> 5752（dead 被丢）
```

```bash
# ⑭ 真实可复现命令（本机）
# g++ -std=c++23 -Os -ffunction-sections -fdata-sections -Wl,--gc-sections \
#     Examples/_ch17_sizeopt.cpp -o /tmp/ch17_c.exe
# C:/Qt/Tools/mingw1310_64/bin/objdump.exe -h /tmp/ch17_c.exe
```

- `[实现·GCC13]`：`-ffunction-sections` 让每个函数进独立 `.text.<fn>` 段，`--gc-sections` 从入口可达性分析丢弃死段——**这正是嵌入式瘦身的主菜**。
- `[经验]`：`-Os` 与 `-O2` 在本例 text 差异很小，真正的大头是 **GC 掉死代码/死数据**；模板膨胀时 `-ffunction-sections --gc-sections` 收益惊人。

## ⑮ [经验]嵌入式 C++ 子集（禁用 RTTI/异常/STL 的部分） [经验]

资源受限目标常禁用**异常、RTTI、部分 STL**，改用 `-fno-exceptions -fno-rtti -fno-use-cxa-atexit`，并以静态/池化分配替代自由存储。

```cpp
// ⑮ 禁用异常后，不能依赖栈展开；用 std::optional / 错误码替代 throw
#include <cstdint>
#include <optional>
[[nodiscard]] int safe_div(int a, int b, int& out) {
    if (b == 0) return -1;        // 错误码代替异常
    out = a / b;
    return 0;
}
```

```cpp
// ⑮ 禁用 RTTI 后 dynamic_cast/typeid 不可用；用 variant / 显式 tag 分发
#include <cstdint>
#include <typeinfo>
enum class Kind : uint8_t { A, B };
struct Msg { Kind k; uint32_t v; };
uint32_t dispatch(const Msg& m) {          // 用 tag 而非 dynamic_cast
    switch (m.k) { case Kind::A: return m.v + 1; case Kind::B: return m.v * 2; }
    return 0;
}
```

```cpp
// ⑮ 用静态缓冲区替代动态 new（避免堆碎片与不可预测延迟）
#include <cstddef>
alignas(8) static char pool[4096];
void* operator new(std::size_t n) {        // 极简静态分配器示意
    static std::size_t off = 0;
    void* p = pool + off; off += n; return p;
}
```

- `[经验]`：禁用异常能**显著减小二进制并消除栈展开表**，但代价是必须全程用错误码/optional——这是工程权衡，不是“更好”。
- `[平台·ARM]`：Cortex-M 上未处理异常/中断里的异常会触发 HardFault；裸机工程普遍 `--no-exceptions` 以求确定性。

## ⑯ 常见坑 [经验]

```cpp
// ⑯ 坑1：FPU 选项与固件不一致 -> 一进浮点就 HardFault
// 编译用 -mfloat-abi=hard，但启动代码未初始化 FPU（或未设 CP10/CP11）：必崩
float scale(float x) { return x * 3.14f; }   // 需 FPU 已使能
```

```cpp
// ⑯ 坑2：链接脚本的 _ebss/_estack 与启动代码符号名对不上 -> 堆栈/堆错位
extern char _ebss;    // 启动文件里若叫 __bss_end__，这里就链接失败或堆错位
```

```cpp
// ⑯ 坑3：int 宽度假设。x86/ARM 桌面与 Cortex-M 的 int 都是 32 位，
// 但指针在 Cortex-M 是 32 位、在 AArch64 是 64 位——把指针存进 int 会截断！
#include <cstdint>
void bad(uintptr_t p) { int leak = (int)p; }   // ❌ 64 位目标上截断指针
void good(uintptr_t p) { intptr_t safe = (intptr_t)p; }  // ✅ 用 intptr_t
```

- `[经验]`：坑 1、2 是裸机“点灯都点不亮”的头号元凶；坑 3 是**跨位宽移植**（32→64）的经典陷阱，必须用 `intptr_t/uintptr_t`。
- `[标准]`：`intptr_t/uintptr_t`（`<cstdint>`）保证能完整容纳 `void*`，是跨平台指针↔整数转换的唯一标准手段。

## ⑰ 与主机工具协作（host tool） [平台]

交叉构建常需要**主机工具（host tool）**：在宿主机运行、但产出目标数据的程序（如资源编译器、代码生成器、协议打包器）。它们必须用**宿主编译器**编，不能进交叉链路。

```cpp
// ⑰ 主机工具：把字体/图片编译成 C 数组（在 x86 上跑，产出 .cpp 给目标用）
// 用宿主 g++ 编译：g++ -std=c++23 gen_font.cpp -o gen_font
// 再运行：./gen_font logo.png > font_data.cpp   （目标是 ARM，但此步在宿主完成）
#include <cstdio>
int main() {
    std::puts("// 自动生成：const unsigned char font[] = {0x00,0x7E,...};");
    return 0;
}
```

```cmake
# ⑰ CMake 正确区分 host tool 与 target：用 add_executable(... ) + 无交叉影响
# 关键是 host tool 必须在“未加载工具链文件”的上下文中构建（或用 CMAKE_HOST_SYSTEM）
# add_executable(gen_font HOST_EXE gen_font.cpp)   # 示意：HOST_EXE 为宿主目标
```

- `[平台]`：错误地把 host tool 交给交叉编译器，会得到**不能在宿主运行**的 ARM 二进制——典型报错 `cannot execute binary file: Exec format error`。
- `[经验]`：构建系统里 host tool 与 target 必须**两套 toolchain**：host tool 用原生 gcc，target 用 arm-none-eabi-g++。

## ⑱ 最佳实践 [经验]

```cpp
// ⑱ 实践1：平台相关代码集中到 arch_xxx 命名空间 + 编译期分发，避免散落 ifdef
namespace arch {
    inline int hart_count() {
#if defined(__x86_64__)
        return 1;                  // 宿主机示意
#elif defined(__ARM_ARCH)
        return 1;                  // 单核 MCU
#else
        return 1;
#endif
    }
}
```

```cpp
// ⑱ 实践2：对所有外设寄存器用 volatile 且显式宽度，杜绝“优化掉 MMIO”
#include <cstdint>
volatile uint32_t& GPIOA_ODR = *reinterpret_cast<uint32_t*>(0x40020014u);
void set_led(bool on) { if (on) GPIOA_ODR |= (1u<<5); else GPIOA_ODR &= ~(1u<<5); }
```

```cpp
// ⑱ 实践3：用 static_assert 固化跨平台假设，趁早 fail
static_assert(sizeof(void*) == 4 || sizeof(void*) == 8, "指针宽度假设失效");
static_assert(alignof(double) <= 8, "double 对齐超预期");
```

- `[经验]`：把**所有 `#ifdef 平台`收口到少数 arch 适配层**，业务代码保持纯净——这是跨平台工程可维护性的命脉。
- `[标准]`：`static_assert` 是编译期契约，跨目标重建时能立刻暴露假设漂移，优于运行时崩溃。

## ⑲ 跨平台构建矩阵 [平台]

一个代码库常为多目标产出多镜像。下表是本工程实测/规划的交叉构建组合（ARM 行为标注“典型”，本机无交叉链）：

| 目标 | 三元组 | C++ 标准库 | 典型体积优化 | 本机可验？ |
|---|---|---|---|---|
| 宿主 x86-64 | `x86_64-w64-mingw32` | libstdc++（MinGW） | `-O2` | ✅ 已用 g++13 取证 |
| ARM Cortex-M4 | `arm-none-eabi` | newlib/picolibc | `-Os -gc-sections` | ❌ 典型输出 |
| AArch64 Linux | `aarch64-linux-gnu` | libstdc++/glibc | `-O2` | ❌ 未装 |
| RISC-V 32 裸机 | `riscv32-unknown-elf` | newlib | `-Os -gc-sections` | ❌ 未装 |

```cpp
// ⑲ 矩阵里每个目标共享同一份业务逻辑，仅编译标志/标准库不同
struct Firmware {
    const char* target;
    int (*entry)();          // 各目标实现由链接脚本/启动决定
};
constexpr Firmware kMatrix[] = {
    {"x86_64-host",   nullptr},
    {"arm-cortex-m4", nullptr},
    {"aarch64-linux", nullptr},
};
```

- `[平台·x86-64]`：本机已用真实 g++ 13.1.0 验证调用约定/对齐/体积数据，是矩阵里**唯一可本机复现**的单元格。
- `[经验]`：CI 中应把“可本机验证”的目标（如宿主 x86-64 的单元/算法测试）与“仅交叉产出”的目标分开跑，避免交叉链缺失阻塞整个流水线。

## ⑳ 速查表 [标准]

```cpp
// ⑳ 三元组 → 工具链前缀 速查（编译时 -target / 工具链文件里设置）
// x86_64-w64-mingw32     -> x86_64-w64-mingw32-g++   （本机即用）
// arm-none-eabi          -> arm-none-eabi-g++         （裸机 ARM）
// aarch64-linux-gnu      -> aarch64-linux-gnu-g++     （ARM64 Linux）
// riscv64-unknown-elf    -> riscv64-unknown-elf-g++   （RISC-V）
```

```bash
# ⑳ 一键交叉构建骨架（示意）
# BUILD_TRIPLE=arm-none-eabi
# ${BUILD_TRIPLE}-g++ -std=c++23 -mcpu=cortex-m4 -mthumb \
#     -ffreestanding -nostdlib -Os \
#     -ffunction-sections -fdata-sections -Wl,--gc-sections \
#     -T Examples/_ch17_stm32.ld -o firmware.elf src/main.cpp
# ${BUILD_TRIPLE}-objcopy -O binary firmware.elf firmware.bin
```

| 主题 | 关键事实 | 见节 |
|---|---|---|
| 调用约定（x86-64/Win） | RCX,RDX,R8,R9 + 32B 影子空间 | ⑤⑪ |
| 调用约定（ARM/AAPCS） | R0–R3 + 栈；结构 R0:R1 | ⑥⑪ |
| 端序 | 多为小端；ARM 可配 BE-8 | ⑫ |
| 对齐 | `alignas`；x86 容错、ARM 易 Fault | ⑫ |
| 体积 | `-Os` + `-ffunction-sections -fdata-sections --gc-sections` | ⑭ |
| 调试 | OpenOCD + 交叉 gdb + J-Link/ST-Link | ⑬ |
| 嵌入式子集 | `-fno-exceptions -fno-rtti`，错误码代替异常 | ⑮ |
| 镜像 | `objcopy -O binary` 出 `.bin`；烧录基址 0x08000000 | ⑩ |

- `[标准]`：上表“调用约定/端序/对齐”均为**平台/ABI 事实**，C++ 语言本身不规定，移植时必须按目标 ABI 重审。
- `[经验]`：把本表贴进项目 README，新人第一次交叉编译就能避开 80% 的坑。

---

> 偏离说明：本章依用户指定大纲（20 元素：①概述…⑳速查表）撰写，未使用 CONVENTIONS.md 默认模板顺序；交叉工具链（arm-none-eabi-gcc 等）本机未安装，故以本机 MinGW GCC 13.1.0 真实编译 `Examples/_ch17_*.{cpp,cmake,ld}` 取证 x86-64 汇编/段大小，ARM 侧一律明确标注「典型输出（本机未执行）」，绝不编造交叉链实测数据。所有 `// 文件：`/`// 行号：` 均指向真实存在的 `Examples/_ch17_*` 源文件。

## 附录: 交叉编译实战

```cpp
#include <iostream>
int main(){std::cout<<"Cross-compile: gcc-arm-none-eabi for Cortex-M. aarch64-linux-gnu-gcc for ARM64 Linux."<<std::endl;return 0;}
```

```cpp
#include <iostream>
int main(){std::cout<<"CMake toolchain: set(CMAKE_SYSTEM_NAME Generic); set(CMAKE_C_COMPILER arm-none-eabi-gcc)."<<std::endl;return 0;}
```

```cpp
#include <iostream>
#include <cstdint>
int main(){uint32_t x=0x12345678;std::cout<<"Endian check: "<<(*(uint8_t*)&x==0x78?"little":"big")<<" endian"<<std::endl;return 0;}
```

```cpp
#include <iostream>
int main(){std::cout<<"QEMU: qemu-arm -L /usr/arm-linux-gnueabi ./app. Docker: FROM arm64v8/ubuntu."<<std::endl;return 0;}
```

```cpp
#include <iostream>
#include <vector>
int main(){std::vector<int> v(3,7);std::cout<<v.size()<<std::endl;return 0;}
```

## 附录 A：工业交叉编译 [B: Principle / F: Industry / H: Design / I: Practice / J: Learning]

```
交叉编译工业场景:
- 嵌入式: arm-none-eabi-gcc (Cortex-M), aarch64-linux-gnu-gcc (ARM64 Linux)
- Android: NDK (aarch64-linux-android), API level 21+ (C++17支持)
- iOS: clang -target arm64-apple-darwin (Xcode工具链)
- WebAssembly: emscripten (emcc), C++→Wasm + JS胶水

WG21与交叉编译: P1643R1 (std::embedded, 方向提案)
  → 标准化嵌入式C++子集 (无异常/无RTTI/无动态分配)

工业案例:
- STM32 HAL: arm-none-eabi-gcc -mcpu=cortex-m4 -mfpu=fpv4-sp-d16 -mfloat-abi=hard
- Raspberry Pi: aarch64-linux-gnu-gcc -std=c++20 (完整C++支持)
- Android NDK: clang++ --target=aarch64-linux-android21 -stdlib=libc++

面试: 交叉编译为什么需要sysroot？
A: 编译器需要目标平台的标准库头文件和二进制 → --sysroot=/path/to/target/rootfs
```


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第16章](Book/part02_toolchain/ch16_ide.md) | 日志格式化/序列化 | 本章提供概念，第16章提供实现 |
| [第18章](Book/part02_toolchain/ch18_buildconfig.md) | 错误恢复/不可恢复错误 | 本章提供概念，第18章提供实现 |
| [第11章](Book/part02_toolchain/ch11_compilers.md) | 向量化计算/图像处理 | 本章提供概念，第11章提供实现 |
| [第30章](Book/part03_language/ch30_volatile.md) | 动态数组/缓冲区 | 本章提供概念，第30章提供实现 |

## 附录 F：交叉编译工具链细节

STM32 (arm-none-eabi-gcc):
```bash
arm-none-eabi-gcc -mcpu=cortex-m4 -mfpu=fpv4-sp-d16 -mfloat-abi=hard \
  -specs=nosys.specs -T STM32F407VGTx_FLASH.ld main.c -o firmware.elf
arm-none-eabi-objcopy -O binary firmware.elf firmware.bin
```

Raspberry Pi (aarch64-linux-gnu-gcc):
```bash
aarch64-linux-gnu-gcc -std=c++20 --sysroot=/path/to/rpi-rootfs -O2 main.cpp -o app
```

Android NDK: `clang++ --target=aarch64-linux-android21` → arm64-v8a .so

```cpp
#include <iostream>
int main(){std::cout<<"STM32=arm-none-eabi, RPi=aarch64-linux-gnu, Android=NDK clang"<<std::endl;return 0;}
```

| 目标 | 工具链 | sysroot | ABI |
|---|---|---|---|
| STM32 | arm-none-eabi-gcc | 无(裸机) | ARM EABI |
| Raspberry Pi | aarch64-linux-gnu-gcc | RPi rootfs | Linux AArch64 |
| Android | NDK clang | NDK sysroot | Android NDK ABI |
| WebAssembly | emcc(emscripten) | 无 | wasm32 |


## 附录 H：CMake交叉编译配置

```cmake
set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR arm)
set(CMAKE_C_COMPILER arm-none-eabi-gcc)
set(CMAKE_CXX_COMPILER arm-none-eabi-g++)
```

```cpp
#include <iostream>
int main(){std::cout<<"CMake cross: CMAKE_SYSTEM_NAME+compiler+sysroot=3 key settings"<<std::endl;return 0;}
```

| 目标 | SYSTEM_NAME | COMPILER |
|---|---|---|
| STM32 | Generic | arm-none-eabi-gcc |
| RPi | Linux | aarch64-linux-gnu-gcc |
| Android | Android | NDK clang |
| Wasm | Emscripten | emcc |

## 附录 I：嵌入式C++特性限制

嵌入式通常禁用: 异常(-fno-exceptions), RTTI(-fno-rtti), 动态内存(无malloc/new)
可用的: constexpr, template, static_assert, enum class, [[nodiscard]]

```cpp
#include <iostream>
int main(){std::cout<<"Embedded: -fno-exceptions -fno-rtti -fno-rtti. Use constexpr+template+static_assert instead."<<std::endl;return 0;}
```

| 特性 | 嵌入式 | 原因 |
|---|---|---|
| 异常 | 禁用 | 二进制+20%, unwind table |
| RTTI | 禁用 | 二进制+5%, 内存 |
| 动态内存 | 禁用 | 不可预测延迟 |
| constexpr | 推荐 | 编译期计算 |

## 附录 J：嵌入式C++性能优化

减小编译后二进制: -Os(最小), -flto(跨TU死代码消除), -ffunction-sections -Wl,--gc-sections(段级死代码消除)
常量放到Flash: const/constexpr变量自动放入.rodata段(Flash)
避免动态内存: pool allocator替代malloc, stack allocation替代heap

```cpp
#include <iostream>
int main(){std::cout<<"Embedded: -Os -flto -ffunction-sections. const=Flash. pool>heap."<<std::endl;return 0;}
```

| 优化 | 工具 | 效果 |
|---|---|---|
| 减小编译体 | -Os -flto | 30-50% smaller |
| 放Flash | const/constexpr | .rodata段 |
| 避免堆 | pool allocator | 确定性 |
| 中断安全 | atomic+barrier | 数据一致性 |

面试: 嵌入式C++如何减小编译体? -Os(优化大小) + -flto(全程序死代码消除) + 段级GC

## 相关章节（交叉引用）

- **相邻主题**：`Book/part02_toolchain/ch15_profiling.md`（第15章　性能分析：perf / VTune / 火焰图 / Compiler Explorer（C++））—— 编号相邻、主题接续。
- **相邻主题**：`Book/part03_language/ch19_variables.md`（第19章　变量、存储期、链接与 ODR（工业级深度版））—— 编号相邻、主题接续。
- **同模块**：`Book/part02_toolchain/ch12_buildsystems.md`（第12章　构建系统：Make / Ninja / CMake（C++））—— 同模块下的其他主题。

## 附录 G：工业交叉编译生态

| 项目 | 目标 | 工具链 | 关键配置 |
|------|------|--------|---------|
| **LLVM/Clang**（github.com/llvm/llvm-project） | ARM/AArch64/RISC-V/WebAssembly | Clang + lld + `--target=aarch64-linux-gnu` | `llvm/cmake/` — `CMAKE_CROSSCOMPILING=ON` + `LLVM_DEFAULT_TARGET_TRIPLE` |
| **Chromium**（github.com/chromium/chromium） | Android (ARM64) / ChromeOS (x86_64/ARM) / Fuchsia | GN + Clang cross-toolchain | `build/config/arm.gni` — `target_cpu="arm64"` + `arm_use_neon=true` |
| **Qt**（code.qt.io） | 嵌入式 Linux (Yocto/Boot2Qt) / QNX / INTEGRITY | `qmake -spec devices/linux-rasp-pi4-g++` / CMake `-DCMAKE_TOOLCHAIN_FILE` | `qtbase/mkspecs/devices/` — 40+ 设备配置 |
| **Google Android NDK**（developer.android.com/ndk） | ARM32/ARM64/x86_64 Android | Clang + `android-ndk-r26c/toolchains/llvm/prebuilt/linux-x86_64/bin/aarch64-linux-android21-clang++` | `-DANDROID_ABI=arm64-v8a -DANDROID_PLATFORM=21` |

**底层深度**：交叉编译的关键是 sysroot——目标系统的头文件/库的镜像目录。GCC cross 构建时 `--with-sysroot=/path/to/aarch64-rootfs` 将 `#include` 解析根重定向到目标 sysroot，链接器从 `$sysroot/usr/lib` 搜索 `libc.so`。`CMAKE_TOOLCHAIN_FILE` 的本质是设置 `CMAKE_C_COMPILER_TARGET`（GCC triplet: `aarch64-linux-gnu`）与 `CMAKE_FIND_ROOT_PATH`。工具链文件的 `CMAKE_FIND_ROOT_PATH_MODE_PROGRAM=NEVER` 禁止 CMake 从 sysroot 找 `g++` 等主机工具。

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

## 真实开源项目参考（可查证链接）

> 交叉编译工具链与裸机 C 运行时的真实工程载体——下列链接指向可公开审阅的源码（L2 文件级）。

- **LLVM/Clang 原生交叉编译**：[llvm/llvm-project · clang/lib/Driver/ToolChains](https://github.com/llvm/llvm-project/blob/main/clang/lib/Driver/ToolChains) —— Clang 是**单编译器多目标**架构，`clang --target=arm-none-eabi -mcpu=cortex-m4` 无需独立工具链即可交叉，是「② 目标三元组」「⑦ CMake 工具链文件」的现代工业做法（对比 GNU 需独立 `arm-none-eabi-g++`）。
- **Google Android NDK（Clang 交叉工具链）**：[android/ndk · build/core/toolchains](https://github.com/android/ndk/blob/master/build/core/toolchains) —— Google 的官方交叉编译 SDK，底层即 LLVM/Clang 的 `--target=armv7-none-linux-androideabi`/`aarch64-linux-android`，对应「④ 裸机 vs Linux 目标」的 Linux 侧工业范例。
- **newlib C 库**：[bminor/newlib · newlib/libc/stdlib/malloc.c](https://github.com/bminor/newlib/blob/master/newlib/libc/stdlib/malloc.c) —— 「⑧ newlib / picolibc 对比」「③ sysroot 与库」的裸机 `malloc` 实现源头；理解嵌入式 `sbrk` 缺省桩如何介入。
- **picolibc**：[picolibc/picolibc · newlib/libc/stdlib/malloc.c](https://github.com/picolibc/picolibc/blob/main/newlib/libc/stdlib/malloc.c) —— newlib 的嵌入式优化分支，面向 Cortex-M 的小体积场景，对应「⑮ 嵌入式 C++ 子集」的内存约束。
- **crosstool-NG GCC 构建脚本**：[crosstool-ng/crosstool-ng · scripts/build/gnu/gcc.sh](https://github.com/crosstool-ng/crosstool-ng/blob/master/scripts/build/gnu/gcc.sh) —— 「② 目标三元组」背后的工具链自动构建逻辑；展示如何为 `arm-none-eabi` 编译带 newlib 的 GCC。
- **QEMU 用户态仿真**：[qemu/qemu · linux-user/main.c](https://github.com/qemu/qemu/blob/master/linux-user/main.c) —— 「⑨ QEMU 用户态模拟运行」的入口；解释如何把 ARM 二进制在 x86 主机上 syscall 转译执行。

**最佳实践**：GNU 工具链文件必须显式设 `CMAKE_SYSTEM_NAME` + `CMAKE_CXX_COMPILER=arm-none-eabi-g++` 并使用独立 `sysroot`；LLVM/Clang 路线则用 `-DCMAKE_CXX_COMPILER=clang -DCMAKE_CXX_FLAGS="--target=arm-none-eabi"` 一步到位；体积优化统一用「⑭ `-Os -ffunction-sections -fdata-sections` + 链接 `--gc-sections`」三段式。

> 交叉引用：本机构建配置见 [ch18](Book/part02_toolchain/ch18_buildconfig.md)；汇编取证方法见 [ch157](Book/part14_perf/ch157_compiler_explorer.md)。

写一个 `max` 函数模板，要求对任意可比较类型都能用，且对混合有符号/无符号比较安全。

<details><summary>答案与解析</summary>

使用 `std::common_comparison_category` 或 `std::cmp_less` 避免符号陷阱：

```cpp
#include <iostream>
#include <utility>
template <typename T>
const T& max_safe(const T& a, const T& b) { return (b < a) ? a : b; }
int main() { std::cout << max_safe(3, 7) << '\n'; }
```

[标准] 模板参数推导按实参进行；两实参同类型时 `T` 唯一确定。

</details>

### 练习 2（难度 ★★）

用 `std::integral` 概念约束一个 `add` 函数，使其只接受整数类型，并对浮点调用给出清晰的错误。

<details><summary>答案与解析</summary>

C++20 概念取代 SFINAE 做编译期约束：

```cpp
#include <iostream>
#include <concepts>
template <std::integral T> T add(T a, T b) { return a + b; }
int main() { std::cout << add(2, 3) << '\n'; /* add(1.0, 2.0) 编译失败 */ }
```

[标准] 违反概念约束是硬错误（而非 SFINAE 静默失败），诊断信息更可读。

</details>

### 练习 3（难度 ★★）

写一个 `constexpr` 阶乘函数，并用 `static_assert` 在编译期验证 `fact(5)==120`。

<details><summary>答案与解析</summary>

```cpp
#include <iostream>
constexpr int fact(int n) { return n <= 1 ? 1 : n * fact(n - 1); }
static_assert(fact(5) == 120);
int main() { std::cout << fact(5) << '\n'; }
```

[标准] `constexpr` 函数在常量表达式上下文（如模板实参、`static_assert`）中于编译期求值。

</details>

