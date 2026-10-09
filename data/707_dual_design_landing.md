# 707 Task D — 双设计要求落地（700-C）

- 日期：2026-10-09
- 科研依据：**700-C 信息论下界 / 双设计要求**（`data/700_sample_complexity.json`、`data/700_design_simulation.json` L22-25）
- 红线：纯计算/编排，detect_calls = 0。

## 1. 科研结论（700-C）

- 配对设计（同一样本两口径各判一次，对不一致对做符号检验）**只能检出 Type I/II**（ψ>0）。
- **Type III/IV（标签/聚合）逐样本裁决不变 ⇒ ψ = 0 ⇒ 配对设计功效恒 0 ⇒ n = ∞** ⇒ 必须改做**设计级对照**。
- 因此审计协议的 **Step 3 必须是「双设计」**：样本级配对（I/II）+ 设计级对照（III/IV）。
- 实测样本量：Type I **849**（ψ=0.00707）、Type II **17**（ψ=0.3534）、Type III/IV **∞**。

## 2. 落地做了什么

| 文件 | 改动 | 科研依据标注 |
|------|------|--------------|
| `tools/sample_size_calculator.py`（**新**） | 实现 700-C 公式：`ε=ψ(2π−1)`；正态近似 `m≥(z·√¼ + z·√(π(1−π)))²/(π−½)²`，`n=m/ψ`；π=1 用精确二项 `m≥log(α/2)/log(1/2)=6`；ψ=0 ⇒ n=∞ | 文件头「科研依据（700-C 信息论下界）」 |
| `tools/audit_protocol.py`（**新**） | 五步审计协议**可执行版**；**Step 3 = 双设计**：自动按 ψ 判定漂移类型 ⇒ I/II 走配对臂（附样本量），III/IV 走设计级对照臂 | 文件头 + Step 3 注释标注「700-C 配对设计对 III/IV 无效，必须双设计」 |

> **说明**：本项目此前**没有**可执行的五步审计协议（协议只存在于论文正文）。707 把它**首次实现**为 `audit_protocol.py`：Step 1 声明 / Step 2 暴露隐含假设 / **Step 3 双设计** / Step 4 同口径重测（联动 T6）/ Step 5 预声明判决规则。

## 3. 验证

**样本量计算器（与 700-C 逐项一致）**：
```
--type I   → m=6, n=849   与 700-C 一致 = True
--type II  → m=6, n=17    与 700-C 一致 = True
--type III → m=None, n=inf  与 700-C 一致 = True
```

**五步协议 · Step 3 双设计路由**（`audit_protocol.py --plan`）：
```
Type I   composition-drop（构成退化）   axis=sample-level  配对可用=True  ⇒ paired
Type II  environment（环境）            axis=sample-level  配对可用=True  ⇒ paired
Type III label-vocabulary（标签词表）    axis=report-level  配对可用=False ⇒ design-level contrast
Type IV  aggregation-rule（聚合规则）    axis=report-level  配对可用=False ⇒ design-level contrast
```
⇒ 与 700-C 完全一致。Type II 单跑：`配对臂可用=True 所需 n=17`；Type III（ψ=0）：`配对臂可用=False ⇒ 设计级对照`。

`ruff check` 两文件：**All checks passed**。

## 4. 诚实边界

- 五步协议的 **Step 4「同口径重测」** 只给出规则与联动（`check_drift_correctability.py` / 698-B T6），**不执行**重测（红线：不跑新 detect）。
- 设计级对照臂的具体对照组（按聚合轴 / 标签轴）需在**具体审计**中实例化；本工具给出的是**路由与判据**，不是自动执行器。
- 样本量公式用**正态近似**（ψ 小时变差）；π=1 用精确二项；KL 地板未实现（属 700-C 的附加列，非本工具范围）。

## 5. 产物

- `tools/sample_size_calculator.py`（新）
- `tools/audit_protocol.py`（新）
- 本报告
