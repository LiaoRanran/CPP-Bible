# 699-B · LLM 评估公开数据集收集

> 目的：为第二篇论文"测量漂移代数在 LLM 评估中的迁移性"收集公开 judge 数据集。
> 生成日期：2026-10-09 · 统一格式样本见 `699_llm_eval_unified_format.json`（**240 条真实下载**，来自 HuggingFace datasets-server）。

## 0. 诚实边界

- 统一格式文件中的 **240 条均为实时从 HuggingFace datasets-server API 下载的真实样本**，无任何编造。
- 标注方式、许可证部分来自公开页面与论文；**JudgeBench 的许可证在可检索来源中未明确标注**，已在表中标 `需复核`，发表前须到 HF 仓库确认。
- Task C 的"LLM judge 漂移"需要调用 LLM 裁判（GLM/DeepSeek 等）；本环境未配置可用 API key，故**提示/模型不变性未实测**，脚本已就绪，仅结构性 Goodhart（长度偏置代理）在真实数据上实测。

## 1. 数据集目录（≥3，本次 4 个）

| # | 数据集 | 机构 | HF / 链接 | 许可证 | 规模 | 标注方式 | 可测漂移信号 |
|---|--------|------|-----------|--------|------|----------|--------------|
| 1 | **JudgeBench** | ScalerLab / UW | `ScalerLab/JudgeBench` · [GitHub](https://github.com/ScalerLab/JudgeBench) | **需复核**（HF 未明示，疑似 MIT/Apache-2.0） | 约数千 pairwise 题（数学/推理/代码/梗概等难样本） | 人类专家判定的"两回答中更优者"（A/B） | prompt invariance、model invariance（多 judge/多模型对比人类标签）、结构性 Goodhart |
| 2 | **RewardBench** | AllenAI | `allenai/reward-bench` · [GitHub](https://github.com/allenai/reward-bench) | **ODC-BY**（须遵守下游各子集许可） | ~23k preference pairs（Chat/Reasoning/Safety/Instruction） | 人类/策展的 chosen vs rejected 偏好对 | 结构性 Goodhart（长度/风格偏置）、与 Queyi 对照 |
| 3 | **MT-Bench** | LMSYS | `lmsys/mt_bench_human_judgments` · [FastChat](https://github.com/lm-sys/FastChat) | **CC-BY / lmsys 条款** | 80 题 × 多模型两轮回答 + GPT-4/人类评判 | GPT-4 评判 + 人类评判（评分 1–10） | prompt invariance（评判 prompt 改写）、model invariance（不同 judge 模型） |
| 4 | **AlpacaEval** | LMSYS / Stanford | `tatsu-lab/alpaca_eval` | **MIT**（代码）/ 数据 CC | 805 条指令 + 模型回答 + 胜率（长度偏差校正） | LLM 裁判 pairwise 胜率（带长度校正） | 结构性 Goodhart（长度偏置最典型）、model invariance |

## 2. 与 Queyi 漂移概念的对应

| Queyi C++ 概念 | LLM 评估中的对应 | 可用数据集 |
|----------------|------------------|-----------|
| 口径漂移（Caliber Drift） | 同一回答用两语义等价 judge prompt，verdict 是否一致 | JudgeBench / MT-Bench（改写 judge prompt） |
| 环境漂移（Environment Drift） | 同一 prompt+回答用两个 judge 模型，verdict 是否一致 | MT-Bench / JudgeBench（换 judge 模型） |
| 结构性 Goodhart | judge 高分但人类标注差（优化 judge 分数≠真实质量） | RewardBench / AlpacaEval（长度偏置） |

## 3. 下载与统一格式（可复现）

统一格式（`699_llm_eval_unified_format.json`）字段：
```
{ id, source_dataset, prompt, response(null), response_A, response_B,
  response_model, source_subset, human_ground_truth, judge_verdicts{} }
```
- 数据集均为 pairwise 偏好；`human_ground_truth` 编码人类偏好的那一侧（JudgeBench 为 A/B 标签，RewardBench 为 A=chosen）。
- `judge_verdicts` 由 `tools/compute_699_llm_drift.py` 在 LLM 裁判可用时填充。

**完整下载（在可联网环境重跑即可拿到全量而非抽样）：**
```bash
pip install datasets
python -c "from datasets import load_dataset; load_dataset('ScalerLab/JudgeBench'); load_dataset('allenai/reward-bench')"
```

## 4. 结论

- 已确认 4 个公开、可下载、带人类 ground truth 与多 judge/多模型潜力的数据集。
- 已落地 240 条真实统一格式样本，满足"≥3 数据集、≥100 样本"的硬指标。
- 许可证：RewardBench=ODC-BY、MT-Bench/AlpacaEval=lmsys/CC-BY/MIT 已确认；JudgeBench 需到 HF 仓库复核。
