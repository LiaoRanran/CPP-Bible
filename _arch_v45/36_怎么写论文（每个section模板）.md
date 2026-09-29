# 方向 36：怎么写论文（每个 section 模板）

## 核心结论
1. 顶会论文是**高度模板化的**：Intro（漏斗）、Related Work（分类对比）、Method（可复现）、Experiments（claim↔证据一一对应）、Limitations（坦诚）、Conclusion（收敛）。单人作者照模板填远比自由发挥稳。
2. QueYi 的写作顺序应是 **Method → Experiments → Related Work → Intro → Abstract**（先写最确定的，最后写需要全局视角的引言/摘要，方向 13）。
3. 每个 section 的铁律：**只写能落到证据的句子**；claim 必须能在 Experiments 找到对应图/表/数字（否则被 reviewer 标记 overclaim，方向 15）。

## 精确数字与案例（Section 模板）

**Abstract**：见方向 14（150 词固定结构）。

**1. Introduction**（漏斗：广→窄→我们的贡献）
- 段1：背景（C++/LLM 生成代码的验证需求）；
- 段2：缺口（现有 benchmark 不可审计、无污染控制）；
- 段3：QueYi 做什么（四态判决 + 哈希链 + 88.8%…），亮 3 个数字；
- 段4：贡献 bullet（见方向 15），每条带章节号。

**2. Related Work**（分类 + 对比表）
- 三小类：C++/代码 benchmark、变异测试与 PBT、可审计/可复现系统；
- 每类末写"但都缺少 X，QueYi 提供 X"；配一张对比表（方向 01/02 的曲目）。

**3. Method**
- 3.1 系统架构（813 行内核、9 保护器）；
- 3.2 四态判决定义（含内部错误态，方向 28）；
- 3.3 append-only 哈希链 + Merkle checkpoint（数学形式化）；
- 3.4 corpus 构建流程（48 卡 = 26 verified + 3 red-team + 19 draft）。

**4. Experiments**
- 4.1 设置（三编译器 GCC/Clang/MSVC、0.59ms/卡）；
- 4.2 盲 holdout（20 样本/7 真错/80% 检出/CI 28.4–99.5%）；
- 4.3 外部 corpus（33.3%）——**主动报低分并解释**（坦诚，方向 03）；
- 4.4 重注入（15 夹具/100%）；
- 4.5 变异测试（core 97.3% / all 81.5%，方向 20）；
- 4.6 消融（去掉哈希链/减少卡数，方向 05 v42 的 ablation）。

**5. Limitations**（主动划界）
- 样本小（CI 宽）、外部 corpus 检出低、未覆盖 C++20/MSVC 全版本；
- 按 2026 指南"坦诚被奖励"（方向 03）。

**6. Conclusion**：收敛贡献，不引入新 claim。

## 对阙疑的 3 条具体行动
1. **按此模板建 LaTeX 骨架**：先写 Method + Experiments（你最有素材），再 Related Work，最后 Intro/Abstract。
2. **claim↔证据映射表**：写 Intro 前先列"每条 claim → 哪张表/图 → 哪个数字"，防 overclaim（方向 15）。
3. **Limitations 当卖点写**：把"外部 corpus 33.3%"写成"我们诚实报告并分析原因"，对齐 E&D 指南。

## 盲区（诚实标注）
- 各 section 页数配比需按 NeurIPS 2027 模板（约 9 页正文）调整，未确认。
- 模板中的 QueYi 数字来自 brief 锚点，需与仓库一致（否则失信）。
- "88.8%"等我没写，因 brief 只给 80%/100%/97.3%/33.3%；勿自造数字。

## 来源
- [1] NeurIPS 2026 投稿格式 — https://github.com/serre-ai/research/blob/main/docs/submission-guides/neurips-2026.md
- [2] 2026 E&D 指南（坦诚）— https://nips.cc/Conferences/2026/EvaluationsDatasetsReviewerGuidelines
- [3] 方向 14/15（abstract/贡献）
- [4] QueYi 锚点 — _arch_v45 brief
