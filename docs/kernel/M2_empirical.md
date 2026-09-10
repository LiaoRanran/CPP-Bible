# G2.1 实证方法 M2（Empirical Method）

> 本文所有规则都由**真实跑出来的事故**反向固化，不是纸面设计。每节末尾标了来源事故。

## 1. 实验卡（字段化，写进 `evidence/{domain}/EV-*.md`）

| 字段 | 必填 | 说明 |
|---|---|---|
| `id` | ✅ | `EV-{DOMAIN}-{NNN}` |
| `serves` | ✅ | 服务哪些原子（多对多） |
| `hypothesis` | ✅ | 待检验断言（可直接抄原子的 `claim`） |
| `controlled_vars` | ✅ | **唯一变量**是什么，其余如何固定 |
| `matrix` | ✅ | `{compiler, version, std, opt, arch, sanitizer, config}` |
| `fixture` | ✅ | 夹具路径（自包含，可一键复现） |
| `command` | ✅ | 完整复现命令（含编译与运行） |
| `expected` | ✅ | 预期观测值（**数值/符号级**，不要"应该能跑"） |
| `actual` | ✅ | 实测值（**留空即伪证据**） |
| `verdict` | ✅ | `confirm` / `refute` / `partial` |
| `falsification` | ✅ | **让它失败的对照实验**及其结果 |
| `depth_layer` | ✅ | 本证据钻到 6 层中的哪层 |
| `artifact` / `artifact_sha256` | ✅ | 产物路径与内容哈希（可复算比对） |
| `artifact_compiler` | ✅ | **该哈希归属的编译器**（如 `GCC 15.3.0 (MinGW-w64)`）；跨编译器/跨平台字节不同，须声明 |
| `artifact_assert[]` | ✅ | 跨编译器**可移植结构断言**（身份不匹配时的替代校验）：`call_count` / `contains` / `absent` |

> 【`command` 书写规范 = 机器执行契约（2026-09-10 定，`tools/atom_evidence_replay.py` 依此执行）】
> ① 多行 = 多条命令；同一行内多步用 `&&` 串联；② 路径一律**正斜杠**（POSIX 语义，两平台可执行；
> 反斜杠会被 argv 解析吞掉）；③ 编译产物**必须写 `build/`**——仓库源只读，根级 exe 泄漏会被
> pre-push 卫生拦；④ **不支持管道/重定向/通配/变量展开**（遇到工具直接报 unsupported，不猜）；
> ⑤ 生成 `artifact` 的那条命令必须出现在 `command` 里（工具据此"删旧工件→重生成→比 sha256"）。
> 复算四项校验任一不过即 `refute`（exit 1）：compile_rc / run_match / artifact_sha / sanitizer。

> 【双轨校验（2026-09-10 CI 红因修复，勿回退）】`artifact_sha256` 的"工件同代"承诺**只在同一
> 编译器（含平台）下成立**：实测同一夹具 MinGW GCC 15.3 与 GCC 13.1 产出的 `.asm` 字节完全不同
> （`d8b6b18d…` vs `cc446339…`），CI 在 Ubuntu 系统 g++ 上重生成必然 mismatch——**这不是工件过期，
> 是跨编译器天然差异**。故工具按编译器身份分流（`tools/atom_evidence_replay.py`）：
> ① 身份**匹配**（本地解析 == 卡 `artifact_compiler`）→ 强制比 `sha256`（原承诺不变）；
> ② 身份**不匹配** → 改判 `artifact_assert[]` 逐条实测；**断言缺失或任一条不满足仍判 refute**
> （"降级"是换成另一种真实校验，不是逃生舱）。
> 写卡要求：两个字段必须同时给，且 `artifact_assert` 必须是**跨编译器稳定**的形态——指令/符号
> 计数（`call_count`）、符号存在性（`contains`）、反例路径不存在（`absent`），**不要**拿字节片段当断言。

## 2. 实验矩阵：两档与选取规则

- **最小充分档（默认，每次提交都跑）**：`{GCC 15.3 × c++23 × -O2}` + `{GCC 15.3 × c++23 × -O0}`。
  选这两个的理由：-O2 是发布常态，-O0 用来排除"优化把观测本身优化掉"（见第 5 节）。
- **全量档（每个原子至少跑一次，进库前）**：编译器 `{GCC 15.3, GCC 13.1, Clang 19}` × std `{c++17, c++20, c++23}` × opt `{O0, O2}` + sanitizer `{ASan, UBSan}`（并发类加 TSan）。
- **选取规则**：论断涉及"标准版本差异" → 全量跑 std 维；涉及"实现细节/ABI" → 全量跑编译器维；涉及"性能" → 加 `-O3` 与基准（用 `Benchmarks/` 与 `_bench_d5_*` 现成夹具）；涉及 UB → 必跑 sanitizer 维。

> 【本机能力，已实测】GCC 15.3.0 / 13.1.0 / 8.1.0（`C:/Qt/Tools/mingw*_64`）；**无 Clang 与 MSVC**，
> CI 的 Clang-19 job 是唯一补齐路径（本机不伪造）。
> 【夹具 ↔ std 绑定（复跑前必看）】GCC 8.1.0 **不支持 `-std=c++23`**（`unrecognized command line
> option`）。故：`_atom_move_alloc.cpp` 用 c++23（8.1 档改 c++17，实测输出相同）；
> `_atom_eval_order.cpp` 统一 c++17。**别拿 c++23 直接跑全部夹具**（2026-09-10 复跑踩坑）。
> 【表述纪律】"三编译器对照"特指 **{GCC, Clang, MSVC}**，其中 Clang 待 CI、MSVC 无路径 → 标注
> "部分达成"；本机三版本 GCC 只能表述为**多版本对照**，两者不得合并宣称。
> 【永久边界（2026-09-10 监工裁决，勿再反复承诺）】MSVC 在本项目**无任何可执行路径**（无许可证/
> 无 runner）。凡"未指定/实现定义"类断言，**标准条文本身即结论**——不需要第三个编译器去"证实"
> 一个标准已明确说"未指定"的东西。故矩阵上限定死为：
> **GCC + Clang 双编译器实测 + MSVC 以标准条文（SRC-STD-*）代替**。任何文档/报告不得写成
> "三编译器全部实测"。

## 3. 证伪导向（不做"只演示成立"的实验）

**规则**：每个论断必须配一个**让它失败的对照**（`falsification` 字段），且对照必须真的失败。
只演示成立的实验 = 恒真测试 = 伪证据（S3）。

真实样本（`Examples/_atom_move_alloc.cpp`）：
- 正确实现 `Buf(Buf&&) noexcept : p(o.p)`（偷指针）→ **移动分配 = 0**
- 证伪对照 `BadBuf(BadBuf&&) : n(o.n) { p = new int[n]; }`（假移动，又分配一次）→ **假移动分配 = 1**
- 若对照也输出 0，说明计数器没接上或实验被折叠，实验无效。

## 4. 观测分层（8 种，逐原子标注用哪几种）

| 层 | 手段 | 现有抓手 |
|---|---|---|
| 退出码/输出 | 编译+运行，比对 stdout | `run_expected.py`（`//@` 契约，65 块全 PASS） |
| 汇编 | `-S -masm=intel` | `verify_asm_evidence.py`（符号级，五态） |
| 对象布局 | `-fdump-record-layouts` / `pahole` | **本机无 pahole**，GCC 支持 dump；待补工具 |
| ABI 符号 | `c++filt` / `objdump` | `tools/toolchain.py: resolve_cxxfilt/resolve_objdump` |
| 指令数 | 汇编块指令计数 | 自写（尚无现成） |
| 基准 | 计时/吞吐 | `Benchmarks/`（34 个）+ `_bench_d5_*.cpp`（126 个）+ `d5_runtime_gate.py` |
| sanitizer | `-fsanitize=address/undefined/thread` | `compile_run_sanitize_pipeline.py` |
| Godbolt 对照 | 外部编译器对照 | CI 的 Clang-19 job（本机无网对照能力） |

**夹具四要求**：自包含（不依赖外部文件）、确定性（同输入同输出，禁用未初始化/时间/地址作为断言）、可重入（可反复跑）、内容寻址缓存（`artifact_sha256` 变了才重跑）。

## 5. 防折叠规则（本次实测的血泪，M2 里我最想让读者记住的一条）

**规则：在 `-O2` 下做"计数类"实验，计数器必须声明 `volatile`（或等价的不可优化副作用），否则实验可能零观测。**

事故链（全部真跑过）：
1. 初版夹具只替换 `operator new`，而代码用 `new int[n]` → 走 `operator new[]` → 计数恒为 0，输出 `0/0/0`。**"移动分配=0"看起来完美证实论断**，实际是空测试。
2. 补了 `operator new[]` 后输出 `1/1/0`，但查汇编发现 `main` 里**没有** `call _Znay`，只有 `mov edx,1` —— **-O2 把计数常量折叠了**：分配"次数"与块大小无关，编译器静态推出 1/1/0，运行输出只是编译器推导的结果，不是运行时观测。
3. 用 `argc` 让大小运行时确定，**仍然折叠**（因为次数与大小无关）。
4. 把计数器改成 `volatile long` 才真正阻断：`main` 里出现 `call malloc` **恰好 3 次**
   （Buf 构造 1 + Buf 拷贝 1 + 证伪对照 `BadBuf` 假移动 1；去掉对照则 2 次），真实移动路径 0 次，
   与运行时 `1/1/0` 互证。

> 口径教训（2026-09-10 复跑修正）：这条最初记成"2 次"，是**只看主实验**数的；夹具加入证伪对照后
> `main` 内实际 3 次。数字必须与"是否含对照"绑定说明，否则复核者会判为"对不上"。

**因此 M2 定死**：
- 计数/计时类实验：`-O0` 与 `-O2` **都必须跑**，两档一致才算数（只跑 -O2 不算）。
- 计数器/观测点必须 `volatile` 或有不可分割的副作用。
- 汇编层必须能找到对应的调用点；**找不到调用点却"证实"了论断 → 判伪证据**（S3 必抓）。

## 6. 纵深链（6 层，逐原子标注钻到哪层）

`标准语义 → 编译器（AST/重载决议）→ 汇编 → C ABI（调用约定/this/vtable/栈帧/布局）→ 运行时（堆/栈/生命周期/内存序）→ 硬件`

标注规则：`depth.layer` 写**最深**那层，`depth.drill_note` 写该层的具体证据（如"`main` 中 `call malloc` 2 次，移动路径无分配"）。**不允许只标到"标准语义"就收工**——那等于没做实证，只是引述。

## 7. 灰色地带判定流程（本次第一刀）

五类：`defined` / `unspecified` / `implementation_defined` / `ub` / `abi_dependent`。

决策树（逐条问，命中即停）：
1. 标准给唯一确定结果？→ `defined`
2. 实现必须写进文档说明？→ `implementation_defined`
3. 标准给了合法结果集合、实现任选其一（不要求文档）？→ `unspecified`
4. 取决于 ABI/调用约定/布局/对齐，而非语言语义？→ `abi_dependent`
5. 标准完全无要求（任何结果都可能，含崩溃）？→ `ub`

**工具**：`tools/gray_zone_scan.py`（句子级初筛 + 疑似误分类告警）。
**实测分布**（1478 个候选句）：`ub 1100 (74.4%)`、`defined 167 (11.3%)`、`implementation_defined 103 (7.0%)`、`unspecified 93 (6.3%)`、`abi_dependent 15 (1.0%)`。

**已抓到的真实误用（3 条 = ch40 ×2 + ch96 ×1，待 G5 修文，本轮不改文）**：
- `part04_memory/ch40_exception_safety.md`、`part08_algorithms/ch96_sorting.md`：`std::sort` 比较器抛异常后写成"顺序**未定义**" → 标准实为**顺序未指定（unspecified）**，不是 UB。读者会误判为 UB 而恐慌。

**三编译器对照模板**：
```
论断：f(g(), h()) 中 g/h 的求值顺序未指定（unspecified，非 UB）
矩阵：{GCC 8.1.0, GCC 13.1.0, GCC 15.3.0} × c++17 × {-O0, -O2}
实测（本机复跑 2026-09-10）：6 组组合全部输出 hg|f(1,2)（右→左求值），rc=0，无 UB 征兆
结论：confirm（属 unspecified）。**多版本两档一致 ≠ 可依赖**——这正是要教给读者的点：
     标准给的是"未指定"，实现今天恰好一致；换编译器/版本/优化级别就可能翻转。
【缺口】Clang-19 列由 CI 补（本机无 Clang）；MSVC 无任何可用路径 → 本行标注"部分达成"，
     不得宣称"三编译器对照已完备"。
```

## 8. 不可实证类（禁止硬造实验）

历史背景、设计哲学、标准化过程 → `kind: traceable_argument`：
- `sources[]` ≥ 2 个**独立**源 + 时间线 + 权威引用
- 明确标注"本论断不可编译验证"
- **禁止**为凑实验而造一个只能演示"我说的对"的程序

## 9. 反例自检

- 有 `expected` 无 `actual` → 伪证据，**不合格**。
- 只有证实没有证伪对照 → 恒真测试，**不合格**。
- -O2 下计数类实验但计数器非 volatile → 可能零观测，**不合格**。
- 汇编层找不到对应调用点却声称"纵深到汇编" → **不合格**（本次就抓到过）。
- 灰色地带只给结论不给决策树 → 执行者无法判新句子，**不合格**。
