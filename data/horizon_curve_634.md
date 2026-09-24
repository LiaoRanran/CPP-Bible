# 634 B2 · Horizon 曲线（复杂度-检出率）

## 一、关键更正：§一 的「60-80 桶 0%」是**陈旧基线**

- `data/verification_horizon_curve_622.json` 共存 **7** 个版本；
- **最早 v1 起 60-80 桶检出率即为 100%**，并非 0%（§一 记的 0% 来自 622 M9 的**原始**发现，后续版本已修复，基线未同步）——本批如实登记该陈旧。

## 二、各版本 bands

| 版本 | 20-40 | 40-60 | 60-80 | score |
|---|---|---|---|---|
| v1 | 0.574 | 0.9699 | 1.0 | 80 |
| v2 | 0.97 | 0.9113 | 1.0 | 80 |
| v3 | 0.8841 | 1.0 | 1.0 | 80 |
| v4 | 0.8845 | 1.0 | 1.0 | 80 |
| v5 | 0.9871 | 1.0 | 1.0 | 80 |
| v6 | 0.9506 | 1.0 | 1.0 | 80 |
| v7 | 0.9872 | 1.0 | 1.0 | 80 |

## 三、最新版本

- 版本 `v7`：60-80 桶 = **1.0**（目标 ≥0.5 ⇒ **达成**）

## 四、623 高复杂度攻击实测（80 条）

- 判定分布：{'blocked': 46, 'escaped': 4, 'detected_nonblock': 16, 'neutral': 12, 'infra_error': 2}
- 检出 = blocked + detected_nonblock = **62/80** = 77.5%
- **新触达 block 规则 17 条**（目标 ≥5 ⇒ **达成**）：`ATOM-AUDIENCE`, `ATOM-DAL-MATCH`, `ATOM-FM-REQUIRED`, `ATOM-GRAY-ZONE`, `ATOM-ID-FORMAT`, `ATOM-ID-UNIQUE`, `ATOM-NO-UNVERIFIED`, `ATOM-REL-DAG`, `ATOM-STATUS-VALUE`, `EV-ARTIFACT-PRODUCER`, `EV-ARTIFACT-VERSION-MATCH`, `EV-FM-DUP-KEY`, `EV-FM-REQUIRED`, `EV-FM-YAML-HARDENING`, `EV-ID-UNIQUE`, `EV-MATRIX`, `EV-MSCV-NO-VERIFY`

## 五、诚实登记（§八.4）

1. **634 未新造高复杂度攻击**：目标「60-80 ≥50%」「触达 ≥5 新规则」**已由 622-624 达成**，本批做的是**复算 + 登记**，不重复造轮子（§零.7 先盘点后清理）；
2. **§一起始基线陈旧**：其「0%」与实测（v1 起 100%）矛盾，已如实更正，不修数字；
3. 623 的 80 条里仍有 **4 条 escaped / 2 条 infra_error / 12 条 neutral**——高复杂度带**并非全绿**，escape 根因见 `data/escape_root_cause_v2_623.md`（登记，本批不重跑）。
