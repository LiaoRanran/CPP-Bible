# 编译可复现性深化（609 E2）

口径定位：603 已锁「同机同日两次编译一致」；本工具把口径**加深一层**（跨时间窗口/跨工具链），仍**不改** replay 本体。

## 一、跨时间窗口 12 宏（每条都有归类，不靠「看心情」）

| 宏 | 类别 | 跨窗口必须屏蔽 | 理由 |
|---|---|---|---|
| `__DATE__` | time | **是** | 编译日期字符串 ⇒ 隔天必然不同 |
| `__TIME__` | time | **是** | 编译时刻字符串 ⇒ 秒级必然不同 |
| `__TIMESTAMP__` | time | **是** | 源文件 mtime 字符串 ⇒ 触盘时间变即变 |
| `__FILE__` | path | **是** | 内含路径 ⇒ 不同工作目录/前缀必不同 |
| `__BASE_FILE__` | path | **是** | 主源文件名 ⇒ 同上 |
| `__FILE_NAME__` | path | 否 | 只含文件名（无目录）⇒ 同仓同文件可复现 |
| `__LINE__` | counter | 否 | 行号由源码决定 ⇒ 同源码同值 |
| `__func__` | counter | 否 | 函数名由源码决定 ⇒ 同源码同值 |
| `__INCLUDE_LEVEL__` | counter | 否 | 包含深度由源码结构决定 |
| `__COUNTER__` | counter | 否 | 同 TU 内递增 ⇒ 同源码同展开顺序即同值 |
| `__STDC_VERSION__` | env | **是** | 随标准版本/编译器变 ⇒ 跨工具链必不同 |
| `__GNUC__` | env | **是** | 随 GCC 主版本变 ⇒ 换工具链必不同 |

- 必须屏蔽：**7/12**（env 2 + path 2 + time 3）

## 二、符号表口径（nm 4 参数）

- `nm --defined-only` —— 只列本 TU 定义的符号；未定义符号（外部引用）随链接环境变 ⇒ 不比它
- `nm --extern-only` —— 只列外部可见符号；静态局部符号名可被优化器重命名 ⇒ 噪声源
- `nm -P` —— portable 输出格式（name type value）；BSD/SysV 三种格式在同一平台都可能出现 ⇒ 必须钉格式
- `nm --no-demangle` —— **不做** C++ 名字还原；demangle 结果随 libiberty 版本变 ⇒ 比 mangled 名更稳

## 三、段一致性口径（objdump 4 参数）

- `objdump -h` —— 只列段头（名/大小/对齐/标志）；比**长度与对齐**：段内容可因时间戳变而头部不变
- `objdump -s` —— 倾印段内容（hex）；比**逐字节**：对 .text/.rodata 等语义段使用
- `objdump -j <段名>` —— 限定单个段；避免把 .comment/.note 等**工具版本印记**段卷进比对
- `objdump --no-show-raw-insn` —— 反汇编不带机器码；避免反汇编器版本差异伪装成语义差异

- **只比长度**的段：`.comment`, `.note.gnu.build-id`, `.note.GNU-stack`, `.debug_info`（工具链会插版本串/构建 id ⇒ 逐字节比必假红）

## 四、diffoscope 替代品

- 仓里不引 diffoscope（依赖重、要外部工具）⇒ 自带 `diff` 子命令：
  首个差异偏移 + 双侧 sha256 + 差异字节数 + 两侧 hex 上下文；
- 定位：**给失败现场用**（谁在哪个字节上变了），不给「全量二进制 diff」能力。

## 五、PE 时间戳口径（611 A3 · 610 E3 实测结论正式化）

> 为什么单列一节：603 锁的是「同机同日两次编译一致」。**对 PE 可执行产物，这句话只在「同一秒内」成立** —— 跨秒必变 2 字节。不写清楚，跨窗口复现测试就会把「时间戳漂移」误判成「内容不可复现」。

| 事实 | 值 / 说明 |
|---|---|
| 新状态名 | `time_window_drift`（与 `ok`/`not_reproducible`/`tampered` 并列，由 `atom_evidence_replay._recompile_invariant_extended` 给出） |
| PE 头时间戳偏移 | `0x88`（= e_lfanew 0x80 + 8，PE/COFF `TimeDateStamp`，32 位） |
| 第二处同族偏移 | `0xd8`（debug 目录里与编译时刻同源的字段；两侧值正好相差 1 秒） |
| 跨时间窗口差异量 | **2 字节**（仅上述两处；长度相同、其余字节逐字节一致） |
| 语义维度 | `nm` 符号表 / `objdump` 段 / `strings` 字符串表**全一致**（差异不触达语义） |
| 取证方法 | 加 `-Wl,--no-insert-timestamp` 再编一对（同样跨 1.1s）⇒ **字节一致**；记 `timestamp_proof=no_insert_timestamp_pair_identical` |
| 可复现配方 | 链接加 `-Wl,--no-insert-timestamp`，或设 `SOURCE_DATE_EPOCH`（实测该开关有效） |
| 本仓影响面 | 56 张证据卡的 `artifact` **全部是 `.asm`**（`g++ -S` 线）⇒ 不受该漂移影响；PE 漂移只在**可执行产物**上出现 |
| 结论（诚实版） | 「同机同日两次编译一致」对 **PE 产物只在「同一秒内」成立**；跨时间窗口必变 2 字节。本批**不改** 603 既有口径、不重冻结，只**显形**并给配方 |

**判读规则（写给复核者）**：

- `sha` 跨窗口**一致** ⇒ `ok`（本仓 56 张卡就是这一档）；
- `sha` 跨窗口**不同**但 `nm`/`objdump`/`strings` **全一致**、且差异只落在 PE 时间戳两处 ⇒ `time_window_drift`（**不是**不可复现，是「秒表在走」）；
- 上述之外（差异触达语义维度、或差异字节不在时间戳内、或加了 `--no-insert-timestamp` 仍不同）⇒ `not_reproducible`（**真问题**，须查工具链/环境）；
- 卡值比对失败（`want_sha` 不符）⇒ `tampered`（与时间窗口无关的另一条路）。

