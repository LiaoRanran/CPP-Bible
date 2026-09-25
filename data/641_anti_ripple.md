# 641 任务 0.3 · 反涟漪验证（640c §五.5）

## 一、做法

只改**一个**权威派生量：把入库产物 `data/grounded_labels_w2.json` 里
`ATOM-CONC-FENCE-001::prop-1` 的 `label` 由 `IN` 改成 `OUT`
（**不动事实源、不动任何代码**），跑受影响的 6 个测试文件（66 例），然后**还原**并复跑。

脚本：`%TEMP%\anti_ripple_641.py`（改前 `shutil.copy2` 备份，`finally` 里还原）。

## 二、结果

**改后：9 项红**（其余 57 例仍绿）

```
FAILED tests/test_w2_derived_640c.py::test_two_paths_consistent_on_real_repo
FAILED tests/test_w2_derived_640c.py::test_live_and_pinned_agree_on_key_derived_quantities
FAILED tests/test_w2_derived_640c.py::test_cli_check_passes
FAILED tests/test_argument_audit_610.py::test_authority_cross_source_consistent
FAILED tests/test_argument_audit_610.py::test_check_consistency_strict
FAILED tests/test_argument_audit_report_610.py::test_generate_full_report_sections
FAILED tests/test_611_tools.py::test_d1_out_mis_review
FAILED tests/test_611_tools.py::test_e1_metrics_611
FAILED tests/test_defense_chain_610.py::test_check_matches_authoritative_w2_artifact
```

* 9/9 都是**跨源一致性 / 漂移告警**型（现算 ≠ 产物）；
* **0 项**是"写死数字批量红"型（后者会表现为与本次改动无关的大片红）；
* 报告类断言也跟着红，是因为它现在取权威源（产物）而不是写死数字——**这是设计使然**。

**还原后：0 项红**（66 例全绿），且 `git diff -- data/grounded_labels_w2.json` 为空
⇒ 产物字节级还原，验证过程零残留。

## 三、结论

| 判据 | 实测 |
|---|---|
| 改一个派生量 ⇒ 触发的是"漂移告警"而非"写死数字批量红" | ✅ 9/9 为漂移告警型 |
| 还原 ⇒ 全绿 | ✅ 0 项红 |

⇒ 640c A1/A2 的"去快照"改造**确实生效**：数字随权威源自动跟随，权威源一动，
只有"现算 vs 产物"这一条真的有验证力的校验会红，不会像旧版那样整片批量红。
