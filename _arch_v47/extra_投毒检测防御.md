# 方向 83：数据投毒的检测与防御（Poisoning Detection & Defense）

> 定位：方向 91 已梳理投毒**攻击**方法，本方向聚焦"如何**发现**并**抵御**"。覆盖五条技术路线：异常检测（outlier detection）、影响函数（influence functions）、鲁棒统计（robust statistics）、数据清洗与数据增强、差分隐私（DP）缓解，外加 trigger inversion（触发器逆向）检测。最后落到阙疑自身：67 规则 / 9 保护器 / 452 条 append-only 账本若被污染（恶意提交假知识卡），如何检测。

---

## 核心结论

1. **被动式"先过滤再训练"（data sanitization）已被系统性攻破**：Koh、Steinhardt、Liang（斯坦福，NeurIPS 2018，期刊版 Machine Learning 2021）证明基于最近邻、训练损失、SVD 的异常检测器均可被"协同贴近 + 约束优化"的投毒绕过——**仅 3% 投毒数据**即可把 Enron 垃圾邮件测试错误率从 3% 推到 **24%**、IMDB 情感分类从 12% 推到 **29%**（摘要逐字核实）。含义：异常检测只能当"第一道滤网"，不能当防御主张本身。
2. **最有效的检测信号往往在"中间表征"而非原始数据**：SPECTRE（Hayase 等，UW/Stanford，ICML 2021）用鲁棒协方差估计放大中毒样本的谱签名；RevPRAG（Tan 等，EMNLP 2025 Findings）用 LLM 中间激活检测 RAG 投毒，达到 **98% 真阳性率、~1% 假阳性率**（摘要逐字核实）；Neural Cleanse（Wang 等，UC Santa Barbara，IEEE S&P 2019）用触发器逆向 + 中值绝对偏差（MAD）异常检测定位后门，unlearning 缓解可把攻击成功率压到 **<6.70%**。
3. **差分隐私与数据增强是"有限但真实"的主动防线**：Geiping 等（Witches' Brew，ICML 2021）承认强 DP（Abadi et al. 2016）是其梯度匹配攻击下"唯一现存的防御"（摘要级表述，具体 ε 未核实），但 DP-Poison（CIKM 2024）表明 FL 场景下攻击者可**利用 DP 本身作掩护**投毒；Borgnia 等（ICASSP 2021）显示 mixup/CutMix 等增强可清洗投毒与后门攻击且不掉精度。对阙疑这类非神经网络规则系统，"中值/裁剪均值聚合 + 来源可追溯 + 重放审计"比照搬 DP 更实际。

---

## 精确数字与案例

### 一、异常检测/数据清洗路线：有效性与被攻破的双重证据

**被攻破的一面（Koh et al. 2018，逐字摘要）**：

> "In this paper, we develop three attacks that can bypass a broad range of common data sanitization defenses, including anomaly detectors based on nearest neighbors, training loss, and singular-value decomposition. By adding just 3% poisoned data, our attacks successfully increase test error on the Enron spam detection dataset from 3% to 24% and on the IMDB sentiment classification dataset from 12% to 29%."

三种攻击分别基于影响函数、极小极大对偶、KKT 条件近似双层优化，核心思想有二：投毒点**彼此靠近**成簇、把投毒写成带约束的优化以避开检测器。作者结论是："Our results underscore the need to develop more robust defenses against data poisoning attacks."（本文后来正式发表于 Machine Learning 2021，DOI 10.1007/s10994-021-06119-y。）

**仍然有效的一面（Deep k-NN 防御，Peri et al., ECCV Workshops 2019；经知乎综述转述，原始数字未直核原文）**：

| 项目 | 数字 |
|---|---|
| 污染样本数 | 800 |
| 选取 k=5000 时移除的带毒样本 | 799 |
| 干净样本误删率 | 0.6% |
| 对 clean-label 投毒的防御成功率（该实验设置下） | 100%（剩余 1 个样本不足以单点攻击成功） |

其关键技巧：不在像素空间而在**特征空间**逐层做 k-NN 重标注，计算标签与真实标签不一致者判为污染。

**对阙疑的启示**：452 条账本天然是结构化数据（规则 ID、判决、置信度、提交者、时间戳），比图像更适合作 k-NN/MAD 异常检测——但 Koh 2018 明确警告：检测器本身就是攻击者的优化目标，**检出率必须与自适应攻击（自适应投毒）共同报告**，否则是虚假安全感。

### 二、影响函数与鲁棒统计：把"这条数据对判决的影响"算出来

- **影响函数系（influence functions）**：Koh & Liang（ICML 2017，UPenn/Stanford）奠定用 Hessian 反作用估计单点对参数影响的基础；投毒检测方向上，Δ-Influence（arXiv 2411.13731，2024-11 提交）指出 SOTA 影响函数 EK-FAC（Grosse et al., 2023）与 TRAK "often fail to accurately attribute abnormal model behavior"，并提出通过数据变换前后影响分数的**负向漂移**来定位毒点。TRIM 类防御（训练时剔除高损失离群点）在混合防御对比研究（Springer 2025 章节 "A Hybrid TRIM and N-LID Defense Against Poisoning Attacks"）中被描述为："Large-scale poisoning attacks were shown to be best addressed by TRIM, which excludes outliers during training"（TRIM 原始出处未在本次调研中直接核实，见盲区）。
- **鲁棒统计系（SPECTRE，ICML 2021，摘要逐字）**：

> "We propose a novel defense algorithm using robust covariance estimation to amplify the spectral signature of corrupted data. This defense provides a clean model, completely removing the backdoor, even in regimes where previous methods have no hope of detecting the poisoned examples."

即：先用鲁棒协方差估计（对抗小簇污染的统计估计器）再算马氏距离，把"毒簇谱签名被压平"的盲区补上。作者：Jonathan Hayase、Weihao Kong、Raghav Somani、Sewoong Oh（华盛顿大学）。代码开源：github.com/SewoongLab/spectre-defense。

- **触发器逆向 + MAD（Neural Cleanse，IEEE S&P 2019，UC Santa Barbara，Bolun Wang 等 7 人）**：对每个标签逆向工程"最小触发器"，用**中值绝对偏差（MAD）**异常检测挑出"显著小于其他触发器"的候选即后门目标。缓解两条路：神经元剪枝（GTSRB 上剪 30% 神经元把攻击成功率压到接近 0%，分类精度仅降 5.06%）；unlearning（全部模型攻击成功率降到 **<6.70%**，分类精度最大降幅 3.6%，GTSRB）。"前 1% 神经元足以启用后门"也是其经验结论。注：常见的"anomaly index 阈值 2"这一具体判定阈值在本次调研中未从原文核实（原 PDF 抓取失败）。

| 方法 | 信号源 | 统计工具 | 报告效果 | 出处 |
|---|---|---|---|---|
| Deep k-NN | 特征空间近邻 | k-NN 重标注 | 移除 799/800 毒点，误删 0.6% | Peri et al., ECCV WS 2019 |
| TRIM | 训练损失 | 剔除高损失点 | 对大规模投毒最佳（转述） | Springer 2025 章节 |
| SPECTRE | 中间表征 | 鲁棒协方差 + 马氏距离 | 完全移除后门（既往方法失效区间） | Hayase et al., ICML 2021 |
| Neural Cleanse | 逆向触发器 | MAD 异常检测 | unlearning 后 ASR < 6.70% | Wang et al., S&P 2019 |
| Δ-Influence | 影响分数漂移 | Hessian 近似 | 归因 EK-FAC/TRAK 失效场景 | arXiv 2411.13731 |

### 三、知识库投毒检测：与阙疑"假知识卡"最同构的战场

**攻击面（PoisonedRAG，Zou、Geng、Wang、Jia，USENIX Security 2025，摘要逐字）**：

> "Our results show PoisonedRAG could achieve a 90% attack success rate when injecting five malicious texts for each target question into a knowledge database with millions of texts. We also evaluate several defenses and our results show they are insufficient to defend against PoisonedRAG, highlighting the need for new defenses."

即：在**数百万条文本**的知识库里每个目标问题只注 **5 条**恶意文本即达 90% 攻击成功率（有一二手转述称对 GPT-4 在 2.68M 语料下达 97%，该数字来自第三方聚合站 threatatlas.ai，未直核原文表格）。论文明确评价了多种**已有防御且判定不足**——这与方向 91 的攻击侧结论正好闭环。

**检测面（RevPRAG，Tan 等 6 人，Findings of EMNLP 2025，pp. 12999–13011，苏州，摘要逐字）**：

> "Our results on multiple benchmarks and RAG architectures show our approach can achieve a 98% true positive rate, while maintaining a false positive rate close to 1%."

机制：对比 LLM 生成"中毒响应 vs 正确响应"时的**中间激活模式差异**，自动化检测管线。这是目前知识库投毒检测公开数字最高的方案之一（AUC 等更细指标未核实）。

**指令微调投毒的规模门槛（Wan、Wallace、Shen、Klein，UC Berkeley，ICML 2023，摘要逐字）**：

> "By using as few as 100 poison examples, we can cause arbitrary phrases to have consistent negative polarity or induce degenerate outputs across hundreds of held-out tasks."

且防御结论悲观："defenses based on data filtering or reducing model capacity provide only moderate protections while reducing test accuracy."（数据过滤类防御只有中等保护且掉精度。）

**知识图谱投毒**：联邦知识图谱嵌入（FKGE）场景 2026 年出现首个系统性非定向投毒研究（"Unveiling and Mitigating Untargeted Poisoning Attacks on FKGE"，ACM，2026-04，其中嵌入级攻击最有效），以及 co-distillation 防御框架（ScienceDirect，2026-04）。均属新文献，细节未深入核实。

**对阙疑的映射**：阙疑的 452 条账本 ≈ PoisonedRAG 的知识库，"假知识卡" ≈ 5 条恶意文本。区别在于：阙疑判决可复算（有独立对账器），因此检测信号不必依赖激活，可用"判决翻转影响"（见行动 2）替代 LLM 激活分析——这是阙疑相对 RAG 文献的结构性优势。

### 四、差分隐私、数据增强与认证式主动防御

- **DP 的两面**：Geiping、Bauermeister、Dröge、Moeller / Fowl、Goldstein 等（Witches' Brew，arXiv 2009.02276，ICML 2021，ImageNet 级工业规模梯度匹配投毒）在防御讨论中的表述（ar5iv 版逐字）："We close by discussing previous defense strategies and how strong differential privacy (Abadi et al., 2016) is the only existing [defense found to resist]"（末句完整逐字未核，主旨为强 DP 是唯一幸存防御——半核实，见盲区）。反例：DP-Poison（Zhang 等，ACM CIKM 2024 / TOIS 期刊版 10.1145/3702325）证明联邦学习下攻击者可在 DP 噪声掩护下投毒，且"maintaining the main task performance"。结论：DP 抬高攻击成本但不等于免疫，且阙疑不训练神经网络，DP-SGD 无直接落点——可借鉴的是其**单样本梯度裁剪思想**：对单张知识卡的"账本影响力"设上限（clamping）。
- **数据增强清洗（Borgnia et al., ICASSP 2021，"Strong Data Augmentation Sanitizes Poisoning and Backdoor Attacks Without an Accuracy Tradeoff"）**：攻击者用 clean-label 投毒污染目标类 10% 图像的设置下，mixup 与 CutMix 均显著压低投毒成功率，CutMix 更优，且可叠加集成学习。经知乎综述（p/624208064）转述核对引用。
- **认证式鲁棒（Jia、Cao、Gong，AAAI 2020，"Intrinsic Certified Robustness of Bagging against Data Poisoning Attacks"）**：m 个子模型投票，集成方差 σ²/m——给出投毒下预测可证稳定界。这是少数给出**证书**（certificate）而非经验数字的防御路线。

| 主动防御 | 类型 | 关键数字 | 出处 |
|---|---|---|---|
| 强 DP（DP-SGD） | 训练时加噪 | Witches' Brew 攻击下唯一幸存（半核实） | Geiping et al., ICML 2021 |
| Bagging 投票 | 集成 | 方差 σ²/m，可证鲁棒 | Jia et al., AAAI 2020 |
| mixup / CutMix | 数据增强 | 10% clean-label 投毒被压制，CutMix 更优 | Borgnia et al., ICASSP 2021 |
| DP-Poison（反例） | 攻击 | DP 掩护下投毒不掉主任务精度 | ACM 10.1145/3702325 |

---

## 对阙疑的 3 条具体行动

1. **给 452 条账本建"规则级 MAD 异常检测器"（2027-03 前）**。新建 `tools/ledger_anomaly_scan.py`（只读账本，不改 gate_engine.py）：对每条规则统计其在 452 条判决中的命中率、置信度分布、触发间隔，用中值绝对偏差（MAD，与 Neural Cleanse 同款统计）标记偏离中值 > 3.5×MAD 的规则/提交模式；输出报告落盘 `research/ledger_anomaly_report_2027Q1.md`。同时对 9 保护器输出聚合方式做鲁棒化改造：凡聚合处（投票/求均值）改为**中值或 20% 裁剪均值**，防单点保护器被腐化拖偏均值。在论文 Threat Model 节写明：检测器以 Koh et al. 2018 的自适应攻击为对手模型，不宣称"免疫"。
2. **做一次"3% 自适应投毒压力测试"并报告检出率（2027-05 前，与盲 holdout 数据同批）**。仿 Koh 2018 的 3% 剂量：在账本副本上程序化插入约 14 条（452×3%）互相"贴近"的假知识卡（同主题、同规则簇、置信度调至逃过简单阈值过滤），先用现有 67 规则引擎过滤，再用行动 1 的检测器检，报告检出率/误删率两个数——这直接补上阙疑目前"0 个投毒相关实验"的空白，且与方向 91 的攻击侧实验构成攻防对（论文里是天然的 datasets+findings 双贡献）。结果写进 `research/12_threats_to_validity.md` 新增小节 **T5：账本投毒与检测**。
3. **给知识卡引入"来源哈希 + 影响审计"两级元数据（2027-06 前）**。每张知识卡新增字段 `source_hash`（提交内容哈希）与 `provenance`（来源：人工/AI 辅助/corpus 抽取），append-only 链已可追，缺的是字段本身；再加 `leave-one-out_impact`（移除该卡后 37 实卡判决翻转数，离散版影响函数，每次 checkpoint 重算一次，成本 O(N) 可接受）。审计对账器（第三方复算）读这两个字段即可复现"这张卡是否对判决分布有异常影响"——把 RevPRAG 的"激活差异"思想替换为阙疑特有的"判决翻转差异"，在论文 E&D 投稿中作为可审计数据集管护（dataset stewardship）的证据点。时间节点与 NeurIPS 2027（约 2027-05 截稿）匹配：T5 实验 05 前完成，元数据字段在 camera-ready 前完成即可。

---

## 盲区（诚实标注）

- **Neural Cleanse 的 "anomaly index 阈值 = 2" 未核实**：原 S&P 2019 PDF（people.cs.uchicago.edu）WebFetch 失败，中文解读（cnblogs/gm7）均未给出该具体阈值；本文只引用了核实到的 unlearning <6.70%、剪枝 30% 神经元等数字。写论文引用前需读原文 Table/Section 5。
- **Witches' Brew 中 DP 具体防御数字未核实**：只核实到摘要级"强 DP 是唯一现存防御"的主旨表述（且经 ar5iv 二次转述，末句逐字存疑）；DP-SGD 的 ε 设置、攻击在 DP 下的成功率下降幅度均未取到。
- **PoisonedRAG 的 97% ASR（GPT-4，2.68M 语料）为二手来源**（threatatlas.ai 聚合页），原文摘要只写 90%；论文中各防御（paraphrasing 等）"不足"的具体数字未取到，引用时应回读 USENIX Security 2025 正文表格。
- **TRIM 的原始出处未核实**：只从 Springer 2025 章节与 Δ-Influence 的 related work 侧面确认其"训练中剔除离群点"机制，未找到 TRIM 首次提出的论文标题与年份，本文件未标注其原始引用。
- **RevPRAG 的 98% TPR / ~1% FPR 来自摘要**，具体用哪些 benchmark、哪些 RAG 架构、AUC 值未从正文核实；且其信号依赖 LLM 内部激活，对黑盒 API 场景不适用——迁移到阙疑时只能借思想不能借数字。
- **Deep k-NN（Peri et al. 2019）的全部数字经知乎中文综述转述**，未直核 ECCV Workshops 原文；"防御成功率 100%"的限定条件（单点攻击不可成）容易被误读，论文写作时若引用必须回原文。
- **样本偏差与赛道契合**：本方向检索以 2018–2026 图像/NLP 分类与 RAG 场景为主，"结构化知识条目/规则账本投毒检测"几乎没有直接文献（最接近的是知识图谱嵌入投毒，2026 年才有首批工作）——阙疑在该交叉点上大概率是空白，但也意味着无现成 baseline 可比，论文需自建评测协议。反过来看这对 NeurIPS E&D 是利好：官方定位 "evaluation itself becomes an object of scientific study"，且欢迎 negative results——若 3% 自适应投毒压力测试中检测器检出率很低（类似外部 corpus 43.8% 的惨淡数字），这本就是一个诚实且有信息量的 negative result，可按 E&D 的批判性分析口径写入论文，而不必粉饰。

---

## 来源

1. Stronger Data Poisoning Attacks Break Data Sanitization Defenses — https://arxiv.org/abs/1811.00741 — "By adding just 3% poisoned data … Enron 3% to 24%, IMDB 12% to 29%" — Pang Wei Koh, Jacob Steinhardt, Percy Liang（Stanford），NeurIPS 2018 / Machine Learning 2021 — 提交 2018-11-02，v2 2021-12-03
2. PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of LLMs — https://arxiv.org/abs/2402.07867 — "90% attack success rate when injecting five malicious texts … into a knowledge database with millions of texts；evaluated defenses are insufficient" — Wei Zou, Runpeng Geng, Binghui Wang, Jinyuan Jia，USENIX Security 2025 — 2024-02-12（v3 2024-08-13）
3. RevPRAG: Revealing Poisoning Attacks in RAG through LLM Activation Analysis — https://aclanthology.org/2025.findings-emnlp.698/ — "98% true positive rate, while maintaining a false positive rate close to 1%"（pp. 12999–13011）— Xue Tan 等 6 人，Findings of EMNLP 2025，苏州 — 2025-11
4. SPECTRE: Defending Against Backdoor Attacks Using Robust Statistics — https://arxiv.org/abs/2104.11315 — "robust covariance estimation to amplify the spectral signature … completely removing the backdoor" — Jonathan Hayase, Weihao Kong, Raghav Somani, Sewoong Oh（UW），ICML 2021（PMLR v139）— 2021-04-22
5. Poisoning Language Models During Instruction Tuning — https://arxiv.org/abs/2305.00944 — "as few as 100 poison examples … data filtering … provide only moderate protections" — Alexander Wan, Eric Wallace, Sheng Shen, Dan Klein（UC Berkeley），ICML 2023 — 2023-05-01
6. Witches' Brew: Industrial Scale Data Poisoning via Gradient Matching — https://arxiv.org/abs/2009.02276 — "strong differential privacy (Abadi et al., 2016) is the only existing defense"（摘要级表述，半核实）— Jonas Geiping 等，ICML 2021 — 2020-09-04
7. Neural Cleanse: Identifying and Mitigating Backdoor Attacks in Neural Networks — https://people.cs.uchicago.edu/~huiyingli/publication/backdoor-sp19.pdf（本次抓取失败，数字经 https://www.cnblogs.com/ggyt/p/18573893 解读页核实）— unlearning 后 ASR < 6.70%；剪 30% 神经元 ASR≈0%、精度 -5.06% — Bolun Wang 等（UC Santa Barbara），IEEE S&P 2019
8. Δ-Influence: Unlearning Poisons via Influence Functions — https://arxiv.org/abs/2411.13731 — "EK-FAC and TRAK often fail to accurately attribute abnormal model behavior" — arXiv 2024-11（OpenReview 2026 版本见 https://openreview.net/forum?id=4XtcG8NNaG）
9. Data Poisoning in Deep Learning: A Survey — https://arxiv.org/abs/2503.22759 — 2025-03-27 综述，配套 GitHub https://github.com/Pinlong-Zhao/Data-Poisoning — Pinlong Zhao 等
10. DP-Poison: Poisoning Federated Learning under the Cover of Differential Privacy — https://dl.acm.org/doi/10.1145/3702325 — DP 噪声掩护下投毒且保持主任务性能 — ACM（CIKM 2024 / 期刊版）— 2024-11
11. Deep k-NN Defense Against Clean-Label Data Poisoning Attacks — Peri et al., ECCV Workshops 2019（数字经知乎综述 https://zhuanlan.zhihu.com/p/624208064 转述，原文未直核）— k=5000 移除 799/800 毒点、误删 0.6%
12. 人工智能安全笔记（4）数据投毒 — https://zhuanlan.zhihu.com/p/624208064 — 被动/主动防御二分法、k-NN、Bagging、mixup/CutMix 数字与引用 — 知乎专栏（二手，用于线索定位）
