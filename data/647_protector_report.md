# 647 B5(联调) · 五个保护器**真上岗**联调（前后对比 + 不打架 + 可回滚）

- 当前模式：**enforce**（`QUEYI_PROTECTOR_MODE`；`--rollback` 一键回 642 灰度）
- 标记键：**17** 个（键空间互不重叠=True，对象层互不相同=True）

## 一、上岗前后对比（enforce 强制量 vs 642 灰度标记量）

| 保护器 | enforce（647 真上岗） | shadow（642 灰度） |
|---|---|---|
| **B1** 单卡判决 | `{"卡片": 23, "高置信动作数": 1, "判决态被改变（enforce 强制量）": 1, "动作分布": {"pass": 21, "block": 1, "warn": 1}}` | `{"卡片": 23, "高置信动作数": 1, "判决态被改变（enforce 强制量）": 0, "动作分布": {"pass": 21, "block": 1, "warn": 1}}` |
| **B2** 人审队列项 | `{"队列": 65, "冻结不入队（enforce 强制量）": 0, "积压警报": false, "占用%": 65.0}` | `{"队列": 65, "冻结不入队（enforce 强制量）": 0, "积压警报": false, "占用%": 65.0}` |
| **B3** 人审条目 | `{"新判决": 3, "强制盲化（enforce 强制量）": 3, "被盲化总数": 3, "生效方法分布": {"ITEM_BLIND": 3}}` | `{"新判决": 3, "强制盲化（enforce 强制量）": 0, "被盲化总数": 1, "生效方法分布": {"BATCH_AUTH": 1, "ITEM_OPEN": 1, "ITEM_BLIND": 1}}` |
| **B4** 规则 | `{"规则": 67, "降级（enforce 强制量）": 3, "暂停（enforce 强制量）": 2, "有样本": 67}` | `{"规则": 67, "降级（enforce 强制量）": 0, "暂停（enforce 强制量）": 0, "有样本": 67}` |
| **B5** 规则候选 | `{"候选": 6, "不放行（enforce 强制量）": 5, "结论分布": {"ADMIT": 1, "REJECT_编码长度": 1, "PENDING_HUMAN": 1, "REJECT_豁免率": 1, "REFUSE_已有规则": 1, "REJECT_热力图缺失": 1}}` | `{"候选": 6, "不放行（enforce 强制量）": 0, "结论分布": {"ADMIT": 1, "REJECT_编码长度": 1, "PENDING_HUMAN": 1, "REJECT_豁免率": 1, "REFUSE_已有规则": 1, "REJECT_热力图缺失": 1}}` |

## 二、不冲突 / 不重复拦截

| 保护器 | 作用对象层 | 标记键空间 |
|---|---|---|
| B1 | 单卡判决 | `conflict_flag`, `conflict_types`, `conflict_strength`, `conflict_action` |
| B2 | 人审队列项 | `queued_pending`, `frozen`, `frozen_enforced`, `enqueued`, `priority_out` |
| B3 | 人审条目 | `blind_state`, `masked`, `residual` |
| B4 | 规则 | `known_error_rate`, `effective_severity`, `rule_active` |
| B5 | 规则候选 | `mdl_decision`, `mdl_published` |

- 五个对象的**集合两两不相交**（卡判决 / 队列项 / 人审条目 / 规则 / 规则候选）⇒ **同一个东西不会被两个保护器同时处置**；
- 标记键空间互不重叠 ⇒ 叠加不互相覆盖；同名不同值 ⇒ `MarkConflictError`（不静默覆盖）；
- `rollback_marks()` 按保护器精确摘除 ⇒ 逐个回滚到底为空。

## 三、零漂移实证（保护器**不动生产工件**）

| 生产工件 | 联调前 | 联调后 | 相同 |
|---|---|---|---|
| `gate_engine.py` | `03cd20dcdbee…` | `03cd20dcdbee…` | ✅ |
| `atom_evidence_replay.py` | `4b142e68a97a…` | `4b142e68a97a…` | ✅ |
| `poison_drill.py` | `37f638004c4d…` | `37f638004c4d…` | ✅ |
| `toolchain.py` | `5920bff6af16…` | `5920bff6af16…` | ✅ |
| `cppbible.py` | `4454db9b4992…` | `4454db9b4992…` | ✅ |
| `decision_ledger` | `ec8cbf5cca2d…` | `ec8cbf5cca2d…` | ✅ |
| `authority_log` | `01b17c520cde…` | `01b17c520cde…` | ✅ |
| `human_queue` | `79c88f6ff7f5…` | `79c88f6ff7f5…` | ✅ |
| `transparency_log` | `03d828216363…` | `03d828216363…` | ✅ |
| `verified_cards` | `078616367855…` | `078616367855…` | ✅ |

- **漂移项：零**

## 四、一键回滚（实测）

- `protector_mode_647.rollback()` ⇒ 模式 enforce → **shadow**
- 回滚后**强制量是否归零**：**True**
- 回滚后实测：`{"B1": {"卡片": 23, "高置信动作数": 1, "判决态被改变（enforce 强制量）": 0, "动作分布": {"pass": 21, "block": 1, "warn": 1}}, "B2": {"队列": 65, "冻结不入队（enforce 强制量）": 0, "积压警报": false, "占用%": 65.0}, "B3": {"新判决": 3, "强制盲化（enforce 强制量）": 0, "被盲化总数": 1, "生效方法分布": {"BATCH_AUTH": 1, "ITEM_OPEN": 1, "ITEM_BLIND": 1}}, "B4": {"规则": 67, "降级（enforce 强制量）": 0, "暂停（enforce 强制量）": 0, "有样本": 67}, "B5": {"候选": 6, "不放行（enforce 强制量）": 0, "结论分布": {"ADMIT": 1, "REJECT_编码长度": 1, "PENDING_HUMAN": 1, "REJECT_豁免率": 1, "REFUSE_已有规则": 1, "REJECT_热力图缺失": 1}}}`

## 诚实登记

1. **联调通过 ≠ 保护器有效**：本模块只证明「能同时上岗 + 不打架 + 可回滚 + 不动生产工件」，**不证明**拦截后更安全（需真实运行数据）；
2. **真实数据上多数强制量为 0**（无高置信冲突卡、队列无「低」项、无 >50% 规则、候选为合成）⇒ 机制由**合成输入**验证，报告已逐项标注；
3. **B1 会真的改判**（内核态 → fail），是五者中唯一直接改判决态的 —— 风险最高；
4. **零漂移的覆盖范围**：5 CORE_TOOLS + 452 账本 + 权威日志 + 人审队列 + 透明日志 + verified 卡清单；**不含**受控目录全量（那是门禁的另一项）；
5. **回滚文件是运行期状态**（`data/647_protector_mode.json`），审计时必须一并记录当前模式。
