# data/ · 数据目录说明

> 这个目录里有 **1600+ 个文件**。这一页回答：*哪个是权威数据、哪个是中间产物、改之前要注意什么。*
> 格式细节见 [`../docs/DATA_FORMAT.md`](../docs/DATA_FORMAT.md)；版本记录见 [`CHANGELOG.md`](CHANGELOG.md)。

---

## 1. 命名规范

| 形态 | 含义 | 能不能改 |
|---|---|---|
| `<批次号>_<主题>.json` / `.md` | 某批次的**产物**（如 `683_real_world_detection_matrix.json`） | ⚠ 见 §3 |
| `<批次号>_<主题>_报告.md` / `验收报告.md` | 该批次的**可读报告** | 不改（历史记录） |
| `<批次号>_<主题>.jsonl` | 逐条原始输出（如 `692_fair_comparison_raw.jsonl`） | 不改 |
| `authority/` | **权威账本**（append-only） | ❌ 只追加 |
| `holdout_expansion/` | 评测集（源 + 逐样本 JSON + SCHEMA/DATASHEET） | ⚠ 见 §3 |
| `real_world/` | 真实靶场 PoC 源文件 | ❌ |
| `annotation_package/` | 人类标注材料包（去标识化） | ⚠ 发出去前必须复核净化 |
| `prompts/` | 批次任务书（`676*_*.md`） | ❌ |
| `evidence_store/` | 证据件存储 | ❌ |

**批次号 = 时间顺序**（`609` → `693`）。数字越大越新，但**不代表更权威**：
权威性取决于该文件是否被 `tools/gen_693_manifest.py` 的清单收录。

---

## 2. 权威 vs 派生

### 权威（冻结，进 sha256 清单）

```
blindspot_676g_detection_matrix.json    1147×8 冻结检测矩阵
676m_a5_matrix_corrected.json           A5 修正矩阵
a5_676f_detection_matrix.json           A5 全量矩阵
676m_sample_manifest_corrected.json     34 类规范词表 + 样本清单
681_type_stats_normalized.json          34 类归一化统计
683_real_world_detection_matrix.json    真实靶场 110×8
683_real_world_project_matrix.json      真实靶场按项目聚合
683_real_world_type_matrix.json         真实靶场按类型聚合
684_complementarity_matrix.json         资产互补性
685_literature_matrix.json              文献对照
689_annotation_key_mapping.json         标注密钥（**不外发**）
holdout_reveal_5_672h.json              holdout reveal
external_corpus_reveal_672h.json        外部语料 reveal
authority/decision_event_v2_ledger.jsonl  452 条权威判决账本
```

校验：

```bash
python tools/gen_693_manifest.py --check     # 14 项 sha256
python tools/verify_data_integrity.py        # 存在性+结构+四态闭集+类型闭集+统计自洽
```

### 派生（可从权威重算，不入清单）

- `682_*`（敏感性）、`686_*`（反事实）、`692_*`（环境/公平对比/LLM 臂）、`693_*`（本批分析）
- `*_report.md` / `*_验收报告.md` 等可读报告
- `croissant.json` / `rai_metadata.json`（由 `tools/gen_682_metadata.py` 生成）

---

## 3. 改动纪律（红线）

1. **已冻结的矩阵不改。** 要改就在新批次里产出**新文件**，旧文件保留可追溯。
2. **`unknown` 永不折叠进 `miss`。** 这是全项目最容易误用的地方。
3. **分母必须写清。** 61.6%（分母 1147）与 94.21%（分母 674）是同一矩阵的两个合法读数。
4. **改了冻结产物 ⇒ 必须** `python tools/gen_693_manifest.py` 重生成清单，
   并在当批验收报告里写明**为什么改**。**绝不允许**为了"让校验过"而重生成清单掩盖改动。
5. **标注密钥不外发。** `689_annotation_key_mapping.json` 只给协调者；
   发给标注者的只有 `annotation_package/`。
6. **`data/prompts/` 是任务书**，不是产物，不改不删。

---

## 4. 693 批次新增

| 文件 | 内容 |
|---|---|
| `693_ai_double_label.json` | AI 双标（A=实测 / B=静态判读）：n=145、raw 78.6%、κ=0.495、31 条分歧 |
| `693_human_adjudication_package.csv` | 31 条分歧裁决表（`human_verdict` **留空**） |
| `693_annotation_guide.md` | 裁决指南（34 类 + 四态 + 边界 case） |
| `693_calibration_examples.md` | 10 条校准题 |
| `693_github_recruitment_issue.md` / `693_community_post.md` / `693_cold_email_template.md` | 招募材料 |
| `693_data_manifest.sha256` / `693_data_manifest.json` | 14 项冻结产物清单 |
| `693_data_integrity.json` | 数据完整性校验结果 |
| `693_perf_bench.json` | 数据访问性能实测 |
| `693_docker_reproduce_report.md` | 复现验证报告（含"未实测构建"登记） |
| `693_original_repo_cve*.{json,md}` | 原始项目 CVE 验证（693-E1） |
| `693_defect_type_deep_analysis.json` / `693_defect_type_report.md` | 缺陷类型深度分析（693-E2） |
| `693_detectability_model.{json,md}` | 可检测性预测模型（693-E3） |
| `693_counterfactual_extended.json` / `693_counterfactual_report.md` | 反事实扩展（693-E4） |
| `693_meta_evaluation_v2.json` / `693_meta_evaluation_report.md` | 元评估 v2（693-E5） |
| `693_related_work_update.md` | 相关工作更新（693-E6） |
| `693_paper_revision_suggestions.md` | 论文修改建议（693-E7） |
| `693_超大批次验收报告.md` | 本批验收报告 |
