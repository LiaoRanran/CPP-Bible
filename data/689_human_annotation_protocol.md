# 689-C1 · 人类标注实验方案（Human Annotation Protocol）

- 生成：2026-10-07｜批次：689｜执行：CodeBuddy（AI）
- 状态：**方案与材料已备；标注执行 = 待人类完成**（评审一致认定：这是投稿前最重要的人工项）
- 材料包：`data/annotation_package/`（145 条，去标签 + 注释净化 + 标识符重命名）
- 协调者密钥：`data/689_annotation_key_mapping.json`（**不得**交给第二标注者）
- 本文档回答：为什么标、标什么、谁来标、怎么标、分歧怎么办、结果怎么用、什么算合格。

---

## 1. 目标与背景

**目标**：用**独立盲目标注**验证项目标签的 construct validity。当前全部检出率、盲区率、
家族分层都建立在**单一标注者（项目作者）**的标签上，且现有的 κ=0.77 / 0.73 均为
**AI 自一致性**（AI self-consistency），**不是人类 IAA**。本实验提供第一份人类
inter-annotator agreement 证据。

**要验证的标签口径**（权威定义见 `data/holdout_expansion/SCHEMA.md` §4.1）：

- `expected_verdict ∈ {catch, miss}` 是**独立检测器判据**（不是"代码是否有缺陷"）：
  - `catch` = 该样本在 **8 资产池**下，至少一个资产产生**非空诊断报告**；
  - `miss` = 无任何资产产生报告（含 sanitizer 挂起超时 rc=124 后仍无报告）。
- 8 资产池与判据（与 `tools/holdout_reveal_661.py::detect` 一致）：
  | 资产 | 判据 |
  |---|---|
  | asan | 输出含 `AddressSanitizer` / `LeakSanitizer` / `detected memory leaks` / `double-free` |
  | ubsan | 输出含 `runtime error` |
  | tsan | ThreadSanitizer 报告（`WARNING: ThreadSanitizer`） |
  | compiler-warn | 编译期告警非空 |
  | cross-compile | g++ 与 clang 两编译器输出**不一致** |
  | linker | 链接期报错 |
  | wunsequenced | 本机工具链恒不可用 ⇒ 恒 unknown（不参与 catch 判定） |
  | compile-time | 无本地检测器 ⇒ 恒 unknown（不参与 catch 判定） |
- `defect_type`：家族级（8 家族）为主、自由文本二级；
  `planted`：人工构造 vs 真实来源重写；`severity`：low/medium/high。

---

## 2. 标注范围（145 条）

| 分层 | 条数 | 来源 | 理由 |
|---|---:|---|---|
| D2 blind holdout | 41 | 676g 矩阵 holdout 全量 | 最暴露于 reviewer scrutiny |
| D3 external corpus | 64 | 676g 矩阵 corpus 全量 | 外部语料，第二暴露 |
| A5 分层层 | 40 | expA–expG 池按 8 家族分层（每家族 5） | 覆盖主要家族；排除 hung（35 条，登记） |
| **合计** | **145** | | 落于评审建议 135–155 |

外加**校准练习集 10 条**（`annotation_package/calibration/`，不属于主集，不进主分析）。

标注量估计：145 条 × 平均 1–2 分钟/条 ≈ **2.5–4 小时**（评审给出的可接受区间）。

---

## 3. 第二标注者要求

1. **盲**：不得接触 `data/annotation_package/` 以外的本项目材料；不得查看 git 历史、
   原始文件名、`689_annotation_key_mapping.json`；不得询问协调者任何样本的原始标签。
2. **资质**：熟悉 C++（能读懂 RAII、模板、原子/内存序、pthread、UB 基本概念）；
   建议：计算机/软件专业研究生、高年级本科生或教师。
3. **独立**：不得与第一标注者（项目作者）讨论具体样本后再标注；校准题对答案环节只讨论**规则口径**，不讨论主集样本。
4. **记录**：填写 `annotation_template.csv` 全部 8 列；对每条给出 1–5 置信度；
   不确定处写进 notes（这些 notes 本身是分析材料）。

---

## 4. 标注指南（要点；全文见 `annotation_package/annotation_guidelines.md`）

每条样本需要标注：

| 字段 | 取值 | 说明 |
|---|---|---|
| `expected_verdict` | catch / miss | **按 8 资产判据**（§1）；不确定时记最低置信度并写 notes |
| `defect_type_family` | 8 家族之一 | memory / bounds / integer / alias_type / concurrency / stl / language_oop / embedded_link |
| `defect_type_free_text` | 自由文本 | 具体机制（如 "stack-buffer overflow"、"missing unlock"） |
| `planted` | true / false / unsure | true=人工构造的注入缺陷；false=真实来源体裁/正常代码；unsure=存疑 |
| `severity` | low / medium / high | 影响的严重程度（不按可检测性） |
| `confidence` | 1–5 | 对该条判定的把握 |
| `notes` | 自由文本 | 边界情形、疑点、依据 |

**边界案例规则**（写进手册并配校准题）：
- **UB 是否可观测**：`expected_verdict` 判的是"8 资产下能否产生报告"。同样是不终止的缺陷，
  sanitizer 可能给报告（如 TSan 报 race）也可能不给（自旋死锁超时）——**按资产判据判，不按"是不是 bug"判**。
- **hung vs crash**：crash/abort 通常产生 stderr 报告 ⇒ 多为 catch；纯挂起（rc=124）默认 miss（除非挂起前已有报告）。
- **标签干净但崩溃**：可能仍是 catch（ubsan 会报 "runtime error"），要按字符串判据核对。
- **跨 TU / ODR 类**：linker 报错 ⇒ catch；仅命名冲突但可链接 ⇒ 可能 miss。
- **逻辑/语义类**（如协议状态机错误）：8 资产下通常**无报告** ⇒ miss（这正是能力边界的一部分，属预期）。
- **对照样本**（无注入缺陷的干净代码）：无报告 ⇒ miss；若工具误报 ⇒ note 记录（假阳性观察）。

**判定顺序建议**：先只看代码，写下"我认为 8 资产会/不会报告"→ 再填类型与严重度 →
对无法确定的条目用本地工具复跑（可选；材料包 `sources/` 含配套依赖文件，可编译）。

---

## 5. 分歧裁决流程

1. 汇总第二标注者的 145 条结果（`annotation_template.csv`）。
2. 计算一致性（脚本 `annotation_package/analyze_annotation.py`，接口已备）：
   - 逐字段报告 **Cohen's κ** 与 **agreement%**、**分歧计数**（κ 在类别强偏斜时会误导，两者必须并列）；
   - 字段：expected_verdict / defect_type_family / planted / severity。
3. 分歧裁决（两级）：
   - 一级：对不一致条目做**双标注者盲讨论**（只谈该条代码与判据）后重标；
   - 二级：仍不一致者，请第三方（建议教师/资深工程师）按同一手册裁决；
   - 全部裁决记录写入 `data/689_annotation_adjudication.md`（模板待填）。
4. 敏感性重算（关键）：用**第二标注者标签**（以及裁决后标签）重跑：
   - A5 主端点 Δ（FD vs Random / Static）；
   - 38.4% 盲区率与 13/34 类型盲区清单；
   - 家族级检出率与 683 真实靶场的家族结构；
   - 结论：**哪些主要结论因标签修正而改变**（预登记：若 §6 阈值不达标，将对应结论标为"标签敏感"）。

---

## 6. 统计分析预案（预注册阈值）

| 指标 | 合格线 | 不达标处置 |
|---|---|---|
| `expected_verdict` κ | **≥0.8** | 若 0.6–0.8：报告并做逐条裁决；若 <0.6：**标签质量列为重大威胁**，摘要不得使用未经重算的标签依赖数字 |
| `defect_type_family` κ | **≥0.7** | 同上；且报告"家族级分歧集中在哪些家族" |
| `planted` κ | ≥0.6（宽松） | 该字段是元信息，仅作参考 |
| `severity` κ | ≥0.6（宽松） | 同上 |

附加要求：
- 所有 κ 必须与 agreement%、分歧计数**同时**报告；
- 分歧集中的类型/家族单独列表（判断盲区清单是否对标签敏感）;
- 若第二标注者与作者标签在 `expected_verdict` 上系统性漂移（如整体更保守），报告漂移方向与量级，
  不做"少数服从多数"式掩盖。

---

## 7. 时间线与角色

| 步骤 | 执行人 | 预计耗时 | 状态 |
|---|---|---|---|
| 方案 + 材料包（本批） | Agent | — | ✅ 已完成 |
| 招募第二标注者 | 用户 | 1–3 天 | ⬜ 待办 |
| 校准练习（10 条） | 第二标注者 | ~30 分钟 | ⬜ 待办 |
| 正式标注（145 条） | 第二标注者 | 2.5–4 小时 | ⬜ 待办 |
| 一致性统计 | Agent（脚本已备） | ~10 分钟 | ⬜ 待办（依赖上一步） |
| 分歧裁决 + 敏感性重算 | Agent + 第三方 | ~2–3 小时 | ⬜ 待办 |
| 写入论文 §7 T1 | Agent | — | ⬜ 待办（现为"AI-only κ + 方案已备"诚实状态） |

---

## 8. 诚实边界（写入论文 Threats 的原文口径）

- **当前状态**：human IAA = 0（未执行）；AI self-consistency κ=0.727 **不能替代**人类 IAA；
- 本批已完成：实验方案 + 去标签材料包 + 校准集 + 统计脚本 + 预注册阈值；
- **待人类执行**：第二标注（投稿前最重要人工项）；
- 禁止把"方案已设计"写成"已完成"；材料包内不含任何原始标签；
- 净化记录（注释遮盖 280 处、标识符重命名 5 个、字符串软化、残余扫描）
  在 `data/689_annotation_leakage_scan.json` 与 `data/689_annotation_key_mapping.json` 中可核验；
- 已知残余：2 处字符串场景标签含 "race"（S059/S106，`scenario=single|race|safe`），
  经评估不构成类型泄露（样本本身即并发用例），保留原样并登记。

---

## 9. 交付物清单

| 文件 | 用途 |
|---|---|
| `data/689_human_annotation_protocol.md` | 本文件（方案总纲） |
| `data/annotation_package/README_标注者必读.md` | 标注者入口（知情说明 + 流程） |
| `data/annotation_package/annotation_guidelines.md` | 判定规则手册（含 8 资产判据与边界案例） |
| `data/annotation_package/sample_list.csv` | 145 条匿名清单（id/文件/依赖） |
| `data/annotation_package/annotation_template.csv` | 填写模板（8 列） |
| `data/annotation_package/sources/S001–S145.cpp` | 净化后源码（含 2 个依赖头文件） |
| `data/annotation_package/calibration/` | 校准练习集（10 条 + answers.csv + 说明） |
| `data/annotation_package/analyze_annotation.py` | 一致性统计脚本（填完 CSV 即跑） |
| `data/689_annotation_key_mapping.json` | 协调者密钥（匿名 id ↔ 原始标签，**包外**） |
| `data/689_annotation_leakage_scan.json` | 去标识化 QA（残留扫描 + 净化记录） |
