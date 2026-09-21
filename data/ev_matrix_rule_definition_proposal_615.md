# 615 B2 · EV-MATRIX-UNBACKED 规则定义补全提案（**只写提案，不改 evidence/，交人审**）

> 依据 B1 双实现差分（`data/ev_matrix_dual_impl_615.md`）。铁律：不改 `evidence/`、不改 `gate_engine.py`（交人裁决后下批执行）。

## 一、隐性预处理（类型 A）
**官方 `gate_engine.py::_raw_without_actual` 除了剥 `actual:` 段，还剥 `artifact_sha256:` 行。**

- 位置（官方代码）：`gate_engine.py` 约 L987–999（`_raw_without_actual`）。
- 触发来源：注释明载「**2026-09-12 由 P12 毒样例首跑暴露：只剥 actual 时毒卡仍靠 sha 全零被放行**」。
- 为何必要：`artifact_sha256` 值 = **64 位十六进制**，其中含 **≥10 位的纯数字片段**；若只剥 `actual`，
  这些数字片段会被「CI run 号裸数字」锚正则（`\d{10,}`）**误收为留痕锚** ⇒ 多编译器毒卡被**结构性放行**（BACKED）。
- 实证：B1 natural 口径（只剥 actual）在 6 张卡上误判 BACKED：
  `EV-CONC-001 / EV-CONC-002 / EV-MEM-001 / EV-MEM-039 / EV-MEM-042 / EV-MEM-043`。

## 二、规则定义文档的现状
- **未找到**一份独立的规则定义文档（`evidence/` 下仅 README；`docs/compiler-matrix.md` 无该规则文本）。
- 规则语义**内嵌于 `gate_engine.py`**（tool_integrity 注释亦载「规则定义内嵌在 gate_engine.py 里」）。
- ⇒ 「规则定义文档」实为**代码 + `References/architecture_架构演进/588_…` 说明**；本提案建议**显式化**该预处理。

## 三、建议写入的具体文本
**建议插入位置**：`588` 说明文档的「matrix 尾注释收口」章节（或新建 `docs/rules/EV-MATRIX-UNBACKED.md`）。

> **建议文本**：
> 「EV-MATRIX-UNBACKED 的留痕锚统计在**剥去 `actual:` 段之后**进行；**同时必须剥去 `artifact_sha256:` 行**。
> 原因：`artifact_sha256` 为 64 位十六进制，含 ≥10 位纯数字片段，会被「CI run 号裸数字」锚（`\d{10,}`）
> 误收为留痕锚，导致多编译器毒卡被结构性放行（2026-09-12 P12 毒样例实证）。
> 即：**锚统计的输入 = 原文 − `actual:` 段 − `artifact_sha256:` 行**。」

## 四、预期影响
- 第二实现补上该预处理后，与官方一致率：**68.4% → 100%（19/19）**（与历史 2b 一致）。
- 对官方判定**零影响**（官方已含该预处理）；本提案只是把**代码里的隐性知识显式化**，
  使"读文档重写"不再丢失（缓解 Knight-Leveson common-mode）。

## 五、边界
- 本文件**仅为提案**；**未修改**任何 `evidence/` 文件、**未修改** `gate_engine.py`。
- 写入规则定义文档需**人审授权**后下批执行。
