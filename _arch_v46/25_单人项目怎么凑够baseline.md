# 方向 25：单人项目怎么凑够 baseline

## 核心结论

1. **单人项目的 baseline 有且只有五类来源，优先级是"直接跑 > 公开基准 > 重实现 > 引用他人数字 > 人类基线"**——前三类可复算，第四类不可比，第五类成本最高且极易被批评为不具代表性（ICML 2025 的 115 篇人类基线综述指出 3–5 个标注者远不足以代表"人类水平"，一般人群基线建议约 1000 人）。
2. **"引用别人论文里的数字"是最后手段，且必须显式标注不可比**：Musgrave 等（2020，ECCV）在统一训练与评估协议后，让过去四年度量学习论文声称的提升**大部分消失**；Wolfrath 等（2024）证明省略 baseline 或与弱 baseline 比较会掩盖方法的真实价值。**统一设置重跑，是唯一能站住的比较方式。**
3. **阙疑有一个别人没有的便宜**：ACM SIGSOFT Empirical Standards 的 Benchmarking 标准把"**benchmark 没人用**""**没人独立复现**""**没有组织维护**"三条**明确列为无效批评（Invalid Criticisms）**，并明说 proto-benchmark 可以用小群体起步。这意味着阙疑**不需要**靠"baseline 数量多"来防守，而应该靠"baseline 可比 + 原始结果可复算"来防守。

---

## 精确数字与案例

### 1. 公开事实：artifact 的"可用"与"能用"之间有一道 79%→25% 的鸿沟

**(a) ICSE artifacts（2015–2024，1372 篇论文）**：给出 artifact 链接的 **1085 篇（79.08%）**；链接可访问的 **941 篇（86.73%）**；**含可执行组件的只有 796 篇（84.59%）**。该研究原文写道："the publicly shared artifacts were **not executable due to undocumented issues**, underscoring the gap between availability and practical reusability."（公开分享的 artifact 因未记录的依赖问题而**不可执行**，暴露了"可用"与"可实际复用"之间的鸿沟。）研究还做了 **100 篇的分层抽样**。

**(b) EuroSys Artifact Evaluation（2021–2025）**：接收论文 38 / 45 / 54 / 71 / 85 篇；artifact 投稿率 58% / 73% / 59% / 47% / 53%；**Artifact Available 占接收论文比例** 55% / 73% / 57% / 45% / **52%**；**Evaluated-Functional 占比** 47% / 60% / 44% / 35% / **49%**；**Results Reproduced 占比** 37% / 44% / 15% / 17% / **25%**。

**(c) 对阙疑的直接含义**：一个单人项目最容易被审稿人质疑的是"你的结果没人验证过"。上面两组数字给出了**反向论证**：即使有完整 artifact 生态的顶会，真正能被复现出结果的比例也只有 **25%**。所以阙疑的 baseline 策略应当把"**让别人能在自己机器上跑出你的表 1**"作为第一优先级——这比多凑三个 baseline 更值钱。

### 2. 五类 baseline 的精确来源清单（含获取成本）

**第 1 类：现成工具直接跑（成本最低，可信度最高）**

| baseline | 获取方式 | 成本估计 | 备注 |
|---|---|---|---|
| **cppcheck** | `apt install cppcheck`（Ubuntu 24.04 仓库版本约 2.13–2.14）；`cppcheck --enable=all --inconclusive --xml` | 半天 | 中文技术博客称其对"传统 C 和嵌入式场景的记忆类和缓冲区类问题覆盖最深"（**非同行评议来源**） |
| **clang-tidy** | `apt install clang-tidy-18`；`clang-tidy -checks='*' file.cpp -- -std=c++20` | 半天 | 同上来源称其对现代 C++ 覆盖面最广（**非同行评议来源**） |
| **UBSan / ASan** | `clang++ -fsanitize=undefined,address -O0/-O1/...` | 1 天（要扫编译档） | 阙疑已有实证：`-O1`→`-O0` 使 **3/5** 个 miss 被同一 sanitizer 抓住 |
| **Valgrind / MSan / TSan** | 包管理器 | 1 天 | 与 ASan 有重叠，可视作"sanitizer 组合"基线的一个变体 |
| **哑基线（grep + 正则）** | 自己写 20 行 | 2 小时 | **最容易被忽略但最有价值**：能证明"你的规则不是正则能替代的" |

**第 2 类：公开基准数据集（成本中等，可信度最高）**

| 基准 | 规模 | 语言 | 备注 |
|---|---|---|---|
| **BUGSC++** | **209 个真实缺陷，来自 22 个开源项目** | **C/C++** | IEEE 文献编号 **10298287**（2023）；"A Highly Usable Real World Defect Benchmark for C/C++"；**获取方式与许可证须核实** |
| **Defects4J** | **835 个 bug（另有 29 个 deprecated）** | Java | `github.com/rjust/defects4j`；**语言不匹配**，只能用于"方法论迁移"论证 |
| **BugsInPy** | 未核实 | Python | 同上，语言不匹配 |
| 阙疑自有夹具 | **15 条**（7 个来源 commit） | C++ | `data/defect_fixtures/defects.json` |

**这一类的关键判断**：阙疑的 **15 条真实缺陷夹具**在规模上远小于 BUGSC++ 的 **209 条**。诚实的处理方式是**主动说明差异**，而不是回避——例如："我们的夹具是 15 条（7 个来源 commit），BUGSC++ 是 209 条（22 个项目）；我们不声称覆盖度可比，只声称我们的夹具是**可重注入验证**的（重注入检出 6/6，历史覆盖 12/15）。"**注意 6/6 的 Clopper-Pearson 95% 下限只有 0.5407**（见方向 24），所以"100% 检出"必须写成"6/6，95% 置信区间 [54.07%, 100%]"。

**第 3 类：自己重实现 baseline（成本最高，但完全可控）**

重实现的成本主要来自"把对方方法在自己环境里跑通"。可参照的算力估算实践：公开的 GPU 小时估算表把"复现并改进某个开源 baseline"作为独立场景单列（`walkinglabs.github.io/hands-on-modern-rl/appendix_gpu_hours/`），说明"复现 baseline"本身已被社区当作一项需要专门预算的工作。阙疑的场景是 CPU + 编译，成本远低于深度学习，但**编译档扫描会成倍放大时间**：若 5 个编译档 × 4 个 sanitizer 组合 × 40 条样本 = **800 次编译运行**，这是需要显式登记在 checklist 第 8 项（算力资源）里的。

**第 4 类：引用公开结果（成本最低，可信度最低）**

Musgrave 等（2020）与 Wolfrath 等（2024）都证明这条路的危险性。若必须引用，写法模板是：

> "We do **not** re-run [Tool X] in our environment. We cite the number reported by [Author, Year, Table N] and mark it as **not directly comparable** because [编译档 / 规则集版本 / 语料 / 判定粒度] differ. For the directly comparable comparison, we re-run [Tool Y] under the alignment protocol of §5.3."

**第 5 类：人类基线（成本最高，且最容易被批评）**

ICML 2025 Spotlight 论文（arXiv:**2506.13776**）系统审查了 **115 项**人类基线研究，给出的具体建议门槛：

- **测试集必须一致**：若因预算只能用子集，**AI 的分数也必须在同一子集上重算**，且子集须随机采样或按难度/主题分层。否则"人机比较"无效。
- **样本量**：多数研究只用 **3–5 个标注者**；对一般人群基线建议做**统计功效分析**，经验法则约需 **1000 名参与者**才能代表美国成年人口；专家基线可用便利样本，但**必须显式定义专家资格**。
- **不确定性**：须报统计检验、置信区间或性能分布，**不能只报点估计**。
- **方法效应**：人机须使用**完全相同的任务说明、示例与上下文**，并随机化题目与选项顺序。
- **努力程度**：公平比较应在相似资源投入下进行（相同时间限制或可比成本）。
- 论文附有 **Appendix B 报告清单**，覆盖参与者人口学特征、抽样策略与纳入排除标准、知情同意与伦理审查、任务说明与培训材料、质量控制措施、评分方法与指标定义、不确定性度量七类。

**阙疑的现实做法**：招募 **3 名同校同学**对 30 条 holdout 做独立判决，报 **Cohen's κ + 置信区间**，并**明确写出**"n=3 是便利样本，不代表人类水平，本基线仅用于估计任务难度的上界，不用于人机对比"。**不要**写"人类准确率 X%"。

### 3. 单人论文的既有事实（用于回应"你只有一个人"的质疑）

- **Scientometrics 2025** 的 *"A note on the topic of single-author articles in science"*（Springer，DOI **10.1007/s11192-025-05315-0**，2025-04-20 在线）：明确指出"**Although the extinction of single-author articles has been predicted multiple times, they continue to be published.**"（尽管单作者论文被多次预言将消失，它们仍在持续发表），并使用两个指标评估单作者文章在不同学科中的规模与影响力差异。
- **arXiv:2607.10780**，*"Return of the solo author: The changing division of labor in science"*（2026-07-14）：以"无人类合著者的论文（solo paper）"为对象做实证探测。**该文的正文与具体数字本方向未核实**，只核实到标题与发表时间。
- **对阙疑的用法**：在 Cover Letter 或 Threats to Validity 里引用这两条，说明"单作者不是方法学缺陷"，并把"单人"转化为**优势**——单人项目没有跨机构协调成本，因此**artifact 的可复现性更容易做到端到端**。这一点正好呼应 §1 的 79%→25% 鸿沟。

### 4. 单人 baseline 的实操成本表（阙疑版）

| 项 | 具体动作 | 一次性成本 | 可复算产物 |
|---|---|---|---|
| cppcheck 基线 | 安装 + 写 `run_baseline.sh` | 0.5 天 | `baseline/cppcheck/*.xml` |
| clang-tidy 基线 | 同上 | 0.5 天 | `baseline/clang_tidy/*.yaml` |
| sanitizer 组合基线 | 5 编译档 × {ASan, UBSan, MSan, TSan, ASan+UBSan} | 2 天（跑机时间为主） | `baseline/sanitizer/matrix.csv` |
| 哑基线（grep+正则） | 20 行脚本 | 2 小时 | `baseline/dumb/regex_hits.csv` |
| BUGSC++ 外部验证 | 下载 + 适配 209 条中的 C/C++ 子集 | **3–5 天**（含许可证核实） | `baseline/bugscpp/results.csv` |
| 人类基线（3 人） | 30 条 × 3 人 + κ 计算 | 2 天（含协调） | `baseline/human/kappa.md` |
| 合计 | — | **约 9–11 人日** | — |

**这个量级对单人项目是可完成的**（约两周全职，或一个月业余）。关键在于**只做前四项**（约 3.5 天）就能构成一个完整的 baseline 表；BUGSC++ 与人类基线属于"加分项"而非必需项。

### 4b. 单人做 baseline 的三个真实障碍与破解法

**障碍一：没有算力也没有时间重跑所有 baseline。** 破解法是把 baseline 分成"必跑"与"可选"两档，必跑档只保留**能在一台机器上跑完**的四项（cppcheck / clang-tidy / sanitizer 组合 / 哑基线）。判断标准不是"这条 baseline 重不重要"，而是"**它的输出能不能变成一行可复算的原始结果**"。凡是不能产出逐样本原始结果的比较（例如只有论文里的一个汇总数字），一律归入"引用但不比"档。

**障碍二：没有第二个标注者，所以做不了真正的一致性检验。** 破解法是**降低主张的层级**而不是伪造数据：把"人类基线"改写成"任务难度的探索性上界"，并明确写出 n=3、便利样本、不代表人类水平。ICML 2025 那份 115 篇人类基线综述的核心建议正是"即使无法达到最高严谨度，也应显式讨论方法学局限并收窄主张范围"。换句话说，**承认 n=3 不够，本身就是一个合格的学术行为**；把 n=3 包装成"人类水平"，才是真正的风险。

**障碍三：没有机构背书，artifact 可能不被信任。** 破解法是**用可验证性替代权威性**。ACM 的 Available 徽章只要求三件事：用 DOI 指向**具体版本**（Zenodo 不要用 "always latest" DOI）、归档在**长期保存的档案库**、以及**不可变**。这三件事都不需要机构，只需要一个人愿意把 DOI、SHA 与校验脚本写清楚。相比之下，"我来自某机构"不能替代任何一项。这也是阙疑把"独立对账器"作为一等贡献的最强理由：**权威性买不到，可验证性写得出来。**

**一个必须避开的陷阱：把"我没跑 baseline"解释成"不需要 baseline"。** Empirical Standards 确实把"benchmark 没人用""没人独立复现""没有组织维护"列为无效批评，但它**没有**把"没有 baseline"列为无效批评。Essential Attributes 里明确要求"要么论证所选既有基准的合理性，要么定义新基准并给出四要素（被基准的质量 / 量化指标 / 测量方法 / 工作负载或任务样本）"，并且要求"allows different configurations of a system under test to compete on their merits without artificial limitations"。也就是说：**"我的 benchmark 新"可以被原谅，"我的 benchmark 没法比较"不可以。**

### 5. 三条能直接写进论文的"防守句"

**防守句 A（回应"baseline 太少"）**——引用 Empirical Standards 的 Invalid Criticisms：
> "We report four directly re-run baselines (cppcheck, clang-tidy, sanitizer suite, and a regex dumb baseline) under a unified alignment protocol. We deliberately do not add further baselines whose reported numbers were produced under different rule sets, compile flags, or evaluation granularity; per the ACM SIGSOFT Empirical Standards for Benchmarking, absence of independent replication and absence of a maintaining organization are explicitly listed as **invalid criticisms** of a new benchmark."

**防守句 B（回应"数据太小"）**——用区间与功效正面回应：
> "Our holdout has 30 seeds (17 planted-true, 9 control, 4 unknown). At this sample size a Wald 95% interval has a half-width of ≈0.16 at p≈0.7; accordingly we report Clopper-Pearson intervals for every proportion and explicitly limit our claims to differences larger than that resolution. Reaching a ±0.10 half-width would require n≈81."

**防守句 C（回应"没人验证过"）**——用 ICSE/EuroSys 数字反向论证：
> "Across 1372 ICSE papers (2015–2024), 79.08% share an artifact link, but only 25% of EuroSys artifact submissions (2025) yielded reproduced results. Our design therefore makes independent verification the first-class contribution: the reconciler does not import the engine (`tools/gate_engine.py`, 3826 lines) and can be run by a third party against the ledger and rule table alone."

---

## 对阙疑的 3 条具体行动

**行动 1（2026-11-30 前，跑通四条直接基线）**：新建 `baseline/run_baselines_676.sh`，一次跑完四条基线，统一输出到 `baseline/out/<tool>/<sample_id>.json`。命令骨架：
```bash
for f in $(jq -r '.samples[].path' data/external_corpus/external_corpus_665.json); do
  cppcheck --enable=all --inconclusive --xml --output-file=baseline/out/cppcheck/$(basename $f).xml "$f"
  clang-tidy -checks='*' "$f" -- -std=c++20 > baseline/out/clang_tidy/$(basename $f).yaml 2>&1
  for O in O0 O1 O2 O3 Os; do
    clang++ -std=c++20 -$O -fsanitize=address,undefined -o /tmp/a.out "$f" && /tmp/a.out > baseline/out/sanitizer/${O}_$(basename $f).log 2>&1
  done
done
```
验收标准：四条基线在**同一 40 条语料、同一编译档集合**上产出逐样本原始结果，可直接生成 `baseline/matrix.csv`。

**行动 2（2026-12-31 前，写对齐协议）**：在 `research/07_baselines.md` 中新增 "Alignment Protocol" 一节，明确写出对齐的三个维度（语料 / 编译档矩阵 / 判定粒度），并对每条 baseline 标注 "re-run by us" 或 "cited, not comparable"。引用 ACM SIGSOFT Empirical Standards 的 "allows different configurations of a system under test to compete on their merits without artificial limitations" 作为协议设计依据，并把三条 Invalid Criticisms 原文抄进 Threats to Validity。**这一节写完之后，"baseline 不够"这条质疑基本被封死。**

**行动 3（2027-02-15 前，评估是否引入 BUGSC++ 与人类基线）**：先做 1 天的可行性核查——核实 **BUGSC++（IEEE 10298287，209 条 / 22 项目）** 的获取方式、许可证、以及能否在本机编译；若可行，抽 30–50 条做外部验证。人类基线只在有把握控制质量时做：3 名同校同学 × 30 条，报 κ + CI，并强制写上"n=3 便利样本，不代表人类水平"。若时间不足，**优先放弃人类基线而不是放弃 BUGSC++**——因为公开基准可复算，人类基线不可复算。

---

## 盲区（诚实标注）

1. **BUGSC++ 的获取方式、许可证、以及 209 条中 C 与 C++ 的分布未核实**（只核实到 IEEE 文献号 10298287、标题 "BUGSC++: A Highly Usable Real World Defect Benchmark for C/C++"、发表年份 2023、"209 real-world bugs collected from 22 open-source projects"）。**行动 3 的第一步必须是核实许可证**，否则可能无法用于投稿。
2. **Defects4J 的 835 与 29 deprecated 来自其 GitHub README 的检索摘要**，未逐行核对。
3. **cppcheck 2.14 / clang-tidy 18 的对比结论来自中文技术博客（CSDN / devpress / codechina）**，**非同行评议来源**，其中的"检测率""速度"数字**本文一概未引用**。若要在论文里使用这类对比，必须自己跑，不能引用博客。
4. **"Papers with Code 于 2025 年 7 月被 Meta 关停"来自第三方站点（codesota.com）的表述**，**未从 Meta 官方渠道核实**。阙疑若要引用"leaderboard 生态的变化"，须自行核实。
5. **ML Reproducibility Challenge（MLRC）**：只核实到官网 `reproml.org` 称 "MLRC 2026 will be an official track at NeurIPS 2026"，以及 2022 年的特刊在 Zenodo（`zenodo.org/records/8200058`）。**其补贴金额（网传 500 美元）未核实**，本文不采用。
6. **Scientometrics 2025 单作者论文那篇的具体数字（单作者论文占比、影响力差异）未核实**，本文只引用了其摘要句 "Although the extinction of single-author articles has been predicted multiple times, they continue to be published."
7. **arXiv:2607.10780 "Return of the solo author" 的正文未核实**，只核实到标题与 2026-07-14 的发表时间。
8. **ICML 2025 human baselines 论文的"约 1000 名参与者"是 rule of thumb 而非功效分析结果**，且转引自论文解读页面，**未逐字核对 arXiv:2506.13776 原文**。
9. **"约 9–11 人日"的成本表是本文基于常规经验的估算**，不是实测值；实际耗时高度依赖环境（编译档扫描的机器时间可能远超人工时间）。
10. **四条基线命令骨架中的参数（`cppcheck --enable=all --inconclusive --xml`、`clang-tidy -checks='*'`、`jq` 路径表达式）未在本机实测**，`jq -r '.samples[].path'` 的字段名须以实际 JSON 为准。
11. **`baseline/` 目录在阙疑仓库中是否存在未核实**（`_arch_v46/00_仓库扫描.md` 未列出该目录），行动 1 中的路径为**建议路径**，落库前须确认不与现有目录冲突。
12. **GPU 小时估算表（walkinglabs.github.io）为社区维护文档**，非同行评议来源；本文只用它说明"复现 baseline 已被当作独立预算项"，未引用其任何具体数字。

---

## 来源

1. "The State of Open Science in Software Engineering Research: A Case Study of ICSE Artifacts"（1372 篇 ICSE 论文 2015–2024：1085 artifact 链接 / 941 可访问 / 796 含可执行组件；100 篇分层抽样）— https://acm-stag.literatumonline.com/doi/10.1145/3744916.3787813
2. "Lessons Learned from Five Years of Artifact Evaluations at EuroSys"，ACM Reproducibility and Replicability 2025，DOI 10.1145/3736731.3746152 — https://dl.acm.org/doi/abs/10.1145/3736731.3746152
3. ACM SIGSOFT Empirical Standards, "Benchmarking (of Software Systems)"（Invalid Criticisms 三条原文、Examples of Acceptable Deviations、Antipatterns）— https://github.com/acmsigsoft/EmpiricalStandards/blob/master/docs/standards/Benchmarking.md
4. K. Musgrave, S. Belongie, S.-N. Lim, "A Metric Learning Reality Check", arXiv:2003.08505；ECCV 2020，DOI 10.1007/978-3-030-58595-2_41 — https://arxiv.org/pdf/2003.08505
5. N. Wolfrath, J. Wolfrath, H. Hu, A. Banerjee, A. N. Kothari, "Stronger Baseline Models — A Key Requirement for Aligning Machine Learning Research with Clinical Utility", arXiv:2409.12116（2024）— https://arxiv.org/abs/2409.12116
6. "Recommendations and Reporting Checklist for Rigorous & Transparent Human Baselines in Model Evaluations", arXiv:2506.13776；ICML 2025 Spotlight（115 项人类基线研究；3–5 标注者 vs 约 1000 人；Appendix B 报告清单）— https://en.papernotes.org/ICML2025/recommender/recommendations_and_reporting_checklist_for_rigorous_transparent_human_baselines/
7. "BUGSC++: A Highly Usable Real World Defect Benchmark for C/C++"，IEEE 文献号 10298287，2023（209 real-world bugs / 22 open-source projects）— https://ieeexplore.ieee.org/document/10298287
8. Defects4J（835 bugs + 29 deprecated）— https://github.com/rjust/defects4j
9. "A note on the topic of single-author articles in science"，*Scientometrics*，2025，DOI 10.1007/s11192-025-05315-0 — https://link.springer.com/article/10.1007/s11192-025-05315-0
10. "Return of the solo author: The changing division of labor in science"，arXiv:2607.10780（2026-07-14）— https://arxiv.org/html/2607.10780v1
11. ML Reproducibility Challenge 官网（MLRC 2026 成为 NeurIPS 2026 官方 track）— https://reproml.org/ ；2022 特刊 Zenodo — https://zenodo.org/records/8200058/files/article.pdf
12. C++ 静态分析工具对比（cppcheck vs clang-tidy）— **非同行评议来源**：https://devpress.csdn.net/v1/article/detail/154845766 ；https://codechina.net/article/weixin_28839629/399425
13. GPU 小时估算表（社区文档，"复现并改进开源 baseline"作为独立预算场景）— https://walkinglabs.github.io/hands-on-modern-rl/appendix_gpu_hours/gpu-hours-estimation
14. "Papers With Code 于 2025 年 7 月被 Meta 关停"（第三方表述，未从 Meta 官方核实）— https://www.codesota.com/papers-with-code
15. 阙疑仓库锚点（holdout 30 / corpus 40 / 缺陷 15 / 重注入 6/6 / 编译档 3-of-5 / gate_engine.py 3826 行）— `_arch_v46/00_仓库扫描.md`、`_arch_v46/ROADMAP.md`
16. 本方向引用的置信区间数字（6/6 → Clopper-Pearson 95% [0.5407, 1.0000]；n=30 时半宽 ≈0.16；±0.10 需 n≈81）为**本次实算**，非引用。
