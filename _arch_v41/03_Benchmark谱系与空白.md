# _arch_v41 · 03 现有 benchmark 测了什么、漏了什么（方向 3）

> 核心问题：主流代码/事实性基准各自测什么，污染问题，"教材级 C++ 知识断言"为何无人覆盖，阙疑 47 卡/452 账本在基准谱系中的位置。
> 诚实标注：【论文·实证】；【官方】；【推断】；【盲区】。

---

## 一、主流代码基准：全部测"写代码"，无一测"知识断言"

| 基准 | 测什么 | 口径与状态 |
|---|---|---|
| HumanEval / MBPP | 函数级代码生成，单测通过率 | 2023 年已饱和（>95%）；LCB 实证存在过拟合【论文·实证，S25】 |
| HumanEval+/MBPP+ | 对抗性扩充测试用例 | 重开区分度，但仍是代码题 |
| LiveCodeBench | 竞赛题持续收集 + 日期窗口防污染；另测自修/执行/测试输出预测 | ICLR 2025；时间窗机制成新可信度地板【论文·实证，S25】 |
| SWE-bench / Verified | 仓库级 issue→PR | Verified 500 题，已成事实标准但污染严重（见下） |
| SWE-bench Pro | 长程仓库任务，GPL/私有代码防污染 | 顶模 ~23% vs Verified 70%+【官方，S24】 |

**关键口径差**：这些基准的问题单元是"一段可执行代码 + 隐藏测试"，判决是"测试通过/失败"。**没有任何一个的单元是"一句可验证的知识断言"**。【推断】

## 二、污染：老基准的系统性失效

- **SWE-bench Verified 泄漏率约 10.6%**（对 StarCoder 的实测）【论文·实证，S23 引 Zhou】。
- 2025/12 最新实验：Claude 模型在 Verified 上表现比 BeetleBox/SWE-rebench 好 3 倍，**仅靠 issue 文本定位被修改文件的能力好 6 倍**——该定位在逻辑上近乎不可能，差异只能用训练记忆解释【论文·实证，S23】。
- OpenAI 已于 2025-09 公开宣布不再以 SWE-bench Verified 为评估口径，行业转向 Pro【第三方汇编，codesota；S24 同源印证】。
- LCB 时间窗证据：DeepSeek 在其发布日后的 LeetCode 题上成绩骤降，早期分数有污染成分【论文·实证，S25】。

## 三、事实性基准：最接近但仍是"通用域 + 文档对拍"

- **FactBench / VERIFY**：真实用户 prompt，按 Web 证据把内容单元判为 **supported / unsupported / undecidable**——三态口径与阙疑"unknown"哲学同源；但域是开放百科，无 C++、无真机层【论文·实证，S26】。
- **SimpleQA Verified（Google DeepMind，1000 题）**：测参数化知识，SOTA F1 仅 55.6——前沿模型事实性远未解决；但形式为短问答、通用域【论文·实证，S27】。
- **LLM-AggreFact（MiniCheck，11 数据集统一）**：文档对拍的 grounded 判定，通用域。[v41-S19]
- **教材域仅有课程对齐尝试**：Pustak AI（NCERT-QA）证明模型脱离教材上下文后 F1 崩塌——**课程特定长尾知识不在参数记忆里**【论文·实证，S28】；但它测的是 K-12 问答，不验证断言。
- 编程教材 RAG 的实测：非 RAG 对教材来源的中位 adherence 为 0%，RAG 也仅 22–40%【论文·实证，S29】。

## 四、硬映射

### 1. 阙疑在基准谱系中的位置（二维定位）【推断】

- 现有格：（代码，执行测试）×（函数/仓库）= 代码基准；（事实断言，文档/Web 对拍）×（通用域）= 事实基准。
- **空格**：（原子化 C++ 知识断言，可执行真机证据 + 独立验证 + 账本留痕）×（教材/教学域）。FactBench 有断言单元但无真机无 C++；AggreFact 有 grounded 判定但域通用；SWE 系有真机但是代码不是断言。
- 阙疑 47 卡 = 该空格的**首批实例化语料**；452 账本 = 该格独有的"判决历史层"——所有主流基准都只有静态题目，无判决演化账本。

### 2. "现有 benchmark 为何不覆盖教材级断言"——三因【推断】

1. 自动评分难：代码题有测试二进制信号，断言对拍需权威证据库，成本极高；
2. 教材域被视为"小众长尾"，工业激励不足；
3. 基准多从训练/能力视角构建（测模型），无人从审计视角构建（测具体产物）。

### 3. v39"独占空白格"结论还成立吗？

**仍成立，但要诚实限定**【推断】：
- 成立：2025-2026 新基准（Pro/FactBench/SimpleQA Verified）均未进入该格；
- 但"独占"是**时点性**的：MiniCheck 式合成数据方法可低成本复制到任何域，一旦有人做 C++ 域核查器（如 FISCAL 之于金融[S21]），格就被共享。阙疑的先发卡位窗口有限，护城河必须押在账本/provenance/治理，而非"第一批卡"。

## 五、直说：风险与短板

- 47 卡 / 每卡 10-11 变异的规模，在基准世界里属"微基准"，**不能自称 benchmark**，宜定位为"审计语料 + 案例研究"，避免被学界按基准标准（样本量、统计功效）一击即碎。【推断】
- 阙疑无日期窗口/防污染机制设计（被测对象是外部 LLM 的具体输出，污染形态不同，但需登记模型版本与 prompt 快照——未见专项【盲区】）。

## 六、来源

[v41-S23] Prathifkumar et al., Does SWE-Bench-Verified Test Agent Ability or Model Memory?, arXiv:2512.10218；[v41-S24] Scale AI, SWE-Bench Pro（官方数据集页；论文 arXiv:2509.16941）；[v41-S25] Jain et al., LiveCodeBench, ICLR 2025 (arXiv:2403.07974)；[v41-S26] Fatahi Bayat et al., FactBench/VERIFY, arXiv:2410.22257；[v41-S27] Haas et al., SimpleQA Verified, arXiv:2509.07968；[v41-S28] Sharma et al., Pustak AI, arXiv:2511.10002；[v41-S29] Sovrano & Bacchelli, Source-Faithful RAG Explanations, arXiv:2604.06211；跨指 [v41-S19] MiniCheck/AggreFact、[v41-S21] FISCAL。

**盲区**：阙疑自身有无 prompt/模型版本快照机制未核实；各基准 C++ 子集的具体占比（LCB 支持 C++ 但默认评测口径以 Python 为主）。
