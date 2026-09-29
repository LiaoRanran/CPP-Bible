# 方向 03：NeurIPS E&D 审稿标准详解（从 OpenReview 看）

## 核心结论
1. E&D（原 D&B）审稿维度与传统 ML track 一致：**Quality / Clarity / Significance / Originality** 四项打分（各 1–10），但额外强调"数据集/基准的可用性、文档、许可、可复现性、偏差与代表性"——这正是 QueYi 的优势区。
2. 2026 官方《Evaluations and Datasets Reviewer Guidelines》明确写道：**作者坦诚局限应被奖励而非惩罚**，并鼓励审稿人用"NeurIPS Paper Checklist"评估；对 QueYi 这种承认检出率 CI 宽（28.4%–99.5%）的工作是利好。
3. OpenReview 公开记录显示：rebuttal 后评分可大幅变动（见方向 04），且 Area Chair 有权在 reviewer 全正面时仍因"控接收率"拒稿——意味着**initial score 不是终局**，写作清晰度与 checklist 完整度直接影响命运。

## 精确数字与案例
- **四维打分**：OpenReview 上 NeurIPS 每篇含 `Rating`（整体）、`Confidence`（审稿人置信度 1–5）、以及 Quality/Clarity/Significance/Originality 分项（每维 1–10，部分年份合并为整体 1–10 + 分项）。
- **接收率锚点**：主会议 ~25.8%、D&B/E&D ~25.3%（2024/2025），说明门槛高。
- **2026 官方指南要点**（`nips.cc/Conferences/2026/EvaluationsDatasetsReviewerGuidelines`）：
  - "answering 'no' to some checklist questions is typically **not** grounds for rejection."
  - "authors should be rewarded rather than punished for being up front about the limitations."
  - 鼓励用 Paper Checklist（数据来源、许可、计算成本、社会影响）作为审稿工具。
- **D&B 专属评审关注（来自 2024 CFP + *State of Data Curation*）**：
  - 数据集创建过程是否透明、可审计；
  - 许可与再分发合规；
  - 代表性偏差（谁被包含/排除）；
  - 与现有基准的增量是否清晰；
  - 是否附可运行 artifact（代码+数据）。
- **OpenReview 实证**：NeurIPS 2024 D&B OpenReview 中可见论文 rebuttal 后"two clear accepts and one accept"；NeurIPS 2023 有 reviewer 因 rebuttal 把评分从 **4 提到 7**（来源：知乎对 OpenReview 低分转高分案例的整理）。

## 对阙疑的 3 条具体行动
1. **对齐 Paper Checklist 写"局限"段**：主动写明盲 holdout 仅 20 样本（CI 28.4%–99.5%）、外部 corpus 仅 33.3% 检出——按 2026 指南，这会被奖励而非扣分；同时写清"为何仍可信"（重注入 100%、哈希链可审计）。
2. **把四维打分映射到 QueYi 卖点**：
   - Quality：变异测试 core 97.3%/all 81.5% + 重注入 100%；
   - Clarity：四态判决 + 附录可运行 demo；
   - Significance：首次把"知识验证"做成可审计基准；
   - Originality：append-only 哈希链 + Merkle checkpoint（区别于普通 PBT）。
3. **提交前自检清单**：对照 2026 指南逐条过"数据来源/许可/可复现/偏差"，并在 supplementary 放 813 行内核 + 452 账本 + 9 保护器，让 reviewer 一键复现 0.59ms/卡。

## 盲区（诚实标注）
- 我未直接读取 OpenReview 2026/2027 评分细则原文（web_fetch 被网络策略阻断），以上来自搜索摘要 + 历年指南推断；**应抓 `nips.cc/Conferences/2026/EvaluationsDatasetsReviewerGuidelines` 原文核对四维权重**。
- 2027 E&D 是否沿用 2026 "Evaluations and Datasets"命名、是否新增 AI 披露硬性要求，需等 2027 CFP（约 2027-05 前后）发布。

## 来源
- [1] 2026 E&D Reviewer Guidelines — https://nips.cc/Conferences/2026/EvaluationsDatasetsReviewerGuidelines
- [2] 2024 D&B Reviewer/CFP — https://neurips.cc/Conferences/2024/CallForDatasetsBenchmarks
- [3] OpenReview 2024 D&B — https://openreview.net/group?id=NeurIPS.cc/2024/Track/Datasets_and_Benchmarks
- [4] Rebuttal 4→7 案例 — https://zhuanlan.zhihu.com/p/2064466275745653337
- [5] 2024/2025 接收率 — https://www.thepaper.cn/newsDetail_forward_31522850
