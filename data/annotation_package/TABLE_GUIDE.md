# 标注表格字段指南（TABLE_GUIDE）

> 配套：`annotation_template.csv`（145 条盲标）、`data/702_annotation_table.csv`（31 条裁决集）。
> 本文件逐条解释每一列"填什么、怎么填、为什么"。

---

## 一、145 条盲标表 `annotation_template.csv`（8 列，全部留空待填）

| 列序 | 列名 | 类型 / 取值 | 怎么填 |
|---:|---|---|---|
| 1 | `anon_id` | 文本（如 `S001`） | **只读**，不要改。这是匿名样本 ID。 |
| 2 | `expected_verdict` | `catch` / `miss` | **核心判定**。8 资产中任一（不含 wunsequenced/compile-time）报告即 `catch`，否则 `miss`。 |
| 3 | `defect_type_family` | 8 家族之一 | `memory` / `bounds` / `integer` / `alias_type` / `concurrency` / `stl` / `language_oop` / `embedded_link`。取"根因"家族。 |
| 4 | `defect_type_free_text` | 自由文本 | 具体机制，如 `double_free`、`missing return`、`memory_order_relaxed missing acquire`。不必重复家族名。 |
| 5 | `planted` | `true` / `false` / `unsure` | 是否"为演示缺陷而人工构造"。**不是**"有没有缺陷"的判断。 |
| 6 | `severity` | `low` / `medium` / `high` | 若在真实系统触发后果多大。**与能否被检测无关**。 |
| 7 | `confidence` | 整数 1–5 | 5 最确定，1 纯猜测（猜就在 `notes` 写卡点）。 |
| 8 | `notes` | 自由文本 | 判定依据、不确定点、发现的残留提示、对特定编译条件/平台的依赖。 |

> 判定口径唯一来源是 `annotation_guidelines.md`。与手册冲突的直觉，一律以手册为准。

---

## 二、31 条裁决集 `data/702_annotation_table.csv`（难度已排序）

本表由 `693_human_adjudication_package.csv` 派生，做了两件事：

1. **新增两列留空待你填**：`your_verdict`（= 你的 `catch`/`miss` 判定）、`your_notes`（备注）。
   它们与原始 `human_verdict` / `human_note` 是**同一含义的两个名字**——你填 `your_verdict` 即可，
   协调者后续会并入分析脚本读取的 `human_verdict` 列。
2. **按难度排序（简单在前，难在后）**，并加 `difficulty_tier` 列。

### 难度怎么算的（透明可复核）

难度 = 标注者 B 的置信度 + 残留提示惩罚：

| 标注者 B 置信度 | 基础档 |
|---|---|
| `high` | Easy |
| `medium` | Medium |
| `low` | Hard |
| （缺失） | Medium |

若 `leak_suspected = yes`（源码残留 `expected_verdict` 原文，是干扰项），档位 **+1**（Easy→Medium，Medium→Hard）。

> 说明：这套 31 条本身就是"AI 两个标注者分歧"的样本，所以整体比 145 条盲标更难、更微妙。
> 难度是**相对**排序（基于 AI 置信度的代理），不是绝对难度评分；同一档内按 `sample_id` 稳定排序。

### 列说明（派生表）

| 列 | 含义 |
|---|---|
| `sample_id` | 匿名样本 ID（只读） |
| `difficulty_tier` | Easy / Medium / Hard（已排序，简单在前） |
| `your_verdict` | **你填**：`catch` / `miss`（留空） |
| `your_notes` | **你填**：备注（留空） |
| `leak_suspected` | 是否疑似残留提示（`yes` 是干扰项，更要凭代码判） |
| `defect_type_A` | AI 标注者 A 给的缺陷类型（仅供参考，不是答案） |
| `annotator_A` / `annotator_B` | AI 两标注者的判定（`catch`/`miss`/`unknown`） |
| `b_confidence` | 标注者 B 的置信度（难度代理来源） |
| `b_reason` | 标注者 B 的理由（仅供参考） |
| `human_verdict` / `human_note` | 官方分析列（与 `your_*` 同义，你填 `your_*` 即可） |
| `code_sha256` | 源码哈希（只读，完整性用） |
| `source_code` | 去标识化源码（你要判的对象） |

> 当前分布：Easy 18 / Medium 11 / Hard 2（共 31）。全部 `your_verdict`、`your_notes` 已留空。

---

## 三、填写纪律（防止白标）

- **不要改名、不要改列顺序、不要删行、不要改 `anon_id` / `sample_id`**——分析脚本按这些对齐。
- 不确定就低 `confidence` + `notes`，**不要跳过任何字段**。
- `miss` 不等于错；`severity` 与 `catch/miss` 无关；`planted` 问的是"是否人工构造"。
- 盲性红线：不要查、不要问任何样本的原始标签 / 来源 / 批次。
