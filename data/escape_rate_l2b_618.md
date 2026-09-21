# escaped/equivalent L2b 精确上界（618 A3 · e-process mixture + L3 shrinkage）

> 纯标准库；数字取自 `data/SNAPSHOT_MANIFEST_617.json` 的 mutation_v7（variants=1593, equivalent=8）；escaped 为声称零逃逸 regime（k=0, n=1593，同 617 A1 `layer_l1`）。

> **L3 明确标注：外推假设，非直接测量**（依赖独立性 scalar=0.153，verifier=1 硬上限）。

## escaped（k=0, n=1593）

- L1 描述性经验率：`0.000000%`
- **L2b e-process mixture anytime 上界（95%）：`0.648842%`**（正上界，禁填 0；区别于 A1 枚举器 None 占位；Beta(1,1) 混合先验，保守）
- L3 shrinkage 外推上界（95%）：`4.235000%` ⚠️ **外推假设，非直接测量**

## equivalent（k=8, n=1593）

- L1 描述性经验率：`0.502197%`
- **L2b e-process mixture anytime 上界（95%）：`1.607924%`**（正上界，禁填 0；区别于 A1 枚举器 None 占位；Beta(1,1) 混合先验，保守）
- L3 shrinkage 外推上界（95%）：`4.311836%` ⚠️ **外推假设，非直接测量**

## 与 617 A1 枚举器的关系

- 617 A1 `tools/escape_rate_estimand.py` 对 escaped/equivalent 的 `anytime_cs_upper_95` 标 `None`（有意为之的诚实占位，禁填 0）。
- 本工具给出 617 A2 方法文档（`data/confidence_sequence_l3_shrinkage.md`）的**可执行 L2b**：e-process mixture 正上界。
- blocked 类型的 L2b 仍由 A1 的置信序列 CS=`0.9062%%` 承担（任何时刻上界）；本工具仅补 escaped/equivalent 两类。

## 方法

- L2b：e-process mixture（Beta(1,1) 混合先验），解 M(θ)=1/α，M(θ)=B(k+1,n-k+1)/(θ^k·(1-θ)^{n-k})；在 θ>k/n 增支二分取上界。
- L3：shrinkage = L1 + (1 - 0.153) × (0.05 - L1)，prior=0.05。
