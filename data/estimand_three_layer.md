# 逃逸率 estimand 三层拆分（617 A1）

> 背景（外部评审 #1）：当前 `1/1406` 与 `0.337%` 混用，未区分 **estimand（被估计的量）** 与 **推断前提（是否冻结 / 是否连续查看）**。
> 连续查看场景下，固定样本 Clopper-Pearson 上界无效。须按**逃逸类型**拆分三层 estimand，并显式标注每层有效性前提。
> 工具：`tools/escape_rate_estimand.py`（按 `--escape-type` 枚举三层）。

## 一、三层定义
### L1 描述性（descriptive）
- 观测样本内的**经验率**。永远有效，但**仅描述已观测样本，不作任何外推/保证**。
- blocked：`1/1406 = 0.0711%`；escaped：`0/1593 = 0`（仅描述冻结样本）；equivalent：`8/1593`。

### L2 推断性（inferential），分两亚类
- **L2a 固定终点（fixed-endpoint）**：需**停止点预注册且非连续查看**。
  - blocked 的 CP 单侧 95% 上界 `0.3370%` 仅在「mutation 是一次性冻结基线、非顺序偷看」前提下有效。
- **L2b anytime-valid（e-process / confidence sequence）**：在**连续决策/统计偷看**下仍有效。
  - blocked 的 CS 上界 `0.9062%`（= CP 的 2.69×）。
  - escaped 的 `0` 必须在 L2b 下用 **e-process mixture** 给正上界（见 A2）。
  - equivalent 需 **conformal 预测带**（见 A2/A3）。

### L3 因果/外推（causal/extrapolation）
- 从冻结样本泛化到**部署**。需**独立性（他验）+ 活性锚**。
- 当前信任根 = `partially_anchored`，L3 必须**折扣（shrinkage）**，不能把 L1/L2 直接当部署逃逸率。

## 二、按逃逸类型的有效推断方法（核心表）
| 逃逸类型 | L1 描述性 | L2a 固定终点 | L2b anytime | L3 外推 |
|---|---|---|---|---|
| blocked | 1/1406 有效 | CP 0.3370% 有效（冻结一次性）| CS 0.9062% 有效 | shrinkage（独立性折扣）|
| escaped | 0/1593 有效 | **无效**（顺序下不能称 0）| e-process mixture（正上界，A2）| shrinkage |
| equivalent | 8/1593 有效 | Wilson 近似（仅参考）| conformal 带（A2/A3）| shrinkage |

## 三、治理结论
1. 对外口径须显式标注**层 + 前提**（哪一层、是否冻结、是否 anytime）。
2. **不允许**把 L1 描述性当部署保证；**不允许**把 L2a 固定终点上界套到连续查看场景。
3. blocked 场景若确为一次性冻结，L2a 可用，但仍应同时报告 L2b CS 作为连续查看下的诚实上界。
4. escaped / equivalent 的精确 L2 待 A2（e-process mixture）/ A3（conformal）补全；当前 L2a 对其标注 `None`（无效）。
