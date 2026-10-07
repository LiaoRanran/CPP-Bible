# 689-B3 · 三组件环境指标（catch / unknown / conditional recall）

- 生成：2026-10-07T21:43:01+08:00｜脚本：tools/environment_metrics_689.py｜种子：6891（确定性）
- 指标定义：catch_rate = catch/total；unknown_rate = unknown/total；conditional_recall = catch/(catch+miss)。

## 1. WSL g++ 13.3（实测）

### 1.1 真实 110 条 · 逐资产

| 资产 | catch | miss | unknown | catch_rate | unknown_rate | cond_recall |
|---|---:|---:|---:|---:|---:|---:|
| asan | 54 | 55 | 1 | 49.09% | 0.91% | 49.54% |
| ubsan | 20 | 89 | 1 | 18.18% | 0.91% | 18.35% |
| tsan | 25 | 84 | 1 | 22.73% | 0.91% | 22.94% |
| compiler-warn | 5 | 105 | 0 | 4.55% | 0.00% | 4.55% |
| wunsequenced | 0 | 0 | 110 | 0.00% | 100.00% | —（分母为 0） |
| cross-compile | 22 | 87 | 1 | 20.00% | 0.91% | 20.18% |
| linker | 0 | 110 | 0 | 0.00% | 0.00% | 0.00% |
| compile-time | 0 | 0 | 110 | 0.00% | 100.00% | —（分母为 0） |
| **OR（8 资产）** | 65 | 45 | 0 | 59.09% | 0.00% | 59.09% |

### 1.2 合成 1147 条 · 逐资产

| 资产 | catch | miss | unknown | catch_rate | unknown_rate | cond_recall |
|---|---:|---:|---:|---:|---:|---:|
| asan | 408 | 729 | 10 | 35.57% | 0.87% | 35.88% |
| ubsan | 270 | 867 | 10 | 23.54% | 0.87% | 23.75% |
| tsan | 263 | 874 | 10 | 22.93% | 0.87% | 23.13% |
| compiler-warn | 143 | 1004 | 0 | 12.47% | 0.00% | 12.47% |
| wunsequenced | 0 | 0 | 1147 | 0.00% | 100.00% | —（分母为 0） |
| cross-compile | 122 | 987 | 38 | 10.64% | 3.31% | 11.00% |
| linker | 10 | 1137 | 0 | 0.87% | 0.00% | 0.87% |
| compile-time | 0 | 0 | 1147 | 0.00% | 100.00% | —（分母为 0） |
| **OR（8 资产）** | 707 | 440 | 0 | 61.64% | 0.00% | 61.64% |

## 2. Windows native（口径推断，非实测）· 真实 110

- **unaware（静默退化记账）**：跨平台资产并集 OR = 26/110 = 23.64%，unknown 0%。
- **aware（感知记账）**：asan/ubsan/tsan 资产级 unknown=100%；感知协议下 asan/ubsan/tsan 记资产级 unknown=100%；样本级 OR 仍为 23.64%，但该数字必须随"能力边界声明"使用，不得与 P1 的 59.09% 直接相减后当"退化"而不说明分母构成

## 3. Δ 对比表

| 对比 | 指标 | Δ |
|---|---|---:|
| clang vs gcc（asan，n=200） | Δcatch_rate | +1.00pp |
| clang vs gcc（asan，n=200） | Δunknown_rate | +1.50pp |
| clang vs gcc（asan，n=200） | Δcond_recall | +1.55pp |
| clang vs gcc（ubsan，n=200） | Δcatch_rate | +2.00pp |
| clang vs gcc（ubsan，n=200） | Δunknown_rate | +1.50pp |
| clang vs gcc（ubsan，n=200） | Δcond_recall | +2.45pp |
| native vs WSL（真实 110，OR） | Δcatch_rate（静默记账） | -35.45pp |
| native vs WSL（真实 110，OR） | Δunknown_rate（静默记账） | +0.00pp |
| native vs WSL（真实 110，OR） | Δcond_recall | -35.45pp |

## 4. clang↔gcc 家族分层（asan+ubsan 池化格）

| 家族 | 格数 | gcc catch% | clang catch% | Δ(clang−gcc)pp | gcc unknown% | clang unknown% |
|---|---:|---:|---:|---:|---:|---:|
| memory | 68 | 26.5 | 26.5 | +0.0 | 0.0 | 0.0 |
| bounds | 44 | 84.1 | 86.4 | +2.3 | 0.0 | 0.0 |
| integer | 42 | 45.2 | 45.2 | +0.0 | 0.0 | 0.0 |
| alias_type | 36 | 22.2 | 22.2 | +0.0 | 0.0 | 0.0 |
| concurrency | 74 | 9.5 | 6.8 | -2.7 | 0.0 | 0.0 |
| stl | 56 | 30.4 | 44.6 | +14.3 | 0.0 | 0.0 |
| language_oop | 42 | 14.3 | 14.3 | +0.0 | 0.0 | 0.0 |
| embedded_link | 38 | 2.6 | 0.0 | -2.6 | 21.1 | 36.8 |

## 5. 读法（四条）

- **r1_cross_toolchain_stable**：同 OS 换编译器（g++↔clang）在 200 抽样上 asan/ubsan 一致率 93.5%，κ=0.864/0.843，Δcatch ≤2pp、Δunknown ≤1.5pp ⇒ 工具链敏感性有限（实测）。
- **r2_environment_loss_dominant**：跨环境（WSL→native）真实 110 的 catch_rate 59.09%→23.64%（−35.45pp，口径推断）；且静默退化时 unknown 不上升（Δunknown=0）——单看 recall 会误以为"只是低了"，看不到"39 个捕获的测量根本未执行"。
- **r3_denominator_pathology**：wunsequenced/compile-time 在真实 110 上的资产级 unknown_rate=100%，但在 OR 口径被其他资产掩盖（样本级 unknown=0）。任何单资产分析若不并报 unknown 率，都会把这两个资产读成"0 检出"。
- **r4_family_layer**：clang↔gcc 的差异集中在 stl 家族（+8/56 格 = +14.3pp，clang 更高），其余家族 Δ 极小；家族层无反转 ⇒ 一致率不是被单一家族拉高的。

## 6. 诚实边界

- windows-native 一档为**架构/口径推断**，非本机实测；不得写成实测数字。
- wsl-clang 档为 200 条分层抽样（非全池），其 catch 率不可与全池 61.64%/59.09% 直接比；仅用于同一样本上的 gcc↔clang 配对对比。
- clang 侧 unknown（7/200）高于 gcc（4/200）：其中含 1 条 clang 编译失败（expF:F176），如实保留为 unknown。
- P2 的"26/110"来自 683 矩阵中跨平台资产 verdict 的并集；若 Windows 上链接器/编译器行为与记录环境不同，绝对值会移动。

复算：`python tools/environment_metrics_689.py`。
