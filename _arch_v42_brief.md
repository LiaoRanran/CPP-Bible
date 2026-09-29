# v42 大调研：从系统到论文——投稿/复现/写作/冷启动

> 执行：trae 外部模型
> 产出：_arch_v42/ 共 12 文件（00总览 + 10方向 + 99来源清单）
> 参考格式：_arch_v39/ 或 _arch_v41/

## 项目现状（锚点）
- 阙疑（QueYi）：C++知识验证系统
- 48卡（26 verified）/ 67规则 / 9保护器 / 452账本
- 四态判决 + append-only哈希链 + Merkle checkpoint
- 盲holdout 20样本（真错7个），检出率80%
- 外部corpus 20条，检出率33%
- 真实缺陷夹具15条，重注入检出100%
- Research Protocol v0.1（RQ1-RQ4）
- 目标：NeurIPS 2027 E&D track
- 论文framing：Evolution of Verification Capability under Evaluation-Integrity Constraints

## 10个调研方向

### 01 NeurIPS E&D 投稿经验与审稿标准
- 2024-2026近三年E&D track录用论文分析
- 审稿标准：Quality/Clarity/Significance/Originality具体怎么打分
- E&D track喜欢什么类型的工作（negative results? critical analysis?）
- 被拒论文的常见原因

### 02 独立复现/第三方审计
- SWE-bench Verified→Pro的教训（数据污染）
- 独立复现者怎么找、怎么签
- 复现kit最小要素
- 单人项目怎么做replication study

### 03 单人研究者找合作者
- 双非本科生，0影响力，怎么找导师/合作者
- 冷邮件模板
- Hugging Face Community Evals的机会
- 什么时候该找合作者，什么时候自己扛

### 04 论文常见拒稿理由
- 审稿人视角：最常见的reject理由
- 单人/本科生论文怎么避免被秒拒
- 过度claim的具体表现
- "没有baseline"到底要几个

### 05 Ablation study 怎么做才不水
- 最小ablation集（Full vs -X vs random-budget）
- 每个ablation要回答什么问题
- 样本量多大才够
- 单人项目怎么跑ablation不烧钱

### 06 Threats to Validity 怎么写
- 五层写法（Construct/Internal/External/Statistical/Temporal）
- 审稿人接受什么样的threats
- 怎么写不被攻击"你自己都知道有问题还投"
- 真实案例：好的threats section长什么样

### 07 开源项目冷启动
- GitHub repo→第一批用户路径
- Show HN/Release Notes怎么写
- 单人项目怎么攒star
- 什么时候该做博客/演讲

### 08 AI辅助研究伦理与披露
- NeurIPS 2026 authorship policy最新
- LLM/Agent使用怎么披露
- 什么程度的AI使用需要写在方法里
- AI不能列为作者的边界

### 09 C++标准/编译器差异权威错误源
- 做外部corpus用：哪些网站/书籍有最权威的C++错误案例
- cppreference/StackOverflow/Standard Drafts
- 跨编译器差异的权威列表
- 真实compiler bug历史（GCC/Clang/MSVC）

### 10 从系统到论文：转化方法
- 怎么把一个工程系统压缩成一个科学问题
- 论文图（figure 1）怎么设计
- 贡献声明三段式模板
- 从"我做了个系统"到"我解决了一个问题"

## 要求
- 每方向一个文件，具体可执行，不要空话
- 关键数据要有来源
- 诚实标注盲区
- 零污染：只写 _arch_v42/
