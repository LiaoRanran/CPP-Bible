# 方向 02：NeurIPS E&D 2025 录用论文全列表

## 核心结论
1. NeurIPS 2025 的 D&B track 接收率约 **25.3%**（主会议约 25.8%），延续"严格、非水"定位；2025 年 LLM 评测类论文占比进一步上升（NeurIPS 2025 blog retrospect 明确）。
2. 2025 官方索引：`neurips.cc/Conferences/2025/DatasetsBenchmarks/AcceptedPapers` 与 OpenReview `NeurIPS.cc/2025/Track/Datasets_and_Benchmarks`；本文件给代表样本 + 抓取法，非全量枚举。
3. 2025 年出现"AI 写作检测"争议（Pangram 分数 ≥90% 的 E&D 论文一年涨 10 倍），这对 QueYi 是**双刃剑**：审稿更警惕 AI 生成内容 → 你的"可验证人工构建 corpus"反成卖点。

## 精确数字与案例
- **接收率**：主会议 **25.8%**、D&B **25.3%**（来源：thepaper.cn 整理，及多个实验室录取通报）。NeurIPS 2025 总投稿约 **19,000+** 篇（行业估算，需以官方 fact sheet 为准）。
- **AI 写作污染信号（极重要）**：2026 年 NeurIPS 官方披露，E&D（原 D&B）track 中 Pangram AI 写作分数 ≥90% 的论文从 2025 到 2026 **增长 10 倍以上**；但官方承认检测对参数敏感（中尺寸检测窗口下，AI 分 90–100% 的论文占比从 42.7% 降到 12.7%）。→ 说明：靠 LLM 代写稿在 E&D 会被重点排查。
- **官方索引**：
  - 录用页：`https://neurips.cc/Conferences/2025/DatasetsBenchmarks/AcceptedPapers`
  - OpenReview：`https://openreview.net/group?id=NeurIPS.cc/2025/Track/Datasets_and_Benchmarks`
  - 第三方整理：`https://legacy.papercopilot.com/paper-list/neurips-paper-list/neurips-2025-accepted-paper-list-datasets-benchmarks-track/`
- **代表趋势论文（公开已知 D&B 系列，年份以官方页为准）**：
  - *BigCode* / *StarCoder 2* 相关数据（代码语料，与 QueYi 邻近）。
  - *LiveCodeBench*（持续更新的代码评测基准，污染控制思路与 QueYi 盲 holdout 同源）。
  - *HELM / HELM Lite*（标准化评测，强调可复现）。
  - *MDK12* / 多模态评测集（2025 增长显著）。
  - 大量"LLM-as-judge 校准"与"benchmark contamination"论文。

## 对阙疑的 3 条具体行动
1. **抓 2025 全列表**并筛"代码/编译/程序分析/AI 评测校准"关键词，存 `_arch_v45/cache/2025_db_titles.md`；与 2024 列表做差集，看赛道是否变拥挤。
2. **把"人工可验证 corpus"写成抗 AI 污染卖点**：在 related work 里直接引用 2025–2026 AI 写作污染数据，说明 QueYi 的 452 账本 + append-only 链是"人构建、机器可验"而非 LLM 生成。
3. **对标 LiveCodeBench 的污染控制**：在其基础上指出 QueYi 用"真实缺陷夹具 15 条重注入 100% 检出"作为 contamination-proof 证据，比单纯去重更强。

## 盲区（诚实标注）
- 未逐条枚举 2025 D&B 全部标题；总投稿 19,000 为行业估算，需官方 fact sheet 确认。
- "AI 写作 10 倍增长"来自 2026 官方披露文章（baijiahao 转述），原始数据应在 NeurIPS 2026 官方博客/政策页，建议抓原文核实百分比口径。
- 2025 是否已有"程序验证"类 D&B 论文需全列表抓取后确认。

## 来源
- [1] NeurIPS 2025 D&B Accepted Papers — https://neurips.cc/Conferences/2025/DatasetsBenchmarks/AcceptedPapers
- [2] NeurIPS 2025 D&B OpenReview — https://openreview.net/group?id=NeurIPS.cc/2025/Track/Datasets_and_Benchmarks
- [3] 2025 接收率 25.8%/25.3% — https://www.thepaper.cn/newsDetail_forward_31522850
- [4] AI 写作污染 10 倍增长 — https://baijiahao.baidu.com/s?id=1877363176757481927
- [5] PaperCopilot 2025 D&B 整理 — https://legacy.papercopilot.com/paper-list/neurips-paper-list/neurips-2025-accepted-paper-list-datasets-benchmarks-track/
