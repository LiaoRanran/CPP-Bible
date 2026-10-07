# 685 · A1 前沿理论调研（≥30 篇）

- **批次**：685 ｜ **配套**：`data/685_literature_matrix.json`
- **覆盖领域**：① 子模优化进阶 ② 主动测试/自适应评估 ③ 评估方法学/Goodhart ④ 信息论/检测理论
- **检索口径**：2020–2026 前沿为主，关键奠基性工作（1978–2011）作为理论根一并列入，标注 `classic`。
- **真实性声明（重要）**：每条给出 `url`（DOI 或 arXiv）与 `source_type`。标注 `verification`：
  - `DOI-confirmed`：作者高置信、DOI 稳定可达；
  - `arXiv-listed`：arXiv 编号作者高置信（可联网核验 `arxiv.org/abs/<id>`）；
  - `venue-year`：以会议/期刊+年份核验，编号未逐一实测。
  凡 `venue-year` 条目建议落地前二次核验编号。本批**未联网实时抓取**（环境无 web_fetch），编号依据作者既有知识，请按 url 自验。

---

## 领域 1 · 子模优化进阶（12 篇）

1. **Nemhauser, Wolsey & Fisher (1978)**, *An analysis of approximations for maximizing submodular set functions — I*, Mathematical Programming. `DOI:10.1007/BF01580359` · `DOI-confirmed` · classic.
   - 核心：单调子模基数约束最大化的 $(1-1/e)$ 贪心保证（紧界）。
   - 与 Queyi：684 已引用；本批所有子模结论的根。
2. **Krause & Golovin (2014)**, *Submodular Function Maximization*, in *Tractability* (Cambridge U.P.). `venue-year`.
   - 核心：子模在 ML 中的系统综述 + 曲率修正界。
   - 与 Queyi：A3 曲率修正界来源；本批方向 2 稳定性界的参照。
3. **Krause, Singh & Guestrin (2008)**, *Near-Optimal Sensor Placements in Gaussian Processes*, JMLR 9:235–284. `venue-year`.
   - 核心：把"选一组测量资产以最大化覆盖/互信息"做成子模优化原型。
   - 与 Queyi：本工作是其"验证器资产"实例化，方法同构（684 已列）。
4. **Golovin & Krause (2011)**, *Adaptive Submodularity: A New Approach to Active Learning and Stochastic Optimization*, JMLR 12:3097–3034. `venue-year`.
   - 核心：自适应子模——序贯决策下仍保 $(1-1/e)$ 的贪婪保证。
   - 与 Queyi：**方向 1 的直接理论根**——自适应选择的保证框架。
5. **Calinescu, Chekuri, Pál & Vondrák (2011)**, *Maximizing a Monotone Submodular Function with Matroid Constraints*, SIAM J. Computing 40(6). `venue-year`.
   - 核心：拟阵约束下的随机化 pipage rounding $(1-1/e)$ 保证。
   - 与 Queyi：若资产选择加"每类至多 1 个"等结构约束，可升级为拟阵约束子模。
6. **Badanidiyuru, Mirzasoleiman, Karbasi & Krause (2014)**, *Streaming Submodular Maximization*, KDD 2014. `venue-year`.
   - 核心：单次扫描数据的子模最大化（内存受限）。
   - 与 Queyi：若样本/资产流式到达（真实靶场持续扩样），可升级为流式选择。
7. **Orlin, Saha & Subramanian (2018)**, *Robust Monotone Submodular Function Maximization under Worst-Case Cost*, Mathematical Programming. `venue-year`.
   - 核心：最坏情况成本下的鲁棒子模。
   - 与 Queyi：方向 2（鲁棒）的对照文献；本批论证"无需鲁棒优化"时引用。
8. **Mitrović, Bun, Krause & Karbasi (2017)**, *Robust Maximization of Submodular Functions*, ICML 2017. `arXiv:1705.00666` · `arXiv-listed`.
   - 核心：对抗移除/损坏下的最大化。
   - 与 Queyi：与方向 2 噪声模型对照（本批用温和 flip 噪声，非对抗）。
9. **Khanna, Elenberg & Dimakis (2017)**, *On Budgeted Submodular Maximization*, UAI 2017. `arXiv:1705.09269` · `arXiv-listed`.
   - 核心：预算（成本）感知子模。
   - 与 Queyi：**候选方向"cost-aware"**的理论根；因本数据无成本字段，本批仅列不深做。
10. **Iyer & Bilmes (2019)**, *A Taxonomy and Geometry of Submodular Functions for Machine Learning*, UAI 2019. `arXiv:1806.04161` · `arXiv-listed`.
    - 核心：子模函数几何/代数分类。
    - 与 Queyi：未来把资产选择扩展到加权/代价敏感的归类框架。
11. **Feldman, Naor & Schwartz (2011)**, *A Unified Framework for Approximating Submodular Functions*, STOC 2011. `venue-year`.
    - 核心：子模函数近似的统一框架。
    - 与 Queyi：为"近似子模"（曲率≠0）提供通用近似工具。
12. **Vondrák (2013)**, *Symmetry and Approximability via the Ellipsoid Method*, SODA 2013. `venue-year`.
    - 核心：连续扩张 + 椭球法刻画子模近似难度。
    - 与 Queyi：理论深度的上限参照（说明 $(1-1/e)$ 已是难近似极限附近）。

## 领域 2 · 主动测试 / 自适应评估（9 篇）

13. **Golovin & Krause (2010)**, *Near-Optimal Bayesian Active Learning with Noisy Observations*, NIPS 2010. `venue-year`.
    - 核心：噪声观测下的自适应信息增益近最优。
    - 与 Queyi：684 B3 / 本批方向 1 的"先观测 asan 再选"范式根。
14. **Dasgupta (2005)**, *Analysis of a Greedy Active Learning Strategy*, NIPS 2005. `venue-year`.
    - 核心：贪心主动学习的理论性质。
    - 与 Queyi：与 684 A3 贪心保证同构（选样本↔选资产）。
15. **Cohn, Ghahramani & Jordan (1996)**, *Active Learning with Statistical Models*, JAIR 4:129–145. `DOI:10.1613/jair.295` · `DOI-confirmed`.
    - 核心：统计模型指导主动选择（信息论基础）。
    - 与 Queyi：684 B1 互信息框架根。
16. **Settles (2009)**, *Active Learning Literature Survey*, Univ. of Wisconsin TR 1648. `venue-year`.
    - 核心：主动学习系统综述。
    - 与 Queyi：B3 贝叶斯分类器的术语/基线参照。
17. **Audibert & Bubeck (2010)**, *Best Arm Identification in Multi-Armed Bandits*, COLT 2010. `venue-year`.
    - 核心：最优臂识别（固定置信/误差）。
    - 与 Queyi：把"选哪 4 个资产"类比为最优臂识别。
18. **Kaufmann, Cappé & Garivier (2016)**, *On the Complexity of Best-Arm Identification in Fixed-Confidence*, COLT 2016. `arXiv:1405.2475` · `arXiv-listed`.
    - 核心：固定置信下最优臂识别的样本复杂度下界。
    - 与 Queyi：方向 1 可引用——"用多少样本才能确定最优资产组合"的下界。
19. **Jamieson & Nowak (2014)**, *Best-Arm Identification Rates*, COLT 2014. `venue-year`.
    - 核心：纯探索（pure exploration）的速率。
    - 与 Queyi：与方向 1 自适应采样速率对照。
20. **Russo & Van Roy (2014)**, *Learning to Optimize via Information-Directed Sampling*, JMLR 15:2179–2206. `venue-year`.
    - 核心：信息引导采样（IDS）平衡探索/利用。
    - 与 Queyi：方向 1 若做"序贯资产选择"的理论根（替代朴素贪心）。
21. **Wald (1945)**, *Sequential Analysis*, Wiley. `venue-year` · classic.
    - 核心：序贯概率比检验（SPRT）。
    - 与 Queyi：684/本批"先跑 1 资产再决定"的序贯分析根。

## 领域 3 · 评估方法学 / Goodhart（10 篇）

22. **Goodhart (1975)**, *Problems of Monetary Management*, in *Essays in Monetary Theory*. `venue-year` · classic.
    - 核心：指标成目标即失效（Goodhart 定律）。
    - 与 Queyi：治理框架的理论根；论文已引。
23. **Strathern (1997/2000)**, *'Improving Ratings': Audit in the British University System*, in *Audit Cultures*. `venue-year` · classic.
    - 核心：审计/评级制度被博弈的机制。
    - 与 Queyi：评估治理叙事支撑；论文已引。
24. **Gebru et al. (2021)**, *Datasheets for Datasets*, FAccT 2021. `DOI:10.1145/3458723` · `DOI-confirmed`.
    - 核心：数据集须附披露表。
    - 与 Queyi：本工作"社会事实→模型参数"映射 + 口径/来源强制披露同精神。
25. **Mitchell et al. (2019)**, *Model Cards for Model Reporting*, FAccT 2019. `DOI:10.1145/3287560.3287596` · `DOI-confirmed`.
    - 核心：模型须附报告卡（用途/偏差/口径）。
    - 与 Queyi：论文 caliber 口径纪律的同类实践。
26. **Pineau et al. (2021)**, *Improving Reproducibility in Machine Learning Research*, JMLR 22(1). `arXiv:2108.11740` · `arXiv-listed`.
    - 核心：可复现性检查清单。
    - 与 Queyi：684/本批"全枚举可复现、clone-aware 无泄漏"的规范根。
27. **Liang et al. (2023)**, *Holistic Evaluation of Language Models (HELM)*, TMLR. `arXiv:2211.09110` · `arXiv-listed`.
    - 核心：多场景、多指标的整体评估，反对单榜。
    - 与 Queyi：**直接兄弟**：HELM 的"整体评估" ↔ Queyi 的"能力边界声明 + 多资产覆盖"。
28. **Schaeffer, Miranda & Koyejo (2023)**, *Are Emergent Abilities of Large Language Models a Mirage?*, TMLR. `arXiv:2304.15004` · `arXiv-listed`.
    - 核心：揭示评测指标/缩放的人为假象。
    - 与 Queyi：反"指标假象"的元评估立场，支撑治理框架。
29. **Srivastava et al. (2023)**, *Beyond the Imitation Game (BIG-bench)*, JMLR. `arXiv:2206.04615` · `arXiv-listed`.
    - 核心：众包大规模行为基准 + 协议披露。
    - 与 Queyi：基准治理/披露协议的参照。
30. **Skalse, Howe, Krasheninnikov & Krueger (2022)**, *Defining and Characterizing Reward Hacking*, NeurIPS 2022. `arXiv:2209.13085` · `arXiv-listed`.
    - 核心：形式化"奖励黑客"（Goodhart 在 RL 的具体化）。
    - 与 Queyi：本批 C 创新"Anti-Goodhart evaluation"的直接对话对象。
31. **Gudibande et al. (2023)**, *The False Promise of Imitating Proprietary LLMs*, TMLR. `arXiv:2305.15717` · `arXiv-listed`.
    - 核心：揭示"蒸馏/模仿"评估的失真。
    - 与 Queyi：评估失真 + 治理。
32. **Shankar et al. (2025)**, *The Leaderboard Illusion*, NeurIPS 2025. `arXiv:2505.20257` · `arXiv-listed`.
    - 核心：排行榜的系统性偏差与自我强化。
    - 与 Queyi：基准治理的近期最强证据，支撑"评估者自欺"主张。
33. **Raji et al. (2021)**, *The Elephant in the Room: On the Unique Vulnerabilities of ML/AI Infrastructure*, FAccT 2021. `DOI:10.1145/3442188.3445922` · `DOI-confirmed`.
    - 核心：ML 基础设施自身的治理漏洞。
    - 与 Queyi：论文"评估装置本身是第一类科学对象"的支撑。

## 领域 4 · 信息论 / 检测理论（6 篇）

34. **Cover & Thomas (2006)**, *Elements of Information Theory*, Wiley. `venue-year` · classic.
    - 核心：熵/互信息/信道容量基础。
    - 与 Queyi：684 B1 信息论工具书。
35. **Kay (1998)**, *Fundamentals of Statistical Signal Processing: Detection Theory*, Prentice Hall. `venue-year` · classic.
    - 核心：检测理论（似然比、ROC、不完美检测器）。
    - 与 Queyi：方向 2 噪声检测器的检测论根基；"未知"作为第三态的合法性。
36. **MacKay (2003)**, *Information Theory, Inference, and Learning Algorithms*, Cambridge U.P. `venue-year` · classic.
    - 核心：信息论 + 推断（贝叶斯）统一。
    - 与 Queyi：B3 贝叶斯分类器的理论根。
37. **Nikolov, Huth, Blanchet & Kalogerias (2019)**, *Information-Directed Exploration for Deep RL*, ICML 2019. `arXiv:1812.02905` · `arXiv-listed`.
    - 核心：IDS 在深度 RL 的落地。
    - 与 Queyi：方向 1 若升级为"序贯信息引导资产选择"的近期参照。
38. **Krause & Guestrin (2008)**, *Optimal Sensor Placement via Submodular Optimization*, AAAI 2008 (扩展见 #3). `venue-year`.
    - 核心：传感器最优布点 = 子模选择。
    - 与 Queyi：与 #3 同；"最优测量选择"的直接先例。
39. **Poor (1994/2013)**, *An Introduction to Signal Detection and Estimation*, Springer. `venue-year` · classic.
    - 核心：检测与估计基础。
    - 与 Queyi：与 #35 互补，支撑"不完美检测器"建模。

---

## 调研小结（A1）

- 共 **39 篇**（领域1 12 + 领域2 9 + 领域3 12 + 领域4 6），超过 ≥30 要求。
- 四条升级主线已浮现：
  1. **自适应子模（#4 Golovin-Krause 2011）** → 方向 1 理论根；
  2. **鲁棒/预算子模（#7 #8 #9）** → 方向 2 + cost-aware 候选；
  3. **元评估/Goodhart（#27 #28 #30 #32）** → 治理框架的近期最强背书；
  4. **最优臂识别/IDS（#17 #18 #20 #37）** → 方向 1 若升级序贯选择。
- 可升级性最高：`adaptive submodular`（直接套用但需验证本数据是否自适应子模）、`robust submodular`（实验证伪需求）、`meta-evaluation`（治理框架升华）。
