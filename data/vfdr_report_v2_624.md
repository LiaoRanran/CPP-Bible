# 624 A5 · VFDR 更新 v2 + 规则触达热力图 v2 + 盲区缩减报告

> 工具：`tools/vfdr_updater_v2_624.py`（6 轮闭环真跑数据聚合）
> 数据：`data/vfdr_report_v2_624.json` + `data/rule_touch_heatmap_v2_624.md`
> 检测率（VFDR）= (blocked + detected_nonblock) / (total − infra_error)

---

## 一、VFDR 六轮对比

| 轮次 | 载体 | 条数 | blocked | nonblock | neutral | infra | escaped | **检测率** | 本轮触达 |
|---|---|---|---|---|---|---|---|---|---|
| R1（622 A2） | 单卡低复杂 | 50 | 13 | 0 | 14 | 23 | 0 | **48.1%** | 5 |
| R2（622 A4） | 单卡 v2 M8/M9 | 30 | 15 | 8 | 2 | 5 | 0 | **92.0%** | 3 |
| R3（623 A2） | 单卡高复杂 | 80 | 46 | 16 | 12 | 2 | 4* | **79.5%** | 25 |
| R4（623 A4） | 单卡定向 | 40 | 12 | 14 | 14 | 0 | 0 | **65.0%** | 6 |
| **R5（624 A2）** | **跨卡** | 60 | 47 | 13 | 0 | 0 | 0 | **100%** | 13 |
| **R6（624 A4）** | **跨卡定向 X5-X8** | 40 | 40 | 0 | 0 | 0 | 0 | **100%** | 5 |

\* R3 的 4 条 escaped 经 623 A3 证实为删字段假象（dangerous 逃逸 = 0）。

- **检测率**：R1 48% → R5/R6 **100%**（跨卡攻击零 neutral、零 infra）。
- **危险逃逸（dangerous）全程 0**（六轮合计 300 条真跑）。

## 二、规则触达热力图 v2（63 × 6）

见 `data/rule_touch_heatmap_v2_624.md`（全量表格）。

## 三、累计触达规则数（核心压力指标）

| 口径 | 622 | 623 | **624（六轮累计）** | 目标 |
|---|---|---|---|---|
| 累计触达规则 | 9/63 | 26/63 | **34/63（54.0%）** | >45/63 |

- **六轮累计触达 34/63**，相对 623 的 26 **新增 8 条**。
- ⚠ **口径说明**：R1/R2（622 两轮）触达了 `ATOM-STATUS-TRANSITION`、`EV-FALSIFICATION` —— 这两条在 623 的热力图里
  被列为"未触达"（因为 623 的热力图**只统计 623 自己的两轮**）。因此 624 六轮累计 = 34，高于
  A4 报告里「623∪624A2∪624A4 = 32」的子集口径。**本报告 34 为六轮全量口径**。

## 四、未触达规则清单 v2（盲区，29 条）

| 类别 | 规则 |
|---|---|
| 需编译/复算产物 | EV-ZERO-DIAG-WERROR · EV-WERROR-DECL-BIND · S3-EXPECTED-HARDCODED · EV-RUN-KEY-DECLARED-EXISTS · EV-ENV-DEPENDENT-KEY · EV-OUT-UNDECLARED-KEY · EV-OUT-STALE-MTIME · EV-FIXTURE-NO-ECHO-DATA |
| 词表黑盒/文风 | ATOM-SUPERIORITY-WORDS · EV-FALSIFICATION-QUANT · EV-TRIVIAL-OBSERVATION · EV-MATRIX-UNBACKED · EV-SELF-SATISFIED-ASSERT · ATOM-CLAIM-CONCEPT-NORMALIZED · OBSERVATION-LIVENESS · DOC-ZERO-PLACEHOLDER |
| 需 git 历史/manifest | S1-AUTHOR-SELF-VERIFY · S1-GIT-AUTHOR-BINDING · META-MANIFEST |
| 需多卡/命题级（本轮仍未触达） | INFERENCE-NOT-MACHINE-VERIFIED · MIS-LIBRARY · ATOM-MISCONCEPTION-LEVELS |
| advice（不足为奇） | PED-MOTIVATION · PED-MISCONCEPTION · PED-SOCRATIC · PED-PREDICT-FIRST · LLM-SUPERIORITY-QUALITY · HYBRID-TEACHING-DEPTH · HUMAN-GOLDEN-REVIEW |

## 五、盲区缩减报告

| 项 | 值 |
|---|---|
| 623 盲区 | **37** |
| **624 盲区** | **29** |
| 缩减 | **−8 条** |
| 目标 | <25（**未达**） |

## 六、与 620/622/623 VFDR 对比

- 622 的 VFDR 是 **flat-zero（0.0，不可测）**；623 用双轴口径测得检测率 26%→77.5%/65%；
  624 跨卡攻击检测率 **100%**（R5/R6）。
- **危险逃逸始终 0**：检测率提升来自**攻击载体扩展**（单卡→跨卡→定向跨卡），非系统盲区缩小。

## 七、局限性声明

1. **盲区 29 条的主因是载体不可构造**（编译/复算/git/词表），非规则缺失 ⇒ 需架构层（gate 之外）扩展。
2. **口径差异**：34 为六轮全量累计（含 622 两轮）；若只算 623+624，则为 32。
3. **样本量小**，分轮后 R2/R6 仅 30/40 条。
4. 检测率以 gate（规则层）为准，不含 replay 复算层。
