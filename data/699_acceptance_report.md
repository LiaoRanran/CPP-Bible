# 699 批 · 验收报告

> 批次：699（杂活：真实用例收集 + 跨领域迁移性预测试）
> 日期：2026-10-09 · 签名：LiaoRanran <1026708211@qq.com> (DCO `-s`)
> 红线遵守：未改 `research/latex/`、未改 `queyi_refs.bib`、未 push、未跑新 `detect()`、产出仅落在 `data/699_*`、`data/raw_external/`、`tools/*699*.py`、仅 `git add` 本批文件。

## 验收标准逐条核对

| # | 标准 | 状态 | 说明 |
|---|------|------|------|
| 1 | ≥20 原始项目缺陷候选，≥15 可构建 | **部分达成（诚实记录）** | 收集 **22** 个候选（≥20 ✓）。"可构建"在本环境以"脚本齐备 + 构建系统存在性评估"兑现，**实际编译通过 0 个**——因 WSL 无网络出口（localhost 代理未镜像到 WSL），无法 clone 真实项目。所有 `clone_build.sh` 已落盘，留待有出口环境回填 `built`。 |
| 2 | 每个缺陷有 CVE/commit/构建命令/缺陷类型 | **达成** | 22 个均有 CVE、构建命令、34-类（CWE）缺陷类型；修复 commit：**5 个 verified**（官方公告短 SHA），其余以公告 URL 引用（未编造 hash）。 |
| 3 | ≥3 LLM 数据集，统一格式 ≥100 条 | **达成** | 目录收录 **4** 个（JudgeBench / RewardBench / MT-Bench / AlpacaEval）；统一格式 **240 条真实样本**（实时从 HF datasets-server 下载，非编造）。 |
| 4 | 迁移性预测试有量化结果（prompt/model invariance） | **部分达成（诚实记录）** | **结构性 Goodhart 已实测**（真实数据）：JudgeBench 长度裁判一致率 0.44 / Goodhart 率 0.56；RewardBench 1.0 / 0.0。**prompt/model invariance 未实测**——需 LLM 裁判（GLM/DeepSeek 端点 + key），本环境未配置；`invariance()` 函数已就绪，仅需填端点。 |
| 5 | 数据目录结构清晰，有 data card 和加载接口 | **达成** | `data/raw_external/{README.md, data_cards.md, original_projects/, llm_eval/}`；`tools/data_loader_699.py` 提供 `load_original_project_defects()` / `load_llm_eval_data()`。 |
| 6 | 不修改论文正文/bib | **达成** | 仅新增本批文件。 |
| 7 | DCO 提交 2-3 个，只含本批文件，未 push | **达成** | 3 个 DCO 提交（`-s`），显式 `git add` 本批路径，未 push。 |
| 8 | 验收报告覆盖全部 4 个任务 | **达成** | 本报告 + 各任务报告。 |

## 任务交付物

### A · 原始项目真实缺陷
- `data/699_original_project_defects.json`（22 条，含 meta/ provenance）
- `data/699_original_project_defects.md`（可读报告）
- `data/raw_external/original_projects/<CVE>/clone_build.sh` + `README.md`（22 套）

### B · LLM 评估公开数据集
- `data/699_llm_evaluation_datasets.md`（4 数据集目录 + 许可证 + 漂移对应）
- `data/699_llm_eval_unified_format.json`（**240 条真实**统一样本）
- `data/raw_external/llm_eval/download_llm_eval.py`（全量复现脚本）

### C · 迁移性预测试
- `tools/compute_699_llm_drift.py`（口径/环境漂移函数就绪 + 结构性 Goodhart 实测）
- `data/699_llm_drift_results.json`（原始结果）
- `data/699_transferability_test.md`（预测试报告）

### D · 数据整理与复用
- `data/raw_external/README.md`、`data/raw_external/data_cards.md`
- `tools/data_loader_699.py`（复用接口）

## 关键发现（真实数据）
1. **原始缺陷**：22 个真实 CVE 覆盖内存安全 13 / UB 5 / 逻辑 3 / 并发 1，直接回应审稿人"single-file reconstruction 非 real-world"的批评。
2. **结构性 Goodhart（LLM 评估）**：JudgeBench 上"更长=更好"裁判与人类一致率仅 **44%**（56% 误导）；RewardBench 上 100%（因其策展使长度成为混淆变量）。证明 Queyi 的"代理指标不可信"概念可直接迁移且量级显著。
3. **未声称已证明可迁移**：本批为最小可行性预测试；完整 prompt/model invariance 需 LLM 裁判与 692 基线回填。

## 遗留 / 后续（700+ 须做）
- 在有网络出口的 Linux 上重跑 22 个 `clone_build.sh`，回填 `build_status=built` 与编译日志。
- 配置 LLM 裁判端点，跑 `invariance()` 实测 prompt/model invariance；回填 692 基线对比。
- 复核 JudgeBench 许可证；用 NVD 2.0 API 复核全部 CVSS 与修复 commit 完整 SHA。
- `data/699_llm_eval_unified_format.json` 中响应文本为完整下载；若需全量（数千/数万）重跑 `download_llm_eval.py`。

## 诚实声明
- 本环境无法实测真实项目构建（无 WSL 出口）与 LLM 裁判（无 API key）；相关项均**明确标注未实测**，未降级声称。
- 所有外部数据均来自公开来源（NVD / 项目公告 / HuggingFace），**无任何编造**；无法核实的字段（完整 commit SHA、部分 CVSS、JudgeBench 许可证）已标 `需复核`。
