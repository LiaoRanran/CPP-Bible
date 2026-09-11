---
id: MIS-MEM-027
name: "ASan 没报 = 没泄漏（把 sanitizer 的静默当成安全证明）"
level: deep
domain: MEM
trigger_patterns:
  - "跑了一遍 ASan，没报错，所以没有内存泄漏"
  - "泄漏检测交给 sanitizer 就行了"
refutations:
  - "退出码与 stderr 根本不携带泄漏信号：泄漏进程照常 `return 0`、stderr 干净（实测 EV-MEM-037 的缺陷侧 `destroyed after scope=0` 而进程正常退出）——把'没看到报错'当结论，等于用一个不携带信号的通道下判断"
  - "ASan/LSan 的判定对优化档与对象存活位置高度敏感（实测三档 × 两结构 5 个数据点）：极简两节点环在 `-O0` 报 80 B/2 次分配、`-O2` 不报；树形结构（含 vector + 导航边）在 `-O0`/`-O1` 不报、加 `__attribute__((noinline))` 隔离构树后 `-O2` 报 224 B/4 次分配。同一份泄漏代码、不同档位的结论可以完全相反"
  - "不依赖 sanitizer 的确定信号是存在的：夹具内 volatile 析构计数（destroyed=0 vs 3）与控制块 `use_count()`（= 局部持有 1 + 强边数）、`weak_ptr::expired()` 都能在没有任何 sanitizer 的环境下判定泄漏与否（实测 EV-MEM-036/037，MinGW 侧 sanitizer 本就 skip）"
source: G5 第三批指令（LEAK-001，裁决 A：重定位为检测侧）；ATOM-MEM-LEAK-001 / EV-MEM-036 / EV-MEM-037；红队 Step 2 的 B5（内联假设未证伪）与 H5（信号分层缺失）
related_atoms: [ATOM-MEM-LEAK-001, ATOM-MEM-WEAK-001, ATOM-MEM-SHARED-001]
---

# MIS-MEM-027 · "ASan 没报 = 没泄漏"

**层级**：deep —— 结构性误解：把**检测工具的一次运行结果**当成**性质证明**。它不是记错一个细节，而是会让人在 CI/评审里用一个不携带信号或随时漏报的通道给出"安全"结论，从而把泄漏带进生产。

## 触发模式（学习者常这么说 / 这么写）
- "跑了一遍 ASan，没报错，所以没有内存泄漏"
- "泄漏检测交给 sanitizer 就行了"

## 为什么它不成立
1. **退出码与 stderr 根本不携带泄漏信号**：泄漏进程照常 `return 0`、stderr 干净（实测 EV-MEM-037 的缺陷侧 `destroyed after scope=0` 而进程正常退出）——把"没看到报错"当结论，等于用一个不携带信号的通道下判断
2. **ASan/LSan 的判定对优化档与对象存活位置高度敏感**（实测三档 × 两结构 5 个数据点）：极简两节点环在 `-O0` 报 80 B/2 次分配、`-O2` 不报；树形结构（含 vector + 导航边）在 `-O0`/`-O1` 不报、加 `__attribute__((noinline))` 隔离构树后 `-O2` 报 224 B/4 次分配。同一份泄漏代码、不同档位的结论可以**完全相反**
3. **不依赖 sanitizer 的确定信号是存在的**：夹具内 volatile 析构计数（destroyed=0 vs 3）、控制块 `use_count()`（= 局部持有 1 + 强边数）、`weak_ptr::expired()` 都能在**没有任何 sanitizer** 的环境下判定泄漏与否（实测 EV-MEM-036/037；MinGW 侧 sanitizer 本就 skip）

## 正确理解
- **判据**：问三次——① 这个信号**在泄漏时会不会变**？（退出码/stderr：不会）② 它**依赖环境**吗？（sanitizer：依赖优化档与存活位置）③ 有没有**零环境依赖**的读数？（内置计数 / 控制块状态）
- 工程做法：**至少一条零依赖信号 + sanitizer 作为补充**，而不是反过来。
- 一个可复用的自检问题：**"我的隔离真的成立吗？去看工件里那个函数还在不在。"**——本条的 B5 拦截正是靠"`-O2` 工件里没有 `build_tree` 符号"揭穿的。

## 出处与关联
- 出处：G5 第三批指令（LEAK-001，裁决 A：重定位为检测侧）；ATOM-MEM-LEAK-001 / EV-MEM-036 / EV-MEM-037；红队 Step 2 的 B5（内联假设未证伪）与 H5（信号分层缺失）
- 关联原子：ATOM-MEM-LEAK-001、ATOM-MEM-WEAK-001、ATOM-MEM-SHARED-001
