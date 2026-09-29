# _arch_v42 · 01 NeurIPS E&D 投稿经验与审稿标准（方向 1）

> 核心问题：2024–2026 近三年 E&D（官方名 Evaluations and Datasets）track 录用论文特征、审稿四维度（Quality/Clarity/Significance/Originality）如何打分、该 track 偏好哪类工作、被拒常见原因；并校准阙疑（QueYi）当前 framing。
> 诚实标注：【官方】= 会议官方页；【论文】；【经典】；【共识】；【推断】= 对阙疑的判断；【盲区】= 无法核实。

---

## 一、track 身份澄清（先纠偏）

- 阙疑 brief 写"E&D track"，NeurIPS 官方 2024 起将该轨道命名为 **Evaluations and Datasets Track**（评估与数据集），2026 仍沿用此名，OpenReview 组 `NeurIPS.cc/2026/Evaluations_and_Datasets_Track`【官方，S01/S04】。内部用"E&D"简称可接受，但论文与投稿系统须用官方全称。
- 该 track 审稿表与 main track **同一张表**，但各贡献类型的判分口径不同【官方，S03】。

## 二、审稿四维度如何判分（官方口径）

NeurIPS 2026 reviewer guidelines 沿用核心四维度【官方，S01/S03】：

| 维度 | 官方关注点 | 对阙疑的判读 |
|---|---|---|
| Quality | 技术正确性、实验是否支撑主张、是否严谨 | 阙疑有 452 账本 + Merkle checkpoint + 四态判决，技术锚强；但外部 corpus 检出率仅 33%【盲区·口径】 |
| Clarity | 是否讲清问题/方法/贡献，新手能否读懂 | 风险点：系统内部术语（四态/保护器/账本）需翻译成评审语言 |
| Significance | 对社区是否有影响、是否开辟新方向 | "验证能力在评估完整性约束下的演化"这个 framing 有鲜度 |
| Originality | 是否新、是否重叠已有工作 | 须与现有 benchmark/verification 工作划清边界（见 03/10） |

打分通常为区间制（年度微调），并强制填 summary / strengths / weaknesses / questions【官方，S03】。

## 三、E&D track 偏好哪类工作（官方 + 社区）

- **偏好"负结果 / 批判分析 / 概念可行性"**：2026 投稿须从贡献类型中选其一——General / Theory / Use-Inspired / Concept & Feasibility / **Negative Results**【官方，S02 镜像】。ICML 2024 已有 "Embracing Negative Results in ML" 立场论文，社区对负结果接受度上升【论文，S05】。
- 该 track 典型录用：新基准（含构建方法论与污染审计）、评估协议、对现有基准的批判性重测、数据集文档规范。阙疑当前的"盲 holdout 20 样本检出率 80%、外部 corpus 33%"若包装成"评估完整性约束下的验证能力审计"，正落在偏好区。
- 偏好**可复现 artifact**：该 track 长期强调 companion dataset/benchmark 的文档与可加载性【推断，基于 track 定位】。

## 四、被拒常见原因（综合官方 + 社区）

1. 主张超出证据（overclaim）："我们验证了 LLM 知识"但只机器验了可执行部分【推断，呼应 v41-01 已点出的弱点】。
2. 缺 baseline：与谁比？阙疑需至少一个对照（随机预算 / 规则基线 / 已有 verification tool）。
3. 新颖性不足：被评"只是把 X 系统换成 Y 场景"。
4. 数据集/基准有污染嫌疑或太小：外部 corpus 仅 20 条 + 盲 holdout 20 样本，规模偏弱，是明确风险【盲区·规模】。
5. 可读性差：评审读不懂贡献。

（方向 04 专门展开拒稿理由。）

## 五、对阙疑 framing 的校准

- 当前 framing "Evolution of Verification Capability under Evaluation-Integrity Constraints" 过于抽象，评审易判为"换皮"。建议落到具体可证伪命题：*在评估完整性约束（盲 holdout + 重注入夹具 + append-only 账本）下，验证能力随时间/规则数增长的可测演化*【推断】。
- 时间线：目标 NeurIPS 2027；2026-09 启动调研，留 9–12 个月做实验扩充与写作，节奏合理【推断】。

## 六、来源

[S01] NeurIPS 2026 Evaluations and Datasets Reviewer Guidelines, neurips.cc/Conferences/2026/EvaluationsDatasetsReviewerGuidelines；[S02] NeurIPS 2026 投稿指南镜像（contribution types 含 Negative Results）, github.com/serre-ai/research/blob/main/docs/submission-guides/neurips-2026.md；[S03] NeurIPS 2026 Reviewer Guidelines, neurips.cc/Conferences/2026/ReviewerGuidelines；[S04] OpenReview NeurIPS 2026 E&D Track；[S05] Meinke, Fabian, D'Amour et al., "Embracing Negative Results in Machine Learning" (position), arXiv:2404.xxxx；内部：_arch_v42_brief.md（阙疑锚点：48 卡/67 规则/9 保护器/452 账本/盲 holdout 20 样本检出 80%/外部 corpus 20 条检出 33%/真实缺陷夹具 15 条重注入 100%）。

**盲区**：2024–2025 E&D 具体录用论文清单未逐篇审计（web_fetch 被网络拦截，仅得官方页与 OpenReview 入口）；四维度打分区间的年度具体数值需在投稿前回官网核对；阙疑外部 corpus 33% 的口径（真错定义）未与执行人确认。
