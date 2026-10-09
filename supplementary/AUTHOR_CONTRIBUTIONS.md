# 作者贡献声明（Author Contributions — CRediT）

**论文：** Queyi: 零成本静态感知的 C++ 缺陷检测资产选择
**单一作者：** Ran Liao（廖冉）/ 合肥大学人工智能与大数据学院

> 本论文由**单一作者**完成。以下按 CRediT（Contributor Roles Taxonomy）14 项角色逐项如实填写。
> 因仅一位作者，**全部角色均为该作者主导（Led by）**。涉及"人类协作"的角色（如 Supervision 下的他人指导、人类标注）如实标注为**无**。

| CRediT 角色 | 贡献说明 | 状态 |
|---|---|---|
| **Conceptualization**（构思） | 提出"零成本静态感知的资产选择"核心问题、研究假设与方法框架 | Led by R. Liao |
| **Data curation**（数据管理） | 设计 1147 样本语料结构；生成构造夹具；重构 110 真实 CVE 最小复现集 | Led by R. Liao |
| **Formal analysis**（形式分析） | A5 统计检验（McNemar p、95% CI）、盲区率、环境感知、κ 一致性分析 | Led by R. Liao |
| **Funding acquisition**（经费获取） | 无外部资助 | **无（None）** |
| **Investigation**（调研） | 系统化梳理 8 类检测资产、环境画像、静默退化机制 | Led by R. Liao |
| **Methodology**（方法论） | 资产选择算法、环境感知校正协议、零成本验证框架（P1–P3） | Led by R. Liao |
| **Project administration**（项目管理） | 批次调度（676f–703）、冻结产物治理、红线纪律执行 | Led by R. Liao |
| **Resources**（资源） | 提供计算环境（WSL2 + g++/clang/sanitizers）、数据集与代码托管 | Led by R. Liao |
| **Software**（软件） | 全部 `tools/*.py` 复算/审计/标注脚本、Docker 配置、最小复现脚本 | Led by R. Liao |
| **Supervision**（监督指导） | 无外部导师/合作者监督 | **无（None）** |
| **Validation**（验证） | 冻结产物审计、`verify_paper_numbers.py` 130 条数字溯源、抽样复算 | Led by R. Liao |
| **Visualization**（可视化） | 论文图表、补充材料表格、盲区/环境感知可视化 | Led by R. Liao |
| **Writing – original draft**（初稿） | 全文撰写 | Led by R. Liao |
| **Writing – review & editing**（修订） | 全文审校、证据分级、口径统一、诚实局限登记 | Led by R. Liao |

## 标注相关的诚实披露

- **缺陷标注**由 AI 第二遍标注器（source-evidence annotator）完成，**非人类专家标注**。因此：
  - "Data curation"中的标注环节由 AI 辅助，作者负责设计标注协议与质量校验。
  - 全仓库**人类标注一致性（human IAA）= 0**，论文已如实陈述，未冒称人类专家一致性。
- 所有需署名的学术贡献均出自作者本人；生成式 AI 仅作研究辅助，不构成作者身份。

## 署名与通信

- **第一作者 / 通讯作者：** Ran Liao（廖冉）
- **所属机构：** School of Artificial Intelligence and Big Data, Hefei University
- **投稿邮箱：** 1026708211@qq.com
