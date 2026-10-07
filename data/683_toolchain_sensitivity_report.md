# 683-B3 · 工具链敏感性报告（clang 18 vs g++ 13.3；Windows vs WSL）

- 基线 = 676g 冻结矩阵（WSL g++ 13.3，双档 -O0/-O2，reuse 不重跑）
- clang 侧 = 本批实测（Ubuntu clang 18.1.3，判定字符串与 661 SAN 分支逐字一致）

## 编译器一致性（asan / ubsan）

| 资产 | n | 一致率 | Cohen's κ | g++ catch% | clang catch% | Δ(clang−g++) | 差异条数 |
|---|---:|---:|---:|---:|---:|---:|---:|
| asan | 200 | 93.5% | 0.864 | 32.5 | 33.5 | 1.0pp | 13 |
| ubsan | 200 | 93.5% | 0.8434 | 24.0 | 26.0 | 2.0pp | 13 |

- **最大检出差异：2.0pp**；≤10pp，工具链敏感性有限（如实报告）

## 跨平台（Windows 原生 vs WSL，n=50 并发类样本）

- Windows 原生裸运行：正常退出 48 / 崩溃 2 / 挂起(10s 超时) 0 / 编译失败 0
- 同一批样本 WSL 侧 tsan（676g）：catch 21/50
- 结论：Windows 侧为无 sanitizer 的裸运行观测（挂起/崩溃/正常）；WSL 侧 tsan 判定取自 676g（Linux 专属工具链）
