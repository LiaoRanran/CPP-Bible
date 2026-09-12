# 资料研究第十七轮：动态链接与加载——GOT/PLT、PIC/PIE、ld.so 与 RELRO

> 2026-09-11，底层工程资料研究员。主题：Linux 动态链接与加载的底层实现（GOT/PLT 延迟绑定、PIC/PIE 位置无关代码、ld.so 加载流程与符号搜索顺序、RELRO 安全机制、符号可见性）。
> 检索方式：general_search + man7.org 共享库培训讲义 + ld.so man page + Linux Foundation ELF 规范 + Eli Bendersky PIC 经典文章 + Oracle x64 ABI 文档。
> **系统域第一轮**（运行时域一轮已完成，本轮进入系统/加载器域）。

---

## 一、动态链接的核心问题

### 1. 为什么需要动态链接？

- 共享库（.so）的**代码段可被多个进程共享**（只读，物理内存只存一份）
- 但共享库的加载地址在编译时**未知**（ASLR 随机化）
- 所以共享库的代码**不能包含绝对地址**——必须是位置无关代码（PIC）

### 2. 解决方案三件套

```
PIC（位置无关代码）  →  代码不含绝对地址，用 RIP 相对寻址
GOT（全局偏移表）    →  存绝对地址的指针数组，运行时由加载器填充
PLT（过程链接表）    →  函数调用的跳板，实现延迟绑定
```

---

## 二、GOT（Global Offset Table，全局偏移表）

### 1. 结构

GOT 是一个指针数组，每个外部符号（函数或全局变量）对应一个条目。存在两个段：

| 段 | 用途 |
|---|---|
| `.got` | 全局变量的地址（数据重定位） |
| `.got.plt` | 函数的地址（PLT 延迟绑定用） |

### 2. .got.plt 的布局

```
GOT[0]  →  _DYNAMIC 段的地址          （动态链接器用）
GOT[1]  →  link_map 指针              （动态链接器用）
GOT[2]  →  _dl_runtime_resolve 地址    （动态链接器的符号解析函数）
GOT[3]  →  第一个导入函数的地址        （初始指向 PLT 内的下一条指令）
GOT[4]  →  第二个导入函数的地址
...
```

- 运行时动态链接器填充每个条目的真实地址
- **来源**：ashishkr.com "GOT/PLT: The Dark Art of Dynamic Linking" + TUM 编译原理讲义
- **可信度**：S

---

## 三、PLT（Procedure Linkage Table，过程链接表）

### 1. 结构

PLT 是一组小代码桩（stub），每个导入函数一个。存在 `.plt` 段（只读代码段）。

```
PLT[0]  →  公共桩：push GOT[1]; jmp *GOT[2]（调用 _dl_runtime_resolve）
PLT[1]  →  printf 的桩：jmp *GOT[3]; push 0x0; jmp PLT[0]
PLT[2]  →  malloc 的桩：jmp *GOT[4]; push 0x1; jmp PLT[0]
...
```

### 2. 延迟绑定（Lazy Binding）的完整流程

**第一次调用 printf：**

```
call printf@plt
  │
  ├─ PLT[printf]: jmp *GOT[printf]
  │     │
  │     └─ GOT[printf] 初始值 = PLT[printf] 的下一条指令地址（push 0x0）
  │        所以 jmp 落到下一条指令，不是真正的 printf
  │
  ├─ push 0x0              ← 符号索引（printf 在重定位表中的索引）
  ├─ jmp PLT[0]            ← 跳转到公共桩
  │
  ├─ PLT[0]: push GOT[1]   ← link_map 指针
  ├─ jmp *GOT[2]           ← 调用 _dl_runtime_resolve
  │
  └─ _dl_runtime_resolve:
        ├─ 根据符号索引查找 printf 的真实地址
        ├─ 在已加载的库中解析符号
        ├─ 填充 GOT[printf] = printf 真实地址
        └─ 跳转到真实 printf
```

**第二次调用 printf：**

```
call printf@plt
  └─ PLT[printf]: jmp *GOT[printf]
        └─ GOT[printf] 已被填充 = printf 真实地址 → 直接跳转
```

- **关键洞察**：第一次调用有解析开销（符号查找 + 哈希表搜索），后续调用只有一次间接跳转（`jmp *GOT`）
- **来源**：PVS-Studio 分析 + CSDN 延迟绑定详解 + Oracle x64 ABI
- **可信度**：S

---

## 四、PIC/PIE（位置无关代码）

### 1. x86-64 的关键：RIP 相对寻址

- x86-64 引入了 **RIP 相对寻址模式**——所有 64 位 mov 引用内存默认用 RIP 相对
- 地址 = 当前指令地址 + 32 位偏移量
- 这使得 PIC 代码在 x86-64 上比 x86-32 高效得多（x86-32 需要 `call __i686.get_pc_thunk.bx` 来获取 PC）

### 2. -fPIC 改变了什么

| 操作 | 非 PIC | PIC（-fPIC） |
|---|---|---|
| 访问全局变量 | `mov rax, [abs_addr]` | `mov rax, [rip+got_offset]` → 间接访问 GOT |
| 调用外部函数 | `call printf` | `call printf@plt` → 经 PLT 间接调用 |
| 调用内部函数 | `call func`（直接） | `call func@plt`（默认也经 PLT，除非 visibility=hidden） |

### 3. PIC vs PIE

| 维度 | PIC（-fPIC） | PIE（-fPIE） |
|---|---|---|
| 用途 | 共享库（.so） | 可执行文件 |
| 位置无关 | 是 | 是 |
| 代码模型 | 大代码模型（支持大偏移） | 小代码模型（可执行文件通常较小） |
| ASLR | 库加载地址随机 | 可执行文件加载地址随机 |
| 性能开销 | 略高（GOT 间接访问） | 略高 |

### 4. 为什么 x86-64 共享库必须用 PIC？

- 非 PIC 代码使用 32 位绝对地址重定位（`R_X86_64_32`）
- 但 64 位地址空间中，32 位重定位可能溢出（库可能被加载到 4GB 以上）
- 所以 GCC 对 x86-64 共享库**强制** PIC——非 PIC 代码会报 `R_X86_64_32 against symbol can not be used` 错误
- **来源**：Eli Bendersky "PIC in shared libraries on x64" + LinuxVox 分析
- **可信度**：S

---

## 五、ld.so 动态加载器

### 1. 启动流程

```
内核加载程序
  │
  ├─ 读取 ELF 头，发现 PT_INTERP = /lib64/ld-linux-x86-64.so.2
  ├─ 加载 ld.so 到内存
  └─ 把控制权交给 ld.so
        │
        ├─ 1. 重定位自身（ld.so 也是 PIC，需要自举）
        ├─ 2. 读取主程序的 .dynamic 段
        ├─ 3. 解析 DT_NEEDED 条目（依赖的共享库列表）
        ├─ 4. 递归加载所有依赖库（深度优先）
        ├─ 5. 对所有库进行符号重定位（填充 GOT，除非延迟绑定）
        ├─ 6. 调用各库的 .init 段（初始化函数）
        └─ 7. 把控制权交给主程序的 _start
```

### 2. 库搜索顺序

```
1. DT_RPATH（已废弃，仅当无 DT_RUNPATH 时）
2. LD_LIBRARY_PATH 环境变量（setuid/setgid 程序忽略，安全原因）
3. DT_RUNPATH（现代推荐，支持 $ORIGIN 相对路径）
4. /etc/ld.so.cache（ldconfig 生成的编译缓存）
5. /lib、/usr/lib（默认路径）
```

- **来源**：ld.so man page + man7.org 共享库培训讲义 + Linux Foundation ELF 规范
- **可信度**：S

### 3. 符号解析

- 动态链接器在**所有已加载库**的符号表中查找符号
- 查找顺序：按依赖图的**广度优先**（先主程序，再其直接依赖，再间接依赖）
- 第一个匹配的符号胜出（可能导致符号冲突/符号劫持）
- 这也是为什么 `-fvisibility=hidden` 很重要——减少导出符号可以避免冲突

---

## 六、RELRO（重定位只读）

### 1. 三种级别

| 级别 | 编译选项 | .got | .got.plt | 符号解析 |
|---|---|---|---|---|
| No RELRO | 默认 | 可写 | 可写 | 延迟绑定 |
| Partial RELRO | `-Wl,-z,relro` | 只读 | 可写 | 延迟绑定 |
| Full RELRO | `-Wl,-z,relro,-z,now` | 只读 | 只读 | 立即绑定（eager） |

### 2. 安全意义

- GOT 是函数指针表——如果攻击者能任意写 GOT，就能控制程序流（GOT overwrite 攻击）
- Partial RELRO：.got（数据重定位）只读，但 .got.plt（函数延迟绑定）仍可写
- Full RELRO：所有符号在加载时解析（`-z,now` 等价于 `LD_BIND_NOW=1`），整个 GOT 只读
- Full RELRO 的代价：启动时解析所有符号（启动变慢），无法延迟绑定
- 几乎所有 Linux 发行版默认启用 Partial RELRO
- **来源**：HackTricks RELRO + Systems Hardening + hiraditya 分析
- **可信度**：A+

---

## 七、符号可见性（Symbol Visibility）

### 1. 三种级别

| 级别 | 行为 |
|---|---|
| `default` | 符号进入动态符号表，可被其他库引用，调用经 PLT |
| `hidden` | 符号**不**进入动态符号表，库内直接调用（无 PLT 开销） |
| `internal` | 类似 hidden，但更严格（不能从外部调用，甚至不能传指针） |

### 2. 最佳实践

```bash
# 编译时默认所有符号 hidden
gcc -fvisibility=hidden -o libfoo.so foo.c

# 只在公开 API 上显式标记 default
__attribute__((visibility("default"))) void public_api();
```

### 3. 好处

- 减少动态符号表大小（加快启动、减小二进制）
- 库内函数调用**不经 PLT**（直接 call，性能更好）
- 防止符号冲突（两个库导出同名符号）
- 防止符号劫持（攻击者无法 interpose 内部符号）

### 4. perf 诊断

> 如果 `perf report` 中看到大量 PLT 条目，说明库边界在消耗性能——用 `-fvisibility=hidden` 可以消除内部调用的 PLT 开销。

- **来源**：cfncloud 动态链接分析 + GCC 文档
- **可信度**：A

---

## 八、dlopen/dlsym（运行时动态加载）

| 函数 | 作用 |
|---|---|
| `dlopen(path, flags)` | 加载共享库，返回句柄 |
| `dlsym(handle, name)` | 查找符号地址 |
| `dlclose(handle)` | 卸载库（引用计数减 1） |
| `dlerror()` | 获取错误信息 |

- `RTLD_NOW`：立即解析所有符号（加载时）
- `RTLD_LAZY`：延迟绑定（默认）
- `RTLD_GLOBAL`：库的符号可被后续加载的库解析
- `RTLD_LOCAL`：库的符号不可见（默认）

---

## 九、知识网络

```
动态链接与加载
├── 核心问题
│   ├── 共享库代码段可共享（只读）
│   └── 加载地址未知 → 不能用绝对地址
│
├── PIC/PIE（位置无关代码）
│   ├── RIP 相对寻址（x86-64 关键）
│   ├── -fPIC（共享库）/ -fPIE（可执行文件）
│   └── 全局变量经 GOT、函数经 PLT
│
├── GOT（全局偏移表）
│   ├── .got（数据重定位）
│   ├── .got.plt（函数地址，延迟绑定）
│   └── GOT[0/1/2] 为动态链接器保留
│
├── PLT（过程链接表）
│   ├── 每个导入函数一个 stub
│   ├── 延迟绑定：第一次解析，后续直接跳转
│   └── _dl_runtime_resolve 填充 GOT
│
├── ld.so（动态加载器）
│   ├── 启动流程：自举 → 解析依赖 → 加载库 → 重定位 → 初始化
│   ├── 库搜索顺序：RPATH → LD_LIBRARY_PATH → RUNPATH → ld.so.cache → /lib
│   └── 符号解析：广度优先，第一个匹配胜出
│
├── RELRO（安全加固）
│   ├── No RELRO / Partial / Full
│   └── Full RELRO = 立即绑定 + GOT 只读
│
├── 符号可见性
│   ├── default / hidden / internal
│   ├── -fvisibility=hidden + 显式 default 标记 API
│   └── 减少 PLT 开销、防止符号冲突
│
└── dlopen/dlsym（运行时加载）
```

---

## 十、本轮最重要的 10 个资料

| # | 资料 | 级别 | 核心价值 |
|---|---|---|---|
| 1 | man7.org "Building and Using Shared Libraries on Linux" | S | 动态链接器的权威培训讲义 |
| 2 | ld.so man page | S | 库搜索顺序的权威定义 |
| 3 | Linux Foundation ELF 规范（Dynamic Linking） | S | DT_RUNPATH/DT_NEEDED 的标准定义 |
| 4 | Eli Bendersky "PIC in shared libraries on x64" | A+ | RIP 相对寻址的经典解释 |
| 5 | ashishkr.com "GOT/PLT: The Dark Art" | A+ | GOT/PLT 布局的清晰图解 |
| 6 | Oracle x64 ABI（PLT 章节） | S | x64 PLT 的官方 ABI 定义 |
| 7 | TUM 编译原理讲义（Object Files, Linker, Loader） | A | 学术视角的完整链路 |
| 8 | HackTricks RELRO | A+ | RELRO 三级别的安全对比 |
| 9 | PVS-Studio "How do exceptions work"（含动态链接） | A | 延迟绑定的逐步分析 |
| 10 | cfncloud "Linux Dynamic Linking" | A | perf 诊断 PLT 开销的实用建议 |

## 十一、强烈建议深入研究的 5 个资料

1. **man7.org 共享库培训讲义**——动态链接的完整权威教程
2. **Eli Bendersky PIC 系列**——x86-64 RIP 相对寻址的最清晰解释
3. **ld.so man page**——库搜索顺序的精确规则
4. **ashishkr.com GOT/PLT**——跟着汇编一步步走延迟绑定
5. **HackTricks RELRO**——理解安全加固的动机和效果

## 十二、适合直接进入 CPP-Bible 的资料

| 资料 | 进入方式 | 目标原子/章节 |
|---|---|---|
| GOT/PLT 延迟绑定 | "调用 printf 时到底发生了什么" | ABI/TOOL 域原子 |
| PIC/PIE 与 RIP 相对寻址 | "为什么共享库必须用 -fPIC" | ABI 域原子 |
| ld.so 搜索顺序 | "动态库是怎么被找到的" | TOOL 域原子 |
| RELRO 安全机制 | "GOT 为什么要只读" | SECURITY/TOOL 交叉 |
| 符号可见性 | "-fvisibility=hidden 为什么能加速" | PERF/TOOL 交叉 |

## 十三、对 CPP-Bible 的工程升级建议

1. **ABI 域新增"动态链接"原子**——GOT/PLT 延迟绑定 + PIC/PIE，这是理解共享库的核心
2. **TOOL 域新增"ld.so 与库搜索"原子**——RPATH/RUNPATH/LD_LIBRARY_PATH 的优先级，解决"为什么我的库找不到"
3. **PERF 域新增"PLT 开销与符号可见性"原子**——`-fvisibility=hidden` 消除内部调用 PLT 开销，含 perf 实测
4. **SECURITY 域新增"RELRO 与 GOT 保护"原子**——No/Partial/Full RELRO 的区别和安全意义
5. **构建系统建议**：项目的 CMake 可以加 `-fvisibility=hidden`（如果有公开 API 标记），减小二进制和加快启动

## 十四、发现的知识空白

1. **动态链接完全空白**——项目没有任何 GOT/PLT/PIC 相关内容
2. **ld.so 加载流程空白**——学生不知道程序启动时动态链接器做了什么
3. **符号可见性空白**——`-fvisibility=hidden` 是工业界标准实践但完全没提
4. **RELRO 安全加固空白**——安全编译选项的核心内容
5. **库搜索顺序空白**——"为什么我的库找不到"是最常见的新手问题

## 十五、下一轮推荐搜索方向

1. **ELF 文件格式深入（按顺序）**——段（section）vs 段（segment）、程序头、节头、符号表、重定位表、readelf/objdump 实战
2. **SIMD intrinsics 与手写向量化**——SSE/AVX/AVX-512/NEON、intrinsics 编程、自动向量化 vs 手写
3. **CMake 构建系统**——target 模型、generator 表达式、大型项目组织、FetchContent
4. **编译器前端**——词法/语法分析、AST、语义分析、模板两阶段查找
5. **C++ 对象模型与 ABI**——vtable、vptr、RTTI、内存布局、name mangling

---

*本轮新增知识节点：动态链接、共享库、GOT、全局偏移表、.got/.got.plt、PLT、过程链接表、延迟绑定、lazy binding、_dl_runtime_resolve、PIC、位置无关代码、PIE、RIP 相对寻址、GOTPCREL、-fPIC/-fPIE、ld.so、动态加载器、DT_NEEDED、DT_RPATH、DT_RUNPATH、LD_LIBRARY_PATH、/etc/ld.so.cache、符号解析、广度优先、RELRO、Partial RELRO、Full RELRO、-z,now、LD_BIND_NOW、符号可见性、default/hidden/internal、-fvisibility=hidden、dlopen/dlsym、RTLD_NOW/RTLD_LAZY。补齐了"动态链接与加载"域的全部核心空白——这是系统域最基础的一轮。*
