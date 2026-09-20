# 612 A3 · 加桥后 W2 重算 + 判决变化分析（只读）

> 复用 `weighted_af_solver` 的 W2 模型（不重实现求解）；同时报告 keep-low 与 upgrade-medium 两种口径（不选边）。
> 桥接边为 MIS→MIS；W2 的 MIS 可信度取自其 MIS↔命题边，故**补桥通常不改判决**——本报告把「零影响」与「结构改善」同时据实列出。

## 一、总览（加桥前后关键数字）

| 口径 | what-if | 应用桥数 | 加桥前 | 加桥后 | 击败边 | 分量 | 翻转 |
|---|---|---|---|---|---|---|---|
| keep-low | approved-only | 0 | IN 114 / OUT 7 / UNDEC 0 | IN 114 / OUT 7 / UNDEC 0 | 17→17 | 11→11 | 0 |
| keep-low | all-medium | 98 | IN 114 / OUT 7 / UNDEC 0 | IN 114 / OUT 7 / UNDEC 0 | 17→17 | 11→7 | 0 |
| keep-low | all-high | 98 | IN 114 / OUT 7 / UNDEC 0 | IN 114 / OUT 7 / UNDEC 0 | 17→17 | 11→7 | 0 |
| upgrade-medium | approved-only | 0 | IN 121 / OUT 0 / UNDEC 0 | IN 121 / OUT 0 / UNDEC 0 | 0→0 | 11→11 | 0 |
| upgrade-medium | all-medium | 98 | IN 121 / OUT 0 / UNDEC 0 | IN 121 / OUT 0 / UNDEC 0 | 0→0 | 11→7 | 0 |
| upgrade-medium | all-high | 98 | IN 121 / OUT 0 / UNDEC 0 | IN 121 / OUT 0 / UNDEC 0 | 0→0 | 11→7 | 0 |

## 二、判决翻转清单

**加桥前后**所有节点判决均未翻转（0 个）——与 611 C3 的「加桥判决变化 0」一致：
桥接边是 MIS→MIS，W2 的 MIS 可信度取自 MIS↔命题边，桥不构成击败。

## 三、风险提示

- 加桥改善的是**连通性**（分量减少），不改判决；「脆弱节点（承重高但辩护弱）」清单待后续结合辩护链细化。
- 加桥是否真成立仍须人审（A2）；本工具只算「若成立」的判决影响。

## 四、口径与边界

- **只读**：不写任何数据文件、不改攻击边；
- 同时报告 keep-low（入库权威口径 IN114/OUT7）与 upgrade-medium（609 A3 口径 IN121/OUT0），**不裁决**；
- `approved-only` 在 0 条批准时应与基线**逐项一致**（--check 锁此不变量）。
