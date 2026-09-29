# 方向 30：DVC 数据版本管理（让 fixtures 可复现、可溯源）

## 核心结论

1. **DVC 的核心思想是"用 Git 管元数据、用 DVC 管大文件"：它在 Git 里只存几 KB 的 `.dvc` 指针文件（含内容哈希与大小），把真正的 GB 级 fixtures 存在 content-addressed 缓存/远端，从而让数据集像代码一样被版本化、被 checkout 到任意历史版本。** 官方文档（DVC user guide）逐字：*"DVC does NOT replace Git! DVC's metafiles (such as dvc.yaml and .dvc files) serve as placeholders for data and ML pipelines."* 对阙疑而言，账本 452 条、holdout 30、corpus 40、mutants 这些 fixtures 一旦进 DVC，每次实验对应的数据版本就被 Git commit 锁定——论文表 N 的"66.7% / 43.8% / 97.3%"就能**精确对应某一版 fixtures**，杜绝"数据悄悄变导致结果不可复现"。

2. **DVC 与 git-lfs 的本质区别：DVC 用独立的 content-addressed object database（ODB）和任意远端（本地/S3/SSH/HF），git-lfs 用 Git 的 smudge/clean 过滤器 + 专用 LFS 服务器；DVC 额外提供 `dvc.yaml` 声明式 pipeline（数据→处理→评估的有向图），git-lfs 只做文件存储不做流程编排。** DeepWiki 的 DVC 缓存文档说明：DVC 的本地 object database（ODB）按**内容哈希**寻址（如 `cache/files/md5/ab/cdef...`），与 Git 的对象模型同构但不依赖 Git 的 LFS 协议。对阙疑：若 fixtures 不大（KB~MB 级），git-lfs 已够；但若将来扩充变异库到 GB 级或要复现"数据版本→判决"全链路，DVC 的 pipeline 能力更契合 E&D "evaluation as object of study" 的可审计诉求。

3. **数据版本化对阙疑不是"锦上添花"而是"硬需求"：盲 holdout 30 的"盲"属性、corpus 40 的 A/B/C 三层划分、mutants 的具体算子，都必须绑定到确定性版本，否则审稿人复现时会拿到"漂移后的数据"而得到不同数字。** MICCAI 2026（方向 17/26）证明"有链接却无代码/数据"是 11.4 个百分点的落差主因；而"有数据但版本不对"是更隐蔽的失败——DVC 用 `git checkout <commit> && dvc checkout` 一步还原当时数据集，正好堵这个洞。

---

## 精确数字与案例

### 一、DVC 工作原理（content-addressed 缓存 + 远端）

根据 DVC 官方用户指南与 DeepWiki 缓存文档：

| 组件 | 作用 | 阙疑对应 |
|---|---|---|
| `.dvc` 文件 | 小指针（~几百字节），含 `md5`/`etag`、`size`、`outs` 路径 | 每个 fixture 一个 `.dvc` |
| **ODB（object database）** | content-addressed 缓存，路径形如 `cache/files/md5/ab/cdef...` | 本地 `./.dvc/cache` |
| `dvc remote` | 远端存储：local / SSH / S3 / GCS / Azure / HF 等 | 匿名镜像站或 HF 数据集 |
| `dvc.yaml` | 声明式 pipeline（stage: 数据准备→评估→产出） | 定义"fixtures→gate_engine→判决" |
| `dvc.lock` | pipeline 各阶段输入/输出哈希快照 | 锁定某次评估的数据+代码版本 |

**关键点**：`.dvc` 与 `dvc.yaml`/`dvc.lock` 都是**纯文本、进 Git**，所以"数据版本"随 Git commit 自然版本化；真正的二进制只在缓存/远端，不污染 Git 历史（避免方向 28 讨论的"大文件撑爆仓库"）。

### 二、DVC vs git-lfs 逐项对比

| 维度 | DVC | git-lfs |
|---|---|---|
| 存储机制 | 独立 ODB + 任意远端 | Git smudge/clean + LFS 服务器 |
| Git 历史 | 只存 `.dvc` 指针（KB 级） | 只存 LFS 指针（KB 级） |
| Pipeline | **有**（`dvc.yaml` 有向图） | 无 |
| 实验追踪 | `dvc exp` 实验分支 | 无原生 |
| 远端灵活性 | S3/SSH/local/HF/阿里云等 | 需 LFS 服务器（GitHub LFS/自建） |
| 适用规模 | MB~TB | MB~GB（受 LFS 配额限制） |
| 学习成本 | 较高（概念多） | 低（透明替换） |

**结论取向**：阙疑当前 fixtures 体量小（JSONL，KB~MB），git-lfs 或 DVC 都行；但鉴于 E&D 强调"评估可审计 + 数据版本绑定结果"，**DVC 的 `dvc.yaml` pipeline 能把"喂哪版数据 → 跑哪个规则集 → 出哪个判决"固化成可复算图**，比 git-lfs 单纯存文件更契合论文卖点。若不想引入 DVC 复杂度，最低方案是"fixtures 直接进 Git（因体积小）+ 在 `dvc.yaml` 等价物里写清版本号"——但 DVC 仍是首选。

### 三、DVC 实操命令（阙疑适配）

```bash
# 1. 初始化（项目根）
dvc init

# 2. 跟踪 fixtures（生成 .dvc 指针，真文件进缓存）
dvc add fixtures/ledger_452.jsonl
dvc add fixtures/holdout_30.jsonl
dvc add fixtures/corpus_40.jsonl
dvc add fixtures/mutants_core.jsonl

# 3. 配置远端（匿名期用本地/HF，录用后可换永久）
dvc remote add -d myremote /path/to/anon-mirror/data
# 或 dvc remote add -d hfremote https://huggingface.co/datasets/<anon>/queyi

# 4. 推送数据到远端
dvc push

# 5. 在 Git 里提交指针（数据版本被 commit 锁定）
git add fixtures/*.dvc .dvc/config .gitignore
git commit -m "lock fixtures v1: ledger452/holdout30/corpus40/mutants"

# 6. 审稿人复现：一键还原当时数据
git clone <anon-repo> && cd queyi && dvc pull && dvc checkout
python gate_engine.py --replay fixtures/ledger_452.jsonl
```

### 四、与 Croissant / 匿名化的衔接（方向 18/19）

- **Croissant 描述"有哪些数据"**：`croissant.json` 的 `distribution.contentUrl` 指向 DVC 远端或匿名镜像的相对路径（方向 18）。DVC 保证"那个 URL 在特定 commit 下内容确定"。
- **匿名期远端**：DVC remote 在双盲期应指向匿名镜像/HF 匿名数据集，避免暴露作者（方向 19）；录用后改 remote 指向正式永久存储。
- **完整性**：DVC 的 content-addressed 缓存天然带哈希，**与阙疑账本的 Merkle root / 哈希链（方向 anchor）同构**——可以写一句论文论证："数据版本用内容哈希寻址（DVC ODB），判决用 Merkle checkpoint，二者共同构成端到端不可篡改的证据链"。

### 五、数据版本化的"隐蔽失败"防范

MICCAI 2026 揭示的是"无数据/空链接"的显性失败；更隐蔽的是"**数据版本漂移**"：

- 作者本地改了 corpus 40 的标注却忘了 `dvc add` + commit → 论文写 43.8% 但评审拿到的是 44.1%。
- 规则集（`rules/`）与 fixtures 版本不匹配 → 同一数据不同结果。
- **DVC 的解法**：`dvc.lock` 把"数据哈希 + 代码哈希 + 产出哈希"绑定；评审 `dvc repro` 会校验输入是否变化，若有漂移会重算或报警。这直接服务 E&D 的"判决可复算"卖点。

---

## 对阙疑的 3 条具体行动

1. **2026-12 前 `dvc init` 并把 4 个 fixtures（ledger_452 / holdout_30 / corpus_40 / mutants）纳入 DVC 跟踪，远端指向匿名镜像/HF 匿名数据集，提交 `.dvc` 指针与 `dvc.yaml`。** 具体：`dvc add fixtures/*.jsonl` → `dvc remote add -d anonremote <匿名存储>` → `dvc push` → `git add fixtures/*.dvc .dvc/config && git commit`。在 `research/30_data_versioning.md` 记录每个 fixture 的 DVC md5 与对应论文表。** 理由：把"数据版本"锁进 Git，杜绝评审复现时的版本漂移（比 git-lfs 多一层 pipeline 可审计性）。

2. **2026-12 写 `dvc.yaml` 把"fixtures → gate_engine → 判决/哈希"声明为 pipeline，并加 `dvc.lock` 固化输入哈希。** 定义 stage：`prepare`（校验 fixtures 完整性）→ `evaluate`（跑 gate_engine 四态判决）→ `digest`（算 Merkle root 与 expected_digest.txt）。评审期用 `dvc repro` 一键重算并自动比对输入哈希是否变化。** 理由：DVC pipeline 把"喂哪版数据出哪个数"固化成图，直接支撑论文"判决可复算"的核心卖点，且比单纯 `pytest` 多一层数据完整性守卫。

3. **2027-01 前把 DVC remote 与 Croissant `distribution.contentUrl`、匿名镜像三者对齐，并保证 `git clone && dvc pull && dvc repro` 是 REPLICATION.md 里的黄金命令（方向 26）。** 即 REPLICATION.md 的不带 `--recurse-submodules` 的黄金命令（方向 29）进一步写成：*`git clone <anon> && cd queyi && dvc pull && dvc repro`*，预期产出与 `expected_digest.txt` 逐位一致（Merkle root 属"必须精确量"，方向 20/26）。** 理由：把数据版本、代码、判决三者用一条命令串起，最大化 AE 通过率漏斗的 Available→Functional→Reproduced 转化（EuroSys 161→136→75，方向 20）。

---

## 盲区（诚实标注）

- **DVC 的具体版本号与 `dvc exp`/`dvc repro` 的精确报错形态未实测**（本组仅从文档推断其行为），提交前需实跑一次 `dvc repro` 确认与现有 `gate_engine.py` 集成顺畅。
- **git-lfs 的配额限制（如 GitHub LFS 免费 1GB 存储/1GB 月流量）未逐字核实**，本组只定性说"受配额限制"，阙疑 fixtures 小故两方案皆可行。
- **"DVC ODB 路径形如 cache/files/md5/ab/cdef..."是 DeepWiki 描述，具体哈希算法（md5 还是 sha256）随 DVC 版本可能变化**；新版本 DVC 默认用 sha256，引用时须注明版本。
- **DVC remote 指向 HF 匿名数据集的实际配置步骤未实操验证**（HF 对 DVC 的支持程度未逐字确认），若该路径不通，退化为"本地远端 + 匿名镜像打包"方案。
- **未核实**：NeurIPS E&D 是否接受 DVC 作为数据托管方式（官方列的平台是 Kaggle/OpenML/HF/Dataverse，方向 18）——DVC remote 用 HF 数据集可间接满足，但纯本地 DVC remote 可能不被认可为"properly hosted"。
- **"数据版本漂移导致 43.8% vs 44.1%"是本组构造的示例数字，非实测**；阙疑目前是否有此类漂移需实跑 `dvc repro` 验证。

---

## 来源

1. DVC User Guide（官方）— https://dvc.org/doc/user-guide — 逐字：*"DVC does NOT replace Git! DVC's metafiles (such as dvc.yaml and .dvc files) serve as placeholders for data and ML pipelines."*；`.dvc` 指针含 md5/size/outs — Iterative — 持续更新
2. Cache and Object Database (DVC, DeepWiki) — https://deepwiki.com/treeverse/dvc/3.2-cache-and-object-database — content-addressed ODB；路径 `cache/files/md5/ab/cdef...`；local ODB + remote — 2025-11-27
3. 存储和获取 DVC 数据 — https://apxml.com/zh/courses/data-versioning-experiment-tracking/chapter-2-versioning-data-dvc/storing-retrieving-dvc-data — 工作区/Git/DVC 缓存/远端 交互流程 — 教程 — 持续更新
4. DVC 实战指南：像 Git 一样管理数据和模型 — https://zeeklog.com/dvc-data-version-control-xiang-gityi-yang-guan-li-ni-de-shu-ju-he-mo-xing — `.dvc` 元文件占位、remote 配置 — 2026-03-23
5. 数据版本控制终极对决：DVC 与 Git LFS — https://blog.csdn.net/gitblog_00458/article/details/153312344 — DVC 完整数据管理 vs git-lfs 最小侵入；复杂度随项目上升 — 2025-10-15
6. DVC 与 Git LFS 对比：MLOps 大文件管理 — https://blog.csdn.net/gitblog_00494/article/details/151291350 — 仓库膨胀/克隆时长对比 — 2025-09-07
7. NeurIPS 2026 E&D Hosting Guidelines — https://neurips.cc/Conferences/2026/EvaluationsDatasetsHosting — 官方托管平台 Kaggle/OpenML/HF/Dataverse（DVC 可借 HF 间接满足）— NeurIPS — 2026
8. The paper has a GitHub, the GitHub has a README… — https://papers.miccai.org/miccai-2026/paper/0729_paper.pdf — 65.5%/54.1%/~13% 空壳率（方向 17 已引）— MICCAI 2026
9. Lessons from Five Years of Artifact Evaluation at EuroSys — https://www.sigops.org/2025/lessons-from-five-years-of-artifact-evaluation-at-eurosys/ — 161/136/75 AE 漏斗（方向 20 已引）— EuroSys — 2025-08-05
10. Croissant Format Specification — https://docs.mlcommons.org/croissant/docs/croissant-spec.html — distribution.contentUrl 指向数据位置（方向 18 已引）— MLCommons — 2026-07-15
