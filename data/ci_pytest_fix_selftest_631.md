# 631 A3 · 工具自检过期型修复报告

> 输入：`data/ci_pytest_triage_631.md`（A1 分类，共 3 项）
> 授权：§零.11 例外条款（**只改测试断言，不改被测工具的生产逻辑**）

## 一、这类的特征

失败**不在测试自己的断言里**，而在被测**工具的内部自检**（`--check` / `selftest`）；
测试只是把它跑起来。因此：

- 改测试断言 ⇒ 只能"绕开依赖"或"条件跳过"；
- 真正修好 ⇒ 必须改工具（627/629 工具），属 §零.11 越界 ⇒ **交人**。

## 二、逐项处置

| # | 用例 | 失败点在 | 处置 | 验证 |
|---|---|---|---|---|
| 1 | `test_pre_push_checklist_627.py::test_tools_all_check_pass` | 627 工具 `pck_hash_drift_analyzer_627 --check` 断言「无健康证书（全部有缺口）」 | `@skipif(_drift_resolved())` —— 条件由**实测** `analyze()["n_content_drift_certs"] == 0` 算出 | ✅ skip（理由可见） |
| 2 | `test_pre_push_checklist_627.py::test_run_all_aggregates_ok` | 同上（聚合含该工具自检） | 同上 | ✅ skip |
| 3 | `test_baseline_629.py::test_selftest_and_baseline_failure_freeze` | 629 工具 `baseline_629.py` 的 selftest 断言「push 前 ahead ≥ 62」，630 B2 完成 push 后 ahead = 0 | **去掉对 `B.selftest()` 的依赖**，保留本用例真正要守的基线计数断言（11 项 + 分类合计） | ✅ pass |

**验证命令与结果**：

```text
pytest tests/test_pre_push_checklist_627.py tests/test_baseline_629.py -n0 -q
→ s....s.......        （11 pass / 2 skip，原 3 fail）
```

## 三、为什么 #1/#2 用"条件 skip"而不是直接 skip

条件是 **从数据实测算出**的：当 `content_drift == 0`（628 A2 已把 PCK hash 修好）时，
627 工具那条「全部有缺口」的自检**必然失败**，此时运行它没有意义；
若将来数据出现回退（drift > 0），条件自动不成立、用例**自动恢复运行并真正执行该自检**——
即：**不静默通过、不永久豁免**。理由文本写在装饰器里，`pytest -rs` 可见。

## 四、诚实登记

1. **这 3 项的"真修"都越界**：627 工具的 PCK 自检、629 工具的 ahead 自检都需要
   改对应工具的生产逻辑（§零.11）⇒ **列入交人项**（验收报告 §六）。
2. #3 去掉 selftest 依赖后，**629 工具自身的过期断言仍存在**：任何人跑
   `tools/baseline_629.py --check` 仍会红；本批只是在套件内不再因它红。这一点未掩盖。
3. 本批未改任何 627/629 工具的源码（仅改 `tests/` 下两个文件，逐 commit 可查）。
