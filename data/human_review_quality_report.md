# 人审质量报告（610 A2 · 只读生成）

> 数据源：`data/human_attack_edge_annotations.jsonl`（用户两次授权的真实人审）；
> 本报告由 `tools/human_review_report.py` 生成，**不含任何外部输入的数字**。

## 1. 总览

- 记录 **388** 条：approve 354（91.2%）· modify 34（8.8%）· reject 0
- MIS 组 **42** 个 · 主题 5 类
- 理由原文记载：抽样验证准确率100%(20/20)

## 2. 按 verdict 分布

| verdict | 条数 | 占比 |
|---|---:|---:|
| approve | 354 | 91.2% |
| modify | 34 | 8.8% |
| reject | 0 | 0.0% |

## 3. 按 MIS 分组（modify 比例 Top 10）

| MIS | 总条数 | approve | modify | modify 比例 |
|---|---:|---:|---:|---:|
| `MIS-LANG-001` | 6 | 0 | 6 | 1.00 |
| `MIS-MEM-001` | 6 | 0 | 6 | 1.00 |
| `MIS-MEM-003` | 6 | 0 | 6 | 1.00 |
| `MIS-UB-001` | 4 | 0 | 4 | 1.00 |
| `MIS-UB-004` | 4 | 0 | 4 | 1.00 |
| `MIS-UB-008` | 4 | 0 | 4 | 1.00 |
| `MIS-UB-014` | 4 | 0 | 4 | 1.00 |
| `MIS-MEM-031` | 24 | 24 | 0 | 0.00 |
| `MIS-MEM-024` | 18 | 18 | 0 | 0.00 |
| `MIS-MEM-026` | 18 | 18 | 0 | 0.00 |

## 4. 按主题分布

| 主题 | MIS 数 | 条数 | 占比 | approve | modify |
|---|---:|---:|---:|---:|---:|
| MEM | 27 | 312 | 80.4% | 300 | 12 |
| UB | 9 | 36 | 9.3% | 20 | 16 |
| HIST | 3 | 24 | 6.2% | 24 | 0 |
| CONC | 2 | 10 | 2.6% | 10 | 0 |
| LANG | 1 | 6 | 1.6% | 0 | 6 |

## 5. 按方向分布

| direction | 条数 |
|---|---:|
| mis_to_prop | 194 |
| prop_to_mis | 194 |

## 6. 质量异常检测

| 类型 | MIS | 说明 |
|---|---|---|
| modify_ratio_1.0 | `MIS-LANG-001` | 6 条全部被判 modify ⇒ 歧义度最高，建议人工复核 |
| modify_ratio_1.0 | `MIS-MEM-001` | 6 条全部被判 modify ⇒ 歧义度最高，建议人工复核 |
| modify_ratio_1.0 | `MIS-MEM-003` | 6 条全部被判 modify ⇒ 歧义度最高，建议人工复核 |
| modify_ratio_1.0 | `MIS-UB-001` | 4 条全部被判 modify ⇒ 歧义度最高，建议人工复核 |
| modify_ratio_1.0 | `MIS-UB-004` | 4 条全部被判 modify ⇒ 歧义度最高，建议人工复核 |
| modify_ratio_1.0 | `MIS-UB-008` | 4 条全部被判 modify ⇒ 歧义度最高，建议人工复核 |
| modify_ratio_1.0 | `MIS-UB-014` | 4 条全部被判 modify ⇒ 歧义度最高，建议人工复核 |
| review_seconds_missing | `*` | 388/388 条无 review_seconds ⇒ 耗时不可回溯测量（不伪造 0，short_time 判定对其不可用） |

## 7. modify 比例 = 1.0 的 MIS（7 个）

- `MIS-LANG-001`（6 条全 modify）
- `MIS-MEM-001`（6 条全 modify）
- `MIS-MEM-003`（6 条全 modify）
- `MIS-UB-001`（4 条全 modify）
- `MIS-UB-004`（4 条全 modify）
- `MIS-UB-008`（4 条全 modify）
- `MIS-UB-014`（4 条全 modify）

## 8. 后续建议

- 上表 `modify_ratio_1.0` 的 MIS 是**歧义度最高**的一组：建议优先安排第二轮人审（把'证据较充分但偏保守'的档位判断沉淀成判据）；
- 耗时类质量指标（automation bias / 单位时间产出）：人审 CLI 的 schema **已扩**（611 A2 新增 `review_seconds`），新记录起即可测；存量 388 条**不可回溯**（如实标 measured=false，**不伪造 0**）；
- 本报告只呈现事实与异常清单，**不自动执行任何人审**、不修改任何注解。

## 9. 耗时统计（review_seconds · 611 A2）

| 指标 | 值 |
|---|---:|
| 记录总数 | 388 |
| **测得** | 0 |
| 未测得（null/缺字段） | 388 |
| measured | **false** |
| 平均（s） | — |
| 中位数（s） | — |
| 最大（s） | — |
| 最小（s） | — |
| 合计（s） | — |
| 计时来源 | — |

- 存量人审未测耗时 ⇒ 统计不可回溯（measured=false，不伪造 0）

- **口径**：只统计**显式测得**的记录；未测的既不按 0 计入、也不参与均值（0 秒是真实值，缺测是另一种状态，两者不可混同）。
