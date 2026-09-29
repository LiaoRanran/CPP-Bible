# 方向 01：Pangram AI 检测工具原理

## 核心结论

1. **Pangram 不是一个"困惑度+突发性"启发式工具，而是一个基于 transformer 的监督式分类器**，其技术核心是 **hard negative mining with synthetic mirrors（合成镜像难负样本挖掘）**：先用"这段文字的主题是什么 → 写一篇关于该主题的文章"两步流程批量生成与人类文本**同主题**的 AI 文本，从而让模型学"这段文字是**怎么**写的"而不是"**关于什么**"（原文：*"We want the model to learn 'How was this text written?' as opposed to 'What is this text about?'"*）。第一代 Pangram Text 报告 99% 准确率，并在领域加权假阳性率上把基线 **2.29% 降到 0.02%**（降幅 100–1000 倍）。
2. **Pangram 3.3.2（就是 NeurIPS 2026 Position Track 用来 desk reject 178 篇的那一版）自身的公布数字是 FPR 0.0539% / FNR 1.9942%**；一个月后发布的 **Pangram 4** 把同一测试集上的 FPR 降到 **0.0041%**（≈1/24,300）、FNR 降到 **0.3396%**，AUROC **0.9916**。也就是说：**NeurIPS 那次筛稿用的是一台比当时最新版差 13 倍假阳性率的机器**（0.0539% ÷ 0.0041% ≈ 13.1）。
3. **Pangram 厂商自己给出的"1/24,300"是在自家分布上测的**，而 2023 年 Stanford 的独立研究测出 7 个商用检测器在 91 篇 TOEFL 作文上的**平均假阳性率 61.22%**。Pangram 用 4 个公开 ESL 语料（ELLIPSE/ICNALE/PELIC/Liang-TOEFL，合计 24,586 篇）报告**总假阳性 1 篇（0.0041%）**——但正如批评者指出的：**这项结果至今没有独立复现**（*"we found no independent replication"*）。对阙疑而言，真正的结论不是"Pangram 准不准"，而是 **"AI 检测器已经成为投稿流程中不可申诉的前置关卡"**，这直接决定项目的写作与披露策略。

---

## 精确数字与案例

### 一、Pangram Text（第一代）的技术细节

来源：*Technical Report on the Pangram AI-Generated Text Classifier*，arXiv:2402.14873v3（2024-07-29），作者 Bradley Emi、Max Spero（Pangram Labs）。

**架构**（逐字）：

> "Our model is a slightly modified transformer-style architecture (Vaswani et al., 2017)."
> "We present Pangram Text, a transformer-based neural network trained to distinguish text written by large language models from text written by humans."
> "We propose a training algorithm, hard negative mining with synthetic mirrors, that enables our classifier to achieve orders of magnitude lower false positive rates on high-data domains such as reviews."

**训练数据规模与分布**：

> "we begin by considering a total pool of approximately 28 million confirmed human-written documents"
> "We exclude 4 million examples from our training pool as a holdout set to evaluate false positive rates"

| 领域 | 人类文本样本数 |
|---|---|
| Business and Product Reviews | 15,000,000 |
| Books | 7,000,000 |
| Scientific Papers | 3,000,000 |
| Wikipedia | 1,000,000 |
| Q&A | 1,000,000 |
| News Articles | 500,000 |
| Creative Writing | 300,000 |
| ESL（英语作为第二语言） | 165,000 |
| Student Writing | 23,000 |
| Email | 16,000 |

训练流程分两步：初始训练集 **每领域 40,000 条（n=360,000）**；随后**每领域挑 10,000 条假阳性（m=80,000），生成等量合成镜像加入训练集后重训**。

> "Hard negative mining reduces false positive rates by 100x-1000x on holdout sets."

**难负样本挖掘前后的分领域 FPR**：

| 领域 | 基线模型 | 难负样本挖掘后 |
|---|---|---|
| Creative Writing | 1.51% | 0.02% |
| Reviews | 1.81% | 0.02% |
| Books | 0.85% | 0.01% |
| Scientific Papers | 1.54% | **0.04%** |
| Wikipedia | 5.34% | 0.05% |
| News | 0.55% | 0.001% |
| Q&A | 2.52% | 0.009% |
| ESL | 1.44% | **0.01%** |
| Email | 6.60% | 0.00% |
| **领域加权总计** | **2.29%** | **0.02%** |

**竞品对比（1,976 篇文档基准，对比 GPTZero / Originality.ai / DetectGPT）**：

> "Our model is the most accurate at 99%, compared to commercial competitors which do not even clear 95%. Our false positive rate is better than the second best model, GPTZero, by a factor of 3, which achieving 7 times better negative error rate."
> "Notably, GPTZero's false negative rate is 10.02%– it is extremely biased towards predicting false negatives rather than false positives."
> "Originality has the opposite issue– its false positive rate is 9.24%, which is simply too high to be practical."

**未见过的开源 LLM 召回率（1% FPR 下）**：

| LLM | Recall @ 1% FPR |
|---|---|
| OpenChat 3.5 | 100.00% |
| Qwen1.5-72B-Chat | 99.93% |
| Vicuna-13B-v1.5 | 99.85% |
| DeepSeek-Coder-33B-Instruct | 99.75% |
| Yi-34B-Chat | 99.68% |
| MythoMax-L2-13b | 99.61% |
| SOLAR-10.7B-Instruct-v1.0 | 99.61% |

2024-07 增补：**GPT-4o 100.0%**、**LLaMA 3 99.97%**、**Claude 3 99.76%**（基准 25,000 篇文档）。

**厂商自己写下的免责声明**（这条对阙疑写 Threats to Validity 极有价值）：

> "We strongly discourage the use of our classifier as a sole arbiter of academic integrity and plagiarism checking. All AI detection tools have a nonzero false positive rate, and should be used in conjunction with other evidence to prove or disprove plagiarism."
> "AI detection is not a substitute nor a reliable tool for proving the factuality or verity of textual information such as news and media."

### 二、Pangram 4 与 3.3.2 的代际差（这是全篇最关键的一张表）

来源：*Pangram 4 Technical Report*，arXiv:2607.27183v1（2026-07-29），Pangram Labs + University of Maryland；作者 Ben Glickenhaus、Katherine Thai、Jenna Russell、Elyas Masrour、Yue Han、Max Spero、Bradley Emi。许可 CC BY-NC-ND 4.0。

**架构**：基于一个开源 MoE 骨干 + 每个任务一个 dense 分类头；构建在 **Pangram 3（EditLens 架构，Thai et al., 2026）** 之上。三类输出标签：`human / ai-assisted / ai-generated`，**逐 token** 输出 logits。

> "The model architecture of Pangram 4 is based on a popular open-weight MoE model. We attach a single dense layer as a custom classification head for each task…"
> "produces logits Z_tok ∈ ℝ^{S×3} over the classes {human, ai-assisted, ai-generated} for each token."

为了修掉因果注意力导致"句首 token 只能看前缀"的问题，用了 **Repeat2**（Leviathan et al., 2025）——把输入序列复制两遍 `x̃ = (x₁,…,x_S, x₁,…,x_S)`，只在第二份上算 loss。推理时长文档切成 **512 token 窗口、步长 256（50% 重叠）**，再用一个三状态线性链 **CRF** 做 MAP 解码。

**核心指标（摘要逐字）**：

> "We achieve an AUROC of 0.9916 with a false positive rate of 0.0041% and a false negative rate of 0.3396%."
> "Pangram 4 achieves the highest accuracy on the AI-text detection task while maintaining a false positive rate of 0.0041% (roughly 1 in 24,000)."

| 指标 | Pangram 3.3.2 | Pangram 4 | 倍数改善 |
|---|---|---|---|
| 假阳性率 FPR（>100 万人类英文文本） | **0.0539%** | **0.0041%**（CI 0.0032%–0.0050%） | 13.1× |
| 假阴性率 FNR（520,000 条 AI 输出，实际打分 519,993） | **1.9942%** | **0.3396%**（CI 0.3242%–0.3558%；1,766 个 FN） | 5.9× |
| AI 润色文本被误判为 AI 的比例 | 0.18% | **0.01%** | 18× |
| AI 辅助（AI-edited）文本召回（n=14,990） | 5.54% | **55.01%** | 9.9× |
| WildChat 编辑文本 AI 辅助召回（n=4,826） | 12.62% | **65.17%** | 5.2× |
| 异质混合文本逐 token 准确率（Overall） | 64.18% | **92.02%** | — |
| 异质混合文本 Doc MAE（越低越好） | 28.60% | **5.87%** | 4.9× |

**按生成模型家族的 FNR（Pangram 4 报告表 3）**：

| 生成模型家族 | Pangram 3.3.2 | Pangram 4 |
|---|---|---|
| Anthropic（Claude 家族） | 1.002% | **0.195%** |
| OpenAI（GPT 家族） | 1.561% | **0.316%** |
| Google Gemini 家族 | 5.138% | **0.498%** |
| DeepSeek V4 家族 | 1.838% | **0.388%** |
| **总体** | **1.9942%** | **0.3396%** |

**多语言（5.6）**：在 FineWeb2 的 **104 种语言、996,273 条**样本上只出现 **14 个假阳性**，多语言 FPR **0.0014%**（CI 0.0008%–0.0024%），多语言 FNR **1.24%**。作者自己指出 **Urdu 5.31%、Persian 3.17%** 的高假阴性率可能源自骨干模型的分词差异——**这是一条被厂商自己承认的"语言相关的不确定性"**。

**非母语英语（5.7）**：

| 语料 | N | 假阳性数 | Pangram 4 FPR | Pangram 3.3.2 FPR |
|---|---|---|---|---|
| ELLIPSE | 3,899 | 0 | 0.000% | 0.000% |
| ICNALE | 5,593 | 0 | 0.000% | 0.000% |
| PELIC | 15,005 | 1 | 0.0067% | 0.0133% |
| Liang TOEFL | 89 | 0 | 0.000% | 0.000% |
| **总计** | **24,586** | **1** | **0.0041%** | **0.0081%** |

**对抗鲁棒性（5.9）**：

> "We find Pangram is robust to humanization attempts. We detect humanized text as AI-generated 97.67% of the time and as either Mixed or AI-generated 98.83% of the time."

BLADER 系列"人类化 agent skill"重写后的 10,223 篇文本中，仅 **44 篇（0.430%）** 成为假阴性。自动红队 agent 跑 24 小时**未发现新的假阳性**。

**厂商自己承认的局限（结论部分逐字，值得抄进阙疑的 Related Work）**：

> "its estimates are statistical, and both false positives and false negatives, although rare, do occur. Its predictions are also to some degree a black box… Predictions for the same text in different contexts may also be inconsistent. For example, a section of a paper run in isolation may receive a different prediction than it does within the full context of the paper."
> "Finally, Pangram 4 does not account for people who intentionally write like LLMs or who have absorbed elements of LLM style into their writing. This form of data drift is a major focus of our ongoing research."

**厂商自己的 AI 使用披露（这条对阙疑的合规策略是决定性的）**：

> "We use AI agents extensively for coming up with research ideas, processing data, writing code, running experiments, and evaluating results. We use some AI assistance in the writing of the technical report, for proofreading and review, but the majority of the writing is ours. We claim full responsibility for the factual accuracy of the claims we make in this report."

——**即：一家 AI 检测公司自己用 AI agent 做研究、写代码、跑实验、写报告，并公开披露。** 这说明学术界现行规范不是"不能用 AI"，而是**"必须如实披露且人对事实负责"**。

**商业背景**：2026-07-29 Pangram Labs 完成 **900 万美元种子轮**，同期发布 Pangram 4 与 Pangram Image（图像检测研究预览）。

### 三、NeurIPS 2026 Position Track 事件：AI 检测如何变成不可申诉的关卡

来源：StrictCite 报道（2026-09-08，含 09-10 更新、09-26 更正）、NeurIPS 官方博客（2026-06-02）、CASRAI 报道（2026-07-23）、Creeta 报道（2026-06-09）。

**规模与判定**：

| 项目 | 数字 |
|---|---|
| 送检论文总数 | **969** |
| 使用检测器 | **Pangram 3.3.2**（注意：Pangram 4 在决定做出后一个月才发布） |
| 初判落在 90–100% "AI 生成"区间 | **42.7%** |
| 拿到满分 100% 的论文 | **28.2%（273/969）** |
| 调整窗口后 90–100% 比例 | **从 42.7% 降到 12.7%** |
| 直接 desk reject | **178 篇（18.4%）**，标准情况下**不接受申诉** |
| 有条件（须提交版本历史，否则同样拒） | **123 篇（12.7%）**，截止 **2026-06-15** |
| 通过 | **668 篇（68.9%）** |
| 最终决定发布日 | **2026-09-24** |

**三条判据（不是单一阈值）**：

- **77 篇**：Pangram 分数 ≥ 0.9，无其他条件；
- **79 篇**：分数 ≥ 0.8 **且** 作者提交了多篇单人署名论文（其中至少一篇超阈值），或该作者已有至少一次 desk reject；
- **22 篇**：分数 ≥ 0.5 **且** 作者声明"未使用 AI"或未作声明。

> "The 178 desk rejections were not a single threshold. They were driven by three separate criteria"

**官方口径**：

> 要求所有投稿 "substantially human-written"，生成式 AI 仅允许用于 "copy-editing or similar peripheral changes"；
> 称这是 "a standard desk-rejection"，三组均 "not subject to appeal under standard circumstances"；
> 主席给出的理由：这样做 "externalizes the cost of verification onto reviewers"。

**趋势数据（官方披露）**：

> "the number of submissions with a Pangram AI score ≥90% increased more than tenfold from 2025 to 2026"

**校准争议的两组实测**：

- **主席方的负对照**：用 ACM FAccT 2022（ChatGPT 普及之前的会议）论文集测试，检测器给出 **0.0% 假阳性**。
- **Berezin 的校准测试**：把**本 track 主席们自己的近期论文**过同一个 Pangram，得到 **24%、36%、45%、69%** 四个 AI 概率分。

> "Had one of the chairs' own papers been submitted with such a declaration, its 0.69 score would have met that tier's threshold."

**循环论证的批评**：

> "The detector's output functioned as ground truth. If it disagreed with the attestation, the attestation lost. Critics called this circular"

**StrictCite 的定性总结**（这是全篇最值得引用的一句）：

> "One is an audit; the other is an opinion with a confidence interval."
> （引文检查器是在做审计——"这个 DOI 不存在"是可核验事实；AI 内容检测器给出的是概率估计——"68% 可能是 AI"。）

### 四、独立证据：Stanford 2023 的非母语者偏差

来源：Liang, W., Yuksekgonul, M., Mao, Y., Wu, E., Zou, J. *GPT detectors are biased against non-native English writers*，arXiv:2304.02819；Stanford HAI 新闻稿（2023-05-15）。

- 测试 **7 个**当时的商用检测器：Originality.AI、Quil.org、Sapling、OpenAI Detector、Crossplag、GPTZero、ZeroGPT（访问日期 **2023-03-15**；多数以 **GPT-2** 为骨干）。
- 样本：**91 篇**人类撰写的 TOEFL 作文 + **88 篇**美国八年级作文（Hewlett ASAP）。
- 结果：
  > "The detectors demonstrated near-perfect accuracy for US 8-th grade essays. However, they misclassified over half of the TOEFL essays as 'AI-generated' (average false positive rate: 61.22%)."
- **18/91（19.78%）**被 7 个检测器**一致**判为 AI；**89/91（97.80%）**至少被一个检测器判为 AI。
- 被一致误判的作文**困惑度显著更低**（P = 9.74E-05）。
- 语言多样性干预后：平均假阳性率 **从 61.22% 降到 11.77%（降幅 49.45%）**，只剩 **1/91（1.10%）**被一致判为 AI。
- 反向实验：把美国八年级作文**改成非母语者风格**，误判率**从平均 5.19% 升到 56.65%**。
- 简单二次自编辑提示词可把检测率**从 100% 降到 13%**（伪造摘要场景：从最高 68% 降到最高 28%）。

Pangram 官方对这项研究的回应（2025-04-23 博客，2026-05 更新）承认其存在，但指出两点：样本只有 91 篇 TOEFL 作文；作者把"GPT-4 改写过的文本"标为 human。Pangram 同时给出自己的 ESL 结果（**总计 25,021 篇，总体 FPR 0.012%**）与对 TurnItIn 的对比：

| 数据集 | Pangram FPR | TurnItIn FPR |
|---|---|---|
| L2（ESL）英语，300+ 词 | **0.02%** | 1.4% |
| L1（母语）英语，300+ 词 | **0.00%** | 1.3% |

### 五、价格与可用性（对阙疑有直接操作意义）

来源：CASRAI 评测（2026-08-18 核验）、Pangram 官方定价页。

| 档位 | 价格 | 字数额度 | 图像扫描 | API 额度 |
|---|---|---|---|---|
| Free | $0 | 2,000 词/日（≈60,000/月） | 3/日 | 无 |
| Individual | $20/月（年付省 $60） | 300,000/月 | 100/月 | 无 |
| Team | $20/座/月（至少 2 座） | 300,000/座/月 | 100/座/月 | 无 |
| Professional | $65/月（年付省 $240） | 1,500,000/月 | 500/月 | $200/月 |
| Developer API | $25 – $1,000 分档 | — | — | 大批量 20% 折扣 |

CASRAI 给的核心判断：

> "at 10,000 submissions a term, a 1% FPR means 100 wrongly-flagged students."
> "A detection score is evidence to open a conversation, never a finding on its own."

---

## 对阙疑的 3 条具体行动

1. **立刻做一次"自测"，把结果写进 Threats to Validity。** 具体做法：新建 `research/12_threats_to_validity.md`，增加小节 **`T1: The AI-detector gate precedes scientific review`**，写入三条硬事实——(a) NeurIPS 2026 Position Track 用 **Pangram 3.3.2** 筛 969 篇，**178 篇（18.4%）**被直接 desk reject 且**标准情况下不可申诉**；(b) 该次筛稿用的 3.3.2 的公布 FPR 是 **0.0539%**，而一个月后发布的 Pangram 4 是 **0.0041%**，即**关卡用的模型比当时最新版差 13 倍**；(c) 官方披露"AI 分 ≥90% 的投稿 2025→2026 **增长十倍以上**"。然后**在同一小节贴出阙疑自己用免费额度（2,000 词/日）对论文 Abstract + Intro 的实测分数**，并注明检测日期与版本号。时间点：**2026-10 底前完成第一次实测**，2027-05 投稿前复测。
2. **建立"人机分工留痕"目录，把披露变成资产而不是风险。** 在仓库新建 `_provenance/`（与 `_arch_v47/` 同级，但**必须加入 `.gitignore` 的白名单管理**，因为它是证据而非产物），结构为 `_provenance/YYYY-MM-DD_<section>.md`，每条记录四个字段：`prompt_sha256`、`model+version`、`human_edit_summary`（人改了什么，至少 3 句）、`verifier`（谁复核了事实）。**先照抄 Pangram 4 的披露范式写一份 `AI_DISCLOSURE.md`**——它的原文是 *"We use AI agents extensively for coming up with research ideas, processing data, writing code, running experiments, and evaluating results… the majority of the writing is ours. We claim full responsibility for the factual accuracy of the claims we make in this report."*。理由：NeurIPS 那 22 篇被判死的论文，**致命点不是"用了 AI"，而是"分数 ≥0.5 且声明未使用 AI"**——**虚假声明本身就是拒稿理由**。
3. **把"检测器不可申诉"与阙疑的核心论点接上，变成论文的一节论证。** 在 Method 或 Discussion 里加一段：AI 检测器与阙疑的**结构对称性**——两者都是"给出判决的黑箱"，但**阙疑的判决可被第三方复算、可追溯到具体规则与证据、且账本是 append-only 的**；而 Pangram 3.3.2 在 NeurIPS 的用法中 *"The detector's output functioned as ground truth"*，是**循环论证**。可直接引用 StrictCite 那句 *"One is an audit; the other is an opinion with a confidence interval."* 作为 contrast。**这一段的作用**：把"阙疑为什么需要存在"从一个工程需求升级为**一个可被 E&D track 接受的元科学论点**（因为 E&D 明确欢迎 "evaluation itself becomes an object of scientific study"）。时间点：与 `00_总览` 的第一卖点"可审计性"合并撰写，2027-06 前定稿。

---

## 盲区（诚实标注）

- **Pangram 第一代报告中的"99% 准确率""比竞品低 38 倍错误率"全部是厂商自测**，测试集（1,976 篇文档）由厂商自己构建，第三方无法核验；报告中的 Claude 被**主动排除**在基准之外（原文承认"getting Claude to respond correctly to our prompts"有问题），因此**该基准对 Claude 生成的文本的代表性未知**。
- **Pangram 4 报告的表 12（公开基准）数字我只取到部分条目**，且该报告为 **CC BY-NC-ND 4.0**（禁止演绎、禁止商用），引用时需注意许可；附录 C 的表 18–29 未取得。
- **"1 in 24,000"是在厂商自己的分布上测出的**（StrictCite 明确指出 *"'1 in 24,000' is a rate measured on the vendor's own test distribution"*）；ESL 上的 0.0041% **至今没有独立复现**。
- **NeurIPS 2026 的 969 / 178 / 42.7% / 28.2% 等数字来自二手报道（StrictCite、Creeta、CASRAI）与官方博客的转述**，我**未直接打开 NeurIPS 官方博客原文逐字核对**；StrictCite 自己标注了 09-26 更正，说明该事件的数据仍在修订中。使用时**必须以官方博客为准**。
- **Berezin 的"主席自己论文得 24%/36%/45%/69%"是"说明性检查"而非对该 track 的正式指控**（原文：*"explicitly as an illustrative check rather than a claim about how those papers were written"*），引用时不可当作"主席论文是 AI 写的"的证据。
- **Stanford 2023 研究的 7 个检测器版本与今日差异巨大**（GPT-2 骨干、2023-03 访问），其 61.22% 的假阳性率**不能直接外推到 2026 年的检测器**；但它是"结构性偏差存在"的历史证据。
- 本文件**未测试任何实际文本**，所有 Pangram 分数均为文献转述，**阙疑自己的分数仍未知**。

---

## 来源

1. Emi, B., Spero, M. *Technical Report on the Pangram AI-Generated Text Classifier* — https://arxiv.org/html/2402.14873v3 — 架构"transformer-style"、28M 人类文档、4M holdout、99% 准确率、领域加权 FPR 2.29%→0.02%、GPTZero FNR 10.02%、Originality FPR 9.24%、ESL FPR 0%、Enron FPR 0.8% — Pangram Labs — 2024-07-29
2. Glickenhaus, B., Thai, K., Russell, J., Masrour, E., Han, Y., Spero, M., Emi, B. *Pangram 4 Technical Report* — https://arxiv.org/html/2607.27183 — AUROC 0.9916 / FPR 0.0041% / FNR 0.3396%；3.3.2 为 0.0539% / 1.9942%；520,000 条合成基准；104 语言 996,273 条 FPR 0.0014%；ESL 24,586 条 1 个 FP；人类化文本 97.67% 被检出；BLADER 10,223 篇 44 个 FN — Pangram Labs + University of Maryland — 2026-07-29
3. Pangram 官方 *How does Pangram work?* — https://www.pangram.com/knowledge-hub/how-does-pangram-work — 分类器模型说明 — 2026-08-21
4. Pangram 官方 *How accurate is Pangram AI Detection on ESL?* — https://www.pangram.com/blog/how-accurate-is-pangram-ai-detection-on-esl — ESL 25,021 篇总体 FPR 0.012%；对 TurnItIn 的 L2 0.02% vs 1.4%；目标 FPR 1/10,000–1/100,000 — 2025-04-23（2026-05 更新）
5. Pangram 官方 *All About False Positives in AI Detectors* — https://www.pangram.com/blog/all-about-false-positives-in-ai-detectors — "误报远比漏报更糟"的厂商立场 — Pangram
6. Liang, W., Yuksekgonul, M., Mao, Y., Wu, E., Zou, J. *GPT detectors are biased against non-native English writers* — https://arxiv.org/html/2304.02819 — TOEFL 平均 FPR 61.22%；18/91 一致误判；89/91 至少被一个误判；干预后降至 11.77%；美国八年级作文误判 5.19%→56.65% — Stanford — 2023
7. Stanford HAI *AI-Detectors Biased Against Non-Native English Writers* — https://hai.stanford.edu/news/ai-detectors-biased-against-non-native-english-writers — 新闻稿 — 2023-05-15
8. StrictCite *NeurIPS Desk-Rejected 178 Position Papers for Being "AI-Generated"* — https://strictcite.com/blog/neurips-2026-position-paper-pangram-ai-detection — 969 篇送检 / 42.7% 落在 90–100% / 273 篇满分 / 178 篇（18.4%）拒稿 / 123 篇有条件 / 668 篇通过 / 三条判据 77+79+22 / 负对照 FAccT 2022 得 0.0% FPR / 主席论文 24%、36%、45%、69% / "One is an audit; the other is an opinion with a confidence interval." — 2026-09-08（09-10 更新、09-26 更正）
9. Creeta News *NeurIPS 2026 Position Paper Desk Rejections via Pangram AI Detector* — https://news.creeta.com/en/neurips-2026-pangram-desk-rejections-uncalibrated/ — 使用 Pangram 3.3.2 筛查全部投稿 — 2026-06-09
10. CASRAI *NeurIPS 2026 Pangram AI-Detector Desk Rejections* — https://casrai.org/news/neurips-2026-pangram-ai-detector-desk-rejection-controversy — 无申诉的自动拒稿门 — 2026-07-23
11. CASRAI *Pangram Review — AI Detector Accuracy* — https://casrai.org/guides/pangram — 定价表（Free 2,000 词/日；Individual $20/月；Professional $65/月；API $25–$1,000）；"10,000 份投稿 × 1% FPR = 100 名学生被误判" — 2026-08-27
12. dmed *When the detector says you didn't write it — lessons from the NeurIPS case* — https://dmed.co.jp/en/blog/ai-detector-desk-rejections-neurips-2026 — 官方博客 2026-06-02 发布 — 2026-07-05
13. finsmes *Pangram Raises $9M in Funding* — https://www.finsmes.com/2026/07/pangram-raises-9m-in-funding.html — 900 万美元种子轮 + Pangram 4 + Pangram Image — 2026-07-29
14. Cheng, Z. et al. *Adversarial Paraphrasing: A Universal Attack for Humanizing AI-Generated Text* — https://github.com/chengez/Adversarial-Paraphrasing — NeurIPS 2025；training-free 通用"去 AI 味"攻击 — 2025
15. Tom's Guide *I tested Pangram, the 'black light' for AI detection* — https://www.tomsguide.com/ai/i-tested-pangram-the-black-light-of-ai-detection-built-by-ex-tesla-and-google-engineers-heres-how-well-it-worked — 由前 Tesla/Google 工程师构建 — 2026-09
