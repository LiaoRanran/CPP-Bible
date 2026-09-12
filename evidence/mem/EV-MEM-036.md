---
id: EV-MEM-036
serves: [ATOM-MEM-LEAK-001]
kind: run
hypothesis: >-
  正确侧基线：owner/observer 结构（父节点用 shared_ptr 拥有子节点、子节点只用 weak_ptr 导航）在
  构树函数返回时整棵树正常析构——实测 constructed=3 / destroyed after scope=3，反向导航仍可用
  （parent reachable=1）；且本场景下进程**无 sanitizer 报错**。
controlled_vars: 同一树形状、同一构树函数（含 `__attribute__((noinline))` 隔离与栈擦洗）、同一编译器与优化档；唯一变量 = parent 的引用强度（本卡 weak；对照卡 EV-MEM-037 为 shared）
matrix:
  compiler: [GCC 15.3.0]
  stdlib: [libstdc++]
  std: [c++23]
  opt: [-O0, -O2]
  arch: [x86-64]
fixture: Examples/atoms/_atom_leak_tree_ok.cpp
command: |
  g++ -std=c++23 -O2 -S -masm=intel Examples/atoms/_atom_leak_tree_ok.cpp -o Examples/atoms/_atom_leak_tree_ok.asm
  g++ -std=c++23 -O2 Examples/atoms/_atom_leak_tree_ok.cpp -o build/_replay_leak_ok.exe && ./build/_replay_leak_ok.exe
artifact: Examples/atoms/_atom_leak_tree_ok.asm
artifact_sha256: 0fd4a1acb85f83b5bd27c62c4022a9085e9b2ad36401ceb8f36b5c10825649f0
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains, text: "destroyed after scope="}   # 观测 1 在工件里（两条独立断言，避免"任一命中即过"放行掏空实体的变异）
  - {kind: contains, text: "parent reachable="}        # 观测 2 在工件里
  - {kind: contains_any, texts: ["_Znwm", "_Znwy"]}    # 分配**调用点**真实存在（本工件 3 处 `call _Znwy`；口径：`grep -cE 'call\s+_Znw'` 按行计）
expected:
  run: 树 3 节点全部构造（constructed=3）、离开作用域全部析构（destroyed after scope=3）；根有 2 个子节点；weak 上行导航可达（parent reachable=1）
  asm: 两条观测标签与分配调用点都在工件里
actual:
  run_cxx23_O2: "root children=2|parent reachable=1|constructed=3|destroyed after scope=3"
  run_cxx23_O0: "root children=2|parent reachable=1|constructed=3|destroyed after scope=3"
verdict: confirm
falsification: >-
  **与 EV-MEM-037 的唯一变量对照（A/B 成对可复核）**：① 若"弱上行"反而破坏所有权链（父提前析构），
  本卡 `destroyed after scope` 会小于 3 或出现悬垂访问——实测 3/3 全析构；② 若 weak 边让节点提前
  消失，`parent reachable` 应为 0——实测 1。两条件均不成立 => 经受住证伪。
  A/B 判决力：两侧结构逐行对齐（同构树函数、同 noinline 隔离、同栈擦洗），唯一差异是 parent 强度，
  `destroyed` 由 3 变 0 ⇒ "环 → 不析构"的因果由这一对卡闭合。
depth_layer: runtime
drill_note: >-
  本卡在 ATOM-MEM-LEAK-001 中的角色是**正确侧基线**，不是机制发现（机制由 ATOM-MEM-WEAK-001 /
  ATOM-MEM-SHARED-001 承担，本卡不复述）。它的价值在于为"检测侧"提供两个输入：
  ① `destroyed after scope` 与 `parent reachable` 都是**运行期读**（工件里为 `mov edx, DWORD PTR
  _ZL11g_destroyed[rip]` 形态），不依赖任何 sanitizer 环境；
  ② 本场景在 WSL 下亦无 sanitizer 报错——但**这不是"没泄漏"的证据**（见 EV-MEM-037 的三档标定：
  同一 LSan 在不同优化档 × 不同结构上给出不同结论）。
reproduce: 见 command 两行，无外部依赖
---

## 为什么这个证据可信

1. **唯一变量对照**：与 EV-MEM-037 逐行对齐（同构树函数 + `noinline` 隔离 + 栈擦洗 + 同观测口径），
   唯一变量是 `parent` 的引用强度；`destroyed` 3 vs 0 把"环 → 不析构"钉死。
2. **两个运行期观测互相独立**：`destroyed after scope`（析构通路）与 `parent reachable`（弱边可用性）
   分别锚在两条断言上，任一条被"掏空实体"的变异打破都会被拦住（不是"任一命中即过"）。
3. **双档一致**：`-O0`/`-O2` 输出逐字一致，计数走 volatile 观测点。
4. **有界声称**：本卡只证明"该结构在该工具链下正确析构"，**不**承担"ASan 能/不能检测"的结论
   （那是 EV-MEM-037 的三档标定 + 原子卡的检测侧论断）。

## 边界诚实说明

- **不做"工程模式增量"声称**：owner/observer 判据已由 ATOM-MEM-WEAK-001 明文给出并由 EV-MEM-016
  实证；本卡只是把它作为对照的正确侧基线，避免与既有原子重复。
- **`parent reachable=1` 是本卡的已知恒真观测**（`root` 仍是活局部量时 `lock()` 必然成功）——
  本卡不把它当作证伪条件，只作为"弱边不破坏可用性"的说明性读数；缺陷侧的对称读数见 EV-MEM-037。
- **`-O0` 档是人工复跑留痕**：`command` 只跑 `-O2`（replay 机器口径沿 EV-MEM-008 先例）。
