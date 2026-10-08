# 693-E5 · 元评估框架 v2 报告

- 生成：2026-10-08T21:17:17+08:00｜脚本：`tools/eval_693_meta_evaluation.py`
- **`detect_calls` = 0**（只读冻结矩阵，符合红线 8）
- 帧：`a5_676f_detection_matrix.json` split=evaluation，n=**566**
- 前身：`686_meta_metrics.json`（686 元评估）

## 1. 区分度（AUC：把资产当二分类器，真值 = expected_verdict）

| 资产 | 计分样本 | AUC |
|---|---:|---:|
| `asan` | 562 | 0.7759 |
| `ubsan` | 562 | 0.6739 |
| `tsan` | 562 | 0.6717 |
| `compiler-warn` | 566 | 0.5788 |
| `cross-compile` | 545 | 0.5558 |
| `linker` | 566 | 0.5062 |
| `compile-time` | 0 | None |
| `wunsequenced` | 0 | None |
| `OR_all8` | 566 | 0.8911 |

## 2. 稳定性

### 2.1 种子（682 的 5000 次重跑）

- FD 率 **54.5936%**；随机分布 mean 40.1913%、SD 9.2521pp
- FD 在随机分布中的百分位：**None**

### 2.2 环境（E1 vs E2 逐资产）

- 共享资产：`compiler-warn`, `cross-compile`, `linker`
- Spearman ρ = **1.0**
- ⚠ E2 支持的 3 个资产是 E1 的子集 ⇒ 其逐资产读数在冻结矩阵上**完全相同**；环境差异体现在**缺失资产**（asan/ubsan/tsan 不在 E2），而不是同一资产的读数变化 ⇒ ρ=1 是构造性结果，不是独立证据。

### 2.3 跑间（tsan）

- 有记录的样本 180 条，稳定性字段的不同形状 5 种

## 3. 公平性（同一资产跨缺陷类型的 recall 离散度）

| 资产 | 类型数(n≥5) | recall 最低% | 最高% | 极差 pp | σ pp | 零 recall 类型数 |
|---|---:|---:|---:|---:|---:|---:|
| `asan` | 39 | 0.0 | 100.0 | **100.0** | 37.43 | 12 |
| `ubsan` | 39 | 0.0 | 100.0 | **100.0** | 31.84 | 14 |
| `tsan` | 39 | 0.0 | 100.0 | **100.0** | 26.15 | 16 |
| `cross-compile` | 39 | 0.0 | 81.82 | **81.82** | 23.04 | 19 |
| `compiler-warn` | 39 | 0.0 | 70.0 | **70.0** | 19.19 | 22 |
| `linker` | 39 | 0.0 | 26.67 | **26.67** | 4.21 | 38 |
| `compile-time` | 39 | 0.0 | 0.0 | **0.0** | 0.0 | 39 |
| `wunsequenced` | 39 | 0.0 | 0.0 | **0.0** | 0.0 | 39 |

- 偏科最严重的资产：**`asan`**
- 公平性 = 同一资产在不同缺陷类型上的 recall 离散度；离散度大 = 系统性偏科。

## 4. 效率（676g 逐格 wall_seconds）

| 资产 | n | 均值 s | 总计 s | 最慢 s | P95 s |
|---|---:|---:|---:|---:|---:|
| `asan` | 1147 | 8.5957 | 9859.32 | 242.307 | 3.258 |
| `ubsan` | 1147 | 8.5945 | 9857.93 | 242.588 | 3.276 |
| `tsan` | 1147 | 8.9226 | 10234.25 | 242.462 | 3.498 |
| `compiler-warn` | 1147 | 0.214 | 245.43 | 1.417 | 0.426 |
| `cross-compile` | 1147 | 11.4695 | 13155.47 | 362.444 | 1.909 |
| `linker` | 1147 | 0.3992 | 457.92 | 1.065 | 0.659 |
| `compile-time` | 1147 | 0.0036 | 4.09 | 0.011 | 0.005 |
| `wunsequenced` | 1147 | 0.0412 | 47.29 | 0.384 | 0.057 |

- 效率帧 n = 1147

## 5. 校准

- **LLM 臂 ECE = 0.3812**（n=292，真实 confidence）
- 检测器（确定性，confidence≡1）ECE = 0.419（n=3363）
- 检测器是确定性的（自报 confidence 恒为 1）⇒ 其 ECE 恰好等于 1 − accuracy，读作「过自信程度」；LLM 臂有真实 confidence ⇒ ECE 有实质含义。

### 5.1 LLM 可靠性曲线

| 置信度区间 | n | 平均置信度 | 实际正确率 | 差 |
|---|---:|---:|---:|---:|
| [0.7,0.8) | 1 | 0.7 | 1.0 | +0.3000 |
| [0.8,0.9) | 2 | 0.825 | 1.0 | +0.1750 |
| [0.9,1.0) | 289 | 0.9953 | 0.6125 | -0.3829 |

## 6. 与 HELM / SV-COMP / DeepFact 的维度对照（**定性，非实测**）

| 框架 | 领域 | 它的维度 | 本装置已覆盖 | 本装置缺失 |
|---|---|---|---|---|
| **HELM** | 通用 LLM 评测 | accuracy、calibration、robustness、fairness、bias、toxicity、efficiency | accuracy、calibration、robustness(环境)、fairness(按类型)、efficiency | toxicity/bias（不适用）、多任务覆盖矩阵 |
| **SV-COMP** | 软件验证竞赛 | soundness、correctness、score-based ranking、witness 校验、CPU-time/memory limits | soundness（negative 可信性）、资源限制（60s 超时）、score-based 组合排序 | 形式化 witness 校验、统一任务定义格式、第三方裁判（独立复算） |
| **DeepFact** | 深度学习模型缺陷检测基准 | label validity、data leakage、distribution shift、baseline fairness | label validity（693-A 人类裁决材料）、data leakage（模板克隆 62.2%）、distribution shift（合成→真实靶场） | 跨数据集迁移实验、训练侧模型 |

> 来源：公开方法论（作者整理，非实测）。
> 本表用于定位本装置的**方法论缺口**，不是与这些框架的性能比较。

## 7. 诚实边界

- 框架对照是**作者按公开方法论整理的定性对照**，不是实测运行结果。
- 环境稳定性的 ρ=1 是构造性的（E2 资产是 E1 子集，同一矩阵读数不变），不构成独立证据。
- 效率数据来自 676g 的 wall_seconds，含 WSL 冷启动与文件系统开销，**不是算法复杂度**。
- 检测器的 ECE 是确定性系统的退化读数（confidence≡1），不可与 LLM 的 ECE 直接比较。
- 本批**未执行**容器环境（无 Docker），故「跨容器稳定性」维度缺失。
