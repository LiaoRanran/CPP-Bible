# 方向 15：贡献声明怎么写才不被嫌 overclaim

## 核心结论
1. overclaim 是双非单人稿的**头号雷**：reviewer 看到"首次/开创性/state-of-the-art"会本能警惕并下探找漏洞。正确做法是**把 claim 收敛到"可证据支撑的最小陈述"**，用数字而非形容词证明。
2. QueYi 的贡献声明应写成"我们提供了 X 的可审计版本"，而非"我们解决了 C++ 验证问题"；每个 claim 后括号跟证据（如 "100% re-injection detection (§5)"）。
3. 2026 E&D 指南明确"坦诚局限被奖励"——所以贡献声明里**主动划边界**（"仅覆盖 48 卡/未测 Clang 全部版本"）反而增信，不扣分。

## 精确数字与案例
- **overclaim 红词**："first"（除非真查过）、"novel"（几乎总 redundant）、"state-of-the-art"（需对比表）、"solve"（太满）、"groundbreaking"。QueYi abstract/intro 应清零这些词。
- **收敛模板**：把"我们提出了全新的 C++ 验证框架"改为"我们贡献了：(1) 一个 append-only 哈希链的 C++ 知识验证原型（813 行，可复现）；(2) 20 样本盲 holdout 上 80% 检出的实证；(3) 15 夹具重注入 100% 检出的污染控制方法。"
- **案例**：NeurIPS 录取稿的贡献段普遍是"3 条 bullet，每条带证据指针"；被拒稿常是"一段散文吹 5 个贡献"。QueYi 用 bullet + 证据。
- **边界写法**：在 contribution 末加 "Scope: verified only on 48 cards / GCC 13 + Clang 17 / not evaluated on C++20 contracts" —— 这叫"划界增信"。

## 对阙疑的 3 条具体行动
1. **贡献写 3 bullet**：严格对应"系统/实证/方法"，每条后括证据章节号（如 (§4) (§5) (§6)），零形容词。
2. **查"first"是否真**：投前用 Semantic Scholar 搜 "C++ knowledge verification benchmark"，确认无人做过再写"to our knowledge, first"；若有人做过，改"complementary to X"。
3. **加 Scope 段**：在 contribution 后写一段"未覆盖：C++20 契约 / MSVC 全版本 / 多线程 UB"，主动划界，对齐 2026 指南的坦诚奖励。

## 盲区（诚实标注）
- "first"是否属实需 Semantic Scholar/Google Scholar 检索确认，我未做该检索（盲区，列为行动 2）。
- overclaim 红词清单来自写作共识，非会议明文；但 reviewer 行为一致。
- 贡献与 abstract 数字需一致（方向 14），避免两处数字打架。

## 来源
- [1] 2026 E&D 指南（奖励坦诚）— https://nips.cc/Conferences/2026/EvaluationsDatasetsReviewerGuidelines
- [2] NeurIPS 投稿指南 — https://github.com/serre-ai/research/blob/main/docs/submission-guides/neurips-2026.md
- [3] Semantic Scholar 查重 — https://www.semanticscholar.org/
