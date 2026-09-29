# 方向 05：ICSE / ASE / FSE 的 E&D track 对比

## 核心结论
1. ICSE / ASE / FSE 没有名为"E&D"的 track，但有等价的 **Artifact Evaluation（制品评测）** 机制 + 多个"benchmark/dataset/tool"类投稿渠道；对 QueYi（一个 C++ 验证**系统**）而言，这些 SE 顶会往往比 ML 的 NeurIPS 更对口。
2. 关键差异：NeurIPS E&D 看重"数据集/基准的贡献与透明度"；SE 顶会（尤其 ICSE/ASE/FSE 的 *Dataset/Tool/Resource* 类）看重"可运行 artifact 的可用性、可复现、对社区的基础设施价值"——QueYi 的 813 行内核 + GitHub 可直接满足。
3. 对双非单人作者，SE 顶会的 *Tool/Demo* 类稿（如 ICSE Tool Demonstration、ASE Tool）门槛相对友好，且 artifact 评测有"可用/可复现"分级徽章，是**先拿一个 SE 顶会 artifact 徽章、再投 NeurIPS** 的稳妥路径。

## 精确数字与案例
- **ICSE**：设独立 **Artifact Evaluation** track（如 ICSE 2022 artifact-evaluation），对每个接收论文的制品打 "available / functional / reusable" 三级徽章；另有 *Software Engineering in Practice*、*Tool Demonstration* 等渠道。
- **ASE**：有 **Tool** 投稿类别（演示可运行工具）与 artifact 评测；ASE 接收率约 20–25%（行业估算，以官方 fact sheet 为准）。
- **FSE**：设 *Artifact Evaluation* + *Reproducibility* 关注；FSE 也有 *Demo* 类。
- **接收率锚点（行业估算，需官方确认）**：ICSE ~20%、ASE ~22%、FSE ~25%；均低于 NeurIPS 主会议但高于其竞争烈度（因受众更专）。
- **QueYi 最匹配处**：
  - ICSE *Dataset/Tool*：QueYi 是"知识验证基准 + 工具"，可投 Tool/Demo；
  - ASE *Tool*：C++ 静态/PBT 验证工具直接对口；
  - FSE *Reproducibility*：append-only 哈希链天然满足可复现审计。

## 对阙疑的 3 条具体行动
1. **双轨投稿策略**：先用 QueYi 投 **ASE Tool / ICSE Tool Demo**（门槛低、要可运行 artifact），拿 artifact 徽章 + 会议曝光；再以"扩展为基准"的版本投 **NeurIPS E&D 2027**。先用 SE 顶会背书，破双非无人识。
2. **准备 artifact 包**：按 ICSE artifact 三级标准（available: 代码在 GitHub；functional: 一条命令跑通 demo；reusable: 文档允许他人扩展 corpus）整理 QueYi，存 `supplementary/artifact.md`。
3. **在 NeurIPS 稿里引用 SE 对标**：related work 列 ICSE/ASE 的 benchmark/tool 论文，说明 QueYi 与它们的差异（可审计哈希链 + 四态判决），展示你懂 SE 社区规范。

## 盲区（诚实标注）
- ICSE/ASE/FSE 的精确接收率、2026/2027 具体 track 名称来自行业记忆，未逐篇核对官方 CFP；应抓各会 2026/2027 官网确认 *Tool/Dataset* 渠道与 artifact 评审细则。
- "SE 顶会比 NeurIPS 对口"是我的判断；若 QueYi 强调"LLM 评测"则 NeurIPS 更对口，需按最终 framing 决定主投会场。
- artifact 徽章的具体评审表单（functional/reusable 判据）需读 ICSE 2026 artifact-evaluation 官网。

## 来源
- [1] ICSE 2022 Artifact Evaluation — https://conf.researchr.org/track/icse-2022/icse-2022-artifact-evaluation
- [2] ICSE D&B 近似渠道 — https://conf.researchr.org/home/icse-2026
- [3] ASE Tool/Dataset — https://conf.researchr.org/home/ase-2026
- [4] FSE Artifact/Reproducibility — https://conf.researchr.org/home/fse-2026
- [5] CrashJS 基准（MSR 2024，SE 基准范例）— https://homepages.ecs.vuw.ac.nz/~craig/publications/msr2024-oliver.pdf
