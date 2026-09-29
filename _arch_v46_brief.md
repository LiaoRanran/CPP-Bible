# 第零步：扫描仓库现状（只读，不要改任何文件）

先做这一步，不要跳过。这一步是为了让后面的调研有精确锚点，不要用旧数字。

## 扫描清单（全部只读）

1. git log --oneline -20 —— 最近20个提交
2. git status —— 当前工作树状态
3. ls atoms/ —— 卡总数（实际数，不要用旧的48/83）
4. ls tools/ —— 工具总数
5. cat tools/gate_engine.py | wc -l —— 内核行数
6. cat data/holdout/holdout.json | python -c "import json,sys; d=json.load(sys.stdin); print(len(d))" —— holdout样本数
7. cat data/external_corpus_665.json | python -c "import json,sys; d=json.load(sys.stdin); print(len(d))" —— 外部corpus数
8. cat data/defect_fixtures/defects.json | python -c "import json,sys; d=json.load(sys.stdin); print(len(d))" —— 缺陷夹具数
9. ls research/ —— Protocol文件列表
10. cat research/paper_v0.3.md | head -50 —— 论文当前状态
11. ls _arch_v*/ -d —— 历史调研轮次
12. ls web/ —— 前端文件列表

## 输出

把以上扫描结果写进 _arch_v46/00_仓库扫描.md，作为后面100个方向的精确锚点。

然后再开始100个方向的调研。

---
# v46 究极究极大调研：跑几小时那种

> 执行：国际版 workbuddy / trae
> 产出：_arch_v46/ 共 105 文件（00总览 + 100方向 + 99来源 + ROADMAP）
> 要求：每个方向至少做 10 次搜索，每个方向 3000+ 字，必须有具体数字/具体论文/具体案例/具体行动
> 格式：参考 _arch_v39/v41/v44/v45

## 项目现状（精确锚点）
- 阙疑（QueYi）：C++知识验证系统
- 83卡（41 verified + 3 red-team + 39 draft）/ 67规则 / 9保护器 / 452账本 / 813行内核
- 四态判决 + append-only哈希链 + Merkle checkpoint
- 盲holdout 30样本（真错17个），检出率66.7%
- 外部corpus 40条（三层），检出率43.8%
- 真实缺陷夹具15条，重注入检出100%
- 变异测试 core 97.3% / all 81.5%
- 独立生成A/B/C：15断言，B推翻9条（60%）
- 反事实算子 P=R=F1=0（待修）
- 目标：NeurIPS 2027 E&D track
- 用户：双非本科生，合肥，嵌入式，0影响力

## 100个调研方向

=== 第一组：论文与学术（25个）===

01 NeurIPS E&D 2024录用论文全列表（每篇标题+作者+机构）
02 NeurIPS E&D 2025录用论文全列表
03 NeurIPS E&D 2026录用论文全列表
04 NeurIPS E&D录用率/投稿数/接收数（三年具体数字）
05 NeurIPS E&D审稿标准详解（从OpenReview看真实分数分布）
06 NeurIPS rebuttal翻盘真实案例
07 NeurIPS desk reject常见原因
08 ICSE E&D track vs NeurIPS E&D对比
09 ASE/FSE的AI验证相关track
10 Workshop论文对求职/申研有用吗
11 双投错峰策略（真实案例）
12 论文被拒后转投哪里
13 arXiv预印本策略（什么时候发/怎么发）
14 引用怎么涨（真实方法/数据）
15 论文版本管理（v0.1→camera-ready）
16 怎么选target venue（决策框架）
17 单人论文写作时间线（精确到周）
18 Abstract写作模板（150词，5个范例）
19 贡献声明怎么写才不被嫌overclaim
20 相关工作怎么写（3个好例子）
21 Method section怎么写
22 Evaluation section怎么写
23 Threats to Validity五层写法详解
24 统计方法精确指南（Clopper-Pearson/Fisher/效应量）
25 单人项目怎么凑够baseline

=== 第二组：技术与系统（25个）===

26 C++ UB完整分类（每类3个真实例子）
27 GCC/Clang/MSVC行为差异top 30
28 真实compiler bug历史top 30
29 内存错误检测工具对比（ASan/TSan/MSan/UBSan/Valgrind）
30 编译优化级别对结果的影响（-O0/-O1/-O2/-O3/-Os）
31 变异测试算子设计（具体算子列表）
32 PBT属性测试最佳实践
33 Python测试工具链（pytest/hypothesis/coverage/mutmut）
34 静态分析工具（clang-tidy/cppcheck/coverity）
35 类型系统与验证（mypy/pyright/Rust types）
36 Git工作流（单人项目怎么用branch/release）
37 CI/CD最小配置（GitHub Actions）
38 日志与可观测性
39 错误处理最佳实践（fail-closed vs fail-open）
40 性能优化profile（cProfile/py-spy）
41 安全（不要泄漏密钥/凭证管理）
42 数据版本管理（DVC等）
43 实验可重复性怎么做
44 小模型验证器（0.5B-7B）可行性
45 多智能体验证真的有用吗（最新实证）
46 轨迹层验证怎么做
47 知识图谱验证 vs 文本验证
48 LLM-as-judge最新方法（2025-2026）
49 事实核查模型（MiniCheck/FactScore等）
50 形式化验证性价比（seL4经验）

=== 第三组：个人与发展（25个）===

51 双非本科生怎么找导师
52 冷邮件模板（3个成功案例）
53 怎么在学术界建立存在感
54 时间管理精确到小时
55 怎么读论文（三遍法实操）
56 怎么写论文（每个section模板）
57 英文写作怎么提高
58 怎么用LLM辅助科研（但不依赖）
59 怎么写技术博客
60 怎么做技术演讲
61 怎么建个人品牌（GitHub/Twitter/小红书）
62 嵌入式工程师2026就业市场
63 长鑫存储嵌入式岗位JD
64 华为嵌入式岗位JD
65 大疆嵌入式岗位JD
66 嵌入式vs AI/后端，哪个更适合双非
67 考研与科研并行时间分配
68 怎么准备复试（展示这个项目）
69 考研没上岸怎么办
70 怎么找实习
71 怎么写简历
72 怎么准备技术面试
73 心理与体力管理（避免burnout）
74 失眠/内耗怎么应对
75 合肥本地就业情况

=== 第四组：未来与竞争（25个）===

76 2026-2028模型能力预测
77 内置验证会取代外部验证吗
78 小模型验证器的未来
79 现在有谁在做类似的事（列10个）
80 大厂在做什么（OpenAI/Anthropic/Google/Meta）
81 阙疑的护城河是什么
82 12-18个月后会被追上吗
83 EU AI Act对验证系统的影响
84 中国AI监管动向
85 高风险AI系统的验证要求
86 grants怎么申请（NLnet/MOSS/NSF）
87 单人开源项目收入来源
88 什么时候该商业化
89 论文中了之后怎么办
90 论文被拒了怎么办
91 项目烂尾了怎么办
92 失败了怎么恢复
93 怎么用这个项目找工作
94 怎么用这个项目申学校
95 下一个项目做什么
96 技术趋势判断（2027-2030）
97 单人项目的历史（成功案例）
98 单人项目的历史（失败案例）
99 这个项目的机会成本
100 终极问题：这个项目值不值得继续

## 要求（每个方向都要较真）
- 每个方向至少做10次搜索
- 每个方向3000+字
- 关键数据必须有来源（URL/论文/作者/年份）
- 数字必须精确
- 每个方向最后给"对阙疑的3条具体行动"
- 诚实标注盲区
- 零污染：只写 _arch_v46/

