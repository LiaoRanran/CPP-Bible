# 方向 18：Croissant 元数据怎么写（E&D 强制的机器可读数据集描述）

## 核心结论

1. **NeurIPS 2026 E&D 把 Croissant 元数据从"推荐"升级为"数据集投稿的强制要求"，且必须同时含 core 与 RAI 两类字段，否则可能 desk-reject。** 官方 E&D Hosting Guidelines（2026）逐字：*"Authors of datasets are **required** to make their datasets available along with Croissant machine-readable metadata (core and RAI)."* 且补充：*"After submissions are closed, if your Croissant file is invalid or if your data is not accessible, your submission may be desk-rejected."* NeurIPS 官方博客（2026-05-04，*Responsible AI metadata requirements for the E&D Track*）进一步说明：*"we are introducing a new requirement for dataset submissions to include machine-readable Croissant metadata that captures both the core dataset description and Responsible AI (RAI) documentation."*

2. **Croissant 是基于 schema.org 的高层数据集格式，由 MLCommons 维护，已被 Hugging Face、OpenML、Kaggle、Dataverse 等平台原生支持；它用 JSON-LD 描述"数据分布在哪、记录集长什么样、字段含义是什么"三层结构。** 官方规范（docs.mlcommons.org，2026-07-15 更新）定义三大核心组件：`distribution`（数据文件/URL）、`recordSet`（表格/记录的 schema）、`field`（每个字段的类型与描述）。对阙疑而言，它的 452 条判决账本、盲 holdout 30、外部 corpus 40、变异 core/all 都要描述成 Croissant 的 recordSet，否则 E&D 投稿在格式关就掉队。

3. **RAI 扩展是本次新增的"合规重头戏"，字段覆盖数据收集方式、收集类型、是否含个人敏感信息、偏见与限制等，且这些字段在 NeurIPS 评审里是"责任 AI"的显性证据。** Croissant RAI 规范（docs.mlcommons.org/croissant-rai-spec，2024-03-06）定义了如 `dataCollection`、`dataCollectionType`、`personalSensitiveInformation`、`dataBiases`、`annotationGuideline`、`ethicalConsiderations` 等字段。对阙疑（判定 C++ 知识卡真伪）而言，最关键的是如实声明：数据集**不含个人敏感信息**（`personalSensitiveInformation: "none"`）、收集类型（`dataCollectionType: "created"` 或 `derived`）、已知偏见（如 corpus 40 的算术不自洽 A/B/C 三层偏差）。

---

## 精确数字与案例

### 一、NeurIPS 2026 E&D 对 Croissant 的硬性时间线与触发条件

来自 E&D Call for Papers、Hosting Guidelines、官方博客三处交叉验证：

| 条款 | 逐字原文 | 对阙疑含义 |
|---|---|---|
| 触发 | E&D CFP：*"If your data is hosted on one of the preferred platforms (Kaggle, OpenML, Hugging Face, Dataverse), a Croissant metadata file is …"* | 选 HF/OpenML/Kaggle/Dataverse 任一即需 Croissant |
| 强制 | Hosting：*"Authors of datasets are **required** to make their datasets available along with Croissant machine-readable metadata (core and RAI)."* | core + RAI 两类都要 |
| 惩罚 | Hosting：*"if your Croissant file is invalid or if your data is not accessible, your submission may be desk-rejected."* | 格式错/不可达 = desk-reject |
| 新增 | 博客 2026-05-04：*"introducing a new requirement for dataset submissions to include … Croissant metadata that captures both the core dataset description and Responsible AI (RAI) documentation."* | 2026 新加 RAI |
| 平台配额 | Hosting：Dataverse 1TB/2.5GB-per-file、Kaggle 200GB、HF 300GB、OpenML 200GB | 选平台看体量 |

**关键时间点**：E&D FAQ 要求数据与代码在 **2026-05-06 (AoE)** 前以最终形态提交；Croissant 文件若投稿关闭后被判 invalid 或数据不可达，即触发 desk-reject。**阙疑的 2027 投稿应把 Croissant 当作"数据集投稿的入场券"，而不是事后补丁。**

### 二、Croissant core 的三层结构与 schema.org 根基

Croissant 论文（arXiv:2403.19546v2，2024-05-30，MLCommons）说明其设计：*"Croissant … combines metadata, resource file descriptions, and ML-specific features into a single file"*，且 *"builds on schema.org, and its Dataset vocabulary"*。官方规范定义：

- **`@type: Dataset`** 根对象，含 `name`、`description`、`creator`、`license`（推荐 SPDX URL，方向 20 已展开）。
- **`distribution`**（一个或多个）：描述数据**物理位置**——`contentUrl`（文件/API URL）、`encodingFormat`（如 `application/jsonlines`）、`contentSize`。阙疑的 `fixtures/ledger_452.jsonl` 即一个 distribution。
- **`recordSet`**（一个或多个）：描述**逻辑结构**——`field` 数组，每个 field 有 `name`、`description`、`dataType`（`http://schema.org/Text`、`Integer`、`Float`、`Boolean` 等）。阙疑账本的字段（claim_text / verdict / rule_id / timestamp / digest）写成 recordSet。
- **`data` / ML 扩展**：可选 `ml:preprocessing`、`ml:split`（`train`/`test`/`validation`）——对阙疑的 holdout 30 / corpus 40 分层尤其有用（标注 `ml:split: "test"`）。

**对阙疑的落地形态**：一个 `croissant.json` 包含 4 个 recordSet（账本 452 / holdout 30 / corpus 40 / mutants），每个带 SPDX license（`Apache-2.0`），distribution 指向匿名镜像的相对路径。

### 三、Croissant RAI 扩展字段清单（合规核心）

Croissant RAI 规范（docs.mlcommons.org/croissant-rai-spec，2024-03-06）把 Responsible AI 拆成若干维度，关键字段（节选，带可写值）：

| RAI 字段 | 含义 | 阙疑应填 |
|---|---|---|
| `dataCollection` | 数据如何被收集 | 描述四态判决 + 抓取/人工标注流程 |
| `dataCollectionType` | `created` / `derived` / `provided` / `generated` / `mined` / `unknown` | `derived`（从公开 C++ 文档派生知识卡）+ `created`（人工校验） |
| `personalSensitiveInformation` | 是否含 PII | `none`（C++ 知识卡不含个人信息） |
| `dataBiases` | 已知偏见 | corpus 40 的 A/B/C 三层算术不自洽（A 54.2%/B 12.5%/C 0%） |
| `annotationGuideline` | 标注规范 | 四态判决准则文件链接 |
| `ethicalConsiderations` | 伦理考量 | 误判知识卡的影响边界声明 |
| `isConsent` / `consentProcedures` | 同意流程 | `false`（无人类受试者） |
| `sensitivePII` | 敏感 PII 细分 | `none` |

规范原文强调 RAI 是 *"one of the main instruments to operationalise RAI is dataset documentation"*，即**把"负责任"落到可机器校验的字段上**。示例中（amazon-science/application-eval-data 的 croissant.json）可见 `"rai:personalSensitiveInformation": "The data associates each product with an identity group…"` —— 说明该字段接受自由文本描述。

### 四、工具链：怎么生成与校验 Croissant

- **mlcroissant Python 库**（MLCommons 官方）：可 `pip install mlcroissant` 后用 `croissant` CLI 校验 JSON-LD 是否符合规范（`croissant validate`）。这是投稿前自检"会不会被 desk-reject"的最低成本工具。
- **Croissant Baker**（lcp.mit.edu/croissant-baker）：MIT 提供的带 UI 的编辑/校验器，支持 RAI 字段录入。
- **平台原生支持**：Hugging Face 数据集页自动读取 Croissant；OpenML、Kaggle、Dataverse 亦支持。投 E&D 时若选这些平台，Croissant 可由平台半自动生成，但仍需人工补 RAI 字段。
- **匿名性注意**：Croissant 的 `creator` 字段若写真实作者名，会破坏双盲（方向 19）。E&D 双盲期应将 creator 写为匿名团队或留占位，待录用后回填。

### 五、Croissant 与"数据集即 artifact"的关系

E&D 的定位（来自 CFP）：*"evaluation itself becomes an object of scientific study"*，且明确 *"Submissions need not introduce a new model or outperform prior work"*。这意味着**阙疑作为"知识验证 benchmark/dataset"完全符合赛道精神**——而 Croissant 正是这种 "dataset-as-artifact" 的官方标准化入口。把数据描述清楚（core）+ 把责任声明清楚（RAI），等于把论文的"可复现/可审计"卖点**前置到了元数据层**，让审稿人/AC 在打开仓库前就能机器校验。

---

## 对阙疑的 3 条具体行动

1. **2026-12 前用 `mlcroissant` 库生成 `croissant.json`，覆盖 4 个 recordSet（账本 452 / holdout 30 / corpus 40 / mutants），core + RAI 全字段填齐，并用 `croissant validate` 通过。** 具体字段：4 个 `distribution` 指向匿名镜像相对路径（`application/jsonlines`）、每个 recordSet 的 `field` 写全（verdict 用 `http://schema.org/Text` + 枚举描述、digest 用 `Text`）、`license` 写 SPDX `https://spdx.org/licenses/Apache-2.0.html`；RAI 至少填 `dataCollectionType: ["derived","created"]`、`personalSensitiveInformation: "none"`、`dataBiases` 写 corpus 40 的 A/B/C 三层算术不自洽。理由：E&D Hosting 逐字"required … core and RAI"，invalid 即可能 desk-reject。

2. **2027-01 前把 Croissant 接入投稿平台并做"双盲 + 可达"双校验。** 选 Hugging Face 或 OpenML 托管 fixtures（配额 HF 300GB / OpenML 200GB 足够），上传后确认 Croissant 被平台解析、`creator` 字段为匿名占位（方向 19 配合）；本地再跑一次 `croissant validate` 确认无 warning。** 同时把 `croissant.json` 放进匿名 GitHub 镜像根目录（方向 19），保证 reviewer 打开即见机器可读元数据。理由：FAQ 要求数据与代码在投稿时即最终形态；双盲期 creator 泄露会触发匿名性违规。

3. **2027-03 前在论文 `Dataset / Artifact` 小节显式引用 Croissant 的 RAI 字段作为"责任 AI"证据，并在 `research/` 新增 `18_croissant.md` 记录字段映射表。** 内容：(i) recordSet ↔ 论文表 N 的字段对照；(ii) RAI 字段逐条填值依据（尤其 `dataBiases` 对应 corpus 40 的 43.8% 检出与 A/B/C 偏差）；(iii) 校验命令与通过截图。** 这把"元数据合规"从"格式门槛"提升为"论文论证资产"（呼应 E&D "evaluation as object of study" 的精神）。

---

## 盲区（诚实标注）

- **NeurIPS 官方博客 2026-05-04 的具体逐字引文（"introducing a new requirement…"）来自检索摘要，未逐字打开正文核对**；本组引用其存在性与"core+RAI 强制"结论，具体措辞建议提交前用 WebFetch 复核。
- **Croissant RAI 字段的完整清单（官方规范列了约 20+ 字段）本组只节选了与阙疑最相关的 8 个**，其余字段（如 `collectingOrgs`、`dataLicenses`、`ratings`）未逐一核实是否 E&D 强制。
- **未核实**：E&D 是否强制要求 `ml:split` 标注（训练/测试划分）。对 holdout 30 的"盲"属性，若 Croissant 能表达"held-out"语义会更有力，但规范支持度未逐字确认。
- **`personalSensitiveInformation: "none"` 的合规判定**：C++ 知识卡理论上不含 PII，但若 corpus 40 含从论坛抓取的代码片段含用户名，可能构成 PII——**此点本组未对 corpus 40 做 PII 扫描**，属待办。
- **mlcroissant 的 `validate` 命令实际报错形态与修复路径未实操验证**（仅知库存在），提交前需实跑一次确认。
- **Croissant 论文 arXiv:2403.19546v2 的具体引用格式/作者未逐字抓取**（仅取到标题与日期），引用时建议用 arXiv 编号。
- **未核实**：NeurIPS 2026 之前年份的 E&D/Datasets 是否也要求 Croissant（本组只取到 2026 年的强制表述），向 2027 投稿时规则可能再次微调。

---

## 来源

1. NeurIPS 2026 Evaluations & Datasets Hosting Guidelines — https://neurips.cc/Conferences/2026/EvaluationsDatasetsHosting — 逐字：*"Authors of datasets are required to make their datasets available along with Croissant machine-readable metadata (core and RAI)."*；*"if your Croissant file is invalid or if your data is not accessible, your submission may be desk-rejected."*；平台配额 Dataverse 1TB / Kaggle 200GB / HF 300GB / OpenML 200GB — NeurIPS — 2026
2. Responsible AI metadata requirements for the E&D Track (NeurIPS 2026) — https://blog.neurips.cc/2026/05/04/responsible-ai-metadata-requirements-for-the-evaluations-and-datasets-track-neurips-2026/ — 逐字：*"introducing a new requirement for dataset submissions to include machine-readable Croissant metadata that captures both the core dataset description and Responsible AI (RAI) documentation."* — NeurIPS — 2026-05-04
3. NeurIPS 2026 Evaluations & Datasets Call for Papers — https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets — 逐字：*"If your data is hosted on one of the preferred platforms (Kaggle, OpenML, Hugging Face, Dataverse), a Croissant metadata file is …"* — NeurIPS — 2026
4. Croissant Format Specification — https://docs.mlcommons.org/croissant/docs/croissant-spec.html — distribution / recordSet / field / ml:split 定义；基于 schema.org Dataset — MLCommons — 2026-07-15
5. Croissant RAI Specification — https://docs.mlcommons.org/croissant/docs/croissant-rai-spec.html — dataCollection / dataCollectionType / personalSensitiveInformation / dataBiases / annotationGuideline / ethicalConsiderations 等字段 — MLCommons — 2024-03-06
6. Croissant: A Metadata Format for ML-Ready Datasets — https://arxiv.org/html/2403.19546v2 — 逐字：*"combines metadata, resource file descriptions, and ML-specific features into a single file"*；*"builds on schema.org, and its Dataset vocabulary"* — MLCommons 等 — 2024-05-30
7. mlcroissant (Python library) — https://github.com/mlcommons/croissant — `croissant validate` CLI；官方校验工具 — MLCommons — 持续更新
8. Croissant Baker (RAI editor) — https://lcp.mit.edu/croissant-baker/user-guide/rai/ — 带 UI 的 RAI 字段编辑/校验器 — MIT — 2026-07-05
9. example croissant.json with RAI — https://github.com/amazon-science/application-eval-data/blob/main/croissant.json — 实测 `"rai:personalSensitiveInformation"` 写法示例 — Amazon Science — 持续更新
10. NeurIPS 2026 E&D FAQ — https://neurips.cc/Conferences/2026/EvaluationsDatasetsFAQ — 数据/代码最终形态提交期限 2026-05-06 AoE；匿名账户要求 — NeurIPS — 2026-04-07
