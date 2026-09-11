# 资料研究第十八轮：ELF 文件格式深入——Header、Section/Segment、符号表与重定位

> 2026-09-11，底层工程资料研究员。主题：ELF（Executable and Linkable Format）文件格式的完整结构（ELF header、program header vs section header、常见 section、符号表、重定位表）+ x86-64 重定位类型详解 + readelf/objdump 实战。
> 检索方式：general_search + Linux Foundation ELF 规范 1.2 + Linux kernel elf.h + Oracle x64 ABI + Qualcomm x86-64 重定位参考 + TUM 编译原理讲义。
> **系统域第二轮**（上一轮动态链接，本轮 ELF 格式深入，直接衔接）。

---

## 一、ELF 文件整体结构

```
┌─────────────────────────┐
│   ELF Header (64B)      │  ← 固定在文件偏移 0
├─────────────────────────┤
│  Program Header Table   │  ← 段表（运行时视图，可执行文件必需）
│  (PT_LOAD, PT_DYNAMIC…) │
├─────────────────────────┤
│                         │
│       Sections          │  ← 节（链接视图，.text/.data/.bss…）
│    (.text, .data, …)    │
│                         │
├─────────────────────────┤
│  Section Header Table   │  ← 节表（链接时必需，可执行文件可 strip）
└─────────────────────────┘
```

- **来源**：Linux Foundation ELF 规范 1.2 + elf(5) man page
- **可信度**：S

---

## 二、Section vs Segment（节 vs 段）——最容易混淆的概念

| 维度 | Section（节） | Segment（段） |
|---|---|---|
| 视图 | 链接视图（编译/链接/调试） | 运行时视图（加载器映射内存） |
| 描述者 | Section Header Table | Program Header Table |
| 数量 | 多（几十上百个） | 少（通常 5-10 个） |
| 代表 | .text, .data, .bss, .symtab, .rela.text | PT_LOAD, PT_DYNAMIC, PT_INTERP |
| 可执行文件 | 可 strip（删除不影响运行） | 必需（加载器需要） |
| 关系 | 一个 segment 包含多个 section | 多个 section 合并成一个 segment |

> **关键洞察**：加载器只看 segment（PT_LOAD 决定哪些内容映射到内存、什么权限），不看 section。Section 是给链接器和调试器用的。

- **来源**：LinuxVox "Section vs Segment" + HandWiki ELF
- **可信度**：S

---

## 三、ELF Header（64 字节）

### 关键字段

| 字段 | 含义 | 示例值 |
|---|---|---|
| e_ident[0:4] | 魔数 | 0x7F 'E' 'L' 'F' |
| e_ident[4] | 类别 | 2 = 64 位（ELFCLASS64） |
| e_ident[5] | 字节序 | 1 = 小端（ELFDATA2LSB） |
| e_type | 文件类型 | ET_REL(.o) / ET_EXEC / ET_DYN(.so/PIE) |
| e_machine | 架构 | 62 = EM_X86_64 |
| e_entry | 入口点 | 程序起始虚拟地址 |
| e_phoff | Program header 偏移 | 文件内偏移 |
| e_shoff | Section header 偏移 | 文件内偏移 |
| e_phnum | Program header 数量 | 通常 8-12 |
| e_shnum | Section header 数量 | 通常 20-40 |
| e_shstrndx | 节名字符串表索引 | 用于解析节名 |

### e_type 的三种值

| 值 | 含义 | 例子 |
|---|---|---|
| ET_REL | 可重定位文件 | .o（编译中间产物） |
| ET_EXEC | 可执行文件（固定地址） | 非 PIE 的可执行文件 |
| ET_DYN | 共享库 / PIE 可执行文件 | .so、现代 Linux 默认可执行文件 |

> 注意：现代 Linux 发行版默认生成 PIE（Position Independent Executable），所以可执行文件的 e_type 也是 ET_DYN——和共享库一样！区别只在于是否有 PT_INTERP 和入口点。

- **来源**：Linux kernel include/uapi/linux/elf.h + elf(5) man page
- **可信度**：S

---

## 四、Program Header（段头）

### 常见类型

| 类型 | 作用 |
|---|---|
| PT_LOAD | 加载到内存的段（最重要，Flags 决定权限 R/RE/RW） |
| PT_INTERP | 动态链接器路径（/lib64/ld-linux-x86-64.so.2） |
| PT_DYNAMIC | 动态链接信息（.dynamic 段） |
| PT_NOTE | 辅助信息（build ID、OS ABI） |
| PT_GNU_STACK | 栈权限（NX 位，通常 RW 不可执行） |
| PT_GNU_RELRO | RELRO 信息 |
| PT_TLS | 线程局部存储 |

### PT_LOAD 的权限与内容

| Flags | 权限 | 典型内容 |
|---|---|---|
| R | 只读 | ELF headers、.rodata、.eh_frame |
| R E | 读+执行 | .text、.plt、.init、.fini |
| R W | 读+写 | .data、.bss、.got、.got.plt |

- **来源**：NDXDeveloper readelf/objdump 教程 + LinuxVox
- **可信度**：A

---

## 五、常见 Section（节）

| Section | 类型 | 权限 | 内容 |
|---|---|---|---|
| .text | SHT_PROGBITS | R-E | 机器代码 |
| .data | SHT_PROGBITS | RW- | 已初始化全局变量 |
| .bss | SHT_NOBITS | RW- | 未初始化全局变量（不占文件空间） |
| .rodata | SHT_PROGBITS | R-- | 只读数据（字符串常量） |
| .plt | SHT_PROGBITS | R-E | 过程链接表（函数跳板） |
| .got | SHT_PROGBITS | RW- | 全局偏移表（数据地址） |
| .got.plt | SHT_PROGBITS | RW- | 全局偏移表（函数地址，延迟绑定） |
| .symtab | SHT_SYMTAB | --- | 静态符号表（可 strip） |
| .dynsym | SHT_DYNSYM | R-- | 动态符号表（运行时必需） |
| .strtab | SHT_STRTAB | --- | 静态字符串表 |
| .dynstr | SHT_STRTAB | R-- | 动态字符串表 |
| .rela.text | SHT_RELA | --- | .text 的重定位表 |
| .rela.dyn | SHT_RELA | R-- | 动态重定位（数据） |
| .rela.plt | SHT_RELA | R-- | PLT 重定位（函数） |
| .dynamic | SHT_DYNAMIC | RW- | 动态链接信息（DT_NEEDED 等） |
| .eh_frame | SHT_PROGBITS | R-- | 异常展开信息（DWARF CFI） |
| .comment | SHT_PROGBITS | R-- | 编译器版本字符串 |
| .note.gnu.build-id | SHT_NOTE | R-- | 构建 ID（唯一标识二进制） |

- **来源**：Linux Foundation ELF 规范 + dev.to ELF 分析
- **可信度**：S

---

## 六、符号表（Symbol Table）

### Elf64_Sym 结构（24 字节）

```c
typedef struct {
    Elf64_Word    st_name;   // 符号名在字符串表中的索引
    unsigned char st_info;   // 高4位=binding，低4位=type
    unsigned char st_other;  // 可见性（低2位）
    Elf64_Section st_shndx;  // 所属节索引
    Elf64_Addr    st_value;  // 符号值（地址或偏移）
    Elf64_Xword   st_size;   // 符号大小（字节）
} Elf64_Sym;
```

### st_info 解析

```
binding = st_info >> 4    // 高 4 位
type    = st_info & 0xf   // 低 4 位
```

| Binding | 值 | 含义 |
|---|---|---|
| STB_LOCAL | 0 | 局部符号（静态函数/变量） |
| STB_GLOBAL | 1 | 全局符号（可被其他模块引用） |
| STB_WEAK | 2 | 弱符号（可被强符号覆盖） |

| Type | 值 | 含义 |
|---|---|---|
| STT_NOTYPE | 0 | 类型未定义 |
| STT_OBJECT | 1 | 数据对象（变量） |
| STT_FUNC | 2 | 函数 |
| STT_SECTION | 3 | 节（重定位用） |
| STT_FILE | 4 | 源文件名 |

### st_other 可见性

| Visibility | 值 | 含义 |
|---|---|---|
| STV_DEFAULT | 0 | 默认（可被其他库引用） |
| STV_INTERNAL | 1 | 内部（不能从外部调用） |
| STV_HIDDEN | 2 | 隐藏（不进入动态符号表） |
| STV_PROTECTED | 3 | 保护（可引用但不能被 interpose） |

### .symtab vs .dynsym

| 维度 | .symtab | .dynsym |
|---|---|---|
| 内容 | 所有符号（含局部） | 只含动态链接需要的符号 |
| 运行时需要 | 否（可 strip） | 是 |
| 大小 | 大 | 小 |
| 用途 | 调试、静态链接 | 动态链接、运行时符号解析 |

- **来源**：Oracle 符号表文档 + Linux kernel elf.h + TUM 讲义
- **可信度**：S

---

## 七、重定位（Relocation）

### 1. 为什么需要重定位？

编译 .o 文件时，外部符号（函数/全局变量）的地址未知——编译器留下"占位符"，并记录重定位条目。链接器（静态/动态）在链接时/加载时填充真实地址。

### 2. Elf64_Rela 结构

```c
typedef struct {
    Elf64_Addr  r_offset;  // 要修改的位置（文件偏移或虚拟地址）
    Elf64_Xword r_info;    // 高32位=符号索引，低32位=重定位类型
    Elf64_Sxword r_addend; // 加数（A）
} Elf64_Rela;
```

### 3. 常见 x86-64 重定位类型

| 类型 | 值 | 字段 | 计算公式 | 用途 |
|---|---|---|---|---|
| R_X86_64_64 | 1 | word64 | S + A | 绝对 64 位地址（非 PIC 数据） |
| R_X86_64_PC32 | 2 | word32 | S + A - P | PC 相对 32 位（内部函数调用） |
| R_X86_64_GOT32 | 3 | word32 | G + A | GOT 偏移（x86-32 用） |
| R_X86_64_PLT32 | 4 | word32 | L + A - P | PLT 相对（外部函数调用） |
| R_X86_64_COPY | 5 | word64 | 复制 | 复制重定位（共享库全局变量） |
| R_X86_64_GLOB_DAT | 6 | word64 | S | GOT 条目（数据，加载时填充） |
| R_X86_64_JUMP_SLOT | 7 | word64 | S | GOT 条目（函数，延迟绑定） |
| R_X86_64_RELATIVE | 8 | word64 | B + A | 基址相对（PIC 内部引用） |
| R_X86_64_GOTPCREL | 9 | word32 | G + GOT + A - P | GOT 条目地址（PIC 数据访问） |
| R_X86_64_32 | 10 | word32 | S + A | 绝对 32 位（非 PIC，共享库禁用） |

### 4. 符号含义

| 符号 | 含义 |
|---|---|
| S | 符号的最终地址 |
| A | 加数（r_addend） |
| P | 重定位位置的地址（被修改处） |
| G | 符号在 GOT 中的偏移 |
| GOT | GOT 本身的地址 |
| L | 符号的 PLT 条目地址 |
| B | 共享库的加载基址 |

### 5. Copy Relocation（复制重定位）

- 可执行文件引用共享库的全局变量时，静态链接器在可执行文件的 .bss 中预留空间
- 运行时动态链接器把共享库中的变量值**复制**到可执行文件中
- 结果：变量有两份副本（共享库一份、可执行文件一份），可执行文件直接访问自己的副本（不经 GOT）
- 这是为什么共享库的全局变量应该尽量避免——复制重定位导致多份副本
- **来源**：BSDCan 2025 "ELF Nightmares" + Oracle x64 ABI
- **可信度**：A+

---

## 八、readelf / objdump 实战命令

### readelf（ELF 专用，输出更清晰）

| 命令 | 作用 |
|---|---|
| `readelf -h binary` | ELF header（类型、架构、入口点） |
| `readelf -S binary` | Section headers（节列表、权限、大小） |
| `readelf -l binary` | Program headers（段列表、内存映射、权限） |
| `readelf -s binary` | 符号表（.symtab） |
| `readelf --dyn-syms binary` | 动态符号表（.dynsym） |
| `readelf -d binary` | .dynamic 段（依赖库 DT_NEEDED） |
| `readelf -r binary` | 重定位条目 |
| `readelf -n binary` | Notes（build ID） |
| `readelf -e binary` | 全部 header（= -h -l -S） |
| `readelf -a binary` | 全部信息 |

### objdump（更通用，支持反汇编）

| 命令 | 作用 |
|---|---|
| `objdump -d binary` | 反汇编（.text 等可执行节） |
| `objdump -S binary` | 源码+反汇编（需 -g 编译） |
| `objdump -t binary` | 符号表 |
| `objdump -T binary` | 动态符号表 |
| `objdump -r binary` | 重定位（.o 文件） |
| `objdump -R binary` | 动态重定位 |
| `objdump -x binary` | 全部 header 信息 |
| `objdump -s -j .text binary` | 查看指定节的十六进制内容 |

### 其他工具

| 命令 | 作用 |
|---|---|
| `nm binary` | 符号表（简洁，U=未定义/T=文本/D=数据） |
| `file binary` | 文件类型（是否 stripped、PIE、架构） |
| `ldd binary` | 动态库依赖 |
| `size binary` | 各节大小（text/data/bss） |
| `strings binary` | 可打印字符串 |

### 典型分析流程

```bash
# 1. 看文件类型
file hello

# 2. 看 ELF header
readelf -h hello

# 3. 看依赖库
readelf -d hello | grep NEEDED
ldd hello

# 4. 看段（加载视图）
readelf -l hello

# 5. 看节（链接视图）
readelf -S hello

# 6. 看符号
readelf -s hello | grep printf
nm hello | grep printf

# 7. 看重定位
readelf -r hello

# 8. 反汇编
objdump -d hello | less
objdump -S hello | less   # 带源码
```

- **来源**：sourceware readelf 文档 + NDXDeveloper 教程 + cppcheatsheet
- **可信度**：S

---

## 九、知识网络

```
ELF 文件格式
├── 整体结构
│   ├── ELF Header（64B，偏移0）
│   ├── Program Header Table（段表，运行时视图）
│   ├── Sections（节，链接视图）
│   └── Section Header Table（节表，可 strip）
│
├── Section vs Segment
│   ├── Section：链接视图，.text/.data/.bss
│   ├── Segment：运行时视图，PT_LOAD/PT_DYNAMIC
│   └── 一个 segment 包含多个 section
│
├── ELF Header
│   ├── e_type：ET_REL / ET_EXEC / ET_DYN
│   ├── e_machine：EM_X86_64
│   └── e_entry：入口点
│
├── Program Header
│   ├── PT_LOAD（R/RE/RW 权限）
│   ├── PT_INTERP（动态链接器路径）
│   ├── PT_DYNAMIC（动态链接信息）
│   └── PT_GNU_STACK / PT_GNU_RELRO
│
├── 常见 Section
│   ├── .text / .data / .bss / .rodata
│   ├── .plt / .got / .got.plt
│   ├── .symtab / .dynsym / .strtab / .dynstr
│   ├── .rela.text / .rela.dyn / .rela.plt
│   ├── .dynamic / .eh_frame / .comment
│   └── .note.gnu.build-id
│
├── 符号表
│   ├── Elf64_Sym（24B）
│   ├── binding：LOCAL/GLOBAL/WEAK
│   ├── type：NOTYPE/OBJECT/FUNC/SECTION
│   ├── visibility：DEFAULT/HIDDEN/PROTECTED
│   └── .symtab（全量）vs .dynsym（动态）
│
├── 重定位
│   ├── Elf64_Rela（offset/info/addend）
│   ├── R_X86_64_64 / PC32 / PLT32 / GOTPCREL
│   ├── R_X86_64_GLOB_DAT / JUMP_SLOT / RELATIVE
│   └── Copy Relocation（共享库全局变量）
│
└── 工具
    ├── readelf（-h/-S/-l/-s/-d/-r/-n）
    ├── objdump（-d/-S/-t/-r/-x）
    └── nm / file / ldd / size / strings
```

---

## 十、本轮最重要的 10 个资料

| # | 资料 | 级别 | 核心价值 |
|---|---|---|---|
| 1 | Linux Foundation ELF 规范 1.2 | S | ELF 格式的权威定义 |
| 2 | Linux kernel include/uapi/linux/elf.h | S | Elf64_Sym/Elf64_Rela 的真实 C 结构 |
| 3 | Oracle x64 ABI（重定位类型） | S | x86-64 重定位类型的官方定义 |
| 4 | Qualcomm x86-64 Relocation Reference | A+ | 重定位计算公式的完整表格 |
| 5 | elf(5) man page | S | ELF 格式的权威手册 |
| 6 | TUM 编译原理讲义（Object Files, Linker, Loader） | A | 学术视角的完整链路 |
| 7 | NDXDeveloper readelf/objdump 教程 | A | 实战命令的清晰总结 |
| 8 | BSDCan 2025 "ELF Nightmares" | A+ | Copy Relocation 等高级话题 |
| 9 | LinuxVox "Section vs Segment" | A | 最易混淆概念的清晰对比 |
| 10 | sourceware readelf 文档 | S | readelf 所有选项的权威说明 |

## 十一、强烈建议深入研究的 5 个资料

1. **Linux Foundation ELF 规范 1.2**——ELF 格式的原始定义
2. **Linux kernel elf.h**——读真实的 C 结构定义
3. **Oracle x64 ABI 重定位章节**——理解每种重定位的计算公式
4. **NDXDeveloper readelf/objdump 教程**——跟着命令一步步分析真实二进制
5. **BSDCan 2025 "ELF Nightmares"**——Copy Relocation、GOT/PLT 的高级理解

## 十二、适合直接进入 CPP-Bible 的资料

| 资料 | 进入方式 | 目标原子/章节 |
|---|---|---|
| ELF 整体结构 | "一个可执行文件里到底有什么" | ABI/TOOL 域原子 |
| Section vs Segment | "节和段有什么区别" | ABI 域原子（最易混淆） |
| 符号表结构 | "nm 输出的每一列是什么意思" | TOOL 域原子 |
| 重定位类型 | "编译器留下的占位符怎么被填充" | ABI 域原子 |
| readelf/objdump 实战 | "5 个命令看懂一个二进制" | TOOL 域专题 |

## 十三、对 CPP-Bible 的工程升级建议

1. **TOOL 域新增"ELF 文件格式"原子**——ELF header + section/segment + 符号表 + 重定位，这是理解编译/链接/加载的基础
2. **TOOL 域新增"readelf/objdump 实战"专题**——5 个命令看懂二进制，含真实输出示例
3. **ABI 域新增"重定位类型"原子**——R_X86_64_PC32/GOTPCREL/PLT32/RELATIVE 的计算公式和用途
4. **证据卡新增"二进制分析"字段**——性能类证据卡附 `readelf -l`/`objdump -d` 输出，证明加载布局和汇编
5. **教学建议**：ELF 格式是"编译→汇编→链接→加载"全链路的交汇点，建议放在编译器域和系统域之间作为桥梁

## 十四、发现的知识空白

1. **ELF 文件格式完全空白**——项目没有任何 ELF 相关内容
2. **Section vs Segment 空白**——最易混淆的概念完全没讲
3. **重定位类型空白**——R_X86_64_* 系列是理解 PIC/PLT/GOT 的基础
4. **readelf/objdump 实战空白**——学生不知道怎么分析二进制
5. **符号表结构空白**——nm 输出的列含义、binding/type/visibility

## 十五、下一轮推荐搜索方向

1. **静态链接与链接器（按顺序）**——ld 的工作原理、符号解析、COMMON 块、链接脚本、ar 归档、静态库链接顺序
2. **SIMD intrinsics 与手写向量化**——SSE/AVX/AVX-512/NEON、intrinsics 编程
3. **CMake 构建系统**——target 模型、generator 表达式、大型项目组织
4. **编译器前端**——词法/语法分析、AST、语义分析、模板两阶段查找
5. **C++ 对象模型与 ABI**——vtable、vptr、RTTI、内存布局、name mangling

---

*本轮新增知识节点：ELF、Executable and Linkable Format、ELF header、e_ident、e_type、ET_REL、ET_EXEC、ET_DYN、e_machine、e_entry、program header、section header、segment、section、PT_LOAD、PT_INTERP、PT_DYNAMIC、PT_GNU_STACK、PT_GNU_RELRO、.text、.data、.bss、.rodata、.plt、.got、.got.plt、.symtab、.dynsym、.strtab、.dynstr、.rela.text、.rela.dyn、.rela.plt、.dynamic、.eh_frame、.note.gnu.build-id、SHT_PROGBITS、SHT_NOBITS、SHT_SYMTAB、SHT_DYNSYM、SHT_RELA、Elf64_Sym、st_name、st_info、st_other、st_shndx、st_value、st_size、STB_LOCAL/GLOBAL/WEAK、STT_NOTYPE/OBJECT/FUNC/SECTION、STV_DEFAULT/HIDDEN/PROTECTED、Elf64_Rela、r_offset、r_info、r_addend、R_X86_64_64、R_X86_64_PC32、R_X86_64_PLT32、R_X86_64_GOTPCREL、R_X86_64_GLOB_DAT、R_X86_64_JUMP_SLOT、R_X86_64_RELATIVE、R_X86_64_COPY、Copy Relocation、readelf、objdump、nm、ldd、size、strings。补齐了"ELF 文件格式"域的全部核心空白——这是编译→链接→加载全链路的基础一轮。*
