# PAP 预注册（D4）

> 门禁：`G-PAP-REGISTERED`（L0）；工具 `tools/pap_register_671g.py`；
> 目录 `data/671g/pap/`（5 份事后补注 + registry）；红路径 `tests/test_d4_pap_671g.py`。

## 为什么

"先看结果再定分析方案"是评估过拟合总入口：看到 87.5% 好看就只报盲测口径、看到 p 不显著就换分母。
PAP 要求**跑实验之前**把 14 项钉死：

1. research_question  2. hypothesis  3. sample_size  4. statistical_method  5. alpha
6. exclusion_criteria  7. variable_definitions  8. analysis_pipeline  9. expected_results
10. data_source  11. code_version  12. rules_version  13. environment  14. registered_at

## 规则

* require 清单（`registry.require`）里的每个实验批次必须有有效 PAP；
* 14 字段缺一/为空 ⇒ block；alpha 必须是 (0,1) 数值，纯描述/区间批次显式写"不适用"；
* **预注册必须早于实验开始**（registered_at ≤ experiment_start），否则 block；
* 已完成实验允许**事后补注册**，但 `registration_type=posthoc` + `posthoc_note`
  （为什么事后、是否可能受结果影响）——事后 PAP **不享受预注册可信度**，不许冒充；
* PAP 与结果分离存放，补注册不得回填"预期结果"去贴结果。

## 本批事后补注册（5 份，标 posthoc）

`pap_holdout-reveal / pap_corpus-reveal / pap_mutation-656 / pap_counterfactual / pap_defect-injection-661`，
全部 `posthoc`，只按各批次**冻结协议**回填方案字段，不修改结果数字。**新实验必须先预注册再跑。**

## 用法

```bash
python tools/pap_register_671g.py --new BATCH                 # 生成模板（预注册）
python tools/pap_register_671g.py --new BATCH --posthoc       # 事后补注册
python tools/pap_register_671g.py --check
```
