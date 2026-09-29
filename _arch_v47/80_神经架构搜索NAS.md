# 方向80：神经架构搜索（NAS）

## 核心结论
1. 神经架构搜索（Neural Architecture Search，NAS）不是“让 AI 自动改任何系统”的同义词，而是把神经网络的结构选择形式化为一个优化问题：先定义搜索空间，再选择搜索策略，最后用某种性能估计方法比较候选结构。Elsken、Metzen、Hutter 的综述把 NAS 分为 search space、search strategy、performance estimation strategy 三个维度；这个三分法对阙疑尤其重要，因为阙疑当前的核心不是一个待压缩的神经网络，而是 C++ 知识断言的可复算判决、可追证据、盲态协议、append-only 哈希链、Merkle checkpoint 和独立对账器。若没有需要优化的神经网络、可微或可比较的损失函数，以及明确的部署约束，把 NAS 接进来只会制造一层难以审计的复杂度。
2. NAS 的历史确实展示了从高成本黑箱搜索到权重共享、可微搜索、硬件感知搜索的演进，但“更快”不等于“更适合阙疑”。Zoph 与 Le 的强化学习方法在 CIFAR-10 上报告 3.65% test error；NASNet 将 CIFAR-10 上搜索的 cell 迁移到 ImageNet，摘要报告 CIFAR-10 2.4% error、ImageNet 82.7% top-1。ENAS 通过共享 child models 的参数，将论文中标准 NAS 的成本降低到约 1/1000，并在单张 GTX 1080Ti 上把搜索控制在 16 小时以内；DARTS 通过双层优化把架构参数连续化，论文页面报告 second-order 结果为 3.3M 参数、2.76±0.09% CIFAR-10 error，搜索成本表中为 4 GPU days，同时把 selection cost 1 GPU day 和最终训练成本区分开。ProxylessNAS 又把目标硬件 latency 直接放入搜索，报告 200 GPU hours，而 MnasNet 约 40,000 GPU hours。历史趋势是降低代价和加入约束，不是消除实验、复现和审计成本。
3. 对阙疑的诚实结论是：当前不需要引入 NAS，且不应为了“AI 自我创造”叙事强行引入。阙疑目前只有 37 张实卡（verified 23、red-team 3、draft 11）加 10 张草稿、67 条规则、9 个保护器、452 条判决账本，内核 gate_engine.py 为 3826 行；盲 holdout 为 30 条，其中真错 17 条、检出率 66.7%，外部 corpus 40 条的 43.8% 口径还存在算术不自洽，反事实算子 P=R=F1=0，且本机 sanitizer 运行时缺失。此时首要问题是修正 ground truth、统计口径、工具链缺口、规则覆盖和可复算证据，而不是搜索一个神经网络拓扑。NAS 最多可以被记录为未来“可选的、受门槛约束的学习型旁路”技术储备：它不能改变四态最终判决，不能替代规则、编译器、测试和独立对账器，也不能成为论文当前贡献的必要组成部分。

---

## 精确数字与案例
### 一、历史路线：从控制器试错到搜索空间设计
NAS 的早期代表是 Zoph 与 Le 2016 年提交、2017 年修订的《Neural Architecture Search with Reinforcement Learning》。其做法是用 RNN controller 生成网络描述，用强化学习最大化验证集准确率。论文摘要明确报告：CIFAR-10 模型 test error 为 3.65%，比相近架构的前一项最好结果低 0.09 个百分点并快 1.05 倍；Penn Treebank 上发现的 recurrent cell test perplexity 为 62.4，比之前最好结果低 3.6。这个结果说明 NAS 的基本闭环：controller 产生候选、训练候选、用验证集反馈更新 controller。但它也暴露了代价：候选结构的每次性能估计都可能需要训练，搜索不是一次前向推理。

NASNet 的关键变化不是单纯扩大搜索，而是设计可迁移的 cell 搜索空间。Zoph、Vasudevan、Shlens、Le 的论文在 CIFAR-10 上搜索卷积 cell，再把 cell 复制、堆叠到 ImageNet；摘要报告 NASNet 在 CIFAR-10 上达到 2.4% error，在 ImageNet 上达到 82.7% top-1 和 96.2% top-5，并称相较上一项人工设计模型少 9 billion FLOPS、计算需求下降 28%。这组数字必须带着实验语境理解：它们来自图像分类 benchmark 和特定模型训练流程，不代表 NAS 对所有软件系统都能找到“更好的架构”。NASNet 的成功恰恰依赖一个可迁移的 cell 假设，而 C++ 知识验证的规则、证据和协议并不存在同构的神经 cell。

### 二、搜索空间、搜索策略和性能估计的实际含义
搜索空间决定 NAS 能够提出什么，往往比搜索算法的名称更重要。以 NAS-Bench-101 为例，固定图搜索空间最多 7 个节点、最多 9 条边，操作集合为 3×3 convolution、1×1 convolution、3×3 max-pool 三种；经过图同构处理后约有 423,000 个唯一架构，原始编码空间约为 510 million。它在 CIFAR-10 上记录 4、12、36、108 epochs 四个训练预算，并对每个架构做 3 次独立训练；论文页面还报告生成数据集的计算量超过 100 TPU years。这说明“搜索空间只有几十万个候选”并不等于“可以逐一认真训练”。

NAS-Bench-201 进一步把问题做成可复现基准：4 个节点、每条边从 5 个操作中选，候选总数 15,625；每个候选在 3 个数据集上提供训练日志和性能，并以统一数据避免不同 NAS 方法反复训练同一候选。它的价值不是证明某一个搜索算法永远最好，而是把算法比较从不可控的训练噪声和硬件差异中部分分离出来。对阙疑的启发是，任何未来的学习组件都应该先有固定、版本化、可查询的基准和日志；不能只公布一次搜索出来的架构和一个漂亮的准确率。

搜索策略大致包括强化学习、进化算法、贝叶斯优化、随机搜索和梯度型方法。性能估计又可以是从头训练、低保真训练、权重共享、代理模型或表格查询。三者之间有明显交换关系：缩小搜索空间会降低成本，却可能把正确答案排除；权重共享能复用训练，却会造成不同子网之间的权重干扰；低 epoch 评估快，却可能改变候选排序；代理 latency 便宜，却可能和真实设备行为不一致。对阙疑而言，这些不是抽象缺点：若学习模块负责知识卡片优先级或候选证据排序，排序误差可以在离线实验中接受；若它直接决定 ACCEPT、REJECT、UNCERTAIN、BLOCK 等最终态，任何搜索近似都不应绕过可复算判决和人工可审计证据。

### 三、DARTS、ENAS 与 ProxylessNAS 的成本账本
DARTS 把离散选择连续化。在每条边上对候选操作使用 softmax 混合，以架构参数 alpha 和网络权重 w 做双层优化：w 在训练集上更新，alpha 在验证集上更新，最后再把连续图离散化。公开页面可核实的候选操作包括 3×3/5×5 separable convolution、3×3/5×5 dilated separable convolution、3×3 max pooling、3×3 average pooling、identity 和 zero，共 8 类；CIFAR-10 搜索设置包括 8 个 cell、50 个 epoch、batch size 64、初始通道 16、单张 GTX 1080Ti。DARTS 表格中 second-order 结果为 3.3M 参数和 2.76±0.09% test error，搜索成本为 4 GPU days；first-order 结果为 3.00±0.14%、1.5 GPU days。论文还特别说明 selection cost 为 1 GPU day，最终评估训练另计，因此不能把“搜索成本”误报成完整项目成本。

DARTS 的优点是梯度效率，缺点是连续松弛、离散化和权重共享可能改变真实候选的相对排名。一个在混合超网络中占优的操作，不一定在从头训练的最终离散网络中占优；不同随机种子、数据划分和训练预算也可能改变结果。因此若未来阙疑使用 DARTS 风格方法，架构搜索只允许产出候选实验配置，最终结论必须经过固定种子、独立复跑、真实工具链和 holdout 验证。

ENAS 的论文题为《Efficient Neural Architecture Search via Parameter Sharing》，作者为 Hieu Pham、Melody Y. Guan、Barret Zoph、Quoc V. Le、Jeff Dean，2018 年提交。它让 controller 在大计算图中搜索子图，child models 共享参数。论文摘要报告 PTB test perplexity 55.8、CIFAR-10 test error 2.89%，并将 CIFAR-10 结果与 NASNet 的 2.65% 做比较；论文 PDF 还报告标准 NAS 使用 450 GPUs、3–4 天，即 32,400–43,200 GPU hours，而 ENAS 搜索使用单张 NVIDIA GTX 1080Ti 且少于 16 小时，论文表述为成本约低 1000 倍。这里应保留“约”和实验边界：参数共享减少的是搜索阶段反复训练的成本，不是把最终模型验证、数据治理、复现和结果审计变成零成本。

ProxylessNAS 把搜索放到目标任务和目标硬件上。其移动端 ImageNet 实验允许 MBConv 的 kernel size 为 3×3、5×5、7×7，expansion ratio 为 3 或 6，并允许 zero operation 跳过 block。论文页面报告 Proxyless-R 达到 74.6% top-1、92.2% top-5、78ms mobile latency，搜索成本为 200 GPU hours；对照 MnasNet 约 40,000 GPU hours，页面报告成本少 200 倍。它还报告移动端 latency predictor 从 5,000 个采样架构中取 4,000 个训练、其余测试，RMSE 为 0.75ms。这个案例对嵌入式背景的作者有参考价值，但也恰好说明成本函数必须是目标设备的真实 latency；阙疑当前的瓶颈不是 C++ 验证内核在某块芯片上的毫秒数，而是数据和判决有效性。

### 四、搜索空间和阙疑任务的错配分析
| NAS 需要的条件 | 阙疑当前状态 | 结论 |
|---|---|---|
| 可搜索的神经网络空间 | 核心是规则、编译器/测试证据、四态判决、哈希链和对账器 | 没有必要为协议层造神经架构 |
| 可优化的连续或可排序目标 | holdout 30、真错 17，外部 corpus 40 且 43.8% 口径待修 | 先修指标，不能把小样本噪声当 NAS reward |
| 充分稳定的训练/验证/测试划分 | 外部 corpus 算术不自洽，反事实 P=R=F1=0 | 先建立 ground truth 和版本化 split |
| 可重复的硬件/软件执行环境 | 本机 sanitizer 运行时全部缺失，GCC/Clang 均有链接缺口 | 先修工具链，NAS 结果无法替代缺失证据 |
| 可接受的搜索成本 | 项目为单人、目标 NeurIPS 2027 E&D、当前工程仍有 227 项工作树漂移 | NAS 会扩大审计面与时间成本 |

阙疑若未来添加机器学习，最合理的切入点也不是 NAS 搜索最终判决器，而是低权限辅助模块，例如：对知识卡片进行人工复核优先级排序、从已有证据索引中召回候选、预测某类测试夹具的覆盖空白、在不改变最终四态的情况下提供“建议检查顺序”。即使如此，也应先用简单、可解释、可复跑的基线（规则、线性模型、浅层树、固定 embedding 检索）建立收益，再用固定小搜索空间做消融。只有当多个明确的候选模型在真实设备或真实流水线上存在稳定的延迟、内存或准确率权衡，NAS 才有工程理由出现。

### 五、对“值得使用”的判定
从研究价值看，NAS 可以作为背景章节或负面结果案例：它代表自动化设计的一个成熟方向，拥有 NAS-Bench-101、NAS-Bench-201 等可复现资源，也有 DARTS、ENAS、ProxylessNAS、Once-for-All 等降低成本的路线。从工程价值看，当前引入不值得。阙疑的论文卖点是“判决可复算 + 证据可追 + 盲态协议不可回盲”，NAS 的随机搜索、权重共享和代理估计反而会给证据链增加新的变量。Once-for-All 的论文说训练和搜索解耦后可得到超过 10^19 个子网络，并报告移动设置下 80.0% ImageNet top-1；这个数字说明搜索空间可以极大，却不能证明更大的空间能改善一套 C++ 知识判决协议。对阙疑最有价值的“自动发现”是发现漏测规则、反例和数据偏差，而不是发现一个无法解释的神经网络拓扑。

---

## 对阙疑的 3 条具体行动
1. **在 2026-10 前把“当前不引入 NAS”写成可审计决策。** 在 `C:/CodeLearnling/note/note/C++/CPP-Bible/_arch_v47/` 保留本方向文件，并在阙疑实际研究仓库的研究决策记录中新增 `NAS_DECISION` 条目，字段至少包括 `status=defer`、`reason=no_neural_architecture_target`、`blocking_metrics`、`review_date`、`owner`。决策正文明确：NAS 不得改变四态判决、不得绕过独立对账器、不得替代编译器/测试证据；复核条件为数据集口径修正、sanitizer 可执行、至少一个学习型辅助模块出现稳定的跨 split 收益。
2. **在 2027-03 前先完成一个非 NAS 的辅助基线，而不是先跑搜索。** 以阙疑现有知识卡和判决账本为输入，在实际项目的实验目录建立版本化字段 `card_id`、`claim_type`、`evidence_id`、`decision_state`、`review_priority`、`split_id`、`toolchain_version`，至少比较规则排序、线性模型或浅层树三类固定基线。每次运行保存输入清单、随机种子、编译器版本、训练/验证/holdout 划分、预测结果哈希和人工复核结果；辅助模型只能输出 `review_priority`，不得写入最终判决字段。若基线都不能稳定改善人工复核吞吐，就没有 NAS 的动机。
3. **只有满足门槛后才在 2027-05 做受限 NAS 可行性实验，并把失败也记录下来。** 门槛为：holdout 与 external corpus 的算术已独立复核；反事实指标不再为未解释的 `P=R=F1=0`；sanitizer 和 C++ 编译链可在干净环境运行；至少有 3 个固定随机种子、独立 holdout、端到端延迟/内存测量和可复算日志。届时只允许在 3–5 个已选模型族或极小的层数/宽度空间中做一次离线比较，优先随机搜索或表格基准，不允许直接把 DARTS/ENAS 的候选写进内核。若收益小于预先登记的工程阈值，或复现方差超过收益，结论应是“继续不引入 NAS”。

---

## 盲区（诚实标注）
- NASNet、DARTS、ENAS、ProxylessNAS 的关键数字已通过论文摘要、HTML 或 PDF 搜索结果核实，但不同论文对“search cost”的边界不完全一致：有的排除 selection cost，有的排除最终模型训练，有的使用 GPU hours，有的使用 GPU days；不能把这些数字直接当作同一硬件、同一价格下的横向成本。
- DARTS 页面同时出现约 1 天、1.5 GPU days、4 GPU days 等口径，分别对应不同实验或 first-order/second-order 与成本拆分；本文采用论文表格中 4 GPU days 的 second-order 搜索成本，并明确另列 1 GPU day selection cost，不把它们相加成未经页面直接给出的“总成本”。
- ENAS 的“1000x less expensive”是论文对标准 NAS 的相对表述，不是对所有 NAS 方法、所有数据集和所有硬件的普遍定律；本文能够核实“单张 GTX 1080Ti、搜索少于 16 小时”和论文给出的标准 NAS 450 GPUs、3–4 天，但没有把它外推成当前 GPU 价格或碳排放数字。
- ProxylessNAS 的 latency 结果依赖特定模型、batch size、设备和测量框架；Pixel 1、Tesla V100、Xeon E5-2640 v4 的结果不能直接代表阙疑的本机 C++ 工具链。论文中的 latency predictor RMSE 0.75ms 也只是其采样和设备条件下的结果。
- NAS-Bench-101 的约 423,000 架构、超过 100 TPU years 和 NAS-Bench-201 的 15,625 候选来自固定图像分类基准，不能说明 C++ 知识卡的搜索空间应如何编码，也不能作为阙疑性能的先验。
- 本文没有核实所有 NAS 后续方法在 2026 年的最新排行榜、价格、碳排放或最优算法，也没有宣称 DARTS、ENAS、ProxylessNAS 在各自论文之外仍保持相同的最佳性；这些内容不影响“阙疑当前不需要引入”的工程判断。
- 阙疑当前的 37 实卡、10 草稿、67 规则、9 保护器、452 账本、3826 行内核、holdout 30、外部 corpus 40、66.7% 与 43.8% 等数字取自共享上下文，而不是本次独立重跑；其中外部 corpus 的算术不自洽和 sanitizer 缺失应优先修复，不能用 NAS 实验掩盖。
- “未来可以用 NAS 做低权限辅助模块”是条件性建议而非实验结论。若没有明确的收益阈值、独立 holdout、审计日志和人工复核协议，这个建议应保持为 deferred，而不是变成新增依赖。

---

## 来源
1. Thomas Elsken、Jan Hendrik Metzen、Frank Hutter，《Neural Architecture Search: A Survey》— https://arxiv.org/abs/1808.05377 — 将 NAS 按 search space、search strategy、performance estimation strategy 三维分类；2018/2019。
2. Barret Zoph、Quoc V. Le，《Neural Architecture Search with Reinforcement Learning》— https://arxiv.org/abs/1611.01578 — CIFAR-10 test error 3.65、PTB perplexity 62.4、RNN controller 与强化学习搜索；Google Brain；2016/2017。
3. Barret Zoph、Vijay Vasudevan、Jonathon Shlens、Quoc V. Le，《Learning Transferable Architectures for Scalable Image Recognition》— https://arxiv.org/abs/1707.07012 — NASNet 的 cell 迁移；CIFAR-10 2.4% error、ImageNet 82.7% top-1、96.2% top-5、少 9 billion FLOPS、计算需求下降 28%；Google；2017/2018。
4. Hieu Pham、Melody Y. Guan、Barret Zoph、Quoc V. Le、Jeff Dean，《Efficient Neural Architecture Search via Parameter Sharing》— https://arxiv.org/abs/1802.03268 — ENAS 参数共享、PTB 55.8、CIFAR-10 2.89%、约 1000 倍成本降低；Google/CMU/Stanford；2018。
5. Hieu Pham 等，《Efficient Neural Architecture Search via Parameter Sharing》PDF— https://arxiv.org/pdf/1802.03268.pdf — 标准 NAS 使用 450 GPUs、3–4 天，即 32,400–43,200 GPU hours；ENAS 单张 GTX 1080Ti、搜索少于 16 小时；2018。
6. Han Cai、Chuang Gan、Tianzhe Wang、Zhekai Zhang、Song Han，《Once-for-All: Train One Network and Specialize it for Efficient Deployment》— https://arxiv.org/abs/1908.09791 — 训练与搜索解耦、超过 10^19 个子网络、移动设置 80.0% ImageNet top-1、相对 MobileNetV3 的准确率/延迟比较；MIT；2019/2020。
7. Hanxiao Liu、Karen Simonyan、Yiming Yang，《DARTS: Differentiable Architecture Search》— https://ar5iv.labs.arxiv.org/html/1806.09055 — 连续架构参数、双层优化、3.3M 参数、2.76±0.09% CIFAR-10 error、second-order 4 GPU days 与成本拆分；2018/2019。
8. Hanxiao Liu、Karen Simonyan、Yiming Yang，《DARTS: Differentiable Architecture Search》OpenReview— https://openreview.net/forum?id=S1eYHoC5FX — 论文版本与“few GPU days”的架构发现成本表述；2018。
9. Han Cai、Chuang Gan 等，《Once-for-All》代码与模型仓库— https://github.com/mit-han-lab/once-for-all — 论文实现、代码和 50 个预训练模型的发布入口；MIT Han Lab；2020。
10. Han Cai、Han 等，《ProxylessNAS: Direct Neural Architecture Search on Target Task and Hardware》— https://arxiv.org/html/1812.00332v2 — 目标硬件 latency、200 GPU hours、约 40,000 GPU hours 的 MnasNet 对照、74.6%/78ms 移动端结果、latency predictor 0.75ms RMSE；MIT/Google 等；2018/2019。
11. Han Cai 等，《ProxylessNAS》代码仓库— https://github.com/mit-han-lab/proxylessnas — 目标任务与硬件直接搜索的实现入口和实验说明；MIT Han Lab；2019。
12. Chris Ying、Aaron Klein、Esteban Real、Eric Christiansen、Kevin Murphy、Frank Hutter、等，《NAS-Bench-101: Towards Reproducible Neural Architecture Search》— https://ar5iv.labs.arxiv.org/html/1902.09635 — 约 423,000 架构、固定图搜索空间、3 次重复、4/12/36/108 epochs、超过 100 TPU years；Google Research；2019。
13. Google Research，NAS-Bench-101 数据集与代码— https://github.com/google-research/nasbench — 423,624 个唯一网络、固定图搜索空间和可查询 benchmark 实现；Google Research；2019。
14. Xuanyi Dong、Yi Yang，《NAS-Bench-201: Extending the Scope of Reproducible Neural Architecture Search》— https://arxiv.org/abs/2001.00326 — 4 节点、5 个操作、15,625 候选、3 个数据集训练日志、10 种 NAS 算法基准；ICLR 2020 spotlight；2020。
15. D-X-Y，NAS-Bench-201 API 与代码— https://github.com/D-X-Y/NAS-Bench-201 — 固定搜索空间、架构查询 API 与复现实验入口；2020。
