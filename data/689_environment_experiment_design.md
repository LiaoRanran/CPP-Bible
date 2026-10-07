# 689-B4 · 环境敏感性实验设计（Environment-Profile Sensitivity）

- 生成：2026-10-07｜批次：689｜执行：CodeBuddy（AI）
- 配套产物：`data/689_environment_metrics.json` + `_report.md`（三组件指标，已计算）、
  `tools/environment_metrics_689.py`（复算脚本）、`data/683_cross_toolchain_results.json`（683-B1 实测）、
  `data/688_reproducibility_quantification.json`（688 量化）。
- 定位：本文把"环境"从复现细节升格为 **measurement tuple 的正式组件**；本设计给出
  两部分实验：Part 1 已有实测并复算；Part 2 一半已量化（静默退化）、一半为**待执行**方案（含判定标准）。

---

## 0. 环境概况（本项目的真实拓扑，必须先说清）

| 环境 profile | 内容 | 实测状态 |
|---|---|---|
| `wsl-gcc-13.3` | WSL Ubuntu 24.04 + g++ 13.3.0：**asan / ubsan / tsan**（-O0/-O2 双档） | ✅ 实测（676g/683 全部样本） |
| `windows-native-mingw` | win32 + MinGW g++ 13.1.0：**compiler-warn / cross-compile / linker**；另 MinGW clang 22.1.8 的 ASan **不可用**（缺 `libclang_rt.asan_dynamic`，已实测登记） | ✅ 实测（3 资产）/ ⬜ sanitizer 替代待实测 |
| `wsl-clang-18.1.3` | WSL + clang 18.1.3：asan / ubsan（200 条分层抽样） | ✅ 实测（683-B1） |
| MSVC /analyze | 本机不存在 | ⬜ 待实测（诚实登记） |

**关键事实**：8 资产池本身**跨两个 OS**（3 个 Linux 运行时资产在 WSL，3 个编译/链接资产在 Windows）。
这不是缺陷而是被测对象的真实形态；但若不显式建模，"换环境"会同时改变多个组件——因此本设计
一律称 **environment-profile sensitivity**，**不称"OS 因果效应"**。

---

## Part 1 · 同 OS 换编译器（WSL 内 g++ ↔ clang，同 OS 同 flags）

**已有实测**（683-B1，n=200 分层抽样，seed 6831；判定字符串与 661 SAN 分支逐字一致）：

| 资产 | 一致率 | Cohen's κ | g++ catch% | clang catch% | Δ(clang−g++) | 差异条数 |
|---|---:|---:|---:|---:|---:|---:|
| asan | 93.5% | 0.864 | 32.5 | 33.5 | +1.0pp | 13 |
| ubsan | 93.5% | 0.843 | 24.0 | 26.0 | +2.0pp | 13 |

**本批补充（按家族分层 + 三组件口径，见 `689_environment_metrics.json`）**：
- Δcatch / Δunknown / Δconditional-recall 逐资产已计算（asan：Δunknown = +1.5pp，clang 侧 unknown 7/200 vs g++ 4/200）；
- 家族分层（asan+ubsan 池化格）：差异集中于 **stl 家族**（gcc 17/56 格 → clang 25/56 格，+14.3pp），
  其余家族 Δ 极小或为 0；**无家族级反转** ⇒ 93.5% 的一致率不是被单一家族拉高的。
- 结论口径：**编译器替换在 200 条抽样上只造成 ≤2pp 的检出漂移与 ≤1.5pp 的 unknown 漂移**；
  这是"环境敏感性有限"的**实测**证据（不得外推到其他环境对）。

**复算**：`python tools/environment_metrics_689.py`；原始数据 `data/683_b1_ckpt.jsonl`（200 条逐样本）。

---

## Part 2 · 部署环境变化（WSL profile ↔ native-Windows profile）

### 2.1 H1（静默退化）——**已量化，实测 + 口径推断混合**

事实链（数字全部来自 `688_reproducibility_quantification.json` 与 683 矩阵）：

| 口径 | 检出（真实 110） | unknown | 说明 |
|---|---:|---:|---|
| WSL 全 8 资产（主口径） | 59.09%（65/110） | 0%（样本级） | asan/ubsan/tsan 承担 39 个捕获（其中 asan 独占 18） |
| Native 跨平台资产并集（3 资产） | **23.64%（26/110）** | 0%（样本级） | 掉点 **−35.45pp**；**unknown 不上升** |
| WSL 资产级 unknown | — | asan/ubsan/tsan：0.9% | wunsequenced/compile-time：100%（恒不可用） |

**核心观察（评审要的"最强对比"的 A 侧）**：
> 在 **environment-unaware** 协议下，丢失的 sanitizer 能力被记为 `miss`，
> 于是 guard 保持"绿色"，而结论已从 59.09% 静默降为 23.64%——
> **没有任何机制会告诉读者"39 个捕获的测量根本没有执行"**。

**诚实边界**：23.64% 中，跨平台 3 资产的 verdict 是**实测**（它们在 Windows 上跑）；
但"若只在此 profile 下作结论"是**口径推断**（未在纯 Windows 上重跑全部流程）。
标注：混合证据，已在报告中显式声明。

### 2.2 H2（感知协议：显式 unknown / hard failure）——**设计，待执行**

**设计目标**：当运行环境不满足声明的 EnvironmentProfile 时，协议必须**拒绝产出"正常结论"**，
以两种方式之一暴露：
1. **资产级 unknown**：不可用资产记 `unknown`（不记 miss），并在输出中打印能力边界：
   `declared profile ⊃ available assets` 的差集清单；
2. **hard failure**：若声明的 profile 是测量语义的一部分（如同一样本跨 profile 对比），
   环境不匹配时直接以非零退出码终止（fail-loud），不产生任何"绿色"结论。

**最小实现（已可复现的演示，不需新环境）**：
- 已有 `REPRODUCE.md` + fail-loud 自检（676g 起落地）：错误环境抛错；
- 本设计补充要求：把"资产可用性清单"纳入每次运行的输出头（机器可读），
  并提供一个 `--profile-check` 模式用于 CI。

**待执行实验清单（含判定标准）**：

| # | 实验 | 方法 | 判定标准（预注册） | 状态 |
|---|---|---|---|---|
| E-env-1 | native sanitizer 替代可行性 | 安装 clang-cl（非 MinGW）或 MSVC，对 110 条真实样本跑 ASan/UBsan 替代 | 若替代可跑：报告替代资产在 110 条上的 catch 率与 WSL 版差异（±10pp 内视为可用替代）；若不可跑：登记为"当前声明环境外不可复现" | ⬜ 待执行（本机无 clang-cl/MSVC） |
| E-env-2 | MSVC `/analyze` 覆盖 | 对 110 条跑 `/analyze`，与 compiler-warn 对照 | 报告覆盖率与新增捕获数；不得与 sanitizer 混口径 | ⬜ 待执行 |
| E-env-3 | aware 协议演示（不需新环境） | 用 `environment_metrics_689.py` 的 aware/unaware 两套记账输出对照 | unaware：Δcatch=−35.45pp、Δunknown=0；aware：Δcatch=0 但新增 3 资产 unknown=100% 边界标记。**两者必须给出不同的结论文本** ⇒ 证明协议层可防静默退化 | ✅ 已演示（见 `689_environment_metrics_report.md` §2/§3） |
| E-env-4 | 容器化复现（Docker 化 WSL profile） | 把 WSL g++13.3 + clang18 + 3 资产的工具链固化进镜像，跑 110 条 | 镜像内复跑结果与 683 矩阵逐条一致（允许 unknown 差异 ≤1 条/资产）；镜像 sha256 落盘 | ⬜ 待执行（本机无 Docker，687 已登记） |
| E-env-5 | native 三资产复跑 QA | 用 MinGW g++ 13.1 对 110 条重跑 compiler-warn/linker，与 683 矩阵比对 | 逐条一致性 ≥95%；低于则登记为"跨运行不稳定"并并入威胁 T5 | ⬜ 待执行（预算内未跑；命令与口径已定） |

### 2.3 预期结论（供论文 Finding 3 使用）

1. **环境是测量的一部分，不是复现细节**：同 OS 换编译器 ≈ 无感（≤2pp）；换部署 profile ≈ 灾难性（−35.45pp、−60% 相对召回）；
2. **静默退化是协议缺陷而非环境缺陷**：问题的根源是"资产不可用 → miss"的默认记账；
3. **三组件指标是必要的最小口径**：只报 recall 会同时掩盖"分母缩小"（unknown 被剔除）与"能力丢失"（不可用被记 miss）。

---

## 3. 与论文的挂接（写作要点）

- §2 measurement tuple 的 `e`（environment profile）字段：字段表 + measurement_context_id 含 `hash(environment_profile)`；
- §5.3 Finding 3 引用：Part 1 的 93.5%/κ=0.864（实测）；Part 2 的 59.09→23.64（混合证据，标注）；
- §7 T3（environment validity）：WSL 硬依赖 + native 推断 + clang-cl/MSVC 待实测；
- 附录 C.3：三组件全表 + profile 字段表 + 本设计的 E-env-1..5 清单（含状态）。

## 4. 诚实边界（不得省略）

- native profile 的 sanitizer 缺失为**架构推断**（本机无 clang-cl/MSVC），不是实测替代；
- `windows-native-mingw` 的 3 资产虽是实测，但其"作为独立 profile 的完整复跑"未做（E-env-5 待执行）；
- 200 条 clang 对照是**分层抽样**（非全池），其 catch 率不可与全池数字直接比；
- E-env-4 的 Docker 化在 687 已登记"本机无 Docker 未实测"，本批不改变该状态。
