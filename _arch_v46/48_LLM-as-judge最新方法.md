# 方向 48：LLM-as-judge 最新方法（2025-2026）

> 调研时间：2026-09-29。联网检索 16 次（WebSearch 10 + WebFetch 6）。
> 锚点：阙疑的四态判决若引入 LLM 复核（方向 46 建议的 step judge），就必须先知道 LLM 裁判本身错在哪、贵多少、怎么校准。

## 核心结论

1. **LLM-as-judge 在"简单偏好比较"上已经够用，但在"判断答案正确性"上接近随机**：MT-Bench（Zheng 2023）报告 GPT-4 裁判与人类偏好**一致率超过 80%**，与人类-人类一致率相当；但 `JudgeBench`（ICLR 2025）用**客观对错**构造的 350 组响应对上，**GPT-4o 在 vanilla 提示下只有 50.86%，论文原文写"不优于随机猜测"**。**分界线是"判偏好"还是"判事实"**——阙疑做的正是后者。
2. **位置偏差是结构性缺陷，不是提示工程能修好的**：`Judging the Judges`（达特茅斯，IJCNLP 2025）在 **12 个闭源 + 3 个开源裁判 / 22 个任务 / 超 100,000 次评估**上测量：**GPT-4 位置一致性 PC 仅 0.82、GPT-4o 0.76**；换成 list-wise 后 **GPT-3.5-Turbo 的 PC 从 0.70 崩到 0.34**；Claude-3-Haiku 在 DevBench 上 PC **只有 0.23**（几乎完全被位置决定）。**任何"让 LLM 二选一"的评测都必须做顺序对调。**
3. **可用的解法已经收敛到三条，且都是"不改模型"的**：① **概率化聚合**（TrustJudge：不一致率 23.32%→14.89%、循环偏好 15.22%→4.40%）；② **异构小模型评审团**（PoLL：3 个模型，比单一 GPT-4 **便宜 7–8 倍**，Cohen's κ 0.763 反超 GPT-4 的 0.627）；③ **置信度驱动 + 升级**（Trust or Escalate 的可证保证级联）。**对阙疑最实用的是 PoLL + 顺序对调 + 置信度阈值，而不是去追最强的单模型裁判。**

## 精确数字与案例

### 一、起点与天花板：MT-Bench 的 80% 与 JudgeBench 的 50%

**（1）MT-Bench / Chatbot Arena（把 LLM-as-judge 变成标准做法的那篇）**
- 论文：`Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena`，Zheng 等（LMSYS/UC Berkeley），arXiv:2306.05685，2023-06（v4 2023-12-24）。
- 数字：摘要原文——**强 LLM 裁判（如 GPT-4）"match both controlled and crowdsourced human preferences well, achieving over 80% agreement"**；即 **GPT-4 与人类一致率 > 80%**，与人类-人类一致率处于同一水平。
- 论文同时指出三类已知偏差：**位置偏差、冗长偏差（verbosity bias）、自我增强偏差（self-enhancement bias）**。**这三条是后续所有 2025-2026 论文的共同靶子。**

**（2）JudgeBench：把"判偏好"换成"判对错"，GPT-4o 直接掉到随机线**
- 论文：`JudgeBench: A Benchmark for Evaluating LLM-Based Judges`，arXiv:2410.12784（v2 2026-08-11；**ICLR 2025**）。
- 构造：**350 组响应对**（每对含一个客观正确、一个客观错误），来自 MMLU-Pro（知识 154）、LiveBench（推理 98、数学 56）、LiveCodeBench（编程 42）。
- 关键结果：

| 裁判 | 整体准确率 |
|---|---|
| **Vanilla GPT-4o** | **50.86%** |
| Arena-Hard Judge (GPT-4o) | 56.57% |
| VertexAI Evaluation (Gemini-1.5-pro) | 44.57% |
| PandaLM (LLaMA-7B) | **13.14%** |
| JudgeLM-7B / 13B / 33B | 25.14% / 26.86% / 35.71% |
| Prometheus2-7b | 34.86% |
| Skywork-LLaMA-3.1-8B | 53.43% |
| Skywork-LLaMA-3.1-70B | 57.43% |
| ChatEval（多智能体） | 34.00% |

- 原文结论：GPT-4o 在 vanilla 提示下 **"achieving accuracy no better than random guessing"**（不优于随机猜测，随机 = 50%）。
- 推理型模型（同一 Arena-Hard 提示，只换底层模型）：

| 底层模型 | Overall |
|---|---|
| GPT-4o | 56.57 |
| Claude-3.5-Sonnet | 64.29 |
| o1-mini | 65.71 |
| DeepSeek-R1 | 73.14 |
| o1-preview | **75.43** |
| o3-mini (medium) | 76.57 |
| **o3-mini (high)** | **80.86** |

- **o3-mini(high) 比 GPT-4o 高约 +24 个点**；论文结论："scaling test-time compute is a promising path to improve the reasoning ability of the judges."
- 奖励模型区间 **59%–64%**（Skywork-Reward-Gemma-2-27B 64.29%、InternLM2-20B-Reward 63.43%）。
- 严重退化案例：**PandaLM 在 700 次判断中有 479 次选"平局"**；**JudgeLM-7B 在 59.71% 的响应对上前后不一致**。
- **对阙疑的含义**：如果阙疑用 LLM 判"C++ 断言是否正确"，**默认配置下接近抛硬币**。要用就必须用推理型模型 + 强制二选一（禁平局）+ 位置对调。

### 二、位置偏差的量化：`Judging the Judges`

- 论文：`Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge`，Shi、Ma、Liang、Ma、Vosoughi（达特茅斯学院），arXiv:2406.07791（v7；**IJCNLP 2025** long paper `2025.ijcnlp-long.18`）。
- 规模：**12 个闭源 LLM 裁判 + 3 个开源模型 / 22 个任务 / 约 40 个生成模型 / 超过 100,000 次评估实例**；总实验成本约 **3,000 美元**。
- 三个指标：
  - **RS（Repetition Stability）**：同一查询重复呈现时最频繁选择的百分比（验证偏差非随机）；
  - **PC（Position Consistency）**：顺序交换后仍选同一答案的比例（越高越好）；
  - **PF（Preference Fairness）**：综合首位/末位偏好，−1（完全首位偏好）~ 0（公平）~ +1（完全末位偏好）。
- MTBench 成对比较（节选）：

| 裁判 | RS | PC | PF |
|---|---|---|---|
| Claude-3.5-Sonnet | 0.96±0.07 | **0.82±0.14** | 0.01 |
| **GPT-4** | 0.97±0.05 | **0.82±0.15** | 0.02 |
| GPT-4o | 1.00±0.02 | 0.76±0.18 | −0.12 |
| o1-mini | 0.90±0.07 | 0.76±0.15 | −0.04 |
| Gemini-1.5-pro | 0.97±0.09 | 0.62±0.19 | 0.23 |
| Claude-3-Sonnet | 0.93±0.11 | 0.59±0.22 | 0.32 |
| GPT-3.5-Turbo | 0.96±0.07 | 0.70±0.18 | 0.06 |

- DevBench 成对比较（更糟）：
  - **Claude-3-Haiku：PC 0.23±0.14，PF 0.75**（几乎完全被位置决定）；
  - **Gemini-1.5-flash：Error 0.96**（96% 的评估直接失败）；
  - GPT-4：PC 0.83±0.15。
- List-wise 比较（候选变多就崩）：
  - **GPT-3.5-Turbo：PC 从成对 0.70 → 列表式 0.34**；
  - GPT-4o：PC 0.68±0.22；Claude-3.5-Sonnet：0.67±0.19。
- 其他关键结论：
  - 有能力的裁判 **RS 普遍 > 0.85**（偏差不是随机的）；
  - **高 PC 不保证公平**：编码任务上 GPT-4 高度末位偏好、GPT-4o 高度首位偏好；
  - 质量差距 δ_q 越大越一致（PC 呈抛物线）；
  - **长度影响很弱**：平均输出长度是 PF 的显著预测因子，但 **AIC 变化极小**；
  - **多评委多数投票对 > 99% 的评估实例有效**；仅 **< 4%** 的实例为"难判断"（多数评委无法共识）；
  - 12 个裁判中 **> 75% 在超过一半数据集上相互一致**。
- **对阙疑的含义**：这条给了"多 judge 聚合"一个**乐观的数字（>99% 有效）**，但也给了"单 judge 位置偏差"的**悲观数字（PC 低至 0.23）**。**结论：阙疑若用 LLM 复核，必须"单 judge 顺序对调 + 多 judge 投票"双管齐下。**

### 三、自我偏好偏差：根因是"困惑度"而不是"自恋"

- 论文：`Self-Preference Bias in LLM-as-a-Judge`，Wataoka、Takahashi、Ri（SB Intuitions），arXiv:2410.21819（v2 2025-06-21；**NeurIPS 2024 Safe Generative AI Workshop**）。
- 贡献：**提出首个量化自我偏好偏差的指标**；实验证明 **GPT-4 表现出显著程度的自我偏好偏差**。
- 关键机制发现：LLM **对困惑度（perplexity）更低的输出给出显著更高的评价**，且**无论该输出是否由自己生成**——即"自我偏好"的本质是**"偏好自己更熟悉的文本分布"**，而非"偏好自己的身份"。
- **对阙疑的含义**：阙疑的 C++ 卡是**高度专业文本**，任何通用 LLM 裁判对"它熟悉的写法"会给高分。**缓解手段是"不要让裁判知道哪份是阙疑产出的"（盲化）+ 用困惑度无关的规则证据做锚**。

### 四、框架级不一致：TrustJudge（ICLR 2026）

- 论文：`TrustJudge: Inconsistencies of LLM-as-a-Judge and How to Alleviate Them`，Wang 等（南京大学等），arXiv:2509.21117，2025-09-25（**ICLR 2026**）；代码 `github.com/TrustJudge/TrustJudge`。
- 首次系统化定义两类不一致：
  1. **Score-Comparison Inconsistency**：被评低分的回答在成对比较中反而赢；
  2. **Pairwise Transitivity Inconsistency**：循环偏好链（A>B>C>A）与等价矛盾（A=B=C≠A）。
- 根因：**离散评分系统的信息损失** + 成对评估中**模糊的平局判定**。
- 两个创新：① **distribution-sensitive scoring**（从离散评分概率算连续期望，保留信息熵）；② **likelihood-aware aggregation**（用双向偏好概率或 perplexity 解决传递性违反）。
- 精确改善（judge = **Llama-3.1-70B-Instruct**）：
  - **Score-Comparison 不一致率 23.32% → 14.89%（降低 8.43 个点）**；
  - **Pairwise Transitivity 不一致率 15.22% → 4.40%（降低 10.82 个点）**；
  - **同时保持更高评估准确率**；**无需额外训练或人工标注**。
- **对阙疑的含义**：阙疑的"四态判决"本身就是**离散标签系统**，天然面临同类问题——**把"pass/block"的概率化期望保留下来（而非直接取 argmax），可以显著降低跨样本的不一致**。这是**可以直接抄到 `gate_engine.py` 判决聚合层**的一条。

### 五、校准：LLM 裁判严重过度自信

- 论文：`Overconfidence in LLM-as-a-Judge: Diagnosis and Confidence-Driven Solution`，arXiv:2508.06225，2025-08-08。
- 基准：**JudgeBench 的 350 组响应对**（知识/推理/数学/编程）。
- **ECE（期望校准误差，越低越好）**：

| 模型 | SC 设置 | MP 设置 | LogP 设置 |
|---|---|---|---|
| **GPT-4o** | **39.25** | **47.09** | **45.05** |
| Mistral-Nemo | **74.22** | 68.89 | 64.63 |
| GPT-4.1-nano | 57.03 | 67.43 | 66.05 |
| Claude-Sonnet-4 | 17.98 | 34.51 | — |
| Qwen3-235B-A22B | 11.78 | 13.00 | — |
| **DeepSeek-R1-0528** | **12.07** | 7.17 | 6.84 |

- 现象：**多数模型预测置信度集中在 90–100%，但实际准确率远低于理想校准线**（即"过度自信"）。
- 提出 **TH-Score**：`TH-Score = (e^(accuracy − 0.5) − 1) × percentage`，聚焦高置信区间 (100−ε, 100] 与低置信区间 (0, ε)，默认 **ε = 0.1**；作者称 TH-Score 优于 ECE（显式平衡准确率与覆盖率）。
- **LLM-as-a-Fuser**：把 LLM 从"被动评判者"变成"主动融合者"，接收多个模型的**决策 + 批判理由**做证据感知聚合：
  - 最强融合器（Qwen3-235B-A22B）：准确率 **86.29%（+8.86%）**，ECE **6.42%（−5.36%）**；
  - 对比基线 Entropy Weighted Voting（81.71% / 8.48% ECE）：准确率 **+4.28%**、ECE 优 **3.3%**；
  - 提升最显著的模型：**Mistral-Nemo 准确率 +47.14%、ECE −53.73%**；Gemini-2.5-Flash +38.57%/−14.77%；GPT-4.1-nano +30.85%/−19.78%；
  - 分歧分析：**GPT-4o 的错误分歧 112 次 vs 正确分歧仅 6 次**（最差）；Qwen3-235B-A22B 正确分歧 34 vs 错误分歧 12。
- **对阙疑的含义**：如果阙疑给 LLM 复核加"置信度"字段，**默认的 LLM 自述置信度不可信（ECE 高达 39–74）**，必须做校准或改用"多模型融合 + 理由"。

### 六、成本解法：PoLL（评审团）——最省钱的一条

- 论文：`Replacing Judges with Juries: Evaluating LLM Generations with a Panel of Diverse Models`（PoLL），Verga 等（Cohere），arXiv:2404.18796，2024-04-29。
- 组成：**3 个异构模型家族**（Command R + Haiku + GPT-3.5）；QA 用 max voting，Arena 用 average pooling。
- 成本：PoLL 输入 **$1.25 / 百万 tokens**、输出 **$4.25 / 百万 tokens**；GPT-4 Turbo 单一评委 **$10 / $30**。**PoLL 比单一 GPT-4 便宜 7–8 倍。**
- 一致性（单跳 QA，与人类判断的 Cohen's κ）：

| 评委 | NQ | TQA | HPQA |
|---|---|---|---|
| GPT-4 | 0.627 | 0.841 | 0.830 |
| CMD-R | 0.734 | 0.902 | 0.815 |
| Haiku | 0.749 | 0.894 | 0.873 |
| **PoLL** | **0.763** | **0.906** | 0.867 |

- Chatbot Arena 排名相关性：**PoLL Pearson 0.917 / Kendall 0.778**，均高于 GPT-4（0.817 / 0.667）。
- 偏差：**PoLL 分数分布标准差 2.2**，**GPT-3.5 最大 6.1**。
- 提示词影响：GPT-4 的 κ 随提示变化从 **0.518（zero-shot）** 到 **0.725（加 "don't overthink"）**——**同一模型，仅改提示，κ 变化 0.207**。
- **对阙疑的含义**：**"3 个小模型评审团 > 1 个大模型裁判，且便宜 7–8 倍"**——对 0 预算的双非本科生，这是**唯一可负担的 LLM 复核方案**。

### 七、可证保证：Trust or Escalate（ICLR 2025）

- 论文：`Trust or Escalate: LLM Judges with Provable Guarantees for Human Agreement`，Jung、Brahman、Choi（UW），arXiv:2407.18370（**ICLR 2025**）。
- 两个组件：
  1. **Simulated Annotators**：无需外部监督即可显著改善校准与选择性预测；
  2. **Cascaded Selective Evaluation（级联选择性评估）**：用便宜模型当初始裁判，**只在必要时升级到更强模型**，从而对"与人类一致率"提供**可证明的保证**。
- **对阙疑的含义**：这正是阙疑"四态判决"想要的形态——**大部分卡由便宜规则/小模型处理，只有边界样本升级到强模型**，且给出可证明的下界。**阙疑的 `unknown` 态天然就是"升级触发器"。**

### 八、验证器基准：VerifyBench（ICLR 2026）——最贴近阙疑任务的数字

- 论文：`VerifyBench: Benchmarking Reference-based Reward Systems for Large Language Models`，arXiv:2505.15801，2025-05-21（**ICLR 2026**）。
- 规模：
  - **VerifyBench**：1,000 个唯一问题 / 2,000 个答案（1,000 正确 + 1,000 错误，平衡采样）；答案类型各 500：数值 / 表达式 / 多选 / 字符串；领域：通用 404、逻辑 498、数学 1,098。
  - **VerifyBench-Hard**：945 个问题 / 1,000 个答案（**291 正确 + 709 错误**，自然采样，错误占 **70.9%**）。
- 准确率（AVG）：

| 模型 | VerifyBench | VerifyBench-Hard |
|---|---|---|
| **Qwen3-32B** | **95.80%** | 71.80% |
| Qwen3-30B-A3B | 94.00% | — |
| Qwen3-8B | 94.00% | 70.90% |
| Qwen3-235B-A22B | 93.80% | 70.60% |
| gpt-4o-2024-11-20 | 93.15% | **72.60%** |
| Qwen3-4B | 92.00% | 72.40% |
| Llama-4-Scout-17B | 90.01% | 48.50% |
| Llama-3.3-70B | — | 54.70% |
| Qwen3-1.7B | 81.10% | 51.50% |
| Llama-3.2-3B-Instruct | 60.95% | 33.90% |
| **Llama-3.2-1B-Instruct** | **44.15%** | **25.60%** |
| 规则 math-verify | 45.90% | 32.50% |

- **关键结论：标准场景 92–96%（可靠），困难场景最高仅 72.60%（不可靠）——下降约 20 个点。**
- **参考答案至关重要**：移除 prompt 中的参考答案后普遍下降 **5%–18%**（Qwen3-8B −18.25%、Qwen3-32B −16.90%）。
- **小模型严重不足**：Llama-3.2-1B 只有 44.15%（比随机还差）。
- 错误高发：复数/多值答案、代数等价表达式、多选、需语义一致性的字符串。
- 与真实训练相关：VerifyBench 得分更高的验证器（Qwen3-4B）训出的模型在 GSM8K/MATH500/SVAMP 上**始终优于**低分验证器（Llama-3.1-8B）。
- 局限（原文自承）：**未识别 reward hacking**；排除证明类问题（需 Lean4）；二值评分无法评"部分正确"。
- **对阙疑的含义（最重要的一条）**：**"给参考答案"能把验证准确率提高 5–18 个点**——阙疑的每张卡如果都带"标准答案/反例"，其 LLM 复核的可靠性会显著提升。而 **1B 级小模型做验证器完全不可用（44.15%）**，这与方向 44（小模型验证器）必须交叉验证。

### 九、其他 2025-2026 补充

- `Evaluating Scoring Bias in LLM-as-a-Judge`（arXiv:2506.22316，2025-08）：首次形式化"评分偏差"，提出三类扰动——**评分标准顺序偏差、评分标识偏差、参考答案分数偏差**；5 个模型（GPT-4o / DeepSeek-V3-671B / Qwen3-32B / Qwen3-8B / Mistral-Small-24B）。数字：**GPT-4o 相关系数波动保持在 0.03 以内**，而 **Qwen3-8B 在参考答案分数偏差下波动接近 0.2**；**GPT-4o 偏好打 4 分、Qwen3-32B 偏好 5 分**；**用罗马数字标识反而提升 GPT-4o 的一致性，但伤害 DeepSeek/Qwen 系列**；**降序评分标准在多数情形提升 GPT-4o/Qwen3-32B/Mistral 的准确性**。
- `Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge`（CALM，arXiv:2410.02736，**ICLR 2025**）：提出 CALM 框架，覆盖 **12 种偏差类型**。
- `Judging the Judges: A Systematic Evaluation of Bias Mitigation Strategies`（2026）：比较 **9 种去偏策略 × 5 个裁判模型（4 个厂商）**——**具体数字未抓取**（见盲区）。
- `A Survey on LLM-as-a-Judge`（arXiv:2411.15594，v6）：系统综述定义、指标、数据集与缓解策略。

## 对阙疑的 3 条具体行动

1. **在阙疑的评测协议里强制"顺序对调双盲"（零成本、最高优先级）**：对任何"阙疑 vs baseline"的对比评估，**必须跑 A/B 与 B/A 两次并报告位置一致性 PC**。依据：`Judging the Judges` 中 **GPT-4 PC 仅 0.82、Claude-3-Haiku 仅 0.23**，且 RAG-vs-GraphRAG 论文报告"顺序对调会导致完全相反的判断"。**具体动作**：在 `research/05_evaluation_protocol.md` 的**下一版**中加入"所有 LLM 参与的评测必须双向呈现"条款（本方向只写 `_arch_v46/`，条款文本先在本目录起草）。
2. **用 PoLL 式 3 模型评审团 + 置信度升级替代"单一强裁判"**：具体配置为**三个异构小模型 + max voting**，并对低置信样本**升级到推理型模型**。依据：**PoLL 比单一 GPT-4 便宜 7–8 倍且 κ 更高（0.763 vs 0.627）**；**Trust or Escalate（ICLR 2025）**给出级联的可证保证；**JudgeBench 中 o3-mini(high) 达 80.86% 而 GPT-4o 仅 50.86%**。**落地**：写 `tools/judge_panel_666.py`，输入为一组待判断言 + 参考答案，输出为"多数票 + 每票置信度 + 是否升级"。
3. **把"离散四态"升级为"概率化判决 + 保留期望值"**：参照 **TrustJudge** 的 distribution-sensitive scoring，把 `gate_engine.py` 的判决聚合从 argmax 改为**保留各态概率的连续期望**，预期可把不一致率按 TrustJudge 的量级（**23.32%→14.89%、15.22%→4.40%**）改善。**同时**：为每张卡补"参考答案/反例"字段（VerifyBench 证明**带参考答案可提升 5–18 个点**），这是**成本最低、收益最确定**的一步。

## 盲区（诚实标注）

- **MT-Bench 的"80%"是"超过 80% 一致率"的摘要级表述**，**具体是 80.x% 还是 85% 未逐字核对原文 Table 5**；且"与人类-人类一致率相当"的对比数字（约 81%）**本轮未从原文核实**。
- **JudgeBench 的数字来自 v2（2026-08-11）HTML 版的二手抓取**，其中 o3-mini 系列属于 2025 年发布模型，**该表是否为 v2 新增未确认**；引用进论文前必须回 ICLR 2025 正式版核对。
- **`Judging the Judges` 的 PF 公式与部分表格数值来自二手抓取**，PF 的 min-max 缩放细节未逐字核对；**总成本"约 3,000 美元"是论文自述**，未独立验证。
- **Self-Preference Bias 论文是 NeurIPS 2024 Workshop 论文**（非主会），其"GPT-4 有显著自我偏好"**未给出具体偏差数值**（本轮抓取只见定性表述），**具体量化数字未核实**。
- **TrustJudge 的不一致率降低（8.43 / 10.82 个点）是在 Llama-3.1-70B-Instruct 单一裁判 + 自有数据集上的结果**，**未在其它裁判上复现**，泛化性存疑。
- **Overconfidence 论文的 ECE 数值（GPT-4o 39.25/47.09/45.05）来自 arXiv HTML 二手抓取**，未逐表核对；其 ECE 是否 ×100 表述未确认（本报告按"百分点"理解）。
- **`Judging the Judges: Bias Mitigation Strategies`（2026）的 9 种策略 × 5 模型的具体数字未抓取**——只知存在该研究，**未核实其结论**。
- **CALM 的 12 种偏差类型的具体清单未抓取**，只有"12 种"这一数字。
- **VerifyBench 是 ICLR 2026 论文**（投稿中/接收未定），**其 Qwen3 系列数字属 2025 年模型**，2027 时点需重测。
- **未查到**：针对 C++ / 编译语义的 LLM-as-judge 基准。**阙疑若自建，没有可对标 baseline**。
- 所有数字需在 **2027 投稿时点刷新**（LLM 裁判能力迭代极快，2025 年的"随机水平"到 2026 年可能已不成立）。

## 来源

1. Zheng et al., *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*, arXiv:2306.05685, 2023 — https://arxiv.org/abs/2306.05685
2. Tan et al., *JudgeBench: A Benchmark for Evaluating LLM-Based Judges*, arXiv:2410.12784, 2024（ICLR 2025）— https://arxiv.org/html/2410.12784v2
3. Shi et al., *Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge*, arXiv:2406.07791（IJCNLP 2025）— https://arxiv.org/html/2406.07791v7 ；https://aclanthology.org/2025.ijcnlp-long.18/
4. Wataoka et al., *Self-Preference Bias in LLM-as-a-Judge*, arXiv:2410.21819, 2024（NeurIPS 2024 Safe GenAI Workshop）— https://arxiv.org/abs/2410.21819
5. Wang et al., *TrustJudge: Inconsistencies of LLM-as-a-Judge and How to Alleviate Them*, arXiv:2509.21117, 2025（ICLR 2026）— https://arxiv.org/abs/2509.21117 ；https://github.com/TrustJudge/TrustJudge
6. *Overconfidence in LLM-as-a-Judge: Diagnosis and Confidence-Driven Solution*, arXiv:2508.06225, 2025 — https://arxiv.org/html/2508.06225v1
7. Verga et al., *Replacing Judges with Juries: Evaluating LLM Generations with a Panel of Diverse Models (PoLL)*, arXiv:2404.18796, 2024 — https://arxiv.org/html/2404.18796v2
8. Jung, Brahman, Choi, *Trust or Escalate: LLM Judges with Provable Guarantees for Human Agreement*, arXiv:2407.18370（ICLR 2025）— https://arxiv.org/abs/2407.18370
9. *VerifyBench: Benchmarking Reference-based Reward Systems for Large Language Models*, arXiv:2505.15801, 2025（ICLR 2026）— https://arxiv.org/html/2505.15801v1 ；http://zjureal.com/VerifyBench/
10. *Evaluating Scoring Bias in LLM-as-a-Judge*, arXiv:2506.22316, 2025 — https://arxiv.org/html/2506.22316v2
11. Ye et al., *Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge (CALM)*, arXiv:2410.02736（ICLR 2025）— https://arxiv.org/abs/2410.02736 ；https://llm-judge-bias.github.io/
12. *A Survey on LLM-as-a-Judge*, arXiv:2411.15594（v6）— https://arxiv.org/html/2411.15594v6 ；Cell Press 版 https://www.cell.com/the-innovation/fulltext/S2666-6758(25)00456-4
13. *Judging the Judges: A Systematic Evaluation of Bias Mitigation Strategies*, 2026（具体数字未抓取）— https://www.scivora.io/articles/judging-the-judges-a-systematic-evaluation-of-bias-mitigation-strategies-in-llm--2026
14. 位置偏差中文工程总结（二手）— https://walterwang0x01.github.io/portfolio/posts/llm-as-judge-bias-calibration/
