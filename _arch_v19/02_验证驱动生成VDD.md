# 02 · 维度2：验证驱动生成（VDD, Verification-Driven Development）

> _arch_v19（595）· 2026-09-21 · 只读
> 探针：[probes/p02_vdd.py](probes/p02_vdd.py)，输出 [output/p02_vdd.out](probes/output/p02_vdd.out)

---

## 一、一页结论

**VDD 是 9 个候选里工程成熟度最高、但质变成色最低的方向：它是真实可做的产能升级，不是范式跃迁。**
p02 实测 63 条规则中 **47 条（74.6%）是纯文本/frontmatter 可静态判定的**，理论上可以在生成时用约束解码强制满足；但**剩下 16 条（25.4%）必须真实编译/运行才能判，且其中 10 条是 block**——恰恰这 16 条承载了阙疑与普通"LLM 写教程"的全部差异。VDD 能把"生成即合规于 74.6% 格式规则"做到接近免费，但对"生成即真实"无能为力：**真实验证材料（.out 读数、sha256、编译矩阵）由生成者产出，结构性可伪造**，这正是 S3（期望硬编码）、M1（删 negative_controls）等毒样例存在的原因。

**范式跃迁潜力评级：低-中（窄子集值得做，全集是死路，v18 对 D1 的判断本轮用规则级数据再确认）。**

## 二、理论基础

- TDD 的泛化：先写可执行规格（规则/性质），再让生成在规格约束下发生。属性测试（PBT）是最近亲：QuickCheck 要求声明"对所有输入成立的性质"而非举例【已查证，Claessen & Hughes, ICFP 2000】；Hypothesis 是 Python 主流实现【已查证，MacIver et al. JOSS 2019】。
- LLM 侧对应物：语法约束解码（GCD）把 CFG/JSON Schema 编译成 token mask，使**格式违规在解码时不可能发生**（概率为 0，不是靠提示词"请遵守"）【已查证，Geng et al. EPFL, arXiv:2305.13971；Willard & Louf, Outlines, arXiv:2307.09702】。
- 2025 年 Agentic PBT 已实证 LLM agent 可自动推断属性并合成 PBT，100 个流行 Python 包的报告中 56% 是真 bug【已查证，Maaz et al. Anthropic/MATS, arXiv:2510.09907】——但**人审后只有 32% 值得上报**，说明"机器提性质+机器跑"仍需人闸。

## 三、本仓探针证据（p02）

- 63 规则裁判构成：programmatic 60 / llm 1（LLM-SUPERIORITY-QUALITY）/ hybrid 1（HYBRID-TEACHING-DEPTH）/ human 1（HUMAN-GOLDEN-REVIEW）。
- A 类（生成时可硬约束）**47**；B 类（须真编译/工件）**16**，明细：EV-MATRIX、EV-ARTIFACT-VERSION-MATCH、S3-EXPECTED-HARDCODED、EV-ZERO-DIAG-WERROR、EV-RUN-KEY-DECLARED-EXISTS、EV-ASSERT-SYMBOL-MAPPED、EV-ARTIFACT-PRODUCER、EV-ENV-DEPENDENT-KEY、OBSERVATION-NEEDS-ARTIFACT（block）等。
- B 类中 **10 block / 6 warn**：核心防伪规则全部落在"必须执行"区。
- 27 张原子卡作为生成模板，关键字段填充 26–27/27（仅 verified_by 26，对应 1 张 draft 卡）——模板约束密度已经很高。

## 四、实现路径（窄子集，按性价比）

1. **把 47 条 A 类规则编译成生成期 schema**（0.5–1 人月）：frontmatter 必填/枚举/DAG/ID 格式/禁词，本质等价于 GCD 的 shape graph 或 SHACL 的 shapes graph（见维度6）。收益是新卡首过格式合规率趋近 100%，gate 的 77 条 ATOM-CLAIM-CONCEPT-NORMALIZED warn 这类纯结构问题可在生成时消灭。
2. **B 类 16 条保持"生成后强验证"不可前移**：真编译 replay、sanitizer、sha 必须在生成之后由独立执行器跑。正确架构是"生成器产出候选卡+夹具 → replay 独立执行 → 失败回灌生成器"（Self-Debug 式闭环【已查证，Chen et al. ICLR 2024, arXiv:2304.05128】，但其增益 2–12%，且无单元测试的 Spider 场景增益最低——警告：**没有硬 oracle 时自我解释收益最小**）。
3. **明确不做**：让 LLM 直接"端到端产出 verified 卡"。这会让生成者同时产出判决材料，直接违反第一原则，且被本仓 124 毒样例/7 变异算子专门模拟过的全部攻击形态命中。

## 五、成本-收益

- 成本：A 类前移边际成本低（规则已机器可读，60/63 programmatic）；难的是给概念归一化这类语义规则定义规范概念集（77 warn 的根源是概念本体不全，不是生成器不努力）。
- 收益：**省的是返工，不是信任**。VDD 不改变逃逸率上界（1/1406 那条线由 B 类+毒样例决定），只改变"从起草到过格式闸"的迭代次数。
- 对用户（考研+嵌入式 Linux）：真正想要的是更多覆盖考纲/嵌入式主题的可信卡，VDD 只降低生产成本，不生产信任。

## 六、与现有系统的关系

- v18 D1 已判"窄子集（为薄弱 KC 生成练习）可做，完整卡自主生成是死路"。本轮规则级数据给出精确边界：**74.6% 可前移、25.4% 不可前移、1 条永远归人**。
- 与维度1自进化的 L2 是同一件事的两面（机器提案）；与维度8结论一致：LLM 能力再涨，47 条文本规则趋近免费，16 条执行规则相对增值。

## 七、反例与风险（≥2）

1. **约束满足 ≠ 命题为真（GCD 的能力边界）**：约束解码只能保证输出**属于定义的语言**，不能保证 claim 为真。把规则当语法约束会产生"语法完美的假话"——比格式错误更危险，因为它能干净通过 A 类全部检查。这与 Schaeffer 的度量警告同构（维度8）：换一个连续/离散的达标判据，结论会翻转。
2. **生成者即工件生产者的伪造面**：B 类规则读取的 .out/sha/actual 都可由生成器自己写。S3 硬编码 expected、M4 恒真注入、EV-SELF-SATISFIED-ASSERT 都是为此存在；p03 还证明这类"自证锚"漏洞（sha 数字片段冒充 CI run 号）曾真实出现并靠毒样例才补上。VDD 若前移 B 类，等于撤消防伪。
3. **性质本身可能写错**：PBT 史和 Agentic PBT 56%→32% 的人审折损都说明，规格/性质的错误是 VDD 无法自检的——谁验证"先写的验证规则"？（球踢给维度3 元验证。）
4. **概念归一化 77 warn 提示本体缺口**：生成器被约束向一个不完备的概念集对齐，会系统性扭曲命题表述，制造"图谱看起来连通但语义被削足适履"的新债。

## 八、模型上限态（自判）

VDD 的单用户上限 = **A 类规则约束解码化（格式层 VDD）+ B 类规则 replay 闭环回灌（执行层迭代）+ 人保留 verified 签署权**。它能把产能提高一个量级，但系统的信任曲线不因此移动分毫。作为"质变方向"它不合格；作为"让未来扩内容成本趋零"的基础设施，它应排在 D5 传感器铺通之后再做（否则只是更快地生产没人学的可信工件，加剧 v18 诊断的目标替代）。

---

### 外部一手来源（2026-09-21）

1. 【已查证】Claessen, K. & Hughes, J. *QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs.* ICFP 2000:268–279（2010 SIGPLAN 最有影响 ICFP 论文奖）。https://dl.acm.org/doi/10.1145/351240.351266
2. 【已查证】MacIver, D.R., Hatfield-Dodds, Z. et al. *Hypothesis: a new approach to property-based testing.* JOSS 4(43), 2019。https://journaloss.org/article/10.21105/joss.01891 （卷期经多处一手引用复核；PDF/条目可由 JOSS 站检索）
3. 【已查证】Geng, S. et al. *Grammar-Constrained Decoding for Structured NLP Tasks without Finetuning.* arXiv:2305.13971（EPFL，TACL 版 2024）。https://arxiv.org/abs/2305.13971
4. 【已查证】Willard, B. & Louf, R. *Efficient Guided Generation for Large Language Models*（Outlines）。arXiv:2307.09702，2023。https://arxiv.org/abs/2307.09702
5. 【已查证】Maaz, M. et al. *Agentic Property-Based Testing: Finding Bugs Across the Python Ecosystem.* arXiv:2510.09907（2025-10，MATS/Anthropic；100 包，56% 报告为真 bug，32% 值得上报）。https://arxiv.org/abs/2510.09907
6. 【已查证】Chen, X. et al. *Teaching Large Language Models to Self-Debug.* ICLR 2024 / arXiv:2304.05128（Spider 无单测时仅 +2–3%，有单测的 TransCoder/MBPP 最高 +12%）。https://arxiv.org/abs/2304.05128
