# 方向 38：怎么用 LLM 辅助科研（但不依赖）

## 核心结论
1. LLM 适合做**检索摘要、代码脚手架、语法润色、反驳预演**；**绝不能让它替你产生核心创新、编造实验数据、或代写全文**——2025–2026 顶会已大规模检测 AI 生成并可能拒稿/追责（方向 02/04）。
2. 讽刺点：QueYi 本身是"验证 LLM 是否可靠"的系统，作者若用 LLM 代写，等于自毁立论。所以 QueYi 稿必须体现"人主导、AI 辅助且披露"。
3. 正确用法：**LLM 当"加速器"和"陪练"**（如让它扮演 reviewer 攻击你的稿），产出仍由你校验；所有 LLM 生成的关键表述都要人工核对 + 披露。

## 精确数字与案例
- **适合**：related work 初筛（让 LLM 从 arXiv 摘要提关键词，你再读原文）、LaTeX/CI 脚本生成、rebuttal 走查、翻译辅助（非全文）。
- **禁止**：让它写 contributions（易 overclaim，方向 15）、编造数据（学术不端）、生成不存在的引用（幻觉引用，reviewer 一眼识破）。
- **案例（警示）**：2025 有作者在系统提示词注入讨好 reviewer 的内容、reviewer 也用 LLM 打分，两端 AI 垃圾被 NeurIPS 点名（方向 04）；E&D track AI 写作分 ≥90% 论文一年涨 10 倍（方向 02）。
- **披露实践**：NeurIPS 类会议要求披露 AI 辅助范围（用于写作/代码/分析）；QueYi 稿可在致谢或方法附"AI usage"一行（方向 08 v42 详解）。

## 对阙疑的 3 条具体行动
1. **LLM 当 reviewer 陪练**：把 QueYi 稿喂给 LLM 让它列 10 条最狠质疑，逐条预写回应（喂给方向 04 的回应库）。
2. **幻觉引用红线**：所有 LLM 建议的引用必须用 Semantic Scholar/Google Scholar 核实存在再引，绝不引用"没读过的论文"。
3. **写披露声明**：在稿末加"AI Usage: LLM 用于语法润色与相关文献初筛，所有科学内容由作者完成"，主动合规。

## 盲区（诚实标注）
- NeurIPS 2027 的 AI 披露具体条款需看 CFP（2026 版可能变化）；方向 08 v42 有更细政策梳理。
- LLM 检测器本身不完善（NeurIPS 承认参数敏感，42.7%→12.7%），但这不构成滥用理由。
- 用 LLM 跑"验证实验"（如让 GPT 生成 C++）本身就是 QueYi 的评测对象，与本方向"写作辅助"不同，勿混。

## 来源
- [1] AI 写作检测争议 — https://baijiahao.baidu.com/s?id=1877363176757481927
- [2] NeurIPS 2025 Reviewer Integrity — https://nips.cc/Conferences/2025/ReviewerIntegrity
- [3] Semantic Scholar 核实引用 — https://www.semanticscholar.org/
- [4] 方向 08 v42（AI 披露；见 _arch_v42）
