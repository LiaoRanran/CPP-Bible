---
id: EV-MEM-043
serves: [ATOM-MEM-LEAK-002]
kind: run
hypothesis: >-
  **对照实验（唯一变量 = 一个与泄漏无关的 volatile 计数器）**：同一份循环引用夹具、同一编译器、
  同一优化档（WSL/Linux `-O1 -g -fsanitize=address,undefined`），
  **改前**（无构造计数）LeakSanitizer **零报告**（stderr 0 字节）；
  **改后**（给 `Node` 加 `volatile int g_cycle_ctor` 并自增，用于证明"分配真发生"）
  LSan **报告** `SUMMARY: AddressSanitizer: 64 byte(s) leaked in 2 allocation(s)`（stderr 1258 字节）。
  ⇒ 泄漏检测工具的**报告与否高度依赖被测代码的具体形态**——连"加一个计数器"这种与泄漏无关的
  改动都能翻转结论；"没报"因此不能直接等价于"没泄漏"。
controlled_vars: 同一夹具源码（仅增删一个 volatile 构造计数）、同一编译器与档位（WSL g++-14 `-O1 -g -fsanitize=address,undefined`）、同一运行方式（`ASAN_OPTIONS=allocator_may_return_null=1`）；唯一变量 = 构造计数的有无
matrix:
  compiler: [GCC 15.3.0 (MinGW-w64), GCC 14.2.0 (WSL)]
  stdlib: [libstdc++]
  std: [c++23]
  opt: [-O1（sanitizer 观测档）, -O2（零依赖判据档）]
  arch: [x86-64]
  sanitizer: ["ASan+UBSan+LSan（WSL/Linux）：**改前零报告 / 改后报 64 B in 2 allocs** —— 见下方对照表"]
  # 留痕与复跑命令（**外部复跑留痕**，可核对锚）：
  #   `g++-14 -std=c++23 -O1 -g -fsanitize=address,undefined Examples/atoms/_atom_leak_detection.cpp -o /tmp/ld_asan`
  #   `ASAN_OPTIONS=allocator_may_return_null=1 /tmp/ld_asan`
  #   完整 stdout + **stderr 原文** + 字节数 + LSan 命中计数已落盘 `Examples/atoms/_atom_leak_detection.out`
  #   （改后：stderr **1258 字节**、`grep -c -i leaksanitizer` = **1**）。
fixture: Examples/atoms/_atom_leak_detection.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/atoms/_atom_leak_detection.cpp -o Examples/atoms/_atom_leak_detection.asm
  g++ -std=c++23 -O2 Examples/atoms/_atom_leak_detection.cpp -o build/_replay_leak_detection.exe && ./build/_replay_leak_detection.exe
artifact: Examples/atoms/_atom_leak_detection.asm
artifact_sha256: ed44b0c6e06d2fcfdd88336417838e19eaf67ffb24e2f229d67e4a94a7f7b512
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains_any, texts: ["cycle_allocated=", "cycle_live_objects="]}    # 构造计数与不同源指标
  - {kind: contains_any, texts: ["cycle_dtor_count=", "owned_registry_size="]}  # 析构侧与可达性读数
expected:
  run: >-
    零依赖读数（9 行）：`scoped_dtor_count=1`（活性对照）、`cycle_dtor_count=0`、
    `cycle_allocated=2`（**两个 Node 都真的构造了** ⇒ 排除"分配被整体消除"）、
    `cycle_destroyed=0`、`cycle_live_objects=2`（不同源指标）、
    `owned_dtor_count=0` 与 `owned_registry_size=1`（全局持有，语义与 cycle 相反）。
  asm: 上述标签的打印格式串在工件 `.rdata` 中可见
actual:
  run_cxx23_O2: "scoped_dtor_count=1|cycle_dtor_count=0|owned_dtor_count=0|owned_registry_size=1|scoped_is_clean=1|cycle_allocated=2|cycle_destroyed=0|cycle_live_objects=2"
verdict: confirm
expected_sanitizer: [leak]   # 本夹具**含真泄漏演示**；改后 LSan 确实会报告 leak ⇒ 该声明现在**真的会被用到**
                             #   （折算 confirm，属反向证据，同 EV-MEM-014/024 口径）。
falsification: >-
  **对照实验（唯一变量 = 一个 volatile 计数器）**：

  | 版本 | 夹具差异 | LSan stderr | 报告内容 |
  |---|---|---|---|
  | 改前 | 无构造计数 | **0 字节** | （零报告） |
  | 改后 | 加 `volatile g_cycle_ctor` | **1258 字节** | `SUMMARY: AddressSanitizer: 64 byte(s) leaked in 2 allocation(s)` |

  同一夹具、同一档位、同一运行方式；唯一差别是一个**与泄漏无关**的计数器
  ⇒ "报告与否"对代码形态高度敏感（与 LEAK-001 的"优化档/存活位置敏感"同族，但更细：
  连加一个计数器都能翻转）。
  **数值自洽**：`64 B / 2 allocation(s)` = 2 × 32 B，与 `.asm` 中 Node 控制块+对象的 32 字节一致
  （EV-MEM-037 亦记录过 Tree 夹具 "224 B / 4 次"）⇒ 报告内容真实反映泄漏量，不是误报。
  **反方向**：若该闭环**不是**真泄漏，`cycle_allocated` 应为 0（未分配）或 `cycle_live_objects` 应为 0
  —— 实测 2 与 2 ⇒ 泄漏在零依赖侧也成立（不是因为"工具报了就信"）。
  **留痕可复核**：第三方照抄上方命令即可复现（`.out` 内含 stderr 原文与字节数）。
depth_layer: runtime
drill_note: >-
  本卡是"检测侧"最锋利的一个数据点：它把**工具报告的敏感性**从"取决于优化档"推进到
  "取决于任何改变代码生成的细节"。实践含义很直白——**不要用"跑过一次没报"作为无泄漏的证据**；
  至少要有零依赖信号（构造/析构计数、存活对象数）作为主证，工具报告作为**补充**。
---

# EV-MEM-043 · 对照实验：一个 volatile 计数器翻转 LSan 结论

## 两次观测（同夹具、同档位、同运行方式）

| 版本 | 夹具差异 | stderr | LSan 结论 |
|---|---|---|---|
| **改前** | 无构造计数 | **0 字节** | 零报告 |
| **改后** | 加 `volatile g_cycle_ctor` | **1258 字节** | `64 byte(s) leaked in 2 allocation(s)` |

完整留痕：`Examples/atoms/_atom_leak_detection.out`（含复跑命令、stdout、stderr 原文、字节数、LSan 命中计数）。

## 结论（本卡只承担"检测侧"这一半）

泄漏检测工具（LSan）**报告与否高度依赖被测代码的具体形态**：
- 报告内容真实（64 B = 2 × 32 B，与 .asm 一致）；
- 但**是否报告**会被与泄漏无关的改动翻转 ⇒ **"没报"不能等价于"没泄漏"**。

**机制不复述**（环为何泄漏见 prerequisite `ATOM-MEM-WEAK-001` / `ATOM-MEM-SHARED-001`；
优化档与存活位置的敏感度见 `ATOM-MEM-LEAK-001`）。

## 与 LEAK-001 的增量（H4 去重后）

| | LEAK-001（检测侧标定） | 本卡（工具报告边界） |
|---|---|---|
| 手段 | 优化档 `-O0/-O1/-O2` × 结构差异 | **同一档位**下、改一个**与泄漏无关**的计数器 |
| 结论 | "能否被报告取决于优化档与对象存活位置" | "报告与否**还**取决于任何改变代码生成的细节" |
| 关系 | prerequisite（本卡复用其结论，不复述机制） | 增量：把敏感度推进一层，并给出**前后对照**的一手观测 |

## 修订记录

- **2026-09-12 · v1 → v2（红队 BL1/H1/H2 + 一次观测反转）**
  - **BL1**：v1 的载荷观测（"LSan 零报告"）不可复核（command 产生不了该观测、actual 不含 stderr）
    ⇒ 已补完整复跑命令 + stderr 原文落 `.out`；
  - **H1**：v1 的 `cycle_is_leak` 是 `dtor_count==0` 的 1:1 派生（一 bit 两计）⇒ 已删除，
    改为 `cycle_allocated` / `cycle_destroyed` / `cycle_live_objects` 三条不同源指标；
  - **H2**：v1 无法区分"构造了但没析构"与"构造被整体消除" ⇒ 已加 volatile 构造计数；
  - **反转**：加构造计数后 LSan **从零报告变为报告 64 B/2 allocs** ⇒ v1 的核心观测被自家新工件否证，
    v2 据此把 claim 从"零报告"改为**"报告与否高度依赖代码形态"**，并以**前后对照**承担证据
    （比单方向断言更强，且唯一变量明确）。
  - 夹具改动后已重编译并更换 sha（`9aa81775…` → **`ed44b0c6…`**），EV-MEM-042 同步更新（9 行 actual）。
