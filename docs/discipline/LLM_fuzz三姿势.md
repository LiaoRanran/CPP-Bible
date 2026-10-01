# LLM fuzz 三姿势（D5 框架）

> 工具 `tools/llm_fuzz_671g.py`（**框架，本批不接 LLM API**）；测试 `tests/test_d5_llm_fuzz_671g.py`。
> 实际调用需 API key/网络，留待后续批次；框架只钉死三姿势的**协议/数据流/判定**。

## 三姿势（真值从不来自 LLM）

| 姿势 | 流程 | 真值来源 |
|---|---|---|
| 1 缺陷发现 | LLM 生成 C++ 代码 → **sanitizer 当 oracle**（asan/ubsan/tsan，-O0/-O2 双档） | oracle 命中=defect |
| 2 变异杀死 | LLM 生成变异体 → 验证器检测 | killed=catch；并入变异杀死率 |
| 3 反事实 | LLM 生成反事实 case → 验证器判决 → **人工标注真值** | 人工 original_holds/falls |

共同纪律：

* LLM 只提供**待判材料**，不自标真值（姿势1 oracle、姿势3 人工）；
* 姿势3 无人工真值 ⇒ **quarantined**，不得进数据集；
* 所有 LLM 批次产物必须过 `G-LLM-CHANNEL`（见 LLM通道安全.md）与 `G-POISON-DETECT`（见 投毒检测.md）；
* 批次落 `data/671g/llm_batches/*.json`，带 source_tag + 四项 defense 证据。

## 用法

```bash
python tools/llm_fuzz_671g.py --posture 1 --code-file x.cpp --sanitizer asan
python tools/llm_fuzz_671g.py --posture 2 --items mutants.json
python tools/llm_fuzz_671g.py --posture 3 --items cf_cases.json
```
未接 runner/验证器时只返回 `framework_only/quarantined`，**不臆标**。
