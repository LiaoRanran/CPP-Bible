# v28 超大发散调研：八方向 × 15 检索 × 概念重构

> v21-v27 已经覆盖了 AI 安全、跨域类比、数学哲学脑科学、行业实践、智能本质。这轮换**八个全新方向**，每个方向 15+ 次检索，总共 120+ 次。
>
> 目标不是找具体工程方案，是**对阙疑做一次全面的概念重构**——看看有没有哪个方向的概念框架能从根本上改变我们看这个系统的方式。
>
> 这是目前为止最大规模的一次发散调研。

## §零 约束

1. **8 个方向，每个 ≥15 次检索**，总共 ≥120 次
2. 每个方向写一个文件
3. 每个方向必须有：核心概念清单（带人名/年份）+ 对阙疑的【发散联想】+ 反直觉发现 + 死路确认 + 对自我进化的含义
4. 不写工程实现方案
5. 零污染：只在 _arch_v28/ 目录下写文件
6. 所有类比标【类比推断】
7. 重磅二手事实标【一方称】

## §一 八个方向

### 方向 A：复杂系统与涌现（≥15 检索）

核心问题：**简单规则怎么产生复杂秩序？系统怎么自发进化？**

要搜的东西：
- 元胞自动机（Conway's Game of Life、Langton's Ant、Wolfram 的 A New Kind of Science）
- 涌现（emergence）——弱涌现 vs 强涌现 vs 因果涌现
- 自组织临界性（SOC，Bak 的沙堆模型）
- 复杂适应系统（CAS，Holland）
- 混沌边缘（edge of chaos，Langton 参数）
- 正反馈 vs 负反馈回路
- 系统韧性（resilience）——Panarchy 模型
- 鲁棒性 vs 脆弱性（Taleb 的 via negativa、Antifragile）
- 网络科学（scale-free networks、小世界）
- 突变论（catastrophe theory）

### 方向 B：经济学与博弈论（≥15 检索）

核心问题：**激励怎么设计？多主体怎么合作？怎么防止搭便车？**

要搜的东西：
- 机制设计（mechanism design）——Hurwicz、Maskin、Myerson
- 公地悲剧（Hardin）——怎么解决
- 声誉系统（eBay、Stack Overflow、Uber）
- 重复博弈——Axelrod 锦标赛
- 信息不对称（Akerlof 柠檬市场、Stiglitz）
- 信号理论（Spence 劳动力市场）
- 激励相容（incentive compatibility）
- 搭便车问题
- 拍卖理论（Vickrey）
- 契约理论（Hart、Holmström）
- 行为经济学（Thaler、Kahneman）对机制设计的影响
- 公共物品博弈实验

### 方向 C：教育学与学习科学（≥15 检索）

核心问题：**人是怎么真正学会东西的？什么教学方法最有效？**

要搜的东西：
- 主动学习 vs 被动听课（Freeman 2014 meta-analysis）
- 间隔重复（Ebbinghaus、SuperMemo、Anki）
- 测试效应（Roediger & Karpicke）
- 迁移学习（transfer of learning）
- 认知负荷理论（Sweller）
- 刻意练习（Ericsson、Charness）
- 元认知（Flavell、Dunlosky）
- 错中学（Bourne、Kaplan）
- 生长型思维（Dweck）
- 直接教学 vs 探究式学习的争论
- 认知学徒制（Collins、Brown、Newman）
- 自我调节学习（Zimmerman）
- 生成效应（generation effect）

### 方向 D：知识社会学与科学学（≥15 检索）

核心问题：**知识是怎么在人类社群里累积的？科学是怎么进步的？**

要搜的东西：
- 科学社会学（Kuhn、Feyerabend、Merton 规范）
- 同行评议的实际运作（不是理想状态）
- 共识怎么形成、怎么打破
- 知识的累积性 vs 革命性（波普尔 vs 库恩 vs 拉卡托斯）
- 科学范式的生命周期
- 重复危机（Open Science Collaboration 2015）
- 预注册（preregistration）的兴起
- 开放科学运动
- 知识生产的基础设施（期刊、会议、数据库）
- 马太效应（Merton）
- 科学的不端行为（Stroebe、Stapel 案例）
- 同行评议的偏差（性别、国籍、声誉）
- 科学计量学（citation networks、H-index）
- 后常规科学（post-normal science）

### 方向 E：生态学与生物多样性（≥15 检索）

核心问题：**生态系统怎么自我调节？多样性为什么重要？**

要搜的东西：
- 生态系统稳定性（Odum）
- 生物多样性 vs 生态系统功能（Tilman）
- 营养级联（trophic cascade）
- 生态位（niche）与竞争排除
- 演替（succession）——原生演替 vs 次生演替
- 关键种（keystone species）
- 入侵物种
- 生态恢复（restoration ecology）
- 共生（symbiosis）——互利共生、寄生、偏利
- 协同进化（coevolution）
- 食物网的鲁棒性
- 冗余 vs 退化（Walker 1999）

### 方向 F：演化生物学与认知演化（≥15 检索）

核心问题：**认知能力是怎么演化出来的？为什么会演化出智能？**

要搜的东西：
- 认知演化（evolution of cognition）
- 社会脑假说（Dunbar）
- 生态智力假说（Byrne & Whiten）
- 马基雅维利智力假说
- 累积文化演化（cumulative culture）
- 文化群体选择（Boyd & Richerson）
- 模因论（Dawkins、Blackmore）
- 生命史理论（life history theory）
- 性选择与认知
- 脑容量演化的代价与收益
- 动物认知（鸦科、章鱼、海豚、灵长类）
- 演化失配（evolutionary mismatch）

### 方向 G：信息论与热力学（≥15 检索）

核心问题：**信息是什么？知识的物理极限在哪？**

要搜的东西：
- Shannon 信息论
- Kolmogorov 复杂度
- 算法信息论（Chaitin、Solomonoff）
- 热力学第二定律与信息（Maxwell's Demon、Szilard）
- Landauer 原理（擦除信息的能量代价）
- 贝叶斯推理与归纳问题
- 所罗门诺夫归纳（Solomonoff induction）
- 奥卡姆剃刀的形式化
- 数据压缩与泛化
- 互信息与特征选择
- 率失真理论
- 费舍尔信息
- 信息几何

### 方向 H：军事学与攻防理论（≥15 检索）

核心问题：**攻防是怎么演化的？怎么建立不可攻破的防线？**

要搜的东西：
- 军事学说（孙子、克劳塞维茨、李德·哈特）
- 攻防平衡（offense-defense balance）
- 军备竞赛
- 纵深防御（defense in depth）
- 安全边际（margin of safety）
- 红队/蓝队训练方法
- 欺骗与反欺骗
- 密码学历史（从凯撒到公钥）
- 网络安全攻防
- 堡垒化（fortification）的历史
- 情报分析（intelligence analysis）
- 战争迷雾（fog of war）
- OODA 循环（Boyd）
- 不对称战争

## §二 交付文件

全部放在 `_arch_v28/` 目录：

1. `00_综合.md` — 八方向总表 + 交叉对比 + 对阙疑的整体启示 + 有没有哪个方向能从根本上重构我们的思路
2. `01_复杂系统.md` — 方向 A
3. `02_经济学.md` — 方向 B
4. `03_教育学.md` — 方向 C
5. `04_知识社会学.md` — 方向 D
6. `05_生态学.md` — 方向 E
7. `06_认知演化.md` — 方向 F
8. `07_信息论热力学.md` — 方向 G
9. `08_攻防理论.md` — 方向 H
10. `zero_pollution.md` — 零污染自证

## §三 每个文件的结构

```markdown
# 方向名

## 核心概念清单
（6-10 个核心概念，每个带人名/年份/一句话解释）

## 反直觉发现
（4-6 个你没想到的结论）

## 对阙疑的发散联想
（8-10 个【类比推断】，每个说清楚：对方是什么 → 阙疑对应什么 → 启发是什么）

## 死路确认
（3-5 个这个方向里看起来有用但实际是死路的）

## 对自我进化系统的含义
（这个方向对"系统自己进化"有什么启发）

## 最值得搬的一个概念
（如果只能搬一个概念过来，搬哪个？为什么？）
```

## §四 综合文件要求

`00_综合.md` 必须有：
1. 八方向总表（方向 × 核心概念 × 对阙疑启发 × 死路）
2. **交叉发现**：哪几个方向独立指向同一个结论？
3. **概念重构**：有没有哪个方向的概念框架能从根本上改变阙疑的设计？
4. **v21-v27 对比**：这轮新发现和之前七轮有什么不同？
5. **Top 5 靶位**：最值得深入的 5 个方向
6. **对阶段 3+ 的建议**：这些发现怎么落地到工程上

## §五 零污染

- 开工前 git status --short 存基线
- 收工后 git status --short 对比
- 唯一差异应该是 `?? _arch_v28/`
- 写 `zero_pollution.md` 记录
