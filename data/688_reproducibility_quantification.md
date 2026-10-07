# 688 · B2 条件复现的量化（WSL 依赖）

- **批次**：688 ｜ **数据**：`688_reproducibility_quantification.json`
- **背景**：686 硬伤 #9——脱离 WSL 则 15 样本降级 unknown、外部召回 35%→10%、guard 仍绿（条件复现）。
- **补实验目标**：在真实靶场 110 样本上**量化**哪些资产依赖 WSL、纯 Windows 下可用性与检出率、有无替代方案。

## 1. 资产可用性（按平台）

| 资产 | 依赖 | 本机（MinGW）状态 | 纯 Windows-native 可用性 |
|---|---|---|---|
| asan | Linux/WSL 运行时 | 跑（WSL）| **不可用** |
| ubsan | Linux/WSL 运行时 | 跑（WSL）| **不可用** |
| tsan | Linux/WSL 运行时 | 跑（WSL）| **不可用** |
| compiler-warn | 任意编译器告警 | 跑 | 可用（需本机编译器）|
| cross-compile | 交叉编译工具链 | 跑 | 可用（需 MinGW/交叉链）|
| linker | 链接期检查 | 跑 | 可用 |
| wunsequenced | 本机 MinGW 不认 -Wunsequenced | **恒 unknown** | 恒 unknown |
| compile-time | 无本地检测器 | **恒 unknown** | 恒 unknown |

## 2. 量化：无 WSL 时的召回塌方
- **全资产 OR 检出率**：59.09%（65/110）。
- **仅跨平台资产**（compiler-warn + cross-compile + linker）并集：**23.64%**（26/110）。
- **失去 WSL 的掉点**：**−35.45pp**（39 个捕获依赖 Linux sanitizer，且不被跨平台资产覆盖）。
- sanitizer 内部：asan 单独承担 18 个、tsan 3 个、ubsan 3 个为"唯一捕获者"（共 24 个单 sanitizer 独苗）；另有 15 个由 ≥2 sanitizer 共抓且无其他资产覆盖 → 合计 39 个 sanitizer-dependent 捕获。

## 3. 运行时成本（wall_seconds_by_asset）
| 资产 | 耗时(s) | 性价比备注 |
|---|---:|---|
| cross-compile | 1026.18 | 最贵（交叉编译）；但跨平台 |
| tsan | 431.62 | 贵 |
| asan | 416.42 | 贵但高价值 |
| ubsan | 412.18 | 贵 |
| linker | 37.21 | 便宜 |
| compiler-warn | 22.87 | **最便宜**，低贡献 |
| wunsequenced | 3.48 | 近 0 贡献（恒 unknown）|
| compile-time | 0.42 | 声明性资产，0 贡献 |

- cross-compile 单资产耗时最长（1026s），却只有跨平台可用资产中贡献中等——效率上值得审视。
- asan/ubsan/tsan 三者耗时相近（~410–430s），贡献却以 asan 为主（A5）。

## 4. Windows 替代方案（观测性，非实测）
- **MSVC `/analyze`**：可提供部分静态告警（对应 compiler-warn 维度），但**不提供 asan/ubsan/tsan 运行时检测**——无法替代 sanitizer 的 39 个捕获。
- **Clang/LLVM 的 ASan/TSan/UBsan 在 Windows 上可通过 clang-cl 启用**，但需**非 MinGW 工具链**；本仓库实测环境为 MinGW g++，未配置 clang-cl → 当前声明环境外不可复现（与 686 #9 一致）。
- 结论：在**纯 Windows-native（MinGW）**下，真实召回上限 ≈ 23.64%（跨平台资产），**无法逼近 59.09%**。

## 5. 对 686 硬伤的处置
- 本补实验**量化**了 686 #9 的严重程度：掉点 35.45pp（≈ 真实召回的 60% 依赖 WSL）。
- 建议论文：在"复现性"段明确"**条件复现**"语义 + 给出本量化（59.09%→23.64%），并保留 fail-loud 自检（错环境抛错）。

## 6. 诚实边界
- "纯 Windows-native 23.64%"是**基于资产可用性推理的口径**，非在本机 Windows-native 实测（本仓库未配置 clang-cl/非 MinGW 链）；属可核验的架构推断，已在文中标注为推理。
- cross-compile 在纯 Windows 是否真可用取决于是否安装了交叉工具链，文中按"编译器依赖、原则可用"处理。
