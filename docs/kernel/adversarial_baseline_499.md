# 对抗基线更新（499 任务8）

> 方法：实跑 `python tools/adversarial_regression.py`（498 收工后）
> 结论：**拦截状态与 494 基线完全一致，无回归、无新逃逸**

## 1. 498 后最新汇总（实跑输出原文）

```
[adv-regression] blocked=25 · escape=0 · visible=2 · gap=0 · skip=35
[adv-regression] 判定为双轨：机器 verdict（refute/infra_error⇒拦、confirm⇒逃逸）优先，
               自述兜底；visible=gate 层 warn/advice（可见化不阻断，需人裁决）；skip ≠ pass
```

## 2. 与 494 基线对比

| 指标 | 494 基线 | 499（498 后） | 变化 |
|---|---|---|---|
| blocked | 25 | 25 | 0 |
| escape | 0 | 0 | 0 |
| visible | 2 | 2 | 0 |
| gap | 0 | 0 | 0 |
| skip | 35 | 35 | 0 |

## 3. 变化分析

**无变化。** 498 批次的改动（frontmatter 批量添加、工件-卡版本绑定 `EV-ARTIFACT-VERSION-MATCH`、增量 replay、trace_logger、tool_integrity、task_state）均未触动对抗回归所锁定的 25 个 blocked 探针的判据，也未改变 35 个 skip 探针的自述/机器可判状态。

- blocked 25：锁在 `tests/test_p0f_zerodiag.py`、`test_p0b_echo.py`、`test_recompile_invariant.py`、`test_discriminative.py`、`test_poison_attack_type.py`、`test_p0g_lock.py` 等，全部 `verdict=refute:*`（卡不可直推），机制层面已拦死。
- visible 2：gate 层 warn/advice（可见化但不阻断，需人裁决），与基线同。
- skip 35：说明型探针（`_adv_v80/probe_misc.py` 等）与历史轮次（v61/v70）无法自动断言，与基线同。**skip ≠ pass**，仍属"机器判不了"的待覆盖区。

## 4. 当前逃逸清单

`escape = 0`。无逃逸。

## 5. 备注

任务 7（机械变异对抗）发现的 2 个真实门禁盲区（M5 `run_match_keys` 假键未反向校验、M8 工件指向不存在文件 gate 不 block）属于**对抗回归框架之外的门禁层漏洞**，不在本对抗回归的 blocked/escape 统计口径内，详见 `docs/kernel/mutation_test_499.md`，建议好模型单独立项修复。
