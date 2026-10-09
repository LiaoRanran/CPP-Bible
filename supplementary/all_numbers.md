# 关键数字总表（supplementary/all_numbers.md）

> 来源：676f–703 各批次报告与冻结 JSON 产物。每个数字标注「来源批次 + 文件 + 复算状态」。
> 复算状态：`✓ 本批已复算` = 704 用冻结产物实际跑过复算脚本；`reported` = 取自批次报告（未重跑）。
> 复算口径见 `data/704_number_recomputation_results.md` 与 `data/704_verify_paper_numbers.json`。

## A. 头条数字（论文主结论）

| 数字 | 含义 | 来源批次 | 文件 | 复算状态 |
|---|---|---|---|---|
| **+24.03pp** | A5 主端点 FD−Random 增益（k=4, 评估集 n=566） | 676f | `data/a5_676f_results.json` / `data/676f_A5重跑报告.md` | ✓ 本批已复算（FD 309 vs Random 173，Δ=136/566） |
| **38.4%** | 检测器盲区率（440/1147，instrument-boundary） | 676g / 681 | `data/blindspot_676g_stats.json` | ✓ 本批已复算（R6: 440/1147=0.3836） |
| **59.09%** | 真实 CVE 重构样本检出率（65/110） | 683 / 689 | `data/683_real_world_detection_matrix.json` | ✓ 本批已复算（or_catch_rate 59.0909） |
| **60.07% → 24.74%** | 环境画像敏感性（WSL→native，A5 评估集 n=566，−35.34pp） | 692 / 703 | `data/703_zero_cost_validation.json` | ✓ 本批已复算（E1 60.0707 / E2_unaware 24.735） |
| **κ=0.727** | Cohen's κ（defect_type，AI 二次标注自一致，n=287） | 682 | `data/682_kappa.json` | ✓ 本批已复算（0.726674） |

## B. A5 与检出率（676f）

| 数字 | 含义 | 来源批次 | 文件 | 复算状态 |
|---|---|---|---|---|
| 1137 样本 × 8 资产 = 9096 判定格，缺格 0、error 0 | 全量跑得动 | 676f | `data/676f_A5重跑报告.md` | reported |
| 54.59% (309/566) | FD 贪心 k=4 检出率 | 676f | `data/a5_676f_results.json` | ✓ 本批已复算（R1） |
| 30.57% (173/566) | 预注册随机单点基线 | 676f | `data/a5_676f_results.json` | ✓ 本批已复算（R1） |
| 24.74% (140/566) | Static 基线 | 676f | `data/a5_676f_results.json` | ✓ 本批已复算（R1） |
| 60.07% (340/566) | 全池 OR 检出 | 676f | `data/a5_676f_results.json` | ✓ 本批已复算（R1） |
| 95% CI [+20.51, +27.55]；McNemar p≈2.3×10⁻⁴¹ (b=136,c=0) | 主端点显著性 | 676f | `data/676f_A5重跑报告.md` | reported |
| +29.41pp（p=1.95×10⁻³，CI [+14.10,+44.73]） | 外部效度（planted=false 真实缺陷子集 n=34） | 676f | `data/676f_A5重跑报告.md` | reported |
| FD 资产集 = {asan, cross-compile, tsan, ubsan} | 贪心 k=4 选择 | 676f | `data/a5_676f_results.json` | ✓ 本批已复算（R3） |
| 退化资产 = {compile-time, wunsequenced} | 全 unknown 资产 | 676f | `data/a5_676f_results.json` | ✓ 本批已复算（R5） |

## C. 盲区与单检测器（676g / 676l / 681）

| 数字 | 含义 | 来源批次 | 文件 | 复算状态 |
|---|---|---|---|---|
| 1147 样本 / 70 缺陷类型（676g）→ 34 规范类型（681） | 测量规模 / 口径归一化 | 676g / 681 | `data/blindspot_676g_stats.json` / `data/681_类型统计重算报告.md` | reported |
| 707/1147 检出（61.6%） | 单资产 OR 并集 | 676g | `data/blindspot_676g_stats.json` | ✓ 本批已复算（R7: 61.6%） |
| 35.6% / 23.5% / 22.9% | 单资产最大覆盖 asan/ubsan/tsan | 676g | `data/676g_检测器盲区地图报告.md` | reported |
| 13/34 类型 >50% 盲 | 类型级盲区 | 681 | `data/681_类型统计重算报告.md` | reported |
| 94.21% (635/674) | 8 资产 OR（分母 expected=catch，旧矩阵） | 676l | `data/676l_单检测器性能报告.md` ⚠️ | reported（注意：此为旧冻结矩阵 674/473，当前矩阵为 640/507） |
| asan Recall 58.50% / Precision 95.34% / F1 72.51% | 最强单资产 | 676l | `data/676l_单检测器性能报告.md` | reported |

## D. 标注一致性 / 环境 / 真实靶场（682 / 692 / 693 / 689）

| 数字 | 含义 | 来源批次 | 文件 | 复算状态 |
|---|---|---|---|---|
| κ=0.437 (expected_verdict)；κ=0.789 (planted)；κ=0.157 (severity, n=262) | 其他维度 κ | 682 | `data/682_kappa.json` | ✓ 本批已读 |
| 287 条（25% 分层抽样，seed=6821） | IAA 抽样规模 | 682 | `data/682_标注一致性报告.md` | reported |
| 75.265%（426 条重分类） | aware 记账 unknown 率 | 692 / 703 | `data/703_zero_cost_validation.json` P2 | ✓ 本批已复算 |
| 94.12% / 97.40% | clang-tidy T1 conditional recall / false-report rate | 692 | `data/692_fair_comparison_report.md` | reported |
| 566 eval 帧（catch 322 / miss 244） | 公平对比评估规模 | 692 | `data/692_fair_comparison_report.md` | reported |
| 96.25% / 87.5% | LLM prompt 不变性（glm-4-flash / glm-4.5） | 692 | `data/692_llm_audit_report.md` | reported |
| n=1147（sha256 清单 14 项 missing 0） | 矩阵完整性 | 693 | `data/693_data_integrity.json` | reported |
| 110 CVE 重构候选（commit 22 / 处理 20 / 取源 13 / 构建 0） | 真实靶场规模 | 693 | `data/693_original_repo_cve_report.md` | reported |
| 人类 IAA A vs B = 78.6% / κ=0.495（去 13 条 leak 后 77.3% / κ=0.458） | 人类标注（仍 pending） | 693 | `data/693_human_iaa_report.md` | reported |
| FD 54.5936%；随机分布 mean 40.1913% / SD 9.2521pp | 元评估帧 n=566 | 693 | `data/693_meta_evaluation_report.md` | reported |
| ECE 0.3812 (n=292, LLM) vs 0.419 (n=3363, 检测器) | 校准 | 693 | `data/693_meta_evaluation_report.md` | reported |

## E. 理论 / 零成本验证（700 / 703）

| 数字 | 含义 | 来源批次 | 文件 | 复算状态 |
|---|---|---|---|---|
| 7 条公理仅 A2/A5 独立（4096 结构域穷举） | 元理论 | 700 | `data/700_metatheory.md` | reported |
| φ_max=32.3222pp，d*=10.16，R²=0.999724 | 相变拟合 | 700 | `data/700_phase_transition.md` | reported |
| Type I n=849 / Type II n=17 / Type III=∞ / Type IV=∞ | 配对设计可检类型 | 700 | `data/700_information_theory.md` | reported |
| P1：检出率 Δ=0.000000pp，构成膨胀 0.4602→0.0000 | 零成本改进 | 703 | `data/703_zero_cost_validation.json` | ✓ 本批已读 |
| P2：60.0707%→24.7350%（Δ−35.3357pp） | 零成本验证 | 703 | `data/703_zero_cost_validation.json` | ✓ 本批已复算 |
| 44.17% 一致率 / 55.83% 结构性 Goodhart | JudgeBench | 703 | `data/703_大批次验收报告.md` | reported |

## F. 数字对账汇总（704 本批）

`tools/verify_paper_numbers.py` 对 v1.1 主稿审计结果：
- 检察 **130 条**；`missing 0`；`consistent 116`；692 批次自洽 **35/35 PASS**；退出码 **0**。
- 数字 token 1860；未归类 156（引用年份 / 排版参数等非结论数字）。
- 输出：`data/704_verify_paper_numbers.json` / `data/704_verify_paper_numbers_report.md`。

> ⚠️ 口径提示：C 节 `676l` 的 94.21% 基于**旧冻结矩阵（catch 674 / miss 473）**；当前冻结矩阵为 **catch 640 / miss 507**（差 34 = 676m 修正的挂起样本）。引用该列时请以 `data/704_number_recomputation_results.md` 的当前口径为准（asan 61.65% 等）。
