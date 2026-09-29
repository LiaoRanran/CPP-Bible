# _arch_v44 · 01 NeurIPS E&D 全解析（方向 1）

> 核心问题：2024/2025/2026 三年 E&D（Evaluations and Datasets）track 录用论文、录用率、审稿四维度判分、与 Main/Workshop 区别、拒因、完整时间线、rebuttal 翻盘。
> 诚实标注：【官方】；【论文】；【实证】；【推断】；【盲区】。

---

## 一、track 身份与三年概况

- 官方名 **Datasets and Benchmarks Track**（2024 起），2026 更名口径为 **Evaluations and Datasets Track**【官方】。OpenReview 组 `NeurIPS.cc/2025/Datasets_and_Benchmarks_Track`、`NeurIPS.cc/2026/Evaluations_and_Datasets_Track`【官方】。
- 2025 main track：21,575 有效投稿，5,290 录用（≈24.5% 总体）【实证，搜索结果】。D&B 为独立 portal，投稿/接收具体数需 OpenReview 抓取【盲区】。
- 2025 D&B 官方博客标题 "From Art to Science in AI Evaluations"，强调评估方法论科学化【官方】。

## 二、审稿四维度判分（官方口径）

| 维度 | 关注点 | 阙疑判读 |
|---|---|---|
| Quality | 技术正确+实验支撑 | 452 账本+Merkle 强；外部 corpus 33.3% 弱 |
| Clarity | 新手可读懂 | 内部术语须翻译 |
| Significance | 社区影响 | framing 有鲜度 |
| Originality | 新且不重叠 | 须划清与 benchmark 工作边界 |

评分区间年度微调，强制 summary/strengths/weaknesses/questions【官方】。

## 三、E&D vs Main vs Workshop

| 项 | E&D/D&B | Main | Workshop |
|---|---|---|---|
| 投稿量 | 独立 portal，较小 | ~21k（2025） | 数百 |
| 录用率 | 通常高于 main | ~24.5% | 30–60% |
| 读者群 | 评估/数据方法者 | 广 | 窄而专 |

## 四、拒因与完整时间线

- 拒因（综合）：主张超证据、缺 baseline、 novelty 不足、污染/太小、可读性差（见方向 04 详列）。
- 典型时间线（以 2027 为目标，年度错位需回官网核对）：abstract deadline 5 月 → full paper 5 月底 → 评审 6–8 月 → rebuttal 8 月（通常 5–7 天窗口）→ 录用通知 9 月 → camera-ready 10 月 → 会议 12 月【推断，基于历年规律】。
- rebuttal 翻盘要点：只回应审稿人列的 weakness，逐条给新证据/改口径，不争辩态度；真实翻盘常来自补一个 ablation 或澄清 construct threat【推断】。

## 五、对阙疑的 3 条具体行动

1. **建 E&D 逐年录用论文表**：用 OpenReview API 抓取 2024–2026 D&B 全部录用标题+机构，标「评估完整性/审计/负结果」三类，作为 related work 底稿（ Blind 区：当前未抓）。
2. **把 rebuttal 预案写进论文草稿**：在 submission 前预填「审稿人可能问的 5 个 weakness + 已备证据」，其中 construct threat 与样本量两条必须预先有回应。
3. **严格按 2027 时间线倒排**：以 9 月录用通知为锚，倒推 abstract(5月)/full(5月底)/rebuttal(8月)/camera-ready(10月)，写入 ROADMAP 周表。

## 六、来源

[S01] NeurIPS 2025 main: 21,575 投 / 5,290 中（xmu.edu.cn 报道）；[S02] NeurIPS 2025 D&B blog "From Art to Science in AI Evaluations"；[S03] NeurIPS 2025 Call for Datasets & Benchmarks；[S04] OpenReview NeurIPS 2025/2026 D&B/E&D Track；[S05] NeurIPS 2026 E&D Reviewer Guidelines；内部：_arch_v44_brief.md。

**盲区**：D&B 2024–2026 具体投稿/接收数、逐年录用论文全清单、OpenReview 真实分数分布未抓取（web_fetch 拦截）。
