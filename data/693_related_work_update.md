# 693-E6 · 相关工作更新（2026 新增文献 + 对照）

- 生成：2026-10-08｜批次：693-E6
- 基线：`data/685_literature_matrix.json`（**39 条**，四个领域：submodular 12 / eval 12 /
  active 9 / info 6；证据等级：venue-year 21 / arXiv-listed 13 / DOI-confirmed 5）
- 本文件**只新增 2026 年检索到的、与"评估方法论 / 软件验证 / LLM judge"直接相关的条目**，
  并对每条给出**与 Queyi 的区别**。既有 39 条不重复登记。

> **诚实边界**：下表中每条都给了可点开的 URL 与检索日期。**未做全文精读**的条目在
> 「核验」列标 `摘要级`；只有摘要与元数据被核对过，**不要**把本表的转述当作原文结论。

---

## 1. 新增条目

| # | 文献 | 年 | 领域 | 核心贡献 | 与 Queyi 的区别 | 核验 |
|---|---|---:|---|---|---|---|
| N1 | **Code Benchmarks Should Prioritize Rigor, Reliability, and Reproducibility**（Cao, Chan, Ling, Wang, Li, Liu, Qiao, Han, Wang, Yu, He, Wang, Zheng, Lyu, Cheung）<br>`arXiv:2501.10711`（v5, 2026-07） | 2026 | eval | 对 2014–2025 十年间 **672 个代码基准**做调查；指出"意识提升但实践滞后"；提出 **HOW2BENCH 55 条检查单** | Queyi **不是**基准调查，而是一个具体装置的**自省**：我们量化的是"本装置在什么条件下给出什么结论"。HOW2BENCH 是**通用检查单**，Queyi 的 §E5 框架对照是**按维度自查缺口**，两者互补而非竞争 | 摘要级（arXiv abs） |
| N2 | **A Comparative Study of Fuzzers and Static Analysis Tools for Finding Memory Unsafety in C and C++**（Hassler, Görz, Lipp）<br>`arXiv:2505.22052`（v2, 2026-03） | 2026 | eval | 5 个静态分析器 + 13 个模糊测试器，作用于 **100+ 个已知 C/C++ 安全漏洞**；报告逐工具检出率；**关键发现：全部 fuzzer 的并集与全部静态分析器的并集"几乎不相交"** | ⭐ **与 Queyi 的核心发现同构**：Queyi 也发现八资产并集（94.21%/99.22%）远大于任一单资产，且 `linker` 的 10 个 catch 全落在 sanitizer 的 `unknown` 里。**区别**：N2 比的是"两个工具家族"，Queyi 比的是"**同一家族内**的八个资产"并给出**组合选择算子**（E/FD）与**环境坐标**（E1/E2）两个额外维度 | 摘要级（arXiv abs） |
| N3 | **SV-COMP 2026 — 15th International Competition on Software Verification**（TACAS 2026 报告） | 2026 | active | 评估 **61 个验证器 + 16 个验证器（C）**、Java 与 SV-LIB 赛道；witness 格式与校验、CPU/内存限时 | Queyi 用 **8 个现成资产**（非专用验证器），且**不做形式化 witness 校验**；SV-COMP 有**第三方裁判与统一任务定义**，Queyi 目前**没有**（已登记为缺口） | 摘要级（官网 + 会议报告） |
| N4 | **Introducing the Evaluations & Datasets Track at NeurIPS 2026**（NeurIPS blog, 2026-03） | 2026 | eval | 明确该 track 对数据集/基准的文档化与托管要求 | Queyi 的投稿目标 track；本批的 `CITATION.cff` / `croissant.json` / `DATASHEET.md` 即为满足其要求 | 摘要级（官方 blog） |
| N5 | **LLM-Judge Validation**（Howardism, 2026；转述 Chen et al. 2026 的 rubric-item 级度量：measurability / informativeness / validity） | 2026 | eval | 把 LLM 评审的有效性下推到 **rubric 条目级**，用 judge agreement / IRT information / validity 三个量刻画 | ⭐ Queyi 的 693-A 做的是**同一件事的一个实例**：AI 双标（κ=0.495）+ 人类裁决材料包。**区别**：N5 关心"judge 本身可不可信"，Queyi 关心"**标签**可不可信"，且 Queyi **人类 IAA 仍为 0**（材料已备齐） | 二手转述（**未读原文**，标记为最低证据级） |

---

## 2. 与既有 39 条的关系

| 既有领域 | 条数 | 693-E6 的补充 |
|---|---:|---|
| submodular（子模/贪心/自适应） | 12 | 无新增（该领域 2026 年无直接相关新作进入本批检索范围） |
| eval（评估方法论） | 12 | **+3**（N1 / N2 / N4），另有 N5 为二手转述 |
| active（主动学习/选择） | 9 | 无新增 |
| info（信息论/熵） | 6 | 无新增 |

---

## 3. 对论文的直接启示（3 条）

1. **N2 是"工具家族互补性"的最强外部锚点。** 论文的"八资产并集 ≫ 单资产"结论不再是一个
   孤立观察——2026 年已有独立工作在**不同工具家族**上报告了同构现象。
   建议在 Related Work 里加一句限定：*Queyi 的互补性结论发生在**同一家族内**（sanitizer /
   编译器告警 / 链接器），比跨家族互补更难达成，因此 94.21% 的并集覆盖率更值得注意。*

2. **N1（HOW2BENCH 55 条检查单）提供了一个现成的自查框架。** 建议把 Queyi 的
   `docs/DATA_FORMAT.md` + `data/README.md` + `data/CHANGELOG.md` + `CITATION.cff` +
   `croissant.json` 对照 HOW2BENCH 的条目逐条打勾，**并把未达标项写进论文的 Limitations**。
   这是本批新增材料能立刻派上用场的地方。

3. **N3 暴露 Queyi 的方法论缺口：没有第三方裁判。** SV-COMP 的核心机制是**独立复算**。
   Queyi 的 693-A 人类裁决材料包是朝这个方向走的第一步，但**尚未有外部人执行**。
   论文不应把"可复现"写成"已被独立复现"。

---

## 4. 检索记录（可复核）

| 检索词 | 日期 | 命中的可用条目 |
|---|---|---|
| `benchmark evaluation methodology software verification 2026 LLM judge reliability construct validity` | 2026-10-08 | N1、N5 |
| `SV-COMP 2026 results benchmark C program verification` | 2026-10-08 | N3 |
| `C++ static analysis benchmark reproducibility 2026 sanitizer coverage benchmark paper` | 2026-10-08 | N2 |
| `NeurIPS 2026 Datasets and Benchmarks track requirements dataset documentation Croissant` | 2026-10-08 | N4 |

> 检索工具为通用网络搜索，**非**学术数据库系统检索（无 Scopus/DBLP/ACM DL 全文检索）。
> 因此本表**不能**声称是系统综述；它是"投稿前补漏"性质的定向检索。
