# 705-B · 检测器能力边界地图（Capability Boundary Map）

> 8 资产在 110 条真实缺陷上的逐资产表现（683 冻结矩阵）。`wunsequenced`/`compile-time` 结构性恒 unknown，
> 不进 OR 分母、不当 miss。

## 逐资产能力边界

| 资产 | catch | miss | unknown | catch% | 能抓什么 | 抓不到什么 |
|---|---:|---:|---:|---:|---|---|
| asan | 54 | 55 | 1 | 49.09% | 堆/栈溢出、UAF、double-free、leak（内存动作） | 逻辑/协议语义、UB 非内存类、并发 race |
| ubsan | 20 | 89 | 1 | 18.18% | 有符号整数溢出等 runtime error | 无符号回绕（默认关）、内存越界、逻辑 |
| tsan | 25 | 84 | 1 | 22.73% | data race / 并发语义 | 单 TU 重构难复现的真实跨模块 race、逻辑 |
| compiler-warn | 5 | 105 | 0 | 4.55% | 警告级诊断（极少） | 绝大多数内存/UB/逻辑 |
| cross-compile | 22 | 87 | 1 | 20.00% | g++/clang++ 输出不一致暴露的 UB/ODR | 单编译器内一致的行为 |
| linker | 0 | 110 | 0 | 0.00% | 多 TU ODR/多定义（真实靶场 0 触发面） | 单 TU 重构样本（全 110 条） |
| wunsequenced | 0 | 0 | 110 | 0.00% | （本机不可用） | 全部 |
| compile-time | 0 | 0 | 110 | 0.00% | （无本地检测器） | 全部 |

## 资产互补性（独苗命中案例）
- **asan 独苗**（典型）：CVE-2014-0160（Heartbleed）、CVE-2021-3711（OpenSSL SM2）、CVE-2023-6246（glibc vsyslog）
- **tsan 独苗**（并发）：CVE-2024-6387（regreSSHion）、CVE-2016-5195（Dirty COW）、CVE-2022-31747（Firefox WebRTC）
- **ubsan 独苗**（UB）：CVE-2022-35737（SQLite printf 溢出）、CVE-2021-46143（expat DTD 组溢出）
- **cross-compile 独苗**（编译器分歧）：CVE-2022-4450（OpenSSL double-free）、CVE-2022-23308（libxml2 UAF）、CVE-2021-30663（WebKit 整数溢出）

## 能力边界的三条结论
1. **语义不可观测区**：逻辑/协议/状态机错误（logic_error 族 OR 3.23%）超出 8 资产观测范围——需性质化测试/状态机建模。
2. **配置缺口区**：UB 子类（无符号回绕/alignment/strict-aliasing）默认未启用 → 可通过补开关修复，但会改变口径（本批冻结）。
3. **环境/平台门控区**：换 deployment profile 丢 35pp（692）；wunsequenced/compile-time/linker 受平台约束——资产可用性本身是测量 tuple 的坐标。

## 诚实边界
- 上述"能抓/抓不到"绑定"本 8 资产 + 本工具链（WSL g++13.3 + MinGW g++13.1/clang22.1）"口径，不外推。
- 加入 MSan/Valgrind 等会改变绝对值（683 §5 已声明）。
