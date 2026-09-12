---
id: MIS-MEM-031
name: "ASan/LSan 没报泄漏就是没有泄漏（把一次工具运行的静默当安全证明）"
level: deep
domain: MEM
trigger_patterns:
  - "跑了一遍 ASan，没报错，所以没有内存泄漏"
  - "CI 里加了 sanitizer，泄漏检测就交给它了"
  - "本地 sanitizer 全绿，可以上线"
refutations:
  - "**本批实测：真泄漏 + 零报告**——`_atom_leak_detection.cpp` 的 `cycle` 是 shared_ptr 强引用闭环：零依赖信号证明它确实泄漏（`cycle_dtor_count=0`、`cycle_is_leak=1`），而在 WSL/Linux 用 `-O1 -g -fsanitize=address,undefined` 运行，stderr **没有任何 LeakSanitizer 报告**（无 `ERROR: LeakSanitizer`、无 `SUMMARY: ... leaked`）"
  - "**且不能归因于"简单内联"**：同一夹具的 `run_cycle()`/`run_scoped()`/`run_owned()` **本就带 `__attribute__((noinline))`**（构环函数被隔离在独立函数里）⇒ 最直接的内联解释已被排除，说明\"没报\"的成因不止一种"
  - "**同族证据（LEAK-001）已证\"报与不报可完全相反\"**：极简两节点环 `-O0` 报 80 B/2 次分配、`-O2` 不报；树形夹具 `-O0`/`-O1` 不报、加 `noinline` 隔离后 `-O2` 报 224 B/4 次分配——同一份泄漏代码、不同档位结论相反"
  - "**零依赖信号是存在的、更稳的**：volatile 析构计数（`scoped_dtor_count=1` 作活性对照、`cycle_dtor_count=0` 判泄漏）与可达性读数（`owned_registry_size=1`）能在**没有任何 sanitizer** 的环境下定性 —— 注意 `cycle` 与 `owned` 的析构计数同为 0 但语义相反（不可达 vs 仍可达），单看计数也不够"
source: G5 第五批（LEAK-002）；ATOM-MEM-LEAK-002 / EV-MEM-042 / EV-MEM-043；LEAK-001 / EV-MEM-037；双平台与 sanitizer 实测（WSL g++-14）
related_atoms: [ATOM-MEM-LEAK-002, ATOM-MEM-LEAK-001, ATOM-MEM-WEAK-001, ATOM-MEM-SHARED-001]
---

# MIS-MEM-031 · "ASan/LSan 没报就是没泄漏"

**层级**：deep —— 它把**一次工具运行的静默**当成**性质证明**。危害在于结论被写进 CI/发布流程：
"sanitizer 全绿"变成放行依据，而工具的报告行为本身依赖优化档、对象存活位置与运行环境。

## 触发模式（学习者常这么说 / 这么写）
- "跑了一遍 ASan，没报错，所以没有内存泄漏"
- "CI 里加了 sanitizer，泄漏检测就交给它了"
- "本地 sanitizer 全绿，可以上线"

## 为什么它不成立
1. **本批实测：真泄漏 + 零报告**：`cycle`（shared_ptr 强引用闭环）被零依赖信号证明确实泄漏（`cycle_dtor_count=0`、`cycle_is_leak=1`），而 WSL/Linux `-O1 -fsanitize=address,undefined` 运行 stderr **完全没有 LeakSanitizer 输出**
2. **不能归因于"简单内联"**：夹具的三个生命周期函数**本就带 `__attribute__((noinline))`** ⇒ 最直接的解释已被排除，"没报"的成因不止一种
3. **同族证据已证"报与不报相反"**（LEAK-001）：极简环 `-O0` 报 80 B、`-O2` 不报；树形 `-O0`/`-O1` 不报、`noinline` 隔离后 `-O2` 报 224 B —— 同一份代码、不同档位结论相反
4. **零依赖信号存在且更稳**：析构计数 + 可达性读数可在无 sanitizer 环境下定性；但注意 `cycle` 与 `owned` 计数同为 0 而语义相反（不可达 vs 进程级持有）⇒ 单看计数也不够，须配可达性

## 正确理解
- **判据（三层信号，从稳到脆）**：
  ① **零依赖观测**：内置计数 / 控制块状态（任何环境都成立）；
  ② **可复算的结构读数**：迭代次数、分配次数等常量（跨环境稳定）；
  ③ **工具报告**：受优化档 / 存活位置 / 运行环境影响 —— **它是补充，不是结论**。
- 工程做法：**先用零依赖信号定性，再用工具找细节**；把"sanitizer 没报"当作"未发现问题"，而不是"没有问题"。
- 一条可复用自检：**"如果这段代码真的泄漏了，我这个信号会不会变？"** —— 不会变的信号（退出码、空 stderr）不能承担结论。

## 与 MIS-MEM-027 的分工
- **027**（第三批）：讲"把 sanitizer 的静默当安全证明"的**检测侧敏感度**（优化档/存活位置）；
- **031**（本条）：进一步给出**三层信号分级**与"零依赖优先"的可操作做法，并补一手实测（真泄漏 + 零报告 + noinline 已具备）。

## 出处与关联
- 出处：G5 第五批（LEAK-002）；ATOM-MEM-LEAK-002 / EV-MEM-042 / EV-MEM-043；LEAK-001 / EV-MEM-037；WSL g++-14 sanitizer 实测
- 关联原子：ATOM-MEM-LEAK-002、ATOM-MEM-LEAK-001、ATOM-MEM-WEAK-001、ATOM-MEM-SHARED-001
