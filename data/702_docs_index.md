# 702 · docs/ 文档索引（Docs Index）

> 目的：把 `docs/` 下 86 个文件按主题分组为 **入门 / 教程 / 参考 / 开发**，方便开源后读者与协作者快速定位。
> 生成方式：脚本扫描 `docs/*.md` + `docs/*.html`（排除子目录 `adr/ assets/ figures/ kernel/ references/ discipline/ 669_调研消化/`）。
> 检查时间：2026-10-09。

---

## 总览

| 分组 | 数量 | 用途 |
|---|---:|---|
| 入门 Getting Started | 9 | 第一次来的人读这些 |
| 教程 Tutorials | 7 | 怎么编译/复现/做内容 |
| 参考 Reference | 34 | 规格、矩阵、形式化规范、可视化 |
| 开发 Dev / Batch Reports | 36 | 各批次验收/复盘/质量检查报告 |
| **合计** | **86** | （另含 7 个子目录，未展开） |

> 子目录（未计入上表）：`adr/`（架构决策记录）、`assets/`（图片）、`figures/`、`kernel/`、`references/`、`discipline/`、`669_调研消化/`。这些多为内部资产，README 不必逐一链接。

---

## 入门 Getting Started（9）

- `docs/GETTING_STARTED.md` — 三步跑通入口
- `docs/README_v2.md` — 文档版 README
- `docs/项目介绍.md` — 项目定位
- `docs/ARCHITECTURE.md` — 系统架构
- `docs/ENVIRONMENT.md` — 环境锁定（含 WSL UTF-16LE 横幅坑）
- `docs/FAQ.md` — 常见问题
- `docs/REPO_METADATA_696.md` — 仓库元数据
- `docs/index.html` — 文档站首页
- `docs/about.html` — 关于页

## 教程 Tutorials（7）

- `docs/论文LaTeX编译验证.md` — 论文编译验证流程
- `docs/演示脚本.md` — 演示脚本
- `docs/video_script_683.md` — 视频脚本（683）
- `docs/content_humanize_playbook.md` — 内容人味增强手册
- `docs/content_writing_analysis.md` — 内容写作分析
- `docs/pytest_two_phase.md` — pytest 两阶段说明
- `docs/工程建设后续任务.md` — 后续工程任务

## 参考 Reference（34）

**数据与治理**
- `docs/DATA_FORMAT.md`、`docs/DATA_GOVERNANCE_696.md`、`docs/ENGINEERING_696.md`、`docs/EXPERIMENTS.md`
- `docs/S6_tool_debt.md`、`docs/SUPREME_ENGINEERING_SPECIFICATION.md`

**规格与形式化**
- `docs/verdict_formal_spec_v1.md`、`docs/verdict_extension.md`、`docs/tool_interface_spec_645.md`
- `docs/trace_layer_spec_658.md`、`docs/trace_layer_665.md`、`docs/trace_layer_prototype_660.md`

**矩阵 / 门禁 / 度量**
- `docs/compiler-matrix.md`、`docs/gate_tiers_658.md`、`docs/metric_layers_658.md`、`docs/caliber_convergence_658.md`

**边界 / 适配 / 迁移**
- `docs/boundary_scope_split_658.md`、`docs/core_rust_boundary_656.md`、`docs/trust_termination_656.md`
- `docs/embedded_adaptation_647.md`、`docs/c_domain_adaptation_647.md`、`docs/migration_647.md`
- `docs/repo_split_final_plan_647.md`、`docs/targeting_plan_647.md`
- `docs/evidence_dual_axis.md`、`docs/pck_c2pa_mapping.md`、`docs/uvk_manifesto.md`

**可视化（HTML）**
- `docs/data.html`、`docs/demo.html`、`docs/paper.html`、`docs/realworld.html`
- `docs/reproduce.html`、`docs/results.html`、`docs/learning_path_viz.html`

## 开发 Dev / Batch Reports（36）

**前端 / 可视化批次**：`666_frontend.md`、`667_frontend.md`、`667_全量复盘.md`、`667_回溯反思.md`、`667_究极大规划.md`、`670c_前端完成度.md`、`670c2_前端状态审计.md`

**CI / 门禁 / 复现**：`668_ci_triage.md`、`669_fast_triage.md`、`669_实验结果.md`、`669d_corpus差异根因.md`、`669d_gate_report.md`、`669d_复现审计.md`、`669d_门禁真实性.md`、`670a_实验结果.md`、`670c_verifier_failures.md`、`670c_verifier_双仓绿.md`、`670c_前端完成度.md`、`independent_generation_658.md`

**调研 / 批判**：`671c_调研启发挖掘.md`、`671f_调研继续消化.md`、`673c_人味增强清单.md`、`673c_红队批判报告.md`

**G5_MEM 质量检查**：`G5_MEM_batch_acceptance_report.md`、`G5_MEM_batch_quality_inspection.md`、`G5_MEM_batch2_quality_inspection.md`、`G5_MEM_batch4_PERFO03_quality_inspection.md`、`G5_MEM_batch4_acceptance_report.md`、`G5_MEM_batch5_quality_inspection.md`

**论文质量清单**：`论文写作质量清单.md`、`论文引用纠错清单.md`、`论文数字纠错清单.md`、`论文逻辑纠错清单.md`、`论文首创性增强清单.md`

**其他验收**：`acceptance_665.md`、`figure1_665.md`、`human_review_item_by_item_process.md`

---

## 改进建议（给 README / 文档维护者）

1. **README §4 项目结构**里 `docs/` 仅写了 "`ENVIRONMENT.md`（环境锁定）与研究报告"，未体现本索引的 4 分组——建议补一句"见 `data/702_docs_index.md`"或在 README 内嵌分组。
2. **大量批次报告（36 个）** 对新读者是噪音；建议在 README 或 docs 首页提供"只看入门 9 篇"的精简路径。
3. **HTML 可视化**（7 个）与 Markdown 内容混放，建议在 README §4 区分"文档"与"交互式报告"。
4. 子目录 `adr/`（架构决策记录）应被 README 引用——ADR 是开源协作的关键资产，当前 README 未提。

> 本索引为**快照**，由脚本生成；新增/重命名文档后重跑脚本即可更新。
