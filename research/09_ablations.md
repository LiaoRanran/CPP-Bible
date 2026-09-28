# 09 · 消融实验（A0–A4）

| 消融 | 去掉什么 | 观测 | 对应假设 |
|---|---|---|---|
| A0 | 无（Full system） | 基准检测率 | H1 上限 |
| A1 | − failure-derived assets | 去掉失败驱动选资，退回随机/B2 | H3（增益来源） |
| A2 | − blind holdout isolation | holdout 在训练期可见 | 测泄漏影响（威胁 3） |
| A3 | − provenance constraints | 判决不要求 provenance 完整 | H4（可信度来源） |
| A4 | random asset addition | 改"随机加资产"替代失败驱动 | H3 对照（B3 内） |

**报告**：每个消融给出 D1/D2 检测率相对 A0 的 Δ，标注是否显著（威胁 7/8 的量化）。
