# llm_eval — LLM 评估公开数据集

本目录存放 699-B 收集的 LLM-as-judge 数据集相关文件。

## 内容

- `download_llm_eval.py` — 在可联网环境重跑即可取**全量**真实样本并写出 `data/699_llm_eval_unified_format.json`。
- 统一格式样本本体在仓库 `data/699_llm_eval_unified_format.json`（本批已落盘 **240 条真实抽样**）。

## 数据集清单（详见 `data/699_llm_evaluation_datasets.md`）

| 数据集 | 用途 | 许可证 | 链接 |
|--------|------|--------|------|
| JudgeBench | 多 judge / 多模型对比人类标签 | 需复核 | https://huggingface.co/datasets/ScalerLab/JudgeBench |
| RewardBench | 偏好对 / 长度偏置 | ODC-BY | https://huggingface.co/datasets/allenai/reward-bench |
| MT-Bench | 多轮评判 / prompt 改写 | CC-BY/lmsys | https://huggingface.co/datasets/lmsys/mt_bench_human_judgments |
| AlpacaEval | 胜率 / 长度校正 | MIT/CC | https://github.com/tatsu-lab/alpaca_eval |

## 统一格式 schema

```json
{
  "id": "JB-<pair_id> | RB-<id>",
  "source_dataset": "JudgeBench | RewardBench",
  "prompt": "<问题/指令>",
  "response": null,            // pairwise 数据集无单回答
  "response_A": "<回答A>",
  "response_B": "<回答B>",
  "response_model": "<生成模型>",
  "source_subset": "<子集/来源>",
  "human_ground_truth": "A|B 或 A>B|B>A (人类偏好侧)",
  "judge_verdicts": {}         // 由 tools/compute_699_llm_drift.py 在 LLM 裁判可用时填充
}
```

## 已知偏差

- RewardBench 的 chosen 被策展为"更好且更长"，长度是其构造上的混淆变量（见 699-C 报告：长度裁判一致率 1.0）。
- JudgeBench 困难样本多，长度裁判一致率仅 0.44 → 长度是最强但最错的代理（结构性 Goodhart）。
- JudgeBench 许可证在可检索来源未明示，发表前须确认。
