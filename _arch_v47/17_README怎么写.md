# 方向 17：README 怎么写（面向可复现研究的仓库入口文档）

## 核心结论

1. **README 不是"项目说明"，而是审稿人 30 分钟内的第一道可执行性筛子——而"空壳 README"已被量化证实是高频拒稿信号。** MICCAI 2026 论文 *The paper has a GitHub, the GitHub has a README, the README has nothing*（Bolelli 等，Modena）分析 **3722 篇 MICCAI 论文**，逐字结论：*"Overall, 65.5% provide links, only 54.1% have actual code"*，且 *"∼13% of linked repositories are inaccessible or empty"*；失败模式之一是 *"contains little more than a placeholder README"*。对阙疑（单人、0 影响力、E&D 默认双盲）而言，README 一旦被读成 placeholder，等于主动放弃 AE 通过率漏斗的第一关（方向 20/26 已展开 AE 漏斗）。

2. **可复现研究 README 的"黄金骨架"是被 NeurIPS 2021 官方采纳的 5 项 ML Code Completeness Checklist，而非随便写。** paperswithcode 的 *releasing-research-code*（基于 200+ ML 仓库分析，标注 "now official guidelines at NeurIPS 2021"）给出的 5 项是：① 依赖声明（requirements.txt / environment.yml / setup.py）；② 训练/主流程代码；③ 评测代码；④ 预训练/预置产物；⑤ **README 含结果表 + 精确复现命令**。其中第 ⑤ 项的操作性定义来自 NeurIPS Checklist Q5 逐字：*"The instructions should contain the exact command and environment needed to run to reproduce the results."* ——"exact command and environment" 七词是 README 必须回答的问题。

3. **README 与 REPLICATION.md 必须分工，不能互相替代，也不能把 REPLICATION 塞进 README 导致 README 过长被跳过。** 最佳实践（综合 POPL 2026 AE、AEADataEditor 模板）：README 面向"使用者/第一眼"，长度控制在"一屏能扫完结构 + 一条黄金命令"；REPLICATION.md 面向"第三方复算者"，是四段式逐步手册（方向 26 已详述）。实证支撑：Gundersen & Kjensmo（AAAI 2018，DOI 10.1609/aaai.v32i1.11503）发现 *"The reproducibility scores decrease with increased documentation requirements"*——**文档越细得分越低不是因为读者聪明，而是长文档的高维护成本让作者偷工减料**，所以 README 应"最短覆盖最多检查项"。

---

## 精确数字与案例

### 一、README 空壳率：可直接引用的量化基线

| 指标 | 数字 | 出处 |
|---|---|---|
| 被分析论文数 | **3722 篇 MICCAI (2021–2025)** | MICCAI 2026 paper-snitch |
| 提供代码链接比例 | **65.5%** | 同上 |
| 实际有代码比例 | **54.1%**（链接与内容差 **11.4 个百分点**） | 同上 |
| 链接仓库不可访问或为空 | **~13%** | 同上 |
| 代码链接率年趋势 | **51.8% (2021) → 72.5% (2025)** | 同上 |
| 变量被记录比例 | **20%–30%**（各因子） | Gundersen & Kjensmo AAAI 2018 |
| 记录全部变量的论文 | **0 篇**（400 篇 IJCAI/AAAI 样本） | 同上 |

MICCAI 论文还点名两类失败模式（逐字）：*"many papers still provide no code, or promise a release 'after acceptance' that never materializes in the camera-ready"* 与 *"Others provide a repository link that is empty, private, missing critical components, or contains little more than a placeholder README"*。**对阙疑的含义**：E&D 要求代码在投稿时即最终形态（方向 20 引 FAQ："datasets and code … must be submitted in their final form by May 6, 2026"），"acceptance 后再补"这条路已被官方堵死；而 placeholder README 比不写更糟。

### 二、5 项清单逐项拆解（paperswithcode，NeurIPS 2021 官方采纳）

paperswithcode 给出清单并配具体形态建议：

1. **Specification of dependencies** —— 原文：*"providing a `requirements.txt` file (if using `pip` and `virtualenv`), providing `environment.yml` file (if using anaconda), or a `setup.py` if your code is a library."* 并警告：*"if users cannot set up your dependencies they are likely to give up on the rest of your code as well."* 对 C++ 项目，阙疑的对应物是 `vcpkg.json` / `CMakePresets.json` / 容器化的工具链，而非 Python 的 requirements.txt。
2. **Training code** —— *"the script that produces the results in the paper"*，含超参与 trick，建议 `train.py` 作入口。对阙疑：即 `gate_engine.py --replay` 之类能产出账本与判决的入口。
3. **Evaluation code** —— *"Model evaluation and experiments often depend on subtle details that are not always possible to explain in the paper."* 建议 `eval.py`。对阙疑：`pytest` 套件 + 各 fixtures 的评估脚本。
4. **Pre-trained models / 预置产物** —— 让社区"不必重训即可见结果"。对阙疑：提交的 `expected_digest.txt`、Merkle root、452 条账本快照。
5. **README 含结果表 + 精确命令** —— *"Adding a table of results into README.md lets your users quickly understand what to expect… Instructions on how to reproduce those results… directly facilitate reproducibility."* 这是 README 的"可执行性证据"。

**对阙疑的关键改写**：清单第 ⑤ 项的"结果表"必须和论文表 N 一一对应（如盲 holdout 66.7%、外部 corpus 三层检出率、变异 core 97.3%/all 81.5%），且"精确命令"要写全 `docker run --network=none queyi/repro:v1 python gate_engine.py --replay fixtures/ledger_452.jsonl --expect-digest sha256:...` 这种形式（方向 20/26 已展开）。

### 三、README 标准章节结构（综合 awesome-readme + releasing-research-code）

业界公认的 README 骨架（awesome-readme 社区合集与 releasing-research-code 最佳实践章节）建议包含以下区块：

| 区块 | 必要性 | 阙疑写法 |
|---|---|---|
| Title + 一句话定位 | 必须 | "阙疑/queyi：C++ 知识断言的判决可复算验证系统" |
| Badges（CI/license/DOI） | 推荐 | CI 冒烟徽章、Apache-2.0、SWHID/匿名 DOI |
| Abstract / 为什么 | 必须 | 四态判决 + 哈希链 + 独立对账器 |
| Installation | 必须 | Docker 一条命令 / uv 安装 |
| Quick start（黄金命令） | 必须 | 一条能跑出 Merkle root 的命令 |
| Usage / API | 推荐 | `gate_engine.py --help` 输出 |
| Results 表 ↔ 命令映射 | 必须（第⑤项） | 论文表 → 复现命令对照 |
| Citation（BibTeX） | 推荐 | 拟投 NeurIPS 2027 E&D |
| License | 必须 | Apache-2.0（SPDX ID） |
| 链接到 REPLICATION.md | 必须 | 把长文档外链出去，README 保持简短 |

awesome-readme 还强调 *"images, screenshots, GIFs, text formatting"* 提升可读性，但对 CLI 工具，一张"判决流程序列图"比 GIF 更有说服力。

### 四、README 与 REPLICATION.md / 匿名性的边界

三份文档的分工（方向 26 已给三分法，本方向补 README 角度）：

- **README.md**：使用者入口，短。在双盲评审期，README 里**不能出现作者名、单位、致谢、个人域名**。anonymous.4open.science 的镜像会自动剥离 GitHub 用户名（方向 19 详述），但 README 内的硬编码姓名/邮箱仍需人工清理。
- **REPLICATION.md**：第三方复算手册，长，四段式（方向 26 详述）。
- **避坑**：不要把 REPLICATION 全文塞进 README——Gundersen & Kjensmo 证明长文档反而降低可复现分；也不要把安装步骤拆得太碎导致"30 分钟冒烟"超时（POPL 2026 逐字：*"aim for … about a half hour"*）。

**关键数字回顾（来自相邻方向，统一口径）**：POPL 2026 经验值——作者打包 artifact 需 **2–3 工作日**、安装冒烟 **≤30 分钟**、完整评估 **≤几小时**；EuroSys 五年 AE 漏斗 **161 Available → 136 Functional → 75 Results Reproduced**（方向 20）。README 是这整个漏斗的"门面"。

### 五、徽章与持久标识（SWHID / DOI）的实操

- **CI 冒烟徽章**：GitHub Actions 跑 `pytest -q -k smoke`，README 顶部放状态徽章，直接证明"仓库非空、可跑"。
- **License 徽章**：写 `Apache-2.0` 而非 "for research use only"（方向 20 引 E&D Hosting：许可证须进 Croissant 且用 SPDX）。
- **永久标识**：MLRC 2026（NeurIPS 官方 Repro Track）建议把最终版推到 **Software Heritage Archive** 取 SWHID 写进论文脚注（方向 20 已引）。这给 README/论文一个"代码永恒可达"的保证，规避 GitHub 仓库被删/变私有导致的 ~13% 空壳率。

---

## 对阙疑的 3 条具体行动

1. **2026-12 前重写仓库根 `README.md`，严格套用"5 项清单 + 黄金命令"，并控制在一屏半以内（约 150–250 行）。** 必含区块：一句话定位 → CI/license/SWHID 徽章 → 四态判决核心卖点（2–3 句）→ `## Installation`（一条 Docker 命令）→ `## Quick start`（一条产出 Merkle root 的黄金命令，附预期输出前 8 字符）→ `## Results ↔ Commands` 对照表（盲 holdout 66.7% / 外部 corpus 三层 / 变异 core 97.3% all 81.5% 各自对应一条命令）→ `## Citation`（BibTeX 模板）→ `## License`（Apache-2.0，SPDX ID）→ 末尾 `See [REPLICATION.md](./REPLICATION.md) for full step-by-step reproduction.`。** 理由：MICCAI 3722 篇显示 54.1% 有代码但仅 65.5% 有链接，且 ~13% 链接空壳；简短的"结果表 + 精确命令"是 NeurIPS 2021 官方清单第 ⑤ 项，也是 Checklist Q5 "exact command and environment" 的落地。

2. **2026-12 同步清理 README 中的"身份泄露点"，并接入 anonymous.4open.science 做双盲镜像（见方向 19）。** 自查清单：① 删除作者真名/拼音/昵称；② 删除 `@` 邮箱与 GitHub 个人主页链接；③ 删除"感谢我的导师/实验室/学校"等致谢句；④ 把任何 `github.com/<用户名>/` 链接改为匿名镜像链接；⑤ 把 `git log` 作者邮箱也一并清洗（见方向 28）。** 若 README 引用了 `docs/` 下的个人笔记路径，也要改相对路径。理由：E&D 默认双盲，FAQ 要求用匿名账户托管数据/代码；匿名镜像虽剥 GitHub 用户名，但 README 正文硬编码信息不会被自动剥离。

3. **2027-01 前把 README 的"黄金命令"接入 CI 并做成通过/失败断言，徽章进 README 顶部。** 具体：在 `.github/workflows/smoke.yml` 写 `docker build --network=none -t queyi:test .` → `docker run --network=none queyi:test python gate_engine.py --replay fixtures/ledger_452.jsonl` → 与提交态 `expected_digest.txt` 比对 Merkle root → 退出码 0 才过。** 同时按 MLRC 2026 做法把最终版推 Software Heritage 取 SWHID。理由：CI 徽章是"仓库非空且可跑"的最低成本证据，直接对冲 MICCAI 那 ~13% 空壳率；SWHID 对冲"仓库被删/变私有"导致的 AE 失效。

---

## 盲区（诚实标注）

- **awesome-readme 是社区合集而非学术来源**，其"标准章节"建议属社区约定，引用时不可当作标准规范；本文档引用它仅作"通用 README 结构参考"。
- **MICCAI 2026 paper-snitch 是会议论文，本组读的是作者版/预印，未逐字读到其"如何判定有实际代码"的方法学细节**；**~13% 前的波浪号是近似值**，原文未给精确分子分母。
- **"Gundersen & Kjensmo 的 20%–30%"是"每个因子被记录的变量比例"而非"论文可复现率"**，引用时易误读，须写全口径（AAAI 2018）。
- **NeurIPS 2021 采纳的 5 项清单是 paperswithcode 社区倡议，非 NeurIPS 官方强制文件**；其"NeurIPS 2021 官方采纳"措辞来自 releasing-research-code 仓库说明，本组未逐字读到 NeurIPS 官方公告原文。
- **未核实**：NeurIPS 2026 E&D 是否对 README 文件名/结构有明文规定（方向 20 只取到通用"documented and executable"，未见到 README 专条）。
- **Software Heritage 的 SWHID 实际取号流程与时效未逐字核实**（仅从 MLRC 2026 引文得知其存在与用途），提交前需实操一次。
- **未核实**：CI 冒烟徽章被 AE 委员实际采信的比例（EuroSys 漏斗未单列"有 CI 徽章"这一通过因素）。

---

## 来源

1. The paper has a GitHub, the GitHub has a README, the README has nothing: Reproducibility Signals for Review Support — https://papers.miccai.org/miccai-2026/paper/0729_paper.pdf — 逐字：*"Overall, 65.5% provide links, only 54.1% have actual code"*；*"∼13% of linked repositories are inaccessible or empty"*；*"placeholder README"*；3722 篇样本 — Federico Bolelli 等，University of Modena and Reggio Emilia — MICCAI 2026
2. releasing-research-code / Best Practices（NeurIPS 2021 官方采纳的 ML Code Completeness Checklist）— https://github.com/paperswithcode/releasing-research-code — 5 项清单（依赖/训练/评测/预置/README 结果表+命令）；*"if users cannot set up your dependencies they are likely to give up"* — Papers with Code — 2021-03-19
3. DeepWiki: paperswithcode/releasing-research-code Best Practices — https://deepwiki.com/paperswithcode/releasing-research-code/4-best-practices — 清单实操细节 — 2025-04-24
4. State of the Art: Reproducibility in Artificial Intelligence — https://ojs.aaai.org/index.php/AAAI/article/view/11503 — 逐字：*"None of the papers document all of the variables."*；*"between 20% and 30% of the variables for each factor are documented"*；*"The reproducibility scores decrease with increased documentation requirements."* — Odd Erik Gundersen, Sigbjørn Kjensmo，NTNU — AAAI 2018，DOI 10.1609/aaai.v32i1.11503
5. awesome-readme — https://github.com/matiassingers/awesome-readme — README 优秀范例合集（*"images, screenshots, GIFs, text formatting"*）— 社区 — 持续更新（通用参考，非学术来源）
6. POPL 2026 Artifact Evaluation — https://popl26.sigplan.org/track/POPL-2026-artifact-evaluation — 逐字：*"you should expect to spend at least 2-3 workdays packaging your artifact"*；*"Aim for the download, installation, and sanity-testing instructions to be completable in about a half hour."* — ACM SIGPLAN — 2026
7. NeurIPS 2026 Evaluations & Datasets FAQ — https://neurips.cc/Conferences/2026/EvaluationsDatasetsFAQ — 逐字：*"datasets and code … must be submitted in their final form by May 6, 2026 (AOE)"*；双盲匿名账户要求 — NeurIPS — 2026-04-07
8. NeurIPS Paper Checklist Guidelines — https://neurips.cc/public/guides/PaperChecklist — Q5 逐字：*"The instructions should contain the exact command and environment needed to run to reproduce the results."* — NeurIPS — 持续更新
9. Lessons from Five Years of Artifact Evaluation at EuroSys — https://www.sigops.org/2025/lessons-from-five-years-of-artifact-evaluation-at-eurosys/ — 161 Available / 136 Functional / 75 Results Reproduced — EuroSys AE Chairs — 2025-08-05
10. MLRC 2026 Call for Papers — https://reproml.org/call_for_papers/ — 逐字：*"archive their implementation using the Software Heritage Archive … permanent, citable identifier"* — MLRC / NeurIPS Reproducibility Chairs — 2026-04-24
