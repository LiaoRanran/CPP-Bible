# 702 · 投稿材料清单（Submission Checklist）

> 目标：把"投稿需要什么"列成一张表，每项标注 **已有 / 待做 / 负责人**。
> 负责人默认为论文作者（Liao Ran / 廖冉）。状态以 2026-10-09 仓库现状为准。

---

## 一、投稿核心材料

| # | 材料 | 位置 / 状态 | 已有/待做 | 负责人 | 备注 |
|---:|---|---|---|---|---|
| 1 | 论文正文（匿名版 TeX） | `research/latex/queyi_neurips2027_v1.1.tex` | 已有（匿名 notice 已置 "Under review"） | 作者 | 编译匿名 PDF 为待做 |
| 2 | 论文 PDF（匿名） | 需从 TeX 编译 | **待做** | 作者 | tectonic 编译；确认无作者/机构泄露 |
| 3 | Cover Letter | `research/latex/cover_letter.tex` v1.7 | 已有（已检查通过） | 作者 | 见 `702_cover_letter_check.md` |
| 4 | 摘要（229 词，据 692） | 论文内 | 已有 | 作者 | 与 cover letter 题名一致 |
| 5 | Rebuttal 弹药库 | `data/697_rebuttal_arsenal_v2.md`（最新） | 已有 | 作者 | 见 `702_rebuttal_index.md` |

---

## 二、补充材料（代码 + 数据）

| # | 材料 | 位置 | 已有/待做 | 负责人 | 备注 |
|---:|---|---|---|---|---|
| 6 | 复现脚本 | `tools/verify_paper_numbers.py`、`gen_693_manifest.py` 等 | 已有 | 作者 | fail-loud、带 `--check` |
| 7 | 一键复现 | `Scripts/reproduce_all.sh` | 已有 | 作者 | Docker 镜像**未实测构建** |
| 8 | 1147×8 冻结矩阵 | `data/blindspot_676g_detection_matrix.json` | 已有 | 作者 | 数字对账源 |
| 9 | 真实靶场 110×8 | `data/683_real_world_detection_matrix.json` | 已有 | 作者 | 109/109 NVD 验证 |
| 10 | 人类标注材料包 | `data/annotation_package/` + `data/702_annotation_table.csv` | 已有（本批优化） | 作者/协调者 | 145 盲标 + 31 裁决，未执行 |
| 11 | 机器可读元数据 | `data/croissant.json`、`data/rai_metadata.json` | 已有 | 作者 | Croissant 1.0 + RAI 1.0 官方校验通过 |
| 12 | 数据卡 | `data/holdout_expansion/DATASHEET.md` | 已有 | 作者 | 口径见 `SCHEMA.md` |

---

## 三、声明类（易漏，重点）

| # | 材料 | 状态 | 已有/待做 | 负责人 | 备注 |
|---:|---|---|---|---|---|
| 13 | 数据可用性声明（Data Availability Statement） | 部分 | **待补/确认** | 作者 | 应在论文或补充材料显式声明数据集 + 代码可获取方式（Apache-2.0 + GitHub 已满足，但需一句话声明） |
| 14 | 伦理声明（Ethics Statement） | **待做** | **待做** | 作者 | 涉及**人类标注者**（同学）——需说明自愿参与、知情同意、匿名/署名选项、无报酬；NeurIPS E&D 要求 ethics statement |
| 15 | 匿名化声明 | 部分 | **待做** | 作者 | 确认正文/补充材料/数据中无作者名、机构、可反推线索 |
| 16 | 利益冲突声明 | 隐含 | **待确认** | 作者 | 独立无基金研究，需一句话 |
| 17 | 计算资源/可复现环境声明 | 已有 | 已有 | 作者 | WSL-bound 主档案、Docker 未实测（诚实声明已写入） |

---

## 四、投稿前最后检查

见 `data/702_pre_submission_checklist.md`（匿名化 / 数字 / TODO / 引用 / 编译 逐项打勾）。

---

## 状态汇总

- **已有且就绪**：1, 3, 4, 6, 7, 8, 9, 10, 11, 12, 17
- **待编译产出**：2（匿名 PDF）
- **待补声明（高优先）**：13（数据可用性）、14（伦理）、15（匿名化核对）
- **待确认措辞**：全仓"Evolving Verifiers"旧题名、旧"three contributions"措辞（见 `702_pre_submission_checklist.md`）

> 本清单为**快照**，非最终决定。负责人字段为默认建议，实际以作者安排为准。
