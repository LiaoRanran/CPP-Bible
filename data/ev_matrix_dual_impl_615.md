# 615 B1 · EV-MATRIX-UNBACKED 独立第二实现对比

> 独立实现（**不 import/copy gate_engine**）；官方 `--check` **未重跑**，官方口径由**历史记录参数化**
> （`_arch_v19/probes/output/p03_meta_verification.out`）。

## 一、一致率（实测）

- 适用卡（多编译器）：**19**（全证据卡 56，崩溃 0）
- 官方口径 UNBACKED：**16**
- 第二实现(natural：仅剥 actual) 与官方：**一致 13 / 分歧 6 => 68.4%**

## 二、分歧卡（natural 把 UNBACKED 误放行为 BACKED）

| 卡 | 官方 | 第二实现(natural) |
|---|---|---|
| `evidence/conc/EV-CONC-001.md` | UNBACKED | BACKED |
| `evidence/conc/EV-CONC-002.md` | UNBACKED | BACKED |
| `evidence/mem/EV-MEM-001.md` | UNBACKED | BACKED |
| `evidence/mem/EV-MEM-039.md` | UNBACKED | BACKED |
| `evidence/mem/EV-MEM-042.md` | UNBACKED | BACKED |
| `evidence/mem/EV-MEM-043.md` | UNBACKED | BACKED |

- 与历史记录 6 张分歧卡**完全吻合**：✅（历史：6 张）

## 三、分歧根因（隐性预处理）

1. 官方 `_raw_without_actual` **除剥 `actual` 段外，还剥 `artifact_sha256:` 行**（2026-09-12 由 P12 毒样例首跑暴露：只剥 actual 时毒卡靠 sha 全零被放行）。
2. `artifact_sha256` 是 64 位十六进制 ⇒ **含 ≥10 位的纯数字片段**，被「CI run 号裸数字」锚正则（`\d{10,}`）误收 ⇒ 多编译器毒卡被**结构性放行**。
3. ⇒ **规则的正确性知识部分埋在预处理里，不在规则主逻辑**；读代码重写会自然丢失（Knight-Leveson common-mode 关切）。

## 四、口径与边界

- 官方逐卡 oracle 由**文档化预处理**（剥 actual + 剥 sha）**重建**，并用历史记录（适用 19 / 一致 13 / 分歧 6 且卡名吻合）**交叉验证**——不重跑 gate --check（615 铁律）。
- 第二实现仅做**对比**，**不替换**官方实现；不改 `gate_engine.py`。

