# 快速开始（QUICKSTART · 3 步上手）

> 目标：让你在 **5 分钟内**知道怎么动笔，1.5–2 小时内标完。

---

## 第 1 步：打开表格

用 Excel / WPS / Google Sheets / VS Code 打开下面任一个文件（别用记事本，会乱码）：

- **145 条完整盲标** → `annotation_package/annotation_template.csv`
- **31 条 AI 分歧裁决（推荐先做，难度已排序）** → `data/702_annotation_table.csv`

每个样本一行，你要填的列已留空（145 条是 8 个字段；31 条是 `your_verdict` / `your_notes`）。

## 第 2 步：看前 5 个示例，建立手感

打开 `README.md` §6 的 3 个示例，以及 `calibration/sources/C01.cpp … C05.cpp`：

- 二次 `delete` ⇒ `catch`（ASan 报 double-free）
- 实参求值顺序 unspecified ⇒ `miss`（任何工具都不报）
- 对齐 UB ⇒ `miss` 但低置信 + `notes`

**记住一条铁律**：你判的是"**检测器会不会报**"，不是"代码坏不坏"。
很多真缺陷 `miss` 是对的，不是你错了。

## 第 3 步：开始标

1. 先通读 `annotation_guidelines.md`（15 分钟，口径唯一来源）。
2. 做 `calibration/` 的 10 道校准题，对 `calibration/answers.csv`；
   分歧 ≥2 条 → 回读手册再开始。
3. 逐条填表：读代码 → 写判定 → 填表。不确定就低 `confidence` + `notes`，**别猜**。
4. 交回：把填好的 CSV 发给协调者（**不要改名、不要改列序、不要删行**）。

---

## 预估时间

| 项目 | 耗时 |
|---|---:|
| 读规则手册 | ~15 min |
| 校准 10 题 + 对答案 | ~15 min |
| 正式标注（145 条 或 31 条裁决） | 145 条约 90–120 min；31 条约 45–60 min |
| 备注 / 答疑 | ~10 min |

**总计约 1.5–2 小时**，可分段完成（建议单次 ≤1 小时，避免疲劳漂移）。

> 时间不够？宁可少标、每条认真标，也不要在疲劳状态下赶完——交回时注明已完成范围即可。
