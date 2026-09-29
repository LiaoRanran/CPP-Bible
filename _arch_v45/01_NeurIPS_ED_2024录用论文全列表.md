# 方向 01：NeurIPS E&D 2024 录用论文全列表

## 核心结论
1. NeurIPS 2024 的 D&B（Datasets & Benchmarks，即本 brief 的 E&D 前身）track 接收率约 **25.3%**，与主会议 25.8% 基本持平，说明评审同等严格、并非"水 track"。
2. 2024 年 D&B 官方录用页（`neurips.cc/Conferences/2024/DatasetsBenchmarks/AcceptedPapers`）是**唯一权威全列表**；本文件给出代表性样本 + 精确抓取方法，未逐条枚举全部标题（盲区见下）。
3. 对 QueYi 最值得关注的是 2024 年出现的"数据策展审计"类论文（如 *The State of Data Curation at NeurIPS*），它们证明 E&D 高度看重**数据集/基准的开发流程透明度**——这正是 QueYi 的 append-only 哈希链 + Merkle checkpoint 可直接对标的点。

## 精确数字与案例
- **规模**：NeurIPS 2024 总投稿约 **15,600** 篇（Appier 新闻稿引述），其中 D&B track 单独审稿；D&B 接收率 **25.3%**（来源：thepaper.cn 对 2024/2025 接收率的整理，及 Appier 引述的 25.3%）。
- **官方索引**：
  - 录用页：`https://neurips.cc/Conferences/2024/DatasetsBenchmarks/AcceptedPapers`
  - OpenReview：`https://openreview.net/group?id=NeurIPS.cc/2024/Track/Datasets_and_Benchmarks`
  - Proceedings：`https://proceedings.neurips.cc/`（2022 起 D&B 并入主会议）
- **代表录用论文（方向与 QueYi 相关，年份以官方页为准，以下为公开已知的 D&B 系列代表作，非 2024 全量）**：
  - *DataComp*（2023 D&B）：用 12.8B 图像池做数据集蒸馏，开创"数据为中心"基准。
  - *Dolma*（2024 D&B）：3T token 开放语料，附完整策展文档。
  - *FineWeb / FineWeb-Edu*（2024）：去重 + 教育过滤的 15T token 语料。
  - *OLMo*（2024）：完全开放的训练数据 + 模型 + 日志。
  - *The Stack / The Stack v2*（2023/2024）：代码语料，与 QueYi 的 C++ 代码验证最邻近。
  - *The State of Data Curation at NeurIPS*（2024）：直接审计 D&B track 的数据集开发实践——**最该精读**。
  - *LiveBench*（ICLR 2025，但同源思路）：污染受限基准，对 QueYi 的"盲 holdout 防污染"设计有直接参考。
- **关键趋势**：2024 D&B 论文大量引入"新数据集作为 benchmark/evaluation 贡献的一部分"，且 LLM 评测占比显著上升（NeurIPS 2025 blog  retrospect 也确认此趋势延续）。

## 对阙疑的 3 条具体行动
1. **抓全列表**：用脚本抓 `neurips.cc/Conferences/2024/DatasetsBenchmarks/AcceptedPapers` 的标题+作者，存到 `_arch_v45/cache/2024_db_titles.md`；重点筛出"代码/编译/程序分析/基准评测"关键词的 5–10 篇，逐篇读 abstract。
2. **对标 *The State of Data Curation at NeurIPS***：把 QueYi 的"哈希链不可篡改 + Merkle checkpoint 可审计"写成一段 200 词的"数据策展透明度"卖点，直接对齐该文提出的评审关注点。
3. **建对照表**：在稿子里加一张表，列 3 篇最相关 D&B 论文的"数据集规模/可复现性声明/许可"，并指出 QueYi 在哪几项上更强（如 append-only 可验证性）。

## 盲区（诚实标注）
- 我**未逐条枚举** 2024 D&B 全部录用标题（估计 200+ 篇），仅给代表样本 + 权威源；完整枚举需抓官方页（已列为行动 1）。
- 部分代表论文的精确录用年份来自公开记忆，可能与官方页有 ±1 年偏差，以 `proceedings.neurips.cc` 为准。
- 2024 D&B 是否含"程序验证/编译"类论文需抓全列表后才能确认；若为空，则说明 QueYi 的 C++ 验证细分赛道竞争极小（利好）。

## 来源
- [1] NeurIPS 2024 D&B Accepted Papers — https://neurips.cc/Conferences/2024/DatasetsBenchmarks/AcceptedPapers
- [2] NeurIPS 2024 D&B OpenReview — https://openreview.net/group?id=NeurIPS.cc/2024/Track/Datasets_and_Benchmarks
- [3] NeurIPS 2024 总投稿 15,600 / D&B 25.3% — Appier press, 2024-10-17
- [4] 2024/2025 接收率整理 — https://www.thepaper.cn/newsDetail_forward_31522850
- [5] The State of Data Curation at NeurIPS — NeurIPS 2024 D&B（proceedings.neurips.cc）
- [6] LiveBench — ICLR 2025, https://iclr.cc/virtual/2025/poster/28134
