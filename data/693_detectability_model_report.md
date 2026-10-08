# 693-E3 · 可检测性预测模型报告

- 生成：2026-10-08T21:13:23+08:00｜脚本：`tools/fit_693_detectability_model.py`
- **`detect_calls` = 0**（只读冻结矩阵 + 源文件，符合红线 8）
- 目标：样本级 or_verdict_available6 == catch（二分类）
- 样本：**1042**（跳过 {'holdout': 41, 'corpus': 64}）；正类基率 **0.593**
- 特征 21 维；结构签名分组数 **559**
- 实现：**纯标准库**自写 CART（Gini）+ L2 逻辑回归（本机无 numpy/sklearn）

## 1. 交叉验证结果（两种折法并列）

| 模型 | 折法 | n | accuracy | AUC | recall | precision | 多数类基线 |
|---|---|---:|---:|---:|---:|---:|---:|
| CART 决策树 | random_5fold | 1042 | **0.6987** | 0.7687 | 0.6877 | 0.7784 | 0.5931 |
| CART 决策树 | group_5fold | 1042 | **0.6775** | 0.7243 | 0.6278 | 0.7854 | 0.5931 |
| L2 逻辑回归 | random_5fold | 1042 | **0.7466** | 0.808 | 0.7023 | 0.8444 | 0.5931 |
| L2 逻辑回归 | group_5fold | 1042 | **0.7179** | 0.7807 | 0.6683 | 0.8227 | 0.5931 |

### 1.1 ⭐ 泄漏导致的高估（本报告最重要的数字）

| 模型 | accuracy 高估 | AUC 高估 |
|---|---:|---:|
| CART 决策树 | **+0.0212** | +0.0444 |
| L2 逻辑回归 | **+0.0287** | +0.0273 |

> 本项目的批内模板克隆率是 **62.2%**（676k）。随机 5 折会把同一模板的参数变体
> 同时放进训练与测试 ⇒ 准确率被高估。上表的差值就是**高估幅度**。
> 任何「我们的模型能预测可检测性」的说法，都必须用 `group_5fold` 的读数。

## 2. 决策树规则（全量拟合，深度上限 5→13 条路径）

```
IF n_mem <= 0.5 AND fam_integer <= 0.5 AND fam_bounds <= 0.5 AND fam_stl <= 0.5 THEN p(catch)=0.36 (n=522)
IF n_mem <= 0.5 AND fam_integer <= 0.5 AND fam_bounds <= 0.5 AND fam_stl > 0.5 THEN p(catch)=0.64 (n=123)
IF n_mem <= 0.5 AND fam_integer <= 0.5 AND fam_bounds > 0.5 AND n_lines <= 7.5 THEN p(catch)=0.62 (n=16)
IF n_mem <= 0.5 AND fam_integer <= 0.5 AND fam_bounds > 0.5 AND n_lines > 7.5 THEN p(catch)=0.98 (n=43)
IF n_mem <= 0.5 AND fam_integer > 0.5 AND chars_per_line <= 23.55 THEN p(catch)=1.00 (n=50)
IF n_mem <= 0.5 AND fam_integer > 0.5 AND chars_per_line > 23.55 AND n_call <= 2.5 THEN p(catch)=0.48 (n=21)
IF n_mem <= 0.5 AND fam_integer > 0.5 AND chars_per_line > 23.55 AND n_call > 2.5 THEN p(catch)=0.95 (n=37)
IF n_mem > 0.5 AND is_memory_safe <= 0.5 AND n_ptr <= 0.5 THEN p(catch)=1.00 (n=12)
IF n_mem > 0.5 AND is_memory_safe <= 0.5 AND n_ptr > 0.5 AND n_ptr <= 13.5 THEN p(catch)=0.61 (n=46)
IF n_mem > 0.5 AND is_memory_safe <= 0.5 AND n_ptr > 0.5 AND n_ptr > 13.5 THEN p(catch)=1.00 (n=16)
IF n_mem > 0.5 AND is_memory_safe > 0.5 AND n_mem <= 1.5 THEN p(catch)=0.84 (n=19)
IF n_mem > 0.5 AND is_memory_safe > 0.5 AND n_mem > 1.5 AND n_mem <= 3.5 THEN p(catch)=0.98 (n=110)
IF n_mem > 0.5 AND is_memory_safe > 0.5 AND n_mem > 1.5 AND n_mem > 3.5 THEN p(catch)=0.89 (n=27)
```

## 3. 逻辑回归系数（|coef| 前 15，标准化后）

| 特征 | 系数 |
|---|---:|
| `n_mem` | +0.7802 |
| `n_thread` | -0.7499 |
| `n_branch` | +0.6131 |
| `max_depth` | -0.5331 |
| `n_loop` | +0.4890 |
| `chars_per_line` | -0.4571 |
| `n_call` | -0.3718 |
| `fam_embedded` | -0.3332 |
| `fam_integer` | +0.3149 |
| `fam_bounds` | +0.3081 |
| `fam_alias_type` | -0.2751 |
| `n_lines` | +0.2680 |
| `fam_stl` | +0.2487 |
| `fam_memory` | -0.1939 |
| `branch_density` | -0.1716 |

## 4. 诚实边界

- 样本主体为合成/半合成（92.9% 人工植入）⇒ 模型学的是**仪器**不是真实缺陷分布。
- 批内模板克隆率 62.2% ⇒ 随机折会泄漏；group_5fold 是更可信的读数。
- 特征只覆盖 expA–expG（能定位到源文件的样本）；holdout/corpus 未纳入。
- 决策树深度与最小叶大小未做调参搜索（避免在 1147 条上过拟合）。
- 目标用 or_verdict_available6；换成 expected_verdict 会得到不同（且更乐观）的结果。
