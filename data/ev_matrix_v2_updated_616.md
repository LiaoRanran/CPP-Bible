# 616 B2 · EV-MATRIX 第二实现补全语义（一致率 68.4% → 100%）

> 独立实现（**不 import/copy gate_engine**）；官方 `--check` 未重跑，官方口径由文档化预处理重建
> + 历史记录交叉验证。

## 一、一致率

| 口径 | 预处理 | 适用卡 | 一致 | 分歧 | 一致率 |
|---|---|---|---|---|---|
| 615 历史自然实现 | P1（仅剥 actual） | 19 | 13 | 6 | **68.4%** |
| **616 补全语义** | **P1+P2（+剥 artifact_sha256 行）** | 19 | 19 | 0 | **100.0%** |

## 二、新增预处理实现
- `strip_sha_lines(text)`：剥 `^artifact_sha256:` 行；`judge(strip_sha=True)` 走补全语义。
- 依据 `data/ev_matrix_rule_definition_v2.md` 的 P2（64 位 sha 数字片段被 `\d{10,}` 锚误收）。

## 三、历史分歧卡（P1-only 相对官方误放行）

| 卡 | 官方 | 615 自然实现 |
|---|---|---|
| `evidence/conc/EV-CONC-001.md` | UNBACKED | BACKED |
| `evidence/conc/EV-CONC-002.md` | UNBACKED | BACKED |
| `evidence/mem/EV-MEM-001.md` | UNBACKED | BACKED |
| `evidence/mem/EV-MEM-039.md` | UNBACKED | BACKED |
| `evidence/mem/EV-MEM-042.md` | UNBACKED | BACKED |
| `evidence/mem/EV-MEM-043.md` | UNBACKED | BACKED |

- 与历史记录 6 张分歧卡**完全吻合**：✅

## 四、仍存在的分歧

- 补全语义下分歧 **0** 条（无）

## 五、边界

- 未修改 `gate_engine.py`；未改 `evidence/`；第二实现只做对比，不替换官方。

