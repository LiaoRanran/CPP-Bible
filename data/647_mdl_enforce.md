# 647 B5 · MDL 规则准入**真上岗**（不过 MDL 不予上线）

- 当前模式：**enforce**（enforce = 不过不给上线；shadow = 一律放行 + 附建议）
- 判据（沿用 642）：编码长度 `savings > cost` · 热力图覆盖 · 豁免率 < 0.3 · 已在册 ⇒ 拒绝更新

## 一、准入实跑（候选为**合成**，非真实提案）

- 候选：**6**；结论分布 `{'ADMIT': 1, 'REJECT_编码长度': 1, 'PENDING_HUMAN': 1, 'REJECT_豁免率': 1, 'REFUSE_已有规则': 1, 'REJECT_热力图缺失': 1}`
- **准予进候选通道**：**1**；**被拒**：**5**

| 候选规则 | 结论 | 是否放行 | 理由 |
|---|---|---|---|
| `CAND-SHORT-001` | **ADMIT** | ✅ | 长度 OK（savings 531.9 > cost 184）· 豁免率 0.1 < 0.3 |
| `CAND-LONG-001` | **REJECT_编码长度** | ⛔ 拒绝 | savings(531.9) ≤ cost(2056) |
| `CAND-NODATA-001` | **PENDING_HUMAN** | ⛔ 拒绝 | 无豁免率数据（提案人未声明且热力图无记录）⇒ 需人补，不代决 |
| `CAND-HIGH-EXEMPT-001` | **REJECT_豁免率** | ⛔ 拒绝 | 豁免率 0.85 ≥ 阈值 0.3 |
| `ATOM-REL-TARGET-HC` | **REFUSE_已有规则** | ⛔ 拒绝 | 只对新规则准入；现有规则**不改不删** |
| `CAND-NEWDIR-X` | **REJECT_热力图缺失** | ⛔ 拒绝 | 不在 VFDR 热力图（65 条在册）或零触达 ⇒ samples_explained=0 ⇒ 必 reject |

### 1.1 合成三档验证（enforce 下）

| 候选 | 结论 | 期望放行 | 实际 | 通过 |
|---|---|---|---|---|
| `CAND-SHORT-001` | ADMIT | True | True | ✅ |
| `CAND-LONG-001` | REJECT_编码长度 | False | False | ✅ |
| `CAND-NODATA-001` | PENDING_HUMAN | False | False | ✅ |
| `CAND-HIGH-EXEMPT-001` | REJECT_豁免率 | False | False | ✅ |
| `ATOM-REL-TARGET-HC` | REFUSE_已有规则 | False | False | ✅ |

## 二、enforce vs shadow

| 模式 | 不过 MDL 时的行为 |
|---|---|
| **enforce** | `published=False` ⇒ **不予上线**（附拒绝理由） |
| shadow（回滚） | `published=True` + 附建议（**642 行为**） |

- 落盘（`--publish`）：`data/647_published_rules.json`（**被拒候选也保留**）

## 三、误判风险评估 + 回滚方案

| 风险 | 触发条件 | 回滚动作 |
|---|---|---|
| 编码长度/豁免率是**启发式** ⇒ 可能误杀好规则 | 被拒候选事后证明能拦到真实攻击 | `QUEYI_PROTECTOR_MODE=shadow` 一键退回只出建议；候选结论全留档（含 savings/cost/理由），人可改判 |
| **缺数据被判 PENDING_HUMAN** ⇒ 也可能挡住真正的新方向 | 新方向规则长期无热力图样本 | 先补攻击样本让热力图可算，再重提；人可显式豁免（本批不自动化） |
| 本批候选是**合成**的 ⇒ 真实提案未被真正拦过 | 有人把「已拒绝上线」当成对待真实提案的既有结论 | 真实提案到来时重跑 `--report`（判据是确定性的，结论可复算） |

## 诚实登记

1. **候选是合成的**：本批**没有真实新规则提案** ⇒ 「被拒上线」实际拦的是合成候选；
2. **判据是启发式**（642 已登记）⇒ 可能误杀；被拒候选**全部保留**可改判；
3. **现有 67 条规则零改动**（本模块只读 gate_engine）；
4. `published=True` 只表示**准予进候选通道**，**不等于已上线生效**（真正入库由人裁决）；
5. **不写 `gate_engine.py`**：本模块没有任何修改规则库的代码路径。
