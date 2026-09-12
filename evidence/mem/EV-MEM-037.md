---
id: EV-MEM-037
serves: [ATOM-MEM-LEAK-001]
kind: run
hypothesis: >-
  缺陷侧 + 检测标定：与 EV-MEM-036 同一棵树、**唯一变量 = parent 的引用强度**（shared 而非 weak）
  ⇒ 整棵树（3 节点）离开作用域后**零析构**（destroyed after scope=0），而进程**正常退出**、
  stderr 无任何信号；同时用三档实验标定"LSan 何时能报这类泄漏"——结论是**对优化档与对象存活位置
  高度敏感**（同一泄漏：`-O0` 极简环报 / `-O0` 树形不报 / `-O2` 树形（`noinline` 隔离后）报 /
  `-O2` 极简环不报）。
controlled_vars: 同一树形状与构树函数（含 `__attribute__((noinline))` 隔离 + 栈擦洗）；唯一变量 = parent 的引用强度（本卡 shared；对照卡 EV-MEM-036 为 weak）
matrix:
  compiler: [GCC 15.3.0]
  stdlib: [libstdc++]
  std: [c++23]
  opt: [-O0, -O2]
  arch: [x86-64]
  sanitizer: ["ASan/LSan（Linux/WSL 侧）：-O0/-O1 不报、-O2（noinline 隔离）报 224 B；本机 MinGW 侧 skip"]
fixture: Examples/atoms/_atom_leak_tree_bug.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/atoms/_atom_leak_tree_bug.cpp -o Examples/atoms/_atom_leak_tree_bug.asm
  g++ -std=c++23 -O2 Examples/atoms/_atom_leak_tree_bug.cpp -o build/_replay_leak_bug.exe && ./build/_replay_leak_bug.exe
artifact: Examples/atoms/_atom_leak_tree_bug.asm
artifact_sha256: e5a31cca38b9b908028db444fe00e83b06762451f2fadcf287ad82d1ba197db6
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains, text: "destroyed after scope="}   # 观测 1（两条独立断言，避免"任一命中即过"）
  - {kind: contains, text: "root use_count="}          # 观测 2（控制块强计数，不依赖夹具自插仪器之外的任何东西）
  - {kind: contains_any, texts: ["_Znwm", "_Znwy"]}    # 分配调用点真实存在（本工件 3 处 `call _Znwy`）
expected_sanitizer: [leak]
expected:
  run: 树 3 节点全部构造（constructed=3）但零析构（destroyed after scope=0）；根被两个子节点强引用（root use_count=3，含局部变量那一份）；进程正常退出
  asm: 两条观测标签与分配调用点都在工件里
actual:
  run_cxx23_O2: "root children=2|root use_count=3|constructed=3|destroyed after scope=0"
  run_cxx23_O0: "root children=2|root use_count=3|constructed=3|destroyed after scope=0"
verdict: confirm
falsification: >-
  **真对照（与 EV-MEM-036 的唯一变量对照）**：① 若"强上行"不产生环，`destroyed after scope` 应为 3
  ——实测 0；把 `parent` 改回 weak（EV-MEM-036）后变回 3 ⇒ 因果由 A/B 闭合。
  ② 若泄漏会以显式失败暴露，本卡应能观察到崩溃/非零退出码/stderr 报错——实测三者皆无
  （`rc=0` 仅作"未观察到崩溃"，**不作**主证）。
  **检测侧标定（本卡新增的判别性内容，全部为实测）**：

  | 夹具 | 结构 | 优化档 | LSan 结果 | 报告原文（节选） |
  |---|---|---|---|---|
  | `_atom_leak_two_node.cpp` | 极简两节点环（2 块） | `-O0` | **报** | `Indirect leak of 40 byte(s) in 1 object(s)` ×2；`SUMMARY: 80 byte(s) leaked in 2 allocation(s)` |
  | `_atom_leak_two_node.cpp` | 同上 | `-O2` | 不报 | — |
  | `_atom_leak_tree_bug.cpp` | 树形 3 节点 + vector + 导航边 | `-O0` | 不报 | — |
  | 同上 | 同上 | `-O1` | 不报 | — |
  | 同上 | 同上（`__attribute__((noinline))` 隔离构树） | `-O2` | **报** | `Indirect leak of 128/64/32 byte(s)`；`SUMMARY: 224 byte(s) leaked in 4 allocation(s)` |

  ⇒ 结论：**"ASan 没报"不能推出"没泄漏"**；能否被报告取决于优化档与对象存活位置（构树被内联时，
  堆指针留在 callee-saved 寄存器/活栈帧里，LSan 判其可达）。`expected_sanitizer: [leak]` 只在
  **命中时**折算反向证据；本卡在 replay 机器口径（`do_sanitizer` 固定 `-O1`）下**已知不触发**，
  该字段不构成本卡的正向或负向信号，仅覆盖"其他环境若命中"的情形。
depth_layer: runtime
drill_note: >-
  把 `parent` 从 weak 改成 shared 只多了一条强边，却让引用计数闭环：root 被两个子节点各持一次
  （`root use_count=3` = 局部变量 1 + 两条 parent 边 2），子节点被 root 的 children 持有 ⇒ 构树函数
  返回时每个对象只从 3 降到 2、不归零，整棵树（含控制块与 vector 缓冲）永不进入释放路径。
  **过程完全静默**：`rc=0`、stderr 干净，唯一异常数字来自夹具自插的观测点。
reproduce: 见 command 两行，无外部依赖
---

## 为什么这个证据可信

1. **A/B 对照**：与 EV-MEM-036 结构逐行对齐、唯一变量是 parent 强度，`destroyed` 3↔0 闭合因果。
2. **静默性实测**：`rc=0` + stderr 干净，把"泄漏为什么危险"从口头警告变成可复核事实。
3. **检测侧标定是判别性内容**：三档 × 两结构的 5 个数据点全部实测（不是"若…则应…"），且**推翻了
   作者先前的归因**——最初结论是"LSan 有结构性漏报"，加 `noinline` 隔离后 `-O2` 树形**能报**，
   说明真正的变量是"优化档 × 存活位置"。这条修正过程本身留在卡内（Step 2/3 节）。
4. **信号分层有据**：检测信号按"是否依赖 sanitizer 环境"分层——`destroyed` 计数（volatile 读）与
   `root use_count`（控制块强计数）都是确定信号；退出码/stderr 不携带信号；sanitizer 层则受上述
   条件影响。

## 边界诚实说明

1. **LSan 结论的适用范围**：全部标定数据来自 WSL / `g++-14.2 / Ubuntu`，`-std=c++23`，sanitizer
   组合 `address,undefined`；`ASAN_OPTIONS` 未额外设置。跨平台/跨版本不保证同样档位映射。
2. **不做 Valgrind 对照**：本机/WSL 未安装 Valgrind，按 M2"工具缺失即如实声明边界"处理，
   不以"另一种工具大概也能测"代替实测（计划书主题含 Valgrind，差异已在原子卡 Step 4 留痕待裁）。
3. **不声称"任何环都必然泄漏"**：这里是 `shared_ptr` 参与的环；判据仍是"所有权图是否有环"。
4. **`-O0` 档是人工复跑留痕**：`command` 只跑 `-O2`。
5. **三个数字口径不同**：`constructed=3`（构造次数）、`destroyed=0`（析构次数）、`use_count=3`
   （控制块强计数，含局部变量那一份）——三者不可互相换算。
