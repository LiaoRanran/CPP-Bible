# 方向 26：REPLICATION.md 怎么写

## 核心结论

1. **"有仓库"和"能复现"之间隔着一条实测可见的鸿沟：约 13% 的已链接仓库无法访问或是空的。** MICCAI 2026 论文 *The paper has a GitHub, the GitHub has a README, the README has nothing: Reproducibility Signals for Review Support*（Bolelli、Santoli、Marchesini、Lumetti、Grana，University of Modena and Reggio Emilia）分析了 **3722 篇 MICCAI 论文**，逐字结论：*"code-linking rising from **51.8% (2021)** to **72.5% (2025)**, but **∼13% of linked repositories are inaccessible or empty**"*；更关键的是 *"Overall, **65.5%** provide links, only **54.1%** have actual code"*。论文还点名两类失败模式：*"many papers still provide no code, or promise a release 'after acceptance' that never materializes in the camera-ready"*，以及 *"Others provide a repository link that is empty, private, missing critical components, or contains little more than a **placeholder README**"*。**对阙疑的直接含义：写了 REPLICATION.md 但内容空洞，比不写更糟——它会被明确归类为 "placeholder README"。**

2. **会议 AE 对"复现文档"有可量化的时间预算：安装与冒烟测试 30 分钟，完整评估几小时。** POPL 2026 Artifact Evaluation 页面逐字给出两条硬指标：*"Aim for the download, installation, and sanity-testing instructions to be completable in about a **half hour**."* 与 *"Aim for the evaluation instructions to take **no more than a few hours**. Clearly note steps that take more than a few minutes to complete. If the artifact cannot be evaluated in a few hours (experiments that require days to run, for example) consider an alternative artifact format, like a **screencast**."* 另外作者侧成本也被量化：*"you should expect to spend **at least 2-3 workdays** packaging your artifact, a large portion of which should be spent writing and testing your detailed instructions, provided in a README file."* **对单人项目的含义：把"30 分钟冒烟 + 2 小时全量"当成 REPLICATION.md 的设计约束，任何超时步骤必须在文档里显式标注预计耗时。**

3. **REPLICATION.md 的正确骨架是"四段式"，且第一段必须是"论文声明清单"（list of claims）而非环境说明。** POPL 2026 逐字：*"Besides the artifact itself, we recommend your documentation contain **four sections**: A complete list of claims made by your paper / Download, installation, and sanity-testing instructions / Evaluation instructions / Additional artifact description (file structure, extending the tool or adding your own examples, etc.)"* 并给出声明清单的写法：*"The list of claims should list all claims made in the paper. For each claim, provide a reference to the claim in the paper, the portion of the artifact evaluating that claim, and the evaluation instructions for evaluating that claim."* 示例：*"Theorem 12 from Section 5.2 of the paper corresponds to the theorem 'foo' in the Coq file 'src/Blah.v' and is evaluated in Step 7 of the evaluation instructions."* **阙疑的对应写法**：把"账本第 452 条判决可复算"、"Merkle checkpoint 一致"、"盲 holdout 检出 66.7%"等每条声明映射到具体脚本与步骤号。

---

## 精确数字与案例

### 一、真实"README 空壳"率：可引用的量化基线

| 指标 | 数字 | 出处 |
|---|---|---|
| 分析论文数 | **3722 篇 MICCAI** | MICCAI 2026 paper-snitch 论文 |
| 提供代码链接比例 | **65.5%** | 同上 |
| 实际有代码比例 | **54.1%**（链接与内容差 **11.4 个百分点**） | 同上 |
| 代码链接率变化 | **51.8%（2021）→ 72.5%（2025）** | 同上 |
| 链接仓库不可访问或为空 | **~13%** | 同上 |
| 未记录任何变量的论文 | *"None of the papers document all of the variables."* | Gundersen & Kjensmo, AAAI 2018 |
| 各因子被记录变量比例 | **20%–30%** | 同上 |
| 样本 | **400 篇 IJCAI/AAAI 论文** | 同上 |

Gundersen & Kjensmo（AAAI 2018，DOI 10.1609/aaai.v32i1.11503）的摘要还有一句对本方向极重要的结论：*"The reproducibility scores decrease with increased documentation requirements."*——**文档要求越细，得分越低**。这不是"作者懒"，而是**细粒度文档成本高**。所以 REPLICATION.md 的设计目标应是"用最少字数覆盖最多被检查项"，而不是写成论文。

NeurIPS 2019 可复现性计划的三大组件（Pineau 等，JMLR 22(164):1−20, 2021，逐字）：*"The program contained three components: a code submission policy, a community-wide reproducibility challenge, and the inclusion of the **Machine Learning Reproducibility checklist** as part of the paper submission process."*——**"checklist"是这三件里唯一能直接复用为 REPLICATION.md 章节结构的**。

### 二、四段式结构（POPL 2026 逐字要求）与阙疑的映射

**第 1 段：List of claims（论文声明清单）**

官方要求逐字：*"Organize the list of claims by section and subsection of the paper."*、*"Listing each claim individually provides the reviewer with a checklist to follow during the second, evaluation phase of the process."*

| 论文声明 | 对应 artifact 部件 | 评估步骤 | 预计耗时 |
|---|---|---|---|
| 盲 holdout 30 条检出 66.7% | `fixtures/holdout_30.jsonl` + `gate_engine.py --eval-holdout` | Step 3 | ~10 秒 |
| 外部 corpus 40 条（A/B/C 三层）检出率 | `fixtures/external_corpus_40.jsonl` | Step 4 | ~10 秒 |
| 账本 452 条判决可复算 | `fixtures/ledger_452.jsonl` + `--replay` | Step 5 | <1 分钟 |
| Merkle checkpoint 一致 | `fixtures/expected_merkle_root.txt` | Step 5 | 同上 |
| 变异 core 97.3% / all 81.5% | `fixtures/mutants_core.jsonl` | Step 6 | 数分钟 |
| 独立对账器可不信任内核复算 | `verifier/` 独立脚本 | Step 7 | <1 分钟 |

**第 2 段：Download / installation / sanity-testing**

官方要求逐字：*"should contain complete instructions for obtaining a copy of the artifact and ensuring that it works. **List any software the reviewer will need (such as virtual machine host software) along with version numbers and platforms that are known to work.** Then list all files the reviewer will need to download"*；*"Your instructions should make clear **which directory to run each command from**, what output files it generates, and how to compare those output files to the paper."*

**注意三个易漏点**：① 必须写"从哪个目录执行"；② 必须写"输出什么文件"；③ 必须写"怎么把输出和论文比"。阙疑的 sanity test 建议设为：`python -c "import gate_engine; print(gate_engine.__version__)"` + `pytest -q -k smoke`，总时长 < 2 分钟。

**第 3 段：Evaluation instructions**

官方要求逐字：*"should describe how to run the complete artifact, end to end, and then evaluate each claim in the paper that the artifact supports. This section often takes the form of **a series of commands that generate evaluation data, and then a claim-by-claim list** of how to check that the evaluation data is similar to the claims in the paper."*；*"If possible, generate data in the same format and organization as in the paper: for a table, include a script that generates a similar table, and for a plot, generate a similar plot."*；*"Explicitly include commands that check soundness… **Explain any checks that fail.**"*

**"Explain any checks that fail"是极容易被忽略的一条**。对阙疑而言，反事实算子 P = R = F1 = 0（已知硬伤）、sanitizer 本机缺失，都必须在 REPLICATION.md 里**显式写明"这一步预期失败，原因是 X"**，而不是让审稿人自己撞上。

**第 4 段：Additional artifact description**

官方要求逐字：*"should explain how the artifact is organized, which scripts and source files correspond to which experiments and components in the paper, and how reviewers can try their own inputs to the artifact."* 阙疑对应：给出 `gate_engine.py`（3826 行）的模块划分、67 条规则（block 44 / warn 16 / advice 7）的存放路径、9 个保护器的位置、452 条账本的 schema。

### 三、必须显式写明的"预期偏差"（最容易被漏掉的一段）

POPL 2026 给出一个可直接套用的句式，逐字：*"**Indicate how similar you expect the artifact results to be.** Program speed usually differs in a virtual machine, and this may lead to, for example, more timeouts. Indicate how many you expect."* 官方示例逐字：*"The paper claims 970/1031 benchmarks pass (claim 5). Because the program runs slower in a virtual machine, more benchmarks time out, so as few as **930** may pass."*

**这是"容忍度声明"的标准写法：给论文值 + 给可接受下界 + 给原因。** 阙疑应写类似：*"The paper claims 66.7% detection on the 30-item blind holdout (claim 1). Because Python hash randomization and library patch versions may alter rule evaluation order in a small number of cases, as few as 63.3% (19/30) may be observed. The Merkle root, however, must match exactly."* ——**注意区分"可容差量"（检出率）与"必须精确量"（账本哈希）**，这与方向 21 的结论一致。

### 四、常见遗漏（综合 POPL 2026 + AEADataEditor 模板 + MICCAI 论文）

AEADataEditor 的 `replication-template`（社会科学的 AEA 数据编辑流程，被广泛借用）把必查项拆成 14 节，其中与计算类项目相关的硬项包括（逐字）：*"Software Requirements"*、*"Controlled Randomness (as necessary)"*、*"Memory, Runtime, and Storage Requirements"*、*"License for Code"*、*"List of tables and programs"*。它还有一条对复现文档的核心方法论：*"Create a list, mapping each of them to a particular program and line number within the program"*——**要求精确到行号**。

综合三个来源，REPLICATION.md 的高频遗漏项清单：

| 遗漏项 | 后果 | 依据 |
|---|---|---|
| 随机种子控制（`PYTHONHASHSEED`、`--seed`） | 结果不可复算 | AEA 模板 "Controlled Randomness" |
| 内存/运行时间/磁盘需求 | 审稿人机器跑不动 | AEA 模板 |
| 精确的软件版本（含编译器版本） | 装错版本失败 | POPL "version numbers and platforms that are known to work" |
| 每个步骤的**预计耗时** | 审稿人无法排期 | POPL "Clearly note steps that take more than a few minutes" |
| 预期偏差与容忍区间 | 微小差异被误判为失败 | POPL "Indicate how similar you expect the artifact results to be" |
| 已知失败项及原因 | 审稿人卡住 | POPL "Explain any checks that fail" |
| 输出文件与论文表格的对应关系 | 无法核对 | POPL "how to compare those output files to the paper" |
| 代码许可证 | 无法判定可否复用 | 方向 20 / AEA 模板 |
| 哪些部分是新增的、哪些是既有软件 | 复用性判定失败 | POPL "clarify which parts of the software are new for this artifact" |
| 数据集的版本与来源 | 数据漂移无法解释 | 方向 30 |
| 遥测/分析代码 | **可能破坏评审匿名性** | POPL "Do not include anything in the artifact that would compromise reviewer anonymity, such as telemetry or analytics." |
| 有危险行为的步骤未标注 | 评审环境风险 | POPL "**Boldly and explicitly flag this**" |

### 五、REPLICATION.md vs REPRODUCTION.md：命名与定位

两者常被混用，建议按以下区分（本组建议，非标准）：

| 文件名 | 定位 | 读者 |
|---|---|---|
| `REPLICATION.md` | 面向**第三方复算者**的逐步操作手册（含声明清单、命令、预期输出、容忍区间） | 审稿人 / AE 委员 / 未来研究者 |
| `REPRODUCTION.md` | 面向**作者自己**的复现记录（环境快照、失败尝试、偏差分析） | 作者 / 论文附录引用 |
| `README.md` | 面向**使用者**的入口（是什么、怎么装、怎么跑一次） | 一般用户 |

**若只能写一份，写 `REPLICATION.md`**（AE 评审直接看它）。命名上另一个细节：**部分会议/AE 会明确要求文件名**（如 AEA 要求 README 为 TXT/MD/PDF 三者之一，逐字：*"Please ensure that a ASCII (txt), Markdown (md), or PDF version of the README are available in the data and code deposit."*），投稿前须核对目标会议的 artifact 说明。

---

## 对阙疑的 3 条具体行动

1. **2026-12 前写出 `REPLICATION.md`，严格按四段式，且第一段是声明表**。骨架：
   - `## 1. Claims and where to verify them` —— 表格列（Claim / Paper location / Artifact component / Step / Expected runtime / Tolerance）。至少覆盖 6 条声明（盲 holdout 66.7%、外部 corpus 三层检出率、账本 452 条可复算、Merkle root 一致、变异 core/all、独立对账器复算）。**Merkle root 一行必须写 `Tolerance: exact match required`**；
   - `## 2. Download, install, sanity test (target: ≤ 30 min)` —— 写清 OS 与版本、Docker/uv 版本、`git clone` 后 `cd` 到哪个目录、`docker build` 命令、冒烟命令 `pytest -q -k smoke` 与其预期输出行；
   - `## 3. Evaluation (target: ≤ 2 hours)` —— 逐条命令 + 每条的输出文件路径 + 与论文表 N 的比对方式；**在末尾专设 `### Known failing or degraded checks` 一节**，显式列出：(i) 反事实算子 P = R = F1 = 0（说明这是已知待修项，非复现失败）；(ii) 本机 sanitizer 缺失（说明改用 Docker 后已解决，或标注仍不可用）；(iii) 变异率不作为缺陷检测率使用的理由；
   - `## 4. Artifact structure` —— `gate_engine.py`（3826 行）模块图、67 条规则与 9 个保护器的路径、账本 schema、fixtures 清单。
   - 开头加一行免责/安全声明：`No telemetry, no network access at runtime, no analytics. All commands are read-only except for writes under ./out/.`

2. **2027-01 前完成"30 分钟冒烟 + 2 小时全量"的实测校准，并把数字写回文档**。做法：找一台干净机器（或全新 Docker 容器 + 空缓存），**掐表**执行第 2、3 段全部命令，记录：① 冒烟测试实际耗时；② 全量评估实际耗时；③ 任何超过 2 分钟的步骤。**若全量 > 2 小时**，按 POPL 官方建议降级：把重活（变异 core 97.3% 的完整重跑）改为提供**预生成的输出 + 校验脚本**，并额外录制一段 screencast（官方逐字建议 *"consider an alternative artifact format, like a screencast"*）。同时在 README 与 REPLICATION.md 顶部各加一行实测耗时声明。

3. **2027-03 前把 REPLICATION.md 与"AE 通过率漏斗"绑定，并在论文 Threats to Validity 里引用外部基线**。具体：(i) 在 `research/` 下新增 `26_replication_doc.md`，记录本文档的四个来源基线——MICCAI 2026 的 **3722 篇 / 65.5% 有链接 / 54.1% 有代码 / ~13% 空壳**、Gundersen & Kjensmo 的 **400 篇 / 20–30% 变量被记录 / 无一篇记录全部**、Pineau 等 JMLR 2021 的三组件、POPL 2026 的 **30 分钟 / 几小时 / 2-3 工作日**；(ii) 在论文里写一句实证定位："据 MICCAI 2026 对 3722 篇论文的分析，仅 54.1% 提供实际可用的代码；本文提供的 artifact 通过 `REPLICATION.md` 的声明-步骤映射与 CI 断言（见方向 25）达到可逐条核验的程度。" (iii) 提交前用 MICCAI 那篇论文的检查表精神做一次自查：**仓库是否非空、是否非私有、是否含许可证、是否含依赖规格（`requirements.lock` / `uv.lock`）、是否含可运行入口、是否含预期输出**——这六项正是 paper-snitch 的 code 分支检查维度。

---

## 盲区（诚实标注）

- **MICCAI 2026 论文（paper-snitch）是会议论文 PDF，本组读取的是作者版，未见同行评审最终定稿**；其 3722 篇的统计口径（如何判定"有实际代码"）本组未逐字读到方法细节。
- **`~13%` 前的波浪号说明这是近似值**；原文写的是 "∼13% of linked repositories are inaccessible or empty"，**未给出精确分子分母**。
- **POPL 2026 的 "half hour" / "a few hours" / "2-3 workdays" 是 AE 主席的经验性建议（原文以 "Aim for" / "In our experience" 表述），不是硬性规则**，且是 PL 会议（偏证明与工具）而非 ML 会议，向 NeurIPS E&D 外推需谨慎。
- **AEADataEditor 的 REPLICATION.md 模板是"审稿人填写的复现报告模板"，不是"作者填写的复现说明模板"**。本组在报告中引用其检查项（Software Requirements / Controlled Randomness / Memory-Runtime-Storage / License for Code）时做了用途迁移，**这是本组的解读，非模板原意**，引用时须注明。
- **Pineau 等 JMLR 2021 的具体数字未逐字获取**：本组只取到摘要与三组件描述，**未读到该文中的代码提交率、checklist 采纳率等具体百分比**。若论文要引用具体数字，须另取全文。
- **Gundersen & Kjensmo 的"20%–30%"是"每个因子被记录的变量比例"**，不是"论文可复现率"，**引用时极易被误读**，须写全口径。
- **未核实**：NeurIPS 2026 E&D 是否要求特定文件名（`REPLICATION.md` / `REPRODUCTION.md` / `README.md`）。方向 20 的检索只取到 E&D 的通用代码要求（*"documented and executable"*），**未见到对复现文档文件名的规定**。
- **"REPLICATION.md vs REPRODUCTION.md 的三分法"是本组提出的建议，无外部依据**，不可作为引用。
- 未核实：POPL 2026 之外，NeurIPS E&D、ICLR、ACL 各自的 AE 时间预算是多少（本组只逐字取了 POPL）。
- **MICCAI 论文中的成本数字（GPT-4o **$0.23**/篇、GPT-5 **$0.43**/篇）与本方向无直接关系**，此处不展开，但在方向 31/后续可能有用。

---

## 来源

1. The paper has a GitHub, the GitHub has a README, the README has nothing: Reproducibility Signals for Review Support — https://papers.miccai.org/miccai-2026/paper/0729_paper.pdf — 逐字：*"Our analysis of 3722 MICCAI papers shows code-linking rising from 51.8% (2021) to 72.5% (2025), but ∼13% of linked repositories are inaccessible or empty."*；*"Overall, 65.5% provide links, only 54.1% have actual code"*；*"promise a release 'after acceptance' that never materializes in the camera-ready"*；*"a repository link that is empty, private, missing critical components, or contains little more than a placeholder README"*；工具 paper-snitch 的三类检查（20 paper criteria / 10 dataset criteria / 6 code components）与人在环一致性（Code 90.70% 一致率 / MCC 0.81；Paper 77.54% / 0.57；Dataset 72.22% / 0.29；Global 80.40% / 0.60，GPT-4o）— Federico Bolelli, Davide Santoli, Kevin Marchesini, Luca Lumetti, Costantino Grana，University of Modena and Reggio Emilia — MICCAI 2026
2. POPL 2026 Artifact Evaluation — https://popl26.sigplan.org/track/POPL-2026-artifact-evaluation — 逐字：四段式文档要求；*"you should expect to spend at least 2-3 workdays packaging your artifact"*；*"Aim for the download, installation, and sanity-testing instructions to be completable in about a half hour."*；*"Aim for the evaluation instructions to take no more than a few hours… consider an alternative artifact format, like a screencast."*；*"Indicate how similar you expect the artifact results to be."* 与 970/1031→930 的示例；*"Explicitly include commands that check soundness… Explain any checks that fail."*；*"Do not include anything in the artifact that would compromise reviewer anonymity, such as telemetry or analytics."*；*"Boldly and explicitly flag this"*；三个 ACM 徽章定义；*"Available… not the same as putting the code on GitHub, GitLab, BitBucket, or your personal website!"*；VirtualBox 7.1 / Ubuntu 20.04 LTS 建议 — ACM SIGPLAN — 2026（时间线为 2025-10 提交、2025-11 评审）
3. AEADataEditor replication-template / REPLICATION.md — https://github.com/AEADataEditor/replication-template/blob/master/REPLICATION.md — 14 节结构；逐字检查项 *"Software Requirements"*、*"Controlled Randomness (as necessary)"*、*"Memory, Runtime, and Storage Requirements"*、*"License for Code (Optional, but recommended)"*、*"List of tables and programs"*；*"Create a list, mapping each of them to a particular program and line number within the program"*；复现分类（full reproduction / full reproduction with minor issues / partial reproduction / not able to reproduce）；失败原因分类（`Discrepancy in output` / `Bugs in code` / `Code missing` / `Code not functional` / `Software not available to replicator` / `Insufficient time available to replicator` / `Insufficient computing resources available to replicator` / `Data missing` / `Data not available` / `Missing README`）；复现者环境清单模板（Mac M2 / RedCloud / CCSS Cloud / BioHPC / WholeTale / CodeOcean / Bitbucket Pipelines / Codespaces / SIVACOR）— AEA Data Editor 团队 — 持续更新
4. State of the Art: Reproducibility in Artificial Intelligence — https://ojs.aaai.org/index.php/AAAI/article/view/11503 — 逐字：*"A total of 400 research papers from the conference series IJCAI and AAAI have been surveyed using the metrics."*；*"None of the papers document all of the variables."*；*"between 20% and 30% of the variables for each factor are documented"*；*"The reproducibility scores decrease with increased documentation requirements."*；三因子 Experiment / Data / Method — Odd Erik Gundersen, Sigbjørn Kjensmo，NTNU — AAAI 2018，DOI 10.1609/aaai.v32i1.11503
5. Improving Reproducibility in Machine Learning Research (A Report from the NeurIPS 2019 Reproducibility Program) — https://jmlr.org/papers/v22/20-303.html — 逐字：*"The program contained three components: a code submission policy, a community-wide reproducibility challenge, and the inclusion of the Machine Learning Reproducibility checklist as part of the paper submission process."* — Joelle Pineau, Philippe Vincent-Lamarre, Koustuv Sinha, Vincent Larivière, Alina Beygelzimer, Florence d'Alché-Buc, Emily Fox, Hugo Larochelle — JMLR 22(164):1−20, 2021
6. NeurIPS Paper Checklist Guidelines — https://neurips.cc/public/guides/PaperChecklist — Q4/Q5/Q6/Q12/Q13/Q16 的逐字措辞（方向 20 已引） — NeurIPS — 持续更新
7. NeurIPS 2026 Evaluations & Datasets Track Call for Papers — https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets — 逐字：*"Code should be documented and executable."* — NeurIPS — 2026
8. MICCAI Paper Submission Guidelines for Reproducible Research — https://conferences.miccai.org/2025/en/PAPER-SUBMISSION-GUIDELINES.html#reproducibleresearch — 经 paper-snitch 论文引用为 [18]（20 paper criteria / 10 dataset criteria 的来源） — MICCAI — 2025（**本组未直读该页**）
9. GitIngest — https://gitingest.com/ — *"Turn any Git Repository into a Prompt-friendly Text Digest"* — 经 paper-snitch 论文引用为 [4]（**第三方工具**）
10. Reproducibility — PyTorch documentation — https://docs.pytorch.org/docs/main/notes/randomness.html — 逐字：*"there are some steps you can take to limit the number of sources of nondeterministic behavior"* — PyTorch 项目 — 2026-05-14（**作为"随机性必须显式控制"的通用参考**）
11. Keras reproducibility recipes — https://github.com/keras-team/keras-io/blob/master/examples/keras_recipes/md/reproducibility_recipes.md — *"Since `tf.config.experimental.enable_op_determinism()` is enabled and we set random seeds using `keras.utils.set_random_seed`"* — Keras 团队 — 未标注日期（**作为"种子设置须写进文档"的示例**）
12. Reproduce Research Workflows — AM-Bench Documentation — https://ambench.github.io/docs/evaluation/reproduce/ — *"Reproduction in AM-Bench means preserving the full data, policy, environment, and evaluation configuration"* — AM-Bench — 2026-09-18（**第三方**）
13. Measuring Reproducibility in LLM Research: A Rubric and Cross-Topic Corpus Study — https://dl.acm.org/doi/10.1145/3820002.3828584 — *"This paper addresses this need by conducting a venue-based, topic-aware reproducibility study of LLM-related research."*；覆盖六类（foundation models, alignment, retrieval-augmented …） — ACM — 2026（**仅取到摘要，具体百分比未核实**）
14. awesome-readme — https://github.com/matiassingers/awesome-readme — README 优秀范例合集（*"images, screenshots, GIFs, text formatting"*） — 社区 — 持续更新（**通用 README 参考，非复现专用**）
