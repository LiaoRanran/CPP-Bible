# 549 · 质变调研：把"工程直觉"升级成"有数学保证的放权系统"（2025-2026 前沿对照）

> 本轮向外调研只盯当前系统五个硬瓶颈，每个都找到 2025-2026 的真实前沿答案，并标注**现在就能做（不依赖模型变强）**还是**等 EIR 门开**。核心结论：系统离"质变"差的不是更多功能，是两件能立刻装的数学/工程锁芯——**共形放权门**和 **RIPR 诚实分类**。
> 检索日期 2026-09-16。链接均为真实来源。

## 〇、一句话总览
我们现在的"什么时候敢让 LLM 进闸 / 拦截率多少算安全"是**拍的阈值**；业界已经有现成的、distribution-free 的统计框架（共形预测 / 选择性预测）能把它变成**有数学上界保证的门**，而 mutation 已经在攒的逃逸数据就是天然校准集。同时，548 那 66 条"无效变异"在突变测试学术界早有名字和判据（RIPR 的 Reachability 失败）。这两件不依赖更强模型，装完系统性质就变了。

## 一、质变地图

| # | 当前瓶颈 | 业界答案 | 现在/等模型 | 性质 |
|---|---|---|---|---|
| Q1 | 放权门 EIR≤5% 是拍的 | 共形预测 / 选择性预测 / Conformal Risk Control | **现在**（纯统计，零 LLM） | 数学保证 |
| Q2 | 逃逸数混"无效提问"（66 条） | 突变测试 RIPR 四层 + equivalent mutant | **现在**（分类法+小工程） | 度量诚实 |
| Q3 | V-iso 阴面要手写、弱卡批量卡壳 | 蜕变测试 Metamorphic Relations + LLMorph 自动 follow-up | 机械模板现在做，LLM 生成等门 | 半自动化 |
| Q4 | 概念图 157 节点跨原子连通 0（标签袋） | HyDRA competency-questions-first + 窄域 grounding 指标 | **现在**（改 KPI 和建图顺序） | 架构纪律 |
| Q5 | mutation 固定 7 算子、不会自己变强 | GPT-Red self-play / FuzzingBrain / 自适应 fuzz 能量调度 | 机械协同进化现在做，LLM 攻击等门 | 进化闭环 |
| Q6 | 异族制衡是否站得住 | Weak-to-Strong / CriticGPT / Embedded Evaluators；debate 会被 reward hacking 骗 | 已验证，固化纪律 | 方法论背书 |

---

## 二、逐个详述

### Q1 · 共形预测：给放权门装数学锁芯（最高优先，质变）
**来源**：
- UniCR, arXiv 2509.01455（2026）：把序列似然/自一致性离散度/检索兼容性/**工具-验证器反馈**融合成校准正确概率，再用 conformal risk control **强制执行用户指定的错误预算**，distribution-free 保证，支持 API-only 黑盒模型。
- SAFER, OpenReview 2026：held-out 校准集上用 **Clopper-Pearson 精确法**校准，达不到风险水平就弃权（abstain）。
- arXiv 2606.16667：false-certification probability ≤ δ 的精确保证（3000 个存在性 claim，Clopper-Pearson，违约频率 0.00）。
- 综述 khuong.uk/.../Uncertainty_aware_LLM：conformal selective prediction = 不确定就 defer 给另一个模型/人。

**对我们的意义**：我们定的门"EIR 95% 置信上界 ≤5% 才让该类 claim 走自动通道"——**Clopper-Pearson 正是"95% 置信上界"的精确算法**。mutation 每类 claim 跑 N 个变异、逃逸 k 个，逃逸率上界 = Beta 分位数 `Beta^{-1}(0.95; k+1, N-k)`。这是纯机械计算，零 LLM，且对任何底层模型分布都成立（distribution-free）。
**最小落地（现在做）**：
1. `tools/conformal_gate.py`：输入某类 claim 的 (N 变异, k 逃逸)，输出逃逸率点估计 + 95% Clopper-Pearson 上界；上界 ≤α（默认 0.05）才标 `auto_eligible`，否则 `defer_human`。
2. 接 mutation_fuzz 报告：每算子/每卡类出一张"放权资格表"，随全量基线刷新。
3. 机器验收：注入已知 k/N，断言上界数值（与 statsmodels/scipy 对照）；N 太小（如 <30）强制 defer（上界必然宽）；k=0 时上界也不为 0（=1-0.05^(1/N)，杜绝"零逃逸=零风险"幻觉）。
**边界**：CP 保证的是 exchangeability（校准集与未来同分布）；领域漂移时保证失效——配 2510.22931 的自适应弃权（漂移检测→收紧/弃权）。这恰好给"换领域插件"提供了量化的重新校准触发点。

### Q2 · RIPR 四层：让逃逸率第一次诚实（高优先，直接修 548 的 66 条）
**来源**：突变测试 RIP/RIPR 模型（Lipton 1971 起；Wiley STVR 1865；ICSE 2024 Ripples of a Mutation）。一个 mutant 被检测到必须依次穿过四层：
1. **Reachability**：测试执行/读取到变异点；
2. **Infection**：变异真的改变了状态/数据；
3. **Propagation**：差异传播到可观察边界（gate 的 Finding / replay 输出）；
4. **Reveal**：断言正确地把差异判成失败。
另有 **equivalent mutant**：语法不同但语义等价、任何输入都杀不死（应排除出分母）。

**对我们的意义**：548 的 66 条"M2 取全文第一个路径、落在注释/正文、门禁从不读"= **Reachability 失败**，结构上不可能被 kill，现在却混在 escaped 里拉低/扭曲拦截率。这与 547 D2（n_a 藏身、判决诚实性）是同一个病。
**最小落地（现在做）**：
- mutation 判决从三分类扩成"先过 R 闸"：变异点必须落在**门禁实际解析的字段/区间**内（用 gate 的字段读取清单反查），否则标 `unreachable`，**不进拦截率分母**（与 malformed 并列单列）。
- 每条 escaped 标注死在哪层（R/I/P/R），报告给"该补哪层"：R 失败=算子没打在真位置；I/P 失败=变异太弱；R 失败=断言缺口（真洞）。
- 机器验收：548 那 66 条重判为 unreachable；真逃逸分母变小后重算拦截率（会更可信，不一定更好看）。

### Q3 · 蜕变测试：V-iso 阴面的学术正名与自动化路径
**来源**：
- 综述 arXiv 2605.13898（2026）：MT 不问"输出对吗"，问"相关输入的输出是否满足必要性质（Metamorphic Relation, MR）"——**这就是阴阳同构**：阳/阴 = source/follow-up，"断言在阴面必须翻转" = MR。
- LLMorph arXiv 2603.23611：自动从 source 生成 follow-up、检测 MR 违背，无需人工标注；MORTAR 2412.15557 自动 MR 匹配；Meta ACH（2025）mutation-guided + LLM 生成测试。
**最小落地**：
- 现在（机械）：建 MR 模式库给阴面分类套模板——`删除因果行→相关断言必须翻转`、`等价重排→断言不应翻转`、`替换为无关实现→应翻转`。把"手写阴面"从艺术变成按 claim 类型选 MR。
- 等门（LLM）：用 LLM 按 MR 自动生成 follow-up 阴面候选，但**采纳仍走 iso_judge 机械判据 + 翻转实测**（LLM 只提候选，不裁决——守住 Q6 纪律）。

### Q4 · 概念图：从"数三元组"改成"competency questions 先于建图"
**来源**：
- HyDRA arXiv 2507.15917：**先让一组 agent 共识出 competency questions（本体必须能回答的问题），再据 CQ 建图**。
- dataaihub KG+LLM 指南（2026）："entity linking 是 grounding 成败关键；**从窄域图 + 可测量 grounding 指标开始——没有质量门的宽图放大错误而非减少错误**"。
- KARMA arXiv 2502.06472：9 agent 含 schema alignment + conflict resolution。
**对我们的意义**：529 实测"概念 157、跨原子连通 0"= 标签袋。三元组数量是**负 KPI**，连通率/CQ 可回答率才是正 KPI。
**最小落地（现在做）**：先写 10-20 条概念图必须回答的 CQ（如"哪些原子共同支撑内存屏障主题、证据是否互通"），连边只为回答 CQ；报"跨原子连通组件数 / CQ 可回答率"，连通不了的概念不计入概念层规模。窄域（先 C++ 内存主题），不铺宽图。

### Q5 · 协同进化：现在做机械版，self-play RL 等门开
**来源**：
- OpenAI GPT-Red（2026-07）：self-play RL，攻击者与多防御者同时训练、协同进化，prompt injection 上 84% vs 人类红队 13%，发现 Fake-CoT 新攻击。
- FuzzingBrain V2（2026-05）：多 agent + fuzz 验证，AIxCC 2025 检测率 90%、41 个真实 0-day。
- AGENTXPLOIT arXiv 2505.05849：MCTS 种子选择迭代 refine。
**对我们的意义 + 纪律**：终局是攻击器/防御器协同进化，但 LLM 攻击者须等 Q1 门开。**现在能做无 LLM 的机械协同进化**：给 mutation 算子加自适应能量调度（AFL 式 bandit：哪类算子近期逃逸多就多分配变异预算，gate 补上后该类逃逸下降、能量自动转移）——这会让"7 个固定算子"变成"会自己追着薄弱面打的算子集"，是 L4 进化层的机械雏形。

### Q6 · 异族制衡：最新证据既背书也警告
**来源**：
- Weak-to-Strong Generalization（Burns 2023，2025 综述 2510.11235）：弱监督者标注、强模型微调，强模型可超过弱监督者本身——**实证支持"弱模型/小白监督强建设者"可行**。
- CriticGPT（2024）：LLM 批评 LLM、augment 人类。
- Anthropic **Embedded Evaluators（2026-09，本周）**：给独立第三方长期员工级访问、不受编辑控制地发布发现——**这正是我们"异族独立对抗、零污染、只交付 _adv 目录"的组织形态**。
- **关键警告（CMU 15780 讲义引 Anthropic 2025：reward hacking 在生产 RL 中自然涌现 misalignment；scalable oversight 的失败模式 = judge 被"有说服力的错误答案"欺骗）**。
**结论（固化现有纪律）**：辩论/批评能**发现**问题、不能**裁决**——异族只负责打穿和报告，终审必须 grounded（编译器/统计门/人签）。我们"禁止 LLM-as-judge 终审、异族不碰正式文件"的纪律被 2025-2026 最新证据再次证明是对的。

---

## 三、明确不做（防止被前沿带偏）
- 不做 LLM-as-judge 终审、不做同质模型辩论当裁判（Q6 已证会被 reward hacking 骗）。
- 不追求概念图三元组数量（负 KPI）；不铺宽域 KG。
- 不让 LLM 在线改 gate 权重 / 自动入库（EIR 门未开前）。
- 共形上界不允许在 k=0 时报 0（零逃逸≠零风险）。

## 四、推荐批次序列
- **批次 J（立刻，纯机械、最高杠杆）**：Q1 conformal_gate + Q2 RIPR reachability 闸。两者都零 LLM、可立即给苦力，且互相咬合（RIPR 先让逃逸数诚实，CP 再在诚实分母上算放权上界）。
- **批次 K**：Q4 概念图 CQ-first 改造（窄域）+ Q3 机械 MR 模式库。
- **批次 L（攒数据/机械进化）**：Q5 自适应能量调度；持续跑全量 mutation 喂 CP 校准集。
- **等模型档（门开后）**：LLM 生成阴面 follow-up、LLM 攻击者（GPT-Red 形态）、跨域自动重新校准。

## 五、给监工的一句话
**Q1+Q2 是这轮真正的质变**：装完之后，系统第一次能对每一类知识说出一句有数学保证的话——"这一类，机器放权后的错误率 95% 置信上界是 X%，低于 5%，可以自动；那一类上界 12%，必须人审"。这正是"随模型变强而连续放权"一直缺的那个**可计算的刻度盘**，而且不依赖任何模型升级。
