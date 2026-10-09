# 补充材料包（Supplementary Material）— Queyi / CPP-Bible

> 论文：`research/latex/queyi_neurips2027_v1.1.tex`（NeurIPS 2027 投稿 v1.1）
> 批次：704（大杂活批次 · 投稿前体力活）
> 本目录只汇总**既有产物**，不修改论文正文与 `queyi_refs.bib`（红线 1/2）。
> 所有数字均来自冻结矩阵 / 已落盘报告；本批**未运行任何新的 `detect()`**（红线 4）。

## 1. 这个包解决什么

论文附录已 30+ 页，实验结果散落在 `data/` 各批次报告与 `tools/` 各脚本中。审稿人拿 Supplementary Material 时需要一个「一个入口、能定位每个数字来源、能复算」的包。本包提供：

| 文件 | 作用 |
|---|---|
| `README.md` | 本文件：包说明 + 附录分组 + 文件索引 |
| `all_numbers.md` | 关键数字总表（来源批次 + 文件 + 复算状态） |
| `scripts_index.md` | `tools/` 全部脚本索引（复现关键脚本 + 745 脚本完整列表） |
| `REPRODUCTION.md` | 从零复现指南（Docker / 本地 / 最小复现） |
| `environment.yml` | 依赖清单（Python / 包 / 系统） |
| `DATA_AVAILABILITY.md` | 数据可用性声明 |
| `ETHICS.md` | 伦理声明 |
| `REPRODUCIBILITY_CHECKLIST.md` | NeurIPS 复现清单逐项回答 |
| `CONFLICT_OF_INTEREST.md` | 利益冲突声明 |
| `AUTHOR_CONTRIBUTIONS.md` | 作者贡献声明（CRediT，单作者） |

## 2. 论文附录分组（35 个 `app:*` 标签，按主题）

> 从 `queyi_neurips2027_v1.1.tex` 提取（只读）。`\appendix` 起始于 tex 第 665 行，附录正文约 1705 行。

### 理论附录（Theory / Method formalism）
| 标签 | 标题 |
|---|---|
| `app:formal` | Formal Definitions and Gate Tiers（从正文移出） |
| `app:driftalgebra` | Measurement Drift Algebra: Three-State Transition Model |
| `app:metatheory` | A metatheory: which axioms are actually independent |
| `app:samplecomplexity` | Sample complexity, and why the protocol needs a second design |
| `app:submodular687` | Submodular formulation and approximation guarantees |
| `app:ceiling687` | Adaptive selection ceiling |
| `app:noise687` | Robustness to detector noise |
| `app:counterfactual687` | Counterfactual robustness |
| `app:meta687` | Meta-evaluation framework |
| `app:stats` | Statistical Caliber（frozen） |

### 实验附录（Experiments / Empirical results）
| 标签 | 标题 |
|---|---|
| `app:a5full` | A5 at Full Scale (676f): 1137 Samples |
| `app:blindspot` | Detector Capability Boundaries (676g): a Blind-Spot Map |
| `app:bench676l` | Detector Depth Benchmark (676l): per-asset performance |
| `app:threats_quantified` | Threats to Validity, Quantified |
| `app:realworld683` | Real-World Validation (683) |
| `app:operator683` | Operator Ablation (All 16 Configurations) (683) |
| `app:toolchain683` | Toolchain Sensitivity (683) |
| `app:reframe689` | Reframing Evidence: Equivalence, Standardization, Environment and Human |
| `app:sensitivity682` | Sensitivity Analysis and Additional Figures (682) |
| `app:clangtidy` | External Tool Comparison (clang-tidy / cppcheck; details) |
| `app:persample` | Per-sample Detail |
| `app:extra` | LLM Arm and External Anchor (details) |
| `app:pinning` | Rule Pinning and e-Process (details) |
| `app:eprocess` | E-Process (exploratory) |

### 数据附录（Data / Provenance）
| 标签 | 标题 |
|---|---|
| `app:datasheet` | Dataset Provenance and Composition |
| `app:datametadata` | Data Metadata (Croissant + Responsible-AI Fields) |
| `app:tables` | Threat, Validity and Evolution Tables |
| `app:humanize` | Humanization Material (full versions; 673c) |

### 工程 / 治理附录（Engineering / Governance / Reproduction）
| 标签 | 标题 |
|---|---|
| `app:repro` | Reproduction Commands |
| `app:reproducibility` | Reproducibility: Environment, Seeds and Commands |
| `app:incidents` | Engineering Incident Log（刻意保留在正文之外） |
| `app:ai` | AI Use Statement |
| `app:related` | Related Work（九小节，v1.1 新增两节） |
| `app:future` | Future Work（remaining items） |

## 3. 复现的最小入口

```bash
# 数字对账（fail-closed，只读冻结产物）
python tools/verify_paper_numbers.py \
  --out-json data/704_verify_paper_numbers.json \
  --out-md  data/704_verify_paper_numbers_report.md

# A5 / 盲区从冻结矩阵独立重算
python tools/recompute_a5_676f.py
```

详见 `REPRODUCTION.md` 与 `scripts_index.md`（A 节）。

## 4. 诚实边界（本包不声称的）

- **不声称「完全可复现」**：本机（Windows）未安装 Docker，所有 `Dockerfile` / `docker-compose.yml` 仅通过语法与路径核验，**未实测构建**（见 `REPRODUCTION.md` §1 与 `docker/README` 头注释）。
- **真实检测链（asan/ubsan/tsan 需要 WSL g++ 13.3 + MinGW g++ 13.1）** 的端到端重跑需在宿主机完成；容器内 Linux 工具链与论文口径存在已知环境差异，仅可用于口径理解，不可翻/改结论。
- **人类 IAA 标注** 截至 703 仍为 `pending`（0 条裁决填入），是论文最大未解决项。
- 声明类文件（`DATA_AVAILABILITY.md` 等）为**模板**，作者需最终确认。
