# 方向 14：Abstract 写作模板（150 词）

## 核心结论
1. Abstract 是审稿人 60 秒定调的地方，结构必须固定：**背景 1 句 → 缺口 1 句 → 我们做了什么 2 句 → 核心结果 2 句（带数字）→ 意义 1 句**。150 词内塞满可验证数字。
2. 对 QueYi，abstract 必须亮出"80% 盲 holdout 检出 / 100% 重注入 / 97.3% 变异 / 0.59ms 每卡"——用精确数字对抗"双非水稿"预设。
3. 禁忌：不要在 abstract 写"首次/开创性"(overclaim，见方向 15)；不要堆术语；不要把局限写进 abstract（留给正文 limitation 段，方向 03）。

## 精确数字与案例
- **字数锚**：NeurIPS abstract 上限通常 150–200 词（CFP 规定）；QueYi 控制在 150 词。
- **模板（填空式）**：
  > [背景] Verifying C++ knowledge in LLM-generated code is unreliable because compiler behaviors and undefined behaviors are undocumented. [缺口] Existing benchmarks lack tamper-proof audit trails and contamination-controlled holdout. [我们] We present QueYi, a C++ knowledge verification system with four-state verdicts, an append-only hash chain and Merkle checkpoints. [结果] On 20 blind holdout samples (7 true errors) QueYi achieves 80% detection (95% CI 28.4–99.5%); on 15 re-injected real defects it reaches 100%; core mutation score 97.3%; per-card verdict 0.59ms. [意义] QueYi provides the first auditable, contamination-resistant benchmark for C++ knowledge verification.
- **案例**：顶会录取 abstract 共性 = "最后一个数字句子让人想读正文"；QueYi 的"100% 重注入 + 0.59ms"正是这种 hook。
- **反例**：写"我们提出了一种 novel 框架"而无数字 → reviewer 直接标"无贡献证据"。

## 对阙疑的 3 条具体行动
1. **照模板填 150 词**：用上面结构，确保 5 个数字（80%/100%/97.3%/0.59ms/48卡）全进 abstract。
2. **删所有形容词**：去掉"powerful/efficient/novel/robust"，只留名词+数字；overclaim 词留给方向 15 专门处理。
3. **做 3 版 A/B/C**：给 2 个外部读者（方向 31）各看一版，选"60 秒内能说出我们做了啥"的那版。

## 盲区（诚实标注）
- 模板中的 QueYi 数字来自 brief 锚点（48卡/80%/100%/97.3%/0.59ms），未经我独立验证，以你仓库实测为准。
- "150 词"为 NeurIPS 常见上限，2027 可能微调，以 CFP 为准。
- abstract 不含局限是惯例，但 E&D 指南奖励坦诚（方向 03），可在末句轻点"小样本 CI 宽"以示诚实。

## 来源
- [1] NeurIPS 2026 投稿格式 — https://github.com/serre-ai/research/blob/main/docs/submission-guides/neurips-2026.md
- [2] 学术摘要结构 — 通用写作规范（方向 36）
- [3] QueYi 锚点数据 — _arch_v45 brief 第 8–17 行
