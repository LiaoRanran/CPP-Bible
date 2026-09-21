# 置信序列 L2b / L3 shrinkage（617 A2 · 补 A1 的精确 L2）

> 配套：`data/estimand_three_layer.md`（A1 三层定义）+ `tools/escape_rate_estimand.py`（A1 枚举器，escaped/equivalent 的 L2b 当前标 None）。
> 本文件给出 escaped / equivalent 的**精确 L2b 方法**与 **L3 外推 shrinkage 公式**，供后续工具落地（A3 或 618）。

## 一、escaped 类型的 L2b：e-process mixture
- 场景：声称「0 逃逸」（如 replay refute=0、mutation 未观测逃逸=0）。在**连续决策/统计偷看**下，直接宣布 0 无效（固定样本 CP 经验虚报 13.80%）。
- 方法：用 **mixture e-process**（Robinson–Egr 等）对「0 vs 小正逃逸率」做序贯检验：在任意停止时间 t，e-process E_t 的 Ville 不等式 P(sup E_t > 1/α) ≤ α 给出 anytime 上界。
- 给定先验（如 Beta(1, K) 的弱信息）与观测 0 逃逸 / n 样本，**e-process mixture 上界** = 1 − (1 − α)^{1/(n+1)} 量级（取决于先验强度），恒为**正上界**，不出现「0」。
- 现状：A1 枚举器对 escaped 的 `anytime_cs_upper_95` 标 None，待本方法落地为 `tools/confidence_sequence.py` 的新分支（留 A3 / 618）。

## 二、equivalent 类型的 L2b：conformal prediction
- 场景：8/1593 语义等价判定的不确定性（逐卡片分布无关保证 + "无法判定"第三态）。
- 方法：对「是否真等价」构造 **split/conformal 预测带**，给出覆盖保证的逃逸率区间，与保形预测/弃权三态（交人项 616 #10）联动。
- 现状：A1 枚举器对 equivalent 的 `anytime_cs_upper_95` 标 None，待 conformal 分支（留 A3 / 618）。

## 三、L3 外推 shrinkage（通用）
- 公式：`rate_L3 = rate_L1 + (1 − independence_level) × (prior − rate_L1)`，prior = 0.05（保守最坏先验）。
- `independence_level` 取自 B1 `tools/verify_independence_level.py`：当前离散=1、连续 scalar≈0.153（verifier=1 硬上限）。
- 含义：独立性越低，部署外推越向先验 0.05 收缩；当前 scalar≈0.153 ⇒ blocked 的 L3 ≈ 0.0711% + 0.847×4.93% ≈ **4.25%**（远松于 L2b CS 0.9062%，诚实反映「无独立第三方」的外推不确定性）。
- 治理：L3 仅在「报告明确标注为部署外推、且独立性支撑」时使用；否则只能报告 L1/L2（冻结样本内）。

## 四、与 A1 的接口
- A1 枚举器已内置 L3 shrinkage（`layer_l3`），入参 `independence_level`；本文件定义其语义与 prior。
- A1 对 escaped/equivalent 的 L2b 标 None 是**有意的诚实占位**，待本文件方法落地后填入正数（禁止填 0）。
