# 方向 09：arXiv 预印本策略（什么时候发、怎么发）

## 核心结论
1. **NeurIPS 允许非匿名预印本**：用 `\usepackage[preprint]{neurips}` 选项发 arXiv（带作者名），且鼓励在投稿前/中发 arXiv 占坑——对 0 影响力的 QueYi 是**最低成本建立时间优先 + 可被引用** 的手段。
2. 策略：**v0.1 择机发（占坑 + 收反馈）→ 每次大改升版本（v0.2/v0.3）→ 正式投稿时锁定一版并注明"under review at NeurIPS E&D 2027"**。但"早发"不等于"草率发"——**数字定稿 + repo 可跑 + ≥4 页草稿三者齐了再发**（作者 2026-09 才上大三，无需抢跑）。
3. 风险：arXiv 不算 peer review，且公开后该稿不能投"禁止预印本"的少数期刊（ML/SE 顶会基本都允许）；对 QueYi 这种细分赛道，被"抢发"风险极低（没人盯 C++ 知识验证）。

## 精确数字与案例
- **政策**：NeurIPS 2026 投稿指南（serre-ai/neurips-2026.md）明确 "Non-anonymous preprints (arXiv, websites) are allowed. Use [preprint] option in style file, NOT [final]." 即带作者名的 arXiv 合规。
- **时间窗**：NeurIPS 2027 投稿约 2027-05（作者届时在大三下）；**不必赶 2026-10**——建议 **2026 末~2027 初**发 v0.1，2027-03 升 v0.3（补实验），2027-05 投稿锁定 v0.4。
- **版本实践**：arXiv 允许更新（replace），每次生成新 ID 后缀但保留主号；引用用主号即可。QueYi 可按 corpus 增长打 tag：v0.1=48 卡 → v0.2=60 卡。
- **占坑价值实证**：顶会大量稿在投稿前已上 arXiv；arXiv 是 CS 事实上的"时间戳"，可证明原创性（对双非作者尤其重要，防被质疑"抄袭"）。
- **风险案例**：少数期刊（如部分 IEEE Tran 旧规）要求未公开发表；但 TSE/EMSE 接受 arXiv 扩展稿，需查 "prior publication" 条款。

## 对阙疑的 3 条具体行动
1. **成熟再发 v0.1（2026 末~2027 初）**：标题含"C++ Knowledge Verification Benchmark"，摘要写清四态判决 + 哈希链 + 盲 holdout 80% 检出；用 `[preprint]` 选项，作者真名（LiaoRanran / GitHub）。
2. **建版本 README**：在 GitHub 放 `arxiv_versions.md`，记录每版变更（v0.1→v0.4 的 corpus/实验增量），投稿时引用该演进证明持续工作。
3. **投稿即标注**：NeurIPS 投稿系统填"preprint arXiv:XXXX"，并在稿末加"Extended from arXiv:XXXX"；被拒转投 ICSE/ASE 时同样声明，合规且不损新颖性。

## 盲区（诚实标注）
- 未抓 2027 NeurIPS 官方 preprint 条款原文（web_fetch 受限）；以 2026 指南 + 业界共识为准，2027 需复核。
- "被抢发风险低"是赛道判断，无数据支撑；若未来出现同类工作，arXiv 时间戳是护城河证据。
- arXiv 的 CS 分类号应选 `cs.SE`（软件工程）+ `cs.PL`（编程语言）或 `cs.AI`，需确认最匹配类别。

## 来源
- [1] NeurIPS 2026 投稿指南（arXiv）— https://github.com/serre-ai/research/blob/main/docs/submission-guides/neurips-2026.md
- [2] arXiv 提交帮助 — https://info.arxiv.org/help/submit/index.html
- [3] NeurIPS 2025 Reviewer Integrity — https://nips.cc/Conferences/2025/ReviewerIntegrity
- [4] arXiv 预印本与双盲矛盾解读 — https://blog.csdn.net/kafka6courier/article/details/152500936
