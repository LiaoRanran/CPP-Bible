# 689-D1 · 公平外部对比方案（Fair Comparison Protocol）

- 生成：2026-10-07｜批次：689｜执行：CodeBuddy（AI）
- 上游：`data/688_E9_fair_recomputation.md`（688-B3）、`data/673e_clang_tidy_cppcheck对比.md`（既有对照）、
  `data/683_real_world_*`（真实靶场）
- 定位（**最重要的一句**）：本对比是 **convergent validity / cross-regime stress-testing**，
  **不是 leaderboard，不 claim superiority over mature verifiers**。

---

## 1. 为什么要重写这节（评审与 686 的指控）

既有 E9 有三个被明确点名的缺陷：
1. **非同环境**：clang-tidy 在 Windows-MinGW，cppcheck 在 WSL，Queyi FD 依赖 WSL g++ + sanitizer ——
   三者不共享编译器/OS；"同一环境"在方法论上不可达；
2. **主口径失败**：预注册的 clang-tidy 四检查族口径给出 100% 召回 + 100% 假阳（零判别力），
   暴露了预注册设计缺陷；
3. **事后选口径**：唯一"可辩护"的 StrictA（仅 `clang-analyzer-*`）是**看到结果之后**选的 ⇒ 探索性。

## 2. 公平性要求清单（评审 8 条）与本项目现状

| # | 要求 | 现状 | 处置 |
|---|---|---|---|
| F1 | identical samples | ✅ 41 holdout / 64 corpus 同一批 | 保留 |
| F2 | identical truth labels | ✅ 同一标签集（单标注者，已列为 T1 威胁） | 保留 + 指向 C 任务的人类标注 |
| F3 | same execution environment where technically possible | ❌ **不可达**（静态 vs 动态、MinGW vs WSL 本质不同） | 如实声明；不做"假统一" |
| F4 | predeclared detector configurations（禁止事后选 best） | ❌ 主口径失败、StrictA 事后选 | 两者**都报**，并明确标注探索性；未来预注册 |
| F5 | identical timeout/resource rules | ⚠️ 部分（超时口径不同家） | 报告各自口径；不做时间归一 |
| F6 | unknown kept distinct from miss | ✅ Queyi 侧严格；外部工具无 unknown 概念 | 外部工具的"无报告"记为 miss，并在口径表注明不对称 |
| F7 | per-defect-family results | ⚠️ 部分（按类型有；家族级可补） | 补家族级对照（见 §4） |
| F8 | false-positive controls（clean 对照组） | ✅ Queyi 有 11 条对照（FP=0）；外部工具未跑对照 | 标为"仅 Queyi 侧有 FP 控制"，记为不对称 |

## 3. 对比对象与可行性判定

| 工具 | 版本/环境 | 可否统一环境 | 处置 |
|---|---|---|---|
| clang-tidy（`clang-analyzer-*`） | LLVM 22.1.8 / Windows-MinGW | 不可（MinGW 无 sanitizer 侧的 FD 对照环境） | **观察性对比**（沿用 673e 数据） |
| cppcheck | 2.13.0 / WSL | 不可（与 FD 同 OS 但静态/动态本质不同） | **观察性对比** |
| SV-COMP 工具（如 UAutomizer、Symbiotic） | 各自镜像 | 不可（需竞赛基础设施与任务格式） | **不实测**；只做定位对比（见 `689_svcomp_positioning.md`） |
| 统一环境重跑 | — | 本批**不重跑**（红线：不改检测器/不做新实验） | 写方案（§5） |

**已可引用的既有结果（口径必须随数字一起引用）**：
- StrictA holdout（事后口径，探索性）：FD 82.9%（34/41） vs clang-analyzer 48.8%（20/41），
  配对 (b,c)=(14,0)，McNemar p=1.2×10⁻⁴，Δ=+34.1pp [19.6, 48.7]；
  **注意 c=0 意味着工具检出是 FD 检出的子集**——这是"观察"不是"更优证明"；
- corpus：FD 62.5% vs cppcheck 54.7%，(b,c)=(13,8)，**p=0.383 不显著**；
- **8 条反向对**（cppcheck 检出而 FD 未检出）全部落在"未初始化变量/重复释放"类——
  **FD 的真实短板，保留为诚实证据**；
- 主口径零判别力（100%/100%）如实保留为"预注册失败"的案例。

## 4. 家族级对照（本批可补，只读既有数据）

**待补**（成本低，若执行）：按 family8 汇总 FD vs clang-tidy/cppcheck 的逐家族命中；
若 673e 数据不足以定位到家族，则明确标注"数据不支持家族级拆分"。
**注意**：本批**未**新增对照运行；若 673e 产物不含逐样本工具结果，本节以"不可拆"结论收尾并登记。

**结论（本批实况）**：273e/688 的产物为**汇总级**（召回/配对计数/反向对清单），
**不含逐样本工具 verdict** ⇒ 家族级拆分不可行，如实登记为限制；
该缺口列入 §5 方案（未来预注册时要求逐样本落盘）。

## 5. 未来公平重跑方案（预注册草案，含判定标准）

前提：把三方迁到同一容器（Ubuntu 22.04 + g++ 13 + clang 18 + cppcheck 2.13 + clang-tidy 18）。

| 步骤 | 内容 | 判定标准 |
|---|---|---|
| P1 | 冻结工具配置清单（检查族、超时、资源限制）并预注册 | 配置清单先于任何结果落盘（时间戳可核） |
| P2 | 对 41+64+110 三个样本集，三方各跑一遍，**逐样本落盘** verdict + 原始输出 | 逐样本文件可复算汇总 |
| P3 | unknown 语义：外部工具"无报告"记 miss；FD 侧保留 unknown | 口径表随结果一起发布 |
| P4 | 家族级 + 类型级对照表；FP 对照（11 条 clean）三方都跑 | 报告 FP/TP 双向 |
| P5 | 预注册主口径 + 全部敏感性口径**一次性**列出（含事后口径，标探索性） | 禁止只报赢的口径 |
| P6 | 结论限定为 convergent validity：三方在哪些家族收敛/发散 | 不写"优于" |

## 6. 对论文的措辞规范（写死）

- 标题用 **"Cross-regime observational comparison (convergent validity)"**；
- 允许写：FD 在内存安全族上与 clang-analyzer 收敛（且 c=0 子集关系）、在 corpus 上与 cppcheck 打平、
  在"未初始化/重复释放"上有 8 条反向对（短板）；
- **禁止**写：FD 优于/胜过/超过任何成熟验证器；禁止把跨环境数字当同环境对比；
- 禁止把 StrictA（事后口径）当主结论；主口径失败必须与 StrictA 并排出现。

## 7. 诚实边界

- 本批**未重跑任何外部工具**（红线）；全部内容是对既有 673e/688 数据的重解读 + 预注册方案；
- 环境不可统一是**方法论事实**（静态 vs 动态、Windows vs WSL），不是配置疏忽；
- SV-COMP 类工具未比较（任务格式/基础设施不同），只做定位（见 D2）。
