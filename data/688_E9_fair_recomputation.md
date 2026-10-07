# 688 · B3 E9 对比的公平化重算

- **批次**：688 ｜ **数据来源**：`673e_comparison_stats.json` / `673e_clang_tidy_cppcheck对比.md`（E9 即原 673e）
- **背景**：686 硬伤 #13——E9 对比"非同环境、主口径失败（100% 召回且 100% FPR=零判别）、StrictA 事后选"。
- **补实验目标**：统一环境下重算；若无法统一，明确限制并改为"观察性对比"。

## 1. 环境不可统一（核心障碍）
| 工具 | 版本 | 环境 | 编译器 |
|---|---|---|---|
| clang-tidy | LLVM 22.1.8（MSYS2/MinGW, x86_64-w64-windows-gnu）| **Windows 原生** | MinGW |
| cppcheck | 2.13.0 | **WSL Ubuntu 24.04** | — |
| Queyi FD | g++13.3 + sanitizer | **WSL** | g++ |

三者**不共享编译器/操作系统**：clang-tidy 在 Windows-MinGW，cppcheck 在 WSL，FD 依赖 WSL g++ + sanitizer。要"同一环境"需把三者迁到同一工具链（如全迁 WSL g++），但 clang-tidy 在 WSL g++ 下的行为与 MinGW 不同、cppcheck 本就 WSL——**重跑可得同 OS，但编译语义仍不同**（静态 vs 动态检测本质不同）。因此**严格公平的头对头对比在方法论上不可行**，属检测器类型差异而非配置疏忽。

## 2. 既有 E9（673e）结果（已预注册，诚实登记）
- **预注册主口径（clang-tidy 四检查族，任意 error/warning）——失败**：holdout 召回 **100%**、假阳 **100%**，**零判别力**（FD 也 100% 召回）。这是预注册设计缺陷，673e 已如实登记。
- **可辩护口径（仅 `clang-analyzer-*`）holdout**：FD **82.9% (34/41)** vs clang-tidy **48.8% (20/41)**，配对 (b,c)=(14,0)，McNemar **p=1.2×10⁻⁴**，Δ **+34.1pp [19.6, 48.7]**，且 **c=0（工具检出是 FD 检出的子集）**。
- **corpus**：FD 62.5% vs cppcheck 54.7%，(b,c)=(13,8)，**p=0.383 不显著**；宽松口径 cppcheck 67.2% 反略高于 FD 62.5%（p=0.69）。**8 条反向对**全部落在 compiler-warn/cross-compile/sanitizer 的"未初始化变量/重复释放"类——FD 真实短板。

## 3. 公平化处置结论
- **无法做严格头对头重算**；本补实验确认环境差异是结构性的（静态 vs 动态、MinGW vs WSL），非配置疏漏。
- **E9 应定位为"跨缺陷区间压力测试 / 观察性对比"，而非 superiority 声明**——这与 686 #13 与 686_rebuttal_redlines（"绝不说我们优于静态分析"）一致。
- 唯一干净的强信号是 **StrictA holdout（FD 更好且 c=0）**，但它仍跨环境，只能作观察性证据，不能作为"FD 优于 clang-tidy"的结论。
- 8 条反向对是**真实、可解释的 FD 短板**（未初始化/重复释放类），应在论文中保留为 honesty 证据，而非掩盖。

## 4. 对论文的建议
- E9 段标题/措辞明确写"**cross-regime observational comparison**"，删去任何 superiority 暗示。
- 保留 StrictA holdout（c=0 强信号）与 corpus 打平 + 8 反向对，作为"FD 不万能"的诚实证据。
- 在 Limitations 注明：clang-tidy/cppcheck 与 FD 不在同一编译器环境，对比仅供压力测试，不构成方法优劣结论。

## 5. 诚实边界
- 本 B3 **未重跑**工具（红线：不修改检测器；且重跑亦不能消除环境差异）。结论基于既有 673e 数据的诚实重解读。
- "零判别力主口径失败"是 673e 已登记的预注册缺陷，本批仅做 framing 建议，不掩盖。
