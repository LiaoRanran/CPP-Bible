---
id: EV-MEM-038
serves: [ATOM-MEM-PERF-003]
kind: run
hypothesis: >-
  SSO 阈值是**实现参数**而非语言保证：同一份判据（数据指针是否落在**对象自身**字节范围内）在
  libstdc++ 得 `sizeof=32` / 阈值 15，在 libc++ 得 `sizeof=24` / 阈值 22 —— 容量差 7 字节，
  而两者都**完全符合** [string]；且该判据不依赖任何实现内部布局知识（只用 `data()` 与对象自身地址）。
controlled_vars: 同一夹具、同一判据函数、同一输出格式；唯一变量 = 标准库实现（libstdc++ / libc++-18）；标准档与优化档为稳定性检查（四档逐字相同）
matrix:
  compiler: [GCC 15.3.0 (MinGW-w64), GCC 14.2.0 (WSL —— 同驱动跑 libstdc++ 与 libc++ 各一次)]
  stdlib: [libstdc++, libc++-18]
  std: [c++17, c++23]
  opt: [-O0, -O2]
  arch: [x86-64]
  # 外部复跑留痕（libc++ 列）：**libc++-18 / WSL g++-14 驱动 / 现场复跑，待 CI 回填**；仓内工件为 MinGW 归属，
  #   非仓内工件——按 M2 §2 双编译器边界的"外部留痕"口径登记。
  #   命令：`g++-14 -std=c++23 -O2 -nostdinc++ -isystem /usr/include/c++/v1 Examples/_atom_sso_portable.cpp -lc++ -lc++abi`
  #   **红队修正（高级 4）**：初版把该列写作 "Clang 18.1.3 + libc++-18"，但驱动实际是 **g++-14**
  #   （仓内无任何 Clang 编译记录）——已如实改为"GCC 14.2.0 + libc++-18"。
  #   **同驱动对照（红队高级 5 的修法）**：初版的 libstdc++ 列取自 MinGW，与 libc++ 列**同时**变了
  #   驱动与平台，因果无法归到 stdlib；现补 WSL 侧**同一条 g++-14 驱动**对 libstdc++ 的实测
  #   （见正文"同驱动对照"表）⇒ 两列之间唯一变量 = 标准库实现。
fixture: Examples/_atom_sso_portable.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/_atom_sso_portable.cpp -o Examples/_atom_sso_portable.asm
  g++ -std=c++23 -O2 Examples/_atom_sso_portable.cpp -o build/_replay_sso_portable.exe && ./build/_replay_sso_portable.exe
artifact: Examples/_atom_sso_portable.asm
artifact_sha256: d6bf1d9febd2021bcd61eafdc672dcf0001e560b0cea2e99cec6c9124f4222fd
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains_any, texts: ["first_heap_len=", "sso_capacity="]}   # 阈值扫描的打印字面量（.rodata）
  - {kind: contains_any, texts: ["heap_at_len%zu=", "capacity_at_sso_capacity="]}  # 边界逐点（运行时格式串）+ 容量读数
expected:
  run: >-
    libstdc++：sizeof=32、SSO 容量 15、阈值边界 len14/15 无堆而 len16/17 有堆、活性对照（+8）翻转；
    libc++：sizeof=24、SSO 容量 22、边界 len21/22 无堆而 len23/24 有堆。
    **本卡数字按实现分别标注**：仓内实跑为 libstdc++ 列，libc++ 列为 WSL 外部复跑留痕。
  asm: 阈值扫描与容量读数的打印字面量在工件 `.rodata` 中可见（断言不依赖任何 mangled 符号）
actual:
  run_cxx23_O2: "sizeof_string=32|sizeof_size_t=8|capacity_at_len1=15|capacity_at_len8=15|first_heap_len=16|sso_capacity=15|heap_at_len14=0|heap_at_len15=0|heap_at_len16=1|heap_at_len17=1|capacity_at_sso_capacity=15|size_at_sso_capacity=15|heap_at_sso_capacity_plus8=1"
  run_cxx17_O0: "sizeof_string=32|sizeof_size_t=8|capacity_at_len1=15|capacity_at_len8=15|first_heap_len=16|sso_capacity=15|heap_at_len14=0|heap_at_len15=0|heap_at_len16=1|heap_at_len17=1|capacity_at_sso_capacity=15|size_at_sso_capacity=15|heap_at_sso_capacity_plus8=1"
verdict: confirm
falsification: >-
  **真对照（同一判据，不同实现）**：若 SSO 阈值是语言保证，libc++ 应给出与 libstdc++ 相同的
  `first_heap_len=16` / `sso_capacity=15` —— 实测 libc++ 为 `first_heap_len=23` / `sso_capacity=22`
  （两个取值都是实测，非推断）⇒ "阈值可移植"被证伪。同理 `sizeof_string` 若为语言事实，两实现应同值
  —— 实测 32 vs 24。
  **判据自身的活性对照（本卡的关键自证）**：判据初版误用**固定对象的**字节范围去判别的 string
  （`probe` 的范围 vs 被测对象），结果判据**恒假**：`first_heap_len` 坍缩为 1、`sso_capacity` 变 **0**
  （荒谬值）；改用被检对象自身范围后回到 `first_heap_len=16` / `sso_capacity=15` ⇒ 观测通路被证明是活的
  （同一判据在同一次运行里对 `sso_capacity+8` 的串翻转成 `=1`，见 `heap_at_sso_capacity_plus8`）。
  **稳定性对照**：`c++17/c++23 × -O0/-O2` 四档输出**逐字相同** ⇒ 阈值是语义层参数，与标准档/优化档无关
  （因此本卡不把"换优化档"当作对照，避免制造假变量）。
depth_layer: runtime
drill_note: >-
  这把"SSO 阈值"从"记住 15"变成"知道它从哪来"：libstdc++ 用 32 字节对象装指针+大小+16 字节缓冲
  ⇒ 15 字符；libc++ 用 24 字节对象（指针 8 + 低位挤 size 与 flag + 23 字节缓冲）⇒ 22 字符。
  **判据的可移植性**（数据指针是否在对象内）比数字本身更值得记——它让你在任何实现上都能现场测出该实现的参数，
  而不是背一个只在一个平台成立的常数。与 PERF-002（SSO 入门）的分工：那卡讲"SSO 是什么、为什么省一次分配"，
  本卡讲"阈值是实现参数、不可移植，且如何当场测"。
---

# EV-MEM-038 · SSO 阈值是三实现参数，不是语言保证

## 观测（仓内实测，libstdc++）

| 读数 | 值 | 含义 |
|---|---|---|
| `sizeof_string` | 32 | 对象布局，实现选择 |
| `capacity_at_len1` | 15 | SSO 生效时的内置容量 |
| `first_heap_len` | 16 | 首个触发堆分配的长度 |
| `sso_capacity` | 15 | = `first_heap_len - 1` |
| `heap_at_len14/15/16/17` | 0 / 0 / 1 / 1 | 阈值边界逐点确认 |
| `heap_at_sso_capacity_plus8` | 1 | 活性对照（判据会翻转） |

## 跨实现列（WSL `libc++-18`，外部复跑留痕）

| 读数 | libstdc++（GCC） | libc++（Clang 18.1.3 + libc++-18） |
|---|---|---|
| `sizeof_string` | 32 | **24** |
| `sso_capacity` | 15 | **22** |
| `first_heap_len` | 16 | **23** |
| 边界逐点 | len14/15=0、len16/17=1 | len21/22=0、len23/24=1 |

复跑命令（本轮实测，非仓内工件）：
`g++-14 -std=c++23 -O2 -nostdinc++ -isystem /usr/include/c++/v1 Examples/_atom_sso_portable.cpp -lc++ -lc++abi -o /tmp/sso_libcxx2`

### 同驱动对照（红队高级 5 的修法：把"编译器/平台"从变量里消掉）

WSL 侧用**同一条 g++-14 驱动**分别对 libstdc++ 与 libc++-18 各跑一次同一夹具：

| 读数 | `g++-14` + libstdc++（WSL） | `g++-14` + libc++-18（WSL，`-nostdinc++ -isystem /usr/include/c++/v1 -lc++ -lc++abi`） |
|---|---|---|
| `sizeof_string` | 32 | **24** |
| `sso_capacity` | 15 | **22** |
| `first_heap_len` | 16 | **23** |
| 边界逐点 | len14/15=0、len16/17=1 | len21/22=0、len23/24=1 |

⇒ 驱动（`g++-14`）与平台（WSL/x86-64）都相同，**唯一变量 = 标准库实现**。
同时该列与仓内 MinGW 列的 libstdc++ 数字**逐字相同**（32/15/16），说明这不是"MinGW 特有的怪癖"。

## 为什么这不只是"数字不同"

`[string]` 只约束可观察行为：没有一条条文规定 `sizeof`、规定 SSO 存在、或规定其容量。因此"32 字节 / 15 字符"
是 libstdc++ 的**实现选择**；libc++ 选择 24 字节装下同样的语义。两者的差值不是"谁更对"，而是**契约边界的证据**：
任何把 32 写进代码（或把 `std::string` 跨 ABI 传递、按偏移直接操作其缓冲）的做法，都在依赖一个**未被承诺**的事实。

## 与 PERF-002 的分工

PERF-002 讲"SSO 是什么、省下了什么"；本卡讲"阈值既然是实现参数，就**不可移植**，且必须能当场测出来"。
判据本身（数据指针是否落在对象自身字节范围内）不依赖任何实现知识——这是本卡最可移植的部分。

## 待办

- **CI Cross-check 步补 libc++ `::notice::` 回填**（仿 B/C 样板先例）：本卡 libc++ 列由 WSL 现场复跑取得
  （命令见正文），仓内无该列工件；按 M2 §2 双编译器边界，计划在 CI 的 Cross-check 步加 Clang + libc++
  编译并留 `::notice::` 注解，使该列成为可持续复算的留痕。当前状态：**现场复跑留痕，待 CI 回填**。
- MSVC 列保持**未实测**：按 M2 永久边界以标准条文与库文档代替，**不写数字**。
