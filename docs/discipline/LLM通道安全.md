# LLM 通道安全（D8，四类攻击面防御）

> 门禁：`G-LLM-CHANNEL`（L0；无 LLM 批次时 unarmed，只 warn）；
> 工具 `tools/llm_channel_defense_671g.py`；批次目录 `data/671g/llm_batches/`；
> 测试 `tests/test_d8_llm_channel_671g.py`。

## 四类攻击面与防线

| 攻击面 | 防线 | 实现 |
|---|---|---|
| 提示注入 | 输入过滤 + 输出校验 | `input_filter`（"ignore previous/你现在是/泄露系统提示"等模式，中英）；`output_validate`（非空、不回显 system 片段） |
| 数据投毒 | canary + 配对反事实探针 | 批次必须带 `defense_checks.canary_pass / pair_consistent_pass`（判决在 投毒检测.md） |
| 模型窃取 | 限流 + 输出水印 | 同 key 相邻请求间隔不得小于配置（默认 1s）；输出带来源标记（queyi/阙疑/generated-by-llm） |
| 评估污染 | 训练/测试 id 不相交 | `evaluate_overlap(train_ids, test_ids)` 必须无交集（配合 评估过拟合防御.md 三分离） |

## 批次格式（`data/671g/llm_batches/<id>.json`）

```json
{"batch_id": "...", "llm_prompt": "...", "llm_output": "...", "source_tag": "queyi ...",
 "defense_checks": {"canary_pass": true, "pair_consistent_pass": true},
 "train_ids": [], "test_ids": []}
```

四项任一不过 ⇒ 该批次 block，不得进数据集。无批次目录 ⇒ warn（如实登记"当前无 LLM 数据通道"，
有批次即强制）。

## 用法

```bash
python tools/llm_channel_defense_671g.py --check
cat input.txt | python tools/llm_channel_defense_671g.py --scan-input -
```
